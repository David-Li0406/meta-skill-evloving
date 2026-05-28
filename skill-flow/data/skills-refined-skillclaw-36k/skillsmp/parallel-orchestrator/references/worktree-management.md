# Git Worktree Management Reference

Detailed guide for managing git worktrees in parallel development.

## Worktree Basics

### What is a Worktree?
A git worktree is an additional working directory linked to your repository. Each worktree:
- Has its own working directory
- Can have a different branch checked out
- Shares the same git history
- Can run independent operations

### Why Use Worktrees for Parallel Development?
1. **Isolation** - Changes in one worktree don't affect others
2. **Parallel Testing** - Run tests in multiple worktrees simultaneously
3. **No Stash Needed** - Work on multiple features without stashing
4. **Clean Merges** - Each feature on its own branch

## Worktree Commands

### Create a Worktree
```bash
# Create worktree with new branch
git worktree add /path/to/worktree -b branch-name

# Create worktree with existing branch
git worktree add /path/to/worktree existing-branch
```

### List Worktrees
```bash
git worktree list
```

### Remove a Worktree
```bash
# Remove worktree (keeps branch)
git worktree remove /path/to/worktree

# Force remove (if uncommitted changes)
git worktree remove --force /path/to/worktree
```

### Prune Stale Worktrees
```bash
git worktree prune
```

## Autonomous-Dev Worktree Strategy

### Directory Structure
```
/tmp/auto-worktrees/
├── task-1/           # Worktree for task 1
│   ├── .git          # Link to main repo
│   ├── src/
│   └── ...
├── task-2/           # Worktree for task 2
└── task-3/           # Worktree for task 3
```

### Branch Naming Convention
```
auto/{task-id}

Examples:
- auto/task-1
- auto/user-model
- auto/api-endpoints
```

### Setup Script Usage
```bash
# Create worktree for a task
${CLAUDE_PLUGIN_ROOT}/scripts/setup-worktree.sh task-id [base-branch]

# Output format (pipe-separated)
/tmp/auto-worktrees/task-id|auto/task-id
```

### Cleanup Process
```bash
# After successful merge
git worktree remove /tmp/auto-worktrees/task-id
git branch -d auto/task-id

# After failed task (preserve for debugging)
# Just remove worktree, keep branch
git worktree remove /tmp/auto-worktrees/task-id
```

## Common Issues and Solutions

### Issue: "fatal: 'branch' is already checked out"
**Cause:** Branch is checked out in another worktree
**Solution:** Use a different branch name or remove the other worktree

### Issue: Worktree directory already exists
**Cause:** Previous worktree wasn't cleaned up
**Solution:**
```bash
rm -rf /tmp/auto-worktrees/task-id
git worktree prune
```

### Issue: Changes not visible after merge
**Cause:** Main worktree needs to be updated
**Solution:**
```bash
git checkout main  # or your base branch
git pull           # if remote tracking
```

### Issue: Merge conflicts between worktrees
**Cause:** Tasks modified same files
**Solution:** Use conflict-resolver skill, merge in dependency order

## Best Practices

1. **Always use /tmp for worktrees** - Easy cleanup, no clutter
2. **Name branches descriptively** - `auto/user-model` not `auto/task-1`
3. **Clean up after completion** - Remove worktrees and merged branches
4. **Copy project profile** - Each worktree needs `.claude/project-profile.yaml`
5. **Run verification in worktree** - Don't rely on main worktree passing
