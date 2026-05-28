---
name: committing-changes
description: Commit message format and task close workflow. Use when ready to commit or closing tasks.
---

# Committing Changes - Commit and Close Workflow

This skill covers the commit message format and how to properly close tasks.

## Commit and Close Workflow

### Step 1: Stage Changes

```bash
git add <specific-files>
```

Prefer staging specific files over `git add -A`.

### Step 2: Commit with Task ID

```bash
git commit -m "[task-id] type: description"
```

Include the task ID in brackets at the start of the message.

### Step 3: Close the Task

```python
call_tool("gobby-tasks", "close_task", {
    "task_id": "<task-id>",
    "commit_sha": "<commit-sha>"
})
```

## Commit Message Format

```
[<task-id>] <type>: <description>

<optional body>
```

### Valid Commit Types

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring |
| `test` | Adding tests |
| `docs` | Documentation |
| `chore` | Maintenance |

### Examples

```
[abc123] feat: add user authentication
[xyz789] fix: resolve password reset bug
[def456] refactor: extract auth logic to service
[ghi012] test: add unit tests for auth module
```

## Closing Without Commits

For non-code tasks (research, planning):

```python
call_tool("gobby-tasks", "close_task", {
    "task_id": "<task-id>",
    "no_commit_needed": True
})
```

## Common Mistakes

### Wrong: Close Before Commit

```python
# This will fail
call_tool("gobby-tasks", "close_task", {"task_id": "abc"})
```

### Right: Commit First, Then Close

```bash
git commit -m "[abc] feat: implement feature"
```

```python
call_tool("gobby-tasks", "close_task", {
    "task_id": "abc",
    "commit_sha": "a1b2c3d"
})
```

## Task Lifecycle

```
open → in_progress → review → closed
```

Tasks may enter `review` status instead of `closed` when:
- Task has `requires_user_review=true`
- Validation criteria fail

User must explicitly close reviewed tasks.
