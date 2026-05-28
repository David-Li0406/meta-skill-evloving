# Kami Creation Module

Creates Kami—beings imbued with Gaia's essence for a specific purpose. The Gaian counterpart to fomori.

## Overview

Kami are humans, animals, plants, or places invested with Gaia's spirit. Unlike spirits bound to hosts, Kami are hosts imbued with Gaia herself. Each exists for a purpose only Gaia fully understands, bound by a geas they cannot break.

## Kami Types

| Type | Description | Gnosis | Willpower | Key Traits |
|------|-------------|--------|-----------|------------|
| Human | People blessed by Gaia | 1 (max 6) | 3 | Most flexible, 21 freebies |
| Animal | Creatures serving Gaia | 3 (max 8) | 2 | Species powers free |
| Plant | Sentient flora | 5 (max 10) | 3 | Immobile, alien |
| Land | Living ecosystems | 5 (max 10) | 3 | Most powerful, slowest |
| Rorqual | Whale-Kami | 3+ | 3+ | Mobile caerns for Rokea |

## Workflow

### Step 1: Determine Type and Purpose
```
Purpose examples:
- Protect endangered species
- Guard a sacred place
- Shelter travelers
- Nurture dreaming children
- Guide lost Kinfolk to safety
```

### Step 2: Create Geas
Every Kami has a restriction tied to their purpose. Breaking it costs powers.

**Geas Examples:**
| Type | Example Geasa |
|------|---------------|
| Prohibition | Never eat what you didn't prepare |
| Movement | Travel only by means Gaia gave you |
| Hospitality | Shelter all who ask, even enemies |
| Protection | Nothing deserves to suffer |
| Duty | Let the children dream |
| Passive | Never stop moving |

### Step 3: Allocate Attributes

**Human Kami:**
- Primary: 6 dots
- Secondary: 4 dots
- Tertiary: 3 dots
- (Each Attribute starts at 1)

**Animal/Plant/Land Kami:**
- Same allocation (6/4/3)
- Animals favor Physical/Mental over Social
- Plant/Land may not use some Attributes actively

### Step 4: Allocate Abilities

| Type | Primary | Secondary | Tertiary | Restrictions |
|------|---------|-----------|----------|--------------|
| Human | 13 | 9 | 5 | None |
| Animal | 11 | 7 | 3 | Lupus restrictions apply |
| Plant/Land | 11 | 7 | 3 | Many passive only |

### Step 5: Select Powers

**Power Allocation:**
- All Kami: 1-3 powers based on purpose
- Animal Kami: +up to 3 species powers free (Wings, Claws/Fangs, etc.)
- All Animal Kami: Immunity to Delirium free

**Consult:** `lookup.py kami.powers powers`

### Step 6: Size Adjustments (Animals Only)

| Size Category | Examples | Adjustment |
|---------------|----------|------------|
| Larger than human | Lion, horse | Size x1 (free) |
| Elephant/orca size | Elephant, orca | Size x2 (free) |
| Massive | Rorqual whales | Use Land rules |
| Large dog | Wolves, large dogs | Size x1 reductive |
| House cat/fox | Cats, foxes | Size x2 reductive |
| Tiny | Mice, small birds | Size x3 reductive |

Minimum 7 Health Levels regardless of size.

### Step 7: Backgrounds

**Human Kami (5 dots):**
- Allies, Contacts, Resources (max 3 each)
- Fate (minimum 1, up to 5)

**Animal Kami (3 dots):**
- Fate (minimum 1)
- Allies, Contacts (if social enough)
- Resources rarely applicable

**Plant/Land Kami:**
- Typically Fate only
- May have spiritual Allies

### Step 8: Freebies (Human Only)

Human Kami receive 21 freebie points.

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Background | 1 |
| Kami Power | 7 |
| Willpower | 1 |
| Gnosis | 2 |

### Step 9: Gnosis Enhancement

**Spirit Ties Power:**
| Type | Base Gnosis | Max with Spirit Ties |
|------|-------------|---------------------|
| Human | 1 | 6 |
| Animal | 3 | 8 |
| Plant/Land | 5 | 10 |

**Berserker Power:** Grants 5 Rage (Kami normally have no Rage)

---

## Special: Rorqual (Whale-Kami)

Massive whale Kami that serve as mobile caerns for the Rokea.

**Unique Traits:**
- All possess Wellspring power free
- May take: Lord of the Land, Moonstone, Spirit Den
- Function as migrating sacred sites
- Extremely rare and ancient

**Creation:** Use Land Kami rules with appropriate marine modifications.

---

## Kami Becoming

The process of becoming Kami is slow:
- **Animals:** Several reproductive cycles
- **Humans:** Up to a decade
- **Plants:** Extended lifespan during transformation
- **Land:** Century or more

**Acceleration Factors:**
- Proximity to other Kami
- Near caerns or thin Gauntlet
- Presence of shapeshifters

**Interruption:** Proto-Kami destroyed before transformation yield 1-5 Gnosis when consumed. DNA (Developmental Neogenics Amalgamated) hunts "Aberrant Cradles." Wyrm-blessed fomori can detect proto-Kami.

---

## Breaking Geasa

| Severity | Consequence |
|----------|-------------|
| Minor breach | Lose 1 power temporarily |
| Moderate breach | Lose multiple powers |
| Severe breach | Lose all powers |
| Plant/Land breach | May lose sentience entirely |

**Absolution:** Correct the mistake, commune with Gaia, or perform great service.

---

## Validation Checklist

- [ ] Type selected with clear purpose
- [ ] Geas defined and specific
- [ ] Attributes allocated correctly for type
- [ ] Abilities allocated with restrictions observed
- [ ] 1-3 purpose powers selected
- [ ] Species powers added (animals)
- [ ] Size adjustments applied (animals)
- [ ] Backgrounds allocated with Fate minimum 1
- [ ] Freebies spent (humans only)
- [ ] Gnosis/Willpower set per type

---

## Output Template

```markdown
# [Name]
## [Type] Kami

**Purpose:** [What Gaia created them for]

**Geas:** [Their restriction/taboo]

### History
[Background and how they came to Gaia's service]

### Appearance
[Physical description, both mundane and spiritual]

### Roleplaying Notes
[Personality, motivations, how they fulfill purpose]

### Traits

**Physical:** Strength X, Dexterity X, Stamina X
**Social:** Charisma X, Manipulation X, Appearance X
**Mental:** Perception X, Intelligence X, Wits X

**Talents:** [List with ratings]
**Skills:** [List with ratings]
**Knowledges:** [List with ratings]

**Powers:** [List of Kami powers]

**Gnosis:** X; **Willpower:** X; **Rage:** X (if Berserker)

### Backgrounds
[If applicable]

### Plot Hooks
- [Story seed 1]
- [Story seed 2]
- [Story seed 3]
```
