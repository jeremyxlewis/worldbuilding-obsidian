# Dataview Query Snippets

Use these queries in your vault dashboards. Copy and paste as needed.

## Characters by Faction

```dataview
TABLE WITHOUT ID
  file.link AS "Character",
  status AS "Status",
  location AS "Location"
FROM "01_Characters"
WHERE faction = "[[Faction Name]]"
SORT file.name ASC
```

## Characters by Location

```dataview
TABLE WITHOUT ID
  file.link AS "Character",
  role AS "Role",
  faction AS "Faction"
FROM "01_Characters"
WHERE location = "[[Location Name]]"
SORT file.name ASC
```

## Active Quests by Region

```dataview
TABLE WITHOUT ID
  file.link AS "Quest",
  quest_giver AS "Quest Giver",
  level_range AS "Level"
FROM "07_Quests_and_Adventures"
WHERE status = "active" AND region = "[[Region Name]]"
SORT file.name ASC
```

## Creatures by CR Range

```dataview
TABLE WITHOUT ID
  file.link AS "Creature",
  cr AS "CR",
  type AS "Type",
  habitat AS "Habitat"
FROM "09_Creatures"
WHERE cr >= 1 AND cr <= 5
SORT cr ASC
```

## Faction Clock Status

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

## Recent Session Notes

```dataview
TABLE WITHOUT ID
  file.link AS "Session",
  session_number AS "#",
  date AS "Date",
  summary AS "Summary"
FROM "10_Campaign"
WHERE type = "session-note"
SORT session_number DESC
LIMIT 10
```

## Magic Items by Rarity

```dataview
TABLE WITHOUT ID
  file.link AS "Item",
  type AS "Type",
  attunement AS "Attunement"
FROM "08_Items_and_Equipment"
WHERE rarity = "legendary" OR rarity = "very rare"
SORT rarity DESC
```

## Characters Without Faction

```dataview
TABLE WITHOUT ID
  file.link AS "Character",
  role AS "Role",
  location AS "Location"
FROM "01_Characters"
WHERE !faction
SORT file.name ASC
```

## Locations Without Description

```dataview
TABLE WITHOUT ID
  file.link AS "Location",
  type AS "Type"
FROM "02_Locations"
WHERE length(file.outlinks) < 2
SORT file.name ASC
```

## Timeline Events

```dataview
TABLE WITHOUT ID
  file.link AS "Event",
  era AS "Era",
  date AS "Date",
  significance AS "Significance"
FROM "06_History_and_Timeline"
SORT date ASC
```

## Word Count by Chapter (Novel)

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

## Scenes by POV Character

```dataview
TABLE WITHOUT ID
  file.link AS "Scene",
  chapter AS "Chapter",
  word_count AS "Words"
FROM "11_Manuscript"
WHERE type = "scene" AND pov = "[[Character Name]]"
SORT chapter ASC
```

## Orphaned Notes

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

## Recently Modified

```dataview
TABLE WITHOUT ID
  file.link AS "Note",
  file.folder AS "Folder",
  file.mtime AS "Modified"
FROM ""
WHERE file.folder != "_Templates" AND file.folder != "_Resources"
SORT file.mtime DESC
LIMIT 20
```

## Calendar View (Events)

```dataview
CALENDAR date
FROM "06_History_and_Timeline"
WHERE date
```

## Tag Cloud

```dataview
LIST length(rows)
FROM ""
FLATTEN file.tags as tag
WHERE tag
GROUP BY tag
SORT length(rows) DESC
LIMIT 30
```
