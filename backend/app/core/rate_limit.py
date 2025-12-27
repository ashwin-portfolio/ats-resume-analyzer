"""
Rate limiting decorator for FastAPI endpoints.
Uses slowapi to apply rate limits based on configuration.
"""
from functools import wraps
from typing import Callable, Any
from fastapi import Request, HTTPException
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


def rate_limit(limit: str) -> Callable:
    """
    Decorator to apply rate limiting to FastAPI endpoints.
    
    Args:
        limit: Rate limit string (e.g., "10/minute", "100/hour")
    
    Returns:
        Decorator function that applies rate limiting
    
    Usage:
        @rate_limit("10/minute")
        async def my_endpoint(request: Request):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Find Request object in args or kwargs
            request: Request | None = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request is None:
                request = kwargs.get('request')
            
            if request is None:
                # If no request found, call function without rate limiting
                # This shouldn't happen in normal FastAPI usage
                return await func(*args, **kwargs)
            
            # Get limiter from app state
            limiter: Limiter = request.app.state.limiter
            
            # Check rate limit using slowapi's limit decorator pattern
            # slowapi uses limiter.limit() which returns a decorator
            # We need to apply it dynamically by wrapping the function
            if limiter.enabled:
                # Create a rate-limited version of the function
                # slowapi's limiter.limit() expects to be used as a decorator
                # We'll use it to create a rate-limited wrapper
                limited_func = limiter.limit(limit)(func)
                
                # Call the rate-limited function
                # Note: slowapi's limit decorator expects the request as first arg
                try:
                    return await limited_func(*args, **kwargs)
                except RateLimitExceeded:
                    raise HTTPException(
                        status_code=429,
                        detail="Rate limit exceeded. Please try again later."
                    )
            
            # Call the original function if rate limiting is disabled
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator
