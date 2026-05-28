---
name: git-worktrees
description: "Use for parallel branch development with workspace isolation."
---

# Git Worktrees

Work on multiple branches simultaneously. Each worktree = isolated workspace.

## Workflow

```
FETCH   -> git fetch origin (ensure latest remote state)
LOCATE  -> Find .worktrees/ or worktrees/
VERIFY  -> Ensure directory is gitignored
CREATE  -> git worktree add .worktrees/name origin/main -b branch/name
SETUP   -> Install dependencies
BASELINE -> Verify tests pass
WORK    -> Implement in isolation
CLEANUP -> git worktree remove when done
```

## Create Worktree

```bash
# ALWAYS fetch first to get latest remote state
git fetch origin

# Check existing directories
ls -d .worktrees worktrees 2>/dev/null

# Verify gitignored
git check-ignore -q .worktrees || echo ".worktrees/" >> .gitignore

# Create from origin/main (NOT local main) to ensure latest code
git worktree add .worktrees/feature-auth origin/main -b feature/auth
cd .worktrees/feature-auth

# Setup
[ -f package.json ] && npm install

# Baseline
npm test  # Must pass before changes
```

**Why `origin/main`?** Local `main` may be behind remote. Always base new work on the latest remote state to avoid merge conflicts and building on stale code.

## Cleanup

```bash
cd /path/to/main/repo
git worktree remove .worktrees/feature-auth
git branch -d feature/auth  # If merged
```

## Commands

```bash
git worktree list                          # List all
git worktree add .worktrees/fix bugfix/123 # Existing branch
git worktree remove .worktrees/feature     # Remove
git worktree prune                         # Clean stale
```

## Decision Criteria

| Situation | Action |
|-----------|--------|
| Feature needs isolation | Create worktree |
| Quick one-file fix | Regular branch |
| Baseline tests fail | Ask user before proceeding |
| Work complete | Remove worktree |

## Red Flags

- **Skipping `git fetch origin` before creating worktree**
- **Creating from local `main` instead of `origin/main`**
- Creating without verifying gitignored
- Proceeding with failing baseline
- Leaving stale worktrees

**Pairs with:** pr-workflow, commit-discipline, tdd
