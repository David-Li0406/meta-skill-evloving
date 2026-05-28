---
name: context7-documentation-query
description: Use this skill to query up-to-date documentation and code examples for programming libraries using Context7.
---

# Context7 Documentation Query

This skill allows you to query up-to-date documentation and code examples for any programming library or framework using Context7's documentation service.

**Version**: 2.0.2 (locked 2026-01-20)

## Environment Variables (Optional)

Setting an API key is **recommended** for higher rate limits:

- `MCP_CONTEXT7_API_KEY`: Your Context7 API key (get a free key at https://context7.com/dashboard)

```bash
export MCP_CONTEXT7_API_KEY="ctx7sk_..."
```

**Without API key**: Works with lower rate limits (suitable for light usage)  
**With API key**: Higher rate limits, free tier is generous for most use cases

## Tools

| Tool | Description |
|------|-------------|
| [resolve-library-id](./tools/resolve-library-id.md) | Resolves a package/product name to a Context7-compatible library ID and returns matching libraries. |
| [query-docs](./tools/query-docs.md) | Retrieves and queries up-to-date documentation and code examples from Context7 for any programming library or framework. |

**⚠️ Always check [tools/](./tools/) for exact parameter names before calling.**

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

## Querying Documentation

To fetch up-to-date documentation and code examples, you must first resolve the library ID using the `resolve-library-id` tool. After obtaining the library ID, you can use the `query-docs` tool.

### Arguments Schema for `query-docs`

The schema below describes the `arguments` object in the request payload.

```json
{
  "type": "object",
  "properties": {
    "libraryId": {
      "type": "string",
      "description": "Exact Context7-compatible library ID (e.g., '/mongodb/docs', '/vercel/next.js', etc.) retrieved from 'resolve-library-id' or directly from user query."
    },
    "query": {
      "type": "string",
      "description": "The question or task you need help with. Be specific and include relevant details."
    }
  },
  "required": [
    "libraryId",
    "query"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

### Background Tasks

If the tool returns a task ID, poll the task status via the MCP request tool:

```json
{"server_id":"context7","method":"tasks/status","params":{"task_id":"<task_id>"}}
```

## Error Handling

If a tool call fails (e.g., "method not found", parameter changes):
1. Try to complete the task using other available tools.
2. Inform the user: "This skill may be outdated - MCP server API has changed."
3. The user needs to run mcp-skill-generator to update this skill.

**Do not retry failed calls repeatedly** - prioritize finding alternatives.

## Updating

To update this skill with newer MCP server version:
1. Run mcp-skill-generator.
2. Provide this skill's path for update.