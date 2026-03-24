#!/usr/bin/env python3
"""Generate Dataview-powered dashboards for a worldbuilding vault."""

import argparse
import sys
from pathlib import Path


def generate_main_dashboard(vault_path: Path, world_name: str, mode: str) -> None:
    """Generate the main dashboard with Dataview queries."""
    dashboard_dir = vault_path / "00_Dashboard"
    dashboard_dir.mkdir(parents=True, exist_ok=True)

    content = f"""---
title: "{world_name} - Dashboard"
type: dashboard
created: {__import__("datetime").date.today().isoformat()}
tags:
  - dashboard
  - world/{world_name.lower().replace(" ", "-")}
---

# {world_name}

> [!tip] Quick Navigation
> This dashboard auto-updates as you add content to your world.

---

## Characters

```dataview
TABLE WITHOUT ID
  file.link AS "Name",
  status AS "Status",
  faction AS "Faction",
  location AS "Location"
FROM "01_Characters"
SORT file.name ASC
```

## Locations

```dataview
TABLE WITHOUT ID
  file.link AS "Name",
  type AS "Type",
  region AS "Region"
FROM "02_Locations"
SORT file.name ASC
```

## Active Quests

```dataview
TABLE WITHOUT ID
  file.link AS "Quest",
  quest_giver AS "Quest Giver",
  level_range AS "Level",
  status AS "Status"
FROM "07_Quests_and_Adventures"
WHERE status = "active" OR status = "available"
SORT status ASC
```

## Factions

```dataview
TABLE WITHOUT ID
  file.link AS "Faction",
  type AS "Type",
  influence AS "Influence",
  alignment AS "Alignment"
FROM "03_Organizations"
SORT influence DESC
```

## Recent Activity

```dataview
TABLE WITHOUT ID
  file.link AS "Note",
  file.folder AS "Folder",
  file.mtime AS "Modified"
FROM ""
WHERE file.folder != "_Templates" AND file.folder != "_Resources"
SORT file.mtime DESC
LIMIT 15
```

## Orphaned Notes

> [!warning] Unlinked Notes
> These notes have no incoming links. Consider connecting them to your world.

```dataview
TABLE WITHOUT ID
  file.link AS "Note",
  file.folder AS "Folder"
FROM ""
WHERE length(file.inlinks) = 0
  AND file.folder != "_Templates"
  AND file.folder != "_Resources"
  AND file.folder != "00_Dashboard"
SORT file.folder ASC
```
"""
    (dashboard_dir / "Dashboard.md").write_text(content)
    print("[+] Generated main dashboard")


def generate_campaign_dashboard(vault_path: Path, world_name: str) -> None:
    """Generate D&D campaign dashboard."""
    dashboard_dir = vault_path / "00_Dashboard"

    content = f"""---
title: "{world_name} - Campaign"
type: dashboard
tags:
  - dashboard
  - campaign
---

# Campaign Dashboard

## Session History

```dataview
TABLE WITHOUT ID
  file.link AS "Session",
  session_number AS "#",
  date AS "Date",
  summary AS "Summary"
FROM "10_Campaign"
WHERE type = "session-note"
SORT session_number DESC
```

## Active Encounters

```dataview
TABLE WITHOUT ID
  file.link AS "Encounter",
  cr AS "CR",
  location AS "Location",
  status AS "Status"
FROM "07_Quests_and_Adventures"
WHERE type = "encounter" AND status != "completed"
SORT cr ASC
```

## Creatures by CR

```dataview
TABLE WITHOUT ID
  file.link AS "Creature",
  cr AS "CR",
  type AS "Type",
  habitat AS "Habitat"
FROM "09_Creatures"
SORT cr DESC
```

## Magic Items

```dataview
TABLE WITHOUT ID
  file.link AS "Item",
  rarity AS "Rarity",
  type AS "Type",
  attunement AS "Attunement"
FROM "08_Items_and_Equipment"
SORT rarity DESC
```

## Faction Clocks

```dataview
TABLE WITHOUT ID
  file.link AS "Faction",
  clock_name AS "Clock",
  clock_filled AS "Filled",
  clock_size AS "Size"
FROM "03_Organizations"
WHERE type = "faction-clock"
SORT clock_filled DESC
```

## Homebrew Rules

```dataview
LIST
FROM "10_Campaign"
WHERE type = "homebrew"
SORT file.name ASC
```
"""
    (dashboard_dir / "Campaign Dashboard.md").write_text(content)
    print("[+] Generated campaign dashboard")


