---
name: EventSource
description: SQLite event sourcing for progress tracking. USE WHEN starting complex tasks, multi-step work, or when asked to track progress. Current state = f(events).
---

# EventSource - Automatic Event Sourcing

**Events are captured automatically via hooks.** No manual logging required.

---

## Quick Reference (READ THIS FIRST)

**Database Location:** `~/.claude/events/{project}.db`

**Timestamps:** Stored as ISO strings (e.g., `2026-01-14 01:54:42`). NO conversion needed.

**Quick Queries:**
```bash
# Use the CLI tool (recommended)
bun ~/.claude/hooks/event-query.ts status       # Current project status
bun ~/.claude/hooks/event-query.ts projects     # List all project DBs

# Direct SQLite (timestamps are already strings!)
sqlite3 ~/.claude/events/es-demo-go.db "
  SELECT timestamp, event_type, entity_id
  FROM events
  ORDER BY timestamp DESC
  LIMIT 10
"

# Last session's work
sqlite3 ~/.claude/events/PROJECT.db "
  SELECT timestamp, event_type, entity_id,
         json_extract(data, '$.prompt_preview') as prompt
  FROM events
  WHERE session_id = (
    SELECT session_id FROM events
    WHERE event_type = 'slice_started'
    ORDER BY timestamp DESC LIMIT 1 OFFSET 1
  )
  ORDER BY timestamp
"
```

**Common Mistakes:**
- ❌ Looking in `~/.claude/project.db` (wrong: use `~/.claude/events/project.db`)
- ❌ Using `datetime(timestamp/1000, 'unixepoch')` (wrong: timestamps are already ISO strings)
- ❌ Manual queries when CLI exists (use `event-query.ts` for common patterns)

---

## How It Works

1. **UserPromptSubmit** → Creates a new slice (logs `slice_started` event)
2. **PostToolUse** → Derives current slice from events, logs tool execution
3. **SessionStop** → Marks session end

Events are stored per-project: `~/.claude/events/{project}.db`

**Pure ES**: Current slice is derived by querying the latest `slice_started` event for the session - no mutable state files.

---

## Philosophy

1. **Events are immutable facts** — Something happened. Record it. Never update or delete.
2. **State is derived** — Current state = fold(events). Always reconstructable.
3. **Slices are vertical** — Each user prompt starts a slice; all resulting events belong to it.
4. **Automatic capture** — Hooks log events; you focus on work.
5. **Project-scoped** — Every event belongs to a project DB.

---

## Schema

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    event_id TEXT UNIQUE,      -- UUIDv7
    timestamp TEXT,
    session_id TEXT,           -- Correlation across slices
    slice_id TEXT,             -- Vertical slice (one user request)
    event_type TEXT,
    entity_type TEXT,
    entity_id TEXT,
    data JSON,
    tags JSON                  -- Flexible filtering
);
```

---

## Auto-Captured Events

| Event Type | Entity Type | When |
|------------|-------------|------|
| `slice_started` | slice | User sends a prompt |
| `file_created` | file | Write tool |
| `file_modified` | file | Edit tool |
| `command_executed` | command | Bash (significant commands) |
| `resource_fetched` | url | WebFetch |
| `web_searched` | search | WebSearch |
| `task_spawned` | task | Task tool |
| `todos_updated` | todos | TodoWrite |
| `session_stopped` | session | Session ends |

**Filtered out** (too noisy): Read, Glob, Grep, LSP, trivial bash commands (ls, cat, echo)

---

## Query Patterns

### Using event-query.ts

```bash
# List all projects with events
bun ~/.claude/hooks/event-query.ts projects

# Project status (files, commands, summary)
bun ~/.claude/hooks/event-query.ts status nixos

# Latest slice events
bun ~/.claude/hooks/event-query.ts slice

# Recent activity across projects
bun ~/.claude/hooks/event-query.ts recent 7
```

### Direct SQL

```sql
-- Files modified today
SELECT entity_id, COUNT(*) as edits
FROM events
WHERE event_type IN ('file_created', 'file_modified')
  AND timestamp > datetime('now', '-1 day')
GROUP BY entity_id;

-- Slice timeline (what happened in a slice)
SELECT timestamp, event_type, entity_id
FROM events
WHERE slice_id = 'your-slice-id'
ORDER BY timestamp;

-- Commands that failed
SELECT timestamp, json_extract(data, '$.command') as cmd
FROM events
WHERE event_type = 'command_executed'
  AND json_extract(data, '$.success') = 0;

-- Recent slices with their events
SELECT
    e.slice_id,
    s.timestamp as started,
    json_extract(s.data, '$.prompt_preview') as prompt,
    COUNT(e.id) as events
FROM events e
JOIN events s ON s.slice_id = e.slice_id AND s.event_type = 'slice_started'
GROUP BY e.slice_id
ORDER BY s.timestamp DESC
LIMIT 10;
```

---

## Vertical Slices

A **slice** represents one user request and all the work that results from it:

```
User: "Add dark mode to the settings page"
  └── slice_started
      ├── file_modified: src/settings.tsx
      ├── file_modified: src/theme.ts
      ├── file_created: src/hooks/useDarkMode.ts
      ├── command_executed: bun test
      └── todos_updated: (3 completed)
```

Benefits:
- Clear audit trail per request
- Easy to see what a single prompt accomplished
- Natural unit for velocity tracking

---

## Cross-Project Queries

To query across all projects:

```bash
# Show recent activity
bun ~/.claude/hooks/event-query.ts recent 7

# Or manually:
for db in ~/.claude/events/*.db; do
  echo "=== $(basename $db .db) ==="
  sqlite3 $db "SELECT COUNT(*) FROM events WHERE timestamp > datetime('now', '-7 days')"
done
```

---

## Integration with TodoWrite

- **TodoWrite** → Real-time task visibility for the user
- **EventSource** → Persistent audit log, automatic capture

Both are useful. TodoWrite shows current state; EventSource records history.

---

## Anti-Patterns

**DON'T:**
- Manually log events (hooks do this)
- Update events (they're immutable)
- Store derived state (reconstruct from events)

**DO:**
- Query to understand project history
- Use slices to correlate related work
- Let hooks capture automatically
