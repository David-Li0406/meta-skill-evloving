<!--
CONTRIBUTION GUIDELINES - READ BEFORE CREATING NEW PATTERNS

Design Principle: Patterns should be comprehensive, not fragmented.
Target: 2-3 patterns per task. If a task needs 7+ patterns, they're too fragmented.

BEFORE CREATING A NEW PATTERN:
1. Search existing patterns - does this content fit in one of them?
2. Prefer updating existing patterns over creating new ones
3. Only create new if the topic is genuinely distinct

NAMING: File must match category prefix (serve-*, engine-*, graph-*, etc.)

VALIDATION (required before committing):
  python scripts/validate-patterns.py
  python scripts/build_agents.py
  python scripts/validate-counts.py  # from repo root

See CONTRIBUTING.md for full guidelines.
-->
---
title: Pattern Title Here
description: Brief description of what this pattern covers
impact: CRITICAL|HIGH|MEDIUM
category: serve|engine|graph|multigpu|model|perf|deploy
tags: tag1, tag2, tag3
consolidates:
  - original-rule-1.md
  - original-rule-2.md
---

# Pattern Title

**Category:** {category} | **Impact:** {LEVEL}

Brief overview paragraph explaining the pattern's purpose, when to use it, and measurable impact.

---

## Core Concepts

### Concept 1

Explanation of the first core concept.

**Pattern:**

```python
# Code example
from max.serve import Server
```

### Concept 2

Explanation of the second core concept.

**Pattern:**

```bash
# CLI example
max serve --model-path model-name
```

---

## Common Patterns

### Pattern Name 1

**When:** Describe the scenario

**Do:**
```python
# Correct pattern
```

**Don't:**
```python
# Anti-pattern to avoid
```

---

## Decision Guide

| Scenario | Approach | See Also |
|----------|----------|----------|
| Scenario 1 | Use approach A | `related-pattern.md` |
| Scenario 2 | Use approach B | `another-pattern.md` |

---

## Quick Reference

- **Key point 1**: Brief explanation
- **Key point 2**: Brief explanation
- **Key point 3**: Brief explanation

---

## Related Patterns

- [`related-pattern.md`](related-pattern.md) — When to use instead
- [`another-pattern.md`](another-pattern.md) — Use together for X

---

## References

- [Official Documentation](https://docs.modular.com/max/)
