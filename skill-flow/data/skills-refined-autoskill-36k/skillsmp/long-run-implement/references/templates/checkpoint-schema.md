# Checkpoint Schema Documentation

## Overview

Checkpoints track executor progress for resume capability and status monitoring.

Location: `{state_path}/plans/{NN}-CHECKPOINT.json`

## Field Definitions

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `plan_number` | string | Plan identifier (e.g., "01", "02") |
| `current_task_index` | number | 0-based index of current task |
| `current_task` | string | Human-readable current task name |
| `status` | string | One of: "in_progress", "completed", "failed", "timeout" |
| `last_activity` | string | ISO 8601 timestamp of last update |

### Progress Tracking Fields

| Field | Type | Description |
|-------|------|-------------|
| `total_tasks` | number | Total task count in plan |
| `completed_tasks` | array | List of completed task objects: `{ name: string, commit: string }` |
| `remaining_tasks` | array | List of remaining task objects: `{ name: string }` |
| `task_commits` | object | Map of task index to commit SHA: `{ "1": "abc123" }` |

### File Tracking Fields

| Field | Type | Description |
|-------|------|-------------|
| `files_modified` | array | List of file paths modified by this plan |
| `partial_commits` | array | Commits made before interruption/failure |

### Error Fields

| Field | Type | Description |
|-------|------|-------------|
| `error` | string\|null | Error message if status is "failed" |

## Usage by Component

### spawn-plan-executor.md
Uses for resume capability:
- `plan_number`, `total_tasks`, `task_commits`, `files_modified`, `last_activity`

### timeout-handling.md
Uses for status display:
- `plan_number`, `current_task`, `completed_tasks`, `remaining_tasks`, `partial_commits`, `last_activity`

### long-run-executor
Writes checkpoint after each task completion.

## Example

```json
{
  "plan_number": "02",
  "current_task_index": 2,
  "current_task": "Task 3: Add API routes",
  "completed_tasks": [
    { "name": "Task 1: Setup", "commit": "abc123" },
    { "name": "Task 2: Models", "commit": "def456" }
  ],
  "remaining_tasks": [
    { "name": "Task 4: Tests" }
  ],
  "last_activity": "2026-01-15T14:30:00Z",
  "status": "in_progress",
  "error": null,
  "total_tasks": 4,
  "task_commits": {
    "1": "abc123",
    "2": "def456"
  },
  "files_modified": ["src/api.ts", "src/models.ts"],
  "partial_commits": []
}
```
