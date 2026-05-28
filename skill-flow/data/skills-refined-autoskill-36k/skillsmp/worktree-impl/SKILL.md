---
name: worktree-impl
description: Create a git worktree for isolated implementation after planning. Use when starting implementation or when a clean worktree is requested.
---

# Git Worktree Implementation

## Workflow

1. Confirm the current directory is a git repo.
2. Fetch latest refs: `git fetch origin`.
3. List existing worktrees: `git worktree list`.
4. Decide branch name.
   - If a name is provided, use it.
   - Otherwise infer naming from `git branch -r` and propose a name for approval.
5. Determine base branch:
   - `git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'`
6. Create the worktree:
   - `git worktree add -b <branch-name> .worktrees/<sanitized-name> origin/<base>`
   - `<sanitized-name>` replaces `/` with `-`.
7. Offer next actions:
   - `cd <worktree-path> && codex`
   - Continue in current session after `cd`

## Placement rules

- Place worktrees under `<repo>/.worktrees/<branch-name>/`.
- Keep `.worktrees/` out of version control (add to `.gitignore` if needed).
