---
title: DEEP Estimation Guide
description: DEEP estimation methodology for epics and stories
keywords: estimation, deep, planning, sizing
skill: epic-story-planning
---

# DEEP Estimation

## What is DEEP?

**D**etailed appropriately - More detail for near-term work
**E**stimated - Relative sizing, not precise time
**E**mergent - Evolves as understanding grows
**P**rioritized - Most important first

## Epic Estimation

| Size | Duration | Complexity |
|------|----------|------------|
| XS | 1-2 days | Single feature, minimal changes |
| S | 3-5 days | Few related features |
| M | 1-2 weeks | Multiple features, some integration |
| L | 2-4 weeks | Significant scope, cross-cutting |
| XL | 4+ weeks | Consider breaking down further |

## Story Points

Relative complexity, not time:

| Points | Meaning |
|--------|---------|
| 1 | Trivial, well-understood |
| 2 | Small, straightforward |
| 3 | Medium, some complexity |
| 5 | Large, complex |
| 8 | Very large, uncertain |
| 13+ | Too big, needs breakdown |

## Task Estimation

For implementation tasks:
- Target: 15-30 minutes each
- Maximum: 2 hours
- If longer: Break down further

## Estimation Process

1. **Relative comparison** - Compare to known reference stories
2. **Planning poker** - Team consensus on complexity
3. **T-shirt sizing** - Quick categorization (S, M, L, XL)
4. **Refinement** - Increase detail as work approaches

## Red Flags

| Indicator | Action |
|-----------|--------|
| Story > 8 points | Break into smaller stories |
| Task > 2 hours | Decompose further |
| Uncertain estimate | Spike/research first |
| Dependencies unclear | Map dependencies explicitly |
