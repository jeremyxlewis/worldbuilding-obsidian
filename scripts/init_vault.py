#!/usr/bin/env python3
"""Initialize a worldbuilding Obsidian vault with full folder structure, templates, and plugin configs."""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

# Vault folder structure
FOLDERS = [
    "00_Dashboard",
    "01_Characters",
    "02_Locations",
    "03_Organizations",
    "04_Cultures_and_Races",
    "05_Systems/Magic",
    "05_Systems/Technology",
    "05_Systems/Economy",
    "05_Systems/Religion",
    "06_History_and_Timeline",
    "07_Quests_and_Adventures",
    "08_Items_and_Equipment",
    "09_Creatures",
    "10_Campaign",
    "11_Manuscript",
    "_Templates",
    "_Resources",
]

# Folder descriptions for README-style notes
FOLDER_DESCRIPTIONS = {
    "00_Dashboard": "Dataview dashboards and overview notes. Start here.",
    "01_Characters": "Player characters and NPCs. One note per person.",
    "02_Locations": "Continents, regions, cities, buildings, dungeons.",
    "03_Organizations": "Factions, guilds, governments, secret societies.",
    "04_Cultures_and_Races": "Races, societies, customs, languages.",
    "05_Systems/Magic": "Magic systems, schools, spell lists, rules.",
    "05_Systems/Technology": "Tech levels, inventions, social impact.",
    "05_Systems/Economy": "Currency, trade routes, scarcity, black markets.",
    "05_Systems/Religion": "Deities, theology, temples, rituals, schisms.",
    "06_History_and_Timeline": "Historical events, eras, calendars, timelines.",
    "07_Quests_and_Adventures": "Quests, adventure hooks, encounters.",
    "08_Items_and_Equipment": "Magic items, artifacts, mundane gear.",
    "09_Creatures": "Monsters, beasts, wildlife, variants.",
    "10_Campaign": "Session notes, homebrew rules, player info.",
    "11_Manuscript": "Chapters, scenes, drafts (novel mode).",
    "_Templates": "Entity templates. Copy these to create new notes.",
    "_Resources": "Images, maps, reference documents.",
}


def get_script_dir() -> Path:
    """Get the directory containing this script."""
    return Path(__file__).parent.parent


def create_vault_structure(vault_path: Path, mode: str) -> None:
    """Create the vault folder structure."""
    for folder in FOLDERS:
        folder_path = vault_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)

    print(f"[+] Created {len(FOLDERS)} folders")


def copy_templates(vault_path: Path) -> None:
    """Copy template files to _Templates folder."""
    templates_src = get_script_dir() / "assets" / "templates"
    templates_dst = vault_path / "_Templates"

    if not templates_src.exists():
        print(f"[!] Templates source not found: {templates_src}")
        return

    count = 0
    for template_file in templates_src.glob("*.md"):
        shutil.copy2(template_file, templates_dst / template_file.name)
        count += 1

    print(f"[+] Copied {count} templates")


def copy_plugin_configs(vault_path: Path) -> None:
    """Copy Obsidian plugin configurations."""
    plugins_src = get_script_dir() / "assets" / "plugins"
    obsidian_dir = vault_path / ".obsidian"
    obsidian_dir.mkdir(exist_ok=True)

    # Community plugins list
    plugins_json = obsidian_dir / "community-plugins.json"
    plugins_list = [
        "obsidian-statblocks",
        "initiative-tracker",
        "dice-roller",
        "obsidian-leaflet-plugin",
        "obsidian-calendar-plugin",
        "templater-obsidian",
        "dataview",
        "table-editor-obsidian",
        "quickadd",
    ]
    plugins_json.write_text(json.dumps(plugins_list, indent=2))

    # Plugin config directory
    plugin_config_dir = obsidian_dir / "plugins"
    plugin_config_dir.mkdir(exist_ok=True)

    # Copy plugin-specific configs if they exist
    if plugins_src.exists():
        for plugin_dir in plugins_src.iterdir():
            if plugin_dir.is_dir():
                dst = plugin_config_dir / plugin_dir.name
                dst.mkdir(exist_ok=True)
                for config_file in plugin_dir.glob("*"):
                    shutil.copy2(config_file, dst / config_file.name)

    print(f"[+] Configured {len(plugins_list)} Obsidian plugins")


def copy_css(vault_path: Path) -> None:
    """Copy CSS snippets to vault."""
    css_src = get_script_dir() / "assets" / "css"
    snippets_dir = vault_path / ".obsidian" / "snippets"
    snippets_dir.mkdir(parents=True, exist_ok=True)

    if css_src.exists():
        for css_file in css_src.glob("*.css"):
            shutil.copy2(css_file, snippets_dir / css_file.name)
            print(f"[+] Added CSS snippet: {css_file.name}")


