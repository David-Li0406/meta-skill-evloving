---
name: idlergear
description: Use this skill for knowledge management in AI-assisted development, particularly when starting a session, tracking tasks, or capturing notes.
---

# IdlerGear Knowledge Management

IdlerGear provides structured knowledge persistence across AI sessions.

## Session Start (MANDATORY)

**Call this MCP tool at the start of EVERY session:**

```
idlergear_session_start()
```

This returns:
- Project vision and goals
- Current plan and open tasks
- Recent notes and session state
- Recommendations for what to work on

## Quick Reference

### Creating Knowledge

| Action | MCP Tool |
|--------|----------|
| Create task | `idlergear_task_create(title="...", labels=["bug"])` |
| Quick note | `idlergear_note_create(content="...", tags=["idea"])` |
| Research | `idlergear_note_create(content="...", tags=["explore"])` |
| Documentation | `idlergear_reference_add(title="...", body="...")` |

### Retrieving Knowledge

| Action | MCP Tool |
|--------|----------|
| List tasks | `idlergear_task_list(state="open")` |
| Search all | `idlergear_search(query="...")` |
| Show vision | `idlergear_vision_show()` |
| Project status | `idlergear_status()` |

### File Status Tracking

Track which files are current, deprecated, archived, or problematic to prevent using outdated code:

| Action | MCP Tool |
|--------|----------|
| Register file | `idlergear_file_register(path="...", status="current")` |
| Deprecate file | `idlergear_file_deprecate(path="...", successor="...", reason="...")` |
| Check file status | `idlergear_file_status(path="...")` |
| List files by status | `idlergear_file_list(status="deprecated")` |

**File statuses:**
- `current` - Active, should be used
- `deprecated` - Outdated, successor available
- `archived` - Old version kept for reference
- `problematic` - Has known issues

## Session End

Before ending a session, consider:
```
idlergear_session_end(notes="what was accomplished")
```

This saves state for the next session.

## Forbidden Actions

**DO NOT create files:**
- `TODO.md`, `NOTES.md`, `SESSION_*.md`, `SCRATCH.md`

**DO NOT write comments:**
- `// TODO:`, `# FIXME:`, `/* HACK: */`

**INSTEAD:** Use `idlergear_task_create()` or `idlergear_note_create()`