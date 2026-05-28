---
description: Transition task to code review mode after implementation
---

# Transition Task to Code Review Mode

Update PROMPT.md in an existing worktree to switch from implementation to **code review** mode. This reviews the implementation code, NOT the task definition.

**For task definition audits**, use `/design-review` instead.

**Task to review:** $ARGUMENTS

## Instructions

### Phase 1: Validate Task

1. Extract task ID from arguments
2. Find task directory
3. Check task status (must be "In Progress")
4. Find existing worktree

### Phase 2: Initialize Review Files

Create/update REVIEW.md in task directory with review template:
- Clarifying Questions section
- Review Findings section
- Suggestions section
- Review Summary section

### Phase 3: Update PROMPT.md

Update PROMPT.md in the worktree to review mode:
- Change Mode to "Code Review"
- Update instructions for reviewing instead of implementing
- Reference REVIEW.md as the output document

### Phase 4: Update INDEX.md

Update task status to "In Review"

### Phase 5: Output Instructions

```
═══════════════════════════════════════════════════════════════════
 REVIEW MODE: {PREFIX}-{NNN} - {Title}
═══════════════════════════════════════════════════════════════════

PROMPT.md updated to review mode in existing worktree.

## Step 1: Exit current session (if any)

## Step 2: Start fresh session in worktree:

cd {ABSOLUTE_WORKTREE_PATH}

## Step 3: Run the bootstrap command:

/prompt

The reviewer will:
- Read TASK.md, PROGRESS.md for context
- Review code for correctness and completeness
- Document findings in REVIEW.md

## TIP: Use a Different Model for Review!

For a fresh perspective, use a different model for the review.

═══════════════════════════════════════════════════════════════════
```

## Error Handling

- **No task ID provided:** "Usage: /backlog-review <task-id>"
- **Task not found:** Show available task IDs
- **Task not in progress:** Show current status and suggest action
- **No worktree exists:** "Task has no worktree. Use /backlog-launch first."

## Related Commands

- `/backlog-launch <ID>` - Launch agent for implementation
- `/backlog-complete <ID>` - Complete and merge task
- `/design-from-review <ID>` - Create tasks from review suggestions
