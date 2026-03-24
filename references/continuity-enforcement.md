# Continuity Enforcement Reference

Deep continuity checking for novelists.

## What to Track

### Physical Descriptions
Store in character frontmatter:
```yaml
---
eye_color: blue
hair_color: auburn
height: 5'7"
scars: "Burn scar on left temple"
tattoos: "Rose on right wrist"
---
```

### Ages and Timeline
```yaml
---
birth_year: 1985
birth_month: 3
birth_day: 15
---
```

**Age calculation:**
```
Current age = current_year - birth_year
If current_month < birth_month: subtract 1
If current_month == birth_month AND current_day < birth_day: subtract 1
```

### Magic System Rules
Store rules in magic system notes. Flag any scene that violates established rules.

### Relationship States
```yaml
---
relationships:
  - character: "[[Elena]]"
    trust: high
    knows_secret: true
    last_interaction: "Book 2, Ch. 12"
---
```

### Character Knowledge
Track what each character knows:
```yaml
---
knows:
  - "[[The Secret of Oakhaven]]" — learned in Book 1, Ch. 5
  - "[[Marcus is a spy]]" — suspected Book 2, Ch. 3, confirmed Book 2, Ch. 8
does_not_know:
  - "[[The prophecy]]" — only readers know this
---
```

### Published vs. Draft
Mark which details are in print:
```yaml
---
canon_status: published  # published = immutable, draft = changeable
published_in: "Book 1"
---
```

## Checking for Contradictions

### Automated Checks

`scripts/validate_world.py` checks for:
- Eye color changes between notes
- Age timeline inconsistencies
- Magic rule violations (keyword matching)
- Broken wikilinks

### Manual Checks

For deeper continuity, the skill instructs Claude to:

1. **Read all character notes** — extract physical descriptions
2. **Read all scenes** — check descriptions match
3. **Build timeline** — verify ages add up
4. **Check magic rules** — flag any scene that violates established rules
5. **Track information flow** — ensure characters only know what they've experienced

## Contradiction Report Format

```markdown
> [!danger] Continuity Error
> **Character:** Elena Vareth
> **Issue:** Eye color changed from blue (Book 1, Ch. 3) to green (Book 3, Ch. 7)
> **References:** [[Book 1 - Chapter 3#Elena's Introduction]], [[Book 3 - Chapter 7#The Mirror]]
> **Severity:** High (physical description, reader-facing)
> **Fix:** Change to blue in Book 3, Ch. 7 or add scene explaining the change
```

## Severity Levels

| Severity | Description | Action |
|----------|-------------|--------|
| High | Reader-facing contradiction (eye color, names, deaths) | Must fix |
| Medium | Internal inconsistency (timeline off by days, minor details) | Should fix |
| Low | Style inconsistency (tone shifts, naming patterns) | Consider fixing |

## Series Bible Automation

The skill can auto-generate a series bible from existing vault content:

1. **Character Bible:** All characters with physical descriptions, relationships, arcs
2. **Timeline Bible:** All events in chronological order with dates
3. **Rules Bible:** All established world rules (magic, technology, physics)
4. **Knowledge Bible:** What each character knows at each point in the story

## Workflow for Continuity Checks

1. Run `scripts/validate_world.py --vault /path --level full`
2. Review the report for automated catches
3. Ask Claude to do deep continuity review of specific scenes
4. Fix contradictions
5. Mark corrected notes with `#needs-review` tag removed
