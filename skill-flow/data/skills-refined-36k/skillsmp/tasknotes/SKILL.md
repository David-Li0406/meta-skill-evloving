---
name: tasknotes
description: Create, update, delete, and list tasks via HTTP API. USE WHEN user wants to create tasks, mark done, update status, or manage tasks.
---

# TaskNotes Skill

CRUD operations on tasks via TaskNotes plugin HTTP API.

## API Endpoint

```
http://127.0.0.1:8090/api
```

## List Tasks

```bash
curl -s "http://127.0.0.1:8090/api/tasks"
curl -s "http://127.0.0.1:8090/api/tasks?status=in-progress"
```

## Create Task

```bash
curl -X POST "http://127.0.0.1:8090/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Task title",
    "status": "open",
    "priority": "high",
    "projects": ["[[Project Name]]"],
    "due": "2026-01-15",
    "scheduled": "2026-01-10"
  }'
```

**Fields:**

| Field | Values |
|-------|--------|
| title | Task name (required) |
| status | `open`, `in-progress`, `done` |
| priority | `none`, `low`, `normal`, `high` |
| projects | `["[[Project Name]]"]` - array of wikilinks |
| due | `YYYY-MM-DD` |
| scheduled | `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS` |

## Update Task

```bash
curl -X PUT "http://127.0.0.1:8090/api/tasks/Tasks%2Fmy-task.md" \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

**Note:** Path must be URL-encoded (`/` → `%2F`, space → `%20`)

## Delete Task

```bash
curl -X DELETE "http://127.0.0.1:8090/api/tasks/Tasks%2Fmy-task.md"
```

## Get Options

```bash
curl -s "http://127.0.0.1:8090/api/options"
```

Returns available statuses, priorities, and projects.

## Example Workflow

```bash
# Create
curl -X POST "http://127.0.0.1:8090/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Review proposal", "status": "open", "projects": ["[[Website Redesign]]"]}'

# Start working
curl -X PUT "http://127.0.0.1:8090/api/tasks/Tasks%2FReview%20proposal.md" \
  -H "Content-Type: application/json" \
  -d '{"status": "in-progress"}'

# Complete
curl -X PUT "http://127.0.0.1:8090/api/tasks/Tasks%2FReview%20proposal.md" \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```
