# generated: 2025-12-25
# System Auto: last updated on: 2026-01-03T14:41:12
# Plan Validation Cycle Skill (Bridge)

Validates implementation plan readiness before entering DO phase.

## Overview

This is a **Validation Skill** (bridge) that acts as a quality gate between plan-authoring-cycle and implementation-cycle.

## Phases

| Phase | Purpose |
|-------|---------|
| CHECK | Verify required sections exist |
| VALIDATE | Check section content quality |
| L4_ALIGN | Match plan against L4 functional requirements |
| APPROVE | Confirm plan is ready |

## Usage

**Manual:**
```
Skill(skill="plan-validation-cycle")
```

**From implementation-cycle:** Optional quality gate before DO phase.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill definition with phase contracts |
| `README.md` | This documentation |

## Quality Checks

- Goal: Single sentence, measurable
- Effort: Real numbers from file analysis
- Tests: Concrete assertions
- Design: File paths and code snippets
- Steps: Actionable checklist items

## L4 Alignment (E2-247)

L4_ALIGN phase reads `.claude/haios/manifesto/L4-implementation.md` and checks:
1. Find work_id in L4 (pattern: `### ModuleName (work_id)`)
2. Extract function requirements from table
3. Match against plan deliverables
4. Report gaps for operator acceptance

## Related

- plan-authoring-cycle: Populates plan sections
- implementation-cycle: Uses validated plans
- close-work-cycle: Parallel validation pattern
