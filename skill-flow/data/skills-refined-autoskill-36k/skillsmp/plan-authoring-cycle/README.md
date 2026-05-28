# generated: 2025-12-25
# System Auto: last updated on: 2025-12-25T17:25:34
# Plan Authoring Cycle Skill

Guides structured population of implementation plan sections after scaffolding.

## Overview

This is a **Cycle Skill** that defines the ANALYZE-AUTHOR-VALIDATE workflow for filling in plan sections.

## Phases

| Phase | Purpose |
|-------|---------|
| ANALYZE | Read plan, identify empty sections |
| AUTHOR | Populate each section systematically |
| VALIDATE | Verify plan is complete and ready |

## Usage

**Manual:**
```
Skill(skill="plan-authoring-cycle")
```

**From implementation-cycle:** When PLAN phase detects empty sections, this skill can be invoked.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill definition with phase contracts |
| `README.md` | This documentation |

## Section Order

1. Goal - What capability will exist?
2. Effort Estimation - Count files, estimate time
3. Current State - What exists now?
4. Desired State - What should exist?
5. Tests First - What tests verify success?
6. Detailed Design - How to implement?
7. Implementation Steps - Ordered checklist

## Related

- work-creation-cycle: Parallel skill for work items
- close-work-cycle: Parallel skill for closure
- implementation-cycle: Uses this skill during PLAN phase
