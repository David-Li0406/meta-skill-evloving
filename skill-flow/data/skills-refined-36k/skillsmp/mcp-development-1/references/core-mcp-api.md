# @sidequest/core/mcp API Reference

Complete API reference for `@sidequest/core/mcp`, the Side Quest MCP toolkit with built-in observability.

---

## Installation

```bash
# In a Side Quest plugin
bun add @sidequest/core
```

---

## Imports

All MCP functionality is exported from a single entry point:

```typescript
import {
  // Server
  startServer,

  // Tool registration
  tool,

  // Schema
  z,

  // Observability
  log,
  createCorrelationId,
} from "@sidequest/core/mcp";
```

### CLI Wrapper Imports (for tools that wrap external CLIs)

```typescript
import { buildEnhancedPath, spawnSyncCollect } from "@sidequest/core/spawn";

// buildEnhancedPath() - Returns PATH with uv, Homebrew, and common tool directories
// spawnSyncCollect() - Executes command and collects stdout/stderr
```

---

## Server Creation

### startServer()

Start an MCP server with optional file logging:

```typescript
startServer("my-plugin", {
  version: "1.0.0",
  fileLogging: {
    enabled: true,
    subsystems: ["search", "index", "api"],
    level: "debug",
    maxSize: 10_000_000,  // 10MB
    maxFiles: 5,
  },
});
```

### ServerConfig

```typescript
interface ServerConfig {
  version: string;        // Semantic version (e.g., "1.0.0")
  fileLogging?: FileLoggingConfig;
}

interface FileLoggingConfig {
  enabled: boolean;       // Enable file logging
  subsystems?: string[];  // Named loggers for hierarchical filtering
  level?: LogLevel;       // "debug" | "info" | "warning" | "error"
  maxSize?: number;       // Max file size in bytes (default: 10MB)
  maxFiles?: number;      // Max rotated files (default: 5)
}
```

---

## Tool Registration

### tool()

Register a tool with the MCP server:

```typescript
tool(
  "my_tool",                    // Tool name
  {
    description: "What it does",
    inputSchema: z.object({...}),
    annotations: {...},
  },
  async (args) => {             // Handler
    return { content: [...] };
  },
);
```

### Full Example

```typescript
import {
  createCorrelationId,
  log,
  startServer,
  tool,
  z,
} from "@sidequest/core/mcp";

tool(
  "search",
  {
    description: "Search the codebase for patterns",
    inputSchema: z.object({
      query: z.string().describe("Search query"),
      limit: z.number().optional().describe("Max results (default: 20)"),
      response_format: z
        .enum(["markdown", "json"])
        .optional()
        .describe("Output format: 'markdown' (default) or 'json'"),
    }),
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async (args: Record<string, unknown>) => {
    const { query, limit = 20, response_format } = args as {
      query: string;
      limit?: number;
      response_format?: string;
    };

    const cid = createCorrelationId();
    const startTime = Date.now();
    log.info({ cid, tool: "search", args: { query, limit } }, "search");

    try {
      const results = await performSearch(query, limit);
      const durationMs = Date.now() - startTime;
      log.info({ cid, tool: "search", success: true, durationMs }, "search");

      const text = response_format === "json"
        ? JSON.stringify(results)
        : formatAsMarkdown(results);

      return { content: [{ type: "text" as const, text }] };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      log.error({ cid, tool: "search", error: errorMessage }, "search");

      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({
            error: errorMessage,
            hint: "Check your query syntax",
            isError: true,
          }),
        }],
        isError: true,
      };
    }
  },
);

startServer("my-plugin", {
  version: "1.0.0",
  fileLogging: {
    enabled: true,
    subsystems: ["search"],
    level: "debug",
  },
});
```

---

## Input Schemas

### Zod Schema

Use the re-exported `z` from `@sidequest/core/mcp`:

```typescript
import { z } from "@sidequest/core/mcp";

const searchSchema = z.object({
  // Required string
  query: z.string().describe("Search query"),

  // Optional number with default
  limit: z.number().optional().default(20).describe("Max results"),

  // Enum
  type: z.enum(["file", "function", "class"]).optional(),

  // Boolean with default
  caseSensitive: z.boolean().optional().default(false),

  // Array
  tags: z.array(z.string()).optional(),

  // Nested object
  filters: z.object({
    minSize: z.number().optional(),
    maxSize: z.number().optional(),
  }).optional(),

  // Standard response_format parameter
  response_format: z
    .enum(["markdown", "json"])
    .optional()
    .describe("Output format: 'markdown' (default) or 'json'"),
});
```

### Best Practices

1. **Always add `.describe()`** - Helps LLMs understand parameters
2. **Always include `response_format`** - Support both markdown and JSON
3. **Use `.optional()` for non-required params** - Be explicit about requirements

---

## Annotations

### ToolAnnotations

