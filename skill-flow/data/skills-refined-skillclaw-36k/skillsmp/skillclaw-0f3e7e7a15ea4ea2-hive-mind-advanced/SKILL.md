---
name: hive-mind-advanced
description: Use this skill when you need to implement an advanced Hive Mind collective intelligence system for queen-led multi-agent coordination with consensus mechanisms and persistent memory.
---

# Hive Mind Advanced Skill

Master the advanced Hive Mind collective intelligence system for sophisticated multi-agent coordination using queen-led architecture, Byzantine consensus, and collective memory.

## Overview

The Hive Mind system represents the pinnacle of multi-agent coordination in Claude Flow, implementing a queen-led hierarchical architecture where a strategic queen coordinator directs specialized worker agents through collective decision-making and shared memory.

## Core Concepts

### Architecture Patterns

**Queen-Led Coordination**
- Strategic queen agents orchestrate high-level objectives.
- Tactical queens manage mid-level execution.
- Adaptive queens dynamically adjust strategies based on performance.

**Worker Specialization**
- Researcher agents: Analysis and investigation.
- Coder agents: Implementation and development.
- Analyst agents: Data processing and metrics.
- Tester agents: Quality assurance and validation.
- Architect agents: System design and planning.
- Reviewer agents: Code review and improvement.
- Optimizer agents: Performance enhancement.
- Documenter agents: Documentation generation.

**Collective Memory System**
- Shared knowledge base across all agents.
- LRU cache with memory pressure handling.
- SQLite persistence with WAL mode.
- Memory consolidation and association.
- Access pattern tracking and optimization.

### Consensus Mechanisms

**Majority Consensus**
- Simple voting where the option with the most votes wins.

**Weighted Consensus**
- Queen vote counts as 3x weight, providing strategic guidance.

**Byzantine Fault Tolerance**
- Requires 2/3 majority for decision approval, ensuring robust consensus even with faulty agents.

## Prerequisites

### Claude-Flow MCP Server Configuration

For MCP-based agent spawning (recommended), the Claude-Flow MCP server must be configured:

**Option A - Via CLI:**
```bash
claude mcp add claude-flow -- npx claude-flow@alpha mcp start
```

**Option B - Via .mcp.json (recommended for projects):**
```json
{
  "mcpServers": {
    "claude-flow": {
      "command": "npx",
      "args": ["claude-flow@alpha", "mcp", "start"]
    }
  }
}
```

## Hooks

### Pre-Execution
```bash
echo "🧠 Hive Mind Advanced activated"
if [ -d "/workspaces/ruvector/.claude/intelligence" ]; then
  cd /workspaces/ruvector/.claude/intelligence
  INTELLIGENCE_MODE=treatment node cli.js pre-edit "$FILE" 2>/dev/null || true
fi
```

### Post-Execution
```bash
echo "✅ Hive Mind Advanced complete"
if [ -d "/workspaces/ruvector/.claude/intelligence" ]; then
  cd /workspaces/ruvector/.claude/intelligence
  INTELLIGENCE_MODE=treatment node cli.js post-edit "$FILE" "true" 2>/dev/null || true
fi
```