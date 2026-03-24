---
name: worldbuilding-obsidian
description: "Generate and manage Obsidian vaults for worldbuilding. Supports D&D homebrew (stat blocks, factions, quests, encounters) and novelists (character arcs, continuity, series bibles). Creates full vault structures with Dataview dashboards, faction clocks, deep continuity enforcement, and humanized in-world writing. Use when building fictional worlds, creating campaign settings, writing novels, managing NPCs, designing magic systems, organizing worldbuilding notes in Obsidian, or asking about D&D/novel worldbuilding workflows."
license: MIT
compatibility: Requires Python 3.8+, Obsidian (free). RAG requires: pip install -r requirements.txt
metadata:
  author: jeremyxlewis
  version: "1.0"
  keywords: worldbuilding, dnd, rpg, novel, obsidian, campaign, fantasy, homebrew
---

# Worldbuilding-Obsidian

Build worlds that feel lived-in, not designed. This skill generates complete Obsidian vaults for D&D homebrew and novelists with faction clocks, deep continuity enforcement, and humanized in-world writing.

## Core Principles

1. **Read before you write.** Always scan existing vault content before generating new entities. The world should constrain what you create.
2. **Follow consequences.** Every addition ripples outward. Trace 1st/2nd/3rd order effects.
3. **Start small, expand.** One town, three NPCs, one quest hook. Grow only as play demands.
4. **Sound human.** Every generated text passes humanizer checks. No "delve," no "tapestry," no "nestled in the heart of."

## When to Use

Use when the user asks to:
- Create a world, campaign setting, or novel bible
- Build an Obsidian vault for worldbuilding
- Generate NPCs, locations, factions, quests, items, creatures
- Design magic systems, religions, economies, cultures
- Track D&D sessions, encounters, or homebrew content
- Manage novel continuity, character arcs, or series bible
- Run diagnostic checks on a world's consistency
- Analyze "what if?" scenarios or trace consequences
- Set up faction clocks or progression systems

Do NOT use when:
- Writing prose fiction (scenes/chapters) without worldbuilding context
- Pure Obsidian syntax questions (use obsidian-markdown skill)
- Non-fiction writing

## Mode Selection

Determine mode from user context. Ask if ambiguous.

| Mode | Folder Active | Focus |
|------|---------------|-------|
| **D&D** | `10_Campaign/`, `07_Quests_and_Adventures/`, `09_Creatures/` | Stat blocks, encounters, session notes, homebrew rules |
| **Novel** | `11_Manuscript/`, `10_Campaign/` (as series bible) | Character arcs, plot structure, continuity, published vs. draft |
| **Hybrid** | All folders | Full worldbuilding for shared universe across media |

## Workflow A: Create New World Vault

When: "Create a world vault," "start a new campaign setting," "build a novel bible"

1. **Ask clarifying questions:**
   - Mode (D&D / Novel / Hybrid)?
   - World name and genre?
   - Tone (dark, epic, whimsical, grounded)?
   - Starting scope (single town? full continent? one city)?
   - Custom calendar needed? If so, month/week names, eras.

2. **Run init script:**
   ```bash
   python scripts/init_vault.py --vault-name "World Name" --mode dnd --output /path/to/vault
   ```

3. **Generate dashboard:** Run `scripts/generate_dashboard.py` on the vault.

4. **Create initial entities:** Based on starting scope:
   - **Single town:** Generate 1 location, 3-5 NPCs, 1 faction, 1 quest hook, 1 mystery
   - **City:** Generate 1 city, 3 districts, 5-8 NPCs, 2-3 factions, 2 quest hooks
   - **Continent:** Generate 1 continent, 3-5 regions, region stubs only (expand later)

5. **Set up calendar** if requested.

6. **Humanize all generated text.** Apply humanizer pass to every description.

7. **Report structure** to user with folder overview and next steps.

## Workflow B: Create Entity

When: "Create an NPC," "add a location," "make a faction," "generate a quest"

