---
name: using-prog
description: Use for all task management - prog is the primary system for tracking work across sessions; use TodoWrite only for quick single-message tasks
---

# Task Management with prog

## Overview

**prog is your primary task management system.** It persists across sessions, supports dependencies, and enables handoffs between agents.

```
prog = strategic, persistent, cross-session (DEFAULT)
TodoWrite = tactical, ephemeral, single-message only
```

## When to Use What

| Situation | Use |
|-----------|-----|
| Any multi-step task | prog |
| Work spanning multiple messages | prog |
| Parallel agent coordination | prog |
| Epics and related tasks | prog |
| Handoffs between sessions | prog |
| Quick breakdown of immediate work (<1 message) | TodoWrite |

**Default to prog.** Only use TodoWrite for trivial, single-message tasks where persistence adds no value.

## Session Start Protocol

On session start, you receive `prog prime` output with:
- Current project status
- In-progress tasks
- Ready tasks (unblocked)

**First action:** Review this context. Pick up in-progress work or claim a ready task.

```bash
# See what's ready
prog ready -p <project>

# Get full context on a task
prog show <id>

# Claim and start
prog start <id>
```

## Core Workflow

### 1. Starting Work

```bash
# Check project status
prog status -p myproject

# See ready tasks
prog ready -p myproject

# Read task details
prog show ts-abc123

# Start working
prog start ts-abc123
```

### 2. While Working

```bash
# Log progress (creates audit trail)
prog log ts-abc123 "Implemented login endpoint"
prog log ts-abc123 "Added input validation"

# Append context to description
prog append ts-abc123 "Decision: Using bcrypt for password hashing"

# Replace description if needed
prog desc ts-abc123 "Updated description with full context"
```

### 3. Completing Work

```bash
# Mark done
prog done ts-abc123

# Or mark blocked for next agent
prog block ts-abc123 "Need API spec from backend team"

# Or cancel if no longer needed
prog cancel ts-abc123 "Requirements changed"
```

## Creating Tasks

```bash
# Simple task
prog add "Implement user authentication" -p myproject

# High priority
prog add "Fix critical login bug" -p myproject --priority 1

# Task under an epic
prog add "Add login form" -p myproject --parent ep-abc123

# Task that blocks another
prog add "Build API endpoint" -p myproject --blocks ts-frontend

# Create an epic
prog add "Authentication system" -p myproject -e
```

## Dependencies

Use dependencies to enforce task ordering:

```bash
# Task A blocks Task B (B can't start until A is done)
prog blocks ts-taskA ts-taskB

# View dependency graph
prog graph
```

Tasks with unmet dependencies won't appear in `prog ready`.

## Integration with Other Skills

### With writing-plans

When creating implementation plans, create corresponding prog tasks:

```bash
# Create epic for the feature
prog add "User Authentication Feature" -p myproject -e
# Returns: ep-abc123

# Create tasks from plan phases
prog add "Phase 1: Database schema" -p myproject --parent ep-abc123
prog add "Phase 2: API endpoints" -p myproject --parent ep-abc123 --blocks ts-phase1
prog add "Phase 3: Frontend forms" -p myproject --parent ep-abc123 --blocks ts-phase2
```

### With executing-plans

Before starting each phase:
```bash
prog start ts-phase1
prog log ts-phase1 "Starting database schema work"
```

After completing:
```bash
prog log ts-phase1 "Schema complete, migrations tested"
prog done ts-phase1
```

### With dispatching-parallel-agents

Create separate tasks for parallel work:
```bash
prog add "Fix auth bug" -p myproject --priority 1
prog add "Fix payment bug" -p myproject --priority 1
prog add "Fix notification bug" -p myproject --priority 1
```

Each agent claims one task via `prog start`.

## Session Close Protocol

**Before ending any session:**

1. Log final progress on in-progress tasks
2. Update task status (done, blocked, or leave in-progress)
3. Add context for the next agent

```bash
# Log where you stopped
prog log ts-abc123 "Completed endpoint, tests passing. Next: add rate limiting"

# If blocked
prog block ts-abc123 "Waiting for Redis config"

# If done
prog done ts-abc123
```

## Command Reference

| Command | Description |
|---------|-------------|
| `prog status -p <project>` | Project overview |
| `prog ready -p <project>` | Tasks ready for work |
| `prog show <id>` | Task details + logs |
| `prog start <id>` | Claim task |
| `prog log <id> <msg>` | Add progress log |
| `prog append <id> <text>` | Add to description |
| `prog done <id>` | Mark complete |
| `prog block <id> <reason>` | Mark blocked |
| `prog cancel <id> [reason]` | Cancel task |
| `prog add <title> -p <proj>` | Create task |
| `prog add <title> -e` | Create epic |
| `prog blocks <id> <other>` | Add dependency |
| `prog graph` | View dependencies |

## Why prog Over TodoWrite

1. **Persistence** - Tasks survive session end, context compaction, crashes
2. **Dependencies** - Enforce task ordering, parallel-safe
3. **Audit trail** - Timestamped logs show exactly what happened
4. **Handoffs** - Next agent picks up with full context
5. **Projects** - Scope work across multiple initiatives
6. **Epics** - Group related tasks logically

## The Rule

**Use prog for everything except trivial single-message tasks.**

When in doubt, use prog. The overhead is minimal; the benefits are substantial.
