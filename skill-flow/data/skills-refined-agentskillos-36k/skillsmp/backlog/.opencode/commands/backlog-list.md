---
description: List all unarchived tasks with status, dependencies, and worktrees
---

# List Tasks

Show all unarchived tasks with their status, dependencies, and associated worktrees.

**Arguments:** $ARGUMENTS

## Instructions

### Step 1: Load Configuration

```bash
cat design.yaml 2>/dev/null
```

Extract `repo_prefix` and `repo_name` for display.

### Step 2: Check for Tasks

Find tasks/INDEX.md in current working directory.

**If not found or empty:**
```
No tasks defined.

To create tasks:
1. Run /design-init to create the tasks/ directory structure
2. Run /design to create your first task
```

### Step 3: Build Dependency Graph

Parse tasks/INDEX.md and build dependency relationships.

### Step 4: Get Worktree Information

```bash
git worktree list
```

For each worktree:
- Check if PROMPT.md exists
- Extract task ID and mode from PROMPT.md
- Build map of task_id → {path, mode, branch}

### Step 5: Display Task List

**If `--worktrees-only` argument:** Skip to worktrees-only view.

**Otherwise, show all tasks:**

```
═══════════════════════════════════════════════════════════════════
 TASK LIST: {REPO_NAME}
═══════════════════════════════════════════════════════════════════

| ID | Title | Status | Dependencies | Worktree |
|----|-------|--------|--------------|----------|
| {PREFIX}-001 | Core infrastructure | ✅ Complete | - | - |
| {PREFIX}-002 | Registry system | 🚀 In Progress | - | feature/registry |

## Summary

Total: N tasks

## Active Worktrees

| Task | Branch | Path | Mode |
|------|--------|------|------|
| {PREFIX}-002 | feature/registry | /path/to/wt | Implementation |

## Next Actions

Ready to start:
- /backlog-launch {PREFIX}-004

═══════════════════════════════════════════════════════════════════
```

## Status Icons

| Status | Icon | Description |
|--------|------|-------------|
| Complete | ✅ | Task finished and merged |
| In Progress | 🚀 | Agent actively working |
| In Review | 📋 | Work complete, code review |
| Ready | 🆕 | All dependencies met, can start |
| Blocked | ❌ | Waiting on dependencies |

## Arguments Reference

| Argument | Description |
|----------|-------------|
| `--worktrees-only` | Show only active worktrees |

## Related Commands

- `/backlog` - Detailed status with dependency analysis
- `/backlog-read <ID>` - Read full task details
- `/backlog-launch <ID>` - Launch a new agent worktree
