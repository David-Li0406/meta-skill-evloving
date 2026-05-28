---
name: frontend-implementation-tdd
description: Use this skill when you need to implement frontend tasks using Test-Driven Development (TDD), ensuring all constraints are followed and tests are written before code.
---

# Body of the merged SKILL.md

## Overview

This skill guides you through implementing frontend tasks using Test-Driven Development (TDD). It emphasizes reading all necessary constraint files before coding, writing failing tests first, and verifying each step of the implementation process.

## When to Use

Use this skill when:
- The user requests to "implement this", "start implementation", or "execute plan".
- You have an implementation plan ready and need to execute it.
- The user specifies to "use TDD", "write test first", or "test-driven" for frontend code.
- You are fixing UI bugs and need to write a failing test that reproduces the bug first.

## Prerequisites

- A task file must exist in `docs/reference/frontend/tasks/` (use `/frontend.tasks` first if not exists).
- Read `design-system.md`, `constraints.md`, and any relevant design specifications before coding.

## Process

1. **Check Task File Exists** (MANDATORY):
   - Look for `docs/reference/frontend/tasks/{story-id}.md`.
   - If it does not exist, stop and instruct the user to run `/frontend.tasks` first.

2. **Read Constraints** (before any code):
   - `docs/reference/frontend/design-system.md` - Colors, typography, spacing.
   - `docs/reference/frontend/constraints.md` - Tech stack, patterns.
   - `docs/reference/frontend/designs/{name}.md` - Component specifications if referenced.

3. **Execute Implementation Steps**:
   - Read the "Implementation Steps" section from the task file.
   - Execute each step in order, running the verification command after each step.
   - If verification fails, fix the issue before proceeding. If it passes, continue to the next step.

4. **After All Steps**:
   - Run unit tests.
   - Run a build check.

5. **Update Task Status**:
   - Update the specific task section in the task file, marking acceptance criteria checkboxes and changing the status from `pending` to `completed`.

6. **Notify Completion**:
   - Inform the user of the task file path and task number.
   - Notify the PM for acceptance, checking related tasks and updating the story status if necessary.

## Execution Flow

```
Check Task File → Read Constraints → Execute Steps → Verify Each → Test → Mark Complete → Notify PM
```

## Step Execution Rules

- **Follow Constraints Exactly**: Always adhere to the design system and constraints.
- **Verify Before Proceeding**: Each step must be verified before moving on.
- **No Skipping**: Execute all steps in order without skipping any verifications.

## Post-Implementation Checklist

1. Run tests: `npm test [component]`.
2. Run build: `npm run build`.
3. Update task status in the task file.
4. Notify PM of completion and request acceptance.
5. Commit changes when ready.

## Error Handling

| Error Type           | Action                                 |
| -------------------- | -------------------------------------- |
| TypeScript error     | Fix type issues, re-verify             |
| Test failure         | Debug test, fix implementation or test |
| Build failure        | Check imports, fix errors              |
| Constraint violation | Re-read constraints, align code        |

## TDD Deep Dive

### The TDD Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

### Red-Green-Refactor Cycle

```
RED → Verify Fails → GREEN → Verify Passes → REFACTOR → Repeat
```

### Common Mistakes

- Implementing without reading the task file.
- Skipping constraints or verification steps.
- Forgetting to run tests before marking tasks complete.

## Key Rules

- Always read the task file and constraints before coding.
- Run verification commands for each step.
- Update task status and notify the PM after completion.

## Iron Law

**NO CODE WITHOUT APPROVED PLAN**

This rule is non-negotiable. Before writing code, ensure that:
1. The task breakdown is approved.
2. Acceptance criteria are defined.
3. Dependencies are identified and available.