# Worldbuilding-Obsidian

A skill for building worlds that feel lived-in, not designed. Generates complete Obsidian vaults for D&D homebrew and novelists with semantic search, faction clocks, deep continuity enforcement, and humanized in-world writing.

## Install

```bash
npx skills add jeremyxlewis/worldbuilding-obsidian
```

### RAG Dependencies (optional, for semantic search)

```bash
pip install -r requirements.txt
```

## What It Does

**8 workflows:**

1. **Create Vault** — Full Obsidian vault with 11 folders, 20+ templates, Dataview dashboards, plugin configs
2. **Create Entity** — Semantic search finds relevant context, then generates world-consistent entities with auto-linked wikilinks
3. **Diagnose World** — 16 diagnostic checks for consistency (W1-W16)
4. **Faction Clocks** — Blades in the Dark-style progression with auto-cascade on fill
5. **Continuity Check** — Deep enforcement for novelists (eye color, ages, timeline, magic rules)
6. **Cascade Analysis** — "What if the king dies?" traces all consequences through your vault
7. **Humanize** — Always-on AI-tell removal (24 categories) + voice injection
8. **Semantic Search** — RAG-powered search finds relevant entities even without explicit wikilinks

## Modes

| Mode | For | Focus |
|------|-----|-------|
| **D&D** | Game Masters | Stat blocks, encounters, session notes, homebrew rules |
| **Novel** | Novelists | Character arcs, plot structure, continuity, series bible |
| **Hybrid** | Both | Full worldbuilding for shared universe across media |

## Features

- **Semantic search (RAG)** — find related entities by meaning, not just wikilinks. "necromancy rituals" finds your Cult of Orcus even if you never linked them
- **World-aware generation** — reads your vault before creating new content
- **20+ Obsidian templates** — characters, locations, factions, quests, magic items, creatures, and more
- **Faction clock system** — track faction goals that advance independently of player action
- **Deep continuity** — catches eye color changes, timeline errors, magic rule violations
- **Dataview dashboards** — pre-built queries for characters, quests, factions, timeline
- **Plugin configs** — Fantasy Statblocks, Dice Roller, Calendarium, Leaflet, Templater
- **Humanized writing** — no "delve," no "tapestry," no "nestled in the heart of"

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

# Find what's related to an entity
python scripts/vault_search.py --vault /path --related "Elara Vareth"

# Check index stats
python scripts/index_vault.py --vault /path --stats
```

The index auto-syncs when files change — no manual re-indexing needed.

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
→ Searches vault for context, generates Thoren with proper frontmatter, wikilinks to related entities

"What would happen if the Merchant's Guild collapses?"
→ Traces 1st/2nd/3rd order consequences through your entire vault

"Check my world for consistency issues"
→ Runs 16 diagnostic checks, reports broken links, empty entities, AI writing patterns

"Advance the Cult of Orcus's faction clock by 1"
→ Updates clock, cascades consequences if clock fills

"Find everything related to necromancy"
→ Semantic search returns Cult of Orcus, undead encounters, death-related magic items
```

## Scripts

| Script | Purpose |
|--------|---------|
| `init_vault.py` | Create full vault scaffold with plugin configs |
| `create_entity.py` | Create entity from template with wikilinks |
| `validate_world.py` | Scan vault for issues, run diagnostics |
| `generate_dashboard.py` | Generate Dataview-powered dashboards |
| `cascade_analysis.py` | Trace "what if?" consequences through vault |
| `index_vault.py` | Index vault for semantic search (RAG) |
| `vault_search.py` | Semantic search across vault content |

## Tech Stack

- **Embedding model:** `intfloat/e5-small-v2` (16ms/query, 128MB RAM, CPU-only)
- **Vector store:** ChromaDB (local, persistent, zero-config)
- **Chunking:** Markdown header-aware splitting (h1-h3)
- **Sync:** Hash-based manifest, incremental re-index on search

## License

MIT
