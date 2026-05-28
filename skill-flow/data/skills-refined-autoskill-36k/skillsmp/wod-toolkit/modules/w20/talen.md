# Talen Module

Create talens (single-use spiritual items) for W20.

## Talen Basics

- Created via **Rite of Binding** (not Rite of the Fetish)
- Single use—spirit departs after activation
- No attunement required
- Multiple created per ritual (1 per success)
- Gnosis roll to activate (difficulty = talen's Gnosis)

## Sample Talens

| Talen | Gnosis | Effect |
|-------|--------|--------|
| Bane Arrows | 4 | Auto-hit Banes, 3 agg |
| Death Dust | 6 | Speak with dead |
| Gaia's Breath | 5 | Heal 4 levels |
| Moon Glow | 8 | Safe Umbral journey |
| Nightshade | 5 | Shadow form 1 hour |
| Wind Snorkel | 3 | Breathe anywhere |
| Wyrm Scale | 8 | Reveal Wyrm servants |

## Output Format

```markdown
# [Talen Name]

**Gnosis**: [Rating]
**Object**: [Physical form]
**Spirit**: [Type bound]

## Effect
[What happens when activated]

## Creation
[What spirit to bind, what object]
```

## Reference
- `lookup.py fetish.talen-examples talen-examples`
