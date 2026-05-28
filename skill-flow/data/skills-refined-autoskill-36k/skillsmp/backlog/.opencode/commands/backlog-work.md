---
description: Start working on a task in the current session (no worktree)
---

# Start In-Session Task

Start working on a task directly in the current session without creating a worktree. Ideal for quick, simple tasks.

**Arguments:** $ARGUMENTS

## Instructions

### Step 1: Parse Arguments

1. Extract task ID from arguments
2. If no task ID provided, show usage or select from Ready tasks

### Step 2: Validate Task

1. Find task directory
2. Check task status (must be Ready, not Complete/In Progress/In Review/Blocked)
3. Check for conflicts (existing worktree or PROMPT.md)

### Step 3: Check for Conflicts

- If task has active worktree: abort with worktree location
- If PROMPT.md exists for different task: abort with current task info

### Step 4: Create PROMPT.md

Generate PROMPT.md in current directory with:
- Task ID and title
- Mode: Implementation (In-Session)
- Required reading list
- Completion instructions

### Step 5: Update INDEX.md

Update task status to "In Progress"

### Step 6: Initialize PROGRESS.md

Update PROGRESS.md to mark task started with session log entry.

### Step 7: Output Instructions

```
═══════════════════════════════════════════════════════════════════
 TASK STARTED: {TASK_ID} - {TASK_TITLE}
═══════════════════════════════════════════════════════════════════

Working in-session (no worktree).

## Required Reading

1. tasks/{TASK_NAME}/TASK.md - Requirements
2. tasks/{TASK_NAME}/PROGRESS.md - Progress log

## Workflow

1. Read the task requirements
2. Implement the changes
3. Update PROGRESS.md as you work
4. When done: /backlog-complete {TASK_ID}

## Current Branch: {CURRENT_BRANCH}

Changes will be committed to this branch on completion.

═══════════════════════════════════════════════════════════════════
```

## Error Handling

- **No task ID provided:** "Usage: /backlog-work <task-id>"
- **Task not found:** Show available task IDs
- **Task has worktree:** Abort with worktree location
- **Another task in progress:** Abort with current task info
- **Task not Ready:** Show current status and suggest action

## Related Commands

- `/backlog-launch <ID>` - Create worktree for isolated work
- `/backlog-complete <ID>` - Complete in-session task
- `/backlog` - View all tasks
