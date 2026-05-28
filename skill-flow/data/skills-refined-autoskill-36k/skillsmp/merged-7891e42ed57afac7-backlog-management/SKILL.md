---
name: backlog-management
description: Use this skill for managing project tasks with the Backlog.md CLI, including task creation, editing, status management, acceptance criteria, and searching.
---

# Backlog.md CLI Skill

You are a Backlog.md CLI expert assistant.

## Overview

Backlog.md is a CLI-based project management tool that uses markdown files to track tasks, documentation, and decisions. All operations go through the `backlog` CLI command.

**Key Principle**: NEVER edit task files directly. Always use CLI commands.

## Task Management Commands

### Create Task

```bash
backlog task create "<title>" -d "<description>" --ac "<criterion 1>" --ac "<criterion 2>"
```

- Use `--draft` for draft tasks.
- Use `-p <parent-id>` for subtasks.
- Include JIRA ticket in title: `"[PROJ-123] Task description"`.

### View Task

```bash
backlog task <id> --plain
```

- Always use `--plain` flag for AI-friendly output.
- Shows all task details, acceptance criteria, plan, and notes.

### Edit Task Metadata

```bash
backlog task edit <id> -s "<status>" -a @<username>
backlog task edit <id> -t "<new title>" -l <label1>,<label2> --priority <priority>
```

- `-s, --status` - Change status ("To Do", "In Progress", "Done").
- `-a, --assignee` - Assign to user.
- `-t, --title` - Update title.
- `-l, --labels` - Set labels (comma-separated).
- `--priority` - Set priority (low/medium/high).

### Manage Acceptance Criteria

```bash
# Add multiple ACs
backlog task edit <id> --ac "<new criterion>" --ac "<another one>"

# Check ACs (mark complete)
backlog task edit <id> --check-ac <index1> --check-ac <index2>

# Uncheck AC
backlog task edit <id> --uncheck-ac <index>

# Remove AC
backlog task edit <id> --remove-ac <index>
```

### Add Implementation Content

```bash
# Add plan (use ANSI-C quoting for newlines)
backlog task edit <id> --plan $'1. Research\n2. Implement\n3. Test'

# Add notes (PR description)
backlog task edit <id> --notes $'Implemented X\nUpdated tests'

# Append to notes
backlog task edit <id> --append-notes $'- Fixed bug\n- Added validation'
```

## Searching & Listing

### Search Tasks

```bash
backlog search "<keyword>" --plain
backlog search "<keyword>" --type task --status "<status>" --plain
```

### List Tasks

```bash
backlog task list --plain
backlog task list -s "<status>" -a @<username> --plain
backlog task list --priority <priority> --plain
```

## Typical Implementation Workflow

```bash
# 1. Find work
backlog task list -s "To Do" --plain

# 2. Start work
backlog task edit <id> -s "In Progress" -a @<username>

# 3. Add plan
backlog task edit <id> --plan $'1. Analyze\n2. Implement\n3. Test'

# 4. Mark ACs complete as you work
backlog task edit <id> --check-ac <index1> --check-ac <index2>

# 5. Add implementation notes
backlog task edit <id> --notes $'Implemented using pattern X\nUpdated files Y and Z'

# 6. Mark done
backlog task edit <id> -s Done
```

## Usage Guidelines

1. **Always use `--plain` flag** when viewing/listing tasks for AI-readable output.
2. **Never edit task files directly** - Always use CLI commands.
3. **Use ANSI-C quoting** (`$'...\n...'`) for multi-line content (plan, notes, description).
4. **Include JIRA ticket** in title when applicable: `[TICKET-123] Description`.
5. **Mark ACs complete** as you work through them.
6. **Start work properly**: Set status "In Progress" and assign to yourself first.

## Error Handling

- Check task exists: `backlog task <id> --plain`.
- List all tasks if ID unknown: `backlog task list --plain`.
- Use search for keywords: `backlog search "<topic>" --plain`.
- For AC operations, verify AC index with `backlog task <id> --plain`.

