---
name: git-worktree
description: Manage git worktrees - create or switch to worktree by branch name. Use when user mentions worktree, gw, gwa, gwc, or wants to switch/create branch workspace.
---

# Git Worktree Manager

Create or switch to git worktree by branch name.

## Usage

User provides branch name only. The skill:
1. Checks if worktree for that branch exists
2. If exists: navigate to it
3. If not: create from `develop` branch, then navigate

## Commands

### Check existing worktrees
```bash
git worktree list
```

### Check if specific branch worktree exists
```bash
git worktree list | grep "{branch-name}"
```

### Create worktree (from develop)
Uses zshrc function `gwa`:
```bash
gwa {branch-name} develop
```
- Converts `/` to `-` in folder name automatically
- Creates at `../{folder-name}` relative to current repo

### Switch to worktree
Uses zshrc function `gwc`:
```bash
gwc {branch-name}
```
- Uses fzf for selection
- Pass branch name as query filter

### Direct navigation
```bash
cd ../{folder-name}
```
Where `{folder-name}` = branch name with `/` replaced by `-`

## Workflow

```bash
# 1. Check if worktree exists
git worktree list | grep "{branch}"

# 2a. If exists - navigate
cd ../{folder-name}

# 2b. If not exists - create then navigate
gwa {branch-name} develop && cd ../{folder-name}
```

## Examples

| Input | Folder | Action |
|-------|--------|--------|
| `fc/feature1` | `fc-feature1` | create/switch |
| `rieul/fix-bug` | `rieul-fix-bug` | create/switch |
| `develop` | `develop` | switch only |

## Notes

- Always branch from `develop`
- Worktree path: `{repo-root}/../{folder-name}`
- Requires zshrc functions: `gwa`, `gwc`
