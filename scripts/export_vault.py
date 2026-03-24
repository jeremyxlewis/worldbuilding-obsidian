#!/usr/bin/env python3
"""Export vault to JSON or CSV for external tools.

Usage:
    python export_vault.py --vault /path --format json --output world.json
    python export_vault.py --vault /path --format csv --output characters.csv --type npc
    python export_vault.py --vault /path --format json --include-locations
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if value.startswith("[") and value.endswith("]"):
                value = [
                    v.strip().strip('"').strip("'") for v in value[1:-1].split(",")
                ]
            fm[key] = value
    return fm


def extract_body(content: str) -> str:
    """Extract body text without frontmatter."""
    match = re.match(r"^---\n.*?\n---\n", content, re.DOTALL)
    if match:
        return content[match.end() :]
    return content


def extract_wikilinks(content: str) -> list:
    """Extract all wikilinks from content."""
    return re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content)


def export_entity(md_file: Path, entity_type: str = None) -> dict:
    """Export a single entity to a dict."""
    content = md_file.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    body = extract_body(content)
    links = extract_wikilinks(content)

    return {
        "name": fm.get("title", md_file.stem),
        "type": entity_type or fm.get("type", "unknown"),
        "status": fm.get("status", ""),
        "tags": fm.get("tags", []),
        "file_path": str(md_file),
        "body": body.strip(),
        "links": links,
    }


def export_json(
    vault_path: Path, entity_type: str = None, include_all: bool = False
) -> list:
    """Export vault to JSON format."""
    entities = []

    folders_to_export = []
    if include_all:
        folders_to_export = [
            "01_Characters",
            "02_Locations",
            "03_Organizations",
            "04_Cultures_and_Races",
            "05_Systems",
            "06_History_and_Timeline",
            "07_Quests_and_Adventures",
            "08_Items_and_Equipment",
            "09_Creatures",
        ]
    elif entity_type:
        type_to_folder = {
            "character": "01_Characters",
            "npc": "01_Characters",
            "location": "02_Locations",
            "region": "02_Locations",
            "faction": "03_Organizations",
            "army": "03_Organizations",
            "treaty": "03_Organizations",
            "culture": "04_Cultures_and_Races",
            "race": "04_Cultures_and_Races",
            "language": "04_Cultures_and_Races",
            "historical-event": "06_History_and_Timeline",
            "quest": "07_Quests_and_Adventures",
            "encounter": "07_Quests_and_Adventures",
            "magic-item": "08_Items_and_Equipment",
            "creature": "09_Creatures",
        }
        folder = type_to_folder.get(entity_type)
        if folder:
            folders_to_export = [folder]
    else:
        folders_to_export = ["01_Characters", "02_Locations", "03_Organizations"]

    for folder in folders_to_export:
        folder_path = vault_path / folder
        if not folder_path.exists():
            continue

        for md_file in folder_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
            entity_type_folder = folder.split("/")[0] if "/" in folder else folder
            entities.append(export_entity(md_file, entity_type_folder))

    return entities


def export_csv(vault_path: Path, entity_type: str) -> list[dict]:
    """Export vault to CSV format (flattened)."""
    entities = export_json(vault_path, entity_type=entity_type)

    rows = []
    for e in entities:
        rows.append(
            {
                "name": e["name"],
                "type": e["type"],
                "status": e["status"],
                "tags": ", ".join(e["tags"]) if e["tags"] else "",
                "links": ", ".join(e["links"]) if e["links"] else "",
                "body": e["body"][:500],
            }
        )

    return rows


def main():
    parser = argparse.ArgumentParser(description="Export vault to JSON or CSV")
    parser.add_argument(
        "--vault",
        required=True,
        help="Path to the Obsidian vault",
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="Export format",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path",
    )
    parser.add_argument(
        "--type",
        help="Filter by entity type (e.g., npc, faction)",
    )
    parser.add_argument(
        "--include-locations",
        action="store_true",
        help="Include all location types (JSON only)",
    )

    args = parser.parse_args()

    vault_path = Path(args.vault)
    if not vault_path.exists():
        print(f"[!] Vault not found: {vault_path}")
        sys.exit(1)

    if args.format == "json":
        entities = export_json(
            vault_path, entity_type=args.type, include_all=args.include_locations
        )
        output = {
            "vault": vault_path.name,
            "export_date": str(Path(__file__).stat().st_mtime),
            "entity_count": len(entities),
            "entities": entities,
        }
        Path(args.output).write_text(json.dumps(output, indent=2, ensure_ascii=False))
        print(f"[+] Exported {len(entities)} entities to {args.output}")

    else:
        if not args.type:
            print("[!] --type is required for CSV export")
            sys.exit(1)
        rows = export_csv(vault_path, args.type)
        if not rows:
            print(f"[!] No entities of type '{args.type}' found")
            sys.exit(1)

        with open(args.output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["name", "type", "status", "tags", "links", "body"]
            )
            writer.writeheader()
            writer.writerows(rows)
        print(f"[+] Exported {len(rows)} entities to {args.output}")


if __name__ == "__main__":
    main()
