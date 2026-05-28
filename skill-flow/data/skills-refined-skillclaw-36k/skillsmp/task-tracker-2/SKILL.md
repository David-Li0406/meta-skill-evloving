---
name: task-tracker
description: Track tasks and subtasks in .claude/tasks/ for context preservation. Use when planning multi-step work, tracking progress, or resuming interrupted sessions.
---

# Task Tracker

**Skill base directory:** `{baseDir}`

Persist task state across LLM sessions using markdown files in `.claude/tasks/`.
Helps agents plan and remember what they're working on, and track progress through
multi-step work.

## Quick Start

Scripts are located in `{baseDir}/scripts/`. Use the full path when invoking:

```bash
# Initialize in current project
{baseDir}/scripts/task.py init

# Add tasks
{baseDir}/scripts/task.py add "Implement user authentication"
{baseDir}/scripts/task.py add "Write login tests" --parent 01-implement-user-authentication

# Work through tasks
{baseDir}/scripts/task.py start 01-implement-user-authentication
{baseDir}/scripts/task.py done
{baseDir}/scripts/task.py next
```

## Directory Structure

Tasks are stored as markdown files. The filesystem hierarchy represents task hierarchy:

```
.claude/tasks/
  01-auth-login/
    00-index.md                    # Parent task metadata
    01-create-login-form.md        # Subtask (leaf)
    02-session-management/
      00-index.md                  # Nested parent
      01-implement-jwt.md          # Leaf
      02-add-refresh-tokens.md     # Leaf
  02-deploy-staging.md             # Top-level leaf task
```

**Key rules:**
- Leaf tasks (no children) → `.md` files
- Parent tasks (have children) → directories with `00-index.md`
- Adding a subtask to a leaf automatically promotes it to a directory
- Removing the last child automatically demotes back to a file

## Task File Format

Each task is a markdown file with YAML frontmatter:

```markdown
---
status: pending
created: 2026-01-06T10:30:00+00:00
updated: 2026-01-06T11:45:00+00:00
deps:
  - 01-auth-login
approach: Use bcrypt for passwords, JWT for sessions
criteria:
  - Login endpoint returns JWT
  - Invalid creds return 401
files:
  - src/routes/auth.ts
  - src/middleware/jwt.ts
---

# Implement session management

Optional longer description here.

## Notes

### 2026-01-06T10:30:00+00:00

Discovered we need to handle token refresh.

### 2026-01-07T14:00:00+00:00

Redis cluster mode requires different client config.
```

### Statuses

| Status | Meaning |
|--------|---------|
| `pending` | Not started |
| `in_progress` | Currently working on |
| `blocked` | Waiting on external factor |
| `complete` | Done |
| `wont_do` | Cancelled/skipped |

### Planning Fields

Optional fields for AI agent context preservation:

| Field | Purpose |
|-------|---------|
| `approach` | How to implement (the plan) |
| `criteria` | What "done" means (list) |
| `files` | Where to look (list of paths) |

These help an agent resume work across sessions without re-discovering context.

## Commands

All output is JSON. Use `{baseDir}/scripts/task.py` for all commands.

### Initialize

```bash
{baseDir}/scripts/task.py init
```

Creates `.claude/tasks/` directory.

### Add Task

```bash
{baseDir}/scripts/task.py add "Task title"
{baseDir}/scripts/task.py add "Subtask title" --parent 01-parent-task
{baseDir}/scripts/task.py add "Task with deps" --deps 01-auth-login 02-database
{baseDir}/scripts/task.py add "With description" --description "Detailed info"
{baseDir}/scripts/task.py add "With approach" --approach "Use existing auth middleware"
{baseDir}/scripts/task.py add "With criteria" --criteria "Tests pass" "Docs updated"
{baseDir}/scripts/task.py add "With files" --files src/auth.ts src/middleware.ts
```

Adding a subtask to a leaf task automatically promotes it to a directory.

### Remove Task

```bash
{baseDir}/scripts/task.py remove 01-auth-login              # Remove task
{baseDir}/scripts/task.py remove 01-auth-login/02-session   # Remove subtask
```

Removing the last child of a parent automatically demotes it back to a file.

### Update Task

