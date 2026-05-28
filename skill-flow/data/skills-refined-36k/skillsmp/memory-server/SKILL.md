---
name: memory-server
description: Personal knowledge base for storing code, architecture decisions,
  and research findings. Use when user says "remember this", "save to memory",
  "find in memory", "what did I learn about". Supports hierarchical tags.
---

# Memory Server

Your personal knowledge base at: {{SERVER_URL}}

## Usage

### Save Information
- "Remember this code snippet about React hooks"
- "Save to memory with tags cloudflare>workers, typescript"
- "Store this API documentation"

### Search & Retrieve
- "What did I save about Durable Objects?"
- "Find my notes on MCP transport"
- "List memories tagged with architecture"

## Available Tools

| Tool | Description |
|------|-------------|
| `add_memory` | Save new memory with name, content, optional URL and tags |
| `find_memories` | Search by query text and/or filter by tags |
| `list_memories` | Browse all memories with pagination |
| `get_memory` | Retrieve specific memory by ID |
| `add_tags` | Add tags to existing memory |
| `delete_memory` | Remove a memory |
| `update_url_content` | Refresh content from URL source |

## Tagging System

Use hierarchical tags for better organization:

```
parent>child format:
- cloudflare>workers
- cloudflare>d1
- mcp>transport
- mcp>tools
- programming>typescript
- architecture>sop
```

## Examples

### Save a Code Snippet
```
"Remember this Hono middleware pattern with tags hono, middleware, cloudflare>workers"
```

### Research Session
```
"What do I have saved about WebSocket implementation?"
"Save this new finding with tags real-time, websockets, durable-objects"
```
