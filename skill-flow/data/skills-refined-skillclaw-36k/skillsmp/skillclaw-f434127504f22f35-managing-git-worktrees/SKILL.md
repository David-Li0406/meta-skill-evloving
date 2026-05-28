---
name: managing-git-worktrees
description: Use this skill when you need to create, manage, and clean up Git worktrees for parallel development, allowing you to work on multiple branches simultaneously without disrupting your current work.
---

# Managing Git Worktrees

## Overview

Git worktrees allow you to have multiple working directories from a single repository, enabling parallel development without switching branches or stashing changes. Each worktree has its own working directory and can be on a different branch, but all worktrees share the same Git history and objects.

## When to Use This Skill

- When working on multiple features or bug fixes simultaneously.
- When reviewing pull requests without disrupting current work.
- When setting up isolated environments for different tasks.
- When needing to clean up completed worktrees.

## Core Commands

### Create Worktree

1. **Ensure Worktrees Directory Exists**
   ```bash
   mkdir -p worktrees
   ```

2. **Verify Worktree Doesn't Already Exist**
   ```bash
   git worktree list | grep "worktrees/issue-$ISSUE_NUMBER"
   ```

3. **Create Worktree from Main**
   ```bash
   git fetch origin main
   git worktree add -b feature/issue-$ISSUE_NUMBER worktrees/issue-$ISSUE_NUMBER origin/main
   ```

### List Worktrees

To list all active worktrees:
```bash
git worktree list
```

### Cleanup Worktrees

To remove worktrees that are no longer needed:
```bash
git worktree prune
```

### Copy Environment Files

To copy environment files from the main repo to a worktree:
```bash
cp .env* worktrees/issue-$ISSUE_NUMBER/
```

## Important Considerations

- Each worktree duplicates the working directory, requiring additional disk space.
- Each worktree may need independent dependency installations.
- Ensure that branch protections are respected across worktrees to prevent accidental deletions.

## Conclusion

This skill provides a structured approach to managing Git worktrees, facilitating efficient parallel development workflows.