```typescript
interface ToolAnnotations {
  readOnlyHint?: boolean;      // No system modifications (default: false)
  destructiveHint?: boolean;   // Deletes or modifies data (default: false)
  idempotentHint?: boolean;    // Safe to call multiple times (default: false)
  openWorldHint?: boolean;     // Affects external systems (default: false)
}
```

### Examples

```typescript
// Safe read-only tool (search, get, list)
annotations: {
  readOnlyHint: true,
  destructiveHint: false,
  idempotentHint: true,
  openWorldHint: false,
}

// Destructive tool (delete, remove)
annotations: {
  readOnlyHint: false,
  destructiveHint: true,
  idempotentHint: true,   // Safe if already deleted
  openWorldHint: true,    // File system effects
}

// Mutating tool (create, update)
annotations: {
  readOnlyHint: false,
  destructiveHint: false,
  idempotentHint: false,  // May have side effects
  openWorldHint: true,
}
```

---

## Observability

### log API

The `log` object provides methods for each log level:

```typescript
import { log } from "@sidequest/core/mcp";

// Log with subsystem (second argument)
log.debug({ cid, details: "..." }, "search");
log.info({ cid, tool: "my_tool", args }, "search");
log.warning({ cid, issue: "..." }, "search");
log.error({ cid, error: "..." }, "search");
```

### createCorrelationId()

Generate unique IDs for request tracing:

```typescript
import { createCorrelationId } from "@sidequest/core/mcp";

const cid = createCorrelationId();  // e.g., "abc123"
```

### Subsystems

Subsystems create hierarchical loggers for filtering:

```typescript
// 1. Register subsystems in startServer
startServer("kit", {
  fileLogging: {
    enabled: true,
    subsystems: ["grep", "semantic", "symbols", "ast"],
  },
});

// 2. Use subsystem name as second argument
log.info({ cid, pattern }, "grep");      // -> kit.grep
log.info({ cid, query }, "semantic");    // -> kit.semantic
log.debug({ cid, symbol }, "symbols");   // -> kit.symbols
```

### Log Location

Logs are written to: `~/.claude/logs/<plugin-name>.jsonl`

Format (JSONL):
```json
{"timestamp":"2024-01-15T10:30:00.000Z","level":"info","logger":"kit.grep","cid":"abc123","pattern":"test"}
```

### Viewing Logs

```bash
# Tail logs in real-time
tail -f ~/.claude/logs/kit.jsonl | jq

# Filter by subsystem
cat ~/.claude/logs/kit.jsonl | jq 'select(.logger | contains("grep"))'

# Filter by correlation ID
cat ~/.claude/logs/kit.jsonl | jq 'select(.cid == "abc123")'

# Filter errors only
cat ~/.claude/logs/kit.jsonl | jq 'select(.level == "error")'
```

---

## Response Format

### Success Response

```typescript
return {
  content: [{ type: "text" as const, text }],
};
```

### Error Response

```typescript
return {
  content: [{
    type: "text" as const,
    text: JSON.stringify({
      error: "Human-readable error message",
      hint: "How to recover",
      isError: true,
    }),
  }],
  isError: true,
};
```

### Format Negotiation

Always respect the `response_format` parameter:

```typescript
const text = response_format === "json"
  ? JSON.stringify(result)
  : formatAsMarkdown(result);

return { content: [{ type: "text" as const, text }] };
```

---

## Error Handling

### Pattern: Try/Catch with Logging

```typescript
async (args: Record<string, unknown>) => {
  const { query } = args as { query: string };
  const cid = createCorrelationId();

  log.info({ cid, tool: "search", args: { query } }, "search");

  try {
    const result = await execute(query);
    log.info({ cid, tool: "search", success: true }, "search");
    return { content: [{ type: "text" as const, text: JSON.stringify(result) }] };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    log.error({ cid, tool: "search", error: errorMessage }, "search");

    return {
      content: [{
        type: "text" as const,
        text: JSON.stringify({
          error: errorMessage,
          hint: "Recovery suggestion",
          isError: true,
        }),
      }],
      isError: true,
    };
  }
}
```

### Pattern: Custom Error Types

```typescript
class ToolError extends Error {
  constructor(
    message: string,
    public code: string,
    public hint?: string,
  ) {
    super(message);
    this.name = "ToolError";
  }
}

// Usage
if (!query) {
  throw new ToolError(
    "Query is required",
    "INVALID_INPUT",
    "Provide a non-empty search query",
  );
}
```

---

## Common Patterns

### Pattern: Timeout Handling

```typescript
const withTimeout = <T>(promise: Promise<T>, ms: number): Promise<T> => {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error("Timeout")), ms),
    ),
  ]);
};

// Usage
const result = await withTimeout(execute(query), 30_000);
```

### Pattern: Graceful Degradation

```typescript
try {
  return await semanticSearch(query);
} catch (error) {
  const msg = error instanceof Error ? error.message : String(error);
  if (msg.includes("not available")) {
    log.warning({ cid, fallback: "grep", reason: msg }, "search");
    return await grepSearch(query);
  }
  throw error;
}
```

