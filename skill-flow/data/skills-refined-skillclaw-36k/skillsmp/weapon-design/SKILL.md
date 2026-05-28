---
name: weapon-design
description: Weapon and item design documentation
category: gamedesign
depends-on: [thermite-integration]
---

# Weapon Design

## Overview

This skill provides guidance for designing weapons, items, and equipment that feel good to use and are balanced.

## When to Use This Skill

Use when:
- Designing weapons
- Creating item systems
- Balancing equipment
- Designing consumables

## Weapon Template

```markdown
## [Weapon Name]

### Type
[Category: melee, ranged, magic, etc.]

### Role
[Combat role: close-range, area denial, sniping, etc.]

### Stats
| Stat | Value | Description |
|------|-------|-------------|
| Damage | [X] | Per hit |
| Fire Rate | [Y] | Attacks per second |
| Accuracy | [Z] | Spread/recoil |
| Range | [R] | Effective distance |
| Magazine | [M] | Ammo capacity |
| Reload | [S] | Reload time |
| [Etc] | [...] | [...] |

### Handling
- **ADS speed:** [Zoom time]
- **Movement speed:** [While aiming]
- **Swap time:** [Equip speed]
- **Recoil pattern:** [Visual feedback]

### Damage Model
| Distance | Head | Body | Legs |
|----------|-----|------|------|
| [Close] | [X] | [Y] | [Z] |
| [Medium] | [X] | [Y] | [Z] |
| [Far] | [X] | [Y] | [Z] |

### Features
- **Feature 1:** [Description]
- **Feature 2:** [Description]

### Counterplay
**Countered by:**
- [Weapon/Strategy] - [Why it works]
- [Weapon/Strategy] - [Why it works]

### Skill Expression
**Floor:** [Minimum effectiveness]
**Ceiling:** [Maximum effectiveness with skill]

### Visual Design
- **Shape:** [Silhouette recognition]
- **Color:** [Team/affiliation indicators]
- **Animation:** [Attack animations]
- **Audio:** [Fire sounds, reload, etc.]

### Acquisition
- **Unlock:** [How to get it]
- **Cost:** [Price/crafting]
- **Rarity:** [Spawn rate]
```

## Weapon Categories

### Melee

Close-quarters combat:
- Swords, axes, maces
- Fist weapons
- Spears and polearms
- Daggers and knives

### Ranged

Distance combat:
- Pistols, rifles, shotguns
- Bows, crossbows
- Thrown weapons
- Magic staves

### Area of Effect

Multiple targets:
- Explosives
- Sprays and cones
- DoTs (Damage over Time)
- Summons

### Utility

Support items:
- Shields
- Grenades
- Traps
- Boosts

## Balance Framework

### Rock-Paper-Scissors

Every weapon category has counters:

```
Melee beats Shotgun
Shotgun beats Sniper
Sniper beats Rifle
Rifle beats LMG
etc.
```

### Niche Protection

Each weapon needs a role:
- **CQC** - Shotguns, SMGs
- **Mid-range** - Rifles
- **Long-range** - Snipers
- **Area denial** - LMGs, explosives

### Skill Indexing

Reward player skill:
- **Headshots** - Precision rewarded
- **Tracking** - Leading targets
- **Timing** - Window-based abilities
- **Positioning** - Map knowledge

## Item Design

### Consumables

Single-use items:
```
Effect → Duration → Cooldown
```

### Equipment

Persistent items:
```
Slot → Effect → Drawback
```

## Balance Levers

Tunable values for balance:

| Lever | Effect |
|-------|--------|
| Damage | Time to kill |
| Fire rate | DPS, ammo consumption |
| Accuracy | Effective range |
| Magazine | Sustained fire duration |
| Reload | Vulnerability window |
| Mobility | Positioning advantage |

## Weapon Review Checklist

Before finalizing a weapon:

- [ ] Clear role and use case
- [ ] Balanced stats for its role
- [ ] Has meaningful counterplay
- [ ] Skill ceiling exists
- [ ] Satisfying to use
- [ ] Distinct from other weapons
- [ ] Visual clarity
- [ ] Audio feedback
- [ ] Technical feasibility confirmed
