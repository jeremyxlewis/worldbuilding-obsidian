# Worldbuilding-Obsidian

A skill for building worlds that feel lived-in, not designed. Generates complete Obsidian vaults for D&D homebrew and novelists with semantic search, faction progress, deep continuity enforcement, and humanized in-world writing.

## Install

```bash
npx skills add jeremyxlewis/worldbuilding-obsidian
```

### RAG Dependencies (optional, for semantic search)

```bash
pip install -r requirements.txt
```

## What It Does

**9 workflows:**

1. **Create Vault** — Full Obsidian vault with 11 folders, 25+ templates, Dataview dashboards, plugin configs
2. **Create Entity** — Semantic search finds relevant context, then generates world-consistent entities with auto-linked wikilinks
3. **Bulk Create** — Generate 50+ NPCs from CSV/JSON at once
4. **Diagnose World** — 20+ diagnostic checks for consistency (W1-W16)
5. **Faction Progress** — Simple session-based tracking with optional programmatic advancement
6. **Continuity Check** — Deep enforcement for novelists (eye color, ages, timeline, magic rules)
7. **Cascade Analysis** — "What if the king dies?" traces all consequences through your vault
8. **Humanize** — Always-on AI-tell removal (24 categories) + voice injection
9. **Export/Import** — JSON/CSV export for external tools

## Modes

| Mode | For | Focus |
|------|-----|-------|
| **D&D** | Game Masters | Stat blocks, encounters, session notes, homebrew rules |
| **Novel** | Novelists | Character arcs, plot structure, continuity, series bible |
| **Hybrid** | Both | Full worldbuilding for shared universe across media |

## Features

- **Semantic search (RAG)** — find related entities by meaning, not just wikilinks. "necromancy rituals" finds your Cult of Orcus even if you never linked them
- **World-aware generation** — reads your vault before creating new content
- **25+ Obsidian templates** — characters, locations, factions, armies, diseases, languages, treaties, quests, magic items, creatures, and more
- **Faction progress tracking** — simple session notation: `Faction: ███░░ 3/6`
- **Canon status** — track draft/beta/published content for novelists
- **Deep continuity** — catches eye color changes, timeline errors, magic rule violations
- **Dataview dashboards** — pre-built queries for characters, quests, factions, timeline
- **Plugin configs** — Fantasy Statblocks, Dice Roller, Calendarium, Leaflet, Templater
- **Humanized writing** — no "delve," no "tapestry," no "nestled in the heart of"
- **Bulk operations** — create 50+ NPCs from CSV/JSON
- **Regional scoping** — filter searches by region
- **Export/Import** — JSON/CSV for external tools

## Semantic Search

The skill includes a RAG layer that embeds your vault into a local vector database. This means the skill can find relevant context even across notes that aren't explicitly linked.

### Setup

```bash
pip install -r requirements.txt
python scripts/index_vault.py --vault /path/to/vault
```

### Usage

```bash
# Search by meaning
python scripts/vault_search.py --vault /path --query "necromancy rituals"

# Filter by entity type
python scripts/vault_search.py --vault /path --query "thieves guild" --type faction

# Filter by region
python scripts/vault_search.py --vault /path --query "cities" --region Northern_Kingdoms

# Pagination
python scripts/vault_search.py --vault /path --query "locations" --offset 20 --n 10

# Find what's related to an entity
python scripts/vault_search.py --vault /path --related "Elara Vareth"

# Check index stats
python scripts/index_vault.py --vault /path --stats

# Faster indexing with parallel workers
python scripts/index_vault.py --vault /path --workers 4
```

The index auto-syncs when files change — no manual re-indexing needed.

## Vault Structure

```
World Name/
├── 00_Dashboard/          # Dataview dashboards
├── 01_Characters/         # PCs and NPCs
├── 02_Locations/          # Continents to buildings
├── 03_Organizations/      # Factions, guilds, governments, armies, treaties
├── 04_Cultures_and_Races/ # Races, societies, customs, languages
├── 05_Systems/
│   ├── Magic/             # Magic systems, schools, rules
│   ├── Technology/        # Tech levels, inventions
│   ├── Economy/           # Currency, trade, trade routes
│   ├── Religion/          # Deities, theology, temples
│   └── Medicine/          # Diseases, plagues
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
→ Searches vault for context, generates Thoren with proper frontmatter, wikilinks to related entities

"Generate 30 NPCs for Frostholm City from NPCs.csv"
→ Bulk creates 30 NPCs, links them all to Frostholm City

"What would happen if the Merchant's Guild collapses?"
→ Traces 1st/2nd/3rd order consequences through your entire vault

"Check my world for consistency issues"
→ Runs 20+ diagnostic checks, reports broken links, empty entities, AI writing patterns, quest orphans, NPC motivation gaps

"Show faction status"
→ Displays progress of all tracked factions using notation like ███░░ 3/6

"Find everything related to necromancy"
→ Semantic search returns Cult of Orcus, undead encounters, death-related magic items
```

## Scripts

| Script | Purpose |
|--------|---------|
| `init_vault.py` | Create full vault scaffold with plugin configs |
| `create_entity.py` | Create entity from template with wikilinks |
| `bulk_create.py` | Bulk create entities from CSV/JSON |
| `advance_clocks.py` | Track faction progress (--status, --faction, --all) |
| `rollback.py` | Snapshot and restore vault state |
| `validate_world.py` | Scan vault for issues, run diagnostics (20+ checks) |
| `generate_dashboard.py` | Generate Dataview-powered dashboards |
| `cascade_analysis.py` | Trace "what if?" consequences through vault |
| `index_vault.py` | Index vault for semantic search (RAG) |
| `vault_search.py` | Semantic search across vault content |
| `export_vault.py` | Export vault to JSON/CSV |

## Tech Stack

- **Embedding model:** `intfloat/e5-small-v2` (16ms/query, 128MB RAM, CPU-only)
- **Vector store:** ChromaDB (local, persistent, zero-config)
- **Chunking:** Markdown header-aware splitting (h1-h3)
- **Sync:** Hash-based manifest, incremental re-index on search
- **Parallel processing:** ThreadPoolExecutor for faster indexing

## License

MIT
