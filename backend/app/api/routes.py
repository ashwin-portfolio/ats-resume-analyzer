"""
API Routes for ATS Resume Analyzer.
Handles all endpoints for resume analysis, health checks, and reports.
"""
import re
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Request
from typing import Optional
import logging

from app.core.schemas import (
    ATSAnalysisResponse,
    HealthCheckResponse,
    ReportListResponse,
    ReportDetail
)
from app.core.config import settings
from app.core.rate_limit import rate_limit
from app.ml import is_model_loaded
from app.models.database import get_db, check_db_connection
from app.models.ats_report import ATSReport, ATSReportCreate
from app.models.keyword import Keyword, KeywordType
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

# Configure logging
logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()


# ===============================
# HELPER FUNCTIONS
# ===============================
def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename (basename only, no path components)
    """
    if not filename:
        return "resume"
    
    # Remove any path components (prevent directory traversal)
    filename = os.path.basename(filename)
    
    # Remove or replace dangerous characters
    # Keep alphanumeric, dots, hyphens, underscores, spaces
    filename = re.sub(r'[^a-zA-Z0-9._\s-]', '', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext
    
    return filename or "resume"


def validate_report_id(report_id: str) -> bool:
    """
    Validate report ID format to prevent injection attacks.
    
    Args:
        report_id: Report ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not report_id:
        return False
    
    # Report IDs should match pattern: rpt_<hex_chars> or usr_<hex_chars>
    # Allow alphanumeric, underscores, hyphens (for UUIDs)
    pattern = r'^[a-zA-Z0-9_-]{8,64}$'
    return bool(re.match(pattern, report_id))


# ===============================
# HEALTH CHECK ENDPOINT
# ===============================
@router.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check(request: Request):
    """
    Health check endpoint to verify API status.
    Includes database and ML model status checks.
    Not rate limited (needed for monitoring).
    
    Returns:
        HealthCheckResponse: API status and version information
    """
    # Check database connection
    db_healthy = check_db_connection()
    
    # Check ML model
    ml_loaded = is_model_loaded()
    
    # Determine overall status
    status = "healthy" if (db_healthy and ml_loaded) else "degraded"
    
    return {
        "status": status,
        "version": "1.0.0",
        "service": "ATS Resume Analyzer",
        "ml_model_loaded": ml_loaded,
        "database_connected": db_healthy
    }


