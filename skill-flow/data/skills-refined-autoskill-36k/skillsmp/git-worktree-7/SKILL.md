---
name: git-worktree
description:
  Manage Git worktrees for isolated parallel development. Use when reviewing PRs, working on
  multiple features, or running autonomous loops without disturbing your main checkout.
---

# Git Worktree Manager

Git worktrees let you have multiple working directories from the same repo. Each worktree has its
own branch checked out, so you can work on multiple things in parallel.

## Why Use Worktrees

- **Code review**: Review a PR without stashing/switching from your current work
- **Parallel features**: Work on feature-a and feature-b simultaneously
- **Testing**: Compare behavior across branches side-by-side
- **Ralph loops**: Run autonomous loops in isolation

## Critical Rule

**Never use `git worktree add` directly.** Always use the manager script:

```bash
~/.claude/skills/git-worktree/scripts/worktree-manager.sh <command>
```

The script handles essential setup (copying `.env` files, updating `.gitignore`) that raw git
commands skip.

## Commands

### Create a worktree

```bash
# Create from main (default)
worktree-manager.sh create feature-branch

# Create from specific base
worktree-manager.sh create feature-branch --from develop
```

Creates `.worktrees/feature-branch/` with:

- The branch checked out
- All `.env*` files copied (except `.env.example`)
- `.worktrees/` added to `.gitignore`

### List worktrees

```bash
worktree-manager.sh list
```

Shows all worktrees with their branches and paths.

### Switch to a worktree

```bash
worktree-manager.sh switch feature-branch
# or
worktree-manager.sh go feature-branch
```

Outputs the path - use `cd $(worktree-manager.sh go feature-branch)` to actually change directory.

### Copy env files

```bash
worktree-manager.sh copy-env feature-branch
```

Manually copy `.env*` files to an existing worktree.

### Cleanup

```bash
# Remove a specific worktree
worktree-manager.sh cleanup feature-branch

# Remove all worktrees (with confirmation)
worktree-manager.sh cleanup --all
```

## Directory Structure

```
my-project/
├── .worktrees/           # All worktrees live here
│   ├── feature-a/        # One directory per worktree
│   └── feature-b/
├── .gitignore            # Automatically updated to ignore .worktrees/
└── ...                   # Main checkout
```

## Workflow Examples

### Review a PR

```bash
# Create worktree for the PR branch
worktree-manager.sh create pr-branch-name

# Navigate to it
cd .worktrees/pr-branch-name

# Review, run tests, etc.
pnpm test

# When done, cleanup
cd ../..
worktree-manager.sh cleanup pr-branch-name
```

### Parallel Development

```bash
# Terminal 1: Main feature work
cd my-project
git checkout feature-a
# ... work ...

# Terminal 2: Quick bugfix
cd my-project/.worktrees/hotfix-123
# ... fix and commit ...
```
