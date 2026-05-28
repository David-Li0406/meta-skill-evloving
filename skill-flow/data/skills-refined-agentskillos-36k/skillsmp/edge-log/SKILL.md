---
name: edge-log
description: Log proof of completed work to the session log. Use after completing significant actions to maintain an audit trail.
---

# Log Proof

Since Codex CLI doesn't have automatic PostToolUse hooks, this skill manually logs proof of completed work.

## When to Use

Call this skill after:
- Completing a step in the plan
- Making significant file changes
- Running tests
- Any action that should be recorded for audit

## Instructions

### 1. Gather Proof Information

Collect:
- **What was done**: Brief description of the action
- **Files modified**: List of changed files
- **Outcome**: Success/failure and any relevant output
- **Timestamp**: Current time

### 2. Append to Session Log

Add an entry to `.proof/session_log.jsonl`:

```json
{
  "timestamp": "2025-01-15T14:30:00Z",
  "type": "manual_log",
  "action": "Completed step 3: Add user authentication",
  "files": ["src/auth.py", "tests/test_auth.py"],
  "outcome": "success",
  "details": "Added JWT-based auth, all tests pass"
}
```

### 3. Create Log Directory if Needed

If `.proof/` doesn't exist:
```bash
mkdir -p .proof
```

### 4. Append Entry

```bash
echo '{"timestamp":"...","type":"manual_log",...}' >> .proof/session_log.jsonl
```

## Log Entry Format

```json
{
  "timestamp": "<ISO 8601 timestamp>",
  "type": "manual_log",
  "action": "<what was done>",
  "files": ["<list>", "<of>", "<files>"],
  "outcome": "success | failure | partial",
  "details": "<additional context>",
  "step": <step number if applicable>
}
```

## Quick Log Template

For common actions, use these templates:

### Step Completion
```json
{
  "timestamp": "<now>",
  "type": "step_complete",
  "step": <N>,
  "description": "<step description>",
  "proof": "<evidence of completion>"
}
```

### File Change
```json
{
  "timestamp": "<now>",
  "type": "file_change",
  "files": ["<path1>", "<path2>"],
  "action": "create | edit | delete",
  "reason": "<why this change was made>"
}
```

### Test Run
```json
{
  "timestamp": "<now>",
  "type": "test_run",
  "command": "<test command>",
  "result": "pass | fail",
  "details": "<N tests, M failures>"
}
```

## Integration with Other Skills

The `$edge-step` skill should call `$edge-log` after completing each step.

Example workflow:
1. `$edge-step` executes the work
2. Work completes successfully
3. `$edge-log` records the proof
4. `active_context.yaml` is updated with step completion

## Why This Matters

Without automatic logging:
- There's no audit trail of what happened
- Proof claims are unverifiable
- State changes are invisible

Manual logging provides:
- Accountability
- Debugging history
- Evidence for self-assessment
