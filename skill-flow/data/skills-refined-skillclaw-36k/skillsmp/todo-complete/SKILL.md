---
name: todo-complete
description: Mark a todo as complete and archive it
trigger_keywords:
  - complete todo
  - finish todo
  - done with todo
  - mark complete
  - todo done
---

# Todo Complete

## Purpose

Mark a todo as completed, update its execution log, move it to the completed/ directory, and handle dependency unblocking for other todos.

## Execution Flow

### Phase 1: Identify Todo

**If user specifies todo in command**:
- Parse the todo identifier (title, filename, or number from list)
- Example: `/todo-complete Reply to client email`

**If not specified**:
1. List active todos using compact format:
   ```
   Which todo would you like to complete?

   1. Reply to client email (High, due 2025-01-15)
   2. Review design docs (Medium, in progress)
   3. Update documentation (Low)
   ```

2. Ask user to select:
   ```json
   {
     "question": "Which todo do you want to complete?",
     "header": "Select Todo",
     "options": [
       {"label": "#1 Reply to client email", "description": "High priority, due 2025-01-15"},
       {"label": "#2 Review design docs", "description": "Medium priority, in progress"},
       {"label": "#3 Update documentation", "description": "Low priority"}
     ],
     "multiSelect": false
   }
   ```

### Phase 2: Confirm Completion

Ask for confirmation:
```json
{
  "question": "Mark 'Reply to client email' as complete?",
  "header": "Confirm",
  "options": [
    {"label": "Yes, complete it", "description": "Archive this todo"},
    {"label": "No, cancel", "description": "Keep todo as active"}
  ],
  "multiSelect": false
}
```

### Phase 3: Update Todo File

1. **Read current file content**

2. **Update frontmatter**:
   ```yaml
   status: completed
   completed_at: [Current date YYYY-MM-DD]
   ```

3. **Add completion entry to execution log**:
   ```markdown
   ### [Current Date]
   - Marked as completed
   - Status: [previous status] → completed
   - Completion confirmed by user
   ```

### Phase 4: Move to Completed

1. **Move file**:
   - From: `Todos/active/[filename]`
   - To: `Todos/completed/[filename]`

2. **Update `Todos/active/README.md`**:
   - Remove the entry for this todo
   - Update "Last updated" timestamp

3. **Update `Todos/completed/README.md`**:
   - Add entry for the completed todo
   - Format: `- [filename](filename) - [title] (Completed: [date])`
   - Update "Last updated" timestamp

4. **Update `Todos/README.md`**:
   - Decrement active count
   - Increment completed count
   - Add to "Recent Changes" section

### Phase 5: Handle Dependencies

**Search for dependent todos**:

1. Use Grep to search `Todos/active/` for files containing this todo's path:
   ```
   grep -l "[completed todo filename]" Todos/active/*.md
   ```

2. For each dependent todo found:
   a. Read the todo file
   b. Parse dependencies list
   c. Update this todo's status to `completed` in the dependencies
   d. Check if ALL dependencies are now completed
   e. If yes:
      - Change status from `blocked` to `pending`
      - Clear `blocking_reason`
      - Add log entry:
        ```markdown
        ### [Current Date]
        - Dependency completed: [completed todo title]
        - Status: blocked → pending
        - All dependencies now satisfied
        ```
   f. Add to unblocked list for reporting

### Phase 6: Report

**Standard completion**:
```
✅ Todo completed: "Reply to client email"

- Previous status: in_progress
- Completed at: 2025-01-13
- Archived to: Todos/completed/2025-01-10_reply-client-email.md
```

**With unblocked todos**:
```
✅ Todo completed: "Reply to client email"

- Previous status: in_progress
- Completed at: 2025-01-13
- Archived to: Todos/completed/2025-01-10_reply-client-email.md

🔓 Unblocked todos:
- "Prepare client presentation" is now ready to start
- "Send follow-up email" is now ready to start

Would you like to start working on any of these?
```

## Error Handling

### Todo Not Found

```
Todo not found: "[search term]"

Active todos:
1. Reply to client email
2. Review design docs
3. Update documentation

Try again with the correct title or number.
```

### Already Completed

```
"[todo title]" is already completed.

Completed on: 2025-01-10
Location: Todos/completed/[filename]
```

### Has Incomplete Dependencies

If completing a todo that other todos depend on, proceed normally (this unblocks those todos).

### Blocked Status

If the todo being completed is currently blocked:
```
Note: This todo was marked as blocked, but you're completing it anyway.
Proceeding with completion...
```

## Batch Completion

If user wants to complete multiple todos:

```json
{
  "question": "Select todos to complete",
  "header": "Batch Complete",
  "options": [
    {"label": "#1 Reply to client email", "description": "High priority"},
    {"label": "#2 Review design docs", "description": "Medium priority"},
    {"label": "#3 Update documentation", "description": "Low priority"}
  ],
  "multiSelect": true
}
```

Process each selected todo in sequence, collecting results for a summary report.
