"""
Embedding model management.
Handles loading and using SentenceTransformer models for semantic similarity.
"""
import logging
from typing import Optional, List
import numpy as np

# Store import error details for better error messages
_import_error: Optional[str] = None
_import_successful: bool = False

try:
    from sentence_transformers import SentenceTransformer
    _import_successful = True
    _import_error = None
except ImportError as e:
    SentenceTransformer = None
    _import_successful = False
    _import_error = str(e)

from app.core.config import settings

logger = logging.getLogger(__name__)

# Global model instance
_model: Optional[SentenceTransformer] = None


def load_embedding_model(model_name: Optional[str] = None) -> SentenceTransformer:
    """
    Load the SentenceTransformer embedding model.
    
    Args:
        model_name: Optional model name override. Defaults to settings.EMBEDDING_MODEL_NAME
        
    Returns:
        Loaded SentenceTransformer model
        
    Raises:
        ImportError: If sentence-transformers is not installed
        RuntimeError: If model loading fails
    """
    global _model
    
    if SentenceTransformer is None:
        # Provide detailed error message with actual import error
        error_detail = _import_error if _import_error else "Unknown import error"
        error_msg = (
            f"sentence-transformers import failed: {error_detail}. "
            "This usually means:\n"
            "  1. The package is not installed: pip install sentence-transformers\n"
            "  2. You're using the wrong Python interpreter (check with: which python)\n"
            "  3. The package was installed in a different environment\n"
            "  4. Missing dependencies (torch, transformers, etc.)\n"
            f"Current import status: {'Failed' if not _import_successful else 'Unknown'}"
        )
        logger.error(f"❌ {error_msg}")
        raise ImportError(error_msg)
    
    if _model is not None:
        logger.info("✅ Using already loaded model")
        return _model
    
    model_name = model_name or settings.EMBEDDING_MODEL_NAME
    
    try:
        logger.info(f"📊 Loading embedding model: {model_name}")
        _model = SentenceTransformer(model_name, cache_folder=settings.MODEL_CACHE_DIR)
        logger.info("✅ Embedding model loaded successfully!")
        return _model
        
    except Exception as e:
        logger.error(f"❌ Failed to load embedding model: {e}")
        raise RuntimeError(f"Failed to load embedding model: {str(e)}")


def get_embedding_model() -> Optional[SentenceTransformer]:
    """
    Get the currently loaded embedding model.
    
    Returns:
        Loaded model or None if not loaded
    """
    return _model


def compute_embeddings(texts: List[str], model: Optional[SentenceTransformer] = None) -> np.ndarray:
    """
    Compute embeddings for a list of texts.
    
    Args:
        texts: List of text strings to embed
        model: Optional model instance. If None, uses global model
        
    Returns:
        Numpy array of embeddings (shape: [num_texts, embedding_dim])
        
    Raises:
        RuntimeError: If model is not loaded
    """
    if model is None:
        model = _model
    
    if model is None:
        raise RuntimeError("Embedding model not loaded. Call load_embedding_model() first.")
    
    if not texts:
        return np.array([])
    
    try:
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return embeddings
    except Exception as e:
        logger.error(f"❌ Error computing embeddings: {e}")
        raise RuntimeError(f"Failed to compute embeddings: {str(e)}")


def compute_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Compute cosine similarity between two embeddings.
    
    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector
        
    Returns:
        Similarity score between 0 and 1
    """
    # Ensure embeddings are 1D
    if embedding1.ndim > 1:
        embedding1 = embedding1.flatten()
    if embedding2.ndim > 1:
        embedding2 = embedding2.flatten()
    
    # Compute cosine similarity
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    similarity = dot_product / (norm1 * norm2)
    # Ensure similarity is between 0 and 1
    return max(0.0, min(1.0, similarity))


def compute_batch_similarity(embeddings1: np.ndarray, embeddings2: np.ndarray) -> np.ndarray:
    """
    Compute cosine similarity between two sets of embeddings.
    
    Args:
        embeddings1: First set of embeddings (shape: [n, dim])
        embeddings2: Second set of embeddings (shape: [m, dim])
        
    Returns:
        Similarity matrix (shape: [n, m])
    """
    # Normalize embeddings
    norm1 = np.linalg.norm(embeddings1, axis=1, keepdims=True)
    norm2 = np.linalg.norm(embeddings2, axis=1, keepdims=True)
    
    # Avoid division by zero
    norm1 = np.where(norm1 == 0, 1, norm1)
    norm2 = np.where(norm2 == 0, 1, norm2)
    
    embeddings1_norm = embeddings1 / norm1
    embeddings2_norm = embeddings2 / norm2
    
    # Compute cosine similarity matrix
    similarity_matrix = np.dot(embeddings1_norm, embeddings2_norm.T)
    
    # Clip to [0, 1]
    return np.clip(similarity_matrix, 0.0, 1.0)


