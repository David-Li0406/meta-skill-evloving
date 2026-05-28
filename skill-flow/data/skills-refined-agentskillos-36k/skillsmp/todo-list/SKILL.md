---
name: todo-list
description: Display all active todos with status and priority
trigger_keywords:
  - show todos
  - list todos
  - my todos
  - view todos
  - what todos
---

# Todo List

## Purpose

Display a summary of all active todos, sorted by priority and due date, with options to take action on specific items.

## Execution Flow

### Phase 1: Locate Todos Directory

1. Search for `Todos/` directory in the current working directory or its parents
2. Check `Todos/active/` for todo files
3. If not found:
   ```
   "No Todos directory found. You can create one using /todo-add."
   ```

### Phase 2: Read Active Todos

1. Use Glob to find all `.md` files in `Todos/active/`:
   ```
   Todos/active/*.md
   ```
   (Exclude README.md)

2. For each todo file, read and parse frontmatter:
   - title
   - status
   - priority
   - due_date
   - created_at
   - source_file
   - dependencies

### Phase 3: Sort Todos

Sort order (primary to tertiary):
1. **Priority**: high → medium → low
2. **Due Date**: overdue → today → this week → later → no date
3. **Created Date**: oldest first (to surface forgotten items)

### Phase 4: Format Output

Display as formatted table:

```
## Active Todos

| # | Title | Priority | Due | Status | Source |
|---|-------|----------|-----|--------|--------|
| 1 | Reply to client email | 🔴 High | 2025-01-15 (2 days) | pending | [email](link) |
| 2 | Review design docs | 🟡 Medium | 2025-01-20 | in_progress | - |
| 3 | Update documentation | 🟢 Low | - | pending | - |

---

### Summary

- **Total**: 3 active todos
- **High Priority**: 1
- **Overdue**: 0
- **Blocked**: 0 (dependencies not met)

### Overdue Items
(none)

### Due Today
(none)

### Due This Week
- Reply to client email (2025-01-15)
```

### Phase 5: Display Status Legend

```
Status:
- pending: Not started
- in_progress: Currently working on
- blocked: Waiting for dependencies

Priority:
- 🔴 High: Urgent/time-sensitive
- 🟡 Medium: Normal priority
- 🟢 Low: When time permits
```

### Phase 6: Offer Actions

Ask user what they want to do next:

```json
{
  "question": "What would you like to do?",
  "header": "Actions",
  "options": [
    {"label": "View details of a todo", "description": "Read the full content of a specific todo"},
    {"label": "Mark a todo complete", "description": "Complete and archive a todo"},
    {"label": "Update a todo", "description": "Change priority, due date, or status"},
    {"label": "Nothing, just viewing", "description": "Close this view"}
  ],
  "multiSelect": false
}
```

If user selects an action, follow up with todo selection:
```json
{
  "question": "Which todo?",
  "header": "Select Todo",
  "options": [
    {"label": "#1 Reply to client email", "description": "High priority, due 2025-01-15"},
    {"label": "#2 Review design docs", "description": "Medium priority, in progress"},
    {"label": "#3 Update documentation", "description": "Low priority, no deadline"}
  ],
  "multiSelect": false
}
```

## Output Formats

### Standard View (default)

Table format as shown above.

### Compact View

If there are many todos (>10):

```
## Active Todos (15 items)

### 🔴 High Priority (3)
1. Reply to client email - due 2025-01-15
2. Fix critical bug - due today ⚠️
3. Submit report - overdue ❌

### 🟡 Medium Priority (7)
4. Review design docs - in progress
5. Update API docs
...

### 🟢 Low Priority (5)
12. Refactor utils
...
```

### Blocked Items

If any todos have unmet dependencies:

```
### ⏸️ Blocked Todos

- **Prepare client presentation** (blocked)
  Waiting for: Review design docs, Get approval
```

## Empty State

If no active todos:

```
## Active Todos

No active todos! 🎉

You can:
- Add a new todo with /todo-add
- Check completed todos in Todos/completed/
```

## Error Handling

### Corrupted Frontmatter

If a todo file has invalid frontmatter:
1. Log warning: "Warning: [filename] has invalid frontmatter"
2. Skip the file in listing
3. Mention at the end: "1 todo file could not be parsed"

### Missing Directory

If `Todos/active/` doesn't exist but `Todos/` does:
1. Offer to create the directory structure
2. Or report "No active todos found"
