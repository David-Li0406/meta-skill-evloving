---
name: agent
description: Show information about the connected Vocal Bridge voice agent including name, mode, phone number, and deployment status.
allowed-tools: Bash
---

Get information about the connected voice agent.

First ensure CLI is installed:

```bash
pip install --upgrade vocal-bridge
```

Then run:

```bash
vb agent
```

This displays:
- Agent name
- Agent ID
- Mode 
- Deployment status
- Phone number
- Greeting message
- Creation date
