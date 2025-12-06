"""
API Routes for ATS Resume Analyzer.
Handles all endpoints for resume analysis, health checks, and reports.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import logging

from app.core.schemas import (
    ATSAnalysisRequest,
    ATSAnalysisResponse,
    HealthCheckResponse,
    ReportListResponse,
    ReportDetail
)
from app.ml import is_model_loaded
from app.models.database import get_db
from app.models.ats_report import ATSReport, ATSReportCreate
from app.models.keyword import Keyword, KeywordCreate, KeywordType
from sqlalchemy.orm import Session
from sqlalchemy import desc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()


# ===============================
# HEALTH CHECK ENDPOINT
# ===============================
@router.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API status.
    
    Returns:
        HealthCheckResponse: API status and version information
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "ATS Resume Analyzer",
        "ml_model_loaded": is_model_loaded()  # Check actual model status
    }


# ===============================
# ATS ANALYSIS ENDPOINT
# ===============================
@router.post("/analyze", response_model=ATSAnalysisResponse, tags=["Analysis"])
async def analyze_resume(
    resume_file: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    job_description: str = Form(..., description="Job description text"),
    db: Session = Depends(get_db)
):
    """
    Analyze resume against job description and generate ATS report.
    
    Args:
        resume_file: Uploaded resume file (PDF or DOCX format)
        job_description: Target job description text
        db: Database session (injected via dependency)
    
    Returns:
        ATSAnalysisResponse: Complete ATS analysis report including:
            - ATS score (0-100)
            - Skill match percentage
            - Matched keywords
            - Missing keywords
            - Recommendations
            - Summary
    
    Raises:
        HTTPException: If file format is invalid or processing fails
    """
    try:
        logger.info(f"📄 Received resume: {resume_file.filename}")
        
        # Validate file type
        allowed_extensions = [".pdf", ".docx", ".doc"]
        
        # Extract file extension safely
        filename_lower = resume_file.filename.lower()
        if "." not in filename_lower:
            raise HTTPException(
                status_code=400,
                detail="File must have an extension. Allowed: " + ", ".join(allowed_extensions)
            )
        
        file_extension = "." + filename_lower.split(".")[-1]
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Read file content
        file_content = await resume_file.read()
        logger.info(f"📊 File size: {len(file_content)} bytes")
        
        # TODO: Extract text from resume
        # from app.utils.file_parser import extract_text_from_file
        # resume_text = extract_text_from_file(file_content, file_extension)
        
        # TODO: Perform ATS analysis
        # from app.ml.analyzer import analyze_resume_text
        # analysis_result = analyze_resume_text(resume_text, job_description)
        
        # TODO: Extract text from resume and perform real analysis
        # For now, use mock data but save to database
        
        # Create mock analysis result
        ats_score = 75.5
        skill_match = 68.3
        matched_keywords_list = [
            "Python", "FastAPI", "React", "PostgreSQL", 
            "Machine Learning", "REST API"
        ]
        missing_keywords_list = [
            "Docker", "Kubernetes", "AWS", "CI/CD", "TensorFlow"
        ]
        summary_text = "Your resume shows strong alignment with the job requirements, particularly in backend development and API design. Consider adding more keywords related to DevOps and cloud technologies."
        recommendations_list = [
            "Add Docker and containerization experience to your resume",
            "Include specific cloud platform experience (AWS/Azure/GCP)",
            "Highlight CI/CD pipeline implementation",
            "Mention any experience with scalable system design",
            "Add metrics and quantifiable achievements"
        ]
        
        # Create ATS Report in database
        report_data = ATSReportCreate(
            ats_score=ats_score,
            skill_match_percentage=skill_match,
            summary=summary_text,
            resume_filename=resume_file.filename,
            job_description=job_description
        )
        
        # Create report instance
        db_report = ATSReport(**report_data.dict())
        db.add(db_report)
        db.flush()  # Get the ID without committing
        
        # Add matched keywords
        for keyword_text in matched_keywords_list:
            keyword = Keyword(
                keyword=keyword_text,
                keyword_type=KeywordType.MATCHED,
                report_id=db_report.id
            )
            db.add(keyword)
        
        # Add missing keywords
        for keyword_text in missing_keywords_list:
            keyword = Keyword(
                keyword=keyword_text,
                keyword_type=KeywordType.MISSING,
                report_id=db_report.id
            )
            db.add(keyword)
        
        # Commit all changes
        db.commit()
        db.refresh(db_report)
        
        logger.info(f"✅ Analysis completed and saved to database. Report ID: {db_report.id}")
        
        # Return response
        return {
            "ats_score": db_report.ats_score,
            "skill_match_percentage": db_report.skill_match_percentage,
            "matched_keywords": matched_keywords_list,
            "missing_keywords": missing_keywords_list,
            "summary": db_report.summary,
            "recommendations": recommendations_list,
            "report_id": db_report.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error during analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing resume: {str(e)}"
        )


# ===============================
# GET REPORT BY ID
# ===============================
@router.get("/report/{report_id}", response_model=ATSAnalysisResponse, tags=["Reports"])
async def get_report(
    report_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a previously generated ATS report by ID.
    
    Args:
        report_id: Unique identifier for the report
        db: Database session
    
    Returns:
        ATSAnalysisResponse: Complete report data
    
    Raises:
        HTTPException: If report not found
    """
    try:
        # Query database for report
        report = db.query(ATSReport).filter(ATSReport.id == report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Get keywords for this report
        keywords = db.query(Keyword).filter(Keyword.report_id == report_id).all()
        matched_keywords = [kw.keyword for kw in keywords if kw.keyword_type == KeywordType.MATCHED]
        missing_keywords = [kw.keyword for kw in keywords if kw.keyword_type == KeywordType.MISSING]
        
        # Generate recommendations (for now, simple mock)
        recommendations = [
            "Add Docker and containerization experience to your resume",
            "Include specific cloud platform experience (AWS/Azure/GCP)",
            "Highlight CI/CD pipeline implementation"
        ]
        
        return {
            "ats_score": report.ats_score,
            "skill_match_percentage": report.skill_match_percentage,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
            "summary": report.summary,
            "recommendations": recommendations,
            "report_id": report.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching report: {str(e)}"
        )


# ===============================
# LIST ALL REPORTS (OPTIONAL)
# ===============================
@router.get("/reports", response_model=ReportListResponse, tags=["Reports"])
async def list_reports(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List all ATS reports with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
    
    Returns:
        ReportListResponse: Paginated list of reports
    """
    try:
        # Get total count
        total = db.query(ATSReport).count()
        
        # Get paginated reports (newest first)
        reports = db.query(ATSReport).order_by(desc(ATSReport.created_at)).offset(skip).limit(limit).all()
        
        # Convert to response format
        report_list = []
        for report in reports:
            # Get keywords for each report
            keywords = db.query(Keyword).filter(Keyword.report_id == report.id).all()
            matched_keywords = [kw.keyword for kw in keywords if kw.keyword_type == KeywordType.MATCHED]
            missing_keywords = [kw.keyword for kw in keywords if kw.keyword_type == KeywordType.MISSING]
            
            report_list.append(ReportDetail(
                report_id=report.id,
                ats_score=report.ats_score,
                skill_match_percentage=report.skill_match_percentage,
                matched_keywords=matched_keywords,
                missing_keywords=missing_keywords,
                summary=report.summary,
                recommendations=[],  # TODO: Store recommendations in DB
                created_at=report.created_at,
                resume_filename=report.resume_filename
            ))
        
        return {
            "total": total,
            "reports": report_list,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"❌ Error listing reports: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing reports: {str(e)}"
        )

