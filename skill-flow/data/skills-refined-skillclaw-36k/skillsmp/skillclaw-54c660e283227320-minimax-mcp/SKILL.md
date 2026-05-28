---
name: minimax-mcp
description: Use this skill for efficient MiniMax MCP server integration, enabling token-efficient AI delegation for web searches, image analysis, and collaborative tasks with Claude.
---

# MiniMax MCP

## Overview

This skill provides complete MiniMax MCP server integration for Claude, enabling token-efficient AI delegation with 85-90% token savings. MiniMax handles heavy computational tasks while Claude plans and reviews, creating an optimal division of labor.

## Usage Guidance

### When to Prefer MiniMax
Consider delegating these tasks to MiniMax for better efficiency:

1. **Web search or research queries** - MiniMax handles external searches well.
2. **Image analysis tasks** - MiniMax VLM API provides visual understanding.
3. **Multi-source research** - When you'd otherwise read 5+ files.
4. **Current information needs** - Docs, trends, releases from 2024-2026.

### When NOT to Delegate
- HPV playtesting or MCP runtime inspection (requires local control and fast feedback).
- Iterative input loops where latency ruins the feedback cycle (batch locally instead).

### Trusted Domains (Auto-Approved)
These sources are reliable and searches are **automatically restricted** to these domains:
- `docs.anthropic.com` - Claude official docs
- `platform.claude.com` - Claude platform docs
- `docs.cursor.com` - Cursor IDE docs
- `cursor.com` - Cursor docs
- `cookbook.openai.com` - OpenAI cookbook
- `godotengine.org` - Godot official docs
- `api.minimax.io` - MiniMax API docs

**Implementation**: The `web-search.sh` script automatically appends `site:` filters to all queries, ensuring results only come from trusted domains. To search other domains, ask Sam for permission and use an alternative search method.

### Decision Trigger
Before using Grep/Glob for research, pause and ask:
> "Would a MiniMax search to trusted docs handle this better?"

If yes → use MiniMax. If searching known local files → use local tools.

### Example Pattern

**Local file task** (use Grep/Read):
```
User: "Find where player_health is defined"
Agent: *Uses Grep to search codebase* ✅
```

**Research task** (use MiniMax):
```
User: "How does Godot 4.5 handle input?"
Agent: *Calls MiniMax search: site:godotengine.org input handling*
MiniMax: *Returns official docs*
Agent: *Reviews results* ✅
```

## Core Capabilities

### 1. MCP Server Integration
- **Launch MCP Server**: Start MiniMax MCP server with appropriate parameters.