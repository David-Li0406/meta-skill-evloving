---
name: todoist-management
description: Use this skill to manage Todoist tasks, projects, labels, and comments via the `todoist` CLI.
---

# Todoist CLI Management

Manage Todoist via the REST API v2.

## Setup

1. Get API token: Todoist → Settings → Integrations → Developer → API token.
2. Set environment variable:
   ```bash
   export TODOIST_API_TOKEN="your_token_here"
   ```
3. Make CLI executable:
   ```bash
   chmod +x ~/clawd/skills/todoist/scripts/todoist
   ```

## CLI Location

```bash
~/clawd/skills/todoist/scripts/todoist
```

## Quick Reference

### Tasks

```bash
# List all tasks
todoist tasks

# List with filter
todoist tasks --filter "today"
todoist tasks --filter "overdue"
todoist tasks --filter "#Work"
todoist tasks --project PROJECT_ID

# Quick views
todoist today
todoist overdue
todoist upcoming

# Get single task
todoist task TASK_ID

# Add task
todoist add "Task description"
todoist add "Task description" --due "due date"
todoist add "Task description" --project PROJECT_ID --labels "label1,label2"

# Update task
todoist update TASK_ID --content "New title"
todoist update TASK_ID --due "new due date"

# Complete / reopen / delete
todoist complete TASK_ID
todoist reopen TASK_ID
todoist delete-task TASK_ID
```

### Projects

```bash
# List projects
todoist projects

# Create project
todoist add-project "Project Name"

# Update project
todoist update-project PROJECT_ID --name "New Name"

# Delete project
todoist delete-project PROJECT_ID
```

### Sections

```bash
# List sections
todoist sections
todoist sections PROJECT_ID

# Create section
todoist add-section --name "Section Name" --project PROJECT_ID

# Delete section
todoist delete-section SECTION_ID
```

### Labels

```bash
# List labels
todoist labels

# Create label
todoist add-label "Label Name"

# Delete label
todoist delete-label LABEL_ID
```

### Comments

```bash
# List comments
todoist comments --task TASK_ID

# Add comment
todoist add-comment "Comment text" --task TASK_ID

# Delete comment
todoist delete-comment COMMENT_ID
```

## Filter Syntax

Todoist supports powerful filter queries:

| Filter | Description |
|--------|-------------|
| `today` | Due today |
| `tomorrow` | Due tomorrow |
| `overdue` | Past due |
| `#ProjectName` | In specific project |
| `@label` | Has label |

Combine with `&` (and) or `|` (or):
```bash
todoist tasks --filter "today & #Work"
```

## Due Date Strings

Natural language due dates:
- `today`, `tomorrow`, `next week`
- `in 3 days`
- `Jan 15`, `2026-01-20`

## Priority Levels

| Value | Meaning |
|-------|---------|
| 1 | Normal (default) |
| 2 | Medium |
| 3 | High |
| 4 | Urgent |

## Output

All commands return JSON. Pipe to `jq` for formatting:

```bash
todoist tasks | jq '.[] | {id, content, due: .due.string}'
```

## Notes

- Requires `curl` and `jq`.
- All output is JSON for easy scripting.
- Task IDs and Project IDs are numeric strings.