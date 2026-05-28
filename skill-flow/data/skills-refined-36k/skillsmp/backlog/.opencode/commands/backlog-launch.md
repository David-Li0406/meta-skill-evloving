---
description: Launch agent worktree for a specific task
---

# Launch Agent Worktree

Create a git worktree and PROMPT.md for a task, ready for agent execution.

**Arguments:** $ARGUMENTS

## Instructions

### Phase 1: Parse Arguments

1. **Extract task ID** from arguments (e.g., "CRANE-003").
2. **Extract optional flags:**
   - `--max-iterations N` - Safety limit for agent iterations (default: 0 = unlimited)
   - `--force` - Launch even if dependencies are incomplete (with warning)

### Phase 2: Validate Task

1. Find task directory: `ls -d tasks/${TASK_ID}-* 2>/dev/null`
2. If not found: Show available tasks and abort
3. Read task files (TASK.md, PROGRESS.md)
4. Check task status (warn if Complete or In Progress)

### Phase 3: Dependency Check

Build dependency graph and verify all dependencies are Complete.

**If blocked (without --force):**
- Show incomplete dependencies
- Show recommended completion order
- Suggest using `--force` to override

### Phase 4: Prepare Task Files

1. Initialize PROGRESS.md if needed
2. Commit task files to ensure worktree has them

### Phase 5: Create Worktree

1. Determine worktree location: `{REPO_ROOT}-wt/feature/{kebab-name}`
2. Create worktree and branch
3. Initialize all submodules recursively
4. Verify submodules are functional

### Phase 6: Setup Agent Environment

1. Create PROMPT.md in worktree root with:
   - Task ID and title
   - Mode: Implementation
   - Required reading list
   - Instructions for the agent
   - Completion promise format

2. Update tasks/INDEX.md status to "In Progress"

### Phase 7: Output Launch Instructions

```
═══════════════════════════════════════════════════════════════════
 AGENT READY: {PREFIX}-{NNN} - {Title}
═══════════════════════════════════════════════════════════════════

## Step 1: Open a new terminal and run:

cd {ABSOLUTE_WORKTREE_PATH}

## Step 2: Start your AI coding assistant

## Step 3: Run the bootstrap command:

/prompt

═══════════════════════════════════════════════════════════════════
```

## Arguments Reference

| Argument | Description |
|----------|-------------|
| `<task-id>` | Task ID to launch (e.g., CRANE-003) |
| `--max-iterations N` | Optional safety limit (default: 0 = unlimited) |
| `--force` | Launch even if dependencies are incomplete |

## Error Handling

- **Task doesn't exist:** Show available task IDs
- **Task already complete:** Warn and ask for confirmation
- **Worktree already exists:** Show path and ask to continue or abort
- **Dependencies incomplete:** Show blockers and recommend order

## Related Commands

- `/backlog` - View all tasks
- `/backlog-work <ID>` - Start task in current session (no worktree)
- `/backlog-complete <ID>` - Complete and cleanup worktree
