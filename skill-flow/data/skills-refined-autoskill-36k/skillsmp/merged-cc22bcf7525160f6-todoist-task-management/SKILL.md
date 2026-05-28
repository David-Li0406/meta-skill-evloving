---
name: todoist-task-management
description: Use this skill to manage tasks, projects, labels, and comments in Todoist via the CLI or REST API. Ideal for adding, completing, listing tasks, and organizing projects.
---

# Todoist Task Management

This skill provides access to Todoist for managing tasks, projects, labels, and comments.

## Setup Required

1. **Get your API token:**
   - Go to Todoist Settings → Integrations → Developer
   - Or visit: [Todoist API Token](https://todoist.com/app/settings/integrations/developer)
   - Copy your API token.

2. **Set as environment variable:**
   ```bash
   export TODOIST_API_TOKEN="your-api-token"
   ```

## When to Use

Use this skill when the user:
- Asks about their tasks, TODOs, or what they need to do.
- Wants to add a new task or reminder.
- Asks about completed tasks or productivity.
- Wants to organize projects or sections.
- Mentions "Todoist" or their task list.

## CLI Commands

### Tasks

- **Show today's tasks:**
  ```bash
  todoist today
  ```

- **List all tasks:**
  ```bash
  todoist tasks
  ```

- **Add a task:**
  ```bash
  todoist add "Task name" --due "tomorrow" --priority 2
  ```

- **Complete a task:**
  ```bash
  todoist done <task_id>
  ```

- **Update a task:**
  ```bash
  todoist update <task_id> --due "next week"
  ```

- **Delete a task:**
  ```bash
  todoist delete <task_id>
  ```

### Projects

- **List projects:**
  ```bash
  todoist projects
  ```

- **Add a project:**
  ```bash
  todoist project-add "New Project"
  ```

- **Update a project:**
  ```bash
  todoist update-project <project_id> --name "Updated Project"
  ```

- **Delete a project:**
  ```bash
  todoist delete-project <project_id>
  ```

### Labels

- **List labels:**
  ```bash
  todoist labels
  ```

- **Add a label:**
  ```bash
  todoist label-add "urgent"
  ```

- **Delete a label:**
  ```bash
  todoist delete-label <label_id>
  ```

### Comments

- **List comments on a task:**
  ```bash
  todoist comments <task_id>
  ```

- **Add a comment:**
  ```bash
  todoist comment <task_id> "Comment text"
  ```

- **Delete a comment:**
  ```bash
  todoist delete-comment <comment_id>
  ```

## Filter Syntax

Todoist supports powerful filter queries:
- `today`, `tomorrow`, `overdue`
- `#project_name` - Tasks in a specific project
- `@label_name` - Tasks with a specific label
- `p1`, `p2`, `p3`, `p4` - Priority levels

Combine filters using `&` (and) or `|` (or):
```bash
todoist tasks --filter "today & #Work"
```

## Notes

- All commands return JSON. Use `jq` for formatting.
- Task IDs are numeric strings (e.g., "8765432109").
- API rate limit: 1000 requests per 15 minutes per user.
- Due strings support natural language in multiple languages.

## Sources

- [Todoist REST API Reference](https://developer.todoist.com/rest/v2/)
- [Find your API token](https://www.todoist.com/help/articles/find-your-api-token-Jpzx9IIlB)