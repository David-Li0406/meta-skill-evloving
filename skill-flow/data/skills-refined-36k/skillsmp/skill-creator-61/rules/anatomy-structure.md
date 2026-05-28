---
title: Standard Directory Structure
impact: CRITICAL
impactDescription: Ensures tools can parse the skill
tags: anatomy, structure
---

## Standard Directory Structure

**Impact: CRITICAL**

Every skill must follow the standard directory structure with `SKILL.md` at the root and optional resources in specific folders.

**Incorrect (messy structure):**

```text
my-skill/
├── README.txt
├── code.py
├── doc.pdf
└── skill_info.md
```

**Correct (standard structure):**

```text
my-skill/
├── SKILL.md (required)
├── scripts/ (optional, executable code)
├── references/ (optional, documentation)
└── assets/ (optional, output files)
```
