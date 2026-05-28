---
name: mcp-deepwiki
description: Access and query GitHub repository documentation using DeepWiki's AI-powered knowledge base. Provides 3 tools for browsing documentation structure, viewing content, and asking questions.
allowed-tools: Bash, Read
---

# DeepWiki

Access and query GitHub repository documentation using DeepWiki's AI-powered knowledge base. Provides structured documentation browsing, content viewing, and natural language Q&A for any public GitHub repository.

**Version**: 0.0.1 (locked 2026-01-20)

## When to Use This Skill

Use this skill when you need to:
- Explore documentation structure of a GitHub repository
- Read comprehensive documentation about a GitHub project
- Ask specific questions about a repository's features, architecture, or usage
- Understand unfamiliar libraries or frameworks through AI-assisted documentation

## Tools

| Tool | Description |
|------|-------------|
| [read_wiki_structure](./tools/read_wiki_structure.md) | Get a list of documentation topics for a GitHub repository |
| [read_wiki_contents](./tools/read_wiki_contents.md) | View documentation about a GitHub repository |
| [ask_question](./tools/ask_question.md) | Ask any question about a GitHub repository |

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
