# Black Spiral Dancer Module

Creates Black Spiral Dancer characters - the fallen Get of Fenris who serve the Wyrm. Use this module for creating BSDs as antagonists or (rarely) tragic player characters.

## Character Creation Differences

Black Spiral Dancers follow standard Garou creation with these modifications:

### Tribal Differences
- **Tribe**: Black Spiral Dancers (no other option)
- **Auspice**: Same five auspices, but all serve the Wyrm
- **Breed**: All three breeds exist; Metis are common and often favored
- **Willpower**: Starting Willpower 3 (not tribal variation)
- **Backgrounds**: Cannot take Pure Breed; can take Ancestors (corrupted), Fetish (Wyrm tainted), Totem (Wyrm totems only)

### The Dance of the Black Spiral
All Black Spirals have walked the Black Spiral Labyrinth in Malfeas. This rite of passage:
- Replaces standard Garou rite of passage
- Involves descending nine circles of the Spiral
- Each circle strips away Gaian beliefs
- Survivors emerge as Wyrm servants
- Some retain sanity; many gain derangements

### Renown
Black Spirals track Renown differently:
- **Infamy** (replaces Glory): Atrocities, victories against Gaians
- **Cunning** (same): Trickery, successful plots
- **Power** (replaces Honor): Dominance, Wyrm favor, spiritual might

## The Black Spiral Litany

The twisted mirror of the Gaian Litany:

1. **Reveal Your Secret Face to the Darkness of the World** - Show true corrupted nature to fellow Spirals
2. **Hunt Only for the Wyrm and Its Will** - All kills serve corruption
3. **Accept the Blight of the Wyrm** - Embrace Wyrm taint, don't resist
4. **Respect the Territory of the Powerful** - Might makes right
5. **Accept All Challenges from Those Above You** - Ritual combat for rank
6. **Submission to Those of Higher Station** - Hierarchy of power
7. **Offer the First Share of the Kill to Those of Greater Glory** - Feed the powerful first
8. **Do Not Consume the Flesh of Humans or Wolves** - (Often ignored; some hives keep it)
9. **Do As Your Elder Decrees** - Absolute obedience to rank
10. **Do Not Suffer the People of the Goddess to Live** - Gaians must die
11. **Respect Those Beneath You, for All Serve** - Even the weak have uses
12. **Guard the Wyrm's Secrets** - Protect hive locations, plans, identities

## Character Template

```
Name: [Name, often taking a "dark" name after the Dance]
Former Tribe: [Get of Fenris for most; rarely others who fell]
Breed: [Homid/Metis/Lupus]
Auspice: [Ragabash/Theurge/Philodox/Galliard/Ahroun]
Rank: [Typically use standard ranks, but called by Spiral names]

--- Attributes ---
[Standard allocation: 7/5/3]

--- Abilities ---
[Standard allocation: 13/9/5]

--- Advantages ---
Gifts: [3 starting - Breed, Auspice, Tribal]
Backgrounds: [5 points - no Pure Breed]
Renown: [By auspice, using Infamy/Cunning/Power]

--- Vitals ---
Rage: [By auspice]
Gnosis: [By breed]
Willpower: 3

--- Derangements ---
[Optional but common - result of the Dance]

--- Notes ---
Hive: [Home Pit]
Pack: [Pack name, totem]
Role: [Function within the hive]
```

## Reference Files

BSD content is integrated into standard Garou references:
- `lookup.py gift.gifts-by-source gifts-by-source` → "Black Spiral Dancers" entry in tribe_gifts
- `lookup.py rite.rites-by-type rites-by-type` → "wyrm_rites" section
- `lookup.py totem.totems totems` → "wyrm" category

BSD-specific content:
- `lookup.py black-spiral.pits pits` - Example hives/Pits
- `lookup.py black-spiral.litany litany` - Black Spiral Litany and Renown system
- `lookup.py rules.taint-mechanics taint-mechanics` - Wyrm taint, corruption, redemption

## The Pits (Hives)

Black Spiral gathering places. Four creation methods:

1. **Tunnels** - Dug beneath corrupted lands, connected to Malfeas
2. **Captured Caerns** - Former Gaian caerns, corrupted over time
3. **Undiscovered Sites** - Places of power Gaians never found
4. **Blighted Locations** - Sites of great tragedy/corruption

### Pit Elements
- **Balefire** - Corrupted sacred fire
- **Spiral Labyrinth** - Physical representation for the Dance
- **Breeding Pens** - Where Kinfolk are kept (traditional hives)
- **Shrine** - To the hive's patron Wyrm-spirit

## Kinfolk Relationships

Modern Black Spirals take two approaches:

**Traditional**: Kinfolk as breeding stock, kept in pens, treated as property
**Modern**: Kinfolk kept at distance, used as agents/spies, educated and useful

Many hives blend approaches - some Kinfolk are "investments" raised with care, others are expendable breeding stock.

## Special Abilities

### World-Strangling Ways
Technique for corrupting nature spirits into Banes. Theurges especially skilled at this.

### Flayers of the World's Skin
Ability to hollow out spirits and wear them as a "second hide" - disguise from Gaian senses.

### Communion with Ancients
Some Black Spirals seek pre-Gaian entities trapped in the Earth - spirits older than Gaia herself.

## Creating BSD Antagonists

For Storyteller use, consider:
- **Motivation**: Why do they fight? Revenge? Corruption? Madness?
- **Sanity Level**: How intact is their mind after the Dance?
- **Connections**: Ties to Pentex? Other hives? Maeljin?
- **Threat Level**: Solo operative or hive-supported?
