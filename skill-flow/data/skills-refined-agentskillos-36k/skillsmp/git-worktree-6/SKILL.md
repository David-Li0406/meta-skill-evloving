---
name: git-worktree
description: Manage Git worktrees for working on multiple branches simultaneously without cloning the repository
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: version-control
---

## What I do

I manage Git worktrees to enable parallel development. I create, list, and remove worktrees so you can work on multiple branches in separate directories without full repository clones.

## When to use me

Use this when:

- You need to work on multiple branches simultaneously
- You're reviewing a PR and need a clean working directory
- You want to avoid stashing or committing WIP changes
- You need to test changes in an isolated environment

## Common Commands

```bash
git worktree list               # List all worktrees
git worktree add <path> <branch>  # Create new worktree
git worktree remove <path>      # Remove worktree
git worktree lock <path>        # Lock worktree from removal
```

## Key Concepts

- **Worktree**: Additional working tree linked to main repo
- **Parent Repository**: The main `.git` directory
- **Locking**: Prevent accidental worktree removal
- **Pruning**: Clean up stale worktree references

## Source Files

- `.git/worktrees/` directory: Worktree metadata
- Parent repository: Main `.git` directory

## Code Patterns

- Create worktrees outside the main project directory
- Use descriptive paths (e.g., `../feature-branch`)
- Always remove worktrees when done to clean up
- Lock worktrees that are actively being used

## Operational Constraints

- Worktree paths must be outside the main repository
- Don't create worktrees on different filesystems (performance)
- Always remove worktrees when finished
- Lock worktrees before long-running operations
