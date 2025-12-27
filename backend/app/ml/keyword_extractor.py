"""
Keyword extraction using TF-IDF and text analysis.
Extracts important keywords from job descriptions and resumes.
"""
import logging
from typing import List, Dict, Tuple
import re
from collections import Counter

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
except ImportError:
    TfidfVectorizer = None

from app.utils.text_cleaner import (
    preprocess_text,
    extract_words,
    remove_stopwords_custom
)
from app.core.config import settings

logger = logging.getLogger(__name__)


def extract_keywords_tfidf(
    resume_text: str,
    job_description: str,
    max_keywords: int = None
) -> Tuple[List[str], List[str]]:
    """
    Extract keywords from resume and job description using TF-IDF.
    
    Args:
        resume_text: Resume text
        job_description: Job description text
        max_keywords: Maximum number of keywords to return
        
    Returns:
        Tuple of (matched_keywords, missing_keywords)
    """
    if TfidfVectorizer is None:
        logger.warning("scikit-learn not available, using simple keyword extraction")
        return extract_keywords_simple(resume_text, job_description, max_keywords)
    
    max_keywords = max_keywords or settings.MAX_KEYWORDS
    
    try:
        # Preprocess texts
        resume_clean = preprocess_text(resume_text)
        jd_clean = preprocess_text(job_description)
        
        # Extract words
        resume_words = extract_words(resume_clean, min_length=settings.MIN_KEYWORD_LENGTH)
        jd_words = extract_words(jd_clean, min_length=settings.MIN_KEYWORD_LENGTH)
        
        # Remove stopwords
        resume_words = remove_stopwords_custom(resume_words)
        jd_words = remove_stopwords_custom(jd_words)
        
        # Create documents for TF-IDF
        documents = [
            ' '.join(resume_words),
            ' '.join(jd_words)
        ]
        
        # Compute TF-IDF
        vectorizer = TfidfVectorizer(
            max_features=max_keywords * 2,
            ngram_range=(1, 2),  # Include unigrams and bigrams
            min_df=1,
            stop_words='english'
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(documents)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get top keywords for job description
            jd_scores = tfidf_matrix[1].toarray()[0]
            jd_keywords = [
                feature_names[i] for i in jd_scores.argsort()[-max_keywords:][::-1]
                if jd_scores[i] > 0
            ]
            
            # Get keywords that appear in both
            resume_scores = tfidf_matrix[0].toarray()[0]
            matched_keywords = []
            missing_keywords = []
            
            # Handle empty jd_keywords case
            if not jd_keywords:
                logger.warning("No keywords extracted from job description")
                return [], []
            
            for keyword in jd_keywords:
                if not keyword or not keyword.strip():
                    continue  # Skip empty keywords
                    
                keyword_idx = vectorizer.vocabulary_.get(keyword)
                if keyword_idx is not None and keyword_idx < len(resume_scores):
                    resume_score = resume_scores[keyword_idx]
                    jd_score = jd_scores[keyword_idx]
                    
                    if resume_score > 0:
                        matched_keywords.append(keyword)
                    else:
                        missing_keywords.append(keyword)
            
            # Ensure we return lists (not None)
            matched_keywords = matched_keywords[:max_keywords] if matched_keywords else []
            missing_keywords = missing_keywords[:max_keywords] if missing_keywords else []
            
            return matched_keywords, missing_keywords
            
        except ValueError as e:
            # Fallback if TF-IDF fails (e.g., empty documents)
            logger.warning(f"TF-IDF failed, using simple extraction: {e}")
            return extract_keywords_simple(resume_text, job_description, max_keywords)
            
    except Exception as e:
        logger.error(f"❌ Error in TF-IDF keyword extraction: {e}")
        return extract_keywords_simple(resume_text, job_description, max_keywords)


def extract_keywords_simple(
    resume_text: str,
    job_description: str,
    max_keywords: int = None
) -> Tuple[List[str], List[str]]:
    """
    Simple keyword extraction using word frequency analysis.
    Fallback method when TF-IDF is not available.
    
    Args:
        resume_text: Resume text
        job_description: Job description text
        max_keywords: Maximum number of keywords to return
        
    Returns:
        Tuple of (matched_keywords, missing_keywords)
    """
    max_keywords = max_keywords or settings.MAX_KEYWORDS
    
    # Preprocess and extract words
    resume_clean = preprocess_text(resume_text)
    jd_clean = preprocess_text(job_description)
    
    resume_words = extract_words(resume_clean, min_length=settings.MIN_KEYWORD_LENGTH)
    jd_words = extract_words(jd_clean, min_length=settings.MIN_KEYWORD_LENGTH)
    
    # Remove stopwords
    resume_words = remove_stopwords_custom(resume_words)
    jd_words = remove_stopwords_custom(jd_words)
    
    # Count word frequencies
    resume_word_set = set(resume_words)
    jd_word_set = set(jd_words)
    jd_word_counts = Counter(jd_words)
    
    # Find matched and missing keywords
    matched_keywords = list(resume_word_set & jd_word_set) if resume_word_set and jd_word_set else []
    missing_keywords = list(jd_word_set - resume_word_set) if jd_word_set else []
    
    # Sort by frequency in job description
    matched_keywords.sort(key=lambda x: jd_word_counts.get(x, 0), reverse=True)
    missing_keywords.sort(key=lambda x: jd_word_counts.get(x, 0), reverse=True)
    
    # Also extract technical terms (capitalized words, common tech terms)
    technical_terms = extract_technical_terms(jd_clean) if jd_clean else []
    matched_technical = [t for t in technical_terms if t and t.lower() in resume_clean.lower()] if resume_clean and technical_terms else []
    missing_technical = [t for t in technical_terms if t and t.lower() not in resume_clean.lower()] if resume_clean and technical_terms else []
    
    # Combine and deduplicate (ensure no None values)
    all_matched = list(dict.fromkeys([kw for kw in (matched_keywords + matched_technical) if kw]))
    all_missing = list(dict.fromkeys([kw for kw in (missing_keywords + missing_technical) if kw]))
    
    # Ensure we return lists (not None) and limit length
    return (all_matched[:max_keywords] if all_matched else [], 
            all_missing[:max_keywords] if all_missing else [])


def extract_technical_terms(text: str) -> List[str]:
    """
    Extract technical terms (capitalized words, acronyms, etc.) from text.
    
    Args:
        text: Input text
        
    Returns:
        List of technical terms
    """
    # Extract capitalized words (likely proper nouns, technologies, etc.)
    capitalized_words = re.findall(r'\b[A-Z][a-z]+\b', text)
    
    # Extract acronyms (all caps, 2-5 letters)
    acronyms = re.findall(r'\b[A-Z]{2,5}\b', text)
    
    # Extract words with numbers (e.g., Python3, HTML5)
    tech_with_numbers = re.findall(r'\b[A-Za-z]+\d+\b', text)
    
    # Combine and deduplicate
    technical_terms = list(dict.fromkeys(capitalized_words + acronyms + tech_with_numbers))
    
    # Filter out common non-technical words
    common_words = {'The', 'This', 'That', 'You', 'Your', 'We', 'Our', 'They', 'Their'}
    technical_terms = [t for t in technical_terms if t not in common_words]
    
    return technical_terms


def calculate_keyword_match_score(
    matched_keywords: List[str],
    missing_keywords: List[str]
) -> float:
    """
    Calculate keyword match score as a percentage.
    
    Args:
        matched_keywords: List of matched keywords
        missing_keywords: List of missing keywords
        
    Returns:
        Match score between 0 and 100
    """
    total_keywords = len(matched_keywords) + len(missing_keywords)
    
    if total_keywords == 0:
        return 0.0
    
    match_ratio = len(matched_keywords) / total_keywords
    return round(match_ratio * 100, 2)




