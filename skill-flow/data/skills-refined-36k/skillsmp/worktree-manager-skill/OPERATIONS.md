# Worktree Operations Guide

Detailed step-by-step instructions for each worktree operation.

## CREATE Operations

**When user wants to create a worktree:**

### Step 1: Extract information
- **Branch name** (required) - The git branch to create the worktree from

### Step 2: Invoke command
```
/git-simple:create_worktree_prompt <branch-name>
```

### Step 3: What happens automatically
The command handles:
- Creates git worktree in `trees/<branch-name>`
- Configures unique ports (auto-calculated if offset not provided)
- Sets up all environment files (.env, .claude/settings.json)
- Installs dependencies

### Step 4: Share results with user
Include:
- Location of worktree directory

---

## LIST Operations

**When user wants to see worktrees:**

### Step 1: Invoke command
```
/git-simple:list_worktrees_prompt
```

### Step 2: What the command shows
The output includes:
- All existing worktrees with their paths
- Quick action commands for management

### Step 3: Share the overview with user
Highlight:
- Which worktrees are currently running
- How to access each one
- Any issues or conflicts

---

## REMOVE Operations

**When user wants to remove a worktree:**

### Step 1: Extract information
- **Branch name** (required) - The name of the worktree to remove

### Step 2: Invoke command
```
/git-simple:remove_worktree_prompt <branch-name>
```

### Step 3: What happens automatically
The command handles:
- Removes git worktree
- Cleans up directories
- Validates complete removal
- Reports success or any issues

### Step 4: Confirm removal with user
Share:
- Confirmation that worktree was removed
- Any cleanup actions performed
