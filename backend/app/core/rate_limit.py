"""
Rate limiting helpers.

We use `slowapi` for rate limiting, but the `Limiter` instance lives in `app.main`
and is attached to `app.state.limiter`.

To avoid circular imports (`main -> routes -> rate_limit -> main`), this module
provides a lightweight `rate_limit()` decorator that retrieves the Limiter from
the current request at runtime.
"""

from __future__ import annotations

import inspect
from functools import wraps
from typing import Any, Callable, Optional, TypeVar, cast

from fastapi import Request

F = TypeVar("F", bound=Callable[..., Any])


def _extract_request(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Optional[Request]:
    """
    Attempt to find the FastAPI/Starlette Request in args/kwargs.

    We prefer `kwargs["request"]` but also support positional usage.
    """
    request = kwargs.get("request")
    if isinstance(request, Request):
        return request

    for arg in args:
        if isinstance(arg, Request):
            return arg
    return None


def rate_limit(limit: Optional[str]) -> Callable[[F], F]:
    """
    Decorator to apply SlowAPI rate limiting to a route handler.

    Usage:
        @rate_limit("10/minute")
        async def handler(request: Request, ...): ...

    If rate limiting is disabled or the limiter isn't available (e.g. tests),
    this decorator is a no-op.
    """

    def decorator(func: F) -> F:
        # If no limit is configured, behave like a no-op decorator.
        if not limit:
            return func

        wrapped_once: Optional[Callable[..., Any]] = None

        def _get_wrapped(*args: Any, **kwargs: Any) -> Callable[..., Any]:
            """
            Resolve and cache the SlowAPI-decorated function.

            If we can't locate a limiter (e.g. during tests) we fall back to the
            original function.
            """
            nonlocal wrapped_once

            if wrapped_once is not None:
                return wrapped_once

            request = _extract_request(args, kwargs)
            if request is None:
                wrapped_once = func
                return wrapped_once

            limiter_state = getattr(getattr(request, "app", None), "state", None)
            limiter = getattr(limiter_state, "limiter", None)
            if limiter is None or not getattr(limiter, "enabled", True):
                wrapped_once = func
                return wrapped_once

            # Apply SlowAPI's decorator lazily (avoids circular imports and ensures
            # app.state.limiter exists).
            wrapped_once = limiter.limit(limit)(func)
            return wrapped_once

        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any):
                wrapped = _get_wrapped(*args, **kwargs)
                result = wrapped(*args, **kwargs)
                if inspect.isawaitable(result):
                    return await result
                return result

            return cast(F, async_wrapper)

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any):
            wrapped = _get_wrapped(*args, **kwargs)
            return wrapped(*args, **kwargs)

        return cast(F, sync_wrapper)

    return decorator
