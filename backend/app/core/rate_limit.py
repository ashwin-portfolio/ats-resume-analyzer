"""
Rate limiting utilities for API endpoints.
Provides decorator-based rate limiting using slowapi.
"""
from functools import wraps
from typing import Callable
from fastapi import Request, HTTPException
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.core.config import settings


def rate_limit(limit: str):
    """
    Decorator for rate limiting endpoints.
    
    Args:
        limit: Rate limit string (e.g., "10/minute", "100/hour")
    
    Usage:
        @rate_limit("10/minute")
        async def my_endpoint(request: Request):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get request from args or kwargs
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                request = kwargs.get('request')
            
            if not request:
                # If no request found, skip rate limiting
                return await func(*args, **kwargs)
            
            # Get limiter from app state
            limiter: Limiter = request.app.state.limiter
            
            if not limiter.enabled:
                return await func(*args, **kwargs)
            
            # Check rate limit
            try:
                # Use slowapi's internal rate limit check
                key = get_remote_address(request)
                limiter.hit(limit, key)
            except RateLimitExceeded:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded: {limit}. Please try again later."
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator

