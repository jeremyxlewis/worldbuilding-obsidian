#!/usr/bin/env python3
"""Search a worldbuilding vault using semantic similarity.

Performs RAG-style search over indexed vault content.

Usage:
    python vault_search.py --vault /path/to/vault --query "necromancy rituals"
    python vault_search.py --vault /path/to/vault --query "thieves guild" --type faction
    python vault_search.py --vault /path/to/vault --query "coastal city" --folder 02_Locations
    python vault_search.py --vault /path/to/vault --related "Thoren Ironforge"
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent dir to path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.search import VaultSearch


def format_results(results: list[dict], json_output: bool = False) -> str:
    """Format search results for display."""
    if json_output:
        return json.dumps(results, indent=2)

    if not results:
        return "No results found."

    lines = []
    for i, r in enumerate(results, 1):
        score = r.get("score", 0)
        source = r.get("entity_title", r.get("source", "Unknown"))
        heading = r.get("heading", "")
        entity_type = r.get("entity_type", "")

        # Score bar
        bar_len = int(score * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)

        lines.append(f"### {i}. {source} — {heading}")
        lines.append(f"**Type:** {entity_type} | **Relevance:** {bar} {score:.0%}")
        lines.append(f"**File:** `{r.get('source', '')}`")
        lines.append("")

        # Truncate text for display
        text = r.get("text", "")
        if len(text) > 300:
            text = text[:300] + "..."
        lines.append(text)
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Search a worldbuilding vault using semantic similarity"
    )
    parser.add_argument(
        "--vault",
        required=True,
        help="Path to the Obsidian vault",
    )
    parser.add_argument(
        "--query",
        help="Search query",
    )
    parser.add_argument(
        "--related",
        help="Find entities related to this name",
    )
    parser.add_argument(
        "--type",
        dest="entity_type",
        help="Filter by entity type (e.g., npc, faction, location)",
    )
    parser.add_argument(
        "--folder",
        help="Filter by folder name (e.g., 01_Characters)",
    )
    parser.add_argument(
        "--region",
        help="Filter by region/subfolder (e.g., Northern_Kingdoms). Searches recursively in that folder.",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=5,
        help="Number of results (default: 5)",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Offset for pagination (default: 0)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--no-update",
        action="store_true",
        help="Skip auto-update of index",
    )

    args = parser.parse_args()

    if not args.query and not args.related:
        parser.error("Either --query or --related is required")

    vault_path = Path(args.vault)
    if not vault_path.exists():
        print(f"[!] Vault not found: {vault_path}")
        sys.exit(1)

    try:
        search = VaultSearch(vault_path)
    except ImportError as e:
        print(f"[!] Missing dependency: {e}")
        print(f"[*] Install with: pip install -r requirements.txt")
        sys.exit(1)

    try:
        if args.related:
            results = search.find_related(
                args.related,
                n_results=args.n,
                auto_update=not args.no_update,
            )
        else:
            results = search.search(
                args.query,
                n_results=args.n,
                entity_type=args.entity_type,
                folder=args.folder,
                region=args.region,
                offset=args.offset,
                auto_update=not args.no_update,
            )
    except Exception as e:
        print(f"[!] Search failed: {e}")
        sys.exit(1)

    print(format_results(results, json_output=args.json))


if __name__ == "__main__":
    main()
