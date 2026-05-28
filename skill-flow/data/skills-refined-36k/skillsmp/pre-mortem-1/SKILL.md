---
name: pre-mortem
description: 'Pre-mortem simulation for specs and designs. Simulates N iterations of implementation to identify failure modes before they happen. Triggers: "pre-mortem", "simulate spec", "stress test spec", "find spec gaps", "simulate implementation", "what could go wrong", "anticipate failures".'
---

# Pre-Mortem Skill

Pre-mortem simulation: find what will go wrong BEFORE implementation.

## Role in the Brownian Ratchet

Pre-mortem is the **pre-implementation filter** - it catches failures before they happen:

| Component | Pre-Mortem's Role |
|-----------|-------------------|
| **Chaos** | Simulate N iterations with different failure modes |
| **Filter** | Each iteration identifies problems before implementation |
| **Ratchet** | Enhanced spec locks lessons learned |

> **Pre-mortem filters BEFORE the chaos of implementation starts.**

Unlike /vibe which filters code after writing, pre-mortem filters specs
before implementation begins. This prevents entire classes of failures
from ever being attempted.

**The Economics:**
- Without pre-mortem: 10 implementation attempts × fix time = expensive
- With pre-mortem: 10 mental simulations + 1 correct implementation = cheap

## Quick Start

```bash
/pre-mortem .agents/specs/2026-01-22-feature-spec.md
```

## Philosophy

> "Simulate doing it 10 times and learn all the lessons so we don't have to."

Instead of:
1. Write spec
2. Implement
3. Hit problems
4. Fix spec
5. Repeat 10 times

Do:
1. Write spec v1
2. **Simulate 10 iterations mentally**
3. Extract ALL lessons upfront
4. Write spec v2 (battle-hardened)
5. Implement once, correctly
