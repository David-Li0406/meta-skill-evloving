---
name: git-worktree
description: Manage Git worktrees for isolated parallel development without branch switching
---

# Git Worktree Skill

Manage isolated development environments using Git worktrees.

## When to Use

- Working on multiple features simultaneously
- Need to review a PR while working on something else
- Testing changes without affecting your main workspace
- Running long builds while continuing development

## Quick Commands

### Create worktree for a new branch
```bash
git worktree add ../feature-xyz -b feature/xyz
```

### Create worktree for existing branch
```bash
git worktree add ../pr-review origin/pr-branch
```

### List all worktrees
```bash
git worktree list
```

### Remove worktree
```bash
git worktree remove ../feature-xyz
```

### Clean up stale worktrees
```bash
git worktree prune
```

## Workflow Patterns

### Pattern 1: Feature Development
```bash
# Create isolated workspace for new feature
git worktree add ../my-feature -b feature/new-thing

# Work in the new worktree
cd ../my-feature

# When done, merge and cleanup
git checkout main
git merge feature/new-thing
git worktree remove ../my-feature
git branch -d feature/new-thing
```

### Pattern 2: PR Review
```bash
# Create worktree for PR review without switching branches
git fetch origin pull/123/head:pr-123
git worktree add ../pr-123-review pr-123

# Review in separate directory
cd ../pr-123-review
go test ./...

# Cleanup after review
git worktree remove ../pr-123-review
git branch -D pr-123
```

### Pattern 3: Hotfix While Working
```bash
# You're working on feature, need to fix prod bug
git worktree add ../hotfix -b hotfix/urgent-fix origin/main

# Fix bug in hotfix worktree
cd ../hotfix
# ... make fixes ...
git commit -am "fix: urgent bug"
git push origin hotfix/urgent-fix

# Return to feature work
cd ../my-feature
```

## Directory Convention

```
~/code/
├── celestia-app/           # Main worktree (main branch)
├── celestia-app-feature/   # Feature worktree
├── celestia-app-hotfix/    # Hotfix worktree
└── celestia-app-review/    # PR review worktree
```

## Best Practices

1. **Naming**: Use descriptive directory names matching the branch
2. **Location**: Keep worktrees as siblings to main repo
3. **Cleanup**: Remove worktrees when done to avoid clutter
4. **Prune**: Run `git worktree prune` periodically

## Common Issues

### "fatal: is already checked out"
The branch is already checked out in another worktree. Use a different branch or remove the existing worktree.

### Stale worktrees after deletion
Run `git worktree prune` to clean up references to deleted worktree directories.

### Submodules not initialized
Run `git submodule update --init` in the new worktree.
