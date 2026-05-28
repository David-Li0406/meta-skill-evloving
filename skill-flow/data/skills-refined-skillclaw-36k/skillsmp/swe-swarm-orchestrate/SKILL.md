---
name: swe-swarm-orchestrate
version: 1.0.0
description: Multi-agent swarm coordination for large tasks
workflow:
  aware: true
  callable_from:
    - WF_SWARM_ORCHESTRATE
  default_return: WF_EXECUTE
  supports_standalone: false
  auto_transition: true
---

# Swarm Orchestrate Skill

Coordinate multi-agent swarm for complex tasks.

## MCP Selection Priority

1. **Claude Flow** (preferred) - General orchestration
2. **RUV-Swarm** (fallback) - DAA learning agents
3. **Sequential** (no MCP) - Chunked execution

## Agent Types

| Agent | Purpose |
|-------|---------|
| researcher | Explore codebase |
| coder | Implement changes |
| analyst | Review patterns |
| optimizer | Performance tuning |
| coordinator | Orchestrate tasks |

## Swarm Topologies

- **mesh** - All agents connected (default)
- **hierarchical** - Tree structure
- **ring** - Circular communication
- **star** - Central coordinator

## Actions

1. **Select swarm system** based on available MCPs
2. **Decompose task** into parallel subtasks
3. **Spawn agents** (ALL in one message)
4. **Coordinate execution**
5. **Synthesize results**

## Critical Rules

- NEVER run `npx claude-flow init` - use MCP tools only
- Spawn agents in parallel (single message)
- Store state in WORKING_MEMORY

## Exit

`> **Skill /swe-swarm-orchestrate complete** - returning to WF_EXECUTE`
