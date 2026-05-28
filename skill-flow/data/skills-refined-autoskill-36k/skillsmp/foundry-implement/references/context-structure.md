# Deep Dive Context Structure

The `task action="prepare"` response provides comprehensive context for task execution.

## Response Structure

```json
{
  "task_data": {
    "id": "task-2-3",
    "title": "Implement JWT verification middleware",
    "type": "task",
    "status": "pending",
    "metadata": {
      "file_path": "src/middleware/auth.ts",
      "estimated_hours": 2,
      "task_category": "implementation"
    },
    "instructions": ["Step 1...", "Step 2..."]
  },
  "dependencies": {
    "can_start": true,
    "blocked_by": [],
    "depends_on": ["task-2-1", "task-2-2"]
  },
  "context": {
    "phase": {
      "id": "phase-2",
      "title": "Authentication Implementation",
      "progress": 0.4
    },
    "parent_task": {
      "id": "task-group-2",
      "title": "Auth Middleware"
    },
    "previous_sibling": {
      "id": "task-2-2",
      "title": "Create token service",
      "status": "completed",
      "summary": "Implemented JWT signing and validation..."
    },
    "sibling_files": [
      "src/services/token.ts",
      "tests/services/token.spec.ts"
    ],
    "journal": [
      {
        "timestamp": "2025-01-15T10:30:00Z",
        "entry_type": "decision",
        "title": "Using RS256 algorithm",
        "content": "Chose RS256 for JWT signing..."
      }
    ],
    "dependencies": {
      "task-2-1": {
        "status": "completed",
        "summary": "Database schema ready"
      }
    }
  }
}
```

## Using Context Fields

| Field | Purpose | Usage |
|-------|---------|-------|
| `task_data.instructions` | Step-by-step guidance | Primary implementation guide |
| `task_data.metadata.file_path` | Target file | Where to implement |
| `context.previous_sibling` | Prior work | Continuity reference |
| `context.sibling_files` | Related files | Files to review |
| `context.journal` | Decisions made | Architectural context |
| `dependencies.can_start` | Readiness check | Verify before starting |

## Fallback: task action="info"

When `task action="prepare"` doesn't provide needed data:

```bash
mcp__plugin_foundry_foundry-mcp__task action="info" spec_id={spec-id} task_id={task-id}
```

Returns focused task details without full context tree.
