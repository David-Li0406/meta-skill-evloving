# PRD JSON Schema

The PRD file (`prd.json`) is the **single source of truth** for story state and progress.
No separate progress.txt - the log is embedded in prd.json.

## Schema

```json
{
  "title": "feature-name",
  "spec_path": "plans/feature-name/spec.md",
  "created_at": "2026-01-23T12:00:00Z",
  "max_iterations": 25,

  "stories": [
    {
      "id": 1,
      "title": "User can create account",
      "category": "functional",
      "skills": ["skill-name-1"],
      "steps": [
        "Create signup form component",
        "Add email validation",
        "Connect to auth API",
        "Show success message"
      ],
      "passes": false,
      "priority": 1,
      "completed_at": null,
      "commit": null
    }
  ],

  "log": [
    {"ts": "2026-01-23T12:00:00Z", "event": "loop_started"},
    {"ts": "2026-01-23T12:30:00Z", "event": "story_complete", "story_id": 1, "commit": "abc123"}
  ]
}
```

## Field Definitions

### Story Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | integer | Yes | Stable reference for tracking |
| `title` | string | Yes | Short, action-oriented title |
| `category` | enum | Yes | Story type (see categories) |
| `skills` | string[] | For UI | Skills to load before implementing |
| `steps` | string[] | Yes | 3-7 verification steps |
| `passes` | boolean | Yes | Starts `false`, set `true` when done |
| `priority` | integer | Yes | 1=first (foundation), higher=later (polish) |
| `completed_at` | ISO8601/null | No | When story was completed |
| `commit` | string/null | No | Commit hash for the story |

### Categories

| Category | Description |
|----------|-------------|
| `functional` | Core feature functionality |
| `ui` | User interface components |
| `integration` | External service connections |
| `edge-case` | Error handling, boundary conditions |
| `performance` | Optimization, caching |

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Feature name (kebab-case) |
| `spec_path` | string | Path to spec.md |
| `created_at` | ISO8601 | PRD creation timestamp |
| `max_iterations` | integer | Recommended iteration count |
| `stories` | array | Ordered list of stories |
| `log` | array | Embedded progress log (hook appends) |

### Log Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `ts` | ISO8601 | Timestamp |
| `event` | string | Event type: `loop_started`, `story_started`, `story_complete`, `iteration_end`, `loop_complete` |
| `story_id` | integer | Story ID (for story events) |
| `commit` | string | Commit hash (for story_complete) |
| `notes` | string | Optional notes |

## Story Size Guidelines

A well-sized story:
- Completes in ~15-30 minutes
- Has 3-7 verification steps
- Touches 1-3 files
- Has no "and" in the title

## Examples

### Good Story (Atomic)

```json
{
  "id": 1,
  "title": "User can view login form",
  "category": "ui",
  "skills": ["frontend-design"],
  "steps": [
    "Create LoginForm component",
    "Add email and password inputs",
    "Add submit button",
    "Form is responsive"
  ],
  "passes": false,
  "priority": 1,
  "completed_at": null,
  "commit": null
}
```

### Bad Story (Too Large)

```json
{
  "id": 1,
  "title": "User can login and see dashboard",
  "category": "functional",
  "steps": [
    "Create login form",
    "Add validation",
    "Connect to API",
    "Store session",
    "Create dashboard layout",
    "Fetch user data",
    "Display user info",
    "Add logout button"
  ],
  "passes": false,
  "priority": 1
}
```

Should be split into:
1. "User can view login form"
2. "User can submit login credentials"
3. "User can view dashboard"
4. "User can logout"

## State Management

### Single Source of Truth

The prd.json file IS the state. The `/go` loop:
- Reads prd.json to find the next incomplete story
- Updates `passes: true` when story completes
- Sets `completed_at` timestamp and `commit` hash
- The hook appends to the embedded `log` array

### What Claude Updates

```json
// Story completion - Claude updates these fields:
{
  "passes": true,
  "completed_at": "2026-01-23T12:30:00Z",
  "commit": "abc123"
}
```

### What Hook Appends (Automatic)

```json
// Hook auto-appends to log array:
{"ts": "...", "event": "story_complete", "story_id": 1, "commit": "abc123"}
```

### Backward Compatibility

Old PRDs without a `log` field still work. The hook creates the log array if missing.
