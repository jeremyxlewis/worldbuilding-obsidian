#!/usr/bin/env python3
"""Create an entity from a template with proper frontmatter and wikilinks."""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent.parent / "assets" / "templates"

# Folder mapping by entity type
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
    "scene": "11_Manuscript",
    "chapter": "11_Manuscript",
}


def load_template(entity_type: str) -> str:
    """Load a template file for the given entity type."""
    template_path = TEMPLATE_DIR / f"{entity_type}.md"
    if not template_path.exists():
        print(f"[!] Template not found: {template_path}")
        print(f"[*] Available templates: {', '.join(sorted(ENTITY_FOLDERS.keys()))}")
        sys.exit(1)
    return template_path.read_text()


def find_related_entities(vault_path: Path, entity_type: str, name: str) -> list:
    """Scan vault for entities that might relate to the new entity."""
    related = []
    for md_file in vault_path.rglob("*.md"):
        if md_file.name.startswith("."):
            continue
        try:
            content = md_file.read_text()
            # Check if the name or type is referenced
            if name.lower() in content.lower():
                related.append(md_file.stem)
        except Exception:
            continue
    return related


def create_entity(
    vault_path: Path,
    entity_type: str,
    name: str,
    properties: dict = None,
    mode: str = "hybrid",
) -> Path:
    """Create an entity note in the vault."""

    # Load template
    template = load_template(entity_type)

    # Determine target folder
    folder_name = ENTITY_FOLDERS.get(entity_type, "01_Characters")
    target_dir = vault_path / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)

    # Create file path
    safe_name = re.sub(r'[<>:"/\\|?*]', "", name)
    file_path = target_dir / f"{safe_name}.md"

    if file_path.exists():
        print(f"[!] File already exists: {file_path}")
        print(f"[*] Use --force to overwrite")
        sys.exit(1)

    # Find related entities
    related = find_related_entities(vault_path, entity_type, name)

    # Replace template placeholders
    content = template
    content = content.replace("{{name}}", name)
    content = content.replace("{{date}}", date.today().isoformat())
    content = content.replace("{{type}}", entity_type)

    # Apply custom properties
    if properties:
        for key, value in properties.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))

    # Add related entity links in a callout if any found
    if related:
        related_section = "\n> [!info] Related Entities\n"
        for entity in related[:10]:  # Limit to 10
            related_section += f"> - [[{entity}]]\n"
        content += related_section

    # Write file
    file_path.write_text(content)
    print(f"[+] Created: {file_path}")

    # Update related entities with backlinks
    for entity_name in related:
        for md_file in vault_path.rglob("*.md"):
            if md_file.stem == entity_name and md_file != file_path:
                try:
                    existing = md_file.read_text()
                    if f"[[{name}]]" not in existing:
                        # Add to a "Related" section if it exists, otherwise append
                        if "## Related" in existing:
                            existing = existing.replace(
                                "## Related",
                                f"## Related\n- [[{name}]]",
                            )
                        else:
                            existing += f"\n\n## Related\n- [[{name}]]\n"
                        md_file.write_text(existing)
                        print(f"[*] Added backlink to {md_file.name}")
                except Exception:
                    continue

    return file_path


def main():
    parser = argparse.ArgumentParser(description="Create an entity from template")
    parser.add_argument(
        "--vault",
        required=True,
        help="Path to the Obsidian vault",
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=list(ENTITY_FOLDERS.keys()),
        help="Entity type",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Entity name",
    )
    parser.add_argument(
        "--mode",
        choices=["dnd", "novel", "hybrid"],
        default="hybrid",
        help="Generation mode",
    )
    parser.add_argument(
        "--property",
        action="append",
        dest="properties",
        help="Custom properties as key=value (can be repeated)",
    )

    args = parser.parse_args()

    vault_path = Path(args.vault)
    if not vault_path.exists():
        print(f"[!] Vault not found: {vault_path}")
        sys.exit(1)

    # Parse properties
    properties = {}
    if args.properties:
        for prop in args.properties:
            if "=" in prop:
                key, value = prop.split("=", 1)
                properties[key] = value

    file_path = create_entity(vault_path, args.type, args.name, properties, args.mode)
    print(f"[✓] Entity created: {file_path}")


if __name__ == "__main__":
    main()