# ===============================
# ATS ANALYSIS ENDPOINT
# ===============================
@router.post("/analyze", response_model=ATSAnalysisResponse, tags=["Analysis"])
@rate_limit(settings.RATE_LIMIT_ANALYZE)
async def analyze_resume(
    request: Request,
    resume_file: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    job_description: str = Form(..., description="Job description text"),
    db: Session = Depends(get_db)
):
    """
    Analyze resume against job description and generate ATS report.
    Rate limited to prevent abuse (configured via settings.RATE_LIMIT_ANALYZE).
    
    Args:
        request: FastAPI request object
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
        RateLimitExceeded: If rate limit is exceeded (when enabled)
    """
    try:
        # Validate filename exists
        if not resume_file.filename:
            raise HTTPException(
                status_code=400,
                detail="File must have a filename"
            )
        
        # Sanitize filename to prevent path traversal
        sanitized_filename = sanitize_filename(resume_file.filename)
        logger.info(f"📄 Received resume: {sanitized_filename}")
        
        # Validate file type
        # Note: .doc (old format) is listed but will be rejected with helpful error message
        allowed_extensions = [".pdf", ".docx", ".doc"]
        
        # Extract file extension safely
        filename_lower = sanitized_filename.lower()
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
        
        # Validate file size
        if len(file_content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / (1024*1024):.1f}MB"
            )
        
        # Validate file is not empty
        if len(file_content) == 0:
            raise HTTPException(
                status_code=400,
                detail="File is empty"
            )
        
        # Extract text from resume (with content validation)
        from app.utils.file_parser import extract_text_from_file
        try:
            resume_text = extract_text_from_file(file_content, file_extension, validate_content=True)
            logger.info(f"✅ Extracted {len(resume_text)} characters from resume")
        except Exception as e:
            logger.error(f"❌ Error extracting text: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to extract text from file: {str(e)}"
            )
        
        # Validate extracted text is not empty
        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Resume file appears to be empty or contains no extractable text (minimum 50 characters required)"
            )
        
        # Validate job description
        job_description = job_description.strip()
        if not job_description or len(job_description) < 10:
            raise HTTPException(
                status_code=400,
                detail="Job description must be at least 10 characters long"
            )
        
        # Warn if job description is very long (will be truncated in DB)
        max_jd_length = 50000
        if len(job_description) > max_jd_length:
            logger.warning(
                f"Job description exceeds {max_jd_length} characters "
                f"({len(job_description)} chars). Will be truncated in database."
            )
        
        # Perform ATS analysis
        from app.ml.analyzer import analyze_resume_text
        from app.ml import get_model
        
        model = get_model()
        if model is None:
            logger.warning("⚠️  ML model not loaded, analysis may be limited")
            raise HTTPException(
                status_code=503,
                detail="ML model not available. Please ensure the model is loaded."
            )
        
        try:
            analysis_result = analyze_resume_text(resume_text, job_description, model)
            logger.info(f"✅ Analysis complete: ATS Score = {analysis_result['ats_score']}")
        except Exception as e:
            logger.error(f"❌ Error during analysis: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {str(e)}"
            )
        
        # Extract results with None safety
        ats_score = analysis_result.get("ats_score", 0.0)
        skill_match = analysis_result.get("skill_match_percentage", 0.0)
        matched_keywords_list = analysis_result.get("matched_keywords") or []
        missing_keywords_list = analysis_result.get("missing_keywords") or []
        summary_text = analysis_result.get("summary", "Analysis completed.")
        recommendations_list = analysis_result.get("recommendations") or []
        
        # Create ATS Report in database with transaction rollback on error
        try:
            report_data = ATSReportCreate(
                ats_score=ats_score,
                skill_match_percentage=skill_match,
                summary=summary_text,
                resume_filename=sanitized_filename,  # Use sanitized filename
                job_description=job_description[:50000]  # Truncate if too long (safety)
            )
            
            # Create report instance
            db_report = ATSReport(**report_data.model_dump())
            db.add(db_report)
            db.flush()  # Get the ID without committing
            
            # Assert that ID is set after flush (type narrowing for type checker)
            if db_report.id is None:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to generate report ID"
                )
            report_id = db_report.id
            
            # Add matched keywords (ensure list is not None and filter empty)
            if matched_keywords_list:
                for keyword_text in matched_keywords_list:
                    if keyword_text and keyword_text.strip():  # Skip empty keywords
                        # Limit length to prevent DB errors (most DBs have VARCHAR limits)
                        keyword_text_limited = keyword_text[:255] if len(keyword_text) > 255 else keyword_text
                        keyword = Keyword(
                            keyword=keyword_text_limited,
                            keyword_type=KeywordType.MATCHED,
                            report_id=report_id
                        )
                        db.add(keyword)
            
            # Add missing keywords (ensure list is not None and filter empty)
            if missing_keywords_list:
                for keyword_text in missing_keywords_list:
                    if keyword_text and keyword_text.strip():  # Skip empty keywords
                        # Limit length to prevent DB errors
                        keyword_text_limited = keyword_text[:255] if len(keyword_text) > 255 else keyword_text
                        keyword = Keyword(
                            keyword=keyword_text_limited,
                            keyword_type=KeywordType.MISSING,
                            report_id=report_id
                        )
                        db.add(keyword)
            
            # Commit all changes
            db.commit()
            db.refresh(db_report)
        except Exception as db_error:
            db.rollback()
            logger.error(f"❌ Database error: {db_error}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save report to database: {str(db_error)}"
            )
        
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
@rate_limit(settings.RATE_LIMIT_DEFAULT)
async def get_report(
    request: Request,
    report_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a previously generated ATS report by ID.
    
    Args:
        request: FastAPI request object
        report_id: Unique identifier for the report
        db: Database session
    
    Returns:
        ATSAnalysisResponse: Complete report data
    
    Raises:
        HTTPException: If report not found or invalid ID format
    """
    try:
        # Rate limiting is enforced via @rate_limit decorator
        # Validate report ID format (prevent injection attacks)
        if not validate_report_id(report_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid report ID format"
            )
        
        # Query database for report (using parameterized query - safe from SQL injection)
        report = db.query(ATSReport).filter(ATSReport.id == report_id).first()  # type: ignore
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Get keywords for this report (filter by type in query for better performance)
        # Note: SQLAlchemy column comparisons return BinaryExpression, not bool, but type checker sees bool
        matched_keywords_query = db.query(Keyword).filter(  # type: ignore
            and_(  # type: ignore
                Keyword.report_id == report_id,  # type: ignore
                Keyword.keyword_type == KeywordType.MATCHED  # type: ignore
            )
        ).all()
        matched_keywords = [kw.keyword for kw in matched_keywords_query]
        
        missing_keywords_query = db.query(Keyword).filter(  # type: ignore
            and_(  # type: ignore
                Keyword.report_id == report_id,  # type: ignore
                Keyword.keyword_type == KeywordType.MISSING  # type: ignore
            )
        ).all()
        missing_keywords = [kw.keyword for kw in missing_keywords_query]
        
        # Generate recommendations based on missing keywords
        from app.ml.analyzer import generate_recommendations
        recommendations = generate_recommendations(
            missing_keywords,
            report.ats_score,
            report.skill_match_percentage
        )
        
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
@rate_limit(settings.RATE_LIMIT_DEFAULT)
async def list_reports(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List all ATS reports with pagination.
    
    Args:
        request: FastAPI request object
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
    
    Returns:
        ReportListResponse: Paginated list of reports
    """
    try:
        # Rate limiting is enforced via slowapi middleware
        # Validate pagination parameters
        if skip < 0:
            skip = 0
        if limit < 1:
            limit = 10
        elif limit > 100:
            limit = 100  # Maximum limit to prevent excessive queries
        # Get total count
        total = db.query(ATSReport).count()
        
        # Get paginated reports (newest first)
        # Note: SQLModel columns work with desc(), type checker may show warning but runtime is correct
        reports = db.query(ATSReport).order_by(desc(ATSReport.created_at)).offset(skip).limit(limit).all()  # type: ignore
        
        # Convert to response format
        report_list = []
        for report in reports:
            # Ensure report.id is not None (type narrowing)
            if report.id is None:
                continue  # Skip reports without ID (shouldn't happen)
            current_report_id = report.id
            
            # Get keywords for each report (filter by type in query)
            # Note: SQLAlchemy column comparisons return BinaryExpression, not bool, but type checker sees bool
            matched_keywords_query = db.query(Keyword).filter(  # type: ignore
                and_(  # type: ignore
                    Keyword.report_id == current_report_id,  # type: ignore
                    Keyword.keyword_type == KeywordType.MATCHED  # type: ignore
                )
            ).all()
            matched_keywords = [kw.keyword for kw in matched_keywords_query]
            
            missing_keywords_query = db.query(Keyword).filter(  # type: ignore
                and_(  # type: ignore
                    Keyword.report_id == current_report_id,  # type: ignore
                    Keyword.keyword_type == KeywordType.MISSING  # type: ignore
                )
            ).all()
            missing_keywords = [kw.keyword for kw in missing_keywords_query]
            
            # Generate recommendations for each report
            from app.ml.analyzer import generate_recommendations
            recommendations = generate_recommendations(
                missing_keywords,
                report.ats_score,
                report.skill_match_percentage
            )
            
            report_list.append(ReportDetail(
                report_id=current_report_id,
                ats_score=report.ats_score,
                skill_match_percentage=report.skill_match_percentage,
                matched_keywords=matched_keywords,
                missing_keywords=missing_keywords,
                summary=report.summary,
                recommendations=recommendations,
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

