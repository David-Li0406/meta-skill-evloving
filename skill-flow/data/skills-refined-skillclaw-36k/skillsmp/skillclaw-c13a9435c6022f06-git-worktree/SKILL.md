---
name: git-worktree
description: Use this skill when you need to manage multiple Git worktrees for parallel development on different branches without switching contexts.
---

# Git Worktree Skill

Manage isolated development environments using Git worktrees to work on multiple branches simultaneously.

## When to Use

- Working on multiple features or bug fixes at the same time
- Reviewing pull requests in isolation
- Testing changes without affecting your main workspace
- Running long builds while continuing development

## Quick Commands

### Create Worktree for a New Branch
```bash
git worktree add ../feature-xyz -b feature/xyz
```

### Create Worktree for an Existing Branch
```bash
git worktree add ../pr-review origin/pr-branch
```

### List All Worktrees
```bash
git worktree list
```

### Remove Worktree
```bash
git worktree remove ../feature-xyz
```

### Clean Up Stale Worktrees
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

## Directory Structure

Recommended layout for worktrees:
```
~/code/
├── main-repo/                # Main repository
├── worktrees/                # Worktree container (gitignored)
│   ├── feature-auth/         # feature/authentication branch
│   ├── feature-profile/      # feature/user-profile branch
│   └── hotfix/               # hotfix branch
```

## Best Practices

1. **Naming**: Use descriptive directory names matching the branch.
2. **Location**: Keep worktrees as siblings to the main repo.
3. **Cleanup**: Remove worktrees when done to avoid clutter.
4. **Prune**: Run `git worktree prune` periodically to clean up stale references.

## Common Issues

### "fatal: is already checked out"
The branch is already checked out in another worktree. Use a different branch or remove the existing worktree.

## Key Concepts

- **Worktree**: An additional working tree linked to the main repository.
- **Locking**: Prevent accidental worktree removal.
- **Pruning**: Clean up stale worktree references.