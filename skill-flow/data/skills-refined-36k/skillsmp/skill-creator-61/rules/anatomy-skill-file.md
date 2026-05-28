---
title: SKILL.md Essentials
impact: CRITICAL
impactDescription: Primary interface for the agent
tags: anatomy, skill-md
---

## SKILL.md Essentials

**Impact: CRITICAL**

SKILL.md is the entry point. It requires YAML frontmatter (name/description) and a Markdown body.

**Incorrect (missing frontmatter):**

```markdown
# My Skill

Here is how to use this skill...
```

**Correct (valid frontmatter):**

```markdown
---
name: my-skill
description: Use this skill when...
---

# My Skill

Here is how to use this skill...
```