```bash
{baseDir}/scripts/task.py update 01-auth-login --title "New title"
{baseDir}/scripts/task.py update 01-auth-login --status complete
{baseDir}/scripts/task.py update 01-auth-login --deps 02-database
{baseDir}/scripts/task.py update 01-auth-login --approach "Changed to use Redis"
{baseDir}/scripts/task.py update 01-auth-login --criteria "Cache hits > 90%"
{baseDir}/scripts/task.py update 01-auth-login --files src/cache.ts
```

### List Tasks

```bash
{baseDir}/scripts/task.py list
{baseDir}/scripts/task.py list --status pending
{baseDir}/scripts/task.py list --status in_progress
```

### Show Task

```bash
{baseDir}/scripts/task.py show 01-auth-login
{baseDir}/scripts/task.py show 01-auth-login/02-session
```

Returns task details including dependency status.

### Get Next Task

```bash
{baseDir}/scripts/task.py next
```

Returns the next task to work on using depth-first logic:
1. If in_progress task has pending subtasks → first pending subtask
2. Otherwise → first pending task with satisfied dependencies

### Start Task

```bash
{baseDir}/scripts/task.py start 01-auth-login
```

Sets status to `in_progress` and records start time. Warns (but allows) if
dependencies incomplete.

### Complete Task

```bash
{baseDir}/scripts/task.py done                  # Current in_progress task
{baseDir}/scripts/task.py done 01-auth-login    # Specific task
```

### Block/Unblock Task

```bash
{baseDir}/scripts/task.py block 01-auth-login --reason "Waiting on API spec"
{baseDir}/scripts/task.py unblock 01-auth-login
```

### Add Note

```bash
{baseDir}/scripts/task.py note 01-auth-login "Discovered edge case X"
{baseDir}/scripts/task.py note 01-auth-login/02-session "Harder than expected"
```

Attach learnings, context, or decisions to a task. Notes are timestamped and
preserved for future sessions.

### View All Notes

```bash
{baseDir}/scripts/task.py notes
```

Returns all notes chronologically across all tasks - a project journal showing
what you learned over time.

### Move Task

```bash
{baseDir}/scripts/task.py move 01-auth-login/03-feature --parent 02-backend
{baseDir}/scripts/task.py move 02-backend/01-api                             # Move to top level
```

Moves a task to a new location and updates any dependency references.

## Dependencies

Tasks can depend on other tasks by path:

```bash
{baseDir}/scripts/task.py add "Deploy" --deps 01-auth-login 02-database-setup
```

Dependencies are soft-blocking:
- `next` skips tasks with incomplete dependencies
- `start` warns but allows starting with incomplete deps

## Rendering for Humans

Use `task-render.py` to generate readable markdown:

```bash
{baseDir}/scripts/task-render.py
```

Output:
```markdown
# Tasks

## In Progress
- **01-auth-login** Implement feature
  _Approach: Use JWT tokens_
  > Discovered we need auth middleware first
  - **01-auth-login/01-create-form** Create login form

## Pending
- **02-deploy-staging** Deploy _(depends on: 01-auth-login)_

## Completed
- [x] **01-auth-login/02-session** Add session management
```

## JSON Output Format

### Success

```json
{
  "ok": true,
  "task": { ... }
}
```

### Error (exit code 1)

```json
{
  "ok": false,
  "error": "Task not found: 01-missing"
}
```

### List

```json
{
  "ok": true,
  "tasks": [ ... ],
  "count": 5
}
```

## Typical Workflow

1. **Starting a session**: Run `{baseDir}/scripts/task.py next` to see what to work on
2. **Resuming after time away**: Run `{baseDir}/scripts/task.py notes` to review learnings
3. **Beginning work**: Run `{baseDir}/scripts/task.py start <id>` on the task
4. **Breaking down work**: Add subtasks with `--parent`
5. **Capturing learnings**: Run `{baseDir}/scripts/task.py note <id> "text"` when you discover something
6. **Completing**: Run `{baseDir}/scripts/task.py done` when finished
7. **Repeat**: Run `{baseDir}/scripts/task.py next` for the next task

## References

For more detailed guidance, use the Read tool to load:
- `{baseDir}/references/markdown-format.md` - The task file format specification
- `{baseDir}/references/project-breakdown.md` - How to decompose projects into atomic tasks
