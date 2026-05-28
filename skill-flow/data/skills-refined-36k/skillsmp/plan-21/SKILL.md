---
name: plan
description: 'Epic decomposition into trackable issues. Triggers: "create a plan", "plan implementation", "break down into tasks", "decompose into features", "create beads issues from research", "what issues should we create", "plan out the work".'
---

# Plan Skill

Create reusable formula templates (.formula.toml) that define structured implementation
patterns. Formulas produce beads issues with proper dependencies and wave computation
for parallel execution.

## Role in the Brownian Ratchet

Formulas are **captured ratchet patterns** - proven solutions that can be reused:

| Component | Formula's Role |
|-----------|----------------|
| **Chaos** | Formula development: multiple attempts to find right structure |
| **Filter** | Successful patterns captured, failed patterns discarded |
| **Ratchet** | `.formula.toml` locks the pattern for reuse |

> **A formula is a ratcheted solution that prevents re-solving the same problem.**

Once a formula works (validated by /crank execution), it becomes a reusable
template. Future work with similar structure instantiates the formula instead
of planning from scratch.

**Formula Hierarchy:**
```
Research → Plan → Implement → Validate → FORMULA (captured pattern)
                                              ↓
                              Future work: cook → pour → execute
```

## Overview

**Core Purpose**: Transform a goal into a reusable formula template (.formula.toml) that
captures the pattern for creating beads issues with dependency ordering and wave-based
parallelization for `/crank` (autonomous) or `/implement-wave` (supervised).

**Key Capabilities**:
- 6-tier context discovery hierarchy
- Prior formula discovery to prevent duplicates
- Feature decomposition with dependency modeling
- Formula template creation with proper TOML structure
- Auto-instantiation via `bd cook`
- Beads issue creation with epic-child relationships
- Wave computation for parallel execution

**Formulas vs Plans**:
- **Formula**: Reusable template (.formula.toml) - can be instantiated multiple times
- **Plan**: One-time execution plan - specific to a single goal

**When to Use**: Work needs 2+ discrete issues with dependencies, or a reusable pattern is desired.
**When NOT to Use**: Single task (use `/implement`), exploratory (use `/research`).

### Flags

| Flag | Description |
|------|-------------|
| `--immediate` | Skip formula creation, directly create beads issues |
| `--cook` | Auto-run `bd cook` after formula creation |
| `--dry-run` | Preview formula output without writing files |
