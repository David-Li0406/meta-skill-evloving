# JSON Specification Structure

The formal specification format used by all SDD tools.

## Top-Level Structure

```json
{
  "spec_id": "feature-name-001",
  "title": "Feature Name Implementation",
  "description": "One paragraph describing the feature",
  "version": "1.0.0",
  "created": "2025-01-15T10:00:00Z",
  "updated": "2025-01-15T10:00:00Z",
  "metadata": {
    "mission": "Ensure every school admin sees accurate trust signals before launch",
    "status": "pending",
    "priority": "high",
    "owner": "developer@example.com",
    "tags": ["feature", "auth"],
    "estimated_hours": 40
  },
  "phases": { ... },
  "journal": []
}
```

## Metadata Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mission` | string | Recommended | Single-sentence mission describing the spec's purpose |
| `status` | string | Yes | `pending`, `active`, `completed`, `archived` |
| `priority` | string | No | `low`, `medium`, `high`, `critical` |
| `owner` | string | No | Email or identifier of owner |
| `tags` | array | No | Categorization tags |
| `estimated_hours` | number | No | Total estimated hours |

> Mission helps provide context and should be populated before handing off the spec.
 
## Phase Structure


```json
{
  "phases": {
    "phase-1": {
      "title": "Foundation",
      "description": "Set up core infrastructure",
      "order": 1,
      "status": "pending",
      "tasks": { ... }
    },
    "phase-2": {
      "title": "Implementation",
      "description": "Build core functionality",
      "order": 2,
      "status": "pending",
      "depends_on": ["phase-1"],
      "tasks": { ... }
    }
  }
}
```

## Task Structure

```json
{
  "task-1-1": {
    "title": "Create database schema",
    "type": "task",
    "status": "pending",
    "description": "Define tables for user authentication",
    "metadata": {
      "file_path": "src/db/schema.sql",
      "task_category": "implementation",
      "estimated_hours": 2
    },
    "instructions": [
      "Create users table with id, email, password_hash",
      "Add sessions table for token storage",
      "Create necessary indexes"
    ],
    "acceptance_criteria": [
      "Schema passes validation",
      "Migrations run without errors"
    ]
  }
}
```

### Required Fields for Implementation Tasks

Best practices for well-structured specs:
- `metadata.mission` at the spec level
- Every `type: "task"` node includes `description`, `acceptance_criteria`, and `metadata.task_category`
- `metadata.file_path` for `implementation` and `refactoring` tasks

## Creating a Spec

```bash
# Create from template
mcp__plugin_foundry_foundry-mcp__authoring action="spec-create" name="feature-name" template="empty"

# Templates: empty (blank spec with no phases - use phase templates to add structure)
```
