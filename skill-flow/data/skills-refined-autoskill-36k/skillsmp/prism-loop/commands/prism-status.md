---
name: prism-status
description: Check current PRISM workflow status
allowed_tools:
  - Bash
  - Read
---

# PRISM Workflow Status

Display the current state of the PRISM workflow loop.

## Execute

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/prism-loop/scripts/prism_status.py"
```

Shows:
- Current step and progress
- Story file path
- Whether paused for manual action
- Which steps will be skipped
