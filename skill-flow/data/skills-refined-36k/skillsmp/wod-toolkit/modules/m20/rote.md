# Rote Module

Design mechanically valid rotes for M20 using the Prism of Focus system with detailed Sphere reference integration.

## Context

| Context | Save Location | Constraints |
|---------|---------------|-------------|
| Standalone | `./rotes/` | Character's Spheres and Practices |
| Character | `[character]/rotes/` | Character's Spheres and Practices only |
| Grimoire | `[project]/rotes/` | Grimoire's Spheres/Practices/Abilities |
| Wonder | `[project]/rotes/` | Wonder's concept |

## What is a Rote?

A codified magical effect: roll **Attribute + Ability** instead of Arete.

Under Prism of Focus:
- Each rote is tied to a specific **Practice**
- The Ability must be **Associated** with that Practice
- Practice rating must be **high enough** for the effect's highest Sphere

## Creation Workflow

1. **Intent** — Effect, scope, target, duration
2. **Spheres** — Query `references/spheres/conjunctions.md` for effect requirements
3. **Verify Capabilities** — Read relevant `references/spheres/[sphere].md` to confirm effect is achievable
4. **Practice** — Must have sufficient rating (≥ highest Sphere used)
5. **Execution** — Instruments, performance (appropriate to Practice)
6. **Dice Pool** — Attribute + Ability (Ability must be Associated with Practice)
7. **Cost** — Total Sphere dots
8. **Paradox** — Use `references/spheres/mechanics.md` for vulgarity assessment
9. **Practice Modifiers** — Note any bonuses/penalties from Practice or Tenets
10. **Document** — Use output format
11. **Validate**

## Sphere Reference Integration

### Quick Sphere Lookup (Preferred)

Use the JSON lookup for efficient queries without loading full files:

```bash
# Get specific sphere level capabilities
python scripts/lookup.py rules.sphere-details sphere-details "Forces 3"
python scripts/lookup.py rules.sphere-details sphere-details "Life 4"

# Search for effects across all spheres
python scripts/lookup.py rules.sphere-details sphere-details --find "heal"
python scripts/lookup.py rules.sphere-details sphere-details --find "teleport"
python scripts/lookup.py rules.sphere-details sphere-details --find "create"
```

Returns: name, capabilities, conjunctions, weight_limit, combat, vulgarity, notes.

### Finding Required Spheres

Check `references/spheres/conjunctions.md` for comprehensive effect → sphere mappings:

| Effect Category | Section in conjunctions.md |
|-----------------|---------------------------|
| Creating from nothing | Creating Things From Nothing |
| Healing | Healing |
| Combat/Harm | Harm and Combat |
| Teleportation | Teleportation and Travel |
| Shapeshifting | Shapeshifting and Transformation |
| Mental effects | Mind Control and Influence |
| Fortune/Curses | Fate, Fortune, and Oaths |
| Illusions | Illusions |
| Spirits/Undead | Spirits and the Dead |
| Item creation | Wonder Creation |
| Weather | Weather and Environment |
| Perception | Perception and Scrying |

### Verifying Capabilities

After identifying spheres, verify the effect is possible:

**Step 1: Quick JSON lookup (usually sufficient)**
```bash
python scripts/lookup.py rules.sphere-details sphere-details "Forces 3"
```

**Step 2: Deep dive (only if needed for edge cases)**
Load the detailed markdown file only for complex questions:

```
references/spheres/correspondence.md  - Space, distance, gates
references/spheres/entropy.md         - Fate, decay, probability
references/spheres/forces.md          - Energy, elements, weather
references/spheres/life.md            - Healing, shapeshifting, bodies
references/spheres/matter.md          - Objects, transmutation
references/spheres/mind.md            - Thoughts, control, astral
references/spheres/prime.md           - Quintessence, enchantment
references/spheres/spirit.md          - Umbra, spirits, Gauntlet
references/spheres/time.md            - Temporal effects
```

Each sphere file contains:
- Level-by-level capabilities
- Weight limits / scope restrictions
- Key conjunctions at each level
- Combat applications
- Special mechanics

### Determining Mechanics

Use `references/spheres/mechanics.md` for:

**Successes Required:**
| Feat Complexity | Successes |
|-----------------|-----------|
| Simple | 1 |
| Standard | 2 |
| Difficult | 3-4 |
| Impressive | 5-9 |
| Mighty | 10-14 |
| Outlandish | 15-19 |
| Godlike | 20+ |