def generate_manuscript_dashboard(vault_path: Path, world_name: str) -> None:
    """Generate novelist manuscript dashboard."""
    dashboard_dir = vault_path / "00_Dashboard"

    content = f"""---
title: "{world_name} - Manuscript"
type: dashboard
tags:
  - dashboard
  - manuscript
---

# Manuscript Dashboard

## Characters by Role

```dataview
TABLE WITHOUT ID
  file.link AS "Character",
  role AS "Role",
  arc_status AS "Arc",
  first_appearance AS "First Appeared"
FROM "01_Characters"
WHERE role
SORT role ASC, file.name ASC
```

## Scenes

```dataview
TABLE WITHOUT ID
  file.link AS "Scene",
  chapter AS "Chapter",
  pov AS "POV",
  word_count AS "Words",
  status AS "Status"
FROM "11_Manuscript"
WHERE type = "scene"
SORT chapter ASC
```

## Chapter Overview

```dataview
TABLE WITHOUT ID
  file.link AS "Chapter",
  chapter_number AS "#",
  word_count AS "Words",
  status AS "Status"
FROM "11_Manuscript"
WHERE type = "chapter"
SORT chapter_number ASC
```

## Timeline

```dataview
TABLE WITHOUT ID
  file.link AS "Event",
  era AS "Era",
  date AS "Date",
  significance AS "Significance"
FROM "06_History_and_Timeline"
SORT date ASC
```

## Continuity Notes

```dataview
TABLE WITHOUT ID
  file.link AS "Note",
  file.mtime AS "Last Modified"
FROM ""
WHERE contains(tags, "#needs-review") OR contains(tags, "#continuity")
SORT file.mtime ASC
```

## Word Count by Section

```dataview
TABLE WITHOUT ID
  file.folder AS "Section",
  sum(file.length) AS "Total Characters"
FROM ""
WHERE file.folder = "11_Manuscript"
GROUP BY file.folder
```
"""
    (dashboard_dir / "Manuscript Dashboard.md").write_text(content)
    print("[+] Generated manuscript dashboard")


def main():
    parser = argparse.ArgumentParser(description="Generate vault dashboards")
    parser.add_argument(
        "--vault",
        required=True,
        help="Path to the Obsidian vault",
    )
    parser.add_argument(
        "--mode",
        choices=["dnd", "novel", "hybrid"],
        default="hybrid",
        help="Generation mode",
    )
    parser.add_argument(
        "--world-name",
        help="World name (auto-detected from vault if not provided)",
    )

    args = parser.parse_args()

    vault_path = Path(args.vault)
    if not vault_path.exists():
        print(f"[!] Vault not found: {vault_path}")
        sys.exit(1)

    world_name = args.world_name or vault_path.name

    print(f"[*] Generating dashboards for: {world_name}")
    print(f"[*] Mode: {args.mode}")
    print()

    generate_main_dashboard(vault_path, world_name, args.mode)

    if args.mode in ("dnd", "hybrid"):
        generate_campaign_dashboard(vault_path, world_name)

    if args.mode in ("novel", "hybrid"):
        generate_manuscript_dashboard(vault_path, world_name)

    print(f"\n[✓] Dashboards generated in: {vault_path / '00_Dashboard'}")


if __name__ == "__main__":
    main()
