# Start Agent Lens

## Quick Start

```bash
# Start server (Terminal 1)
cd ~/.claude/skills/agent-lens/apps/server
bun run dev

# Start client (Terminal 2)
cd ~/.claude/skills/agent-lens/apps/client
bun run dev

# Or use the convenience script from project root:
bun run start-obs
```

Open browser: **http://localhost:5173**

## Prerequisites

- Bun runtime installed
- Agent Lens skill configured
- Hooks enabled in `~/.claude/settings.json`

## What You'll See

- **Real-time event streaming** from Claude Code sessions
- **Dual-pane layout** (process timeline + metrics)
- **Hierarchical event visualization** with parent-child relationships
- **HITL approval interface** for human-in-the-loop requests
- **Performance metrics** (tokens, costs, latency)

## Documentation

See [SKILL.md](../SKILL.md) for complete documentation.
