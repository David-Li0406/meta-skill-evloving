---
name: veilbreakers-balance-check
description: Use when modifying game balance numbers (damage, capture rates, synergy values). Validates changes won't break the game.
---

# VeilBreakers Balance Check

## Overview

Validate balance changes BEFORE they break the game. One wrong number can ruin months of work.

## When to Use

- Modifying damage formulas
- Changing capture rates
- Adjusting synergy bonuses
- Tweaking corruption effects
- Adding new abilities/skills
- Changing cooldowns

## The Balance Systems

### Brand Effectiveness (10 Brands)
- 2x damage to 2 brands (strong against)
- 0.5x damage to 2 brands (weak against)
- 1x damage to 6 brands (neutral)

**Verify:** Every brand has exactly 2 strong, 2 weak, 6 neutral.

### Synergy Tiers
| Tier | Match | Damage | Defense | Corruption |
|------|-------|--------|---------|------------|
| FULL | 3/3 | +8% | +8% | 0.5x |
| PARTIAL | 2/3 | +5% | +5% | 0.75x |
| NEUTRAL | 0-1/3 | +0% | +0% | 1.0x |
| ANTI | Weak brand | +0% | +0% | 1.5x |

**Verify:** Bonuses stack additively, not multiplicatively.

### Corruption States
| Range | State | Modifier |
|-------|-------|----------|
| 0-10% | ASCENDED | +25% |
| 11-25% | Purified | +10% |
| 26-50% | Unstable | +0% |
| 51-75% | Corrupted | -10% |
| 76-100% | Abyssal | -20% |

**Verify:** Bounds are inclusive/exclusive as intended.

### Ability Cooldowns
| Slot | Cooldown Range |
|------|----------------|
| Basic | None |
| Defend | None |
| Skill 1 | 4-6 seconds |
| Skill 2 | 10-15 seconds |
| Skill 3 | 18-25 seconds |
| Ultimate | 45-90 seconds |

**Verify:** New abilities fall within range for their slot.

## The Check Process

### Step 1: Document the Change
```
What: [Exact number change]
From: [Old value]
To: [New value]
Why: [Reasoning]
```

### Step 2: Launch Balance Analyzer
```
Task: Launch balance-analyzer agent with:
"Analyze balance impact of changing [X] from [old] to [new]"
```

### Step 3: Edge Case Analysis
Calculate these scenarios:
1. **Best case**: Max synergy + ASCENDED + type advantage
2. **Worst case**: ANTI synergy + Abyssal + type disadvantage
3. **Average case**: NEUTRAL + Unstable + neutral type

### Step 4: Check for Breaks
| Problem | Indicator |
|---------|-----------|
| One-shot | Best case kills in 1 hit |
| Unkillable | Worst case can't die |
| Dead option | Never optimal to use |
| Power creep | Strictly better than existing |

### Step 5: Document Decision
```
Change: [Approved / Modified / Rejected]
Final value: [number]
Reasoning: [explanation]
```

## Quick Formulas

**Damage dealt:**
```
base_damage * brand_multiplier * synergy_bonus * corruption_modifier
```

**Capture chance:**
```
base_rate + health_modifier + corruption_modifier + method_bonus + item_bonus
```

**Effective stats:**
```
base_stat * (1 + synergy_bonus) * corruption_modifier
```

## Red Flags

Stop and reconsider if:
- Change is more than ±20% from current
- Multiple systems affected simultaneously
- Edge case goes beyond intended range
- You're "fixing" a perceived issue without data
