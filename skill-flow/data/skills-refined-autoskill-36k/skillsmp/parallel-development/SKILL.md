---
name: parallel-development
description: Run multiple Claude Code sessions simultaneously using git worktrees. Use when discussing parallel work, worktrees, concurrent development, or multiple sessions.
---

# Parallel Development

Run 5+ Claude Code sessions simultaneously to maximize productivity.

## Why Parallel Sessions?

**Don't wait for Claude to finish one thing before starting another.**

Benefits:
- Work on multiple features simultaneously
- Don't block on long-running tasks
- Experiment without affecting main work

## Git Worktrees

Worktrees allow multiple working directories from a single repository.

### Creating a Worktree

```bash
# Create worktree with new branch
git worktree add -b feature/auth ../project-auth main

# Create worktree with existing branch
git worktree add ../project-fix-123 fix/issue-123
```

### Listing Worktrees

```bash
git worktree list
```

### Removing Worktrees

```bash
git worktree remove ../project-auth
git worktree prune
```

## Parallel Session Workflow

### 1. Identify Independent Tasks
Choose tasks that don't overlap in files.

### 2. Create Worktrees
```bash
git worktree add -b feature/auth ../project-auth main
git worktree add -b feature/ui ../project-ui main
```

### 3. Start Claude Sessions
Open separate terminals for each worktree:
```bash
cd ../project-auth && claude
cd ../project-ui && claude
```

### 4. Work Independently
Each session works on its task.

### 5. Merge Results
```bash
git checkout main
git merge feature/auth
git merge feature/ui
```

### 6. Clean Up
```bash
git worktree remove ../project-auth
git worktree remove ../project-ui
```

## Best Practices

1. **Independent tasks**: Choose work with different file footprints
2. **Focused sessions**: One task per worktree
3. **Regular syncs**: Pull main into feature branches
4. **Clean up**: Remove worktrees when done

## Example Layout

```
~/projects/
├── my-app/                 # Main - coordination
├── my-app-auth/            # Session 2 - auth feature
├── my-app-dashboard/       # Session 3 - dashboard
└── my-app-perf/            # Session 4 - performance
```
