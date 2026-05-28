---
title: Use References for Knowledge
impact: HIGH
impactDescription: Keeps SKILL.md lean
tags: anatomy, references
---

## Use References for Knowledge

**Impact: HIGH**

Use `references/` for documentation, schemas, and policies. Do not duplicate this info in SKILL.md.

**Incorrect (bloated SKILL.md):**

```markdown
# Database Schema

[...500 lines of schema definition...]
```

**Correct (referenced schema):**

```markdown
# Database Schema

For table definitions, see [references/schema.md](references/schema.md).
```
