# Reliquary Module

Create Earthbound prison-anchors.

## Overview

A reliquary is the physical object that anchors an Earthbound demon to the material world. Without a mortal host, the Earthbound requires this object to maintain existence outside the Abyss.

---

## Reliquary Types

| Type | Size | Durability | Power | Mobility |
|------|------|------------|-------|----------|
| **Portable** | Handheld to person-sized | Moderate | Limited | High |
| **Stationary** | Furniture to room-sized | High | Moderate | None |
| **Architectural** | Building or structure | Very High | High | None |
| **Natural** | Geographic feature | Extreme | Maximum | None |

---

## Creating a Reliquary

### Step 1: Physical Object

What is the reliquary?

| Category | Examples |
|----------|----------|
| **Idol** | Statue, figurine, mask, amulet |
| **Vessel** | Urn, box, chest, sarcophagus |
| **Weapon** | Sword, staff, dagger, axe |
| **Book** | Tome, scroll, tablet |
| **Furniture** | Throne, altar, mirror, bed |
| **Architecture** | Temple, tomb, tower, well |
| **Natural** | Stone, tree, cave, spring |

### Step 2: Origin

How was this reliquary created?

| Origin | Description |
|--------|-------------|
| **Crafted** | Made specifically to house the demon |
| **Claimed** | Existing object the demon bound to |
| **Evolved** | Started small, grew over time |
| **Corrupted** | Former holy object now tainted |

### Step 3: Ratings

| Aspect | Description | Rating |
|--------|-------------|--------|
| **Durability** | Resistance to damage | 1-5 |
| **Power Capacity** | How much Faith can be channeled | 1-5 |
| **Concealment** | How hidden from detection | 1-5 |
| **Mobility** | Ease of moving (if possible) | 0-3 |

### Step 4: Protection

How is the reliquary defended?

| Defense Type | Examples |
|--------------|----------|
| **Physical** | Vault, guards, traps |
| **Supernatural** | Wards, curses, bound spirits |
| **Social** | Cult guardians, false ownership |
| **Concealment** | Hidden location, disguise |

### Step 5: Vulnerability

Every reliquary can be destroyed. What is its weakness?

| Weakness Type | Examples |
|---------------|----------|
| **Material** | Must be melted, dissolved, burned |
| **Ritual** | Requires specific ceremony |
| **True Name** | Speaking demon's name weakens it |
| **Holy** | Blessed weapons, holy water |
| **Specific** | Unique requirement (blood of X, etc.) |

---

## Reliquary Mechanics

### Power Radius

Earthbound power diminishes with distance:

| Zone | Range | Power Level |
|------|-------|-------------|
| **Core** | Line of sight | Full |
| **Inner** | Building/compound | 75% |
| **Domain** | Neighborhood/area | 50% |
| **Reach** | City/region | 25% |
| **Beyond** | Outside reach | Cannot act directly |

### Destruction Effects

Destroying a reliquary harms but rarely kills an Earthbound:

| Destruction Level | Effect |
|-------------------|--------|
| **Damaged** | Earthbound weakened; Faith costs doubled |
| **Broken** | Earthbound banished temporarily |
| **Destroyed** | Earthbound cast into limbo; may reform over decades |
| **Annihilated** | Earthbound destroyed permanently (very rare) |

### Moving a Reliquary

If the reliquary is portable:
- Moving it moves the Earthbound's power center
- Requires significant Faith expenditure
- Vulnerable during transit
- May require cult support

---

## Historical Reliquaries

### Ancient Period
- Stone idols, bronze statues
- Often in temples or sacred groves
- Some became famous artifacts

### Medieval Period
- Relics in churches (corrupted)
- Weapons and armor
- Alchemical vessels

### Modern Era
- Art objects, antiques
- Corporate headquarters (architectural)
- Digital? (theoretically possible, highly experimental)

---

## Data Lookup

```bash
# Get reliquary templates
python scripts/lookup.py d20.setting reliquaries "portable"

# Search by material
python scripts/lookup.py d20.setting reliquaries --find "stone"
```

---

## Output Template

```markdown
# Reliquary: [Name]

**Earthbound**: [Demon name]
**Type**: [Portable/Stationary/Architectural/Natural]
**Age**: [How old]

## Physical Description

**Object**: [What it is]
**Material**: [What it's made of]
**Size**: [Dimensions]
**Appearance**: [Visual description]
**Markings**: [Symbols, inscriptions]

## Ratings

| Aspect | Rating | Notes |
|--------|--------|-------|
| Durability | ●●●○○ | [Description] |
| Power Capacity | ●●●●○ | [Description] |
| Concealment | ●●○○○ | [Description] |
| Mobility | ●○○○○ | [If applicable] |

## Origin

[How the reliquary came to be]

## Location

**Current Site**: [Where it is now]
**History**: [Previous locations]
**Environment**: [Surroundings]

## Protection

### Physical
- [Defense 1]
- [Defense 2]

### Supernatural
- [Ward/trap 1]
- [Ward/trap 2]

### Guardians
- [Who guards it]

## Vulnerability

**Known Weaknesses**:
- [Weakness 1]
- [Weakness 2]

**Destruction Requirements**:
[What would be needed to destroy it]

## Power Zones

| Zone | Range | Description |
|------|-------|-------------|
| Core | [Distance] | [What's in this zone] |
| Inner | [Distance] | [What's in this zone] |
| Domain | [Distance] | [What's in this zone] |
| Reach | [Distance] | [What's in this zone] |

## History

[Significant events in the reliquary's existence]

## Current Status

[Present situation, any ongoing events]

## Notes

[Additional information]
```
