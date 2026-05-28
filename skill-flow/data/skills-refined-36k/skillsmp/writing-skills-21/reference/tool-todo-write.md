# TodoWrite Tool

Display task progress with checkboxes.

## How It Works in Skills

Claude can call TodoWrite to show structured task lists. Useful for multi-step skills to show progress.

## Schema

```typescript
TodoWrite({
  todos: [
    {
      content: string, // Task description (imperative)
      status: "pending" | "in_progress" | "completed",
      activeForm: string, // Present continuous form
    },
  ],
});
```

## Examples

**Migration skill with progress:**

```yaml
---
name: db-migrator
description: Runs database migrations with progress tracking
---

# Database Migrator

Create todo list for migration steps:

1. TodoWrite with items:
   - "Backup database" (pending)
   - "Run migrations" (pending)
   - "Verify schema" (pending)
   - "Update seeds" (pending)

2. As each step completes, update status to completed

3. Keep exactly one item as in_progress at a time
```

**Code review checklist:**

```yaml
---
name: review-checklist
description: Structured code review with checklist
---

Create review checklist with TodoWrite:
- "Check for security issues" / "Checking security"
- "Verify test coverage" / "Verifying tests"
- "Review error handling" / "Reviewing errors"
- "Check performance" / "Checking performance"

All start as pending. Mark in_progress as you work through each.
```

## Links

- Issues:
  - [#1173](https://github.com/anthropics/claude-code/issues/1173) - Updates in Task tool not visible
  - [#6891](https://github.com/anthropics/claude-code/issues/6891) - Visual checkbox regression
  - [#8723](https://github.com/anthropics/claude-code/issues/8723) - Request for persistent task panel
