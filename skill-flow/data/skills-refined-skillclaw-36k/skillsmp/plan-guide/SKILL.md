---
name: plan-guide
description: vive-specific planning guidance.
allowed-tools: Read, Grep, Glob
---

# Planner Guide (vive)

## Role
- **Analyst**: Understand the current codebase and requirements.
- **Architect**: Design the solution structure (Rust modules, TUI layout).
- **Planner**: Break down the solution into small, executable steps (Issues/Tasks).

## Workflow

1.  **Analyze**:
    - Read `docs/requirements.md`, `docs/architecture.md`, and `docs/spec-ja.md`.
    - Check the current Rust codebase (`src/`).
    - Identify missing components or inconsistencies.

2.  **Plan**:
    - Create a step-by-step plan.
    - Identify dependencies (e.g., "Need Core Discovery before UI Integration").

3.  **Output**:
    - List of tasks/issues to be created.
    - Critical path analysis.
    - Architecture diagrams (Mermaid) if needed.

## Guidelines
- **Idempotency**: Operations should be safe to run multiple times.
- **Isolation**: Prefer using Git Worktrees for parallel tasks.
- **Rust Idioms**: Ensure the plan respects Rust ownership/borrowing rules and module structure.
