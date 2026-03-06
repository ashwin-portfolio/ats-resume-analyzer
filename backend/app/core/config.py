"""
Configuration settings for the application.
Uses environment variables for sensitive data.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List
from pydantic import field_validator


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
    # Note: legacy `.doc` files are not supported; use `.docx`.
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx"]
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://*.vercel.app"
    ]
    
    # Keyword Extraction Settings
    MIN_KEYWORD_LENGTH: int = 2
    MAX_KEYWORDS: int = 50
    
    # Rate Limiting Settings
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_ANALYZE: str = "10/minute"  # 10 requests per minute for /analyze
    RATE_LIMIT_DEFAULT: str = "100/minute"  # 100 requests per minute for other endpoints
    
    @field_validator('ALLOWED_EXTENSIONS', 'CORS_ORIGINS', mode='before')
    @classmethod
    def parse_list_from_env(cls, v):
        """Parse comma-separated string from .env into list, or return list as-is"""
        if isinstance(v, str):
            # Handle comma-separated values from .env
            return [item.strip() for item in v.split(',') if item.strip()]
        if isinstance(v, list):
            return v
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


# Create global settings instance
settings = Settings()

