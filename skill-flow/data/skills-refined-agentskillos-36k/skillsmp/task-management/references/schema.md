# Task Schema

## File Structure

```yaml
# .claude/tasks/tasks.yaml
version: "1.0"
metadata:
  project: "project-name"
  created: "2026-01-22"
  updated: "2026-01-22T10:00:00Z"

tasks:
  - id: "t-001"
    title: "Task title"
    status: pending
    created: "2026-01-22T10:00:00Z"
    updated: "2026-01-22T10:00:00Z"
    # ... optional fields

_counter: 1
```

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Auto-generated: t-XXX |
| title | string | Task title |
| status | enum | pending, in_progress, completed, blocked |
| created | ISO date | Creation timestamp |

## Optional Fields

| Field | Type | Values |
|-------|------|--------|
| description | string | Detailed description |
| priority | enum | low, medium, high, critical |
| effort | enum | S, M, L, XL |
| tags | string[] | Category tags |
| assignee | string | Assignee name |
| due_date | date | YYYY-MM-DD format |

## Context Linking

```yaml
context:
  plan: "plans/260122-feature/plan.md"
  phase: 2
  branch: "feature/auth"
  files:
    - "src/auth/*"
```

## Progress Tracking

```yaml
progress:
  checklist:
    - [x] "Subtask 1"
    - [ ] "Subtask 2"
  notes: "Additional notes"
```

## Dependencies

```yaml
blocks: ["t-003", "t-004"]     # Tasks this blocks
blocked_by: ["t-002"]          # Tasks blocking this
```

## Custom Fields

```yaml
custom:
  sprint: 5
  points: 3
  reviewer: "john"
```

## Archive Structure

```yaml
# .claude/tasks/archive/260122-batch.yaml
archived:
  - id: "t-001"
    # ... all task fields
    completed_at: "2026-01-22T15:00:00Z"
    archived_at: "2026-01-22T15:00:01Z"
```
