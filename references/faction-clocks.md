# Faction Clocks Reference

Blades in the Dark-style faction progression system.

## How It Works

Each faction has one or more "clocks" — circular progress trackers that advance independently of player action. When a clock fills, something significant happens in the world.

## Clock Sizes

| Size | Use Case |
|------|----------|
| 4 segments | Quick, small goals |
| 6 segments | Standard faction goals |
| 8 segments | Major, world-changing events |
| 10 segments | Epic, campaign-defining arcs |

## When Clocks Advance

### Between Sessions (DM Discretion)
- Roll 1d6 for each active clock
- On a 5-6, advance the clock by 1
- Modify based on player actions (helped/hindered the faction)

### In Response to Events
- Player action helps faction: advance clock
- Player action hinders faction: don't advance or rewind
- Major world event: advance related clocks

### Automatic Triggers
- Certain quest completions advance specific clocks
- Time skips advance all clocks by proportional amount

## Creating Clocks

### Frontmatter
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
  - "Necropolis manifested, city under siege"
---
```

### Trigger Design
Each trigger should:
1. Be observable by players
2. Escalate in severity
3. Create new hooks or complications
4. Affect existing world elements

## Clock Interactions

### Competing Clocks
Two factions racing toward conflicting goals. When one advances, the other may slow.

### Dependent Clocks
One clock can't complete until another fills. Creates sequential story beats.

### Cascade Clocks
When one clock fills, it automatically advances another faction's clock.

## Example Clock Web

```
Cult of Orcus: "Raise Necropolis" (6 segments)
  ↓ fills triggers
City Guard: "Martial Law" (4 segments)
  ↓ fills triggers
Merchant Guild: "Emergency Trade" (4 segments)
  ↓ fills triggers
Thieves Guild: "Exploit Chaos" (6 segments)
```

## Clock Tracking in Obsidian

### Visual Progress
Use checkboxes in the clock note:
```markdown
## Progress
- [x] Segment 1
- [x] Segment 2
- [x] Segment 3
- [ ] Segment 4
- [ ] Segment 5
- [ ] Segment 6
```

### Dataview Query
```dataview
TABLE WITHOUT ID
  file.link AS "Faction",
  clock_name AS "Clock",
  clock_filled AS "Filled",
  clock_size AS "Size",
  round((clock_filled / clock_size) * 100) AS "% Complete"
FROM "03_Organizations"
WHERE type = "faction-clock"
SORT clock_filled DESC
```

## DM Tips

1. **Don't tell players about clocks.** Let them observe the effects, not the mechanism.
2. **Advance clocks in the background.** Between sessions, not during.
3. **Make clocks visible through fiction.** NPCs mention events, rumors circulate.
4. **Let players interfere.** If they stop a clock, it rewinds or stalls.
5. **Have backup clocks.** If players stop one, another faction fills the vacuum.
