---
name: claiming-tasks
description: Quick reference when blocked by "no active task" error. Shows how to create or claim a task before editing files.
---

# Claiming Tasks - Resolving Edit Blocks

This skill helps when you're blocked from editing files due to missing an active task.

## You've Been Blocked

The workflow system requires an active task before file modifications. If you see:

```
Blocked: No active task. Create or claim a task before editing files.
```

Follow the steps below to resolve.

## Quick Fix

### Option 1: Create a New Task

```python
# 1. Create the task
result = call_tool("gobby-tasks", "create_task", {
    "title": "Your task title",
    "description": "What you're doing",
    "task_type": "task",  # or bug, feature, epic
    "session_id": "<your_session_id>"  # Required - from SessionStart context
})

# 2. Set to in_progress
call_tool("gobby-tasks", "update_task", {
    "task_id": result["task_id"],
    "status": "in_progress"
})

# 3. Now you can edit files
```

### Option 2: Claim an Existing Task

```python
# Get suggested next task
result = call_tool("gobby-tasks", "suggest_next_task", {
    "session_id": "<your_session_id>"
})

# Set to in_progress
call_tool("gobby-tasks", "update_task", {
    "task_id": result["ref"],
    "status": "in_progress"
})
```

## Finding Your Session ID

Your `session_id` is injected at session start. Look for:

```
session_id: fd59c8fc-...
```

If not present, retrieve it with `get_current`:

```python
call_tool("gobby-sessions", "get_current", {
    "external_id": "<your-cli-session-id>",
    "source": "claude"
})
```

## Why This Matters

Tasks ensure:
- All code changes are tracked
- Work can be reviewed and linked to commits
- Dependencies between tasks are respected
- Session handoff preserves context