def generate_dashboard(vault_path: Path, mode: str, world_name: str) -> None:
    """Generate the main dashboard note with Dataview queries."""
    dashboard_dir = vault_path / "00_Dashboard"

    # Main dashboard
    dashboard = f"""---
title: "{world_name} - Dashboard"
type: dashboard
tags:
  - dashboard
  - world/{world_name.lower().replace(" ", "-")}
---

# {world_name}

> [!tip] Quick Navigation
> Use this dashboard to navigate your world. All queries update automatically as you add content.

## Characters

```dataview
TABLE status AS "Status", faction AS "Faction", location AS "Location"
FROM "01_Characters"
SORT file.name ASC
```

## Locations

```dataview
TABLE type AS "Type", region AS "Region", status AS "Status"
FROM "02_Locations"
SORT file.name ASC
```

## Active Quests

```dataview
TABLE quest_giver AS "Quest Giver", level_range AS "Level", status AS "Status"
FROM "07_Quests_and_Adventures"
WHERE status = "active"
SORT file.name ASC
```

## Factions

```dataview
TABLE type AS "Type", influence AS "Influence", alignment AS "Alignment"
FROM "03_Organizations"
SORT influence DESC
```

## Recent Changes

```dataview
TABLE file.folder AS "Folder", file.mtime AS "Modified"
FROM ""
SORT file.mtime DESC
LIMIT 10
```

## Orphaned Notes

> [!warning] Notes with no incoming links
> These notes are not referenced by any other note. Consider linking them or they may be forgotten.

```dataview
TABLE file.folder AS "Folder"
FROM ""
WHERE length(file.inlinks) = 0 AND file.folder != "_Templates" AND file.folder != "_Resources"
SORT file.name ASC
```
"""
    (dashboard_dir / "Dashboard.md").write_text(dashboard)

    # Mode-specific dashboard
    if mode in ("dnd", "hybrid"):
        dnd_dashboard = f"""---
title: "{world_name} - Campaign Dashboard"
type: dashboard
tags:
  - dashboard
  - campaign
---

# Campaign Dashboard

## Session Notes

```dataview
TABLE session_number AS "Session", date AS "Date", summary AS "Summary"
FROM "10_Campaign"
WHERE type = "session-note"
SORT session_number DESC
```

## Active Encounters

```dataview
TABLE cr AS "CR", location AS "Location", status AS "Status"
FROM "07_Quests_and_Adventures"
WHERE type = "encounter" AND status != "completed"
SORT cr ASC
```

## Creatures

```dataview
TABLE cr AS "CR", type AS "Type", habitat AS "Habitat"
FROM "09_Creatures"
SORT cr DESC
```

## Magic Items

```dataview
TABLE rarity AS "Rarity", type AS "Type", attunement AS "Attunement"
FROM "08_Items_and_Equipment"
SORT rarity DESC
```

## Faction Clocks

```dataview
TABLE clock_name AS "Clock", clock_filled AS "Filled", clock_size AS "Size"
FROM "03_Organizations"
WHERE type = "faction-clock"
SORT clock_filled DESC
```
"""
        (dashboard_dir / "Campaign Dashboard.md").write_text(dnd_dashboard)

    if mode in ("novel", "hybrid"):
        novel_dashboard = f"""---
title: "{world_name} - Manuscript Dashboard"
type: dashboard
tags:
  - dashboard
  - manuscript
---

# Manuscript Dashboard

## Characters by Arc Status

```dataview
TABLE arc_status AS "Arc Status", first_appearance AS "First Appeared", role AS "Role"
FROM "01_Characters"
WHERE role = "protagonist" OR role = "antagonist" OR role = "supporting"
SORT role ASC
```

## Scenes

```dataview
TABLE chapter AS "Chapter", pov AS "POV", word_count AS "Words", status AS "Status"
FROM "11_Manuscript"
WHERE type = "scene"
SORT chapter ASC
```

## Timeline

```dataview
TABLE era AS "Era", date AS "Date", significance AS "Significance"
FROM "06_History_and_Timeline"
SORT date ASC
```

## Continuity Checks Needed

```dataview
TABLE file.folder AS "Folder", file.mtime AS "Last Modified"
FROM ""
WHERE contains(tags, "#needs-review")
SORT file.mtime ASC
```
"""
        (dashboard_dir / "Manuscript Dashboard.md").write_text(novel_dashboard)

    print(f"[+] Generated {mode} dashboards")


def create_world_meta(vault_path: Path, world_name: str, mode: str) -> None:
    """Create a world metadata note."""
    meta = f"""---
title: "{world_name}"
type: world
mode: {mode}
created: {__import__("datetime").date.today().isoformat()}
status: active
tags:
  - world
  - meta
---

# {world_name}

## Overview

*Describe your world here. What makes it unique? What's the core concept?*

## Core Concept

> [!tip] The Heart of Your World
> Every good world has one constraint that everything else adapts to. What's yours?

## Mode

This world is configured for **{mode}** mode.

## Quick Start

1. Open `00_Dashboard/Dashboard.md` to see your world at a glance
2. Start with one location and 3 NPCs
3. Add complexity only as play demands

## Settings

| Setting | Value |
|---------|-------|
| Mode | {mode} |
| Created | {__import__("datetime").date.today().isoformat()} |
| Status | Active |
"""
    (vault_path / "_World Meta.md").write_text(meta)
    print("[+] Created world metadata note")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a worldbuilding Obsidian vault"
    )
    parser.add_argument(
        "--vault-name",
        required=True,
        help="Name of the world/vault",
    )
    parser.add_argument(
        "--mode",
        choices=["dnd", "novel", "hybrid"],
        default="hybrid",
        help="Generation mode (default: hybrid)",
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Output directory (default: current directory)",
    )

    args = parser.parse_args()

    vault_path = Path(args.output) / args.vault_name
    vault_path.mkdir(parents=True, exist_ok=True)

    print(f"[*] Initializing vault: {vault_path}")
    print(f"[*] Mode: {args.mode}")
    print()

    create_vault_structure(vault_path, args.mode)
    copy_templates(vault_path)
    copy_plugin_configs(vault_path)
    copy_css(vault_path)
    generate_dashboard(vault_path, args.mode, args.vault_name)
    create_world_meta(vault_path, args.vault_name, args.mode)

    print()
    print(f"[✓] Vault created: {vault_path}")
    print(f"[*] Open in Obsidian: obsidian://open?vault={args.vault_name}")
    print(f"[*] Or: File > Open folder as vault > {vault_path}")


if __name__ == "__main__":
    main()
