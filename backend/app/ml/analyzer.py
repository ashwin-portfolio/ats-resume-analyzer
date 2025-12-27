"""
Main ATS analysis logic.
Combines text extraction, keyword analysis, and semantic similarity.
"""
import logging
from typing import Dict, List, Tuple
import numpy as np

from app.ml.embeddings import (
    load_embedding_model,
    get_embedding_model,
    compute_embeddings,
    compute_similarity
)
from app.ml.keyword_extractor import (
    extract_keywords_tfidf,
    calculate_keyword_match_score
)
from app.utils.text_cleaner import preprocess_text
from app.core.config import settings

logger = logging.getLogger(__name__)


def analyze_resume_text(
    resume_text: str,
    job_description: str,
    model=None
) -> Dict:
    """
    Perform comprehensive ATS analysis on resume text against job description.
    
    Args:
        resume_text: Extracted resume text
        job_description: Job description text
        model: Optional pre-loaded embedding model
        
    Returns:
        Dictionary containing:
            - ats_score: Overall ATS score (0-100)
            - skill_match_percentage: Skill match percentage (0-100)
            - matched_keywords: List of matched keywords
            - missing_keywords: List of missing keywords
            - summary: Analysis summary
            - recommendations: List of improvement recommendations
    """
    try:
        logger.info("🔍 Starting ATS analysis...")
        
        # Preprocess texts
        resume_clean = preprocess_text(resume_text)
        jd_clean = preprocess_text(job_description)
        
        if not resume_clean or not jd_clean:
            raise ValueError("Resume or job description text is empty after preprocessing")
        
        # Load model if not provided
        if model is None:
            model = get_embedding_model()
            if model is None:
                logger.warning("Model not loaded, loading now...")
                model = load_embedding_model()
        
        # Extract keywords
        logger.info("📝 Extracting keywords...")
        matched_keywords, missing_keywords = extract_keywords_tfidf(
            resume_clean,
            jd_clean,
            max_keywords=settings.MAX_KEYWORDS
        )
        
        # Ensure we have lists (not None)
        matched_keywords = matched_keywords if matched_keywords is not None else []
        missing_keywords = missing_keywords if missing_keywords is not None else []
        
        # Calculate keyword match score
        keyword_match_score = calculate_keyword_match_score(
            matched_keywords,
            missing_keywords
        )
        
        # Compute semantic similarity using embeddings
        logger.info("🧠 Computing semantic similarity...")
        resume_embeddings = compute_embeddings([resume_clean], model)
        jd_embeddings = compute_embeddings([jd_clean], model)
        
        # Validate embeddings were computed successfully
        if not resume_embeddings or len(resume_embeddings) == 0:
            raise ValueError("Failed to compute resume embeddings")
        if not jd_embeddings or len(jd_embeddings) == 0:
            raise ValueError("Failed to compute job description embeddings")
        
        resume_embedding = resume_embeddings[0]
        jd_embedding = jd_embeddings[0]
        
        semantic_similarity = compute_similarity(resume_embedding, jd_embedding)
        semantic_score = semantic_similarity * 100  # Convert to percentage
        
        # Calculate overall ATS score
        # Weighted combination: 60% keyword match, 40% semantic similarity
        ats_score = (keyword_match_score * 0.6) + (semantic_score * 0.4)
        ats_score = round(ats_score, 2)
        
        # Ensure score is between 0 and 100
        ats_score = max(0.0, min(100.0, ats_score))
        
        # Generate summary
        summary = generate_summary(
            ats_score,
            keyword_match_score,
            semantic_score,
            len(matched_keywords),
            len(missing_keywords)
        )
        
        # Generate recommendations
        recommendations = generate_recommendations(
            missing_keywords,
            ats_score,
            keyword_match_score
        )
        
        logger.info(f"✅ Analysis complete! ATS Score: {ats_score}")
        
        return {
            "ats_score": ats_score,
            "skill_match_percentage": round(keyword_match_score, 2),
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
            "summary": summary,
            "recommendations": recommendations
        }
        
    except Exception as e:
        logger.error(f"❌ Error during analysis: {e}")
        raise RuntimeError(f"Analysis failed: {str(e)}")


def generate_summary(
    ats_score: float,
    keyword_score: float,
    semantic_score: float,
    matched_count: int,
    missing_count: int
) -> str:
    """
    Generate a human-readable summary of the analysis.
    
    Args:
        ats_score: Overall ATS score
        keyword_score: Keyword match score
        semantic_score: Semantic similarity score
        matched_count: Number of matched keywords
        missing_count: Number of missing keywords
        
    Returns:
        Summary text
    """
    if ats_score >= 80:
        quality = "excellent"
        advice = "Your resume is well-aligned with the job requirements."
    elif ats_score >= 65:
        quality = "good"
        advice = "Your resume shows strong alignment, with room for improvement."
    elif ats_score >= 50:
        quality = "moderate"
        advice = "Your resume needs significant improvements to better match the job requirements."
    else:
        quality = "needs improvement"
        advice = "Your resume requires substantial updates to align with the job requirements."
    
    summary = (
        f"Your resume has a {quality} ATS score of {ats_score:.1f}%. "
        f"{advice} "
        f"You matched {matched_count} keywords and are missing {missing_count} important keywords. "
        f"Your semantic similarity score is {semantic_score:.1f}%, indicating "
        f"{'strong' if semantic_score >= 70 else 'moderate' if semantic_score >= 50 else 'weak'} "
        f"alignment with the job description's overall content and requirements."
    )
    
    return summary


def generate_recommendations(
    missing_keywords: List[str],
    ats_score: float,
    keyword_score: float
) -> List[str]:
    """
    Generate actionable recommendations based on analysis.
    
    Args:
        missing_keywords: List of missing keywords
        ats_score: Overall ATS score
        keyword_score: Keyword match score
        
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    # Keyword-based recommendations
    if missing_keywords:
        top_missing = missing_keywords[:5]
        if len(top_missing) == 1:
            recommendations.append(
                f"Add '{top_missing[0]}' to your resume to improve keyword matching."
            )
        else:
            keywords_str = ", ".join([f"'{kw}'" for kw in top_missing[:3]])
            recommendations.append(
                f"Add these important keywords to your resume: {keywords_str}."
            )
    
    # Score-based recommendations
    if ats_score < 50:
        recommendations.append(
            "Consider restructuring your resume to better align with the job description."
        )
        recommendations.append(
            "Highlight relevant skills and experiences more prominently."
        )
    elif ats_score < 70:
        recommendations.append(
            "Add more specific technical skills and tools mentioned in the job description."
        )
        recommendations.append(
            "Quantify your achievements with metrics and numbers where possible."
        )
    
    # General recommendations
    if keyword_score < 60:
        recommendations.append(
            "Review the job description carefully and incorporate more relevant keywords naturally."
        )
    
    if len(missing_keywords) > 10:
        recommendations.append(
            "Your resume is missing many important keywords. Consider adding a skills section."
        )
    
    # Ensure we have at least a few recommendations
    if not recommendations:
        recommendations.append(
            "Your resume is well-optimized! Continue to tailor it for each application."
        )
        recommendations.append(
            "Keep your resume updated with the latest technologies and skills."
        )
    
    return recommendations[:5]  # Limit to 5 recommendations