1. **Determine entity type** from user request. See [references/entity-templates.md](references/entity-templates.md) for all types.

2. **Search for context (RAG).** Before generating, run semantic search:
   ```bash
   python scripts/vault_search.py --vault /path/to/vault --query "description of what you're creating"
   ```
   This finds relevant existing entities even without explicit wikilinks. Use results as generation context.

3. **Read existing vault.** Before generating:
   - Scan target folder for existing entities (to match style, naming conventions)
   - Parse frontmatter of related entities (factions, locations, characters)
   - Build relationship graph from wikilinks
   - Read any referenced entities fully

4. **Generate entity** using appropriate template:
   - Fill frontmatter with all relevant properties
   - Write content that respects established facts
   - Create wikilinks to all related entities
   - Include D&D stat blocks if in D&D mode (see [references/dnd-systems.md](references/dnd-systems.md))

4. **Humanize text.** Apply humanizer pass (see [references/humanizer-integration.md](references/humanizer-integration.md)).

5. **Create .md file** in correct folder with proper naming.

6. **Update related entities.** Add wikilinks back from referenced entities.

7. **Report** what was created and what it links to.

### Entity Quick Reference

| Request | Folder | Template |
|---------|--------|----------|
| NPC / Character | `01_Characters/` | character.md |
| Location (city, dungeon, etc.) | `02_Locations/` | location.md or region.md |
| Faction / Guild / Government | `03_Organizations/` | faction.md |
| Culture / Race | `04_Cultures_and_Races/` | culture.md or race.md |
| Magic System | `05_Systems/Magic/` | magic-system.md |
| Religion / Deity | `05_Systems/Religion/` | religion.md |
| Technology | `05_Systems/Technology/` | technology.md |
| Economy | `05_Systems/Economy/` | economy.md |
| Historical Event | `06_History_and_Timeline/` | historical-event.md |
| Quest / Adventure | `07_Quests_and_Adventures/` | quest.md |
| Encounter | `07_Quests_and_Adventures/` | encounter.md |
| Magic Item / Equipment | `08_Items_and_Equipment/` | magic-item.md |
| Creature / Monster | `09_Creatures/` | creature.md |
| Session Note | `10_Campaign/` | session-note.md |
| Scene / Chapter | `11_Manuscript/` | scene.md or chapter.md |

## Workflow C: Diagnose World

When: "Check my world for issues," "run diagnostics," "is my world consistent"

1. **Run validator:**
   ```bash
   python scripts/validate_world.py --vault /path/to/vault --level full
   ```

2. **Apply diagnostic framework** (see [references/diagnostics.md](references/diagnostics.md)):
   - W1-W7.5: Core worldbuilding issues (inherited from worldbuilding skill)
   - W8-W12: D&D-specific issues
   - W13-W16: Novelist-specific issues

3. **Report issues** in Obsidian callout format:
   ```markdown
   > [!warning] W4: Economy Doesn't Make Sense
   > **Location:** 03_Organizations/Merchant's Guild.md
   > **Issue:** Guild controls all trade but no supply chain exists
   > **Fix:** Add trade routes, rival merchants, black market
   ```

4. **Suggest fixes** for each issue with specific file references.

## Workflow D: Faction Clock Update

When: "Advance the faction clock," "what are the factions doing," "tick the clocks"

1. **Read faction notes** in `03_Organizations/`.
2. **Parse clock state** from frontmatter.
3. **Advance clock** by requested amount (default: 1).
4. **Check if clock filled:**
   - If filled: trigger cascade (see Workflow F)
   - Generate affected location updates, NPC reactions, new quest hooks
5. **Update faction note** with new clock state.
6. **Report** current state of all faction clocks.

### Clock Frontmatter Format
```yaml
---
type: faction-clock
faction: "[[Cult of Orcus]]"
clock_name: "Raise the Necropolis"
clock_size: 6
clock_filled: 3
clock_triggers:
  - "Undead rise in the old cemetery"
  - "Temple district reports strange lights"
  - "Noble family found dead"
  - "City guard discovers underground temple"
  - "Mass resurrection in the slums"
  - "Necropolis fully manifested"
---
```

