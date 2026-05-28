# Treasure Module

Create magical Treasures for C20—enchanted items with cantrip powers, both crafted and imbued.

## Treasure vs. Chimera

| Aspect | Treasure | Chimera (Item) |
|--------|----------|----------------|
| Nature | Enchanted with cantrip power | Pure dreamstuff |
| Creation | Crafted or imbued with Glamour | Dreamed into existence |
| Power | Active magical effects | Passive or physical only |
| Activation | Costs Glamour | Usually free |
| Visibility | Often visible to mortals | Fae sight only (unless Wyrd) |

**Rule**: If an item has active magical powers (cantrip-like effects), it's a Treasure. Simple chimerical weapons/armor are Chimera.

## Treasure Types

| Type | Description | Creation |
|------|-------------|----------|
| **Crafted** | Made with Art of Infusion | Requires Infusion Art |
| **Imbued** | Glamour poured into existing item | Requires Glamour investment |
| **Dross** | Solidified Glamour | Natural or created |
| **Token** | Minor magical trinket | Various |

---

## Treasure Rating

| Rating | Power Level | Glamour Pool | Examples |
|--------|-------------|--------------|----------|
| 1 | Token | 1-2 | Lucky charm, glowing stone |
| 2 | Minor | 3-4 | Seeing glass, truthstone |
| 3 | Useful | 5-7 | Healing salve, flying cloak |
| 4 | Powerful | 8-10 | Flaming sword, invisibility ring |
| 5 | Legendary | 11+ | Caliburn, artifacts of legend |

### Treasure Background Conversion
| Background Dots | Treasure Value |
|-----------------|----------------|
| 1 | Single Token or Rating 1 Treasure |
| 2 | Rating 2 Treasure or 2 Tokens |
| 3 | Rating 3 Treasure |
| 4 | Rating 4 Treasure or multiple lower |
| 5 | Rating 5 Legendary Treasure |

---

## Creation Workflow

1. **Concept** — Purpose, form, origin
2. **Type** — Crafted, Imbued, or Dross
3. **Rating** — Power level (1-5)
4. **Physical Form** — What the item looks like
5. **Powers** — Cantrip effects it can produce
6. **Activation** — How to use, Glamour cost
7. **Limitations** — Restrictions, drawbacks
8. **Origin** — How it was created
9. **Validate**

---

## Treasure Powers

Treasures contain cantrip effects. Define each power as:

### Power Components
| Component | Description |
|-----------|-------------|
| **Effect** | What the power does |
| **Art** | Which Art it emulates |
| **Realm** | Target type (Actor, Fae, etc.) |
| **Activation** | Glamour cost, action required |
| **Duration** | How long it lasts |
| **Limit** | Uses per day/scene |

### Power Examples

| Power | Art | Effect | Typical Cost |
|-------|-----|--------|--------------|
| Concealment | Chicanery | Become invisible | 1 Glamour |
| Fae Sight | Soothsay | See through illusions | 1 Glamour |
| Healing Touch | Primal | Heal wounds | 2 Glamour |
| Swift Travel | Wayfare | Teleport short distances | 2 Glamour |
| Command | Sovereign | Give compelling order | 2 Glamour |
| Dream Gate | Wayfare | Open portal to Dreaming | 3 Glamour |
| Shapeshifting | Metamorphosis | Change form | 2 Glamour |
| Balefire Strike | Pyretics | Fire attack | 2 Glamour |

---

## Crafted Treasures (Infusion Art)

Created using the Infusion Art. Requires:

### Creation Requirements
| Rating | Infusion Level | Glamour Cost | Time |
|--------|----------------|--------------|------|
| 1 | 1 | 5 | Hours |
| 2 | 2 | 10 | Day |
| 3 | 3 | 15 | Week |
| 4 | 4 | 25 | Month |
| 5 | 5 | 40+ | Year+ |

### Crafted Treasure Rules
- Creator must know the Arts being infused
- Glamour is permanently invested
- May require special materials
- Higher rating = more powers or stronger single power

---

## Imbued Treasures

Created by pouring Glamour into an existing item over time.

### Imbuing Process
1. Select appropriate vessel (item with symbolic connection)
2. Spend Glamour over extended period
3. Item gains power based on Glamour invested

