---
name: mcp-fetch
description: Web content fetching and conversion to markdown for efficient LLM consumption. Provides 1 tool for fetching URLs and extracting content.
allowed-tools: Bash, Read
---

# MCP Fetch Server

Fetches URLs from the internet and converts web content to markdown format for easier LLM analysis. Supports chunked reading, raw HTML extraction, and content length control.

**Version**: 2025.4.7 (locked 2026-01-20)

## Tools

| Tool | Description |
|------|-------------|
| [fetch](./tools/fetch.md) | Fetches a URL from the internet and optionally extracts its contents as markdown |

**⚠️ Always check [tools/](./tools/) for exact parameter names before calling.**

## Prompts

| Prompt | Description |
|--------|-------------|
| fetch | Fetch a URL and extract its contents as markdown |

See [prompts.md](./prompts.md) for details.

## Usage

### Quick Start

**⚠️ Before calling any tool, read its documentation in [tools/](./tools/) to get the exact parameter names.**

```bash
# List available tools and their schemas
node ./scripts/mcp-caller.mjs list

# Then check tools/<tool-name>.md for parameter details
```

### CLI (Single Call)

Run from this skill directory:
```bash
node ./scripts/mcp-caller.mjs call <tool> '<json-args>'
node ./scripts/mcp-caller.mjs resource <uri>
node ./scripts/mcp-caller.mjs prompt <name> '<json-args>'
node ./scripts/mcp-caller.mjs list
```

Example:
```bash
node ./scripts/mcp-caller.mjs call fetch '{"url": "https://example.com"}'
```

### Programmatic (Batch/Parallel)

For batch operations or complex logic, use the API module:

```javascript
// example.mjs - Run from this skill directory
import { callTool, listTools } from './scripts/api.mjs';

// First, check available tools and their schemas
const tools = await listTools();
console.log(tools.map(t => ({ name: t.name, params: Object.keys(t.inputSchema?.properties || {}) })));

// Then call with correct parameters (see tools/*.md for details)
const result = await callTool('toolName', { /* check tools/toolName.md for params */ });

// Parallel calls
const results = await Promise.all([
  callTool('tool1', { /* params from tools/tool1.md */ }),
  callTool('tool2', { /* params from tools/tool2.md */ }),
]);

console.log(JSON.stringify(results, null, 2));
```

**Available API functions:**
- `callTool(name, args)` - Call a tool
- `listTools()` - List available tools (includes inputSchema with parameter info)
- `readResource(uri)` - Read a resource
- `listResources()` - List resources
- `getPrompt(name, args)` - Get a prompt
- `listPrompts()` - List prompts
- `close()` - Close connection (optional cleanup)

## Error Handling

If a tool call fails (e.g., "method not found", parameter changes):
1. Try to complete the task using other available tools
2. Inform user: "This skill may be outdated - MCP server API has changed"
3. User needs to run mcp-skill-generator to update this skill

**Do not retry failed calls repeatedly** - prioritize finding alternatives.

## Updating

To update this skill with newer MCP server version:
1. Run mcp-skill-generator
2. Provide this skill's path for update
