# Entity Templates Reference

All entity types and their templates. Templates are in `assets/templates/`.

## Entity Type → Folder Mapping

| Entity Type | Folder | Template File | Mode |
|-------------|--------|---------------|------|
| character | 01_Characters/ | character.md | All |
| npc | 01_Characters/ | npc.md | D&D |
| location | 02_Locations/ | location.md | All |
| region | 02_Locations/ | region.md | All |
| faction | 03_Organizations/ | faction.md | All |
| culture | 04_Cultures_and_Races/ | culture.md | All |
| race | 04_Cultures_and_Races/ | race.md | All |
| magic-system | 05_Systems/Magic/ | magic-system.md | All |
| religion | 05_Systems/Religion/ | religion.md | All |
| technology | 05_Systems/Technology/ | technology.md | All |
| economy | 05_Systems/Economy/ | economy.md | All |
| historical-event | 06_History_and_Timeline/ | historical-event.md | All |
| quest | 07_Quests_and_Adventures/ | quest.md | D&D |
| encounter | 07_Quests_and_Adventures/ | encounter.md | D&D |
| magic-item | 08_Items_and_Equipment/ | magic-item.md | D&D |
| creature | 09_Creatures/ | creature.md | D&D |
| session-note | 10_Campaign/ | session-note.md | D&D |
| scene | 11_Manuscript/ | scene.md | Novel |
| chapter | 11_Manuscript/ | chapter.md | Novel |
| faction-clock | 03_Organizations/ | faction-clock.md | All |

## Frontmatter Conventions

All entities use YAML frontmatter with these common fields:

```yaml
---
title: "Entity Name"
type: entity-type          # Matches template type
status: draft              # draft, active, completed, archived
tags: []                   # For categorization and Dataview queries
aliases: []                # Alternative names for wikilink resolution
---
```

## Humanizer Rules for Templates

All generated text in templates must follow humanizer rules:

1. **No banned words:** delve, tapestry, vibrant, serves as, stands as, pivotal role, nestled in, rich history, ancient civilization, looms, ancient prophecy
2. **Be specific:** Use concrete sensory details, not vague adjectives
3. **Vary rhythm:** Mix short and long sentences
4. **Have opinions:** In-world authors should have biases
5. **Add mess:** Tangents, contradictions, half-formed thoughts are human
