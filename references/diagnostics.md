# Diagnostic Framework

16 diagnostic states for checking worldbuilding consistency.

## Core World States (W1-W7.5)

Inherited from the worldbuilding skill.

### W1: Backdrop World
**Symptoms:** Setting exists but has no independent logic
**Check:** Do locations have their own economies, politics, histories?
**Fix:** Add consequence cascade to each major location

### W2: World Without Consequences
**Symptoms:** Technology/magic exists but hasn't transformed society
**Check:** Has every speculative element been traced through 3 orders?
**Fix:** Apply consequence cascade to all magic/technology

### W3: Institutions Without History
**Symptoms:** Organizations feel designed rather than evolved
**Check:** Do factions have founding dates, crises survived, internal contradictions?
**Fix:** Add founding story, at least one crisis, one internal debate

### W4: Economy Doesn't Make Sense
**Symptoms:** Trade exists without supply chains; prices arbitrary
**Check:** Is there a fundamental scarcity? How is value determined? Underground economy?
**Fix:** Add trade routes, scarcity factors, black market

### W5: Belief Systems Are Shallow
**Symptoms:** Religion is flavor without theological depth
**Check:** Do religions explain existence? Affect daily decisions? Have schisms?
**Fix:** Add theological core, daily practice impact, at least one schism

### W6: Culture Without Depth
**Symptoms:** Traditions feel random; surface-level aesthetic
**Check:** Do cultures have regional variation? Class differences? Historical reasons for customs?
**Fix:** Add at least 3 distinct traditions with historical explanations

### W7: Flat Non-Humans
**Symptoms:** Species are humans in costume
**Check:** Do non-humans have different biology that shapes cognition and culture?
**Fix:** Start with biology → trace to cognition → trace to culture

### W7.5: Language Feels Generic
**Symptoms:** Names sound like English; no linguistic texture
**Check:** Do names follow consistent phonetic patterns? Are there in-world linguistic differences?
**Fix:** Establish phonetic rules for each culture/language

## D&D Diagnostics (W8-W12)

### W8: Encounter Balance Issues
**Symptoms:** Encounters too easy or too hard for party
**Check:** CR vs. party level, action economy, terrain advantages
**Fix:** Adjust creature count, add terrain hazards, scale HP/damage

### W9: Magic Item Economy Broken
**Symptoms:** Too many or too few magic items
**Check:** Items per level, rarity distribution, attunement slots
**Fix:** Adjust loot tables, add crafting requirements, introduce item degradation

### W10: Quest Hooks Orphaned
**Symptoms:** Quests with no connection to main plot or world
**Check:** Does each quest link to at least 2 other entities (NPC, location, faction)?
**Fix:** Add connections to existing world elements

### W11: NPC Motivation Gaps
**Symptoms:** NPCs exist without clear reasons
**Check:** Does each NPC have a want, a fear, and a secret?
**Fix:** Add motivation, consequence of failure, hidden agenda

### W12: Geography Inconsistencies
**Symptoms:** Travel times don't make sense, biomes don't follow rules
**Check:** Are travel times proportional to distance? Do biomes follow climate logic?
**Fix:** Add travel time table, adjust biome placement

## Novelist Diagnostics (W13-W16)

### W13: Character Arc Stagnation
**Symptoms:** Characters don't grow or change
**Check:** Does each major character have a defined arc with at least 3 growth points?
**Fix:** Define start state, end state, and 3 turning points

### W14: POV Knowledge Bleed
**Symptoms:** POV character knows things they shouldn't
**Check:** Track what each character has experienced vs. what they know
**Fix:** Add knowledge tracking to character notes, flag violations

### W15: Pacing Issues
**Symptoms:** Too many events clustered or too sparse
**Check:** Timeline density, scene tension curve, chapter length variation
**Fix:** Spread events, add tension variation, adjust chapter lengths

### W16: Theme Inconsistency
**Symptoms:** World doesn't reinforce theme
**Check:** Does every major element relate to the core theme?
**Fix:** Add thematic connections to locations, factions, magic systems

## Running Diagnostics

Use `scripts/validate_world.py --vault /path/to/vault --level full`

The validator checks:
- Broken wikilinks
- Empty entities
- Duplicate entities
- Orphaned notes
- Missing frontmatter
- AI writing patterns (humanizer)

## Report Format

```markdown
> [!danger] W4: Economy Doesn't Make Sense
> **File:** 03_Organizations/Merchant's Guild.md
> **Issue:** Guild controls all trade but no supply chain exists
> **Fix:** Add trade routes, rival merchants, black market
```
