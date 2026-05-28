---
name: finish-task
description: Concludes a task by verifying code (lint/test) and merging changes.
---

# FINISH-TASK

> **Identity**: Code Quality Gatekeeper
> **Goal**: Ensure changes are safe, correct, and merged cleanly.

## Usage

Run this skill when the implementation is complete and you are ready to merge the worktree into main.

## Instructions

1.  **Context Check**: Ensure you are in the correct worktree (`git status`).
2.  **Commit**: Ensure all changes are committed.
3.  **Sync**: Fetch and merge `origin/main` to ensure up-to-date integration.
4.  **Verify**: Run the verification script.
    ```bash
    python3 .agent/skills/common/scripts/verify.py
    ```
5.  **Merge & Cleanup** (If verification passes):
    - Switch to root (`cd ../..`).
    - Merge the branch: `git merge --no-ff <task-branch>`.
    - Delete worktree: `git worktree remove .worktrees/<task-branch>`.
    - Delete branch: `git branch -d <task-branch>`.

## Scripts

- `../common/scripts/verify.py` (Shared Verification Logic)
