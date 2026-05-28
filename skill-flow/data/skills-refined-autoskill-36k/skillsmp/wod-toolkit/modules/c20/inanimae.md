# Inanimae Module

Create Inanimae characters for C20—the elemental fae, spirits of nature's building blocks.

## What are Inanimae?

Inanimae are fae born from the elemental forces of nature—earth, water, fire, air, wood, and artificial materials. They are ancient, tied to physical elements, and perceive the world differently than Kithain.

## Inanimae vs. Kithain

| Aspect | Inanimae | Kithain |
|--------|----------|---------|
| Origin | Elemental forces | Human dreams |
| Body | Anchored to element | Mortal host |
| Perception | Elemental senses | Human-like |
| Glamour | Tied to element | From Dreaming |
| Banality | Vulnerable | Resistant |
| Aging | Extremely slow | Mortal-paced |

---

## Inanimae Phyla (Kiths)

### Glomes (Earth)
**Concept**: Stone and earth spirits, patient and enduring
- **Glamour**: 3 | **Willpower**: 6
- **Element**: Earth, stone, crystal, metal
- **Birthright**: Stone Form—become living stone
- **Frailty**: Slowness—cannot act quickly
- **Sliver**: Gems, precious stones

### Kuberas (Wood/Plants)
**Concept**: Forest spirits, growth and decay
- **Glamour**: 5 | **Willpower**: 4
- **Element**: Wood, plants, forests
- **Birthright**: Plant Bond—command vegetation
- **Frailty**: Rooted—tied to growing things
- **Sliver**: Seeds, living wood

### Ondines (Water)
**Concept**: Water spirits, fluid and changeable
- **Glamour**: 5 | **Willpower**: 4
- **Element**: Water, rivers, seas, rain
- **Birthright**: Water Form—become liquid
- **Frailty**: Desiccation—suffer away from water
- **Sliver**: Shells, coral, pearls

### Parosemes (Air)
**Concept**: Air spirits, swift and ephemeral
- **Glamour**: 6 | **Willpower**: 3
- **Element**: Air, wind, weather
- **Birthright**: Wind Form—become intangible
- **Frailty**: Flighty—difficulty focusing
- **Sliver**: Feathers, captured breath

### Solimonds (Fire)
**Concept**: Fire spirits, passionate and consuming
- **Glamour**: 6 | **Willpower**: 4
- **Element**: Fire, heat, light
- **Birthright**: Flame Form—become living fire
- **Frailty**: Consumption—must burn to live
- **Sliver**: Ash, burnt items, flame-forged

### Mannikins (Artificial)
**Concept**: Spirits of crafted things, urban elementals
- **Glamour**: 4 | **Willpower**: 5
- **Element**: Crafted materials, machines, cities
- **Birthright**: Object Bond—inhabit artificial things
- **Frailty**: Unnatural—rejected by natural elements
- **Sliver**: Machine parts, crafted objects

Reference: `lookup.py gallain.inanimae inanimae`

---

## The Anchor System

Inanimae are **Anchored** to their element—they must maintain connection to survive.

### Anchor Types

| Type | Description |
|------|-------------|
| **Husk** | Material body (like changeling mortal seeming) |
| **Sliver** | Portable piece of element |
| **Anchor Site** | Fixed location of element |

### Anchor Mechanics

- Must remain near Anchor or suffer
- Anchor can be targeted by enemies
- Destroying Anchor may destroy Inanimae
- Can have multiple Anchors

---

## Slivers

A **Sliver** is a portable piece of an Inanimae's element:

| Phylum | Example Slivers |
|--------|-----------------|
| Glome | Gemstone, metal nugget |
| Kubera | Living seed, wooden token |
| Ondine | Vial of water, pearl |
| Paroseme | Captured wind, feather |
| Solimond | Eternal flame, warm coal |
| Mannikin | Gear, circuit, tool |

**Sliver Protection**: Inanimae can retreat into Sliver for safety.

---

## Creation Differences

| Category | Kithain | Inanimae |
|----------|---------|----------|
| Attributes | 7/5/3 | 6/5/4 |
| Abilities | 13/9/5 | 11/7/4 |
| Backgrounds | 5 | 5 |
| Arts | 3 | 2 + Phylum Art |
| Realms | 5 | 5 |
| Glamour | By kith | By phylum |
| Willpower | By kith | By phylum |
| Banality | By seeming | 2 (all) |
| Freebies | 15 | 15 |

---

## Creation Steps

1. **Concept** — Phylum, elemental nature
2. **Anchor Type** — Husk, Sliver, or Site
3. **Attributes** — 6/5/4 across Physical/Social/Mental
4. **Abilities** — 11/7/4 (cap 3)
5. **Backgrounds** — 5 dots (limited selection)
6. **Arts** — 2 dots + free Phylum Art
7. **Realms** — 5 dots
8. **Glamour** — By phylum
9. **Willpower** — By phylum
10. **Banality** — 2
11. **Birthrights & Frailty** — From phylum
12. **Freebies** — 15
13. **Validate**

