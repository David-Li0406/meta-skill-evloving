---
name: prism-approve
description: Approve the current gate and advance to the next workflow phase
allowed_tools:
  - Bash
  - Read
---

# /prism-approve

Approve the current gate and advance the workflow to the next phase.

## Execute

Run the approval script:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/prism-loop/scripts/prism_approve.py"
```

## Behavior

- At `red_gate`: Approves RED phase → advances to GREEN phase (implementation)
- At `green_gate`: Completes workflow and cleans up state

The script outputs the instruction for the next agent step, so the workflow continues automatically.

## When to Use

Use this command when the workflow is paused at a gate and you've verified the work is ready to proceed.
