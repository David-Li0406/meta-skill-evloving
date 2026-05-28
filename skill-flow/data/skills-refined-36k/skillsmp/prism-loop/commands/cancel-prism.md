---
name: cancel-prism
description: Cancel active PRISM workflow loop
allowed_tools:
  - Bash
  - Read
---

# Cancel PRISM Workflow

Stop the currently active PRISM workflow loop.

## Execute

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/prism-loop/scripts/cancel_prism_loop.py"
```

Report the result to the user.
