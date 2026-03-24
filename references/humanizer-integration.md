# Humanizer Integration Reference

Making worldbuilding text sound like it was written by people, not AI.

## Banned Patterns (Auto-Flagged)

### Words to Remove
| Banned | Why | Replace With |
|--------|-----|-------------|
| delve | Overused AI word | explore, dig into, investigate |
| tapestry | Cliché metaphor | web, pattern, mess, tangle |
| vibrant | Vague adjective | specific color/texture |
| serves as | Copula avoidance | is, works as, acts as |
| stands as | Copula avoidance | is, remains, endures as |
| pivotal role | Generic importance | specific impact |
| nestled in | Location cliché | sits in, hides in, sprawls across |
| rich history | Vague praise | specific events, named eras |
| ancient civilization | Generic backstory | named culture, specific people |
| looms | Drama word | grows, spreads, approaches |
| ancient prophecy | Fantasy cliché | specific text, named prophet |
| realm | Generic fantasy | named place, "the country," "this land" |
| forge/forge ahead | Overused verb | build, create, push through |

### Patterns to Avoid
- **Rule of three:** "brave, strong, and wise" — pick the most specific one
- **Em dash overuse:** — use periods and commas instead — mix it up
- **Copula avoidance:** "serves as a testament" → "shows" or "proves"
- **Formulaic structure:** Hook → History → Current → Future (every time)
- **Vague attributions:** "many believe" → "the farmers of Thornwall believe"

## Injection Rules (Make It Sound Human)

### Have Opinions
**AI:** "The city has a complex history spanning centuries."
**Human:** "Most people in Aldenmere will tell you the city was founded by heroes. The sewer workers know better — it was founded by people who didn't want to deal with the smell."

### Vary Rhythm
**AI:** "The forest is vast and ancient and mysterious and dangerous."
**Human:** "The Ashwood is old. Older than the kingdom. Older than the language we're speaking. Some of the trees remember when the gods still walked, and they don't think much of what we've done with the place."

### Be Specific
**AI:** "The tavern has a distinct atmosphere."
**Human:** "The Broken Wheel smells like spilled ale and burnt mutton. A one-eyed dog sleeps under the bar. Three farmers argue about crop prices in the corner, and they've been arguing since noon."

### Add Mess
**AI:** "The kingdom was founded in the year 1023 by King Aldric the Great."
**Human:** "The kingdom claims it was founded in 1023 by Aldric the Great. The truth is messier — Aldric was one of five warlords who spent twenty years trying to kill each other before they got tired and agreed to share. The history books just skip the boring parts."

### Use Concrete Feelings
**AI:** "She felt anxious about the upcoming battle."
**Human:** "She couldn't stop checking her sword. Drew it, sheathed it, drew it again. Her palms were sweating and she kept wiping them on her trousers until the fabric was damp."

### Let Voices Differ
A priest writes differently than a merchant:
- **Priest:** "The Light of Pelor guides us through the darkness of uncertainty."
- **Merchant:** "Look, I don't care who's in charge as long as the roads are safe and the tariffs stay reasonable."

## Applied To

### Location Descriptions
Should read like a travel guide written by someone with opinions, not a Wikipedia entry.

### Faction Histories
Written by biased in-world chroniclers. One faction's hero is another's villain.

### NPC Dialogue
Distinct speech patterns. A soldier speaks differently than a scholar.

### Quest Hooks
Urgent, specific stakes. "The village well is poisoned and children are getting sick" beats "There's a mysterious problem in the village."

### Magic System Descriptions
Written by practitioners with theories, not encyclopedias with facts.

### Religious Texts
Written by believers with theological arguments, not neutral observers.

## Validation

`scripts/validate_world.py` checks for banned patterns and flags them. Fix by replacing with more specific, concrete language.
