"""
Configuration settings for the application.
Uses environment variables for sensitive data.
"""
from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Create a .env file in backend/ directory with these values.
    """
    # API Settings
    API_VERSION: str = "1.0.0"
    API_TITLE: str = "ATS Resume Analyzer"
    DEBUG: bool = True
    
    # Database Settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/ats_db"
    
    # ML Model Settings
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    MODEL_CACHE_DIR: str = "./model_cache"
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".pdf", ".docx", ".doc"]
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "https://*.vercel.app"
    ]
    
    # Keyword Extraction Settings
    MIN_KEYWORD_LENGTH: int = 2
    MAX_KEYWORDS: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

