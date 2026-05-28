---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification
---

# Using Git Worktrees

## Overview

This skill provides two scripts for managing git worktrees:

1. **create-worktree.sh** - Creates isolated workspaces for parallel development
2. **cleanup-worktree.sh** - Removes worktrees and optionally their branches

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Creating a Worktree

Use the `create-worktree.sh` script:

```bash
./scripts/create-worktree.sh <branch-name>
```

**Arguments:**

- `branch-name` (required): Name of branch to create/checkout

**What it does:**

- Creates worktree in `.worktrees/<branch-name>`
- Creates branch if it doesn't exist, or checks out existing branch
- Verifies `.worktrees` is in `.gitignore` (adds and commits if needed)
- Returns the full path to the created worktree

**Example:**

```bash
# Create worktree for feature/auth branch
WORKTREE_PATH=$(./scripts/create-worktree.sh feature/auth)
cd "$WORKTREE_PATH"
```

**Arguments:**

- `branch-name` (required): Name of branch to create/checkout
- `location` (optional): One of `.worktrees`, `worktrees`, or `global`

**What it does:**

- Creates branch if it doesn't exist, or checks out existing branch
- Auto-detects worktree location (prefers `.worktrees` > `worktrees`)
- Verifies project-local directories are in `.gitignore` (adds and commits if needed)
- Returns the full path to the created worktree

**Example:**

```bash
# Create worktree for feature/auth branch
WORKTREE_PATH=$(./scripts/create-worktree.sh feature/auth)
cd "$WORKTREE_PATH"
```

## Cleaning Up a Worktree

Use the `cleanup-worktree.sh` script:

```bash
./scripts/cleanup-worktree.sh <worktree-path> [--delete-branch]
```

**Arguments:**

- `worktree-path` (required): Path to the worktree to remove
- `--delete-branch` (optional): Also delete the associated branch

**What it does:**

- Removes the worktree directory
- Optionally deletes the branch if `--delete-branch` is provided
- Validates worktree exists before attempting removal

**Example:**

```bash
# Remove worktree only
./scripts/cleanup-worktree.sh .worktrees/feature/auth

# Remove worktree and delete branch
./scripts/cleanup-worktree.sh .worktrees/feature/auth --delete-branch
```

## Workflow

### Starting Work

1. Announce you're using the skill
2. Run `create-worktree.sh` with the branch name
3. Change to the worktree directory
4. Run project setup (npm install, etc.) if needed
5. Verify tests pass before starting work

### Finishing Work

1. Ensure changes are committed/pushed if needed
2. Return to main workspace
3. Run `cleanup-worktree.sh` with appropriate flags
4. If branch was merged, use `--delete-branch`

## Location Strategy

All worktrees are created in `.worktrees/` (hidden, project-local).

**Safety:** The `.worktrees` directory is automatically added to `.gitignore` if not already ignored.

## Integration

**Called by:**

- **brainstorming** (Phase 4) - When implementation follows approved design
- Any skill needing isolated workspace

**Pairs with:**

- **finishing-a-development-branch** - For cleanup after work complete
- **executing-plans** or **subagent-driven-development** - Work happens in worktree
