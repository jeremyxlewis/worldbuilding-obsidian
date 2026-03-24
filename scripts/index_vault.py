#!/usr/bin/env python3
"""Index a worldbuilding vault for semantic search.

Creates a vector index of all .md files in the vault using
sentence-transformers embeddings and ChromaDB storage.

Usage:
    python index_vault.py --vault /path/to/vault
    python index_vault.py --vault /path/to/vault --full  # Force full re-index
    python index_vault.py --vault /path/to/vault --stats  # Show index stats
"""

import argparse
import sys
from pathlib import Path

# Add parent dir to path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.indexer import VaultIndexer


def main():
    parser = argparse.ArgumentParser(
        description="Index a worldbuilding vault for semantic search"
    )
    parser.add_argument(
        "--vault",
        required=True,
        help="Path to the Obsidian vault",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Force full re-index (default: incremental)",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show index statistics and exit",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of parallel workers for indexing (default: 1)",
    )

    args = parser.parse_args()

    vault_path = Path(args.vault)
    if not vault_path.exists():
        print(f"[!] Vault not found: {vault_path}")
        sys.exit(1)

    indexer = VaultIndexer(vault_path)

    if args.stats:
        try:
            stats = indexer.get_stats()
            print(f"[*] Index Statistics:")
            print(f"    Total chunks: {stats['total_chunks']}")
            print(f"    Indexed files: {stats['indexed_files']}")
            print(f"    Index path: {stats['index_path']}")
            print(f"    Needs update: {stats['needs_update']}")
        except Exception as e:
            print(f"[!] Could not read index: {e}")
            print(f"[*] Run without --stats to create the index")
        return

    print(f"[*] Vault: {vault_path}")
    print(f"[*] Index path: {indexer.index_path}")
    print()

    try:
        if args.full or not indexer.manifest:
            indexer.full_index(show_progress=True, max_workers=args.workers)
        else:
            indexer.incremental_index(show_progress=True)
    except ImportError as e:
        print(f"\n[!] Missing dependency: {e}")
        print(f"[*] Install with: pip install -r requirements.txt")
        sys.exit(1)

    # Show stats after indexing
    stats = indexer.get_stats()
    print(
        f"\n[✓] Index complete: {stats['total_chunks']} chunks from {stats['indexed_files']} files"
    )


if __name__ == "__main__":
    main()
