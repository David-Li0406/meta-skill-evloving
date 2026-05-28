---
description: Read and display a specific task from tasks/
argument-hint: <task-id>
allowed-tools: Read, Glob, Grep
---

# Read Task

Display the full content of a specific task from its task directory.

**Task to read:** $ARGUMENTS

## Instructions

1. **Extract task ID** from arguments (e.g., "CRANE-003", "IDX-007").

2. **Find task directory:**
   ```bash
   # Find task directory matching the ID
   ls -d tasks/${TASK_ID}-* 2>/dev/null
   ```

3. **If task not found:**
   ```
   Task {TASK_ID} not found.

   Available tasks:
   - {PREFIX}-001: {Title}
   - {PREFIX}-002: {Title}
   ...

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
**Worktree:** {Worktree branch or "Not started"}
**Directory:** tasks/{PREFIX}-{NNN}-{kebab-name}/

---

## Requirements (TASK.md)

{Full content of TASK.md}

---

## Progress (PROGRESS.md)

**Last checkpoint:** {Last checkpoint summary}

{Latest session log entry or "No progress recorded yet"}

---

## Review (REVIEW.md)

**Status:** {Review status or "Not yet reviewed"}

{Review summary or "No review yet"}

═══════════════════════════════════════════════════════════════════

## Actions

- To launch agent: /backlog:launch {PREFIX}-{NNN}
- To review: /backlog:review {PREFIX}-{NNN}
- To complete: /backlog:complete {PREFIX}-{NNN}
```

## Output Sections

### Requirements
Full content of TASK.md including:
- Description
- User stories
- Acceptance criteria
- Files to create/modify
- Inventory check
- Completion criteria

### Progress
From PROGRESS.md:
- Current checkpoint status
- Latest session log entry
- Build/test status

### Review
From REVIEW.md (if exists):
- Review status
- Number of findings
- Recommendations

## Error Handling

- **No task ID provided:** "Usage: /backlog:read <task-id> (e.g., /backlog:read CRANE-003)"
- **Task doesn't exist:** Show available task IDs from tasks/INDEX.md
- **No tasks/ directory:** "Run /design:init to set up task management"
- **Missing TASK.md:** "Task directory exists but TASK.md is missing"

## Examples

```bash
# Read task by ID
/backlog:read CRANE-003

# Read task by full directory name
/backlog:read CRANE-003-uniswap-v4-utils
```

## Notes

- Task IDs are permanent and never renumbered
- This is a read-only command - it does not modify any files
- Use `/backlog:launch <ID>` to create a worktree and start working on a task
