---
name: autonomous-task-execution
description: Use this skill when you want to execute long-running tasks that require multiple sessions to complete, managing task decomposition, progress tracking, and autonomous execution.
---

# Autonomous Task Execution

Execute complex, long-running tasks across multiple sessions using a dual-agent pattern (Initializer + Executor) with automatic session continuation.

## Quick Start

Use the `run-session.sh` script to manage autonomous tasks:

```bash
# Start a new autonomous task
~/.codex/skills/autonomous-task-execution/scripts/run-session.sh "Task description"

# Continue an existing task
~/.codex/skills/autonomous-task-execution/scripts/run-session.sh --task-name <task-name> --continue

# List all tasks and their progress
~/.codex/skills/autonomous-task-execution/scripts/run-session.sh --list

# Show help
~/.codex/skills/autonomous-task-execution/scripts/run-session.sh --help
```

## Directory Structure

All task data is stored in `.autonomous/<task-name>/` under the project root:

```text
project-root/
└── .autonomous/
    ├── <task-name>/
    │   ├── task_list.md        # Master task checklist
    │   ├── progress.md         # Session-by-session notes
    │   ├── session.id          # Last session ID for resumption
    │   └── session.log         # JSON Lines output from sessions
    └── ...
```

This allows multiple autonomous tasks to run in parallel without conflicts.

## Workflow Overview

```text
User Request → Generate Task Name → Create .autonomous/<task-name>/ → Execute Sessions
```

## Script Options

```text
Usage:
  run-session.sh "task description"           Start new task (auto-generates name)
  run-session.sh --task-name <name> --continue Continue specific task
  run-session.sh --list                        List all tasks
  run-session.sh --help                        Show help

Options:
  --task-name <name>       Specify task name explicitly
  --continue, -c           Continue existing task
  --no-auto-continue       Don't auto-continue after session
  --max-sessions N         Limit to N sessions
  --list                   List all existing tasks
  --resume-last            Resume the most recent session
  --network                Enable network access (uses danger-full-access sandbox)
```

## Important Notes

1. **Task Isolation**: Each task has its own directory, preventing conflicts.
2. **Task Naming**: Auto-generated from description (lowercase, hyphens, max 30 chars).
3. **Task List is Sacred**: Never delete or modify task descriptions, only mark `[x]`.
4. **One Task at a Time per Session**: Focus on completing tasks thoroughly.
5. **Auto-Continue**: Sessions auto-continue with a 3-second delay; Ctrl+C to pause.
6. **Session Resumption**: Use `--resume-last` to preserve conversation context.
7. **Network Mode**: `--network` uses `--dangerously-bypass-approvals-and-sandbox`; only use in an isolated environment.

## Usage Examples

### Example 1: Start New Task

```bash
~/.codex/skills/autonomous-task-execution/scripts/run-session.sh "Build a REST API for todo app"
```

### Example 2: Continue Existing Task

```bash
~/.codex/skills/autonomous-task-execution/scripts/run-session.sh --task-name <task-name> --continue
```

### Example 3: List All Tasks

```bash
~/.codex/skills/autonomous-task-execution/scripts/run-session.sh --list
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Task not found | Run `--list` to see existing tasks |
| Multiple tasks | Specify task name with `--task-name` |
| Session stuck | Check `session.log` in task directory |
| Need to restart | Delete task directory and start fresh |
| Resume failed | Remove `session.id` to start fresh session |