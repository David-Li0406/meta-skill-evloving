---
name: orchestrate-[mission]
description: [Action] [Context] by coordinating specialized skills. Use when [User Trigger].
license: Apache-2.0
metadata:
  author: [Author]
  version: "1.0"
---

# Mission: [Mission Name]

This skill orchestrates the [Mission] by delegating to specialized skills.

## When to use this skill

Use this skill when you need to [High-level Goal] which requires coordinating [Skill A], [Skill B], etc.

## Dependencies (Sub-Skills)

- `[skill-a]`: For [Task A]
- `[skill-b]`: For [Task B]

## Execution Plan

1.  **Preparation**:
    - Call `[skill-a]` to prepare the environment.
    - _Decision Point_: If preparation fails, abort.

2.  **Execution**:
    - Call `[skill-b]` to perform the main task.
    - Ensure inputs from Step 1 are passed correctly.

3.  **Verification**:
    - Call `[skill-a]` again to verify final state.

## Routing Logic

- If User asks for [X], use `[skill-a]`.
- If User asks for [Y], use `[skill-b]`.

## Progressive Disclosure

If this mission involves complex orchestration logic or many sub-tasks, move detailed SOPs to `references/ORCHESTRATION.md`.
