---
name: git-worktrees
description: Create, list, and remove git worktrees for parallel agent work. Use when you need isolated workdirs, new worktree branches, or safe cleanup workflows.
---

# Git Worktrees

## Canonical path

All worktrees go in `/workspaces/worktrees/`. This is a bind mount configured in devcontainer.json.

Example: `/workspaces/worktrees/materials-authoring`

## Use the project scripts

- Create: `scripts/worktree-new.sh /workspaces/worktrees/<name> <branch> [--force]`
- Remove: `scripts/worktree-remove.sh /workspaces/worktrees/<name> [--force]`
- List: `git worktree list`

## Notes

- The scripts validate the repo state and install npm deps after creation.
- Use `--force` only when you understand the safety checks you are bypassing.
- Cleanup order: remove the worktree first, then delete the branch.
