---
name: status
description: Check Vocal Bridge authentication status. Shows current API key, connected agent name, and connection health.
allowed-tools: Bash
---

Check the current Vocal Bridge authentication status.

First ensure CLI is installed:

```bash
pip install --upgrade vocal-bridge
```

Then run:

```bash
vb auth status
```

This shows:
- API URL
- API Key (masked)
- Authentication status
- Connected agent name and mode
- Agent ID
- Phone number (if assigned)
