---
description: Archive completed tasks to tasks/archive/
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
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
   3. /backlog:complete merges to main

   Use /backlog to see task statuses.
   ```

3. **For each completed task:**

   a. **Move task directory to archive:**
      ```bash
      mv tasks/${PREFIX}-${NNN}-${name}/ tasks/archive/
      ```

   b. **Update INDEX.md:**
      - Remove task from "Active Tasks" table
      - Add to "Archived Tasks" section (or create if missing)

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
| {PREFIX}-002 | Slipstream Utils | 2026-01-07 |

Moved to: tasks/archive/

Remaining active tasks: {PREFIX}-003, {PREFIX}-004, {PREFIX}-005

Committed: chore: archive completed tasks

═══════════════════════════════════════════════════════════════════
```

## Archive Structure

After archiving:

```
tasks/
├── INDEX.md                    # Active tasks only
├── TEMPLATE.md
├── {PREFIX}-003-active-task/   # Still active
├── {PREFIX}-004-another-task/  # Still active
└── archive/
    ├── {PREFIX}-001-completed/ # Archived
    └── {PREFIX}-002-completed/ # Archived
```

## INDEX.md Archive Section

Add to bottom of INDEX.md:

```markdown
## Archived Tasks

| ID | Title | Completed | Location |
|----|-------|-----------|----------|
| {PREFIX}-001 | V3 Mainnet Fork Tests | 2026-01-05 | archive/{PREFIX}-001-v3-mainnet-fork-tests/ |
| {PREFIX}-002 | Slipstream Utils | 2026-01-07 | archive/{PREFIX}-002-slipstream-utils/ |
```

## Selective Archive

To archive only specific tasks (future enhancement):

```bash
/backlog:prune {PREFIX}-001 {PREFIX}-002
```

Currently archives ALL completed tasks.

## Error Handling

- **No completed tasks:** Inform user, no changes made
- **No tasks/ directory:** "Run /design:init to set up task management"
- **Archive directory missing:** Create it automatically
- **Move fails:** Show error, suggest manual intervention

## Notes

- Task IDs are never renumbered after archival
- Archived tasks retain all files (TASK.md, PROGRESS.md, REVIEW.md)
- Use `/backlog:read` with full path to read archived tasks
- Archive can be deleted manually if not needed

## Related Commands

- `/backlog` - See all task statuses
- `/backlog:complete` - Mark task as complete
- `/design:from-review` - Create new tasks from review findings
