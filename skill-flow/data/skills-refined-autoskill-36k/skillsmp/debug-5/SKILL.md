---
name: debug
description: Stream real-time debug events from the Vocal Bridge voice agent. Shows transcriptions, agent responses, tool calls, and errors.
allowed-tools: Bash
---

Stream real-time debug events from the voice agent.

First ensure CLI is installed:

```bash
pip install --upgrade vocal-bridge
```

Then run:

```bash
vb debug $ARGUMENTS
```

This command runs continuously until interrupted (Ctrl+C).

## Options

- `--poll` - Use HTTP polling instead of WebSocket
- `-i 0.5` - Poll interval in seconds (default 0.5, only used with --poll)

## Event Types

The debug stream shows:
- **USER** - User transcriptions (what the caller said)
- **AGENT** - Agent responses (what the agent said)
- **TOOL** - Tool calls made by the agent
- **RESULT** - Tool call results
- **BG QUERY** - Background LLM queries (concierge modes)
- **BG RESULT** - Background query results
- **ERROR** - Errors encountered
- **SESSION** - Session start/end events
- **STATE** - State changes
- **HOLD** - Hold started/ended

## Prerequisites

Debug mode must be enabled in the agent's Capabilities settings at https://vocalbridgeai.com

To enable:
1. Go to your agent in the Vocal Bridge dashboard
2. Click 'Edit'
3. Enable 'Debug Mode' in the Capabilities section
4. Save changes
