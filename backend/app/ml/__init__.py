"""
Machine Learning package
Contains ML models, embeddings, and analysis logic
"""

# Global flag to track if ML model is loaded
_ml_model_loaded = False
_ml_model = None


def is_model_loaded() -> bool:
    """Check if ML model is currently loaded"""
    return _ml_model_loaded


def set_model_loaded(status: bool) -> None:
    """Set the model loaded status (internal use)"""
    global _ml_model_loaded
    _ml_model_loaded = status


def get_model():
    """Get the loaded ML model"""
    return _ml_model


def set_model(model) -> None:
    """Set the ML model (internal use)"""
    global _ml_model
    _ml_model = model

