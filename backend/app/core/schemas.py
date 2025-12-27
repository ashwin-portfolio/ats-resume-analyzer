"""
Pydantic schemas for request/response validation.
Ensures type safety and automatic API documentation.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


# ===============================
# HEALTH CHECK SCHEMAS
# ===============================
class HealthCheckResponse(BaseModel):
    """Response schema for health check endpoint"""
    status: str = Field(..., description="Service status (healthy/degraded/unhealthy)")
    version: str = Field(..., description="API version")
    service: str = Field(..., description="Service name")
    ml_model_loaded: bool = Field(..., description="ML model loading status")
    database_connected: Optional[bool] = Field(None, description="Database connection status")


# ===============================
# ATS ANALYSIS SCHEMAS
# ===============================
class ATSAnalysisResponse(BaseModel):
    """Response schema for ATS analysis results"""
    ats_score: float = Field(..., description="Overall ATS score (0-100)", ge=0, le=100)
    skill_match_percentage: float = Field(..., description="Skill match percentage (0-100)", ge=0, le=100)
    matched_keywords: List[str] = Field(..., description="Keywords found in both resume and JD")
    missing_keywords: List[str] = Field(..., description="Keywords in JD but missing from resume")
    summary: str = Field(..., description="Brief analysis summary")
    recommendations: List[str] = Field(..., description="Actionable recommendations")
    report_id: str = Field(..., description="Unique report identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ats_score": 75.5,
                "skill_match_percentage": 68.3,
                "matched_keywords": ["Python", "FastAPI", "React", "PostgreSQL"],
                "missing_keywords": ["Docker", "Kubernetes", "AWS"],
                "summary": "Strong alignment with job requirements...",
                "recommendations": ["Add Docker experience", "Highlight cloud platforms"],
                "report_id": "rpt_123456"
            }
        }


# ===============================
# REPORT SCHEMAS
# ===============================
class ReportDetail(BaseModel):
    """Detailed report schema with metadata"""
    report_id: str
    ats_score: float
    skill_match_percentage: float
    matched_keywords: List[str]
    missing_keywords: List[str]
    summary: str
    recommendations: List[str]
    created_at: Optional[datetime] = None
    resume_filename: Optional[str] = None
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models (Pydantic v2)


class ReportListResponse(BaseModel):
    """Response schema for listing multiple reports"""
    total: int = Field(..., description="Total number of reports")
    reports: List[ReportDetail] = Field(..., description="List of reports")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Maximum records returned")

