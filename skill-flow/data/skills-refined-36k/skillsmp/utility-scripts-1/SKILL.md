---
name: utility-scripts
description: |
  Comprehensive guide to teamwork script usage patterns for project, task, and wave management.
  Use this skill to understand available scripts, their parameters, and common usage patterns.
---

# Utility Scripts

## What is SCRIPTS_PATH?

`SCRIPTS_PATH` is the expanded absolute path to teamwork scripts.

Your prompt includes it like this:
```
SCRIPTS_PATH: /Users/name/.claude/plugins/cache/hardworker-marketplace/teamwork/0.20.0/src/scripts
```

Use this path to call Bun scripts.

## Core Rules

1. **JSON via scripts, Markdown via Read** - Always use scripts to access JSON data
2. **Always pass `--project` and `--team`** - Required for all teamwork scripts
3. **Use `$SCRIPTS_PATH` variable** - Reference the scripts directory passed in your prompt

## Project Management Scripts

### project-create.js

Create a new teamwork project with metadata.

```bash
bun "$SCRIPTS_PATH/project-create.js" \
  --project <name> \
  --team <name> \
  --goal "Project goal description"
```

### project-get.js

Retrieve project metadata.

```bash
bun "$SCRIPTS_PATH/project-get.js" \
  --project <name> \
  --team <name>
```

### project-status.js

Get comprehensive project status dashboard.

```bash
# Table format (default)
bun "$SCRIPTS_PATH/project-status.js" \
  --project <name> \
  --team <name> \
  --format table

# JSON format
bun "$SCRIPTS_PATH/project-status.js" \
  --project <name> \
  --team <name> \
  --format json

# Extract specific field using dot notation
bun "$SCRIPTS_PATH/project-status.js" \
  --project <name> \
  --team <name> \
  --field stats.progress

# Verbose output with task details
bun "$SCRIPTS_PATH/project-status.js" \
  --project <name> \
  --team <name> \
  --verbose
```

## Task Management Scripts

### task-create.js

Create a new task with dependencies.

```bash
bun "$SCRIPTS_PATH/task-create.js" \
  --project <name> \
  --team <name> \
  --id "1" \
  --title "Task title" \
  --description "Task description" \
  --role backend \
  --complexity standard \
  --blocked-by "2,3"
```

**Complexity values**: `simple` | `standard` | `complex`
**Role values**: `frontend` | `backend` | `devops` | `test` | `docs` | `security` | `review` | `worker`

### task-get.js

Get single task details.

```bash
bun "$SCRIPTS_PATH/task-get.js" \
  --project <name> \
  --team <name> \
  --id "1"
```

### task-list.js

List tasks with optional filtering.

```bash
# List all tasks
bun "$SCRIPTS_PATH/task-list.js" \
  --project <name> \
  --team <name> \
  --format json

# List available tasks (status=open, no blocker, not claimed)
bun "$SCRIPTS_PATH/task-list.js" \
  --project <name> \
  --team <name> \
  --available

# Filter by role
bun "$SCRIPTS_PATH/task-list.js" \
  --project <name> \
  --team <name> \
  --available \
  --role backend
```

### task-claim.js

Atomically claim a task with optimistic concurrency control.

```bash
# Claim with explicit owner
bun "$SCRIPTS_PATH/task-claim.js" \
  --project <name> \
  --team <name> \
  --id "1" \
  --owner ${CLAUDE_SESSION_ID}

# Auto-detect owner from CLAUDE_SESSION_ID
bun "$SCRIPTS_PATH/task-claim.js" \
  --project <name> \
  --team <name> \
  --id "1"
```

### task-update.js

Update task status, evidence, or metadata.

