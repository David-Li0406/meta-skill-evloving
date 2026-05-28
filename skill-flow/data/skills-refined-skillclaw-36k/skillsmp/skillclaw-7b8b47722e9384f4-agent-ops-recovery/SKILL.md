---
name: agent-ops-recovery
description: Use this skill when handling failures and errors during workflow, such as build breaks, unexpected test failures, or when the agent gets stuck. It provides a semi-automatic recovery process with user confirmation for destructive actions.
---

# Error Recovery Workflow

## Trigger Conditions

Use this skill when:
- Build/lint fails unexpectedly after agent changes.
- Tests fail that were passing in baseline.
- Agent encounters ambiguity it cannot resolve.
- Implementation is stuck or going in circles.

## Recovery Procedure

### Step 1: Diagnose (Invoke Debugging)

For non-trivial failures, invoke `agent-ops-debugging`:

1. Apply a systematic debugging process:
   - Reproduce the issue consistently.
   - Define expected vs actual behavior.
   - Form a hypothesis about the root cause.
2. Use debugging output to inform recovery decisions.
3. If the root cause is unclear after initial analysis, continue debugging before recovery.

### Step 2: Assess Rollback Options

- **Option A**: Fix forward — issue is minor and can be resolved quickly.
- **Option B**: Partial rollback — revert specific file(s) to the last good state.
- **Option C**: Full rollback — revert all agent changes since the last checkpoint.
- **Option D**: Escalate — document the issue, mark the task as blocked, and ask the user.

### Step 3: Propose Action

Present options to the user with:
- What will be reverted/changed.
- Risk assessment.
- Recommendation.

### Step 4: Execute (with Confirmation)

- For non-destructive actions (fix forward): proceed.
- For destructive actions (rollback): **ask user first**.
- Update `.agent/focus.md` with the recovery action taken.

## Destructive Actions (Require Confirmation)

- `git reset`
- `git checkout -- <file>` (discard changes)
- `git revert`
- Deleting files
- Overwriting files with previous versions

## Non-Destructive Actions (Can Proceed)

- `git stash`
- Reading files
- Running diagnostics
- Updating focus/tasks with findings

## Post-Recovery

1. Update `.agent/focus.md` with what happened.
2. Invoke `agent-ops-tasks` to create an issue for root cause investigation.
3. Update `.agent/memory.md` with "pitfall to avoid" if applicable.
4. Re-run baseline comparison before continuing.

## Issue Discovery After Recovery

After recovery, invoke `agent-ops-tasks` discovery procedure:

1. Create an issue for the incident.
   ```
   📋 Recovery completed. Create issue to track the incident.
   ```