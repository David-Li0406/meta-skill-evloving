---
name: arch-skip
description: Skip the current step without verification (escape hatch)
disable-model-invocation: true
---

# /arch-skip Skill

**Status: Active**

Skip the current step without running verification. Use this as an escape hatch when blocked or when a step is no longer needed.

## Usage

```
/arch-skip [reason]
```

**Examples:**
- `/arch-skip` - Skip without a reason
- `/arch-skip "Step no longer needed after requirements change"`
- `/arch-skip "Blocked by external dependency, will revisit later"`

## Prerequisites

- Run `/arch [request]` to generate the plan
- Run `/arch-start` to begin execution
- Be on an active step (not completed)

---

## Step 1: Read Current State

Read `.claude/arch/state.json`.

If missing, stop and output:

```
Error: Architecture artifacts not found.
Run /arch [request] first to generate the plan.
```

If `phase` is `"planning"` or `current_step` is `null`, stop and output:

```
Error: Session not started.
Run /arch-start to begin execution.
```

If `phase` is `"completed"`, stop and output:

```
Session already completed. Nothing to skip.
```

---

## Step 2: Confirm Skip

Read the current step from `.claude/arch/TASK_GRAPH.json` and display:

```
About to skip step: [id] - [title]
Goal: [goal]

This step will NOT be verified. Continue? (y/n)
```

Wait for user confirmation. If user declines, stop without changes.

---

## Step 3: Execute Skip

Run this command (include reason if provided):

```bash
python scripts/arch_session.py skip --reason "[user's reason]"
```

Or without reason:

```bash
python scripts/arch_session.py skip
```

---

## Step 4: Report New State

**If there is a next step:**

```
Skipped step: [previous_id]
Reason: [reason if provided]

Next Step: [id] - [title]
Goal: [goal]
Allowed Paths: [allowed_paths]
Verification: [verification commands]
Success Criteria: [success_criteria]

Implement this step, then run /arch-next when ready.
```

**If session is completed:**

```
Skipped step: [previous_id]
Reason: [reason if provided]

All steps completed. Session finished.

Note: Some steps were skipped. Review implementation completeness.
```

---

## When to Use

Use `/arch-skip` when:

- **Blocked by external factors** - waiting on API keys, dependencies, etc.
- **Requirements changed** - step is no longer relevant
- **Step is optional** - nice-to-have that can be deferred
- **Verification is broken** - tests fail due to environment issues, not code

Do NOT use `/arch-skip` to:

- Avoid fixing failing tests
- Skip steps you're unsure how to implement
- Rush through the plan without proper implementation

---

## Constraints

- **No verification**: Step is marked as skipped, not completed
- **User confirmation**: Always confirm before skipping
- **Reason recommended**: Provide a reason for audit trail
- **One step at a time**: Only skips the current step
