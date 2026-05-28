---
name: task-management
description: Project-level task management with YAML storage. Use when adding/tracking tasks, managing work items, creating to-dos, generating task views, linking tasks to plans/phases, or using /task and /tasks commands. Stores tasks in .claude/tasks/ with auto-archive on completion.
version: 1.0.0
---

# Task Management

Persistent project-level task tracking with YAML storage and markdown views.

## Quick Start

```bash
# Add task
node .claude/skills/task-management/scripts/task-cli.cjs add "Task title" --priority high --effort M

# List tasks
node .claude/skills/task-management/scripts/task-cli.cjs list --status pending

# Work on task (sets in_progress)
node .claude/skills/task-management/scripts/task-cli.cjs work t-001

# Complete task (auto-archives)
node .claude/skills/task-management/scripts/task-cli.cjs complete t-001 --notes "Done"

# Generate markdown view
node .claude/skills/task-management/scripts/task-cli.cjs view
```

## Slash Commands

- `/task add <title>` - Create new task
- `/task <id>` - View task details
- `/tasks` - List all tasks
- `/tasks pending` - Filter by status

## Storage

Tasks stored in `.claude/tasks/tasks.yaml`. Completed tasks auto-move to `archive/{YYMMDD}-batch.yaml`.

## Task Fields

**Required:** id, title, status, created

**Optional:** description, priority (low/medium/high/critical), effort (S/M/L/XL), tags, assignee, due_date, context, progress, blocks, blocked_by, custom

## References

- `references/cli-reference.md` - Full CLI command reference
- `references/schema.md` - Complete task schema documentation
- `references/workflow.md` - Task workflow and best practices
