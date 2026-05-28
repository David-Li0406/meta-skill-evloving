---
name: mcp-builder
description: Use this skill when creating Model Context Protocol (MCP) servers, adding tools to extend Claude's capabilities, or integrating external APIs as MCP tools.
---

# MCP Builder Skill

You have expertise in building Model Context Protocol servers to extend Claude's capabilities.

## When to Use

This skill activates for:

- Creating new MCP servers
- Adding tools to existing servers
- Integrating external APIs as MCP tools
- Configuring MCP servers in Claude Desktop/Code
- Debugging MCP server issues

## MCP Server Quickstart

### Project Setup

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
```

### Minimal Server Template

```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({ name: "my-server", version: "1.0.0" }, { capabilities: { tools: {} } });

// Define tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "my_tool",
      description: "What this tool does and when Claude should use it",
      inputSchema: {
        type: "object",
        properties: {
          param: { type: "string", description: "Parameter description" },
        },
        required: ["param"],
      },
    },
  ],
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "my_tool") {
    const { param } = request.params.arguments as { param: string };
    return {
      content: [{ type: "text", text: `Result for: ${param}` }],
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### package.json

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "bin": { "my-mcp-server": "./dist/index.js" },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["src/**/*"]
}
```

## Tool Design Patterns

### API Wrapper