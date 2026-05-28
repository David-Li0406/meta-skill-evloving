---
name: status
description: Show Inference Confidenz current status and recent history
allowed-tools: Bash
user-invocable: true
---

# Inference Confidenz Status

Display the current status and recent confidence history.

```!
"${CLAUDE_PLUGIN_ROOT}/scripts/status.sh"
```

This shows:
- Whether Confidenz is enabled
- Current display format
- Recent confidence scores (if logging is enabled)
- Configuration file location
