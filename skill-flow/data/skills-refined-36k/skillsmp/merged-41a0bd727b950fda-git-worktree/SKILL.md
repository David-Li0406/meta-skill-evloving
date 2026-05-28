---
name: git-worktree
description: Use this skill to manage Git worktrees for parallel development on multiple branches without switching or cloning the repository.
---

# Git Worktree Skill

Manage isolated development environments using Git worktrees.

## When to Use

- Working on multiple features simultaneously
- Reviewing a PR while working on something else
- Testing changes without affecting your main workspace
- Running long builds while continuing development
- Avoiding stashing or committing WIP changes

## Quick Commands

### Create Worktree for a New Branch
```bash
git worktree add <path> -b <branch>
```

### Create Worktree for an Existing Branch
```bash
git worktree add <path> <branch>
```

### List All Worktrees
```bash
git worktree list
```

### Remove Worktree
```bash
git worktree remove <path>
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
# ... review commands ...
# Cleanup after review
git worktree remove ../pr-123-review
git branch -D pr-123
```

### Pattern 3: Hotfix While Working
```bash
# You're working on a feature, need to fix a prod bug
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

Recommended layout:
```
/Users/dev/
├── my-project/              # Main repository
│   ├── .git/               # Git database
│   ├── src/
│   └── ...
└── my-project-worktrees/    # All worktrees here
    ├── feature-auth/       # feature/authentication branch
    ├── feature-profile/    # feature/user-profile branch
    ├── hotfix-urgent/      # hotfix/urgent-fix branch
    └── review-pr-123/      # Reviewing PR #123
```

## Best Practices

1. **Naming**: Use descriptive directory names matching the branch.
2. **Location**: Keep worktrees as siblings to the main repo.
3. **Cleanup**: Remove worktrees when done to avoid clutter.
4. **Prune**: Run `git worktree prune` periodically.

## Common Issues

### "fatal: is already checked out"
The branch is already checked out in another worktree. Use a different branch or remove the existing worktree.

### Stale Worktrees After Deletion
Run `git worktree prune` to clean up references to deleted worktree directories.

### Submodules Not Initialized
Run `git submodule update --init` in the new worktree.

## Troubleshooting

### Issue: Disk Space Concerns
- Use symlinks for shared dependencies.
- Remove worktrees when PRs are merged.
- Run `git worktree prune` regularly.

### Issue: IDE Confusion with Multiple Worktrees
- Open each worktree as a separate workspace.
- Use IDE's multi-window/split-workspace features.

## Agent Instructions

When delegating worktree setup to a version-control agent:

```
Task: Create worktrees for stacked PR development

Requirements:
- Create 3 worktrees in /project-worktrees/
- Worktree 1: pr-001 with branch feature/001-base-auth
- Worktree 2: pr-002 with branch feature/002-user-profile
- Worktree 3: pr-003 with branch feature/003-admin-panel

Commands:
git worktree add ../project-worktrees/pr-001 -b feature/001-base-auth
git worktree add ../project-worktrees/pr-002 -b feature/002-user-profile
git worktree add ../project-worktrees/pr-003 -b feature/003-admin-panel

Verification: git worktree list should show all 3 worktrees
```

## Benefits

✅ **No Branch Switching:** Work on multiple branches without `git checkout`  
✅ **Parallel Servers:** Run multiple dev environments simultaneously  
✅ **Preserve State:** Build artifacts and dependencies stay per-branch  
✅ **Safer Reviews:** Test PRs without affecting the main working directory  
✅ **Faster Context Switch:** Jump between worktrees instead of rebasing  

## Related Skills

- `stacked-prs` - Combine worktrees with stacked PR workflow
- `git-workflow` - General git branching patterns
- `code-review` - Review code in isolated worktrees