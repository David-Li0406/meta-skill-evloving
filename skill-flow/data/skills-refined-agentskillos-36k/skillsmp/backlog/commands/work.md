---
description: Start working on a task in the current session (no worktree)
argument-hint: <task-id>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Start In-Session Task

Start working on a task directly in the current session without creating a worktree. This is ideal for quick, simple tasks that don't need worktree isolation.

**Arguments:** $ARGUMENTS

## Instructions

### Step 1: Parse Arguments

1. **Extract task ID** from arguments (e.g., "MKT-007").

2. **If no task ID provided:**
   - Use AskUserQuestion to select from Ready tasks
   - Or show usage: `/backlog:work <task-id>`

### Step 2: Validate Task

1. **Find task directory:**
   ```bash
   ls -d tasks/${TASK_ID}-* 2>/dev/null
   ```

2. **If not found:** Show available tasks and abort.

3. **Read task status from INDEX.md:**
   ```bash
   grep "| ${TASK_ID} |" tasks/INDEX.md
   ```

4. **Check status:**
   - If "Complete": Abort - "Task is already complete"
   - If "In Progress": Check for conflicts (Step 3)
   - If "In Review": Abort - "Task is in review mode"
   - If "Blocked": Abort - "Task is blocked by dependencies"
   - If "Ready": Proceed

### Step 3: Check for Conflicts

**Check for existing worktree:**

```bash
# Check if task has an active worktree
WORKTREE=$(git worktree list | grep -i "${TASK_ID}" | head -1)

if [[ -n "$WORKTREE" ]]; then
  WT_PATH=$(echo "$WORKTREE" | awk '{print $1}')
  echo "ERROR: Task ${TASK_ID} has an active worktree at:"
  echo "  ${WT_PATH}"
  echo ""
  echo "Options:"
  echo "1. Continue work in the worktree instead"
  echo "2. Remove the worktree first with /backlog:complete or manually"
  exit 1
fi
```

**Check for existing PROMPT.md:**

```bash
if [[ -f "PROMPT.md" ]]; then
  # Read task ID from existing PROMPT.md
  EXISTING_TASK=$(grep "^\*\*Task:\*\*" PROMPT.md | sed 's/.*\*\*Task:\*\* \([A-Z]*-[0-9]*\).*/\1/' | head -1)

  if [[ -n "$EXISTING_TASK" && "$EXISTING_TASK" != "$TASK_ID" ]]; then
    echo "ERROR: Another task is already in progress in this session"
    echo "  Current: ${EXISTING_TASK}"
    echo "  Requested: ${TASK_ID}"
    echo ""
    echo "Options:"
    echo "1. Complete the current task first: /backlog:complete ${EXISTING_TASK}"
    echo "2. Abandon the current task: rm PROMPT.md"
    exit 1
  fi
fi
```

### Step 4: Branch Handling

```bash
CURRENT_BRANCH=$(git branch --show-current)

if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
  # On main - optionally create feature branch
  # For simple tasks, can stay on main
  # For complex tasks, suggest creating branch

  echo "Currently on main branch."
  echo "For simple tasks, you can work directly on main."
  echo "For complex tasks, a feature branch will be created on completion if needed."
fi
```

### Step 5: Create PROMPT.md

**Load task details:**

```bash
TASK_DIR=$(ls -d tasks/${TASK_ID}-* 2>/dev/null | head -1)
TASK_NAME=$(basename "$TASK_DIR")

# Read task title from TASK.md
TASK_TITLE=$(grep "^# Task" "${TASK_DIR}/TASK.md" | sed 's/# Task [A-Z]*-[0-9]*: //')

# Read repo name from design.yaml
REPO_NAME=$(grep "^repo_name:" design.yaml | sed 's/repo_name: *//')
```

**Generate PROMPT.md:**

