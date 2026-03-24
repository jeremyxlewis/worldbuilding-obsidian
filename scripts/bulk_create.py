#!/usr/bin/env python3
"""Bulk create entities from CSV or JSON input.

Usage:
    python bulk_create.py --vault /path --input entities.csv --type npc
    python bulk_create.py --vault /path --input cities.json --type location --city "Kingdom Name"
"""

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent.parent / "assets" / "templates"

ENTITY_FOLDERS = {
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
    "magic-system": "05_Systems/Magic",
    "religion": "05_Systems/Religion",
    "technology": "05_Systems/Technology",
    "economy": "05_Systems/Economy",
    "trade-route": "05_Systems/Economy",
    "disease": "05_Systems/Medicine",
    "historical-event": "06_History_and_Timeline",
    "quest": "07_Quests_and_Adventures",
    "encounter": "07_Quests_and_Adventures",
    "magic-item": "08_Items_and_Equipment",
    "creature": "09_Creatures",
    "session-note": "10_Campaign",
}


def load_template(entity_type: str) -> str:
    """Load a template file for the given entity type."""
    template_path = TEMPLATE_DIR / f"{entity_type}.md"
    if not template_path.exists():
        template_path = TEMPLATE_DIR / "character.md"
    return template_path.read_text()


def create_bulk_entities(
    vault_path: Path,
    entity_type: str,
    entities: list[dict],
    city_link: str = None,
) -> list[Path]:
    """Create multiple entities from a list of entity dicts."""
    template = load_template(entity_type)
    folder_name = ENTITY_FOLDERS.get(entity_type, "01_Characters")
    target_dir = vault_path / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)

    created = []
    import re

    for entity in entities:
        name = entity.get("name", entity.get("title", "Unnamed"))
        safe_name = re.sub(r'[<>:"/\\|?*]', "", name)
        file_path = target_dir / f"{safe_name}.md"

        if file_path.exists():
            print(f"[!] Skipping (exists): {file_path}")
            continue

        content = template
        content = content.replace("{{name}}", name)
        content = content.replace("{{date}}", date.today().isoformat())
        content = content.replace("{{type}}", entity_type)

        for key, value in entity.items():
            if key != "name":
                content = content.replace(f"{{{{{key}}}}}", str(value))

        if city_link:
            content += f"\n\n## Location\n- **City:** [[{city_link}]]\n"

        content += f"\n\n## Bulk Creation\n- **Created:** {date.today().isoformat()}\n"

        file_path.write_text(content)
        created.append(file_path)
        print(f"[+] Created: {file_path}")

    return created


def parse_csv(path: Path) -> list[dict]:
    """Parse CSV file into list of dicts."""
    entities = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entities.append(dict(row))
    return entities


def parse_json(path: Path) -> list[dict]:
    """Parse JSON file into list of dicts."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "entities" in data:
        return data["entities"]
    return [data]


def main():
    parser = argparse.ArgumentParser(description="Bulk create entities from CSV/JSON")
    parser.add_argument(
        "--vault",
        required=True,
        help="Path to the Obsidian vault",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input file (CSV or JSON)",
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=list(ENTITY_FOLDERS.keys()),
        help="Entity type",
    )
    parser.add_argument(
        "--city",
        help="Link all entities to a city location",
    )

    args = parser.parse_args()

    vault_path = Path(args.vault)
    if not vault_path.exists():
        print(f"[!] Vault not found: {vault_path}")
        sys.exit(1)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[!] Input file not found: {input_path}")
        sys.exit(1)

    if input_path.suffix == ".csv":
        entities = parse_csv(input_path)
    elif input_path.suffix == ".json":
        entities = parse_json(input_path)
    else:
        print(f"[!] Unsupported file type: {input_path.suffix}")
        sys.exit(1)

    print(f"[*] Creating {len(entities)} {args.type} entities...")

    created = create_bulk_entities(
        vault_path,
        args.type,
        entities,
        city_link=args.city,
    )

    print(f"\n[✓] Created {len(created)} entities")


if __name__ == "__main__":
    main()
