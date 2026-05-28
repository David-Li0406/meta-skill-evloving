---
name: mcp-grep
description: Search over a million GitHub repositories for real-world code examples using grep.app. Find literal code patterns, usage examples, and implementation patterns across popular open-source projects. Perfect for discovering how developers use specific APIs, libraries, or coding patterns.
version: 1.0.0
author: MCP Skill Generator
tags: [mcp, github, code-search, examples, grep]
allowed-tools: Bash, Read
---

# MCP Grep - GitHub Code Search

Search over a million public GitHub repositories for real-world code examples and usage patterns.

**Version**: 0.1.0 (locked 2026-01-20)

## Overview

This skill provides access to [grep.app](https://grep.app), a GitHub code search service that helps you find actual code implementations across a massive collection of repositories. Unlike keyword search, this tool searches for **literal code patterns** - the exact text that appears in source files.

**Key Features:**
- Search literal code patterns (like `grep`)
- Support for regular expressions
- Filter by language, repository, or file path
- Case-sensitive and whole-word matching options
- Multi-line pattern matching with regex

## Tools

| Tool | Description |
|------|-------------|
| [searchGitHub](./tools/searchGitHub.md) | Find real-world code examples by searching for literal code patterns |

**⚠️ Always check [tools/](./tools/) for exact parameter names before calling.**

## Use Cases

- **API Usage Examples**: Find how developers use unfamiliar APIs or libraries
- **Syntax Reference**: Check correct syntax, parameters, or configuration
- **Best Practices**: Discover production-ready implementation patterns
- **Integration Examples**: See how different libraries work together

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

## Search Tips

### Good Search Patterns (Literal Code)
- ✅ `useState(` - Find React useState calls
- ✅ `import React from` - Find React imports
- ✅ `async function` - Find async function declarations
- ✅ `(?s)try {.*await` - Find try-catch with await (regex)

### Bad Search Patterns (Keywords)
- ❌ `react tutorial` - Not literal code
- ❌ `best practices` - Too generic
- ❌ `how to use` - Natural language query

### Using Regex

Enable regex mode with `useRegexp: true` for advanced patterns:

```bash
# Multi-line pattern (prefix with (?s))
node ./scripts/mcp-caller.mjs call searchGitHub '{"query":"(?s)useState\\(.*loading","useRegexp":true}'
```

## Configuration

Connection settings are in `config.toml`:

```toml
transport = "http"
url = "https://mcp.grep.app"
```

No authentication required for basic usage. If API key support is added in the future, use the `MCP_GREP_API_KEY` environment variable.

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

## References

- [grep.app](https://grep.app) - Official web interface
- [Vercel Blog: Grep a Million GitHub Repositories via MCP](https://vercel.com/blog/grep-a-million-github-repositories-via-mcp)
- [MCP Documentation](https://modelcontextprotocol.io)

## Limitations

- Searches literal code patterns, not semantic understanding
- Results depend on indexed repositories (may not include very recent commits)
- Regular expressions must be supported by the service's regex engine
