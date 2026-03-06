"""
Security and production middleware.
Handles security headers, request ID tracking, and other production concerns.
"""
import uuid
import logging
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

# Context variable to store request_id for logging
request_id_context: ContextVar[str] = ContextVar('request_id', default='system')


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.
    Protects against XSS, clickjacking, MIME sniffing, and other attacks.
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Only add HSTS in production (HTTPS)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Content Security Policy (adjust based on your needs)
        # Allow self, Vercel, and common CDNs
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "  # FastAPI docs need unsafe-inline/eval
            "style-src 'self' 'unsafe-inline'; "  # Tailwind/Next.js need unsafe-inline
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp
        
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add a unique request ID to each request.
    Helps with tracing and debugging in production.
    """
    async def dispatch(self, request: Request, call_next):
        # Generate or get request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Add to request state for use in handlers
        request.state.request_id = request_id
        
        # Set in context variable for logging
        request_id_context.set(request_id)
        
        try:
            # Process request
            response = await call_next(request)
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
        finally:
            # Clear context variable after request
            request_id_context.set('system')







