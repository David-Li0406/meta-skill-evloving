# Haunt Module

Create demon territories and gathering places.

## Overview

A Haunt is a location claimed by one or more demons as territory. Like vampire Elysiums or werewolf caerns, Haunts serve as meeting places, power bases, and refuges.

---

## Types of Haunts

### Personal Haunt
Territory of a single demon.
- **Size**: Single building or small area
- **Control**: Total authority
- **Use**: Refuge, thrall meetings, private business

### Court Haunt
Territory of an organized demon group.
- **Size**: Larger building or district
- **Control**: Shared among court members
- **Use**: Politics, gatherings, formal business

### Contested Haunt
Territory claimed by multiple parties.
- **Size**: Varies
- **Control**: Disputed
- **Use**: Neutral ground, dangerous meetings

### Sacred Haunt
Location with inherent supernatural significance.
- **Size**: Varies (often modest)
- **Control**: May resist control
- **Use**: Ritual, power gathering, pilgrimages

---

## Haunt Characteristics

### Location Rating (1-5)

| Rating | Description |
|--------|-------------|
| 1 | Minor location; small building or room |
| 2 | Modest location; house or small business |
| 3 | Significant location; large building or compound |
| 4 | Major location; estate, tower, or district |
| 5 | Legendary location; landmark or sacred site |

### Security Rating (1-5)

| Rating | Description |
|--------|-------------|
| 1 | Minimal; mundane locks only |
| 2 | Basic; alarms, guards, or wards |
| 3 | Moderate; multiple layers of protection |
| 4 | High; supernatural defenses active |
| 5 | Fortress; nearly impenetrable |

### Faith Resonance (0-5)

| Rating | Description |
|--------|-------------|
| 0 | Dead zone; difficult to use Faith here |
| 1 | Weak; normal Faith use |
| 2 | Moderate; +1 to Faith rolls |
| 3 | Strong; +2 to Faith rolls |
| 4 | Potent; +3 to Faith rolls, may attract attention |
| 5 | Sacred; +4 to Faith rolls, beacon to supernaturals |

### Concealment (1-5)

| Rating | Description |
|--------|-------------|
| 1 | Obvious; any supernatural can sense it |
| 2 | Noticeable; requires Awareness roll to detect |
| 3 | Hidden; requires active search to find |
| 4 | Secret; known only to those told |
| 5 | Legendary; existence doubted by most |

---

## Creating a Haunt

### Step 1: Concept

What is this place and why is it a Haunt?

| Type | Examples |
|------|----------|
| **Residence** | Apartment, house, mansion, hotel |
| **Business** | Club, restaurant, office, warehouse |
| **Institution** | Church, hospital, university, museum |
| **Landmark** | Monument, ruin, natural feature |
| **Underground** | Basement, tunnel, bunker, catacomb |

### Step 2: History

Every significant location has a past:
- Who built it and why?
- What significant events occurred here?
- Who held it before current owner?
- Why does it resonate with the supernatural?

### Step 3: Ratings

Assign dots (typically 5-10 total for starting Haunts):
- Location (1-5)
- Security (1-5)
- Faith Resonance (0-5)
- Concealment (1-5)

### Step 4: Features

What makes this Haunt special?

| Feature | Effect |
|---------|--------|
| **Library** | +2 to Research rolls |
| **Workshop** | +2 to Crafts rolls |
| **Sanctum** | Protected meditation space |
| **Holding Cells** | Secure containment |
| **Escape Routes** | Multiple exits |
| **Mundane Cover** | Legitimate business facade |
| **Thrall Quarters** | Housing for servants |
| **Ritual Chamber** | Space for ceremonies |

### Step 5: Defenses

How is the Haunt protected?

| Defense Type | Examples |
|--------------|----------|
| **Mundane** | Locks, alarms, guards, cameras |
| **Supernatural** | Wards, bound spirits, traps |
| **Social** | Police protection, mob ties, cult |
| **Concealment** | Hidden entrance, misdirection |

---

## Haunt Politics

### Claiming Territory

- Requires presence and assertion of control
- Other demons may challenge claims
- Courts may mediate disputes
- Violence often settles disagreements

### Neutral Ground

Some Haunts are designated neutral:
- No violence allowed
- Oaths of peace enforced
- Violations bring retribution from all
- Often used for negotiations

### Trespassing

Entering another's Haunt uninvited:
- Considered serious offense
- May trigger wards or alarms
- Justifies defensive response
- Formal complaint can be made to courts

---

## Special Haunts

### Reliquary Sites

Haunts containing an Earthbound:
- See `modules/d20/reliquary.md`
- Extremely high Faith Resonance
- Earthbound controls territory
- Very dangerous for other demons

### Contested Sites

Locations multiple parties want:
- Often sites of conflict
- May have rotating control
- Neutral zones sometimes established
- Resources attract competition

### Lost Haunts

Former Haunts now abandoned or lost:
- May contain valuable resources
- Often dangerous to explore
- Previous owners may have left traps
- Reclaiming requires effort

---

## Data Lookup

```bash
# Get haunt templates
python scripts/lookup.py d20.setting haunts "court-haunt"

# Search by feature
python scripts/lookup.py d20.setting haunts --find "ritual"
```

---

## Output Template

```markdown
# [Haunt Name]

**Type**: [Personal/Court/Contested/Sacred]
**Owner**: [Demon name or court]
**Location**: [City, neighborhood, address]

## Concept

[What is this place? What makes it significant?]

## Ratings

| Aspect | Rating | Notes |
|--------|--------|-------|
| Location | ●●●○○ | [Size and significance] |
| Security | ●●○○○ | [Defense level] |
| Faith Resonance | ●●○○○ | [Power level] |
| Concealment | ●●●○○ | [How hidden] |

## History

[Origin and significant events]

## Physical Description

### Exterior
[What it looks like from outside]

### Interior
[Layout and notable rooms]

### Hidden Areas
[Secret spaces, if any]

## Features

| Feature | Location | Effect |
|---------|----------|--------|
| [Feature] | [Where] | [Mechanical benefit] |

## Defenses

### Mundane
- [Defense 1]
- [Defense 2]

### Supernatural
- [Ward/trap 1]
- [Ward/trap 2]

## Inhabitants

### Demon(s)
- [Demon 1] — [Role]

### Thralls
- [Thrall 1] — [Role]

### Others
- [Mortal staff, etc.]

## Politics

**Claimed By**: [Who holds formal claim]
**Disputed By**: [Anyone challenging]
**Neutral Status**: [If neutral ground]
**Court Affiliation**: [If part of court territory]

## Current Events

[Recent developments affecting the Haunt]

## Map

[Link to map or description of layout]
```
