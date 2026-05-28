---
name: plan-review-skill
description: Use when about to implement a plan, when plan seems incomplete or has gaps, when unsure if tasks are feasible, or when validating spec before coding
---

# Plan Review Skill

Two-phase review: analyze/document findings (separate agent), then apply approved changes (main context).

## Quick Reference

| Phase | Where | Why |
|-------|-------|-----|
| Phase 1: Review | Separate agent | Context-intensive, autonomous |
| Phase 2: Apply | Main context | Needs user interaction |

**Input:** Plan path (e.g., `_tasks/15-feature/02-plan.md`)
**Output:** `_plan-review.md` with findings + recommendation

## Baseline Problem (Why Separate Agent)

**Without separation:** Main agent reads plan, creates review doc, manages iterations, tracks findings → consumes significant context before user interaction even begins.

**With separation:** Single Task tool call → agent returns summary only → main context preserved for Phase 2 user discussion.

Context savings: ~80% reduction in main conversation token usage for Phase 1.

---

## Phase 1: Review → Separate Agent

Spawn single agent for entire Phase 1:

```
Task tool (general-purpose):
  description: "Plan review: {PLAN_NAME}"
  prompt: |
    Review {TARGET} and create {TARGET_DIR}/_plan-review.md.

    **Iterate (max 4)** until no NEW findings. Assess:
    - Completeness: requirements covered? edge cases?
    - Feasibility: achievable? hidden complexity? dependencies?
    - Clarity: implementer can follow? specific paths? verification steps?
    - YAGNI: unnecessary scope? duplication?

    **Checklist:** tasks have file paths, verification steps, correct order, no scope creep.

    Categorize: Critical/Important/Minor. Commit review. Return summary only.
```

**After agent returns:** Present summary to user, ask which findings to address/skip. **STOP for user direction.**

---

## Phase 2: Apply → Main Context

*After user approval only.* Why main context? User interaction needed.

1. Apply user-approved fixes to source plan
2. Mark findings `[x]` in `_plan-review.md`
3. Commit: `git commit -m "plan: apply review feedback for {PLAN_NAME}"`
4. Update `_plan-review.md` with Resolution section (addressed/skipped)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Running Phase 1 in main context | Always spawn agent - preserves context |
| Applying fixes without user approval | STOP after Phase 1, wait for direction |
| Skipping commit after review | Commit `_plan-review.md` before presenting |
| Over-iterating (>4 rounds) | Quality gate: stop when no NEW findings |

---

## Example

```
User: /plan-review _tasks/20-e2e-testing/02-plan.md
Claude: [Spawns Phase 1 agent]
Agent: "2 Critical, 3 Important, 1 Minor. Needs revisions."
Claude: Plan review complete. [summary] Full details: _plan-review.md
User: Address Critical and Important. Skip Minor.
Claude: [Phase 2 in main context - applies fixes]
```
