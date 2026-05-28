---
name: edge-step
description: Execute the current step from the plan in active_context.yaml. Use when ready to work on the next task in a structured workflow.
---

# Execute Current Step

Read `active_context.yaml` to understand the current plan and step.

## Instructions

1. **Read the current step** from `active_context.yaml`
   - Find the step matching `current_step`
   - Understand what needs to be done

2. **Check for reminders** - Read `.proof/archive.jsonl` for recurring weak checks
   - If any check has failed 2+ times across sessions, show a reminder:

   ```
   REMINDER: [check_name] has been weak across sessions
   Focus: [specific improvement tip]
   ```

   Common reminders:
   | Weak Check | Reminder |
   |------------|----------|
   | mismatch_detection | "Add Expected vs Actual before major operations" |
   | plan_revision | "If this step fails, write a NEW step before retrying" |
   | tool_switching | "If tool fails twice, switch immediately" |
   | memory_update | "After this step, ask: what did I learn?" |
   | proof_generation | "Attach evidence inline, not after" |
   | stop_condition | "If uncertain, frame as bounded options" |

3. **Mark it in_progress** - Update the step's status in active_context.yaml

4. **Do the work** - Execute the step
   - Keep changes minimal and focused
   - If something unexpected happens, STOP and reassess
   - **Apply the reminder** if one was shown

5. **Verify it worked** - Run a test or check

6. **Mark complete** - Update status to `completed` and set proof path

7. **Advance current_step** - Increment to next pending step

## After Completion

Update active_context.yaml:
```yaml
current_step: [next step number]
plan:
  - description: "The step you just did"
    status: completed
    proof: "description of evidence"  # or specific artifact path
```

Add any lessons learned to memory:
```yaml
memory:
  - trigger: "relevant keywords"
    lesson: "What you learned"
    reinforced: 1
```

## If Blocked

If you cannot complete the step:
1. Mark status as `blocked`
2. Add a note explaining why
3. Do NOT advance current_step
4. Report the blocker clearly

## Proof Capture (IMPORTANT)

Since Codex CLI doesn't have automatic proof capture, you MUST manually log proof after completing each step.

### After Completing Work:

1. **Create proof directory** (if needed):
   ```bash
   mkdir -p .proof
   ```

2. **Append to session log**:
   ```bash
   echo '{"timestamp":"<ISO_TIME>","type":"step_complete","step":<N>,"description":"<STEP_DESC>","files":["<FILES>"],"outcome":"success"}' >> .proof/session_log.jsonl
   ```

3. **Or use the logging skill**:
   ```
   $edge-log
   ```

### What to Log:
- **Files modified**: Actual paths changed
- **Tests run**: Commands and results
- **Outcome**: success/failure/partial
- **Evidence**: Specific proof (test output, line counts, etc.)

### Example Log Entry:
```json
{
  "timestamp": "2025-01-15T14:30:00Z",
  "type": "step_complete",
  "step": 3,
  "description": "Add user authentication",
  "files": ["src/auth.py", "tests/test_auth.py"],
  "outcome": "success",
  "proof": "26 tests pass, JWT validation working"
}
```

This manual logging replaces Claude Code's automatic PostToolUse hook.
