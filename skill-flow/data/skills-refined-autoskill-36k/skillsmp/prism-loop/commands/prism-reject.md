---
name: prism-reject
description: Reject the current gate and loop back to planning phase
allowed_tools:
  - Bash
  - Read
---

# /prism-reject

Reject the current gate and loop back to an earlier phase.

## Execute

Run the rejection script:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/prism-loop/scripts/prism_reject.py"
```

## Behavior

- At `red_gate`: Loops back to step 1 (review_previous_notes) to redo planning
- At `green_gate`: Not available (use /cancel-prism to abort)

The script outputs the instruction for the step it loops back to, so the workflow restarts automatically.

## When to Use

Use this command when the work at a gate is not ready:

### At RED Gate
Reject if:
- Tests have syntax/import errors instead of assertion failures
- Acceptance criteria are unclear or incomplete
- Story requirements need revision
- Test coverage is inadequate

After rejection, the planning phase restarts and the workflow will progress back to the gate once the issues are addressed.