---

## Phylum Arts

Each phylum has a unique Art:

| Phylum | Art | Focus |
|--------|-----|-------|
| Glome | Petros | Earth/stone manipulation |
| Kubera | Verdage | Plant manipulation |
| Ondine | Aquis | Water manipulation |
| Paroseme | Stratus | Air/weather manipulation |
| Solimond | Pyretics | Fire manipulation |
| Mannikin | Kineticis | Machine manipulation |

**Free Art**: Inanimae get 1 dot in their Phylum Art free.

---

## Inanimae Backgrounds

Limited selections:

| Background | Available | Notes |
|------------|-----------|-------|
| Anchor | Yes (special) | Strength of elemental connection |
| Chimera | Yes | Often elemental creatures |
| Holdings | Limited | Elemental-touched only |
| Mentor | Yes | Elder Inanimae |
| Resources | Limited | From elemental sources |
| Retinue | Yes | Elemental servants |

### Special Background: Anchor

| Dots | Anchor Strength |
|------|-----------------|
| 1 | Single weak anchor |
| 2 | One strong or two weak |
| 3 | Multiple anchors |
| 4 | Very strong connection |
| 5 | Legendary anchor |

---

## Inanimae Perception

Inanimae perceive the world through their element:

| Phylum | Primary Sense |
|--------|---------------|
| Glome | Vibration, pressure, density |
| Kubera | Growth, decay, life energy |
| Ondine | Flow, moisture, temperature |
| Paroseme | Sound, movement, pressure |
| Solimond | Heat, light, energy |
| Mannikin | Function, structure, purpose |

---

## Banality and Inanimae

Inanimae start with Banality 2 but are **vulnerable**:

| Situation | Effect |
|-----------|--------|
| Away from element | Discomfort, Glamour loss |
| Banal environment | Severe drain |
| Element destroyed | Possible death |
| Cold Iron | Devastating |

### Elemental Refuge
Inanimae can retreat to pure elemental environments to recover.

---

## Output Format

```markdown
# [Character Name]

**Type**: Inanimae
**Phylum**: [Glome/Kubera/Ondine/etc.]
**Anchor Type**: [Husk/Sliver/Site]
**Element**: [Specific element]
**Location**: [Where they dwell]

## Concept
[Description of this elemental spirit]

## Anchor

### Type
[Husk/Sliver/Site]

### Description
[What the anchor is, where it is]

### Vulnerability
[How the anchor could be threatened]

## Attributes

### Physical
| Attribute | Rating |
|-----------|--------|
| Strength | ●●●○○ |
| Dexterity | ●●○○○ |
| Stamina | ●●●○○ |

### Social
[etc.]

### Mental
[etc.]

## Abilities
[Standard format]

## Advantages

### Backgrounds
| Background | Rating |
|------------|--------|
| Anchor | ●●●○○ |
| [Background] | ●●○○○ |

### Arts
| Art | Rating |
|-----|--------|
| [Phylum Art] | ●●○○○ |
| [Other Art] | ●○○○○ |

### Realms
| Realm | Rating |
|-------|--------|
| [Realm] | ●●○○○ |

## Birthrights & Frailty

### Birthrights
- **[Birthright Name]**: [Description]

### Frailty
- **[Frailty Name]**: [Description]

## Vital Statistics

| Stat | Rating |
|------|--------|
| Glamour | ●●●●●○○○○○ |
| Willpower | ●●●●○○○○○○ |
| Banality | ●●○○○○○○○○ |

## Elemental Form
[Description of pure elemental appearance]

## Material Form
[Description when manifesting physically]

## Elemental Perception
[How they perceive the world through their element]

## History
[Ancient history, awakening, current situation]

## Motivation
[What drives them]
```

---

## Validation

- [ ] Phylum selected
- [ ] Anchor type specified
- [ ] Anchor described
- [ ] Attributes: 15 dots (6/5/4)
- [ ] Abilities: 22 dots (11/7/4)
- [ ] Arts: 3 dots total (including free Phylum Art)
- [ ] Realms: 5 dots
- [ ] Backgrounds: 5 dots (valid selections)
- [ ] Anchor background included
- [ ] Banality: 2
- [ ] Birthrights and Frailty from phylum

---

## Reference Data

```bash
# Inanimae phyla
python scripts/lookup.py gallain.inanimae inanimae "Glome"

# Phylum Arts
python scripts/lookup.py arts.phylum-arts phylum-arts "Petros"

# Anchor mechanics
python scripts/lookup.py gallain.anchors anchors --all
```
