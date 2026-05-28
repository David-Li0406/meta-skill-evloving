---
description: Read and display a specific task from tasks/
---

# Read Task

Display the full content of a specific task from its task directory.

**Task to read:** $ARGUMENTS

## Instructions

1. **Extract task ID** from arguments (e.g., "CRANE-003", "IDX-007").

2. **Find task directory:**
   ```bash
   ls -d tasks/${TASK_ID}-* 2>/dev/null
   ```

3. **If task not found:**
   ```
   Task {TASK_ID} not found.

   Available tasks:
   - {PREFIX}-001: {Title}
   - {PREFIX}-002: {Title}

   Use /backlog to see all tasks.
   ```

4. **Read task files:**
   - `tasks/{ID}-{name}/TASK.md` - Requirements
   - `tasks/{ID}-{name}/PROGRESS.md` - Implementation progress (if exists)
   - `tasks/{ID}-{name}/REVIEW.md` - Review notes (if exists)

5. **Display formatted output:**

```
═══════════════════════════════════════════════════════════════════
 TASK: {PREFIX}-{NNN} - {Title}
═══════════════════════════════════════════════════════════════════

**Status:** {Status from TASK.md}
**Dependencies:** {Dependencies or "None"}
**Directory:** tasks/{PREFIX}-{NNN}-{kebab-name}/

---

## Requirements (TASK.md)

{Full content of TASK.md}

---

## Progress (PROGRESS.md)

{Latest session log entry or "No progress recorded yet"}

---

## Review (REVIEW.md)

{Review summary or "No review yet"}

═══════════════════════════════════════════════════════════════════

## Actions

- To launch agent: /backlog-launch {PREFIX}-{NNN}
- To review: /backlog-review {PREFIX}-{NNN}
- To complete: /backlog-complete {PREFIX}-{NNN}
```

## Error Handling

- **No task ID provided:** "Usage: /backlog-read <task-id>"
- **Task doesn't exist:** Show available task IDs
- **No tasks/ directory:** "Run /design-init to set up task management"

## Related Commands

- `/backlog` - View all tasks
- `/backlog-launch <ID>` - Create worktree and start working
