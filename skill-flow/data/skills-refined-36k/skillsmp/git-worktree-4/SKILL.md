---
name: git-worktree
description: Git worktree management for parallel development workflows. Use when the user wants to work on multiple branches simultaneously without stashing, create isolated environments for features/bugfixes, or manage worktrees (create, list, remove, prune). Triggers on requests like "create a worktree", "work on branch X in parallel", "set up a new feature branch environment", or worktree-related operations.
---

# Git Worktree

Manage git worktrees to work on multiple branches simultaneously in separate directories.

## Quick Reference

| Task | Command |
|------|---------|
| Create worktree | `python scripts/worktree.py create <branch>` |
| Create with deps | `python scripts/worktree.py create <branch> -i` |
| Create + open editor | `python scripts/worktree.py create <branch> -e code` |
| List worktrees | `python scripts/worktree.py list` |
| Remove worktree | `python scripts/worktree.py remove <path>` |
| Prune stale refs | `python scripts/worktree.py prune` |

## Creating Worktrees

### Basic Creation

Create a worktree for an existing or new branch:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py create feat/my-feature
```

This creates:
- A sibling directory: `../repo-name-feat/my-feature`
- A new branch from `main`/`master` if the branch doesn't exist

### With Options

```bash
# From specific base branch
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py create feat/new -b develop

# Custom path
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py create feat/new -p ~/projects/feature-work

# Install dependencies after creation
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py create feat/new -i

# Open in VS Code
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py create feat/new -e code

# All options combined
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py create feat/new -b develop -i -e cursor
```

### Supported Editors

`-e` flag accepts: `code`, `cursor`, `idea`, `webstorm`, `pycharm`, `zed`, `sublime`, `vim`, `nvim`

### Supported Package Managers

When using `-i`, the script auto-detects:
- **Node.js**: npm, yarn, pnpm, bun
- **Python**: uv, poetry, pipenv, pip
- **Ruby**: bundler
- **Go**: go mod
- **Rust**: cargo

## Listing Worktrees

```bash
# Table format (default)
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py list

# JSON format
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py list -f json
```

## Removing Worktrees

```bash
# Remove worktree
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py remove ../repo-name-feat/my-feature

# Force remove (even if dirty)
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py remove ../repo-name-feat/my-feature -f
```

## Pruning Stale References

Clean up worktree references for directories that no longer exist:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py prune
```

## Workflow Examples

### Feature Development

1. Create worktree for new feature:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py create feat/user-auth -i -e code
   ```

2. Work on the feature in the new directory
3. When done, remove the worktree:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py remove ../repo-feat/user-auth
   ```

### Hotfix While Working on Feature

When you need to fix a bug but don't want to stash your current work:

```bash
# Create worktree for the fix
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py create fix/critical-bug -b main -i

# Fix the bug, commit, push, merge PR
# Then remove the worktree
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py remove ../repo-fix/critical-bug
```

### Code Review

Review a PR without disrupting your current work:

```bash
# Create worktree from the PR branch
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py create pr-review -b origin/feat/someone-elses-work

# Review, then clean up
python ${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py remove ../repo-pr-review
```
