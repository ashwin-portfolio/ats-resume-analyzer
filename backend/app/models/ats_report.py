"""
ATS Report database model.
Stores resume analysis results and recommendations.
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from uuid import uuid4


class ATSReportBase(SQLModel):
    """Base schema for ATS Report"""
    ats_score: float = Field(..., ge=0, le=100, description="Overall ATS score (0-100)")
    skill_match_percentage: float = Field(..., ge=0, le=100, description="Skill match percentage (0-100)")
    summary: str = Field(..., description="Brief analysis summary")
    resume_filename: Optional[str] = Field(None, description="Original resume filename")
    job_description: Optional[str] = Field(None, description="Job description used for analysis")


class ATSReport(ATSReportBase, table=True):
    """
    ATS Report database model.
    
    Stores complete analysis results including:
    - ATS score and skill match percentage
    - Summary and recommendations
    - Matched and missing keywords (via relationships)
    - Timestamps and metadata
    """
    __tablename__ = "ats_reports"
    
    # Primary key
    id: Optional[str] = Field(
        default_factory=lambda: f"rpt_{uuid4().hex[:12]}",
        primary_key=True,
        description="Unique report identifier"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Report creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Last update timestamp"
    )
    
    # Relationships (forward reference - will be resolved at runtime)
    matched_keywords: List["Keyword"] = Relationship(
        back_populates="report",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    
    class Config:
        """Pydantic config"""
        from_attributes = True


class ATSReportCreate(ATSReportBase):
    """Schema for creating a new ATS report"""
    pass


class ATSReportRead(ATSReportBase):
    """Schema for reading an ATS report"""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    matched_keywords: List[dict] = []  # Will be populated from Keyword model

