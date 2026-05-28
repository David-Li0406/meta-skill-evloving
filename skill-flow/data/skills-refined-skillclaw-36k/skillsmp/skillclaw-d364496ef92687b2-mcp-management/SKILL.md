---
name: mcp-management
description: Use this skill to manage Model Context Protocol (MCP) servers by discovering, analyzing, and executing tools, prompts, and resources from configured MCP servers.
---

# MCP Management

Skill for managing and interacting with Model Context Protocol (MCP) servers.

## Overview

MCP is an open protocol enabling AI agents to connect to external tools and data sources. This skill provides scripts and utilities to discover, analyze, and execute MCP capabilities from configured servers without polluting the main context window.

**Key Benefits**:
- Progressive disclosure of MCP capabilities (load only what's needed)
- Intelligent tool/prompt/resource selection based on task requirements
- Multi-server management from a single config file
- Context-efficient: subagents handle MCP discovery and execution
- Persistent tool catalog: automatically saves discovered tools to JSON for fast reference

## When to Use This Skill

Use this skill when:
1. **Discovering MCP Capabilities**: Need to list available tools, prompts, or resources from configured servers.
2. **Task-Based Tool Selection**: Analyzing which MCP tools are relevant for a specific task.
3. **Executing MCP Tools**: Calling MCP tools programmatically with proper parameter handling.
4. **MCP Integration**: Building or debugging MCP client implementations.
5. **Context Management**: Avoiding context pollution by delegating MCP operations to subagents.

## Core Capabilities

### 1. Configuration Management

MCP servers are configured in `.opencode/.mcp.json`.

**Gemini CLI Integration** (recommended): Create a symlink to `.gemini/settings.json`:
```bash
mkdir -p .gemini && ln -sf .opencode/.mcp.json .gemini/settings.json
```

**GEMINI.md Response Format**: The project root contains `GEMINI.md` that Gemini CLI auto-loads, enforcing structured JSON responses:
```json
{"server":"name","tool":"name","success":true,"result":<data>,"error":null}
```

### 2. Capability Discovery

Use the following commands to aggregate capabilities from multiple servers:
```bash
npx tsx scripts/cli.ts list-tools  # Saves to assets/tools.json
npx tsx scripts/cli.ts list-prompts
npx tsx scripts/cli.ts list-resources
```

### 3. Intelligent Tool Analysis

The LLM analyzes `assets/tools.json` directly to provide insights on tool relevance and usage.