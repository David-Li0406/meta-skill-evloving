# MCP Integration

## Overview

Add MCP server capabilities to CLI tools. Expose CLI functionality as MCP tools with auto-generated schemas.

## withMcp Configuration

```typescript
.withMcp({
  serverInfo: { name: string, version: string, description?: string },
  defaultTransport?: McpTransportConfig,
  defaultTransports?: McpTransportConfig[],
  toolOptions?: GenerateMcpToolsOptions,
  log?: string | McpLoggerOptions,
  logPath?: LogPath,
  lifecycle?: McpLifecycleEvents,
  dxt?: DxtOptions,
  httpServer?: HttpServerOptions
})
```

## Transport Types

```typescript
// STDIO transport (default)
{ type: "stdio" }

// SSE transport
{ type: "sse", host?: string, port?: number, path?: string }

// Streamable HTTP
{
  type: "streamable-http",
  host?: string,
  port?: number,
  path?: string,
  cors?: CorsOptions,
  auth?: AuthOptions
}
```

## Server Info

```typescript
{
  name: "my-cli",
  version: "1.0.0",
  description?: "My CLI description",
  author?: { name, email?, url? },
  repository?: { type: string, url: string },
  license?: "MIT",
  homepage?: string,
  documentation?: string,
  support?: string,
  keywords?: string[],
  logo?: string
}
```

## Unified Tools (CLI + MCP)

```typescript
.addTool({
  name: string,              // Auto-sanitized for MCP
  description?: string,
  flags: readonly IFlag[],
  handler: (ctx: IHandlerContext) => any,
  outputSchema?: OutputSchemaConfig
})
```

**Output schema patterns:**

- `"successError"` - `{ success: boolean, message?, error? }`
- `"successWithData"` - `{ success: boolean, data: any, message?, error? }`
- `"list"` - `{ items: any[], count?, hasMore? }`
- `"fileOperation"` - `{ path: string, size?, created?, modified?, exists? }`
- `"processExecution"` - `{ exitCode: number, stdout?, stderr?, duration?, command? }`

## Generate MCP Tools

```typescript
// Auto-generate from CLI structure
const tools = parser.toMcpTools({
  defaultOutputSchema: "successWithData",
  outputSchemaMap: { toolName: z.object({...}) },
  autoGenerateOutputSchema: true
})

// Register tools
server.registerTool(tool.name, { description, inputSchema }, tool.execute)
```

## MCP Logging

```typescript
import { createMcpLogger, logger } from "@alcyone-labs/arg-parser";

// Create logger
const mcpLogger = createMcpLogger("MyServer", "./logs/mcp.log");

// Use in handler
mcpLogger.info("Processing request");
mcpLogger.error("Failed", error);

// Or use exported logger
logger.info("Message");
logger.error("Error", error);
```

## Console Hijacking

MCP mode hijacks `console` to prevent STDOUT contamination. Use logger instead.

## Lifecycle Events

```typescript
{
  onInitialize?: (clientInfo, protocolVersion, capabilities) => void,
  onInitialized?: () => void,
  onShutdown?: () => void,
  onServerInfo?: () => { name, version }
}
```

## DXT Options

```typescript
{
  include?: (string | { from: string, to: string })[]
}
```

## Error Handling

```typescript
// Create error response
createMcpErrorResponse(message);

// Create success response
createMcpSuccessResponse(content);
```

## Protocol Versions

- Output schemas require MCP >= 2025-06-18
- Use `parser.setMcpProtocolVersion(version)` for compatibility
