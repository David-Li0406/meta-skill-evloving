---
name: multi-agent-dispatch
description: Dispatch tasks to remote VMs for parallel execution or specialized work.
---

# Multi-Agent Dispatch

Dispatch tasks to remote VMs for parallel execution or specialized work.

## When to Use

- Task needs **specific VM** (GPU → epyc6, macOS → macmini)
- **Parallelize** work across VMs
- Need **status notifications** via Slack

## Quick Commands

```bash
# Dispatch task
dx-dispatch epyc6 "Run make test"
dx-dispatch macmini "Build iOS"

# Check VMs
dx-dispatch --list

# Resume session
dx-dispatch epyc6 "Continue" --session ses_xxx
```

## Slack Notifications

Include in task prompt:
```
After completing, use slack_conversations_add_message 
to post summary to channel C09MQGMFKDE.
```

## Full Guide

See [docs/MULTI_AGENT_COMMS.md](../../docs/MULTI_AGENT_COMMS.md)
