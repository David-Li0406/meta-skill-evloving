# Gift Module

Create and document Gifts for W20.

## What is a Gift?

Gifts are supernatural abilities taught by spirits. They are:
- Learned from spirits (or rarely, other Garou)
- Organized by level (1-5)
- Categorized by source: Breed, Auspice, or Tribe

## Level Guidelines

| Level | Availability | Power Scope |
|-------|--------------|-------------|
| 1 | Cliath | Perception, minor effects |
| 2 | Fostern | Moderate manipulation |
| 3 | Adren | Significant effects |
| 4 | Athro | Major transformations |
| 5 | Elder | Legendary, devastating |

## Gift Components

1. **Name** — Distinctive title
2. **Level** — 1-5
3. **Source** — Breed/Auspice/Tribe
4. **Description** — Narrative effect
5. **System** — Roll, cost, duration, effect
6. **Teaching Spirit** — What spirit teaches it

## Output Format

```markdown
# [Gift Name]

**Level**: [1-5]
**Source**: [Breed/Auspice/Tribe]
**Teaching Spirit**: [Spirit type]

## Description
[What the Gift does narratively]

## System
**Roll**: [Attribute] + [Ability] (difficulty [X])
**Cost**: [Gnosis/Rage/Willpower or None]
**Duration**: [Instant/Scene/Permanent]
[Mechanical details]
```

## Reference
- `lookup.py gift.gifts-by-source gifts-by-source` — All Gifts by breed/auspice/tribe
