"""RAG library for worldbuilding-obsidian."""

from .indexer import VaultIndexer
from .search import VaultSearch
from .chunker import chunk_file, chunk_by_headers
from .embeddings import embed_texts, embed_query

__all__ = [
    "VaultIndexer",
    "VaultSearch",
    "chunk_file",
    "chunk_by_headers",
    "embed_texts",
    "embed_query",
]
