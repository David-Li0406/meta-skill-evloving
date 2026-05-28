# Apocalyptic Form Module

The demon's true celestial appearance, revealed when spending Faith.

## Overview

Every demon has exactly **one Visage**—their apocalyptic form—determined by their **primary Lore** at character creation. When revealed, this form grants 4 low-torment abilities or 4 high-torment abilities, depending on the demon's current state.

---

## Core Rules

### One Visage Per Character

A demon's Visage is permanently set by their **primary Lore** (the Lore with the most dots at creation). This cannot be changed.

| Primary Lore | Visage Name | House Association |
|--------------|-------------|-------------------|
| Celestials | Bel | Common (all) |
| Fundament | — | Common (all) |
| Humanity | — | Common (all) |
| Flame | Nusku | Devils |
| Radiance | Qingu | Devils |
| Awakening | Dagan | Scourges |
| Firmament | Anshar | Scourges |
| Winds | Ellil | Scourges |
| Earth | Kishar | Malefactors |
| Paths | Antu | Malefactors |
| Forge | Mummu | Malefactors |
| Light | Shamash | Fiends |
| Patterns | Ninsun | Fiends |
| Portals | Nedu | Fiends |
| Longing | Ishhara | Defilers |
| Storms | Adad | Defilers |
| Transfiguration | Mammetum | Defilers |
| Beast | Zaltu | Devourers |
| Flesh | Aruru | Devourers |
| Wild | Ninurtu | Devourers |
| Death | Namtar | Slayers |
| Spirit | Nergal | Slayers |
| Realms | Ereshkigal | Slayers |

### Activation

- **Cost**: 1 Faith point
- **Duration**: One scene
- **Action**: Reflexive (can be done at any time)
- **Dismissal**: Free action, no cost

### Low-Torment vs High-Torment Form

Which abilities manifest depends on the demon's **current Torment**:

| Condition | Form Manifested |
|-----------|-----------------|
| Torment < 7 | Low-Torment (angelic) abilities |
| Torment ≥ 7 | High-Torment (monstrous) abilities |

**Critical**: A demon with Torment 7+ **cannot** manifest their low-torment form. They are locked into the monstrous version.

### Trait Count

Every Visage grants exactly:
- **4 Low-Torment Abilities** (angelic form)
- **4 High-Torment Abilities** (monstrous form)

A character in apocalyptic form has access to only ONE set of 4 abilities at a time, never both.

---

## Benefits of Apocalyptic Form

When in apocalyptic form, demons gain:

1. **Lethal Soak**: Can use Stamina to soak lethal damage
2. **Visage Abilities**: The 4 abilities from their current form
3. **Intimidation**: Mortals who witness the form may flee or freeze

---

## Revealing the Form

### Voluntary Revelation

Spend 1 Faith. Form manifests instantly.

### Involuntary Revelation

Certain circumstances may force revelation:
- Frenzy or extreme emotional state
- Taking aggravated damage
- Storyteller discretion for dramatic moments

### Witnesses

Mortals who see an apocalyptic form:
- May require Willpower roll to act normally
- May flee in terror
- May rationalize what they saw afterward

---

## Common Ability Types

Visage abilities fall into categories:

### Physical Enhancements
- Attribute bonuses (+Str, +Dex, +Sta)
- Increased Size (typically +1/3 height)
- Extra Health Levels
- Extra Limbs

### Combat Abilities
- Claws/Teeth (typically Str+2 aggravated)
- Wings (glide at 3x running speed)
- Armor/Scales (soak dice)
- Natural weapons (horns, tail, quills)

### Sensory Abilities
- Enhanced Senses (-2 difficulty Perception)
- Night Vision
- Supernatural Vision
- 360-degree vision

### Special Powers
- Immunity (fire, bashing, falling)
- Aura effects (healing, fear, distraction)
- Extra Actions (spend Faith)
- Improved Initiative (+2)

---

## Creating a Character's Visage

### Step 1: Identify Primary Lore

Look at the character's Lore dots. The Lore with the most dots is the primary Lore.

**Tie-breaker**: If two Lores are tied, the player chooses which is primary.

### Step 2: Record Visage Name

Note the Visage name from the table above.

### Step 3: Record Abilities

Look up the Visage in `modules/d20/apocalyptic-traits.md` and record:
- 4 Low-Torment abilities
- 4 High-Torment abilities

### Step 4: Describe Appearance

Write a brief description of both angelic and monstrous appearances.

---

## Data Lookup

```bash
# Get Visage by Lore
python scripts/lookup.py d20.apocalyptic visages "Forge"

# List all Visages
python scripts/lookup.py d20.apocalyptic visages
```

---

## Validation Checklist

- [ ] Primary Lore identified
- [ ] Visage name recorded
- [ ] 4 low-torment abilities listed
- [ ] 4 high-torment abilities listed
- [ ] Appearance described (both forms)
- [ ] Current Torment noted (determines active form)

---

## Output Template

```markdown
## Apocalyptic Form

**Visage**: [Name]
**Primary Lore**: [Lore name]
**Current Form**: [Low-Torment/High-Torment]

### Appearance

**Low-Torment (Angelic)**:
[Description]

**High-Torment (Monstrous)**:
[Description]

### Low-Torment Abilities (Torment < 7)

1. **[Ability Name]**: [Effect]
2. **[Ability Name]**: [Effect]
3. **[Ability Name]**: [Effect]
4. **[Ability Name]**: [Effect]

### High-Torment Abilities (Torment ≥ 7)

1. **[Ability Name]**: [Effect]
2. **[Ability Name]**: [Effect]
3. **[Ability Name]**: [Effect]
4. **[Ability Name]**: [Effect]
```
