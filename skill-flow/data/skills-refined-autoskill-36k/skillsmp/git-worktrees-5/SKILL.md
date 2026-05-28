---
name: git-worktrees
description: Manage git worktrees for parallel development. Use when user mentions worktrees, parallel branches, or working on multiple branches simultaneously.
---

# Git Worktrees

Work on multiple branches simultaneously without stashing or switching.

## Worktree Location

All worktrees live in `.worktrees/` at repo root.

```
project/
├── .worktrees/
│   ├── feat-auth/
│   └── fix-login/
└── (main working tree)
```

## Naming Convention

Worktree folder matches branch name pattern:

| Branch | Worktree Folder |
|--------|-----------------|
| `yurifrl/feat/auth` | `.worktrees/feat-auth` |
| `yurifrl/fix/login-bug` | `.worktrees/fix-login-bug` |
| `hotfix/urgent` | `.worktrees/hotfix-urgent` |

**Pattern**: Take the last two segments, join with hyphen.

## Commands

### Create Worktree

```bash
# New branch
git worktree add .worktrees/<folder> -b <branch-name>

# Existing branch
git worktree add .worktrees/<folder> <existing-branch>
```

### List Worktrees

```bash
git worktree list
```

### Remove Worktree

```bash
git worktree remove .worktrees/<name>
```

### Prune Stale

```bash
git worktree prune
```

## Workflow

- Create worktree for feature/fix work
- Each worktree is independent (own node_modules, build cache, etc.)
- Remove worktree when branch is merged
- Run `git worktree prune` to clean up stale references

## Tips

- Worktrees share the same `.git` - commits are visible everywhere
- Don't forget to install dependencies in new worktree
