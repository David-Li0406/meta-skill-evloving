# MCP Protocol & Marketplace Conventions

Reference guide for MCP (Model Context Protocol) fundamentals and SideQuest Marketplace conventions.

---

## What is MCP?

Model Context Protocol is a standardized way for Claude (and other LLMs) to interact with external tools and data sources.

### Core Concept

```
┌──────────┐                    ┌──────────────────┐
│  Claude  │ ◄──────JSON-RPC─► │  MCP Server      │
│  (Host)  │                    │  (Tool Provider) │
└──────────┘                    └──────────────────┘
     ▲                                     │
     │                                     │
     └─────── stdio / HTTP / SSE ─────────┘
```

1. **Claude (Host)** → Asks for available tools via `ListToolsRequest`
2. **MCP Server** → Returns list of tools with schemas
3. **Claude** → User calls a tool
4. **Claude → MCP Server** → Sends `CallToolRequest` with parameters
5. **MCP Server** → Executes tool, returns results
6. **Claude** → Formats response for user

### Why MCP?

- **Standardized interface** - All MCP servers work the same way
- **Type safety** - Input schemas prevent errors
- **Discoverability** - Claude can see available tools
- **Separation of concerns** - Tools are separate processes
- **Security** - Tools run with limited context
- **Scalability** - Add tools without modifying Claude

---

## MCP Terminology

### Tool

A function Claude can call. Has:
- **name**: Unique identifier (e.g., `mcp__git_git-intelligence__get_recent_commits`)
- **description**: What it does
- **inputSchema**: Parameters (JSON Schema)
- **annotations**: Metadata (readOnly, destructive, etc.)

### Resource

A reference to data (files, URLs, etc.). Tools can work with resources.

### Prompt

Pre-defined prompts that tools can suggest to users.

### Server

Subprocess that provides tools/resources. Communicates via stdio/HTTP/SSE.

### Host

Claude Code (or other LLM client) that uses MCP servers.

### Transport

Communication mechanism: stdio (pipe-based), HTTP (network), SSE (streaming).

---

## SideQuest Marketplace Conventions

### Directory Structure

**Standard:**

```
plugins/my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── mcp/                          )
│   └── my-server/
│       ├── index.ts
│       └── package.json
├── .mcp.json
├── package.json
└── CLAUDE.md
```

### Tool Naming Convention

```
mcp__<plugin-name>_<server-name>__<tool_name>
```

**Format:**
- `mcp__` = MCP prefix (required)
- `<plugin-name>` = kebab-case plugin name
- `_` = separator
- `<server-name>` = kebab-case server name
- `__` = separator (double underscore)
- `<tool_name>` = snake_case tool name

**Examples:**

```
mcp__git_git-intelligence__get_recent_commits
mcp__kit_kit__grep
mcp__biome-runner_biome-runner__lint_check
mcp__clipboard_clipboard__copy
```

### .mcp.json Format

```json
{
  "mcpServers": {
    "my-server": {
      "command": "bun",
      "args": ["run", "${CLAUDE_PLUGIN_ROOT}/mcp/my-server/index.ts"],
      "env": {}
    }
  }
}
```

**Critical:** Always use `${CLAUDE_PLUGIN_ROOT}` for relative paths. Claude Code sets this variable.

### Required Parameters

Every tool MUST support:

```typescript
response_format: z.enum(["markdown", "json"])
  .optional()
  .default("markdown")
```

This allows Claude to request data in either format.

### Error Response Format

All errors MUST return:

```json
{
  "error": "Human-readable message",
  "hint": "How to recover (optional)",
  "isError": true
}
```

With HTTP response flag:

```typescript
return {
  content: [{
    type: "text",
    text: JSON.stringify({ error: "...", isError: true })
  }],
  isError: true
};
```

---

## Tool Discovery & Registration

### How Claude Finds Tools

1. **Claude Code loads plugins** - Reads `.claude-plugin/plugin.json`
2. **Claude Code starts MCP servers** - Uses `.mcp.json` config
3. **Claude asks for tools** - Sends `ListToolsRequest`
4. **Server responds** - Returns tool list with schemas
5. **Claude registers tools** - Tools now available for use

### Tool Visibility

Tools are:
- ✅ Visible to Claude in context
- ✅ Callable by user directly
- ✅ Available to other plugins
- ✅ Integrated into help/discovery

---

## Plugin Integration

### plugin.json Registration

```json
{
  "name": "@sidequest/my-plugin",
  "version": "1.0.0",
  "description": "Description",
  "author": "Author",
  "commands": [
    {
      "name": "my-command",
      "description": "Command description",
      "file": "commands/my-command.md"
    }
  ],
  "skills": [
    {
      "name": "my-skill",
      "description": "Skill description",
      "file": "skills/my-skill/SKILL.md"
    }
  ],
  "hooks": [
    {
      "name": "my-hook",
      "file": "hooks/hooks.json"
    }
  ],
  "mcpServers": [
    {
      "name": "my-server",
      "description": "Server description",
      "configPath": ".mcp.json"
    }
  ]
}
```

---

## Testing in Marketplace

### Validation

```bash
# Validate all plugins
bun run validate

# Validate single plugin
claude plugin validate plugins/my-plugin

# Check specific issues
bun typecheck
```

**Checks include:**
- ✅ Tool naming convention
- ✅ response_format parameter
- ✅ .mcp.json syntax
- ✅ Directory structure
- ✅ TypeScript compilation