## Workflow E: Continuity Check (Novelist)

When: "Check continuity," "did I contradict myself," "eye color changed"

1. **Read established canon** — scan all notes for published/in-print markers.
2. **Read target content** — the new draft or scene to check.
3. **Flag contradictions** (see [references/continuity-enforcement.md](references/continuity-enforcement.md)):
   - Physical descriptions (eye color, hair, height, scars)
   - Ages and timeline arithmetic
   - Magic system rule violations
   - Relationship state changes
   - POV character knowledge bleed
4. **Generate report** with exact file:line references.
5. **Suggest fixes** that preserve narrative intent.

### Contradiction Report Format
```markdown
> [!danger] Continuity Error
> **Character:** Elena Vareth
> **Issue:** Eye color changed from blue (Book 1, Ch. 3) to green (Book 3, Ch. 7)
> **References:** [[Book 1 - Chapter 3#Elena's Introduction]], [[Book 3 - Chapter 7#The Mirror]]
> **Severity:** High (physical description, reader-facing)
```

## Workflow F: Cascade Analysis

When: "What would happen if...," "trace the consequences," "impact analysis"

1. **Identify the change** (e.g., "the king dies").
2. **Read vault** — find all entities connected to the subject.
3. **Trace consequences:**
   - **1st Order:** Direct effects (succession crisis, power vacuum)
   - **2nd Order:** Systemic adaptations (factions maneuver, economy shifts)
   - **3rd Order:** Cultural evolution (new language, ethical debates, normalized changes)
4. **Generate impact report** with affected entities and suggested updates.
5. **Optionally apply changes** if user confirms.

## Workflow G: Humanize Generated Text

Applied automatically after every generation. See [references/humanizer-integration.md](references/humanizer-integration.md).

### Banned Patterns
- "delve," "tapestry," "vibrant," "serves as," "stands as," "pivotal role"
- "nestled in the heart of," "rich history," "ancient civilization"
- "mysterious darkness looms," "ancient prophecy foretold"
- Rule of three overuse, em dash overuse, copula avoidance
- Vague attributions ("many believe," "scholars suggest")

### Injection Rules
- **Have opinions:** In-world authors have biases
- **Vary rhythm:** Short punchy + long exploratory sentences
- **Be specific:** "burnt tallow and old fish" not "a distinct atmosphere"
- **Add mess:** Tangents, contradictions between sources
- **Use concrete feelings:** "She hated how her hands shook" not "she felt anxious"
- **Let voices differ:** A priest writes differently than a merchant

## Obsidian Conventions

This skill generates Obsidian-flavored Markdown. For syntax details (wikilinks, callouts, frontmatter, embeds, tags), defer to the **obsidian-markdown** skill.

Key conventions used:
- **Frontmatter** for all entity metadata (type, status, tags, aliases)
- **Wikilinks** (`[[Entity Name]]`) for all relationships
- **Callouts** for important info (`> [!note]`, `> [!warning]`, `> [!danger]`)
- **Tags** for categorization (`#character`, `#location`, `#quest/active`)
- **Dataview** queries for dynamic dashboards
- **Mermaid** diagrams for timelines and relationships

## Vault Folder Structure

```
World Name/
├── 00_Dashboard/          # Dataview dashboards, overview notes
├── 01_Characters/         # PCs, NPCs, one note per person
├── 02_Locations/          # Continents to buildings
├── 03_Organizations/      # Factions, guilds, governments
├── 04_Cultures_and_Races/ # Races, societies, customs
├── 05_Systems/
│   ├── Magic/             # Magic systems, schools, rules
│   ├── Technology/        # Tech levels, inventions
│   ├── Economy/           # Currency, trade, scarcity
│   └── Religion/          # Deities, theology, temples
├── 06_History_and_Timeline/ # Events, eras, calendars
├── 07_Quests_and_Adventures/ # Quests, hooks, encounters
├── 08_Items_and_Equipment/   # Magic items, artifacts, gear
├── 09_Creatures/          # Monsters, beasts, wildlife
├── 10_Campaign/           # Session notes, homebrew rules
├── 11_Manuscript/         # Chapters, scenes (novel mode)
├── _Templates/            # All entity templates
└── _Resources/            # Images, maps, reference docs
```

