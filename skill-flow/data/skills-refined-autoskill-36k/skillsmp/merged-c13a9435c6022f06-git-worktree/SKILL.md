---
name: git-worktree
description: Use this skill to manage Git worktrees for parallel development on multiple branches without switching or cloning the repository.
---

# Git Worktree Skill

Manage isolated development environments using Git worktrees, allowing you to work on multiple branches simultaneously.

## When to Use

- Working on multiple features or pull requests at the same time
- Reviewing a PR while continuing development
- Testing changes in an isolated environment
- Running long builds without affecting your main workspace

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

### Feature Development
```bash
# Create isolated workspace for new feature
git worktree add <path-to-worktree> -b <feature-branch>

# Work in the new worktree
cd <path-to-worktree>

# When done, merge and cleanup
git checkout main
git merge <feature-branch>
git worktree remove <path-to-worktree>
git branch -d <feature-branch>
```

### PR Review
```bash
# Create worktree for PR review without switching branches
git fetch origin pull/<PR-number>/head:<branch-name>
git worktree add <path-to-worktree> <branch-name>

# Review in separate directory
cd <path-to-worktree>
# Run tests or review code
# Cleanup after review
git worktree remove <path-to-worktree>
git branch -D <branch-name>
```

### Hotfix While Working
```bash
# You're working on a feature, need to fix a production bug
git worktree add <path-to-hotfix> -b <hotfix-branch> origin/main

# Fix bug in hotfix worktree
cd <path-to-hotfix>
# ... make fixes ...
git commit -am "fix: urgent bug"
git push origin <hotfix-branch>

# Return to feature work
cd <path-to-feature>
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

1. **Naming Convention**: Use descriptive directory names matching the branch.
2. **Location Strategy**: Keep worktrees outside the main repository to avoid clutter.
3. **Cleanup Discipline**: Remove worktrees when done to maintain a clean workspace.
4. **One Branch Per Worktree**: Each worktree should be permanently on one branch.

## Common Issues

### "fatal: is already checked out"
The branch is already checked out in another worktree. Use a different branch or remove the existing worktree.

### Stale Worktrees After Deletion
Run `git worktree prune` to clean up references to deleted worktree directories.

### Disk Space Concerns
Consider using symlinks for shared dependencies to save space.

## Agent Instructions

When delegating worktree setup to a version-control agent, specify the requirements and commands clearly to ensure proper setup.

## Benefits

- **No Branch Switching**: Work on multiple branches without `git checkout`.
- **Parallel Servers**: Run multiple development environments simultaneously.
- **Safer Reviews**: Test PRs without affecting the main working directory.
- **Faster Context Switch**: Jump between worktrees instead of rebasing.

## Related Skills

- `stacked-prs` - Combine worktrees with stacked PR workflow.
- `git-workflow` - General git branching patterns.
- `code-review` - Review code in isolated worktrees.