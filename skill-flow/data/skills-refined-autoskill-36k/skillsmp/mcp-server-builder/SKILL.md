---
name: mcp-server-builder
description: |
  Build MCP (Model Context Protocol) servers with TypeScript SDK. Use when:
  - Creating new MCP servers for tools, resources, or prompts
  - Upgrading existing MCP servers to latest protocol (2025-11-25)
  - Implementing file operations, API integrations, or data providers
  - Adding structuredContent, outputSchema, or annotations to tools
  Triggers: "mcp server", "filesystem mcp", "tool server", "resource server"
---

# MCP Server Builder

Build production-ready MCP servers using `@modelcontextprotocol/sdk` TypeScript SDK.

## Quick Start

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0"
}, {
  capabilities: {
    tools: { listChanged: true },
    resources: { subscribe: false, listChanged: true }
  }
});

// Define tool with Zod schema
server.tool(
  "my_tool",
  "Tool description for LLM",
  { input: z.string().describe("Input parameter") },
  async (args) => ({
    content: [{ type: "text", text: `Result: ${args.input}` }],
    structuredContent: { result: args.input }
  })
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Tools

### Schema Definition
```typescript
const ToolSchema = z.object({
  path: z.string().describe("File path"),
  encoding: z.enum(["text", "base64"]).optional().default("text")
});

server.tool("read_file", "Read file contents", ToolSchema.shape, handler);
```

### Response Format
```typescript
// Success with structured content
return {
  content: [{ type: "text", text: "Human-readable result" }],
  structuredContent: { data: result, count: 42 }
};

// Error response
return {
  content: [{ type: "text", text: "Error: File not found" }],
  structuredContent: { error: "File not found", path: "/missing" },
  isError: true
};
```

### Tool Annotations (optional)
```typescript
server.tool("dangerous_action", "...", schema, handler, {
  annotations: {
    destructive: true,
    idempotent: false,
    readOnly: false
  }
});
```

## Resources

```typescript
server.resource(
  "workspace://project-info",
  "Project Information",
  async () => ({
    contents: [{
      uri: "workspace://project-info",
      mimeType: "text/plain",
      text: "Project details here"
    }]
  })
);
```

## Roots Protocol

Handle dynamic workspace directories from client:

```typescript
import { RootsListChangedNotificationSchema, type Root } from "@modelcontextprotocol/sdk/types.js";

server.server.setNotificationHandler(RootsListChangedNotificationSchema, async () => {
  const response = await server.server.listRoots();
  if (response?.roots) {
    updateAllowedDirectories(response.roots);
  }
});

server.server.oninitialized = async () => {
  const caps = server.server.getClientCapabilities();
  if (caps?.roots) {
    const response = await server.server.listRoots();
    // Initialize from roots
  }
};
```

## TypeScript Strict Mode

With `noUncheckedIndexedAccess: true`:

```typescript
// ❌ Wrong
if (results.length === 1) {
  text = results[0].path; // TS2532: possibly undefined
}

// ✅ Correct
if (results.length === 1) {
  const first = results[0];
  if (first) {
    text = first.path;
  }
}
```

## Error Handling Pattern

```typescript
function formatToolError(message: string, data: Record<string, unknown> = {}): CallToolResult {
  return {
    content: [{ type: "text", text: message }],
    structuredContent: { error: message, ...data },
    isError: true
  };
}

// Usage in tool handler
try {
  const validPath = await validatePath(args.path);
  // ... operation
} catch (error) {
  return formatToolError(
    `Error: ${error instanceof Error ? error.message : String(error)}`,
    { path: args.path }
  );
}
```

## Truncation for Large Responses

```typescript
const MAX_RESPONSE_CHARS = 100000;

function truncateContent(content: string, maxChars = MAX_RESPONSE_CHARS) {
  if (content.length <= maxChars) return { content, truncated: false };
  const notice = "[... truncated]";
  return {
    content: content.slice(0, maxChars - notice.length) + notice,
    truncated: true
  };
}
```

## References

For detailed protocol specification, see:
- `docs/mcp/specification/server/tools.mdx` - Tool definitions, outputSchema, structuredContent
- `docs/mcp/specification/server/resources.mdx` - Resource URIs, subscriptions, annotations
- `docs/mcp/specification/server/prompts.mdx` - Prompt templates and arguments
- `docs/mcp/specification/basic/lifecycle.mdx` - Initialization, capabilities, shutdown
- `docs/mcp/schema/schema.ts` - TypeScript type definitions
