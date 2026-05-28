---
name: stats
description: Show call statistics for the Vocal Bridge voice agent including total calls, success rate, and average duration.
allowed-tools: Bash
---

Show call statistics for the voice agent.

First ensure CLI is installed:

```bash
pip install --upgrade vocal-bridge
```

Then run:

```bash
vb stats $ARGUMENTS
```

This displays:
- Total sessions
- Completed sessions
- Failed sessions
- Abandoned sessions
- Total duration
- Average duration
- Total messages
- Average messages per call

Use `--json` flag for machine-readable output.
