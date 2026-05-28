---
name: restore-tasks
description: Restore tasks from a previous Claude Code session into the current session. Use when user wants to recover, restore, or load tasks from a past session, or when they mention tasks were lost after /clear or session restart. Triggers on "restore tasks", "load tasks", "recover tasks", "get my tasks back", "tasks from previous session".
---

# Restore Tasks

Recover persisted tasks from previous sessions.

## Storage Structure

```
~/.claude/tasks/<session-id>/     # Task JSON files (1.json, 2.json...)
~/.claude/projects/<encoded-path>/<session-id>.jsonl  # Session data
```

Path encoding: `/Users/bob/foo` → `-Users-bob-foo`

## Workflow

### 1. List available sessions

```bash
~/.claude/skills/restore-tasks/scripts/list-task-sessions.sh [project-path]
```

Returns JSON:
```json
{
  "sessions": [
    {"sessionId": "...", "summary": "...", "modified": "2026-01-23T17:39:14.519Z", "taskCount": 7}
  ],
  "total": 10,
  "showing": 5,
  "hasMore": true
}
```

Options:
- `--limit N` - Show N sessions (default: 5)
- `--all` - Show all sessions

Sessions sorted by `modified` (most recent first).

### 2. User selects session

Use `AskUserQuestion` to present choices. Format each option as:
- **label**: Truncated summary (max ~30 chars)
- **description**: `{taskCount} tasks • {formatted_date}` (e.g., "7 tasks • Jan 23, 5:39 PM")

Include "Show more sessions" option if `hasMore` is true.

Example:
```json
{
  "question": "Which session to restore?",
  "header": "Session",
  "options": [
    {"label": "Exchange rates app API...", "description": "7 tasks • Jan 23, 5:39 PM"},
    {"label": "Multi-Agent Review & Skill...", "description": "5 tasks • Jan 23, 5:08 PM"},
    {"label": "Show more sessions", "description": "5 more available"}
  ],
  "multiSelect": false
}
```

If user selects "Show more", run script with `--all` and re-prompt.

### 3. Load tasks

```bash
~/.claude/skills/restore-tasks/scripts/dump-tasks.sh <session-id>
```

Returns JSON array of task objects.

### 4. Recreate tasks

For each task in the JSON:

1. Call `TaskCreate` with:
   - `subject`: task.subject
   - `description`: task.description
   - `activeForm`: task.activeForm

2. After all created, call `TaskUpdate` for each with `blockedBy` dependencies:
   - `taskId`: new task ID (matches original)
   - `addBlockedBy`: task.blockedBy array

### 5. Confirm

Call `TaskList` to show restored tasks.

## Task JSON Schema

```json
{
  "id": "1",
  "subject": "Task title",
  "description": "Full description",
  "activeForm": "Present continuous form",
  "status": "pending|in_progress|completed",
  "blocks": ["2", "3"],
  "blockedBy": ["4"]
}
```

## Error Handling

| Situation | Action |
|-----------|--------|
| No project data | Report "No Claude data for this directory" |
| No task sessions | Report "No previous sessions with tasks found" |
| Session not found | Ask user to verify session ID |
