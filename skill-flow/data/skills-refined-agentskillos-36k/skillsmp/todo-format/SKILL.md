---
name: Todo Format
description: >-
  Knowledge about the todo task file format and workflow.
  Use this skill when working with files in todo/open/, todo/wip/, or todo/done/ directories.
version: 0.1.0
---

# Todo Format Knowledge

## Directory Structure

```
todo/
├── open/     # New tasks, not yet started
├── wip/      # Work in progress
└── done/     # Completed tasks
```

## File Naming

**Pattern:** `<ID>-<slug>.md`

- **ID**: 3-digit zero-padded number (001, 042, 123)
- **Slug**: Kebab-case title, max 50 chars

**Examples:**
- `001-fix-login-bug.md`
- `042-add-dark-mode-support.md`
- `123-refactor-api-endpoints.md`

## Task File Structure

```markdown
# <ID>: <Title>

**Status:** open | **Priority:** medium | **Assignee:** unassigned
**Created:** 2026-01-21 | **Branch:** <id>-<slug>

## Description
Brief description of the task.

## Tasks
- [ ] Task 1
- [ ] Task 2
- [x] Completed task

## Dependencies
- Depends on: 039, 041
- Blocks: 044

## PRD
<!-- Inferred from implementation decisions -->

## Implementation Log
<!-- Timestamped entries of work done -->
```

## Status Values

| Status | Directory | Meaning |
|--------|-----------|---------|
| `open` | `todo/open/` | Not started |
| `wip` | `todo/wip/` | Work in progress |
| `done` | `todo/done/` | Completed |

Status in file header must match the directory location.

## Header Fields

| Field | Format | Example |
|-------|--------|---------|
| Status | open/wip/done | `wip` |
| Priority | high/medium/low | `high` |
| Assignee | name or "unassigned" | `Thomas Landgraf` |
| Created | YYYY-MM-DD | `2026-01-21` |
| Started | YYYY-MM-DD HH:MM | `2026-01-21 14:30` |
| Completed | YYYY-MM-DD HH:MM | `2026-01-21 18:45` |
| Branch | id-slug | `042-fix-login-bug` |

## Task Checkboxes

```markdown
- [ ] Not started
- [x] Completed
```

## Dependencies

Reference other tasks by ID only (no paths):
```markdown
- Depends on: 039, 041
- Blocks: 044, 045
```

- **Depends on**: This task needs those tasks completed first
- **Blocks**: Those tasks are waiting on this task

## Implementation Log Format

```markdown
### 2026-01-21 14:30
**Files modified:**
- `src/auth/login.js` - Fixed token validation
- `tests/auth.test.js` - Added 3 test cases
**Notes:** Optional additional context
**Result:** In progress / Success / Failed

### 2026-01-21 18:45
**Completed** by Thomas Landgraf
**Summary:** Brief summary of accomplishment
```

## PRD Section

The PRD (Product Requirement Definition) is inferred from implementation:
- Document decisions made during development
- Capture requirements that emerged from building
- Keep concise - bullet points preferred

## Git Integration

- **Branch naming**: `<id>-<slug>` (e.g., `042-fix-login-bug`)
- **Manual commits**: Plugin never auto-commits
- **Clean state**: Starting a task requires clean git working directory

## Commands

| Command | Purpose |
|---------|---------|
| `/todo:add <desc>` | Create new task in open/ |
| `/todo:start [id]` | Move to wip/, create branch |
| `/todo:update` | Log progress, update tasks |
| `/todo:done [id]` | Move to done/, finalize |
