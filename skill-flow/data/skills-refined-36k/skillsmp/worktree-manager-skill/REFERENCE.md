# Worktree Quick Reference

Technical details, command syntax, and configuration reference.

## Command Syntax

### Create Worktree
```bash
/git-simple:create_worktree_prompt <branch-name>
```

**Parameters:**
- `branch-name` (required) - Name of the git branch

**Example:**
```bash
/git-simple:create_worktree_prompt feature-auth
/git-simple:create_worktree_prompt hotfix-bug 
```

---

### List Worktrees
```bash
/git-simple:list_worktrees_prompt
```

**Parameters:** None

**Output includes:**
- Worktree paths
- Quick commands

---

### Remove Worktree
```bash
/git-simple:remove_worktree_prompt <branch-name>
```

**Parameters:**
- `branch-name` (required) - Name of the worktree to remove

**Example:**
```bash
/git-simple:remove_worktree_prompt feature-auth
```

---

## Directory Structure

### Main Repository
```
project/
├── .claude/
│   ├── settings.json
│   └── commands/
├── .env

```

### Worktree Structure
```
project/
└── trees/
    └── <branch-name>/
        ├── .claude/
        │   └── settings.json (isolated config)
        ├── .env (unique ports)
```

---

## Git Worktree Fundamentals

### What is a Git Worktree?
A git worktree is an additional working directory attached to the same repository. Multiple worktrees can exist simultaneously, each checked out to different branches.

### Benefits
- Work on multiple branches simultaneously
- No need to stash/switch branches
- Isolated development environments
- Test multiple features in parallel

### Limitations
- Each branch can only be checked out in one worktree
- Worktrees share git history/objects
- Disk space required for each copy

---

## Isolation Features

Each worktree has:

| Feature | Isolation Level | Notes |
|---------|----------------|-------|
| **File System** | Complete | Separate working directory |
| **Configuration** | Complete | Own .env and settings.json |
| **Dependencies** | Complete | Own node_modules |
| **Git History** | Shared | Same repository |
| **Git Config** | Shared | Same git settings |

---

## Related Capabilities

### Main Repository
- Default environment
- No special setup needed
- Can run alongside worktrees

### Parallel Development
- Run main + multiple worktrees simultaneously
- Each fully isolated
- No conflicts between environments
- Test features against different bases

### Branch Preservation
- Removing a worktree doesn't delete the branch
- Branch still exists in git
- Can recreate worktree anytime
- Safe to cleanup unused worktrees

---

## Best Practices

### When to Create Worktrees
✓ Testing multiple features simultaneously
✓ Reviewing PRs while working on features
✓ Hot-fixing production while developing
✓ Running integration tests in isolation

### When NOT to Create Worktrees
✗ Simple branch switching (use git checkout)
✗ Temporary file viewing (use git show)
✗ Quick edits (stash and switch)

### Cleanup Recommendations
- Remove worktrees when feature is merged
- Don't let unused worktrees accumulate
- Regular audit with `/git-simple:list_worktrees_prompt`
- Free up ports for active development

### Naming Conventions
- Use descriptive branch names
- Avoid special characters
- Keep names concise
- Match branch naming scheme

---

## Technical Implementation

### Creation Process
1. Validate branch exists
2. Calculate/verify port offset
3. Create git worktree
4. Copy configuration templates
5. Update ports in configs
6. Install dependencies
7. Start services
8. Verify startup
9. Report access info

### Removal Process
1. Find processes on worktree ports
2. Kill server process
3. Kill client process
4. Remove git worktree
5. Clean up directories
6. Validate removal
7. Report results

### Status Checking
1. List git worktrees
2. Read configuration for each
3. Check if processes running
4. Verify port accessibility
5. Generate comprehensive report
