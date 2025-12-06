"""
Keyword database model.
Stores keywords found in resume analysis (matched and missing).
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from enum import Enum


class KeywordType(str, Enum):
    """Type of keyword"""
    MATCHED = "matched"  # Found in both resume and job description
    MISSING = "missing"  # In job description but not in resume


class KeywordBase(SQLModel):
    """Base schema for Keyword"""
    keyword: str = Field(..., index=True, description="Keyword text")
    keyword_type: KeywordType = Field(..., description="Type of keyword (matched/missing)")
    importance: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="Keyword importance score (0-1)"
    )


class Keyword(KeywordBase, table=True):
    """
    Keyword database model.
    
    Stores keywords extracted during analysis:
    - Matched keywords: Found in both resume and JD
    - Missing keywords: In JD but not in resume
    """
    __tablename__ = "keywords"
    
    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign key to ATSReport
    report_id: str = Field(foreign_key="ats_reports.id", index=True)
    
    # Relationship (forward reference - will be resolved at runtime)
    report: Optional["ATSReport"] = Relationship(back_populates="matched_keywords")
    
    class Config:
        """Pydantic config"""
        from_attributes = True


class KeywordCreate(KeywordBase):
    """Schema for creating a new keyword"""
    report_id: str


class KeywordRead(KeywordBase):
    """Schema for reading a keyword"""
    id: int
    report_id: str

