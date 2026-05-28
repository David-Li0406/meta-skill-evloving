# Session State JSON Format

## Complete Schema

```json
{
  "session_id": "string - Unique session identifier",
  "timestamp": "string - ISO 8601 timestamp",
  "project_root": "string - Absolute path to project",
  "project_name": "string - Human-readable project name",
  "edited_files": ["array", "of", "file", "paths"],
  "todos": [
    {
      "content": "string - Todo description",
      "status": "pending|in_progress|completed",
      "activeForm": "string - Present continuous form"
    }
  ],
  "phase": {
    "name": "string - Current phase name",
    "completion": "number - 0-100",
    "chunk_id": "string - Optional chunk identifier",
    "chunk_files": ["array", "of", "files", "in", "chunk"]
  },
  "plan": {
    "file": "string - Plan file name",
    "path": "string - Absolute path to plan",
    "total_tasks": "number",
    "completed_tasks": "number",
    "progress": "number - 0-100",
    "last_modified": "string - ISO 8601 timestamp"
  },
  "git": {
    "branch": "string - Current branch name",
    "has_uncommitted_changes": "boolean",
    "staged_files": "number",
    "unstaged_files": "number",
    "untracked_files": "number",
    "last_commit": "string - Short hash and message"
  },
  "session_duration_minutes": "number",
  "checkpoint_reason": "automatic|manual|phase_complete|Stop hook",
  "checkpoint_type": "periodic|event_driven|user_requested",
  "activity_summary": {
    "files_created": "number",
    "files_modified": "number",
    "lines_added": "number",
    "lines_deleted": "number",
    "commits": "number"
  },
  "context_notes": "string - Optional freeform notes",
  "warnings": ["array", "of", "warning", "messages"]
}
```

## Required Fields

Minimum viable state file:
- `session_id`
- `timestamp`
- `project_root`
- `checkpoint_reason`

All other fields optional but recommended.

## Field Descriptions

### session_id
Format: `session_YYYY-MM-DD_HH-MM-SS`
Example: `session_2026-01-22_15-30-45`
Purpose: Unique identifier for this session

### edited_files
Array of file paths relative to project_root
Limit: 50 most recent files
Order: Most recently edited first

### todos
Array of todo objects with:
- `content`: Task description
- `status`: One of: pending, in_progress, completed
- `activeForm`: Present continuous (for in_progress display)

### phase
Current work phase information:
- `name`: Phase title (e.g., "Phase 3: API Integration")
- `completion`: Percentage 0-100
- `chunk_id`: Optional chunk identifier if using chunking
- `chunk_files`: Files in this chunk for context

### checkpoint_reason
Why this checkpoint was created:
- `automatic`: Periodic auto-save (every 15 min)
- `manual`: User-initiated save
- `phase_complete`: Phase finished
- `Stop hook`: Session ending

## Size Limits

Target state file size: <10 KB
- Limit edited_files to 50 entries
- Limit todos to 50 entries
- Truncate long warnings to 500 chars each
- Keep context_notes under 1000 chars

## Validation

Check JSON validity:
```bash
jq '.' .claude/.project-state.json >/dev/null
```

Validate required fields:
```bash
jq -e '.session_id, .timestamp, .project_root, .checkpoint_reason' \
  .claude/.project-state.json >/dev/null
```

## Backup Strategy

Before overwriting:
```bash
cp .claude/.project-state.json .claude/.project-state.json.bak
```

Write atomically:
```bash
echo "$STATE_JSON" > .claude/.project-state.json.tmp
mv .claude/.project-state.json.tmp .claude/.project-state.json
```
