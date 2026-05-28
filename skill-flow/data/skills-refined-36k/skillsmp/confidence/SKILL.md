---
name: confidence
description: Check or set the auto-continuation confidence threshold
allowed-tools: Read, Write
user-invocable: true
---

# Confidence Threshold

Quick access to view or modify the confidence threshold for auto-continuation.

If "$ARGUMENTS" is a number between 0-99, set the threshold to that value.
If "$ARGUMENTS" is empty, show the current threshold.

The confidence threshold determines when Claude Code will automatically proceed with "Yes" responses:
- **Higher threshold (80-99)**: More conservative, requires higher certainty
- **Lower threshold (50-79)**: More permissive, continues more often
- **Very low (0-49)**: Very aggressive, almost always continues

Recommended: 80 (default) for most workflows, 90+ for critical operations.
