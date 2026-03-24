"""Hash-based vault indexer with incremental updates."""

import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

from .chunker import chunk_file, Chunk
from .embeddings import embed_texts


class VaultIndexer:
    """Manages the vector index for a worldbuilding vault."""

    def __init__(self, vault_path: str | Path, index_path: Optional[str | Path] = None):
        self.vault_path = Path(vault_path)
        self.index_path = Path(index_path) if index_path else self.vault_path / ".rag"
        self.manifest_path = self.index_path / "manifest.json"
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> dict:
        """Load the manifest file if it exists."""
        if self.manifest_path.exists():
            try:
                return json.loads(self.manifest_path.read_text())
            except (json.JSONDecodeError, Exception):
                return {}
        return {}

    def _save_manifest(self):
        """Save the manifest to disk."""
        self.index_path.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(json.dumps(self.manifest, indent=2))

    @staticmethod
    def _file_hash(filepath: Path) -> str:
        """Compute SHA-256 hash of file contents."""
        return hashlib.sha256(filepath.read_bytes()).hexdigest()

    def _get_vault_files(self) -> list[Path]:
        """Get all .md files in the vault, excluding internal dirs."""
        exclude = {"_Templates", "_Resources", ".rag", ".obsidian", ".git"}
        files = []
        for f in self.vault_path.rglob("*.md"):
            if f.name.startswith("."):
                continue
            if any(part in exclude for part in f.parts):
                continue
            files.append(f)
        return files

    def get_changed_files(self) -> tuple[list[Path], list[Path], list[Path]]:
        """Detect added, modified, and deleted files since last index.

        Returns (added, modified, deleted).
        """
        current_files = set(self._get_vault_files())
        indexed_files = set(Path(p) for p in self.manifest.keys())

        added = sorted(current_files - indexed_files)
        deleted = sorted(indexed_files - current_files)

        modified = []
        for f in sorted(current_files & indexed_files):
            current_hash = self._file_hash(f)
            cached_hash = self.manifest.get(str(f), {}).get("hash", "")
            if current_hash != cached_hash:
                modified.append(f)

        return added, modified, deleted

    def needs_update(self) -> bool:
        """Check if any files have changed since last index."""
        added, modified, deleted = self.get_changed_files()
        return bool(added or modified or deleted)

    def get_collection(self):
        """Get or create the ChromaDB collection."""
        try:
            import chromadb
        except ImportError:
            raise ImportError(
                "chromadb is required for RAG. Install with: pip install chromadb"
            )

        self.index_path.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(self.index_path / "chroma_db"))
        return client.get_or_create_collection(
            name="vault",
            metadata={"hnsw:space": "cosine"},
        )

    def full_index(self, show_progress: bool = True, max_workers: int = 4):
        """Perform a full index of all vault files."""
        files = self._get_vault_files()

        if show_progress:
            print(f"[*] Indexing {len(files)} files...")

        all_chunks: list[Chunk] = []

        if max_workers > 1:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(chunk_file, str(f)): f for f in files}
                for future in as_completed(futures):
                    try:
                        chunks = future.result()
                        all_chunks.extend(chunks)
                    except Exception as e:
                        if show_progress:
                            print(f"[!] Error indexing {futures[future]}: {e}")
        else:
            for f in files:
                chunks = chunk_file(str(f))
                all_chunks.extend(chunks)

        if not all_chunks:
            print("[!] No chunks created. Check your vault has .md files with content.")
            return

        if show_progress:
            print(f"[*] Created {len(all_chunks)} chunks, generating embeddings...")

        # Generate embeddings
        texts = [c.text for c in all_chunks]
        embeddings = embed_texts(texts)

        # Store in ChromaDB
        collection = self.get_collection()

        # Clear existing data
        try:
            collection.delete(where={})
        except Exception:
            pass

        # Batch add (chromadb has limits on batch size)
        batch_size = 100
        for i in range(0, len(all_chunks), batch_size):
            batch_chunks = all_chunks[i : i + batch_size]
            batch_embeddings = embeddings[i : i + batch_size]

            collection.add(
                documents=[c.text for c in batch_chunks],
                embeddings=batch_embeddings,
                ids=[f"chunk_{i + j}" for j in range(len(batch_chunks))],
                metadatas=[c.metadata for c in batch_chunks],
            )

        # Update manifest
        self.manifest = {}
        for f in files:
            self.manifest[str(f)] = {
                "hash": self._file_hash(f),
                "mtime": f.stat().st_mtime,
            }
        self._save_manifest()

        if show_progress:
            print(f"[+] Indexed {len(all_chunks)} chunks from {len(files)} files")

    def incremental_index(self, show_progress: bool = True):
        """Only re-index files that have changed."""
        added, modified, deleted = self.get_changed_files()

        if not (added or modified or deleted):
            if show_progress:
                print("[*] Index is up to date")
            return

        collection = self.get_collection()

        # Remove deleted files from collection
        for f in deleted:
            # Find chunk IDs for this file
            chunk_ids = [
                k for k, v in self.manifest.items() if v.get("source") == str(f)
            ]
            if chunk_ids:
                try:
                    collection.delete(ids=chunk_ids)
                except Exception:
                    pass
            del self.manifest[str(f)]

        # Re-index added + modified files
        changed_files = added + modified
        if not changed_files:
            self._save_manifest()
            return

        if show_progress:
            print(f"[*] Re-indexing {len(changed_files)} changed files...")

        all_chunks: list[Chunk] = []
        for f in changed_files:
            chunks = chunk_file(str(f))
            all_chunks.extend(chunks)

        if all_chunks:
            texts = [c.text for c in all_chunks]
            embeddings = embed_texts(texts)

            # Upsert (add or update)
            batch_size = 100
            for i in range(0, len(all_chunks), batch_size):
                batch_chunks = all_chunks[i : i + batch_size]
                batch_embeddings = embeddings[i : i + batch_size]

                collection.upsert(
                    documents=[c.text for c in batch_chunks],
                    embeddings=batch_embeddings,
                    ids=[f"chunk_{hash(c.chunk_id)}" for c in batch_chunks],
                    metadatas=[c.metadata for c in batch_chunks],
                )

        # Update manifest for changed files
        for f in changed_files:
            self.manifest[str(f)] = {
                "hash": self._file_hash(f),
                "mtime": f.stat().st_mtime,
            }
        self._save_manifest()

        if show_progress:
            print(
                f"[+] Re-indexed {len(all_chunks)} chunks from {len(changed_files)} files"
            )

    def update(self, show_progress: bool = True):
        """Update the index (incremental if possible, full if first time)."""
        if not self.manifest:
            self.full_index(show_progress)
        else:
            self.incremental_index(show_progress)

    def get_stats(self) -> dict:
        """Get index statistics."""
        collection = self.get_collection()
        count = collection.count()
        return {
            "total_chunks": count,
            "indexed_files": len(self.manifest),
            "index_path": str(self.index_path),
            "needs_update": self.needs_update(),
        }
