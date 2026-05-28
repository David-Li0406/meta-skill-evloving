---
name: edge-done
description: Validate session completion before ending work. Use when finishing a coding session to ensure state was saved and proof exists.
---

# Session Completion Validation

This skill replaces the Stop hook from Claude Code. Run it before ending your session to validate that work was properly recorded.

## When to Use

Call this skill when:
- Finishing work for the session
- Before closing Codex CLI
- When switching to a different project
- The user says "done", "finished", "that's all", "goodbye"

## Instructions

### 1. Read Current State

Load `active_context.yaml` and check:

| Check | Requirement | Validation |
|-------|-------------|------------|
| State exists | `active_context.yaml` file present | File can be read |
| Objective set | `objective` field has value | Not null or empty |
| Plan exists | `plan` array has items | At least one step |
| Progress made | At least one step completed OR in_progress | Status check |

### 2. Check for State Modification

Compare the current state against what was loaded at session start:
- Were any steps advanced?
- Were any steps marked completed?
- Was any memory added?

If NO state modification occurred:
```
WARNING: No progress recorded this session
- No steps were completed
- No steps were advanced
- State is unchanged from session start

Did you forget to update active_context.yaml?
```

### 3. Check for Proof

Look for evidence of work in `.proof/session_log.jsonl`:

```bash
# Check if proof file exists and has entries
ls -la .proof/session_log.jsonl
```

| Condition | Status |
|-----------|--------|
| File exists with entries | Proof captured |
| File missing or empty | No proof recorded |

If NO proof exists:
```
WARNING: No proof captured this session
- .proof/session_log.jsonl is missing or empty
- Run $edge-log to record what you did
```

### 4. Validate Plan Consistency

Check for orphaned or inconsistent states:

| Issue | Detection | Suggestion |
|-------|-----------|------------|
| Step marked in_progress but no current_step | Orphaned work | Mark complete or reset |
| current_step points to completed step | Stale pointer | Advance current_step |
| Blocked steps without notes | Missing context | Add blocking reason |

### 5. Generate Session Summary

Produce a summary of the session:

```
========================================
SESSION COMPLETION CHECK
========================================

Session: [session.id]
Objective: [objective]

Progress:
  Steps completed this session: [N]
  Current step: [current_step] - [description]
  Overall progress: [completed/total] steps

State Changes:
  - [List of what changed in active_context.yaml]

Proof Captured:
  - [N] log entries in .proof/session_log.jsonl
  - Last entry: [timestamp] - [action summary]

Validation:
  [x] State file modified
  [x] Proof file has entries
  [x] Plan is consistent
  [ ] Issue: [if any]

Status: READY TO END | NEEDS ATTENTION
========================================
```

### 6. Block or Allow

**If all checks pass:**
```
Session validation PASSED

You may end this session. Progress and proof are recorded.

Next session: Run $edge-context to reload state.
```

**If checks fail:**
```
Session validation FAILED

Issues that need attention:
1. [Issue 1]
2. [Issue 2]

Suggested actions:
- [How to fix issue 1]
- [How to fix issue 2]

Please resolve these before ending the session, or acknowledge:
"End anyway - I understand progress may be lost"
```

## Comparison to Claude Code Stop Hook

| Claude Code (Hook) | Codex CLI (Skill) |
|--------------------|-------------------|
| Automatic - runs when session ends | Manual - user must invoke |
| Blocks termination if checks fail | Warns but cannot block |
| State hash comparison | Manual state review |
| Proof file existence check | Same check, manual |

## Quick Validation

For a fast check without full summary:

```
Quick Session Check:
- State modified: [yes/no]
- Proof exists: [yes/no]
- Ready to end: [yes/no]
```

## Tips

- **Run early, run often**: Check validation before committing to end
- **Log as you go**: Use `$edge-log` after each major action
- **Update state promptly**: Mark steps complete immediately after finishing

## Integration with Other Skills

The `$edge-step` skill should automatically call `$edge-log` after completing each step, which means proof should accumulate naturally.

Recommended workflow:
1. `$edge-context` - Load state at session start
2. `$edge-step` (repeats) - Execute work
3. `$edge-done` - Validate before ending

## If Validation Fails

### No state modification
```bash
# Add a note to active_context.yaml showing session activity
# Even if no steps completed, document what was investigated
```

### No proof captured
```bash
# Create proof retroactively
mkdir -p .proof
echo '{"timestamp":"<now>","type":"session_summary","action":"<what you did>","outcome":"<result>"}' >> .proof/session_log.jsonl
```

### Inconsistent plan state
```yaml
# Fix in active_context.yaml
current_step: [correct value]
plan:
  - description: "..."
    status: [correct status]
```
