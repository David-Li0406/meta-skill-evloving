---
name: implement
description: 'Execute a single beads issue with full lifecycle. Triggers: "implement", "work on task", "fix bug", "start feature", "pick up next issue".'
---

# Implement Skill

Execute a SINGLE beads issue from `open` to `closed`.

## Role in the Brownian Ratchet

Implement is the **micro-ratchet** - the atomic unit of progress:

| Component | Implement's Role |
|-----------|------------------|
| **Chaos** | Coding attempts, debugging, iteration |
| **Filter** | Tests must pass, lint must pass |
| **Ratchet** | Issue status: `open` → `in_progress` → `closed` |

> **The issue lifecycle IS the ratchet. Once closed, work is permanent.**

Each `/implement` cycle is a complete micro-ratchet:
```
open → in_progress (chaos) → tests pass (filter) → closed (ratchet)
```

**Key property:** Issues don't go backward. `closed` is permanent.
Failed attempts stay `in_progress` until fixed or marked blocked.

## Overview

Take a beads issue through: context → implement → test → close → commit.

**When to Use**: Any beads issue needs execution.

**When NOT to Use**: Creating issues (`/plan`), research (`/research`), bulk (`/implement-wave`).