```markdown
# Agent Task Assignment

**Task:** {TASK_ID} - {TASK_TITLE}
**Repo:** {REPO_NAME}
**Mode:** Implementation (In-Session)
**Task Directory:** tasks/{TASK_NAME}/

## Required Reading

1. `tasks/{TASK_NAME}/TASK.md` - Full requirements
2. `tasks/{TASK_NAME}/PROGRESS.md` - Prior work and current state

## Instructions

1. Read TASK.md to understand requirements
2. Read PROGRESS.md to see what's been done
3. Implement the task requirements
4. **Update PROGRESS.md** as you work
5. When complete, run: `/backlog:complete {TASK_ID}`

## On Context Compaction

If your context is compacted or you're resuming work:
1. Re-read this PROMPT.md
2. Re-read PROGRESS.md for your prior state
3. Continue from the last recorded progress

## Completion

When implementation is done:

```
/backlog:complete {TASK_ID}
```

This will:
- Clean up PROMPT.md
- Update INDEX.md status to Complete
- If on a feature branch: rebase and merge to main
```

### Step 6: Update INDEX.md

```bash
# Update status to "In Progress"
sed -i.bak "s/| ${TASK_ID} |\([^|]*\)| Ready |/| ${TASK_ID} |\1| In Progress |/" tasks/INDEX.md
rm -f tasks/INDEX.md.bak

echo "✓ Task status updated to In Progress"
```

### Step 7: Initialize PROGRESS.md

**If PROGRESS.md doesn't exist or shows "Not started":**

Update PROGRESS.md to mark task started:

```bash
# Add session log entry
TODAY=$(date +%Y-%m-%d)
```

Append or update session log with:
```markdown
### {TODAY} - In-Session Work Started

- Task started via /backlog:work
- Working directly in current session (no worktree)
- Ready to begin implementation
```

### Step 8: Register with Built-in Task Feature

**IMPORTANT:** Use the built-in Task feature to track active work in the session.

Call `TaskCreate` with:
- **subject**: `{TASK_ID}: {TASK_TITLE}`
- **description**: Read from `tasks/{TASK_NAME}/TASK.md` - include the full task description
- **activeForm**: `Working on {TASK_ID}`

Then call `TaskUpdate` to set status to `in_progress`:
- **taskId**: The ID returned from TaskCreate
- **status**: `in_progress`

This provides real-time visibility of your current work in Claude's UI.

### Step 9: Output Instructions

```
═══════════════════════════════════════════════════════════════════
 TASK STARTED: {TASK_ID} - {TASK_TITLE}
═══════════════════════════════════════════════════════════════════

Working in-session (no worktree).

## Context Loaded

PROMPT.md created with task context.
Built-in Task registered for session tracking.

## Required Reading

Read these files to understand the task:

1. tasks/{TASK_NAME}/TASK.md - Requirements
2. tasks/{TASK_NAME}/PROGRESS.md - Progress log

## Workflow

1. Read the task requirements
2. Implement the changes
3. Update PROGRESS.md as you work
4. When done: /backlog:complete {TASK_ID}

## Current Branch: {CURRENT_BRANCH}

{If on main}
Working on main branch. For simple tasks this is fine.
Changes will be committed directly to main on completion.

{If on feature branch}
Working on feature branch: {CURRENT_BRANCH}
On completion, branch will be rebased onto main and merged.

═══════════════════════════════════════════════════════════════════
```

## Error Handling

- **No task ID provided:** "Usage: /backlog:work <task-id>"
- **Task not found:** Show available task IDs
- **Task has worktree:** Abort with worktree location
- **Another task in progress:** Abort with current task info
- **Task not Ready:** Show current status and suggest action
- **No tasks/ directory:** "Run /design:init first"

## Related Commands

- `/backlog:launch <ID>` - Create worktree for isolated work
- `/backlog:complete <ID>` - Complete and cleanup in-session task
- `/backlog:read <ID>` - Read task details
- `/backlog` - View all tasks