**Vulgarity Assessment:**
- Usually Coincidental: Rank 1 perception, subtle probability, unwitnessed healing, Mind effects
- Usually Vulgar (no witnesses): Teleportation, creating matter/forces/life, major shapeshifting
- Always Vulgar: Rewinding time, obvious impossibilities, raising the dead

## Practice-Rote Integration

### Practice Rating Requirement
The Practice rating must be **at least equal to the highest Sphere** in the rote:

| Highest Sphere | Minimum Practice |
|----------------|------------------|
| 1 | Practice 1 |
| 2 | Practice 2 |
| 3 | Practice 3 |
| 4 | Practice 4 |
| 5 | Practice 5 |

### Associated Abilities
Each Practice has specific Associated Abilities. The rote's Ability **must be Associated** with its Practice.

```bash
python scripts/lookup.py rules.practices practices "High Ritual Magick"
# Returns associated_abilities: Academics, Awareness, Enigmas, Esoterica, Occult, Research, Science
```

### Practice Benefits
Many Practices provide difficulty bonuses for certain rote types:

| Practice | Benefit Condition |
|----------|-------------------|
| Alchemy | Creating Charms/Gadgets (half Quintessence cost) |
| Craftwork | Creating physical objects (-1 diff) |
| Faith | Acting in accordance with faith (-1 diff) |
| High Ritual Magick | Extended rituals (-1 diff, +1 die/hour) |
| Martial Arts | Body movement effects (-1 diff) |

### Practice Penalties
Some Practices have penalties for certain rote types:

| Practice | Penalty Condition |
|----------|-------------------|
| Alchemy | Fast-casting (+1 diff) |
| High Ritual Magick | Fast-casting without preparation (+2 diff) |
| Craftwork | Purely mental/spiritual effects (+1 diff) |

## Sphere Levels Quick Reference

| Level | Scope |
|-------|-------|
| 1 | Perception, sensing |
| 2 | Minor manipulation, self/willing |
| 3 | Significant effects, affect others |
| 4 | Major transformations, permanent |
| 5 | Create from nothing, large-scale |

### The Prime 2 Rule
To conjure Pattern from nothing:
- Forces 3 + Prime 2 → fire, lightning, energy
- Matter 3 + Prime 2 → solid objects
- Life 3 + Prime 2 → simple organisms
- Mind 3 + Prime 2 → mental constructs
- Spirit 3 + Prime 2 → ephemera

## Rote Costs

| Source | Cost |
|--------|------|
| From scratch | Total Sphere dots |
| From teacher/grimoire | Half total (rounded up) |

**Requirement**: When learning from Mentor/Library/Grimoire, their rating must exceed the rote's highest Sphere.

### Starting Rotes
- Characters begin with **6 rote dots**
- Additional: 4 Freebies = 1 rote dot, or 3 XP = 1 rote dot

## Output Format

```markdown
# [Rote Name]

**Rote Type**: [Category]
**Sphere Requirements**: [Sphere N, Sphere N]
**Total Sphere Dots**: [N]
**Practice**: [Practice Name] (Rating [N] required)
**Dice Pool**: [Attribute] + [Ability]

## Effect
[2-3 sentences describing what the rote does]

## Sphere Justification
[Explain why these sphere levels are required, referencing capabilities from sphere files]

## Execution
[How the rote is performed using the Practice]
- **Instruments Used**: [List relevant instruments]
- **Time Required**: [Instant/Turns/Minutes/Hours]

## Paradigmatic Explanation
[How the mage's paradigm explains why this works]

## Practice Modifiers
- **Benefit**: [Any difficulty reduction from Practice benefit]
- **Tenet Bonus**: [If Practice is Associated with mage's Tenets: -1 diff]
- **Tenet Penalty**: [If Practice is Limited by mage's Tenets: +1 diff]

## Common Uses
- [Use 1]
- [Use 2]

## Paradox Considerations
**Coincidental** when [circumstances].
**Vulgar** when [circumstances].

## Successes
- **Base Successes Needed**: [N] ([Simple/Standard/Difficult/etc.])
- **Additional Successes**: [What they provide]

## Limitations
- [Limit 1]

## System Notes
**Difficulty**: [N] (base 6, +/- modifiers)
**Duration**: [Instant/Concentration/Scene/Story]
```

## Validation

- [ ] Sphere levels match effect scope (verified against sphere reference files)
- [ ] Effect is achievable at stated levels (from conjunctions.md or sphere files)
- [ ] Practice rating ≥ highest Sphere in rote
- [ ] Ability is Associated with Practice
- [ ] Dice pool makes sense narratively
- [ ] Paradox assessment accurate (from mechanics.md)
- [ ] Instruments appropriate to Practice
- [ ] Success requirements appropriate for complexity

**When dependency:**
- [ ] All Spheres within parent constraints
- [ ] Practice within parent constraints (Grimoire, Character)
- [ ] Ability within parent constraints

## Reference Data

```bash
# PRIMARY: Sphere details (capabilities, conjunctions, vulgarity)
python scripts/lookup.py rules.sphere-details sphere-details "Forces 3"
python scripts/lookup.py rules.sphere-details sphere-details --find "healing"

# Quick sphere level lookup (one-line summaries)
python scripts/lookup.py rules.sphere-levels sphere-levels "Forces"

# Practice details (includes associated abilities, benefit, penalty)
python scripts/lookup.py rules.practices practices "High Ritual Magick"

# Common effects quick lookup
python scripts/lookup.py rules.common-effects common-effects --find "fire"

# Tenet-Practice associations
python scripts/lookup.py rules.tenets tenets "A Rational Universe"

# For complex edge cases only, read markdown:
# references/spheres/[sphere].md

# For comprehensive effect → spheres table:
# references/spheres/conjunctions.md

# For mechanics (successes, vulgarity):
# references/spheres/mechanics.md
```

## Example Rotes by Practice

### Alchemy Rote
**Elevate Material** (Matter 2, Prime 2)
- Practice: Alchemy 2+
- Ability: Science (Chemistry) or Crafts
- Benefit: Half Quintessence cost when creating charm
- Instruments: Laboratory, formulas, reagents
- Sphere Reference: Matter 2 allows "Basic transmutation (same state/properties)", Prime 2 provides "Fuel patterns with Quintessence"

### High Ritual Magick Rote
**Summon Guardian Spirit** (Spirit 3)
- Practice: High Ritual Magick 3+
- Ability: Occult or Esoterica
- Benefit: Extended ritual (-1 diff per hour, max -3)
- Penalty: Fast-cast at +2 difficulty
- Instruments: Circle, incense, sacred names, ceremonial robes
- Sphere Reference: Spirit 3 allows "Step sideways, heal/harm spirits, awaken/lull object spirits"

### Martial Arts Rote
**Iron Body Meditation** (Life 2, Prime 2)
- Practice: Martial Arts 2+
- Ability: Do or Meditation
- Benefit: Body movement = no instruments needed
- Penalty: Cannot perform if restrained
- Instruments: Breathing, movement, focus
- Sphere Reference: Life 2 allows "heal self, cosmetic self-changes", Prime 2 adds durability through Quintessence

### Reality Hacking Rote
**Exploit System Weakness** (Correspondence 2, Entropy 2)
- Practice: Reality Hacking 2+
- Ability: Computer or Research
- Benefit: -2 difficulty in digital environments
- Instruments: Code, exploits, mathematical formulas
- Sphere Reference: Correspondence 2 allows "Sense distant locations, touch/affect through space", Entropy 2 allows "Control probability, force specific random outcomes"

### Weather-Witching Rote
**Call the Storm** (Forces 4, Entropy 3)
- Practice: High Ritual Magick 4+
- Ability: Occult or Science
- Sphere Reference: From Forces sphere file - "Forces 4 + Entropy 3: Strong 'suggestions' to existing weather. Takes hours to manifest unless vulgar."
- Vulgarity: Coincidental if existing conditions allow; vulgar if creating impossible weather
- Successes: Per mechanics.md, "Weather follows natural tendencies of existing climate"

### Resurrection Rote
**Return from the Threshold** (Life 4, Spirit 4, Prime 3)
- Practice: High Ritual Magick 4+
- Ability: Occult, Esoterica, or Medicine
- Sphere Reference: From conjunctions.md - "Revive recently dead (~5 min): Life 4 + Spirit 4 + Prime 3"
- Vulgarity: Always vulgar ("Raising the dead" per mechanics.md)
- Successes: Impressive (5-9) minimum

## Return Format (for parent modules)

```
Created: ./rotes/silver_conduit.md
Name: Silver Conduit
Spheres: Prime 2, Correspondence 1
Practice: High Ritual Magick (2+)
Effect: Channel Quintessence across distances
Sphere Verification: Correspondence 1 (sense spatial relationships), Prime 2 (fuel patterns with Quintessence)
```
