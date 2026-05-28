# Rite Module

Create and document rites for W20.

## Rite Categories

| Category | Purpose | Base Roll |
|----------|---------|-----------|
| Accord | Restore harmony | Charisma + Rituals |
| Caern | Manage caerns | Variable |
| Death | Honor the dead | Charisma + Rituals |
| Mystic | Spirit interaction | Wits + Rituals |
| Punishment | Enforce law | Variable |
| Renown | Recognize achievements | Charisma + Rituals |
| Seasonal | Celebrate cycles | Stamina + Rituals |
| Minor | Daily observances | No roll |

## Level Guidelines

| Level | Rituals Required | Examples |
|-------|-----------------|----------|
| Minor | 1 | Bone Rhythms, Greet Moon |
| 1 | 1 | Cleansing, Binding |
| 2 | 2 | Summoning, Accomplishment |
| 3 | 3 | Fetish, Totem |
| 4 | 4 | Rending the Veil |
| 5 | 5 | Caern Building |

## Output Format

```markdown
# [Rite Name]

**Level**: [Minor/1-5]
**Category**: [Type]

## Description
[What the rite accomplishes]

## System
**Roll**: [Attribute] + Rituals (difficulty [X])
**Participants**: [Minimum required]
**Time**: [Duration to perform]

### Success/Failure
[Outcomes]
```

## Reference
- `lookup.py rite.rites-by-type rites-by-type` — All rites by category
