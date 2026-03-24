"""Embedding generation using sentence-transformers."""

from __future__ import annotations

import os
from pathlib import Path

# Default model - best speed/accuracy tradeoff for <1000 docs
DEFAULT_MODEL = "intfloat/e5-small-v2"

_model_cache = {}


def get_model(model_name: str = DEFAULT_MODEL):
    """Get or load a sentence-transformers model (cached)."""
    if model_name not in _model_cache:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers is required for RAG. "
                "Install with: pip install sentence-transformers"
            )
        _model_cache[model_name] = SentenceTransformer(model_name)
    return _model_cache[model_name]


def embed_texts(texts: list[str], model_name: str = DEFAULT_MODEL) -> list[list[float]]:
    """Embed a list of texts and return vectors."""
    model = get_model(model_name)
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


def embed_query(query: str, model_name: str = DEFAULT_MODEL) -> list[float]:
    """Embed a single query string."""
    return embed_texts([query], model_name)[0]


def get_model_info(model_name: str = DEFAULT_MODEL) -> dict:
    """Get info about the embedding model."""
    model = get_model(model_name)
    return {
        "name": model_name,
        "max_seq_length": model.max_seq_length,
        "embedding_dimension": model.get_sentence_embedding_dimension(),
    }
