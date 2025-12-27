"""
Text cleaning and preprocessing utilities.
Handles normalization, tokenization, and text cleaning for resume analysis.
"""
import re
from typing import List
import unicodedata


def normalize_text(text: str) -> str:
    """
    Normalize text by removing extra whitespace and normalizing unicode.
    
    Args:
        text: Raw text input
        
    Returns:
        Normalized text string
    """
    if not text:
        return ""
    
    # Normalize unicode characters (e.g., convert special quotes to regular quotes)
    text = unicodedata.normalize('NFKD', text)
    
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def clean_text(text: str) -> str:
    """
    Clean text by removing special characters while preserving structure.
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    
    # Remove non-printable characters except newlines and tabs
    text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
    
    # Normalize line breaks
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\r', '\n', text)
    
    # Remove excessive line breaks (more than 2 consecutive)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Normalize whitespace
    text = normalize_text(text)
    
    return text


def extract_sentences(text: str) -> List[str]:
    """
    Extract sentences from text.
    
    Args:
        text: Input text
        
    Returns:
        List of sentences
    """
    if not text:
        return []
    
    # Simple sentence splitting (can be improved with NLTK if needed)
    # Split on sentence-ending punctuation followed by space or newline
    sentences = re.split(r'[.!?]+\s+', text)
    
    # Filter out empty sentences and normalize
    sentences = [normalize_text(s) for s in sentences if normalize_text(s)]
    
    return sentences


def extract_words(text: str, min_length: int = 2) -> List[str]:
    """
    Extract words from text, filtering by minimum length.
    
    Args:
        text: Input text
        min_length: Minimum word length to include
        
    Returns:
        List of words (lowercased)
    """
    if not text:
        return []
    
    # Extract words (alphanumeric sequences)
    words = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
    
    # Filter by minimum length
    words = [w for w in words if len(w) >= min_length]
    
    return words


def remove_stopwords_custom(words: List[str]) -> List[str]:
    """
    Remove common stopwords that are not useful for keyword extraction.
    Custom implementation without external dependencies.
    
    Args:
        words: List of words
        
    Returns:
        List of words with stopwords removed
    """
    # Common English stopwords
    stopwords = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have',
        'had', 'what', 'said', 'each', 'which', 'their', 'time', 'if',
        'up', 'out', 'many', 'then', 'them', 'these', 'so', 'some', 'her',
        'would', 'make', 'like', 'into', 'him', 'has', 'two', 'more', 'very',
        'after', 'words', 'long', 'than', 'first', 'been', 'call', 'who',
        'oil', 'sit', 'now', 'find', 'down', 'day', 'did', 'get', 'come',
        'made', 'may', 'part'
    }
    
    return [w for w in words if w not in stopwords]


def preprocess_text(text: str) -> str:
    """
    Full text preprocessing pipeline.
    
    Args:
        text: Raw input text
        
    Returns:
        Preprocessed text ready for analysis
    """
    if not text:
        return ""
    
    # Clean and normalize
    text = clean_text(text)
    text = normalize_text(text)
    
    return text




