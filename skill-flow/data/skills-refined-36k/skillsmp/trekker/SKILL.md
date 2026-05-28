---
name: trekker
description: Persistent task memory for AI agents across sessions
version: 0.3.1
---

# Trekker - Issue Tracker for AI Agents

Trekker provides persistent task memory across sessions. Unlike TodoWrite which is conversation-scoped, trekker stores tasks in a SQLite database that survives context resets.

## Quick Reference

**Run `trekker quickstart` for the complete command reference and workflow guide.**

---

## When to Use Trekker vs TodoWrite

| Aspect | Trekker | TodoWrite |
|--------|---------|-----------|
| Scope | Multi-session | Single-session |
| Persistence | SQLite database | Conversation-scoped |
| Best for | Complex projects, dependencies | Linear checklists |

**Decision rule**: "Will I need this context tomorrow?" If yes, use Trekker.

---

## Strict Usage Rules

### CRITICAL: Skills vs CLI Commands

**Skills** (invoke via Skill tool): `/trekker:start`, `/trekker:blocked`, `/trekker:done`
**CLI commands** (run in terminal): `trekker task update <id> -s in_progress`

| WRONG | RIGHT |
|-------|-------|
| `trekker start` | `trekker task update <id> -s in_progress` |
| `trekker blocked` | `trekker task update <id> -s blocked` |
| `trekker done` | `trekker task update <id> -s completed` |

**Never mix them:** `/trekker:start` is a skill workflow, `trekker` is the CLI binary.

### MUST DO

1. **Search before starting new work** - recall past decisions and avoid duplicate effort
2. **Set status `in_progress` before starting work** on any task
3. **Add summary comment before marking `completed`**
4. **Search before creating** - avoid duplicates
5. **One task `in_progress` at a time** - complete current work first
6. **Use `--toon` flag** for programmatic output to save tokens
7. **Reference tasks by ID** (e.g., TREK-1, EPIC-1) in discussions
8. **Add checkpoint comment before context reset** with: what's done, what's next, files modified
9. **Write meaningful descriptions** - tasks without context are useless to future sessions

### MUST NOT DO

1. **Never invent task IDs** - only use IDs returned by trekker commands
2. **Never overwrite without confirmation** - always show current state before update
3. **Never mark complete without summary** - future sessions depend on this context
4. **Never skip dependency checks** - verify blockers are resolved first
5. **Never assume task exists** - verify with `trekker task show <id>` first
6. **Never delete without explicit user request** - prefer `archived` status

### When to Create Issues

**CREATE** when:
- Work spans multiple sessions
- Task has dependencies or subtasks
- User explicitly requests tracking
- Bug or feature needs documented investigation
- Work needs to be handed off to another session

**DO NOT CREATE** when:
- Task is trivial (< 1 minute)
- User explicitly declines
- Just exploring or brainstorming
- One-off question or clarification

---

## Essential Workflow

### Session Start (Context Recovery)

**ALWAYS run these commands at session start** to understand what's happening:

```bash
# 1. What's currently being worked on?
trekker --toon task list --status in_progress

# 2. What changed recently? (audit trail)
trekker history --limit 10

# 3. Full picture of active work
trekker list --type task --status todo,in_progress --sort priority:asc

# 4. Get context from comments on active tasks
trekker comment list <task-id>
```

**Why context recovery matters:**
- You don't remember previous sessions - history restores that context
- Audit log shows WHO changed WHAT and WHEN
- Prevents duplicate work and conflicting changes
- Reveals decisions made by other agents or past sessions

### Starting New Work (Search First)

**ALWAYS search before starting new tasks** to recall past decisions, avoid duplicate work, and build on existing context:

```bash
# Search for related past work
trekker search "authentication"
trekker search "login bug"

# Check completed tasks for context
trekker --toon task list --status completed
```

**Why search matters:**
- Past tasks contain solutions and decisions you've forgotten
- Avoid re-investigating already-solved problems
- Find related code changes and file locations
- Build on previous work instead of starting from scratch

### Working on Tasks

```bash
# Start a task
trekker task update <task-id> -s in_progress

# Document progress
trekker comment add <task-id> -a "claude" -c "Progress: ..."

# Complete with summary
trekker comment add <task-id> -a "claude" -c "Summary: ..."
trekker task update <task-id> -s completed
```

### Before Context Reset

```bash
trekker comment add <task-id> -a "claude" -c "Checkpoint: done X. Next: Y. Files: a.ts, b.ts"
```

