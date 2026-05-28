---
title: Progressive Disclosure
impact: HIGH
impactDescription: Optimizes token usage
tags: principles, context-loading
---

## Progressive Disclosure

**Impact: HIGH**

Use a three-level loading system to manage context:

1. Metadata (always loaded)
2. SKILL.md body (loaded on trigger)
3. References/Scripts (loaded only when needed)

**Incorrect (flat structure):**

```markdown
<!-- SKILL.md (10,000 lines) -->

# Huge Manual

[...entire content of API docs included directly in SKILL.md...]
```

**Correct (progressive structure):**

```markdown
<!-- SKILL.md (Concise) -->

# API Guide

For detailed endpoint definitions, see [references/api_docs.md](references/api_docs.md).
```
