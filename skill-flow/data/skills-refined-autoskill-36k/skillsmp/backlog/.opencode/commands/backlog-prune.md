---
description: Archive completed tasks to tasks/archive/
---

# Prune Completed Tasks

Move completed task directories to tasks/archive/ and update INDEX.md.

## Instructions

1. **Read tasks/INDEX.md** and identify tasks with "Complete" status.

2. **If no completed tasks:**
   ```
   No completed tasks to archive.

   Tasks are marked Complete after:
   1. Implementation finished (TASK_COMPLETE promise)
   2. Code review passed (REVIEW_COMPLETE promise)
   3. /backlog-complete merges to main

   Use /backlog to see task statuses.
   ```

3. **For each completed task:**

   a. **Move task directory to archive:**
      ```bash
      mv tasks/${PREFIX}-${NNN}-${name}/ tasks/archive/
      ```

   b. **Update INDEX.md:**
      - Remove task from "Active Tasks" table
      - Add to "Archived Tasks" section

4. **Commit changes:**
   ```bash
   git add tasks/
   git commit -m "chore: archive completed tasks"
   ```

5. **Show what was archived:**

```
═══════════════════════════════════════════════════════════════════
 TASKS ARCHIVED
═══════════════════════════════════════════════════════════════════

Archived {N} completed tasks:

| Task | Title | Completed |
|------|-------|-----------|
| {PREFIX}-001 | V3 Mainnet Fork Tests | 2026-01-05 |

Moved to: tasks/archive/

Committed: chore: archive completed tasks

═══════════════════════════════════════════════════════════════════
```

## Archive Structure

After archiving:

```
tasks/
├── INDEX.md                    # Active tasks only
├── {PREFIX}-003-active-task/   # Still active
└── archive/
    └── {PREFIX}-001-completed/ # Archived
```

## Error Handling

- **No completed tasks:** Inform user, no changes made
- **No tasks/ directory:** "Run /design-init to set up task management"
- **Archive directory missing:** Create it automatically

## Related Commands

- `/backlog` - See all task statuses
- `/backlog-complete` - Mark task as complete
