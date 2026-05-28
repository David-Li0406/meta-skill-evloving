# Ultrawork State Schema

## Directory Structure

### Session Directory (Internal Metadata)

```
~/.claude/ultrawork/sessions/{session-id}/
├── session.json        # Session metadata (JSON)
├── context.json        # Explorer summaries (JSON)
├── exploration/        # Detailed exploration (Markdown)
│   ├── overview.md     # Project overview (always first)
│   ├── exp-1.md        # Targeted exploration
│   └── exp-N.md        # (dynamic count based on goal)
└── tasks/              # Task files (JSON)
    ├── 1.json
    ├── 2.json
    └── verify.json
```

**Stored in session directory**: exploration, tasks, context - temporary/internal metadata only

### Project Directory (User Deliverables)

Design documents, specs, and other **user-requested deliverables** are saved to project directory:

```
{working_dir}/docs/plans/
├── YYYY-MM-DD-{goal-slug}-design.md     # Design document
├── YYYY-MM-DD-{goal-slug}-spec.md       # Spec document
└── ...
```

**Stored in project directory**: design.md, spec, and other user-requested document deliverables

Session ID is provided by Claude Code via hooks (CLAUDE_SESSION_ID).

## context.json Schema (v2.1)

```json
{
  "version": "2.1",
  "expected_explorers": ["overview", "exp-1", "exp-2"],
  "exploration_complete": false,
  "explorers": [
    {
      "id": "overview",
      "hint": "Project overview",
      "file": "exploration/overview.md",
      "summary": "..."
    }
  ],
  "key_files": ["src/index.ts", "package.json"],
  "patterns": ["auth", "api-routes"],
  "constraints": []
}
```

| Field | Description |
|-------|-------------|
| `expected_explorers` | IDs of explorers that should complete |
| `exploration_complete` | Auto-set to true when all expected explorers finish |
| `explorers` | Completed explorer summaries with links to markdown |
| `key_files` | Important files discovered during exploration |
| `patterns` | Code patterns identified |

## session.json Schema (v5.1)

**Note:** Tasks are stored as separate files in `tasks/` directory, not embedded in session.json.

```json
{
  "version": "5.1",
  "session_id": "abc123-def456",
  "working_dir": "/path/to/project",
  "goal": "Original user request",
  "started_at": "2026-01-08T12:00:00Z",
  "updated_at": "2026-01-08T12:30:00Z",
  "phase": "PLANNING",
  "exploration_stage": "not_started",
  "iteration": 1,
  "plan": {
    "approved_at": null
  },
  "options": {
    "max_workers": 0,
    "max_iterations": 5,
    "skip_verify": false,
    "plan_only": false,
    "auto_mode": false
  },
  "evidence_log": [
    {
      "timestamp": "2026-01-08T12:15:00Z",
      "type": "agent_completed",
      "agent_id": "task-def456",
      "task_id": "1",
      "status": "completed",
      "summary": "Migration completed successfully"
    }
  ],
  "cancelled_at": null
}
```

| Field | Type | Description |
|-------|------|-------------|
| `working_dir` | string | Project root path. User deliverables (design docs, etc.) are saved relative to this path |

## tasks/{id}.json Schema

Each task is stored as a separate JSON file in the `tasks/` directory.

```json
{
  "id": "1",
  "subject": "Setup database",
  "description": "Create and run database migrations",
  "status": "open",
  "blockedBy": ["0"],
  "complexity": "standard",
  "criteria": [
    "Migration runs without error",
    "Schema validates"
  ],
  "evidence": [
    "npx prisma migrate deploy: All migrations applied successfully",
    "npm test: All tests passed"
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Task identifier |
| `subject` | string | Short task title |
| `description` | string | Detailed task description |
| `status` | string | `open`, `in_progress`, `resolved`, `failed` |
| `blockedBy` | string[] | IDs of tasks that must complete first |
| `complexity` | string | `trivial`, `standard`, `complex` |
| `criteria` | string[] | Success criteria list |
| `evidence` | string[] | Evidence strings (command outputs, results) |

## Phase Values

| Phase | Description |
|-------|-------------|
| `EXPLORATION` | Explorer agents gathering context |
| `PLANNING` | Design and task decomposition |
| `EXECUTION` | Workers executing tasks |
| `VERIFICATION` | Verify task running |
| `COMPLETE` | All criteria met |
| `FAILED` | Unrecoverable failure |
| `CANCELLED` | User cancelled |

## Exploration Stage Values

| Stage | Description |
|-------|-------------|
| `not_started` | Exploration not begun |
| `overview` | Overview explorer running |
| `analyzing` | Analyzing overview, generating hints |
| `targeted` | Targeted explorers running |
| `complete` | All exploration finished |

## Task Status Values

| Status | Description |
|--------|-------------|
| `open` | Ready to start |
| `in_progress` | Worker assigned |
| `resolved` | Completed with evidence |
| `failed` | Could not complete |

## Evidence Types

| Type | Description |
|------|-------------|
| `command_output` | Shell command result |
| `test_result` | Test suite output |
| `api_response` | HTTP response |
| `file_content` | File diff or content |
| `screenshot` | Visual verification |
| `manual` | User-provided evidence |

## State Transitions

```
EXPLORATION → PLANNING    (explorers complete)
PLANNING → EXECUTION      (planner completes)
EXECUTION → VERIFICATION  (all impl tasks done)
VERIFICATION → COMPLETE   (verify passes)

Any → FAILED              (unrecoverable error)
Any → CANCELLED           (user cancels)
```