### Natural Imbuing
Some items become Treasures through:
- Prolonged exposure to Glamour
- Significant emotional events
- Connection to powerful Dreamers
- Found in the Dreaming

---

## Dross

Solidified Glamour in physical form.

### Dross Types
| Type | Form | Glamour Content |
|------|------|-----------------|
| Pebble | Small stone | 1 Glamour |
| Crystal | Gem-like | 2-3 Glamour |
| Sculpture | Shaped form | 3-5 Glamour |
| Pool | Liquid | Variable |

### Dross Uses
- Consume to regain Glamour
- Trade as currency among fae
- Power Treasures
- Fuel powerful cantrips

---

## Special Treasure Properties

### Positive Properties
| Property | Effect |
|----------|--------|
| Loyal | Returns to owner |
| Glamour Battery | Stores extra Glamour |
| Self-Charging | Regenerates power |
| Intelligent | Has awareness/personality |
| Linked | Bonded to specific user |
| Dual-Natured | Visible to mortals AND fae |

### Negative Properties (Flaws)
| Property | Effect |
|----------|--------|
| Hungry | Drains Glamour from user |
| Fragile | Easily damaged |
| Temperamental | Doesn't always work |
| Cursed | Has negative side effect |
| Possessive | Jealous of other items |
| Visible | Cannot be hidden |

---

## Treasures of Banality

Dark treasures infused with Banality rather than Glamour. Weapons of the Dauntain and enemies of the Dreaming.

| Type | Effect |
|------|--------|
| Iron Token | Inflicts Banality damage |
| Banality Trap | Drains Glamour from area |
| Dream Cage | Imprisons chimera |
| Forgetfulness Stone | Causes Mists effect |

**Warning**: Creating or using Treasures of Banality may be considered hostile by other Kithain.

---

## File Structure

```
[project]/
├── treasures/
│   ├── [treasure_name].md
│   └── ...
```

---

## Output Format

```markdown
# [Treasure Name]

**Rating**: [1-5] ●●●○○
**Type**: [Crafted/Imbued/Dross]
**Form**: [Physical description]
**Owner**: [Current owner, if any]

## Concept
[Brief description of what this treasure is and does]

## Appearance
[Detailed physical description]

## Powers

### [Power Name]
**Art Emulated**: [Art]
**Realm**: [Realm]
**Effect**: [What it does]
**Activation**: [How to use it]
**Cost**: [Glamour cost]
**Duration**: [How long it lasts]
**Limit**: [Uses per day/scene, if any]

### [Additional Power Name]
[Same format]

## Properties

| Property | Effect |
|----------|--------|
| [Property] | [Description] |

## Glamour Pool
**Maximum**: [N] Glamour
**Recharge**: [How it regains Glamour]

## Limitations
- [Limitation 1]
- [Limitation 2]

## Origin
[How the treasure was created, its history]

## Current Status
[Where it is now, who has it, any active plots]
```

---

## Example Treasures

### The Moonstone Pendant (Rating 2)
- **Type**: Imbued
- **Form**: Silver pendant with opalescent stone
- **Power**: Chicanery 2 effect—wearer can create minor illusions
- **Cost**: 1 Glamour per use
- **Glamour Pool**: 4
- **Origin**: Belonged to an Eiluned seer, absorbed dreams over centuries

### Thornblade (Rating 4)
- **Type**: Crafted
- **Form**: Elegant sword with rose-thorn hilt
- **Powers**: 
  - Primal 3 attack (entangling thorns on hit)
  - Wayfare 2 (blade returns when thrown)
- **Cost**: 1 Glamour per power
- **Glamour Pool**: 8
- **Properties**: Loyal (returns to owner), Living (thorns grow)
- **Limitation**: Only bonds with one owner at a time

---

## Validation

- [ ] Rating appropriate for power level
- [ ] Type specified (Crafted/Imbued/Dross)
- [ ] Powers clearly defined with Art/Realm
- [ ] Glamour costs specified
- [ ] Glamour pool set for rating
- [ ] Limitations noted
- [ ] Origin explained
- [ ] Matches Treasure background dots (if from character)

---

## Reference Data

```bash
# Treasure examples
python scripts/lookup.py chimera.treasures treasures "sword"

# Power templates
python scripts/lookup.py chimera.treasure-powers treasure-powers "healing"

# Art effects for treasures
python scripts/lookup.py arts.arts arts "Infusion"
```