Full help: `backlog --help`.

## Best Practices

### Writing Good Tasks

**Title**: Clear, concise, action-oriented.

```bash
# ✅ Good
backlog task create "Implement user authentication"
backlog task create "Fix memory leak in image processor"

# ❌ Bad
backlog task create "Users"
backlog task create "There's a problem with the app"
```

**Description**: Explain the "why" and context.

```bash
backlog task create "Add rate limiting to API" \
  -d "Current API has no rate limiting, causing server overload during peak hours. Need to implement per-user rate limiting to prevent abuse."
```

**Acceptance Criteria**: Focus on outcomes, not implementation.

```bash
# ✅ Good - Testable outcomes
--ac "API rejects requests after 100 requests per minute per user"
--ac "User receives clear error message when rate limited"
--ac "Rate limit resets after 60 seconds"

# ❌ Bad - Implementation details
--ac "Add a rate limiter middleware"
--ac "Use Redis for tracking"
```

### Task Organization

**Use Labels Effectively**

```bash
# Organize by type, area, and priority
backlog task create "Fix login bug" -l bug,urgent,auth
backlog task create "Optimize queries" -l enhancement,backend,performance
backlog task create "Update docs" -l documentation,frontend
```

**Use Tags for Metadata**

```bash
# Tags for filtering and organization
--tag "sprint:23"
--tag "epic:user-management"
--tag "team:backend"
```

### Definition of Done

**A task is Done only when ALL of these are complete:**

1. ✅ All acceptance criteria checked: `--check-ac <index1> --check-ac <index2> ...`
2. ✅ Implementation notes added: `--notes "..."`
3. ✅ Status set to Done: `-s Done`.

**Never mark task as Done without completing ALL items.**

## Command Reference

### Core Commands

```bash
# Tasks
backlog task create <title> [options]
backlog task list [filters] --plain
backlog task <id> --plain
backlog task edit <id> [options]
backlog task archive <id>
backlog task demote <id>

# Search
backlog search <query> [filters] --plain

# Board & Reports
backlog board
backlog browser
backlog report --output <file>

# Documents
backlog doc create <title>
backlog doc list --plain
backlog doc edit <id>

# Decisions
backlog decision create <title>
backlog decision list --plain
backlog decision <id> --plain
```

### Common Options

```bash
# Task creation/editing
-t, --title           Task title
-d, --description     Task description
-s, --status          Status (To Do, In Progress, Done, Blocked)
-a, --assignee        Assignee (@username)
-l, --labels          Comma-separated labels
--priority            Priority (low, medium, high)
--ac                  Add acceptance criterion
--check-ac            Check AC by index
--uncheck-ac          Uncheck AC by index
--remove-ac           Remove AC by index
--plan                Implementation plan
--notes               Implementation notes
--append-notes        Append to notes
--dep                 Add dependency (task-id)
--draft               Create as draft
-p, --parent          Parent task ID

# Filters
--plain               Plain text output (AI-friendly)
--status              Filter by status
--assignee            Filter by assignee
--tag                 Filter by tag
--priority            Filter by priority
--type                Filter by type (task, doc, decision)
```

## Tips

1. **Always use `--plain`** when listing or viewing for AI processing.
2. **Start tasks properly**: Set In Progress and assign to yourself.
3. **Check AC as you go**: Don't wait until end to mark them complete.
4. **Use multiline properly**: Use `$'...\n...'` syntax for newlines.
5. **Multiple flags work**: `--check-ac <index1> --check-ac <index2>`.
6. **Organize with labels**: Use consistent labeling scheme.
7. **Atomic tasks**: One PR = One task.
8. **PR-ready notes**: Format notes as GitHub PR description.
9. **Never edit files directly**: Always use CLI commands.
10. **Search is fuzzy**: "auth" finds "authentication".