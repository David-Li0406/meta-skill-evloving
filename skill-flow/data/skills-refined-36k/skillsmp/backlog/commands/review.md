---
description: Transition task to code review mode after implementation (not task definition audit - see /design:review for that)
argument-hint: <task-id>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Transition Task to Code Review Mode

Update PROMPT.md in an existing worktree to switch from implementation to **code review** mode. This reviews the implementation code, NOT the task definition.

**For task definition audits** (checking TASK.md quality), use `/design:review` instead.

**Task to review:** $ARGUMENTS

## Instructions

### Phase 1: Validate Task

1. **Extract task ID** from arguments (e.g., "CRANE-003").

2. **Find task directory:**
   ```bash
   ls -d tasks/${TASK_ID}-* 2>/dev/null
   ```

3. **Check task status in INDEX.md:**
   - Must be "In Progress" to transition to review
   - If "Ready": "Task hasn't been launched yet. Use /backlog:launch first."
   - If "Complete": "Task is already complete."
   - If "In Review": "Task is already in review mode."

4. **Find worktree:**
   ```bash
   git worktree list | grep "${BRANCH_NAME}"
   ```
   - Must have an existing worktree to transition

### Phase 2: Initialize Review Files

1. **Create/update REVIEW.md** in task directory (if not exists):

```markdown
# Code Review: {PREFIX}-{NNN}

**Reviewer:** (pending)
**Review Started:** {TODAY}
**Status:** In Progress

---

## Clarifying Questions

Questions asked to understand review criteria:

(Questions and answers will be recorded here during review)

---

## Review Findings

### Finding 1: (pending)
**File:** (pending)
**Severity:** (pending)
**Description:** (pending)
**Status:** Open
**Resolution:** (pending)

---

## Suggestions

Actionable items for follow-up tasks:

### Suggestion 1: (pending)
**Priority:** (pending)
**Description:** (pending)
**Affected Files:**
- (pending)
**User Response:** (pending)
**Notes:** (pending)

---

## Review Summary

**Findings:** (pending)
**Suggestions:** (pending)
**Recommendation:** (pending)

---

**When review complete, output:** `<promise>REVIEW_COMPLETE</promise>`
```

### Phase 3: Update PROMPT.md

Update PROMPT.md in the worktree to review mode:

```markdown
# Agent Task Assignment

**Task:** {PREFIX}-{NNN} - {Title}
**Repo:** {REPO_NAME}
**Mode:** Code Review
**Task Directory:** tasks/{PREFIX}-{NNN}-{kebab-name}/

## Required Reading

1. `tasks/{PREFIX}-{NNN}-{kebab-name}/TASK.md` - Requirements to verify
2. `PRD.md` - Project context and standards (if exists)
3. `tasks/{PREFIX}-{NNN}-{kebab-name}/PROGRESS.md` - Implementation notes
4. `tasks/{PREFIX}-{NNN}-{kebab-name}/REVIEW.md` - Your review document

## Review Instructions

1. Read TASK.md to understand what was required
2. Read PROGRESS.md to understand what was implemented

3. **If unclear on review criteria:**
   - Use AskUserQuestion to clarify expectations
   - Write questions and answers to REVIEW.md "Clarifying Questions" section

4. **Review the code:**
   - Check all acceptance criteria in TASK.md are met
   - Verify test coverage
   - Look for bugs, edge cases, security issues
   - Update REVIEW.md with findings as you go
   - Mark findings as Resolved if you answer your own questions

5. **Write suggestions:**
   - Document actionable improvements in REVIEW.md
   - Prioritize by severity
   - These will be used to create follow-up tasks

6. When review is complete: `<promise>REVIEW_COMPLETE</promise>`

## On Context Compaction

If context is compacted or you're resuming:
1. Re-read this PROMPT.md
2. Re-read REVIEW.md for your prior findings
3. Continue review from where you left off
```

### Phase 4: Update State File

1. **Update state file** (if exists):
   ```yaml
   ---
   active: true
   iteration: 1
   max_iterations: {N or 0}
   started_at: "{ISO_TIMESTAMP}"
   task_id: "{TASK_ID}"
   mode: "review"
   ---
   ```

### Phase 5: Update INDEX.md

1. **Update task status** to "In Review":
   ```markdown
   | {PREFIX}-{NNN} | {Title} | In Review | {Deps} | feature/{name} |
   ```

### Phase 6: Output Instructions

```
═══════════════════════════════════════════════════════════════════
 REVIEW MODE: {PREFIX}-{NNN} - {Title}
═══════════════════════════════════════════════════════════════════

PROMPT.md updated to review mode in existing worktree.

## Step 1: Exit current Claude session (if any)

The implementation agent should have exited after TASK_COMPLETE.

## Step 2: Start fresh Claude session:

cd {ABSOLUTE_WORKTREE_PATH}
claude --dangerously-skip-permissions

## Step 3: Give Claude this prompt:

/up:prompt

The reviewer will:
- Read PROMPT.md (now in review mode)
- Read TASK.md, PROGRESS.md for context
- Ask clarifying questions if needed (saved to REVIEW.md)
- Review code for correctness and completeness
- Document findings in REVIEW.md
- Output <promise>REVIEW_COMPLETE</promise> when done

## TIP: Use a Different Model for Review!

For a fresh perspective, use a different model:

claude --model claude-sonnet-4-20250514 --dangerously-skip-permissions

═══════════════════════════════════════════════════════════════════
```

**CRITICAL: Output the following promise tag to allow session exit:**

```
<promise>TASK_BLOCKED:review_mode_configured_start_new_session</promise>
```

## Why Same Worktree?

- Reviewing the same files that were implemented
- No need to duplicate the environment
- User can choose different model for review (fresh perspective)
- Simpler workflow - just update PROMPT.md and start new session

## Error Handling

- **No task ID provided:** "Usage: /backlog:review <task-id>"
- **Task not found:** Show available task IDs
- **Task not in progress:** Show current status and suggest appropriate action
- **No worktree exists:** "Task has no worktree. Use /backlog:launch first."
- **Already in review:** "Task is already in review mode."

## Related Commands

- `/backlog:launch <ID>` - Launch agent for implementation
- `/backlog:complete <ID>` - Complete and merge task
- `/design:from-review <ID>` - Create tasks from review suggestions
