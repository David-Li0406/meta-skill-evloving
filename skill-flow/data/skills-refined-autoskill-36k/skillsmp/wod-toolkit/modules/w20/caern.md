# Caern Module

Create caerns (sacred sites) for W20.

## Caern Statistics

### Level (1-5)
| Level | Gnosis/Month | Gauntlet Mod |
|-------|--------------|--------------|
| 1 | 3 | -1 |
| 2 | 5 | -2 |
| 3 | 7 | -3 |
| 4 | 9 | -4 |
| 5 | 10+ | -5 |

### Types
Gnosis, Rage, Willpower, Strength, Stamina, Enigmas, Healing, Leadership, Visions, Wyld

Each type grants +2 to related rolls (or +1 to Attribute).

### Base Gauntlet
| Location | Gauntlet |
|----------|----------|
| Deep wilderness | 4 |
| Rural | 5 |
| Most places | 6 |
| Small city | 7 |
| Downtown | 8 |
| Inner city | 9 |

**At Caern**: Gauntlet = Base - Level

## Output Format

```markdown
# [Caern Name]

**Level**: [1-5]
**Type**: [Type] (+[bonus])
**Location**: [Geographic]

## Statistics
| Stat | Value |
|------|-------|
| Gnosis/Month | [X] |
| Gauntlet (Heart) | [X] |
| Type Bonus | [+X] |

## The Bawn
[Protected territory, ~1 mile per level]

## Caern Spirit
[Name and nature of the Incarna]

## History
[Founding, events]
```

## Reference
- `lookup.py caern.caern-types caern-types`