### Pattern: Pagination

```typescript
const inputSchema = z.object({
  query: z.string(),
  limit: z.number().optional().default(20),
  offset: z.number().optional().default(0),
});

// Handler
const results = await search(query);
const paginated = results.slice(offset, offset + limit);

return {
  content: [{
    type: "text" as const,
    text: JSON.stringify({
      results: paginated,
      total: results.length,
      hasMore: offset + limit < results.length,
    }),
  }],
};
```

---

## Best Practices

### 1. Always Log with Correlation IDs

```typescript
const cid = createCorrelationId();
log.info({ cid, tool: "my_tool", args }, "subsystem");
// ... execute ...
log.info({ cid, tool: "my_tool", success: true, durationMs }, "subsystem");
```

### 2. Always Support response_format

```typescript
const text = response_format === "json"
  ? JSON.stringify(result)
  : formatAsMarkdown(result);
```

### 3. Always Provide Error Hints

```typescript
return {
  content: [{
    type: "text" as const,
    text: JSON.stringify({
      error: "File not found",
      hint: "Check the file path and ensure it exists",
      isError: true,
    }),
  }],
  isError: true,
};
```

### 4. Type Args Explicitly

```typescript
async (args: Record<string, unknown>) => {
  const { query, limit } = args as {
    query: string;
    limit?: number;
  };
  // ...
}
```

### 5. Use Subsystems for Organization

Group related tools under the same subsystem:

```typescript
// All file operations
log.info({ cid, ... }, "fileOps");

// All search operations
log.info({ cid, ... }, "search");

// All API calls
log.info({ cid, ... }, "api");
```

---

## CLI Wrapper Module (@sidequest/core/spawn)

For MCP tools that wrap external CLI programs:

### buildEnhancedPath()

Returns an enhanced PATH that includes common tool locations:

```typescript
import { buildEnhancedPath } from "@sidequest/core/spawn";

const enhancedPath = buildEnhancedPath();
// Includes: ~/.local/bin (uv), /opt/homebrew/bin, standard PATH
```

### spawnSyncCollect()

Executes a command and collects stdout/stderr:

```typescript
import { spawnSyncCollect } from "@sidequest/core/spawn";

const result = spawnSyncCollect(
  ["bun", "run", "script.ts", "--arg", value],
  { env: { PATH: buildEnhancedPath() } }
);

// result.exitCode - 0 for success, non-zero for error
// result.stdout - Standard output as string
// result.stderr - Standard error as string
```

### Complete CLI Wrapper Example (from Kit)

```typescript
import { createCorrelationId, log, tool, z } from "@sidequest/core/mcp";
import { buildEnhancedPath, spawnSyncCollect } from "@sidequest/core/spawn";

tool("my_cli_wrapper", {
  description: "Wraps external CLI tool",
  inputSchema: {
    query: z.string().describe("Query to pass to CLI"),
    response_format: z.enum(["markdown", "json"]).optional()
      .describe("Output format: 'markdown' (default) or 'json'"),
  },
  annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
}, async (args: Record<string, unknown>) => {
  const { query, response_format } = args as { query: string; response_format?: string };

  const cid = createCorrelationId();
  const startTime = Date.now();
  log.info({ cid, tool: "my_cli_wrapper", args: { query } }, "cli");

  const format = response_format === "json" ? "json" : "markdown";
  const pluginRoot = process.env.CLAUDE_PLUGIN_ROOT || ".";

  const result = spawnSyncCollect(
    ["bun", "run", `${pluginRoot}/src/cli.ts`, "search", query, "--format", format],
    { env: { PATH: buildEnhancedPath() } }
  );

  log.info({ cid, tool: "my_cli_wrapper", success: result.exitCode === 0, durationMs: Date.now() - startTime }, "cli");

  return {
    ...(result.exitCode !== 0 ? { isError: true } : {}),
    content: [{ type: "text" as const, text: result.exitCode === 0 ? result.stdout : result.stderr }],
  };
});
```

---

## Summary

`@sidequest/core/mcp` provides:

- **startServer()** - Start MCP server with observability
- **tool()** - Register tools with schemas and handlers
- **z** - Zod for type-safe schemas
- **log** - Hierarchical logging with subsystems
- **createCorrelationId()** - Request tracing

`@sidequest/core/spawn` provides:

- **buildEnhancedPath()** - Enhanced PATH for CLI discovery
- **spawnSyncCollect()** - Execute CLI and collect output

**Key patterns:**

1. Import from `@sidequest/core/mcp` for MCP functionality
2. Import from `@sidequest/core/spawn` for CLI wrappers
3. Use correlation IDs for request tracing
4. Log with subsystems for hierarchical filtering
5. Support both markdown and JSON response formats
6. Return structured errors with recovery hints

See Kit plugin for production examples: @./kit-case-study.md
