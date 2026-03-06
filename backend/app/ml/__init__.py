"""
Machine Learning package
Contains ML models, embeddings, and analysis logic
"""

from __future__ import annotations

from typing import Any

# Global flag to track if ML model is loaded.
# This is intentionally simple; for multi-worker deployments you'd typically
# load per-worker, not share across processes.
_ml_model_loaded: bool = False
_ml_model: Any | None = None


def is_model_loaded() -> bool:
    """Check if ML model is currently loaded"""
    return _ml_model_loaded


def set_model_loaded(status: bool) -> None:
    """Set the model loaded status (internal use)"""
    global _ml_model_loaded
    _ml_model_loaded = status


def get_model() -> Any | None:
    """Get the loaded ML model"""
    return _ml_model


def set_model(model: Any | None) -> None:
    """Set the ML model (internal use)"""
    global _ml_model
    _ml_model = model