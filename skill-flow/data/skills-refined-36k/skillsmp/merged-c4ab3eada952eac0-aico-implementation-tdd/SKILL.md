---
name: aico-implementation-tdd
description: Use this skill when you need to implement tasks for frontend or backend with Test-Driven Development (TDD) principles.
---

# Body of the merged SKILL.md

## Overview

This skill guides you through implementing tasks using Test-Driven Development (TDD) principles. It applies to both frontend and backend tasks, ensuring that you read the necessary task files and constraints, write failing tests first, verify each step, and update task statuses accordingly.

## When to Use

Use this skill when:
- You are asked to "implement a task/plan", "start implementation", or "execute a plan".
- You have a task file (story-* or standalone-*) ready to execute.
- You need to apply TDD principles, such as "write test first" or "test-driven".
- You are fixing bugs and need to write a failing test first.

## TDD Principles

- **Iron Law**: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.
- **TDD Cycle**: RED (failing test) → Verify fails → GREEN (minimal code) → Verify passes → REFACTOR.

## Prerequisites

- A task file located in `docs/reference/{frontend|backend}/tasks/` (story-* or standalone-*).
- Read the relevant constraints and design specifications before coding.

## Implementation Process

### 1. Read Task File (MANDATORY)

- Locate the task file in `docs/reference/{frontend|backend}/tasks/`.
- Accept either:
  - **Story-based**: `story-{story-name}.md`
  - **Standalone**: `standalone-{task-name}.md`
- Ensure the user specifies the task number (e.g., "implement story-user-profile Task 1").

### 2. Read Constraints FIRST

- Read the following files before any coding:
  - `docs/reference/{frontend|backend}/design-system.md`
  - `docs/reference/{frontend|backend}/constraints.md`
  - If applicable, read `docs/reference/{frontend|backend}/designs/{name}.md`.

### 3. Execute Implementation Steps

- Read the "Implementation Steps" section from the task file.
- Execute each step in order:
  - Run the action.
  - Run the verification command after each step.
  - If it fails, fix the issue before proceeding.
  - If it passes, continue to the next step.

### 4. After All Steps

- Run unit tests.
- Run a build check.

### 5. Update Task Status

- Update the specific task section in the task file:
  - Mark acceptance criteria checkboxes: `- [ ]` → `- [x]`.
  - Change Status from `pending` to `completed`.
  - Update the "Progress" section at the bottom of the file.

### 6. Notify Completion

- Show the task file path and task number.
- Show completion status.
- If applicable, check the related story and update its task status.

## Execution Flow

```
Read Task File
     ↓
Read Constraints (design-system.md, constraints.md, designs/)
     ↓
Execute Step 1 → Verify → Pass? → Continue
                      ↓
                     Fail → Fix → Retry
     ↓
Execute Step 2 → Verify → Pass? → Continue
     ↓
     ...
     ↓
Run Unit Tests
     ↓
Run Build Check
     ↓
Update Task File (mark AC completed, update status)
     ↓
Show Completion Summary
```

## Key Rules

- Always read the task file first.
- Always read all constraint files before writing any code.
- Must run verification commands for each step.
- Always run tests before marking the task complete.
- Must update the task file (mark acceptance criteria, update status).

## Common Mistakes

- ❌ Start without reading the task file → ✅ Always read the task file first.
- ❌ Skip reading constraints → ✅ Always read before coding.
- ❌ Skip verification → ✅ Run the verify command for each step.
- ❌ Skip tests → ✅ Run tests before marking complete.
- ❌ Forget to update the task file → ✅ Update acceptance criteria and status.

## TDD Deep Dive

### The TDD Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

### Red-Green-Refactor Cycle

```
RED → Verify Fails → GREEN → Verify Passes → REFACTOR → Repeat
```

### Example Workflow

```bash
# User: "Implement story-user-profile Task 1"

1. ✓ Read task file: docs/reference/frontend/tasks/story-user-profile.md
2. ✓ Read constraints:
   - design-system.md
   - constraints.md
   - designs/user-profile.md (if referenced)

3. ✓ Execute Step 1: Create component file
   → Run: npm run typecheck
   → ✓ Pass

4. ✓ Execute Step 2: Implement layout
   → Run: npm run dev
   → ✓ Pass

5. ✓ Execute Step 3: Add tests
   → Run: npm test Component
   → ✓ 3 tests passed

6. ✓ Run full test suite
   → Run: npm test
   → ✓ All tests passed

7. ✓ Run build
   → Run: npm run build
   → ✓ Build successful

8. ✓ Update task file:
   - Updated Task 1 section
   - Marked all acceptance criteria as completed
   - Status: completed
   - Updated Progress: 1/5 completed

9. ✓ Notify PM for acceptance.
```

## Iron Law

**NO CODE WITHOUT APPROVED PLAN**

This rule is non-negotiable. Before writing code:
1. Task breakdown must exist and be approved.
2. Acceptance criteria must be defined.
3. Dependencies must be identified and available.

### Rationalization Defense

| Excuse                         | Reality                                     |
| ------------------------------ | ------------------------------------------- |
| "It's a simple change"         | Simple changes often have hidden complexity |
| "I'll document after coding"   | Post-hoc documentation is always incomplete |
| "Tests can wait until later"   | Untested code is broken code                |
| "I know what needs to be done" | Assumptions without validation cause bugs   |