---
name: taskwarrior-management
description: Use this skill for managing tasks with Taskwarrior, including adding, listing, completing, modifying, and filtering tasks, as well as time tracking and organizing work items.
---

# Taskwarrior Task Management

You are helping the user manage their tasks using Taskwarrior (the `task` command).

## Core Principles

1. Always show the user what commands you're running.
2. Display task output clearly so the user can see their tasks.
3. Use Taskwarrior's built-in formatting - don't try to reformat the output.
4. Confirm successful operations with the user.

## Common Operations

### Adding Tasks

```bash
# Basic task
task add "<task_description>"

# With priority (H=High, M=Medium, L=Low)
task add "<task_description>" priority:H

# With due date
task add "<task_description>" due:<date>

# With project
task add "<task_description>" project:<project_name>

# With tags
task add "<task_description>" +<tag1> +<tag2>

# Combined
task add "<task_description>" project:<project_name> priority:H due:<date> +<tag>
```

### Listing Tasks

```bash
# List all pending tasks
task list

# List all tasks (including completed)
task all

# Filter by project
task project:<project_name> list

# Filter by tag
task +<tag> list

# Filter by status
task status:pending list
task status:completed list

# Next most important task
task next

# Custom reports
task overdue
task waiting
task blocked
```

### Completing Tasks

```bash
# Complete by ID
task <task_id> done

# Complete multiple tasks
task <task_ids> done
```

### Modifying Tasks

```bash
# Modify description
task <task_id> modify "<new_description>"

# Add/change priority
task <task_id> modify priority:H

# Add/change due date
task <task_id> modify due:<date>

# Add to project
task <task_id> modify project:<project_name>

# Add tags
task <task_id> modify +<tag1> +<tag2>

# Remove tags
task <task_id> modify -<tag>
```

### Deleting and Managing

```bash
# Delete a task
task <task_id> delete

# Start/stop a task (time tracking)
task <task_id> start
task <task_id> stop

# Annotate a task (add notes)
task <task_id> annotate "<note>"

# Set task as waiting
task <task_id> modify wait:<date>
```

### Searching and Filtering

```bash
# Search descriptions
task /<keyword>/ list

# Complex filters
task project:<project_name> and +<tag> list
task due.before:<date> list  # end of week
task priority:H list
```

### Context Management

```bash
# Define a context (filter preset)
task context define <context_name> project:<project_name>

# List contexts
task context list

# Set active context
task context <context_name>

# Clear context
task context none

# Show current context
task context show
```

### Information and Reports

```bash
# Show task details
task <task_id> info

# Show summary
task summary

# Show burndown
task burndown.daily

# Show statistics
task stats
```

## Someday/Maybe Workflow

**Two tiers:**
- **Committed** (no tag): Active work, 10-20 tasks.
- **Aspirational** (`+someday`): Learning, research, ideas, 50-150 tasks.

```bash
# Adding
task add "<task_description>" project:<project_name> priority:H    # Committed
task add "<task_description>" +someday +<tag>                     # Aspirational

# Promoting
task <task_id> modify -someday                                     # Ready to commit
```

## Time Tracking

```bash
task <task_id> start               # Start working
task active                         # See what's active
task <task_id> stop                # Stop when done
task timesheet week                 # View time summary
```

## Best Practices

1. **IDs change**: Task IDs can change as tasks are completed/deleted. Always list tasks first to get current IDs.
2. **Confirm before bulk operations**: When deleting or modifying multiple tasks, show the user what will be affected first.
3. **Use filters wisely**: Help users create effective filters to find tasks quickly.
4. **Contexts are powerful**: Suggest setting up contexts for common work modes (work, personal, urgent, etc.).
5. **Date helpers**: Taskwarrior supports many date formats:
   - `today`, `tomorrow`, `yesterday`
   - `eow`, `eom`, `eoq`, `eoy` (end of week/month/quarter/year)
   - `soww`, `somw` (start of work week/month)
   - Relative: `5days`, `2weeks`, `1month`
   - ISO format: `2025-12-31`

## Error Handling

- If a command fails, explain why and suggest corrections.
- If no tasks match a filter, let the user know.
- If task IDs are invalid, list current tasks to help the user find the right ID.

## Example Workflow

When the user asks to manage tasks:

1. Show them their current tasks first (if relevant).
2. Execute their requested operation.
3. Show the updated state.
4. Confirm success.

Example:
```
User: "Add a high priority task to fix the login bug"
1. Run: task add "Fix login bug" priority:H +bug
2. Show the output (new task created).
3. Optionally run: task list to show the updated list.
```