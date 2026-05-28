---
name: taskwarrior
description: Command-line task management with TaskWarrior. Use when user mentions tasks, todos, adding tasks, listing tasks, task priorities, time tracking, or managing work items. Covers essential commands, filtering, time tracking, and the someday/maybe workflow for separating committed from aspirational work.
---

# TaskWarrior

Command-line task manager focused on time tracking and two-tier task organization.

## Essential Commands

```bash
t list -someday           # Actionable tasks (default view)
t add "Task" project:name priority:H
t 15 done                 # Mark complete
t 23 start                # Begin time tracking
t 23 stop                 # End time tracking
t timesheet week          # View time spent
```

## Filtering

```bash
# By commitment level
t list -someday                 # Committed work
t list +someday                 # Aspirational (browse when capacity)
t list +today                   # Today's focus

# By project/priority
t list project:flashbots
t list -someday priority:H

# By date
t list due.before:eow           # Due this week
t overdue                       # Past due
```

## Someday/Maybe Workflow

**Two tiers:**
- **Committed** (no tag): Active work, 10-20 tasks
- **Aspirational** (`+someday`): Learning, research, ideas, 50-150 tasks

```bash
# Adding
t add "Finish visa" project:visa priority:H    # Committed
t add "Learn Rust" +someday +learning          # Aspirational

# Promoting
task 42 modify -someday                        # Ready to commit
```

## Time Tracking

```bash
t 42 start               # Start working
t active                 # See what's active
t 42 stop                # Stop when done
t timesheet week         # View time summary
```

## AI Interface

Use `taskai` for reads (clean output), `task` for writes:

```bash
taskai list -someday | grep "project"
taskai overdue
```

## Modifications

```bash
task 102 modify project:test priority:H     # Single task
task 102 103 104 modify +someday            # Multiple tasks
echo "all" | task +learning modify +someday # Bulk with confirmation bypass
```

For configuration, troubleshooting, and backup procedures, see [detailed.md](references/detailed.md).
