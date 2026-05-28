---
name: wrap-up
description: Finalize work session with optional commit and skill review.
---

# Wrap Up

Use this skill when implementation or investigation is complete.

## Flow

### If code changed:

1. Use `verify` skill (if not already done)
2. Use `git-commit` skill, ask user before committing
3. Use `skill-review` skill

### If investigation only:

1. Use `skill-review` skill