### Local Testing

```bash
# Start Claude Code with plugin
claude code plugins/my-plugin

# List available tools
/help  # Should show your tools

# Test tool directly
# Tool should appear in autocomplete
```

---

## Common Patterns

### Pattern: Single Tool Server

```typescript
// mcp/my-server/index.ts
const server = new Server({
  name: "my-server",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "mcp__my_my-server__do_something",
    description: "Does something useful",
    inputSchema: {
      type: "object",
      properties: {
        input: { type: "string" },
        response_format: { type: "string", enum: ["markdown", "json"] }
      },
      required: ["input"]
    }
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // Handle tool call
});
```

### Pattern: Multi-Tool Server

```typescript
// Each tool in separate file for clarity
import { searchTool } from "./tools/search.js";
import { indexTool } from "./tools/index.js";

const tools = [
  searchTool,
  indexTool,
  // Add more tools here
];

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools
}));
```

---

## Protocol Details

### ListToolsRequest

Claude asks: "What tools do you provide?"

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

**Server Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "mcp__...",
        "description": "...",
        "inputSchema": { /* ... */ }
      }
    ]
  }
}
```

### CallToolRequest

Claude asks: "Please execute this tool"

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "mcp__git_git-intelligence__get_recent_commits",
    "arguments": {
      "limit": 10,
      "response_format": "json"
    }
  }
}
```

**Server Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[JSON or markdown result here]"
      }
    ]
  }
}
```

---

## Marketplace Submission

### Requirements

1. **Valid plugin.json** - Metadata complete
2. **Tool naming convention** - `mcp__<name>_<server>__<tool>`
3. **response_format support** - Every tool accepts this parameter
4. **Error handling** - Proper error responses with isError flag
5. **Documentation** - Clear descriptions for all tools
6. **Tests** - Basic tests for each tool
7. **No circular deps** - Tools don't require each other's plugins

### Quality Checks

- ✅ Validation passes: `bun run validate`
- ✅ Build succeeds: `bun run ci:full`
- ✅ Tests pass: `bun test`
- ✅ No TypeScript errors: `bun typecheck`
- ✅ Code is formatted: `biome format`

---

## Common Issues

### Issue: Tool Not Appearing

**Check:**
1. Tool name matches pattern `mcp__*`
2. ListToolsRequestSchema handler is implemented
3. .mcp.json syntax is valid
4. Server starts without errors
5. Tool has proper inputSchema

**Debug:**
```bash
# Test server directly
bun run mcp/my-server/index.ts

# Check .mcp.json
cat .mcp.json

# Validate plugin
claude plugin validate plugins/my-plugin
```

### Issue: Tool Crashes on Call

**Check:**
1. Handler has try/catch
2. Error response has isError: true
3. Arguments match inputSchema
4. No async/await issues

**Debug:**
```typescript
// Add logging
console.error("Tool failed:", error);

// Test with simple data
const result = await executeTool({ input: "test" });
```

### Issue: response_format Not Working

**Check:**
1. Zod schema includes response_format
2. Handler respects response_format parameter
3. Default is "markdown"

**Fix:**
```typescript
const inputSchema = z.object({
  // ... other fields
  response_format: z.enum(["markdown", "json"])
    .optional()
    .default("markdown")  // REQUIRED!
});

// In handler
const format = args.response_format || "markdown";
```

---

## Best Practices

### 1. Tool Naming

```typescript
// ✓ Good: Clear and specific
"mcp__git_git-intelligence__get_recent_commits"

// ✗ Bad: Too generic
"mcp__git_git-intelligence__get"
```

### 2. Error Messages

```typescript
// ✓ Good: Helpful and specific
{
  error: "Invalid query format. Expected JSON object.",
  hint: "Check that query is properly formatted.",
  isError: true
}

// ✗ Bad: Generic
{ error: "Error", isError: true }
```

### 3. Documentation

```typescript
// ✓ Good: Clear and detailed
{
  name: "mcp__search_fileserver__search_files",
  description: "Search files by name or content. Supports regex patterns in queries.",
  inputSchema: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Search pattern (supports regex)"
      },
      limit: {
        type: "number",
        description: "Max results to return (1-100, default 20)"
      }
    }
  }
}

// ✗ Bad: Vague
{
  name: "search",
  description: "Search",
  inputSchema: { /* ... */ }
}
```

### 4. Schema Validation

```typescript
// ✓ Good: Clear constraints
z.object({
  query: z.string().min(1).max(1000),
  limit: z.number().int().min(1).max(100)
})

// ✗ Bad: No validation
z.object({
  query: z.any(),
  limit: z.any()
})
```

---

## Summary

MCP enables:

- ✅ Standard tool interface
- ✅ Type-safe schemas
- ✅ Discovery and documentation
- ✅ Standardized error handling
- ✅ Multi-format responses

**Key marketplace conventions:**

1. **Directory:** Use `mcp/` not `mcp-servers/`
2. **Naming:** Follow `mcp__<name>_<server>__<tool>` pattern
3. **Parameters:** Always support `response_format`
4. **Errors:** Return `{ error, hint, isError: true }`
5. **Paths:** Use `${CLAUDE_PLUGIN_ROOT}` in .mcp.json

**Next steps:**

- Study Kit plugin implementation: @./kit-case-study.md
- Review mcpez API: @./mcpez-patterns.md
- Learn error handling: @./error-handling.md
- Review main skill: @../SKILL.md
