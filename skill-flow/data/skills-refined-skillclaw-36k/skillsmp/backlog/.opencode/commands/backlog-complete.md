---
description: Complete a task - supports worktree and in-session workflows
---

# Complete Task

Finalize a completed task. Supports multiple workflows:

1. **In-Session Mode:** PROMPT.md exists, no worktree - complete task in current session
2. **Worktree Phase 1:** From task worktree - commit, rebase, mark pending merge
3. **Worktree Phase 2:** From main - fast-forward merge, archive, cleanup

**Arguments:** $ARGUMENTS

## Mode Detection

This command automatically detects the workflow mode based on:
- Current git branch (main vs feature branch)
- Whether we're in a worktree
- Whether PROMPT.md exists

## In-Session Mode

**Context:** PROMPT.md exists in current directory, NOT running from a worktree.

1. Extract task ID from PROMPT.md or arguments
2. Commit all changes (except PROMPT.md)
3. If on feature branch: rebase onto main and merge
4. Remove PROMPT.md
5. Update INDEX.md status to Complete
6. Optionally push with `--push` flag

## Worktree Phase 1 (from task worktree)

1. Verify we're on a feature branch (not main)
2. Commit remaining changes (exclude PROMPT.md)
3. Rebase onto local main
4. Mark task as "Pending Merge" in INDEX.md
5. Output instructions to switch to main worktree

## Worktree Phase 2 (from main)

1. Verify we're on main branch
2. Find the worktree branch for the task
3. Verify task status is "Pending Merge" (from worktree branch)
4. Fast-forward merge main to include changes
5. Mark task as Complete
6. Update dependent tasks (cascade unblocking)
7. Archive task files to tasks/archive/
8. Remove worktree and delete branch
9. Optionally push with `--push` flag

## Arguments Reference

| Argument | Description |
|----------|-------------|
| `<task-id>` | Task ID being completed (e.g., CRANE-003) |
| `--push` | Push main to origin after completion |

## Error Handling

- **On main branch (Phase 1):** "Phase 1 must be run from task worktree"
- **Not on main (Phase 2):** "Phase 2 must be run from main worktree"
- **Task not Pending Merge:** "Run Phase 1 from task worktree first"
- **Rebase conflicts:** Show resolution steps

## Related Commands

- `/backlog-launch <ID>` - Launch agent for implementation
- `/backlog-review <ID>` - Transition task to review mode
- `/backlog` - View all tasks
