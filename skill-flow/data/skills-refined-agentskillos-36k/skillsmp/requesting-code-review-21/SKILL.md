---
name: requesting-code-review
description: Use when you need to dispatch code-reviewer after completing implementation work. Manages the review → fix → re-review loop until zero issues remain.
---

# Requesting Code Review

## Overview

Code review catches defects before they cascade. This skill guides dispatching the `code-reviewer` agent after implementation, handling review results, dispatching `bug-worker` for fixes, and iterating until zero issues remain. The goal is clean code, not just working code.

## When to Use

**Mandatory:**
- After completing a task from a work plan
- After implementing a feature or fix
- Before merging to main branch

**Recommended:**
- When stuck and seeking a fresh perspective
- Before major refactoring (establish quality baseline)
- After resolving complex bugs

## Core Principle

**Review early, review often.** Small, frequent reviews catch issues when they're cheap to fix. Large, infrequent reviews let defects compound.

## The Review Loop

```
┌─────────────────┐
│  Implementation │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  code-reviewer  │──────┐
└────────┬────────┘      │
         │               │
    ┌────┴────┐          │
    │ Issues? │          │
    └────┬────┘          │
         │               │
    Yes  │  No           │
         │   └───────────┼──► Done (proceed)
         ▼               │
┌─────────────────┐      │
│   bug-worker    │      │
└────────┬────────┘      │
         │               │
         └───────────────┘
              (re-review)
```

Exit when: Zero issues across all categories (Critical, Important, Minor).

## Step 1: Prepare for Review

Before dispatching review:

1. **Verify implementation is complete.** Don't review partial work.
2. **Run verification commands yourself first.** Catch obvious failures before review:
   ```bash
   pytest [test_files] -v
   ruff check [files]
   mypy [files]
   ```
3. **Capture git state** for review context:
   ```bash
   BASE_SHA=$(git rev-parse HEAD~1)  # Before your changes
   HEAD_SHA=$(git rev-parse HEAD)     # After your changes
   ```

## Step 2: Dispatch Code Reviewer

Invoke the `code-reviewer` agent with:

- **What was implemented**: Brief description of the feature/fix
- **Task reference**: Link to work plan task or requirements
- **Files changed**: List of modified files
- **Base and head commits**: For understanding the diff

The reviewer returns:
- Status (APPROVED / BLOCKED)
- Issue summary (Critical, Important, Minor counts)
- Detailed issues with Location, Issue, Impact, Fix

## Step 3: Handle Review Response

### Zero Issues

If the review returns APPROVED with zero issues:
1. Celebrate briefly
2. Proceed to next task

### Any Issues Found

If the review identifies issues (any category):

1. **Dispatch `bug-worker` agent** with the review output
2. `bug-worker` will:
   - Fix all issues (Critical → Important → Minor)
   - Commit each fix individually
   - Trigger re-review automatically
3. **Continue loop** until zero issues

**Fix ALL issues — including every Minor issue.** The goal is ZERO issues on re-review. Minor issues are not optional; they indicate real concerns about code quality.

## Step 4: Track Issues Across Cycles

Maintain a mental model of prior issues across review cycles:

| Cycle | Critical | Important | Minor | Status |
|-------|----------|-----------|-------|--------|
| 1     | 2        | 3         | 5     | Fix    |
| 2     | 0        | 1         | 2     | Fix    |
| 3     | 0        | 0         | 0     | Done   |

Only mark an issue resolved when the re-reviewer explicitly confirms it. Don't assume fixes worked.

## Handling Failures

| Situation | Action |
|-----------|--------|
| Zero issues | Proceed to next task |
| Any issues | Dispatch bug-worker, re-review |
| Operational error | Stop, report to human, wait for guidance |
| Agent timeout | Retry with focused scope (changed files only) |
| 3 failed retries | Escalate to human |

## Integration with Agents

This skill orchestrates two agents:

| Agent | Role | When Invoked |
|-------|------|--------------|
| `code-reviewer` | Finds issues | After implementation, after fixes |
| `bug-worker` | Fixes issues | When review finds any issues |

## Anti-Rationalizations

- "This change is simple, skip review" — Simple changes still need verification. Small bugs cause big problems.
- "I'll fix that minor issue later" — Later never comes. Fix all issues now.
- "It's just a style issue" — Style consistency reduces cognitive load. Fix it.
- "The reviewer is being pedantic" — If you disagree, provide technical reasoning with evidence. Don't just dismiss.
- "Re-review is overkill" — Fixes can introduce new issues. Always re-review.

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Skipping review for "simple" changes | Defects hide in simple code | Review everything |
| Proceeding with unfixed issues | Technical debt compounds | Zero issues before proceeding |
| Not tracking issues across cycles | Lose sight of what was fixed | Maintain issue tracking |
| Assuming fixes worked | Fixes can introduce regressions | Always re-review |
| Dismissing minor issues | Minor issues indicate real concerns | Fix all categories |

## Quick Reference

```
1. Complete implementation
2. Run verification commands (pytest, ruff, mypy)
3. Dispatch code-reviewer
4. If issues found → dispatch bug-worker → re-review
5. Repeat until zero issues
6. Proceed to next task
```

## Summary

1. **Review after every completed task.** Don't batch reviews.
2. **Fix ALL issues.** Critical, Important, AND Minor. Zero issues is the goal.
3. **Always re-review after fixes.** Fixes can introduce new problems.
4. **Track issues across cycles.** Verify each issue is resolved.
5. **Never skip review.** There's no such thing as a change too simple to review.
