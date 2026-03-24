# Dataview Queries Reference

Pre-built queries for worldbuilding dashboards.

## Character Queries

### All Characters
```dataview
TABLE WITHOUT ID file.link AS "Name", status AS "Status", faction AS "Faction", location AS "Location"
FROM "01_Characters"
SORT file.name ASC
```

### By Faction
```dataview
TABLE WITHOUT ID file.link AS "Name", role AS "Role", location AS "Location"
FROM "01_Characters"
WHERE faction = "[[Faction Name]]"
SORT file.name ASC
```

### By Location
```dataview
TABLE WITHOUT ID file.link AS "Name", role AS "Role", faction AS "Faction"
FROM "01_Characters"
WHERE location = "[[Location Name]]"
SORT file.name ASC
```

### Protagonists
```dataview
TABLE WITHOUT ID file.link AS "Name", arc_status AS "Arc Status", first_appearance AS "First Appeared"
FROM "01_Characters"
WHERE role = "protagonist"
SORT file.name ASC
```

## Location Queries

### All Locations
```dataview
TABLE WITHOUT ID file.link AS "Name", type AS "Type", region AS "Region"
FROM "02_Locations"
SORT file.name ASC
```

### By Region
```dataview
TABLE WITHOUT ID file.link AS "Name", type AS "Type", population AS "Population"
FROM "02_Locations"
WHERE region = "[[Region Name]]"
SORT file.name ASC
```

## Quest Queries

### Active Quests
```dataview
TABLE WITHOUT ID file.link AS "Quest", quest_giver AS "Quest Giver", level_range AS "Level"
FROM "07_Quests_and_Adventures"
WHERE status = "active"
SORT file.name ASC
```

### Available Quests
```dataview
TABLE WITHOUT ID file.link AS "Quest", quest_giver AS "Quest Giver", region AS "Region"
FROM "07_Quests_and_Adventures"
WHERE status = "available"
SORT file.name ASC
```

## Faction Queries

### All Factions
```dataview
TABLE WITHOUT ID file.link AS "Faction", type AS "Type", influence AS "Influence", alignment AS "Alignment"
FROM "03_Organizations"
SORT influence DESC
```

### Faction Clocks
```dataview
TABLE WITHOUT ID file.link AS "Faction", clock_name AS "Clock", clock_filled AS "Filled", clock_size AS "Size"
FROM "03_Organizations"
WHERE type = "faction-clock"
SORT clock_filled DESC
```

## Campaign Queries

### Session History
```dataview
TABLE WITHOUT ID file.link AS "Session", session_number AS "#", date AS "Date", summary AS "Summary"
FROM "10_Campaign"
WHERE type = "session-note"
SORT session_number DESC
```

### Encounters
```dataview
TABLE WITHOUT ID file.link AS "Encounter", cr AS "CR", location AS "Location", status AS "Status"
FROM "07_Quests_and_Adventures"
WHERE type = "encounter"
SORT cr ASC
```

## Manuscript Queries

### Scenes
```dataview
TABLE WITHOUT ID file.link AS "Scene", chapter AS "Chapter", pov AS "POV", word_count AS "Words", status AS "Status"
FROM "11_Manuscript"
WHERE type = "scene"
SORT chapter ASC
```

### Chapters
```dataview
TABLE WITHOUT ID file.link AS "Chapter", chapter_number AS "#", word_count AS "Words", status AS "Status"
FROM "11_Manuscript"
WHERE type = "chapter"
SORT chapter_number ASC
```

## Utility Queries

### Orphaned Notes
```dataview
TABLE WITHOUT ID file.link AS "Note", file.folder AS "Folder"
FROM ""
WHERE length(file.inlinks) = 0 AND file.folder != "_Templates" AND file.folder != "_Resources" AND file.folder != "00_Dashboard"
SORT file.folder ASC
```

### Recently Modified
```dataview
TABLE WITHOUT ID file.link AS "Note", file.folder AS "Folder", file.mtime AS "Modified"
FROM ""
WHERE file.folder != "_Templates" AND file.folder != "_Resources"
SORT file.mtime DESC
LIMIT 20
```

### Tag Cloud
```dataview
LIST length(rows)
FROM ""
FLATTEN file.tags as tag
WHERE tag
GROUP BY tag
SORT length(rows) DESC
LIMIT 30
```

### Calendar View
```dataview
CALENDAR date
FROM "06_History_and_Timeline"
WHERE date
```
