---
description: Display task status summary from tasks/INDEX.md
---

# Backlog Status

Display a summary table of all tasks from tasks/INDEX.md with dependency-aware status computation.

**Arguments:** $ARGUMENTS

## Instructions

### Step 1: Load Configuration

```bash
cat design.yaml 2>/dev/null
```

Extract `repo_prefix` and `repo_name`.

### Step 2: Check for Tasks

Find tasks/INDEX.md in current working directory.

**If not found or empty:** Report that no backlog is defined:
```
No backlog defined.

To create a backlog:
1. Run /design-init to create the tasks/ directory structure
2. Run /design to create your first task
```

### Step 3: Build Dependency Graph

Parse tasks/INDEX.md and build dependency relationships:
- Parse each task row for ID, title, status, dependencies
- Build forward and reverse dependency maps

### Step 4: Check for Circular Dependencies

Detect any circular dependencies in the task graph and report them.

### Step 5: Compute Effective Status

For each task, compute the effective status based on dependencies:

**Status computation rules:**
- If stored status is "In Progress", "In Review", or "Complete" → keep it
- If stored status is "Ready" or "Blocked":
  - Check all dependencies
  - If any dependency is not "Complete" → "Blocked"
  - If all dependencies are "Complete" → "Ready"

### Step 6: Display Status Table

```
═══════════════════════════════════════════════════════════════════
 BACKLOG STATUS: {REPO_NAME}
═══════════════════════════════════════════════════════════════════

| ID | Title | Status | Computed | Dependencies | Blockers |
|----|-------|--------|----------|--------------|----------|
| {PREFIX}-001 | ... | Complete | Complete | - | - |
| {PREFIX}-002 | ... | Ready | Ready | - | - |

## Summary

- Complete: N
- In Progress: N
- Ready: N (computed, all deps met)
- Blocked: N (computed, waiting on deps)

## Ready for Agent

Tasks that can be started (all dependencies complete):
- {PREFIX}-001: {Title}

═══════════════════════════════════════════════════════════════════
```

### Step 7: Optional Views

**If `--graph` argument:** Show ASCII dependency visualization

**If `--critical-path` argument:** Show longest dependency chain

**If `--order` argument:** Show recommended task execution order (topological sort)

## Arguments Reference

| Argument | Description |
|----------|-------------|
| `--graph` | Show ASCII dependency graph visualization |
| `--critical-path` | Show longest dependency chain |
| `--order` | Show recommended task execution order |

## Related Commands

- `/backlog-read <ID>` - Read full task details
- `/backlog-launch <ID>` - Launch agent worktree for a task
- `/backlog-review <ID>` - Transition task to review mode
- `/backlog-complete <ID>` - Complete and merge a task
- `/backlog-prune` - Archive completed tasks
- `/backlog-list` - List active worktrees
- `/design` - Create a new task

## Error Handling

- **No tasks/ directory:** "Run /design-init to set up task management"
- **No design.yaml:** "Run /design-init to configure the repository"
- **Empty INDEX.md:** "No tasks defined. Use /design to create your first task"
- **Circular dependencies:** Show cycle path and affected tasks
