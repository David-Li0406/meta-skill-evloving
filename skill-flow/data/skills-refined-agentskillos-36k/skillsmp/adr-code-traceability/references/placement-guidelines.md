**Skill**: [ADR Code Traceability](../SKILL.md)

# ADR Reference Placement Guidelines

When and where to add ADR references in code for optimal traceability.

---

## When to Add References

### Always Add (File Headers)

Add ADR reference in file header for:

- **New files** created as part of the ADR implementation
- **New modules/packages** introduced by the ADR
- **Configuration files** with settings specific to the ADR

### Selectively Add (Inline Comments)

Add inline ADR comments for:

- **Non-obvious implementation choices** - Why was this approach chosen?
- **Workarounds or constraints** - What limitation drove this decision?
- **Breaking changes** - What changed and why?
- **Performance-critical code** - Why was this optimization necessary?

### Do NOT Add

Skip ADR references for:

- **Every line touched** - Only add where traceability adds value
- **Trivial changes** - Formatting, typo fixes, minor refactors
- **Standard patterns** - Well-known idioms that don't need explanation
- **Test files** - Unless the test approach itself is an ADR decision

---

## Placement Decision Tree

```
Is this a NEW file created by the ADR?
├── Yes → Add reference in file header
└── No → Is the change non-obvious?
    ├── Yes → Add inline comment with reason
    └── No → Skip ADR reference
```

---

## File Header vs Inline Comment

| Placement          | Use For                                     | Example                        |
| ------------------ | ------------------------------------------- | ------------------------------ |
| **File header**    | Entire file implements ADR                  | New service, new module        |
| **Inline comment** | Specific code block relates to ADR          | Algorithm choice, config value |
| **Both**           | New file with specific non-obvious sections | New file with workaround       |

---

## Good vs Bad Examples

### Good: File Header for New Module

```python
"""
Redis cache adapter for session management.

ADR: 2025-12-01-redis-session-cache
"""

class RedisSessionCache:
    ...
```

### Good: Inline for Non-Obvious Choice

```python
# ADR: 2025-12-01-rate-limiting - Using token bucket over sliding window
# for better burst handling in our use case
rate_limiter = TokenBucketLimiter(rate=100, burst=20)
```

### Bad: Unnecessary Reference

```python
# ADR: 2025-12-01-fix-typo  # ❌ Trivial change doesn't need ADR
name = "correct_spelling"
```

### Bad: Every Line

```python
# ADR: 2025-12-01-my-feature  # ❌ Too verbose
import os
# ADR: 2025-12-01-my-feature  # ❌ No value added
import sys
```

---

## Traceability Value Test

Before adding an ADR reference, ask:

1. **Would a future developer benefit from knowing why this exists?**
2. **Is the connection to the ADR non-obvious from context?**
3. **Does this code represent a deliberate decision vs standard practice?**

If all answers are "No" → Skip the reference.
If any answer is "Yes" → Add the reference.

---

## Maintenance

When modifying code with ADR references:

- **Keep reference if ADR still applies** - Implementation evolved but decision stands
- **Remove reference if ADR superseded** - New ADR replaces the old decision
- **Update reference if ADR amended** - Point to the current version

ADR references should track the **decision**, not the **implementation details**.