### Completing Epics (Keep Board Clean)

When all tasks in an epic are done, use `epic complete` to archive everything at once:

```bash
# Complete epic and archive all its tasks/subtasks
trekker epic complete <epic-id>
```

**Why this matters:**
- Keeps kanban board focused on active work
- Archived tasks remain searchable but don't clutter views
- Single command vs manually archiving each task

**When to use:**
- All tasks under the epic are completed
- Feature/milestone is fully delivered
- User confirms epic is done

---

## Key Commands

| Command | Purpose |
|---------|---------|
| `trekker task create -t "Title"` | Create task |
| `trekker task list [--status X]` | List tasks |
| `trekker task show <id>` | Show details |
| `trekker task update <id> -s <status>` | Update status |
| `trekker comment add <id> -a "claude" -c "..."` | Add comment |
| `trekker dep add <id> <depends-on>` | Add dependency |
| `trekker search "<query>"` | Full-text search |
| `trekker history [--entity <id>]` | View audit log of changes |
| `trekker list [--type X] [--sort Y]` | Unified view with filters |
| `trekker epic complete <epic-id>` | Complete epic & archive all tasks |

**Need more details?** Run `trekker quickstart` for full command syntax and examples.

---

## History & Audit Trail (Critical for Context)

Use `trekker history` to understand what happened in past sessions:

```bash
# Recent changes across all entities
trekker history --limit 20

# Changes to a specific task
trekker history --entity TREK-1

# Only task updates (filter by type)
trekker history --type task --action update

# Changes since a specific date
trekker history --since 2025-01-15 --limit 30

# Filter by action type
trekker history --action create,update --limit 15
```

**When to use history:**
- Session start - understand recent activity
- Before modifying a task - see its change trail
- Debugging conflicts - who changed what when
- Resuming work - recall context from previous sessions

---

## List Command (Comprehensive Views)

Use `trekker list` for unified views across epics, tasks, and subtasks:

```bash
# All active items, prioritized
trekker list --status todo,in_progress --sort priority:asc

# Critical and high priority work
trekker list --priority 0,1 --sort priority:asc

# Only tasks (no epics/subtasks)
trekker list --type task --status todo

# Sort by creation date (newest first)
trekker list --sort created:desc --limit 20

# Alphabetical by title
trekker list --sort title:asc
```

**Pro tip:** Combine filters for focused views:
```bash
trekker list --type task --status in_progress --priority 0,1,2
```

---

## Status Values

Tasks: `todo`, `in_progress`, `completed`, `wont_fix`, `archived`

## Priority Scale

0=critical, 1=high, 2=medium (default), 3=low, 4=backlog, 5=someday

---

## Task Quality Requirements (MANDATORY)

Future sessions depend entirely on what you write. Low-quality tasks waste time.

### Task Titles - Be Specific

| BAD (vague) | GOOD (actionable) |
|-------------|-------------------|
| "Fix bug" | "Fix null pointer in UserService.getById when user not found" |
| "Add feature" | "Add email validation to registration form with RFC 5322 regex" |
| "Update code" | "Refactor PaymentProcessor to use strategy pattern for providers" |
| "Work on auth" | "Implement JWT refresh token rotation with 7-day expiry" |

### Task Descriptions - Provide Context

Every task MUST have a description (`-d` flag) that answers:
- **What**: What exactly needs to be done?
- **Why**: Why is this needed? What problem does it solve?
- **Where**: Which files/components are involved?

```bash
# BAD
trekker task create -t "Fix login"

# GOOD
trekker task create -t "Fix login failure when password contains special chars" \
  -d "Users with & or < in passwords get 500 error. Issue in auth/validator.ts line 42. Need to escape before SQL query."
```

### Comments - Be Detailed

| BAD | GOOD |
|-----|------|
| "Working on it" | "Progress: Added input sanitization to validator.ts. Testing edge cases next." |
| "Done" | "Summary: Fixed by escaping special chars in sanitizePassword(). Added tests in validator.test.ts. Verified with manual testing." |
| "Stuck" | "Blocked: Need DB admin access to verify fix in staging. Contacted @ops in Slack." |

---

## Multi-Instance Safety

Trekker uses SQLite with Write-Ahead Logging (WAL) for concurrent access.

**Best practices:**
- Always fetch latest state before updates: `trekker task show <id>`
- Use comments for coordination between instances
- Prefer additive operations (comments) over destructive ones (delete)
- If conflict detected, refresh and retry
