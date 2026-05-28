---
id: mcp-model-context-protocol
name: "MCP (Model Context Protocol)"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

## MCP (Model Context Protocol)

### Problem

No standard way to connect LLMs to external tools/data.

### Solution: Model Context Protocol

**What is MCP?**
- Open protocol for LLM-tool communication
- Standardized tool definitions
- Secure context sharing
- Developed by Anthropic

**Components:**
```
MCP Server (tools/data) <-> MCP Client (Claude Code, etc.)
                              |
                           LLM Request
```

**Example MCP Server:**
```json
{
  "name": "database",
  "description": "Query company database",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"}
    }
  }
}
```

**Benefits:**
- Reusable tool definitions
- Security through protocol
- Composable capabilities
- Standard across clients
