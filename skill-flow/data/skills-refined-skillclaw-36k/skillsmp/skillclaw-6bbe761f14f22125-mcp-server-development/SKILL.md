---
name: mcp-server-development
description: Use this skill when developing MCP (Model Context Protocol) servers with the TypeScript SDK, implementing tools, resources, or prompts, and ensuring compliance with the MCP specification.
---

# MCP Server Development Guide

## Overview

This guide provides comprehensive instructions for building robust MCP servers that enable LLMs to interact with external services. It covers server initialization, request handling, Zod schemas, error handling, and JSON-RPC patterns.

## High-Level Workflow

Creating a high-quality MCP server involves several key phases:

### Phase 1: Research and Planning

1. **Understand MCP Design Principles**
   - Balance API coverage with specialized workflow tools.
   - Use clear, descriptive tool names for discoverability.
   - Design tools for concise context management and actionable error messages.

2. **Study MCP Protocol Documentation**
   - Familiarize yourself with the MCP specification and key pages, including transport mechanisms and tool definitions.

3. **Select Your Technology Stack**
   - Recommended: TypeScript for its SDK support and static typing.
   - Use Streamable HTTP for remote servers and stdio for local servers.

### Phase 2: Implementation

1. **Server Initialization**
   ```typescript
   import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
   import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

   const server = new McpServer({
     name: "my-server",
     version: "1.0.0"
   });

   const transport = new StdioServerTransport();
   await server.connect(transport);
   ```

2. **Defining Tools**
   - Use Zod for input validation and define tools with clear schemas.
   ```typescript
   const ToolSchema = z.object({
     input: z.string().describe("Input parameter")
   });

   server.tool("my_tool", "Tool description", ToolSchema, async (args) => ({
     content: [{ type: "text", text: `Result: ${args.input}` }],
     structuredContent: { result: args.input }
   }));
   ```

3. **Error Handling**
   - Implement actionable error messages and ensure graceful error handling.
   ```typescript
   return {
     content: [{ type: "text", text: "Error: File not found" }],
     structuredContent: { error: "File not found", path: "/missing" },
     isError: true
   };
   ```

### Phase 3: Testing and Deployment

- Ensure your server is reliable, discoverable, and performant.
- Follow JSON-RPC 2.0 and MCP specifications strictly.

## Conclusion

This guide serves as a foundational resource for developing MCP servers, ensuring they are well-structured, compliant, and capable of bridging AI assistants with external systems.