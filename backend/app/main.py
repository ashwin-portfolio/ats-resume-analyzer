"""
Main FastAPI application entry point.
Handles app initialization, CORS, and route registration.
"""
import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uvicorn

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.middleware import SecurityHeadersMiddleware, RequestIDMiddleware, request_id_context
from app.ml import set_model_loaded, set_model
from app.models.database import init_db, check_db_connection


class RequestIDFormatter(logging.Formatter):
    """
    Custom formatter that safely handles request_id in log records.
    Reads request_id from context variable (set by RequestIDMiddleware).
    If request_id is not available (e.g., during startup/shutdown),
    it defaults to 'system'.
    """
    def format(self, record):
        # Get request_id from context variable (set by middleware)
        # This works for async contexts and is thread-safe
        try:
            record.request_id = request_id_context.get()
        except LookupError:
            # Context variable not set (e.g., during startup/shutdown)
            record.request_id = 'system'
        return super().format(record)


# Configure structured logging
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
if settings.DEBUG:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s"

# Create handler with custom formatter
handler = logging.StreamHandler(sys.stdout)
if settings.DEBUG:
    # Use custom formatter for debug mode to handle request_id safely
    formatter = RequestIDFormatter(log_format)
else:
    formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format=log_format,
    handlers=[handler],
)

logger = logging.getLogger(__name__)


# Initialize rate limiter with Redis backend for distributed rate limiting (optional)
# For single-instance deployments, in-memory storage is sufficient
limiter = Limiter(
    key_func=get_remote_address,
    enabled=settings.RATE_LIMIT_ENABLED,
    storage_uri="memory://"  # Use in-memory storage (can be upgraded to Redis for distributed systems)
)

# Lifespan event handler (replaces deprecated @app.on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Replaces deprecated @app.on_event() handlers.
    """
    # Startup
    logger.info("🚀 Starting ATS Resume Analyzer API...")
    
    # Initialize database
    logger.info("🗄️  Initializing database...")
    if check_db_connection():
        logger.info("✅ Database connection successful!")
        # Note: Tables are created via Alembic migrations, not here
        # init_db()  # Uncomment if you want to create tables on startup (not recommended for production)
    else:
        logger.warning("⚠️  Database connection failed! Check your DATABASE_URL in .env")
    
    # Load ML models
    logger.info("📊 Loading ML models...")
    from app.ml.embeddings import load_embedding_model
    try:
        model = load_embedding_model()
        set_model(model)
        set_model_loaded(True)
        logger.info("✅ ML model loaded successfully!")
    except Exception as e:
        logger.error(f"⚠️  ML model not loaded: {e}")
        logger.warning("   The API will still work but analysis will be limited.")
        set_model_loaded(False)
    logger.info("✅ API ready!")
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("👋 Shutting down ATS Resume Analyzer API...")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="ATS Resume Analyzer API",
    description="AI-powered Resume ATS scoring and analysis system",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if settings.DEBUG else None,  # Disable redoc in production
    lifespan=lifespan  # Use lifespan instead of deprecated events
)

# Add rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add security middleware (must be before CORS)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIDMiddleware)

# CORS middleware configuration for frontend
# Separate exact origins from wildcard patterns
exact_origins = []
origin_regex_patterns = []

for origin in settings.CORS_ORIGINS:
    origin = origin.strip()
    if not origin:
        continue
    
    # Check if origin contains wildcard pattern
    if '*' in origin:
        # Convert wildcard pattern to regex
        # e.g., "https://*.vercel.app" -> r"https://.*\.vercel\.app"
        regex_pattern = origin.replace('.', r'\.').replace('*', '.*')
        origin_regex_patterns.append(regex_pattern)
    else:
        # Exact origin match
        exact_origins.append(origin)

# Combine all regex patterns into a single pattern
# FastAPI's allow_origin_regex accepts a single regex string
combined_regex = None
if origin_regex_patterns:
    # Combine multiple patterns with OR operator
    combined_regex = '|'.join(f'({pattern})' for pattern in origin_regex_patterns)

app.add_middleware(
    CORSMiddleware,
    allow_origins=exact_origins if exact_origins else ["http://localhost:3000"],
    allow_origin_regex=combined_regex,  # Dynamic regex patterns from settings
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Restrict methods
    allow_headers=["Content-Type", "Authorization", "X-Request-ID"],  # Restrict headers
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "ATS Resume Analyzer API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for uncaught errors.
    In production, hides internal error details for security.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    # Log full error details
    logger.error(
        f"Unhandled exception: {type(exc).__name__}: {str(exc)}",
        exc_info=True,
        extra={"request_id": request_id}
    )
    
    # Return user-friendly error (hide details in production)
    error_detail = str(exc) if settings.DEBUG else "An internal error occurred. Please try again later."
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": error_detail,
            "request_id": request_id
        }
    )


# Run the application (for development only)
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,  # Auto-reload only in debug mode
        log_level="debug" if settings.DEBUG else "info"
    )

