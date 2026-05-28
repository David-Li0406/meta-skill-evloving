---
name: memory-mcp
description: Use this skill when you need to interact with and troubleshoot the Memory MCP server for episodic memory retrieval and pattern analysis.
---

# Memory MCP Server

Interact with and troubleshoot the Memory Model Context Protocol (MCP) server for the self-learning memory system.

## When to Use

- Starting or configuring the memory-mcp server
- Using MCP tools for memory retrieval and pattern analysis
- Validating the MCP server implementation
- Debugging MCP server issues (connection, tool execution, performance)
- Testing MCP tools using the MCP inspector
- Understanding MCP configuration and environment variables

## MCP Server Overview

The memory-mcp server exposes episodic memory functionality through the Model Context Protocol, allowing AI agents to:
- Query past experiences and learned patterns
- Analyze successful strategies from historical episodes
- Execute code in a secure sandbox environment
- Perform advanced statistical and predictive analysis
- Monitor server health and metrics

**Location**: `./target/release/memory-mcp-server`  
**Configuration**: `.mcp.json`  
**Transport**: stdio (Standard Input/Output)

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `query_memory` | Query episodic memory for relevant past experiences |
| `analyze_patterns` | Analyze patterns from past episodes |
| `advanced_pattern_analysis` | Perform statistical analysis and predictive modeling |
| `execute_agent_code` | Execute TypeScript/JavaScript in a secure sandbox |
| `health_check` | Check server health status |
| `get_metrics` | Retrieve comprehensive monitoring metrics |

## Starting the Server

```bash
# Build
cargo build --release --bin memory-mcp-server

# Run directly
export TURSO_DATABASE_URL="file:./data/memory.db"
./target/release/memory-mcp-server

# Run via MCP Inspector for testing
npx -y @modelcontextprotocol/inspector ./target/release/memory-mcp-server
```