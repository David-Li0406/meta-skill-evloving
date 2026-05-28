# Node Module

Create Nodes (places of power) for M20.

## What is a Node?

A location where Quintessence gathers, providing:
- **Quintessence**: Free-flowing energy
- **Tass**: Solidified Quintessence
- **Reality Zone**: Practice difficulty modifiers

## Core Statistics

### Rank (0-10)

| Rank | Description | Base Points |
|------|-------------|-------------|
| 1 | Minor trickle | 3 |
| 2 | Small wellspring | 6 |
| 3 | Moderate | 9 |
| 4 | Significant | 12 |
| 5 | Major | 15 |
| 6+ | Legendary | 18+ |

**Base Points = 3 × Rank**

### Size

| Rating | Size | Modifier |
|--------|------|----------|
| -2 | Household Object | +2 pts |
| -1 | Small Room | +1 pts |
| 0 | Average Room | 0 |
| +1 | Small Building | -1 pts |
| +2 | Large Building | -2 pts |

### Ratio (Quint : Tass)

| Rating | Ratio | Modifier |
|--------|-------|----------|
| -2 | 0.0 (All Tass) | +2 pts |
| -1 | 0.25 | +1 pts |
| 0 | 0.5 | 0 |
| +1 | 0.75 | -1 pts |
| +2 | 1.0 (All Quint) | -2 pts |

## Point Calculation

```
Points Remaining = Base - Resonance Cost - Merit/Flaw - Size - Ratio
Quint/Week = floor(Points Remaining × Ratio)
Tass/Week = Points Remaining - Quint/Week
```

**Validation**: Points Remaining > 0

## Resonance

Minimum Required = Rank + Resonance from Merits/Flaws

Only Resonance beyond minimum costs points (1/dot).

```bash
python scripts/lookup.py rules.resonance-traits resonance-traits "Forces"
```

## Reality Zone (Prism of Focus)

Every Node has a Reality Zone = Rank.

Under Prism of Focus, Reality Zones affect **Practice difficulty**:
- **Positive ratings (+1 to +5)**: Low-level effects (≤ rating) using that Practice are always **Coincidental**
- **Negative ratings (-1 to -5)**: High-level effects (≥ 6-|rating|) using that Practice are always **Vulgar**

**Zone Design Rules:**
1. Total of all Practice ratings must = 0 (positive cancels negative)
2. Sum of positive ratings = Rank
3. Use only base Practices (not Specialized/Corrupted)

**Example (Rank 3 Node):**
```
Witchcraft +3 (Sphere 1-3 effects always Coincidental)
Hypertech -2 (Sphere 4+ effects always Vulgar)
Cybernetics -1 (Sphere 5+ effects always Vulgar)
Total: +3 + (-2) + (-1) = 0 ✓
```

```bash
python scripts/lookup.py rules.practices practices --keys
python scripts/lookup.py rules.reality-zones reality-zones "excluded_practices"
```

## Merits & Flaws

Max 7 points each. See `references/node/node-merits-flaws.md`.

## Creation Workflow

1. **Concept** — Location, why Quintessence gathers
2. **Rank** — 1-3 starting, 4-5 major, 6+ legendary
3. **Size/Ratio** — Extent and manifestation
4. **Resonance** — Traits ≥ Minimum
5. **Merits/Flaws** — Story elements
6. **Reality Zone** — Practices summing to 0
7. **Output Description** — Quint feel, Tass form
8. **Validate**

## Point Validation Block

```
Base Points:           [3 × Rank] = X
- Resonance beyond min:         - X
- Net Merit/Flaw:               - X
- Size:                         - X
- Ratio:                        - X
= Points Remaining:             = X

Output: X Quint/week + X Tass/week = X ✓
Resonance: X total (min: X) ✓
Reality Zone: +X positive, sum = 0 ✓
```

## Validation

- [ ] Rank 0-10
- [ ] Points Remaining > 0
- [ ] Resonance ≥ Minimum
- [ ] Reality Zone sums to 0
- [ ] Reality Zone positives = Rank
- [ ] Merit/Flaw ≤ 7 each
- [ ] Quint + Tass = Points Remaining

## Output Format

See `references/node/output-template.md`.

## Return Format

```
Created: ./nodes/wellspring.md
Name: The Wellspring
Rank: 3
Output: 6 Quint/week
```
