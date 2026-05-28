---
name: todo-add
description: Manually add a new todo item to the todo list
trigger_keywords:
  - add todo
  - new todo
  - create todo
---

# Todo Add

## Purpose

Manually create a new todo item when automatic detection is not applicable or when user wants to add a personal task.

## Prerequisites

- A `Todos/` directory must exist in the knowledge base
- The `Todos/` directory should have a `RULE.md` with todo configuration
- If not exists, offer to create the directory structure

## Execution Flow

### Phase 1: Locate Todos Directory

1. Search for `Todos/` directory in the current working directory or its parents
2. If not found, search in common knowledge base locations
3. If still not found, ask user:
   ```
   "No Todos directory found. Would you like me to create one?"
   Options:
   - "Yes, create in [suggested path]"
   - "Yes, but in a different location"
   - "No, cancel"
   ```

### Phase 2: Gather Todo Information

Use AskUserQuestion to collect information:

**Question 1: Title** (required)
```json
{
  "question": "What is the todo item?",
  "header": "Todo Title",
  "options": [
    {"label": "Type your answer", "description": "Describe the task briefly"}
  ],
  "multiSelect": false
}
```

**Question 2: Priority**
```json
{
  "question": "What is the priority?",
  "header": "Priority",
  "options": [
    {"label": "High", "description": "Urgent or time-sensitive task"},
    {"label": "Medium (Recommended)", "description": "Normal priority task"},
    {"label": "Low", "description": "Can be done when time permits"}
  ],
  "multiSelect": false
}
```

**Question 3: Due Date** (optional)
```json
{
  "question": "When is this due?",
  "header": "Due Date",
  "options": [
    {"label": "No deadline", "description": "No specific due date"},
    {"label": "Today", "description": "Due by end of today"},
    {"label": "Tomorrow", "description": "Due by end of tomorrow"},
    {"label": "This week", "description": "Due by end of this week"}
  ],
  "multiSelect": false
}
```

### Phase 3: Create Todo File

1. **Generate filename**:
   - Format: `YYYY-MM-DD_[slug-from-title].md`
   - Example: `2025-01-13_reply-client-email.md`
   - Slug: lowercase, hyphens instead of spaces, max 50 chars

2. **Create file** in `Todos/active/`:

```yaml
---
title: [User provided title]
status: pending
priority: [high|medium|low]
created_at: [Current date YYYY-MM-DD]
due_date: [If provided, YYYY-MM-DD format]
source_file: null
source_type: manual
tags: []
dependencies: []
related_files: []
---

# [Title]

## Task Details

[Description if provided, otherwise leave for user to fill]

## Checklist

- [ ] [First step - user can edit]

## Execution Log

### [Current Date]
- Todo created manually
- Status: pending
- Priority: [priority]
```

### Phase 4: Update Governance

1. **Update `Todos/active/README.md`**:
   - Add new entry to the file list
   - Format: `- [filename](filename) - [title] (Priority: [priority], Due: [date or 'none'])`
   - Update "Last updated" timestamp

2. **Update `Todos/README.md`**:
   - Update active todo count
   - Add to "Recent Changes" section

### Phase 5: Report

Confirm creation with summary:

```
✅ Todo created successfully!

Title: [title]
Priority: [priority]
Due Date: [date or 'No deadline']
Location: Todos/active/[filename]

You can:
- View all todos with /todo-list
- Mark complete with /todo-complete
- Update details with /todo-update
```

## Error Handling

### No Todos Directory

If no `Todos/` directory exists:
1. Offer to create the directory structure
2. If user agrees, create:
   - `Todos/RULE.md` (with default todo governance rules)
   - `Todos/README.md` (index file)
   - `Todos/active/README.md`
   - `Todos/completed/README.md`

### Duplicate Title

If a todo with similar title exists:
1. Notify user: "A similar todo already exists: [title]"
2. Offer options:
   - "Create anyway with different name"
   - "Open existing todo"
   - "Cancel"

## Default RULE.md Template

If creating new Todos directory, use this template:

```markdown
# Todos - Personal Task Management

## Purpose

Centralized management of all todo items.

## Todo Tracking

enabled: true
todos_directory: [current path]

## Structure

Todos/
├── active/      # Active todos
└── completed/   # Completed todos

## Naming Convention

YYYY-MM-DD_todo-title-slug.md

## Allowed Operations

- Create: Allowed
- Update: Allowed (must update execution log)
- Delete: Not allowed (archive to completed/ instead)
- Move: Only between active/ and completed/
```