```bash
# Add simple evidence
bun "$SCRIPTS_PATH/task-update.js" \
  --project <name> \
  --team <name> \
  --id "1" \
  --add-evidence "Created src/middleware/auth.ts"

# Update status
bun "$SCRIPTS_PATH/task-update.js" \
  --project <name> \
  --team <name> \
  --id "1" \
  --status resolved

# Update metadata (title, description, role)
bun "$SCRIPTS_PATH/task-update.js" \
  --project <name> \
  --team <name> \
  --id "1" \
  --title "New task title" \
  --description "Updated description" \
  --role frontend

# Mark resolved with evidence
bun "$SCRIPTS_PATH/task-update.js" \
  --project <name> \
  --team <name> \
  --id "1" \
  --status resolved \
  --add-evidence "npm test: 5/5 passed, exit 0"

# Release task (clear claimed_by)
bun "$SCRIPTS_PATH/task-update.js" \
  --project <name> \
  --team <name> \
  --id "1" \
  --release
```

**Status values**: `open` | `in_progress` | `resolved`

## Wave Management Scripts

### wave-calculate.js

Calculate wave groupings from task dependencies using topological sort.

```bash
bun "$SCRIPTS_PATH/wave-calculate.js" \
  --project <name> \
  --team <name>
```

### wave-status.js

Query wave progress and status.

```bash
# JSON format (default)
bun "$SCRIPTS_PATH/wave-status.js" \
  --project <name> \
  --team <name> \
  --format json

# Table format
bun "$SCRIPTS_PATH/wave-status.js" \
  --project <name> \
  --team <name> \
  --format table
```

### wave-update.js

Update wave status.

```bash
bun "$SCRIPTS_PATH/wave-update.js" \
  --project <name> \
  --team <name> \
  --wave 1 \
  --status in_progress
```

**Wave status values**: `planning` | `in_progress` | `completed` | `verified` | `failed`

## Common Patterns

### Worker Task Execution Flow

```bash
# 1. List available tasks for your role
bun "$SCRIPTS_PATH/task-list.js" --project <name> --team <name> --available --role backend

# 2. Claim a task
bun "$SCRIPTS_PATH/task-claim.js" --project <name> --team <name> --id "1" --owner ${CLAUDE_SESSION_ID}

# 3. Update status to in_progress
bun "$SCRIPTS_PATH/task-update.js" --project <name> --team <name> --id "1" --status in_progress

# 4. Collect evidence during implementation
bun "$SCRIPTS_PATH/task-update.js" --project <name> --team <name> --id "1" \
  --add-evidence "Created src/feature.ts"

# 5. Mark resolved with final evidence
bun "$SCRIPTS_PATH/task-update.js" --project <name> --team <name> --id "1" \
  --status resolved \
  --add-evidence "npm test: all tests passed"
```

### Orchestrator Monitoring Flow

```bash
# 1. Get project status
bun "$SCRIPTS_PATH/project-status.js" --project <name> --team <name>

# 2. Check wave status
bun "$SCRIPTS_PATH/wave-status.js" --project <name> --team <name>

# 3. Get specific task details if needed
bun "$SCRIPTS_PATH/task-get.js" --project <name> --team <name> --id "1"
```

## Error Handling

All scripts follow consistent error patterns:

- Exit code 0: Success
- Exit code 1: Error (details in stderr)
- JSON output: Success data to stdout
- Error messages: Always to stderr

## Quick Reference

| Operation | Script | Key Parameters |
|-----------|--------|----------------|
| Get project info | `project-get.js` | `--project <name> --team <name>` |
| Get project status | `project-status.js` | `--project <name> --team <name> [--format json\|table]` |
| List available tasks | `task-list.js` | `--project <name> --team <name> --available` |
| Get task details | `task-get.js` | `--project <name> --team <name> --id <id>` |
| Claim task | `task-claim.js` | `--project <name> --team <name> --id <id> --owner <session_id>` |
| Update task | `task-update.js` | `--project <name> --team <name> --id <id> [--status <status>] [--add-evidence "..."]` |
| Check waves | `wave-status.js` | `--project <name> --team <name>` |
| Calculate waves | `wave-calculate.js` | `--project <name> --team <name>` |
