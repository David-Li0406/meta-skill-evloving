# Spirit Module

Create spirits for W20.

## Spirit Hierarchy

| Rank | Name | Trait Total | Essence |
|------|------|-------------|---------|
| 1 | Gaffling | 9-18 | 9-20 |
| 2 | Jaggling | 19-30 | 20-35 |
| 3 | Incarna | 31-50 | 35-60+ |
| 4+ | Celestine | 51+ | 100+ |

## Traits
- **Rage** — Combat, aggression
- **Gnosis** — Spiritual power
- **Willpower** — Mental resistance
- **Essence** = Rage + Gnosis + Willpower (minimum)

## Universal Charms
- **Airt Sense** — Detect spirit trails
- **Reform** — Reconstitute after "death"

## Common Charms
Armor, Blast, Cleanse, Corruption, Healing, Materialize, Peek, Possession, Shapeshift, Swift Flight, Tracking

## Output Format

```markdown
# [Spirit Name]

**Rank**: [Gaffling/Jaggling/Incarna]
**Type**: [Nature/Elemental/Conceptual/Triat]

## Statistics
| Trait | Rating |
|-------|--------|
| Rage | [X] |
| Gnosis | [X] |
| Willpower | [X] |
| Essence | [X] |

## Charms
- [Charm]: [Effect]

## Appearance
[How it manifests]

## Chiminage
[What it wants for aid]
```

## Reference
- `lookup.py spirit.spirit-types spirit-types`
- `lookup.py spirit.spirit-charms spirit-charms`
