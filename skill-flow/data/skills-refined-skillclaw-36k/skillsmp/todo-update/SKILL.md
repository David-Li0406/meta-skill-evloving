---
name: todo-update
description: Update todo details (priority, due date, status, notes)
trigger_keywords:
  - update todo
  - change todo
  - edit todo
  - modify todo
---

# Todo Update

## Purpose

Modify an existing todo's properties (status, priority, due date) or add execution notes and related information.

## Execution Flow

### Phase 1: Identify Todo

**If user specifies todo in command**:
- Parse the todo identifier
- Example: `/todo-update Review design docs`

**If not specified**:
1. List active todos
2. Ask user to select:
   ```json
   {
     "question": "Which todo do you want to update?",
     "header": "Select Todo",
     "options": [
       {"label": "#1 Reply to client email", "description": "High priority, due 2025-01-15"},
       {"label": "#2 Review design docs", "description": "Medium priority, in progress"},
       {"label": "#3 Update documentation", "description": "Low priority"}
     ],
     "multiSelect": false
   }
   ```

### Phase 2: Determine Update Type

Ask what to update:

```json
{
  "question": "What would you like to update?",
  "header": "Update Type",
  "options": [
    {"label": "Status", "description": "Change to pending, in_progress, or blocked"},
    {"label": "Priority", "description": "Change to high, medium, or low"},
    {"label": "Due Date", "description": "Set or change the deadline"},
    {"label": "Add Note", "description": "Add an entry to the execution log"},
    {"label": "Add Dependency", "description": "Link this todo to another todo"},
    {"label": "Add Related File", "description": "Link to a file in the knowledge base"}
  ],
  "multiSelect": true
}
```

### Phase 3: Collect New Values

Based on selection, gather the new values:

**Status Change**:
```json
{
  "question": "New status?",
  "header": "Status",
  "options": [
    {"label": "pending", "description": "Not started yet"},
    {"label": "in_progress", "description": "Currently working on this"},
    {"label": "blocked", "description": "Waiting for something else"}
  ],
  "multiSelect": false
}
```

If blocked, also ask for reason:
```
What is blocking this todo? (e.g., "Waiting for client response")
```

**Priority Change**:
```json
{
  "question": "New priority?",
  "header": "Priority",
  "options": [
    {"label": "High", "description": "Urgent or time-sensitive"},
    {"label": "Medium", "description": "Normal priority"},
    {"label": "Low", "description": "Can wait"}
  ],
  "multiSelect": false
}
```

**Due Date Change**:
```json
{
  "question": "New due date?",
  "header": "Due Date",
  "options": [
    {"label": "Remove deadline", "description": "Clear the due date"},
    {"label": "Today", "description": "Due by end of today"},
    {"label": "Tomorrow", "description": "Due by end of tomorrow"},
    {"label": "This week", "description": "Due by end of this week"},
    {"label": "Next week", "description": "Due by end of next week"}
  ],
  "multiSelect": false
}
```

**Add Note**:
```
What note would you like to add?
(This will be added to the execution log with today's date)
```

**Add Dependency**:
1. List other active todos
2. Ask user to select which one this depends on
3. Update dependencies list in frontmatter

**Add Related File**:
```
Enter the path to the related file (relative to knowledge base root):
```

### Phase 4: Update File

1. **Read current file**

2. **Update frontmatter fields**:
   ```yaml
   # Updated fields only
   status: [new status]
   priority: [new priority]
   due_date: [new date or null]
   blocking_reason: [if blocked]
   dependencies:
     - path: [new dependency path]
       status: [current status of that todo]
   related_files:
     - [new file path]
   ```

3. **Add execution log entry**:
   ```markdown
   ### [Current Date]
   - [Description of change]
   - [Field]: [old value] → [new value]
   ```

   Examples:
   ```markdown
   ### 2025-01-13
   - Priority updated
   - Priority: medium → high

   ### 2025-01-13
   - Status changed to blocked
   - Status: pending → blocked
   - Reason: Waiting for client response

   ### 2025-01-13
   - Added note: "Discussed requirements with team, need more details"
   ```

### Phase 5: Handle Status Changes

**If changed TO blocked**:
- Require blocking_reason
- Add to frontmatter

**If changed FROM blocked**:
- Clear blocking_reason
- Log unblock reason in execution log

**If changed TO in_progress**:
- Log when work started

### Phase 6: Update Governance

1. If title or priority changed, update `Todos/active/README.md`
2. Update "Last updated" timestamp

### Phase 7: Report

```
✅ Todo updated: "Review design docs"

Changes made:
- Priority: medium → high
- Due date: (none) → 2025-01-20
- Added note: "Client requested by end of week"

Current state:
- Status: pending
- Priority: high
- Due: 2025-01-20

View all todos: /todo-list
```

## Bulk Update

For updating multiple todos at once:

```json
{
  "question": "Select todos to update",
  "header": "Batch Update",
  "options": [
    {"label": "#1 Reply to client email", "description": "High priority"},
    {"label": "#2 Review design docs", "description": "Medium priority"},
    {"label": "#3 Update documentation", "description": "Low priority"}
  ],
  "multiSelect": true
}
```

Then ask what change to apply to all:
- Common use case: Change priority of multiple items
- Apply same change to all selected

## Quick Updates

Support shorthand commands:

- `/todo-update #1 priority high` → Change todo #1 to high priority
- `/todo-update "Review docs" status in_progress` → Start working on todo
- `/todo-update #2 due tomorrow` → Set due date to tomorrow

Parse these patterns and skip confirmation if unambiguous.

## Error Handling

### Todo Not Found

```
Todo not found: "[search term]"

Active todos:
1. Reply to client email
2. Review design docs

Try again with the correct title or number.
```

### Invalid Value

```
Invalid priority value: "urgent"

Valid options:
- high
- medium
- low
```

### Circular Dependency

If adding a dependency would create a loop:

```
Cannot add dependency: This would create a circular dependency.

[Todo A] → depends on → [Todo B] → depends on → [Todo A]

Please choose a different todo or remove an existing dependency first.
```
