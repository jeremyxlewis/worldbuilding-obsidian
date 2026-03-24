"""Semantic search over a worldbuilding vault."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .embeddings import embed_query
from .indexer import VaultIndexer


class VaultSearch:
    """Search a worldbuilding vault using semantic similarity."""

    def __init__(self, vault_path: str | Path, index_path: Optional[str | Path] = None):
        self.vault_path = Path(vault_path)
        self.indexer = VaultIndexer(vault_path, index_path)

    def search(
        self,
        query: str,
        n_results: int = 5,
        entity_type: Optional[str] = None,
        folder: Optional[str] = None,
        auto_update: bool = True,
    ) -> list[dict]:
        """Search the vault for relevant chunks.

        Args:
            query: Search query string
            n_results: Number of results to return
            entity_type: Filter by entity type (e.g., "npc", "faction")
            folder: Filter by folder name (e.g., "01_Characters")
            auto_update: Automatically re-index if files changed

        Returns:
            List of result dicts with keys: text, source, heading, score
        """
        # Auto-update index if needed
        if auto_update and self.indexer.needs_update():
            self.indexer.incremental_index(show_progress=False)

        collection = self.indexer.get_collection()

        if collection.count() == 0:
            return []

        # Build metadata filter
        where_filter = {}
        if entity_type:
            where_filter["entity_type"] = entity_type
        if folder:
            where_filter["source"] = {"$contains": folder}

        # Query
        query_embedding = embed_query(query)

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, collection.count()),
            where=where_filter if where_filter else None,
            include=["documents", "metadatas", "distances"],
        )

        # Format results
        formatted = []
        if results and results.get("documents") and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i] if results.get("metadatas") else {}
                distance = results["distances"][0][i] if results.get("distances") else 0
                # Convert cosine distance to similarity score (0-1)
                score = (
                    round(1 - distance, 4)
                    if distance <= 1
                    else round(1 / (1 + distance), 4)
                )

                formatted.append(
                    {
                        "text": doc,
                        "source": meta.get("source", ""),
                        "entity_type": meta.get("entity_type", ""),
                        "entity_title": meta.get("entity_title", ""),
                        "heading": meta.get("heading", ""),
                        "heading_path": meta.get("heading_path", ""),
                        "tags": meta.get("tags", []),
                        "score": score,
                    }
                )

        return formatted

    def find_related(
        self,
        entity_name: str,
        n_results: int = 5,
        auto_update: bool = True,
    ) -> list[dict]:
        """Find entities related to a specific entity by name."""
        # Search using the entity name and its content
        results = self.search(
            f"entities related to {entity_name}",
            n_results=n_results + 5,  # Get extra to filter out self
            auto_update=auto_update,
        )

        # Filter out the entity itself
        filtered = [
            r
            for r in results
            if entity_name.lower() not in r.get("entity_title", "").lower()
        ]

        return filtered[:n_results]

    def find_similar(
        self,
        text: str,
        n_results: int = 5,
        auto_update: bool = True,
    ) -> list[dict]:
        """Find entities similar to a given text description."""
        return self.search(text, n_results=n_results, auto_update=auto_update)

    def context_for_generation(
        self,
        entity_type: str,
        description: str,
        related_names: list[str] = None,
        n_results: int = 5,
        auto_update: bool = True,
    ) -> str:
        """Build context string for entity generation.

        Searches the vault for relevant entities and formats them
        as context for the LLM to use when generating new content.
        """
        results = []

        # Search by description
        desc_results = self.search(
            description,
            n_results=n_results,
            auto_update=auto_update,
        )
        results.extend(desc_results)

        # Search by related entity names
        if related_names:
            for name in related_names[:3]:
                name_results = self.find_related(name, n_results=2, auto_update=False)
                results.extend(name_results)

        # Deduplicate by source
        seen = set()
        unique_results = []
        for r in results:
            key = f"{r['source']}::{r['heading']}"
            if key not in seen:
                seen.add(key)
                unique_results.append(r)

        # Format as context
        if not unique_results:
            return ""

        context_parts = ["## Relevant World Context\n"]
        for r in unique_results[:n_results]:
            source = r.get("entity_title", r["source"])
            heading = r.get("heading", "")
            score = r.get("score", 0)

            context_parts.append(f"### {source} — {heading} (relevance: {score:.0%})")
            context_parts.append(r["text"])
            context_parts.append("")

        return "\n".join(context_parts)
