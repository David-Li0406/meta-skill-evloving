# Haunt Module

Create Haunts (personal or shared refuges) for W20 wraiths.

## What is a Haunt?

A Haunt is a location in the Shadowlands where a wraith has established a sanctuary. It provides:
- **Shroud Reduction**: Easier to affect the Skinlands
- **Safe Slumber**: Secure place to rest
- **Maelstrom Protection**: Shelter from spectral storms
- **Pathos Gathering**: Some Haunts accumulate Memoriam

## Core Statistics

### Rating (1-5)

| Rating | Size | Shroud Reduction | Capacity |
|--------|------|------------------|----------|
| 1 | Small (closet, phone booth) | -1 | 1 wraith |
| 2 | Survival-sized (small room) | -2 | 1 wraith |
| 3 | Fair-sized (apartment) | -3 | 2-3 wraiths |
| 4 | Opulent OR Special | -4 | 4 wraiths |
| 5 | Majestic (mansion) | -5 | 5+ wraiths |

**Rating 4 "Special"**: Mobile Haunt, heavily defended, hidden, etc.

### Skinlands Correspondence

Every Haunt corresponds to a physical location in the Skinlands:
- Usually connected to a Fetter or Passion
- Skinlands location often appears run-down or abandoned
- Location should make narrative sense for the character

---

## Haunt Types

### Personal Haunt
- Single wraith owner
- Connected to personal Fetters/Passions
- Full Background dots benefit owner

### Shared Haunt
- Multiple wraiths pool Background dots
- Trust required (sharing a Haunt is intimate)
- Benefits split among inhabitants

### Fetter-Haunt
- Haunt IS a Fetter
- Rare and powerful
- Double significance if threatened

---

## Creation Workflow

1. **Rating** — 1-5 (from Background dots)
2. **Location** — Skinlands correspondence
3. **History** — Why this place matters
4. **Features** — Physical description
5. **Defenses** — Protection measures
6. **Advantages** — Special benefits
7. **Threats** — Potential dangers
8. **Validate**

---

## Haunt Features

### Standard Features (by Rating)

| Rating | Features |
|--------|----------|
| 1 | Basic shelter, minimal comfort |
| 2 | Functional space, some amenities |
| 3 | Comfortable, defensible, storage |
| 4 | Luxurious, multiple rooms, strong defenses |
| 5 | Palatial, extensive grounds, formidable |

### Special Features (Storyteller Discretion)

| Feature | Effect |
|---------|--------|
| **Memoriam Gathering** | Generates Pathos passively |
| **Nihil Proximity** | Quick escape route (risky) |
| **Historical Resonance** | Enhanced Arcanos effects |
| **Hidden Entrance** | Difficult to locate |
| **Warded** | Resistant to Spectres |

### Dangers

| Danger | Description |
|--------|-------------|
| **Contested** | Others claim the space |
| **Exposed** | Easily found by enemies |
| **Skinlands Activity** | Living people frequent the area |
| **Unstable** | May shift or deteriorate |
| **Nihil Nearby** | Spectres can emerge |

---

## Location Examples

### Urban Haunts
- Abandoned apartment
- Condemned building
- Empty office
- Forgotten subway station
- Derelict warehouse

### Rural Haunts
- Old farmhouse
- Hunting cabin
- Cemetery mausoleum
- Covered bridge
- Collapsed mine entrance

### Mobile Haunts (Rating 4+)
- Ghost ship
- Spectral train car
- Haunted vehicle
- Wandering structure

### Famous Haunted Locations
- Already have strong Shroud reduction
- Often contested
- May have existing wraith inhabitants

---

## Output Format

```markdown
# [Haunt Name]

**Rating**: ●●●○○ (3)
**Type**: [Personal/Shared]
**Owner(s)**: [Wraith name(s)]

## Location

### Skinlands
[Physical address or description]
[Current state of the building/place]

### Shadowlands
[How it appears to wraiths]
[Notable differences from Skinlands appearance]

## History
[Why this place matters to the wraith]
[Any significant events that occurred here]

## Features

### Physical
- [Feature 1]
- [Feature 2]

### Supernatural
- **Shroud Reduction**: -[N]
- **Capacity**: [N] wraiths
- [Any special features]

## Defenses
- [Defense 1]
- [Defense 2]

## Threats
- [Potential danger 1]
- [Potential danger 2]

## Fetter Connection
[If the Haunt is connected to a Fetter, describe the link]
```

---

## Validation

- [ ] Rating 1-5
- [ ] Shroud reduction matches rating
- [ ] Skinlands location described
- [ ] Shadowlands appearance described
- [ ] History connects to owner's background
- [ ] Features appropriate to rating
- [ ] Defenses noted
- [ ] Potential threats identified

---

## Shared Haunt Rules

When multiple wraiths share a Haunt:

### Point Pooling
- Total rating = sum of all contributed Background dots
- Maximum rating 5 (excess points provide special features)

### Benefits
- All inhabitants gain Shroud reduction
- Safe space for Circle meetings
- Shared defense responsibilities

### Risks
- Conflict over space/resources
- One member's enemies become everyone's enemies
- Loss of one member may affect rating

---

## Reference Data

```bash
# Haunt rules
cat references/locations/haunt-rules.md

# Example Haunts
python scripts/lookup.py locations.example-haunts example-haunts --keys
```
