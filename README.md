# Worldbuilding-Obsidian

A skill for building worlds that feel lived-in, not designed. Generates complete Obsidian vaults for D&D homebrew and novelists with faction clocks, deep continuity enforcement, and humanized in-world writing.

## Install

```bash
npx skills add jeremyxlewis/worldbuilding-obsidian
```

## What It Does

**7 workflows:**

1. **Create Vault** — Full Obsidian vault with 11 folders, 20+ templates, Dataview dashboards, plugin configs
2. **Create Entity** — Reads existing vault first, generates world-consistent entities with auto-linked wikilinks
3. **Diagnose World** — 16 diagnostic checks for consistency (W1-W16)
4. **Faction Clocks** — Blades in the Dark-style progression with auto-cascade on fill
5. **Continuity Check** — Deep enforcement for novelists (eye color, ages, timeline, magic rules)
6. **Cascade Analysis** — "What if the king dies?" traces all consequences through your vault
7. **Humanize** — Always-on AI-tell removal (24 categories) + voice injection

## Modes

| Mode | For | Focus |
|------|-----|-------|
| **D&D** | Game Masters | Stat blocks, encounters, session notes, homebrew rules |
| **Novel** | Novelists | Character arcs, plot structure, continuity, series bible |
| **Hybrid** | Both | Full worldbuilding for shared universe across media |

## Features

- **World-aware generation** — reads your vault before creating new content
- **20+ Obsidian templates** — characters, locations, factions, quests, magic items, creatures, and more
- **Faction clock system** — track faction goals that advance independently of player action
- **Deep continuity** — catches eye color changes, timeline errors, magic rule violations
- **Dataview dashboards** — pre-built queries for characters, quests, factions, timeline
- **Plugin configs** — Fantasy Statblocks, Dice Roller, Calendarium, Leaflet, Templater
- **Humanized writing** — no "delve," no "tapestry," no "nestled in the heart of"

## Vault Structure

```
World Name/
├── 00_Dashboard/          # Dataview dashboards
├── 01_Characters/         # PCs and NPCs
├── 02_Locations/          # Continents to buildings
├── 03_Organizations/      # Factions, guilds, governments
├── 04_Cultures_and_Races/ # Races, societies, customs
├── 05_Systems/            # Magic, technology, economy, religion
├── 06_History_and_Timeline/ # Events, eras, calendars
├── 07_Quests_and_Adventures/ # Quests, hooks, encounters
├── 08_Items_and_Equipment/   # Magic items, artifacts, gear
├── 09_Creatures/          # Monsters, beasts, wildlife
├── 10_Campaign/           # Session notes, homebrew rules
├── 11_Manuscript/         # Chapters, scenes (novel mode)
├── _Templates/            # All entity templates
└── _Resources/            # Images, maps, reference docs
```

## Example Usage

```
"Create a world vault for my dark fantasy D&D campaign set in a coastal city"
→ Generates full vault with starter NPCs, locations, factions, and quest hooks

"Create an NPC — a dwarven blacksmith named Thoren"
→ Reads existing vault, generates Thoren with proper frontmatter, wikilinks to related entities

"What would happen if the Merchant's Guild collapses?"
→ Traces 1st/2nd/3rd order consequences through your entire vault

"Check my world for consistency issues"
→ Runs 16 diagnostic checks, reports broken links, empty entities, AI writing patterns

"Advance the Cult of Orcus's faction clock by 1"
→ Updates clock, cascades consequences if clock fills
```

## Scripts

| Script | Purpose |
|--------|---------|
| `init_vault.py` | Create full vault scaffold with plugin configs |
| `create_entity.py` | Create entity from template with wikilinks |
| `validate_world.py` | Scan vault for issues, run diagnostics |
| `generate_dashboard.py` | Generate Dataview-powered dashboards |
| `cascade_analysis.py` | Trace "what if?" consequences through vault |

## License

MIT
