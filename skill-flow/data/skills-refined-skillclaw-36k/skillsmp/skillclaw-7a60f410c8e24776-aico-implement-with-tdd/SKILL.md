---
name: aico-implement-with-tdd
description: Use this skill when you need to implement a task (frontend or backend) using Test-Driven Development (TDD) principles, ensuring that all steps are verified and constraints are followed.
---

# Skill body

## Prerequisites
- Have a task file in `docs/reference/{frontend|backend}/tasks/` (either `story-*` or `standalone-*`).
- Read the relevant constraint files: 
  - For frontend: `docs/reference/frontend/design-system.md`, `docs/reference/frontend/constraints.md`
  - For backend: `docs/reference/backend/constraints.md`

## Process

0. **Check task file EXISTS** (MANDATORY):
   - Look for `docs/reference/{frontend|backend}/tasks/{story-id}.md`
   - If NOT exists → STOP and inform the user to run the appropriate task breakdown command.

1. **Read constraints FIRST** (before any code):
   - Load the necessary design and constraints files based on the task type.

2. **Execute implementation steps**:
   - Read the "Implementation Steps" section from the task file.
   - For each step:
     - If it's a test step: write a failing test, verify it fails.
     - If it's an implementation step: write the minimal code, verify the test passes.
     - Run verification commands after each step.
     - If a step fails → fix before proceeding.

3. **After all steps**:
   - Run the full test suite.
   - Run any necessary build checks (e.g., type checks, linters).

4. **Update task status**:
   - Update the specific task section in the file.
   - Mark acceptance criteria checkboxes: `- [ ]` → `- [x]`.
   - Change Status from `pending` to `completed`.
   - Notify the PM for acceptance.

## Execution Flow

```
Check Task File → Read Constraints → Execute Steps (TDD) → Verify Each → Run All Tests → Mark Complete → Notify PM
```

## TDD Cycle
- RED (write failing test) → Verify fails → GREEN (implement minimal code) → Verify passes → REFACTOR.