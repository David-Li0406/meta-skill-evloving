---
name: extreme-programming-workflow
description: Use this skill when implementing features, adding functionality, or doing test-driven development. It orchestrates the Extreme Programming workflow, coordinating planning, TDD, refactoring, and commits.
---

# Extreme Programming Workflow

## Overview

This skill orchestrates the full XP workflow for feature implementation. It coordinates sub-skills and ensures proper sequencing of phases.

## The XP Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  📋 PLAN     → Discuss and break down the feature          │
│  🔴 DEVELOP  → TDD cycle (red-green)                       │
│  🔵 REFACTOR → Improve design (tests stay green)           │
│  💾 COMMIT   → Save working state                          │
│  🔁 ITERATE  → Next task or feature complete               │
└─────────────────────────────────────────────────────────────┘
```

## Phase 1: Planning (📋 PLAN)

**Goal:** Understand and decompose the feature before writing any code.

1. **Invoke:** Switch to `planning` skill
2. Discuss requirements and break down the feature into tasks.

---

## Phase 2: Development (🔴 DEVELOP)

**Goal:** Implement the task using strict TDD.

1. **Invoke:** Switch to `development` skill
2. Follow the TDD cycle:
   - Write a failing test (RED)
   - Write minimum code to pass the test (GREEN)
   - Verify all tests are passing

---

## Phase 3: Refactoring (🔵 REFACTOR)

**Goal:** Improve code design while keeping tests green.

1. **Invoke:** Switch to `refactor` skill
2. Ensure all tests pass before continuing.

---

## Phase 4: Commit (💾 COMMIT)

**Goal:** Save working state with a clear, simple commit message.

1. **Invoke:** Switch to `commit-helper` skill
2. Commit after each passing test, after completing a task, or after a refactoring session.

---

## Phase 5: Iterate (🔁 ITERATE)

**Goal:** Continue until the feature is complete.

1. Mark the task as done.
2. Review remaining tasks and adjust the plan if needed.
3. Return to Phase 2 for the next task.
4. When all tasks are complete, the feature is done.

---

## Core Principles (Always Apply)

- **Communication first** — discuss before coding.
- **Small steps** — one task, one test, one change at a time.