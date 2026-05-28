---
title: Use Assets for Output
impact: MEDIUM
impactDescription: Provides resources for generation
tags: anatomy, assets
---

## Use Assets for Output

**Impact: MEDIUM**

Use `assets/` for files that should be part of the agent's output (templates, images, fonts).

**Incorrect (generating from scratch):**

```markdown
Generate a logo pixel by pixel...
```

**Correct (using asset):**

```markdown
Use the brand logo from `assets/logo.png`.
```