## D&D Mechanical Support

See [references/dnd-systems.md](references/dnd-systems.md) for full details.

Includes: stat blocks, CR calculations, spell descriptions, class features, encounter balancing, XP budgets, loot tables, magic item rarity tiers.

## Custom Calendar System

See [references/calendar-systems.md](references/calendar-systems.md) for templates.

Supports custom month/week/day names, era definitions, moon phases, seasonal events, and Mermaid timeline visualization.

## Plugin Configuration

Generated vault includes configured Obsidian community plugins:

| Plugin | Purpose |
|--------|---------|
| Fantasy Statblocks | D&D 5e stat blocks in notes |
| Initiative Tracker | Combat encounter management |
| Dice Roller | Inline dice rolling |
| Obsidian Leaflet | Interactive maps |
| Calendarium | Custom fantasy calendars |
| Templater | Dynamic entity templates |
| Dataview | Database queries and dashboards |
| QuickAdd | Rapid entity creation macros |

Plugin configs are included in `assets/plugins/` and applied during vault generation.

## Reference Files

Load these only when needed:

| File | When to Load |
|------|-------------|
| [references/entity-templates.md](references/entity-templates.md) | Creating any entity type |
| [references/diagnostics.md](references/diagnostics.md) | Running world diagnostics |
| [references/dnd-systems.md](references/dnd-systems.md) | D&D stat blocks, spells, items |
| [references/dataview-queries.md](references/dataview-queries.md) | Building dashboards |
| [references/calendar-systems.md](references/calendar-systems.md) | Custom calendar setup |
| [references/faction-clocks.md](references/faction-clocks.md) | Faction progression system |
| [references/continuity-enforcement.md](references/continuity-enforcement.md) | Novel continuity checking |
| [references/humanizer-integration.md](references/humanizer-integration.md) | AI-tell removal patterns |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/init_vault.py` | Create full vault scaffold with plugin configs |
| `scripts/create_entity.py` | Create entity from template with wikilinks |
| `scripts/validate_world.py` | Scan vault for issues, run diagnostics |
| `scripts/generate_dashboard.py` | Generate Dataview-powered dashboards |
| `scripts/cascade_analysis.py` | Trace "what if?" consequences through vault |
| `scripts/index_vault.py` | Index vault for semantic search (RAG) |
| `scripts/vault_search.py` | Semantic search across vault content |

## RAG (Semantic Search)

Requires dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### How It Works
1. **Index:** `index_vault.py` chunks all .md files by headings, embeds them, stores in ChromaDB at `{vault}/.rag/`
2. **Search:** `vault_search.py` finds semantically relevant content before generation
3. **Auto-sync:** Index updates automatically when files change (hash-based detection)

### Usage
```bash
# First-time setup: index the vault
python scripts/index_vault.py --vault /path/to/vault

# Search for related content
python scripts/vault_search.py --vault /path/to/vault --query "necromancy rituals"

# Filter by entity type
python scripts/vault_search.py --vault /path/to/vault --query "thieves guild" --type faction

# Find entities related to a specific entity
python scripts/vault_search.py --vault /path/to/vault --related "Thoren Ironforge"

# Check index stats
python scripts/index_vault.py --vault /path/to/vault --stats
```

### Integration
Workflow B (Create Entity) automatically runs RAG search before generation to find related context. This ensures new entities reference existing world elements even without explicit wikilinks.

Base directory for this skill: `skills/worldbuilding-obsidian/`
Relative paths are relative to this base directory.
