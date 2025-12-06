"""
Main FastAPI application entry point.
Handles app initialization, CORS, and route registration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.api.routes import router as api_router
from app.core.config import settings
from app.ml import set_model_loaded, set_model
from app.models.database import init_db, check_db_connection

# Initialize FastAPI app
app = FastAPI(
    title="ATS Resume Analyzer API",
    description="AI-powered Resume ATS scoring and analysis system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",  # Vercel deployment (wildcard pattern)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
async def global_exception_handler(request, exc):
    """
    Global exception handler for uncaught errors
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup.
    Load ML models, initialize database connections, etc.
    """
    print("🚀 Starting ATS Resume Analyzer API...")
    
    # Initialize database
    print("🗄️  Initializing database...")
    if check_db_connection():
        print("✅ Database connection successful!")
        # Note: Tables are created via Alembic migrations, not here
        # init_db()  # Uncomment if you want to create tables on startup (not recommended for production)
    else:
        print("⚠️  Database connection failed! Check your DATABASE_URL in .env")
    
    # Load ML models
    print("📊 Loading ML models...")
    # TODO: Load embedding model here
    # from app.ml.embeddings import load_embedding_model
    # try:
    #     model = load_embedding_model()
    #     set_model(model)
    #     set_model_loaded(True)
    #     print("✅ ML model loaded successfully!")
    # except Exception as e:
    #     print(f"⚠️  ML model not loaded: {e}")
    #     set_model_loaded(False)
    set_model_loaded(False)  # Model not yet implemented
    print("✅ API ready!")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown.
    Clean up resources, close DB connections, etc.
    """
    print("👋 Shutting down ATS Resume Analyzer API...")


# Run the application (for development only)
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )

