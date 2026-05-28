# Sorcerer Path Module

Create custom Paths for M20 Sorcerer hedge wizards.

## Path Design Philosophy

Paths represent **linear, focused magical abilities** that work within reality's rules. Unlike Sphere magic, Paths:

- Follow **predictable, calculable principles**
- Are **capped by mundane Ability ratings**
- Require **time** to cast (1 turn/level for spells, 10 min/level for rituals)
- Have **specific failure consequences** instead of Paradox

## Path Structure Types

### Type A: Aspect-Based
Path grants control over Aspects (Duration, Targets, Range, etc.). Each level allows higher Aspect ratings.

**Examples**: Conjuration, Fascination, Healing, Hellfire

### Type B: Level-Based Effects
Each level unlocks specific capabilities. Less flexible but often more powerful.

**Examples**: Divination, Ephemera, Shapeshifting

### Type C: Ritual-Only
No spells — everything is rituals. Usually creation-focused.

**Examples**: Alchemy, Enchantment, Summoning/Binding/Warding

---

## Creating a New Path

### Step 1: Conceptualization

Define:
1. **Core Theme**: What aspect of reality does it manipulate?
2. **Scope**: What can it do? What can it NOT do?
3. **Flavor**: How is it different from existing Paths?
4. **Limitations**: How does it stay within "linear magic" bounds?

**Test**: Could an Awakened mage do this with a single Sphere? If yes, reconsider.

### Step 2: Structure Selection

| If the Path... | Use Type |
|----------------|----------|
| Primarily scales existing effects | A (Aspect-Based) |
| Unlocks new capabilities at each level | B (Level-Based) |
| Only creates lasting items/effects | C (Ritual-Only) |

### Step 3: Define Levels

#### Type A (Aspect-Based)
Define which Aspects apply:

```bash
python scripts/lookup.py sorcerer.aspects aspects --keys
```

| Level | Core Capability |
|-------|-----------------|
| • | Minor sensing/perception, minimal effect |
| •• | Basic manipulation, self-affecting |
| ••• | Significant effects, affect others |
| •••• | Major transformations |
| ••••• | Mastery, legendary capabilities |

#### Type B (Level-Based)
Define specific effects at each level.

#### Type C (Ritual-Only)
Define what can be created/accomplished at each level.

### Step 4: Define System Elements

**Modifiers**: What makes the Path easier/harder?
- Familiar targets? (-1 difficulty)
- Resisting targets? (+1-2 difficulty)
- Sleeper witnesses? (successes removed)

**Time**:
- Spells: 1 turn per level (standard)
- Rituals: 10 minutes per level (standard)

**Aspects** (Type A): Which Aspects apply?

### Step 5: Price of Failure

Every Path needs **botch consequences**. Common types:

| Type | Description |
|------|-------------|
| Backfire | Effect targets caster |
| Misfire | Hits wrong target |
| Corruption | Works but twisted |
| Exhaustion | Caster suffers damage/fatigue |
| Attraction | Unwanted attention (spirits, etc.) |
| False Success | Appears to work, actually failed |

### Step 6: Sample Rituals

Include 2-4 rituals at various levels. See `modules/sorcerer-ritual.md` for template.

---

## Path Template

```markdown
# [Path Name]

## Overview
[2-3 sentences describing theme and capabilities]

## In Practice
[How different Practices might use this Path]

## System

**Type**: [Spell / Ritual / Both]
**Common Abilities**: [List]
**Modifiers**: [List any difficulty modifiers]
**Time**: [Casting time]
**Aspects**: [List or "Level-based effects"]

**Effects**:
| Level | Effect |
|-------|--------|
| • | [First level] |
| •• | [Second level] |
| ••• | [Third level] |
| •••• | [Fourth level] |
| ••••• | [Fifth level] |

**Price of Failure**: [Describe botch consequences]

## Sample Rituals

### [Ritual Name] (•)
[Description and mechanics]

### [Ritual Name] (•••)
[Description and mechanics]
```

---

## Example Custom Paths

### Path of Echoes (Level-Based)

**Overview**: Manipulation of sound and vibration.

**Modifiers**: -1 diff in quiet, +1 in noisy

**Effects**:
| Level | Effect |
|-------|--------|
| • | Enhance/suppress sounds, detect vibrations |
| •• | Project voice, create phantom sounds |
| ••• | Sonic assault (2L/success), echolocation |
| •••• | Shatter objects, temporary deafness |
| ••••• | Sonic invisibility, lethal scream attacks |

**Aspects**: Duration, Range, Number of Targets, Damage

**Price of Failure**: Temporary deafness, embarrassing sounds

### Path of Veils (Level-Based)

**Overview**: Manipulation of boundaries and thresholds.

**Modifiers**: +1 diff on magically warded thresholds

**Effects**:
| Level | Effect |
|-------|--------|
| • | Sense threshold strength, detect hidden doors |
| •• | Lock/unlock mundane doors, modify thresholds |
| ••• | Create minor thresholds, pass through thin walls |
| •••• | Seal areas completely, one-way passages |
| ••••• | Merge distant thresholds (door-to-door travel) |

**Aspects**: Duration, Range, Area

**Price of Failure**: Trapped on wrong side, threshold inverts

### Path of Threads (Ritual-Only)

**Overview**: Magical crafting focused on textiles.

**Effects**:
| Level | Creation |
|-------|----------|
| • | Clothing that never stains/tears, perfect knots |
| •• | Cloaks (+2 Stealth), thread that reveals lies |
| ••• | Garments providing soak dice, veils of disguise |
| •••• | Bonds that restrain supernaturals, damage conversion |
| ••••• | Flying carpets, cloaks of invisibility |

**Price of Failure**: Thread tangles, item cursed

---

## In-Game Path Creation

Characters can create new Paths through extended effort:

### Requirements
- **Mastered** (level 5) at least one Path first
- Clear conceptualization
- Assign Path Ability

### Process
1. Roll Path Ability dice pool at difficulty 8 once per month
2. Accumulate 25 successes to unlock first dot
3. Repeat for each additional dot
4. Botch = start over from scratch
5. At completion, spend 1 permanent Willpower to cement

---

## Validation Checklist

- [ ] Theme is distinct from existing Paths
- [ ] Works within reality (not bending it like Spheres)
- [ ] Clear scope and limitations
- [ ] Reasonable power progression
- [ ] Defined system elements (modifiers, aspects, time)
- [ ] Meaningful failure consequences
- [ ] Sample rituals demonstrate range
- [ ] Could reasonably be learned by a mortal
- [ ] Doesn't obsolete existing Paths
