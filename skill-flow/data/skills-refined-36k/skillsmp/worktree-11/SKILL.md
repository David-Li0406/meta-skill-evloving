---
name: worktree
description: Manage git worktrees. Use when user wants to create, list, delete, or switch worktrees. Helps with branch-based development workflows where each branch has its own working directory.
---

# Git Worktree Management

## Overview

Git worktrees create isolated working directories that share the same repository. Work on multiple branches simultaneously without stashing or switching.

**Announce at start:** "I'm using the worktree skill to manage git worktrees."

## Quick Commands

```bash
# Create worktree with new branch
git worktree add .worktrees/<name> -b <branch-name>

# Create worktree from existing branch
git worktree add .worktrees/<name> <existing-branch>

# List worktrees
git worktree list

# Remove worktree
git worktree remove .worktrees/<name>

# Prune stale worktrees
git worktree prune
```

## Recommended Directory Structure

```
project/
├── .worktrees/           # Hidden, keeps project root clean
│   ├── feature-auth/     # Worktree for auth feature
│   ├── bugfix-login/     # Worktree for login fix
│   └── experiment-new-ui/ # Experimental work
├── .gitignore            # Must include .worktrees/
└── ... (main working tree)
```

**Why `.worktrees/`:**
- Hidden (starts with dot)
- Project-local (easy to find)
- Clear naming convention

## Setup Workflow

### 1. Detect Current Location

```bash
# Check if already in a worktree
git rev-parse --is-inside-work-tree
git worktree list | grep "$(pwd)"

# Get main repo root
git rev-parse --show-toplevel
```

### 2. Verify .gitignore

**CRITICAL:** Before creating worktrees, ensure `.worktrees/` is in `.gitignore`:

```bash
# Check if already ignored
grep -q "^\.worktrees/$" .gitignore && echo "OK" || echo "MISSING"

# Add if missing
echo ".worktrees/" >> .gitignore
git add .gitignore
git commit -m "chore: add .worktrees to gitignore"
```

### 3. Create Worktree

```bash
# Create directory if needed
mkdir -p .worktrees

# New branch from current HEAD
git worktree add .worktrees/<name> -b <branch-name>

# New branch from specific base
git worktree add .worktrees/<name> -b <branch-name> origin/main

# From existing remote branch
git fetch origin
git worktree add .worktrees/<name> origin/<branch-name>
```

### 4. Post-Creation Setup

Each worktree needs its own setup:

```bash
cd .worktrees/<name>

# Node.js
yarn install  # or npm install

# Nuxt
npx nuxt prepare

# Python
pip install -r requirements.txt

# Rust
cargo build
```

## Common Operations

### List All Worktrees

```bash
git worktree list
# Output:
# /path/to/project           abc1234 [main]
# /path/to/project/.worktrees/feature  def5678 [feature-branch]
```

### Switch to Worktree

```bash
cd .worktrees/<name>
```

### Remove Worktree

```bash
# Safe remove (checks for uncommitted changes)
git worktree remove .worktrees/<name>

# Force remove
git worktree remove --force .worktrees/<name>

# Also delete branch
git worktree remove .worktrees/<name>
git branch -d <branch-name>
```

### Clean Up Stale References

```bash
# Remove worktree info for deleted directories
git worktree prune

# Check what would be pruned
git worktree prune --dry-run
```

### Move Worktree

```bash
git worktree move .worktrees/<old-name> .worktrees/<new-name>
```

## Branch Naming Conventions

| Prefix | Use Case | Example |
|--------|----------|---------|
| `feature/` | New features | `feature/user-auth` |
| `bugfix/` | Bug fixes | `bugfix/login-crash` |
| `hotfix/` | Urgent fixes | `hotfix/security-patch` |
| `experiment/` | Experimental work | `experiment/new-ui` |
| `refactor/` | Code refactoring | `refactor/api-cleanup` |

Worktree directory mirrors branch:
- Branch: `feature/user-auth`
- Worktree: `.worktrees/feature-user-auth`

## Integration with Development

### Starting Feature Work

```bash
# 1. Create worktree
git worktree add .worktrees/feature-x -b feature/x origin/main

# 2. Setup
cd .worktrees/feature-x
yarn install
npx nuxt prepare  # for Nuxt projects

# 3. Verify clean baseline
yarn test
```

### Finishing Feature Work

```bash
# 1. From worktree, push and create PR
git push -u origin feature/x

# 2. After merge, cleanup
cd /path/to/main/repo
git worktree remove .worktrees/feature-x
git branch -d feature/x
```

### Parallel Development

Work on multiple features simultaneously:

```bash
# Terminal 1 - Feature A
cd .worktrees/feature-a
yarn dev --port 3001

# Terminal 2 - Feature B
cd .worktrees/feature-b
yarn dev --port 3002

# Terminal 3 - Main
yarn dev --port 3000
```

## Troubleshooting

### "fatal: '<path>' is a worktree but..."

Branch is already checked out:
```bash
# Check where branch is checked out
git worktree list | grep <branch-name>

# Use different branch name or remove existing worktree
```

### "fatal: '<branch>' is already checked out"

```bash
# Create new branch instead
git worktree add .worktrees/<name> -b <new-branch-name>
```

### Worktree shows wrong branch

```bash
# Check actual state
cd .worktrees/<name>
git status
git branch

# If corrupted, remove and recreate
git worktree remove .worktrees/<name>
git worktree add .worktrees/<name> -b <branch>
```

### node_modules issues

Each worktree needs its own `node_modules`:
```bash
# Never symlink node_modules between worktrees
cd .worktrees/<name>
rm -rf node_modules
yarn install
```

### .nuxt not generating types

```bash
cd .worktrees/<name>
rm -rf .nuxt
npx nuxt prepare
```

## Quick Reference

| Task | Command |
|------|---------|
| Create (new branch) | `git worktree add .worktrees/<name> -b <branch>` |
| Create (existing branch) | `git worktree add .worktrees/<name> <branch>` |
| List | `git worktree list` |
| Remove | `git worktree remove .worktrees/<name>` |
| Prune stale | `git worktree prune` |
| Move | `git worktree move <old> <new>` |
| Check if in worktree | `git rev-parse --show-toplevel` |

## Red Flags

**Never:**
- Create worktrees without `.worktrees/` in `.gitignore`
- Share `node_modules` between worktrees
- Check out same branch in multiple worktrees
- Leave stale worktrees (prune regularly)

**Always:**
- Use `.worktrees/` directory (or ask user preference)
- Run project setup after creating worktree
- Verify baseline tests pass
- Clean up worktrees after merging PRs
