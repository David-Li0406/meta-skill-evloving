---
name: mcp-development
description: Build production-grade MCP (Model Context Protocol) servers with observability, correlation ID tracing, and dual logging. Use when creating new MCP servers, adding tools to existing servers, implementing file logging, debugging MCP issues, wrapping CLI tools with spawnSyncCollect, or following Side Quest marketplace patterns. Covers @sidequest/core/mcp declarative API, @sidequest/core/spawn CLI wrapper patterns, Zod schemas, Bun runtime, and 9 gold standard patterns validated across Kit plugin (18 tools). Includes error handling, response format switching, MCP annotations, and graceful degradation.
---

# MCP Development Skill

Build production-grade MCP servers using `@sidequest/core/mcp` and Bun.

---

## Quick Start

```bash
/plugin-template:create my-plugin
cd plugins/my-plugin
```

Create `mcp/index.ts`:

```typescript
#!/usr/bin/env bun
import { createCorrelationId, log, startServer, tool, z } from "@sidequest/core/mcp";

tool("hello", {
  description: "A simple greeting tool",
  inputSchema: {
    name: z.string().describe("Name to greet"),
    response_format: z.enum(["markdown", "json"]).optional()
      .describe("Output format: 'markdown' (default) or 'json'"),
  },
  annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
}, async (args: Record<string, unknown>) => {
  const { name, response_format } = args as { name: string; response_format?: string };

  const cid = createCorrelationId();
  log.info({ cid, tool: "hello", args: { name } }, "greeting");

  const greeting = `Hello, ${name}!`;
  const text = response_format === "json" ? JSON.stringify({ greeting }) : `# Hello\n\n${greeting}`;

  log.info({ cid, tool: "hello", success: true }, "greeting");
  return { content: [{ type: "text" as const, text }] };
});

startServer("my-plugin", {
  version: "1.0.0",
  fileLogging: { enabled: true, subsystems: ["greeting"], level: "debug" },
});
```

Create `.mcp.json`:

```json
{
  "mcpServers": {
    "my-plugin": {
      "command": "bun",
      "args": ["run", "${CLAUDE_PLUGIN_ROOT}/mcp/index.ts"]
    }
  }
}
```

Test: `bun run mcp/index.ts`

---

## 6-Step Handler Pattern

Every handler follows this pattern:

```typescript
async (args: Record<string, unknown>) => {
  const { query, response_format } = args as { query: string; response_format?: string };

  // 1. Generate correlation ID
  const cid = createCorrelationId();
  const startTime = Date.now();

  // 2. Log request
  log.info({ cid, tool: "my_tool", args: { query } }, "search");

  try {
    // 3. Execute business logic
    const result = await doSomething(query);

    // 4. Format output
    const text = response_format === "json" ? JSON.stringify(result) : formatAsMarkdown(result);

    // 5. Log response
    log.info({ cid, tool: "my_tool", success: true, durationMs: Date.now() - startTime }, "search");

    // 6. Return MCP response
    return { content: [{ type: "text" as const, text }] };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    log.error({ cid, tool: "my_tool", error: errorMessage }, "search");

    return {
      content: [{ type: "text" as const, text: JSON.stringify({ error: errorMessage, hint: "Recovery action", isError: true }) }],
      isError: true
    };
  }
}
```

---

## Gold Standard Patterns

9 production-validated patterns from Kit plugin. See @./references/gold-standard-patterns.md for details.

| # | Pattern | Purpose |
|---|---------|---------|
| 1 | Declarative Tool Registration | Type-safe Zod schemas + MCP annotations |
| 2 | Correlation ID Tracing | Request tracking across logs |
| 3 | Structured Error Responses | `{ error, hint, isError: true }` |
| 4 | Response Format Switching | Markdown (default) + JSON |
| 5 | File Logging Configuration | Subsystem-based hierarchical logs |
| 6 | MCP Annotations | `readOnlyHint`, `destructiveHint`, etc. |
| 7 | No Nested Package.json | Avoid MCP discovery failures |
| 8 | Dual Logging | MCP protocol + file persistence |
| 9 | Separation of Concerns | Business logic vs MCP layer |

---

## Tool Registration

```typescript
tool("my_tool", {
  description: "What this tool does",
  inputSchema: {
    query: z.string().describe("Search query"),
    limit: z.number().optional().describe("Max results"),
    response_format: z.enum(["markdown", "json"]).optional()
      .describe("Output format: 'markdown' (default) or 'json'"),
  },
  annotations: {
    readOnlyHint: true,      // No side effects
    destructiveHint: false,  // Doesn't delete data
    idempotentHint: true,    // Safe to retry
    openWorldHint: false,    // Local only
  },
}, handler);
```

---

## File Logging

```typescript
startServer("my-plugin", {
  version: "1.0.0",
  fileLogging: {
    enabled: true,
    subsystems: ["search", "index", "api"],
    level: "debug",  // "debug" | "info" | "warning" | "error"
    maxSize: 10_000_000,  // 10MB
    maxFiles: 5,
  },
});
```

**Logs:** `~/.claude/logs/<plugin>.jsonl`

**View:** `tail -f ~/.claude/logs/my-plugin.jsonl | jq`

**Filter:** `jq 'select(.cid == "abc123")'`

---

## CLI Wrapper Pattern

For tools wrapping external CLIs:

```typescript
import { buildEnhancedPath, spawnSyncCollect } from "@sidequest/core/spawn";

const result = spawnSyncCollect(
  ["bun", "run", `${pluginRoot}/src/cli.ts`, "search", query],
  { env: { PATH: buildEnhancedPath() } }
);

return {
  ...(result.exitCode !== 0 ? { isError: true } : {}),
  content: [{ type: "text" as const, text: result.exitCode === 0 ? result.stdout : result.stderr }],
};
```

---

## Error Handling

For detailed error patterns, see @./references/error-handling.md.

**Quick pattern:**

```typescript
enum ToolError {
  InvalidInput = "INVALID_INPUT",
  NotFound = "NOT_FOUND",
  Timeout = "TIMEOUT",
  InternalError = "INTERNAL_ERROR",
}

// Return structured error
return {
  content: [{ type: "text", text: JSON.stringify({ error: msg, errorType, hint, isError: true }) }],
  isError: true
};
```

**Type guard:**

```typescript
type Result<T> = { ok: true; data: T } | { ok: false; error: string; hint?: string };
const isSuccess = <T>(r: Result<T>): r is { ok: true; data: T } => r.ok;
```

---

## Advanced Features

For complete examples, see @./references/core-mcp-api.md.

**Graceful degradation:**

```typescript
try {
  return await semanticSearch(query);
} catch (error) {
  if (error.message.includes("not available")) {
    log.warning({ cid, fallback: "grep" }, "search");
    return await grepSearch(query);
  }
  throw error;
}
```

**Timeout:**

```typescript
const withTimeout = <T>(promise: Promise<T>, ms: number) =>
  Promise.race([promise, new Promise<T>((_, reject) => setTimeout(() => reject(new Error("Timeout")), ms))]);
```

**ResponseFormat enum:**

```typescript
enum ResponseFormat { MARKDOWN = "markdown", JSON = "json" }
const format = response_format === "json" ? ResponseFormat.JSON : ResponseFormat.MARKDOWN;
```

---

## Testing

```typescript
import { describe, expect, test } from "bun:test";

describe("my-server", () => {
  test("executes tool", async () => {
    const result = await callTool("mcp__my-plugin_my-server__hello", { name: "Nathan" });
    expect(result.content[0].text).toContain("Hello");
  });

  test("handles errors", async () => {
    const result = await callTool("mcp__my-plugin_my-server__search", { query: "" });
    expect(result.isError).toBe(true);
  });
});
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Server won't start | `bun run mcp/index.ts` to check errors |
| Tool not appearing | Check .mcp.json path, verify tool name pattern |
| Handler crashes | Add try/catch, log args before processing |
| Nested package.json | Delete it — breaks MCP discovery |

---

## Reference Links

**Essential:**
- @./references/gold-standard-patterns.md — 9 patterns with pitfalls + best practices
- @./references/kit-case-study.md — Kit's 18-tool production implementation

**API:**
- @./references/core-mcp-api.md — `@sidequest/core/mcp` + `@sidequest/core/spawn`
- @./references/error-handling.md — Error taxonomy and recovery strategies
- @./references/mcp-protocol.md — MCP protocol and marketplace conventions

**CLI:**
- `/plugin-template:create` — Generate plugin scaffold
- `/review-mcp` — Validate against checklist

---

## Summary

1. **Import:** `tool`, `startServer`, `log`, `createCorrelationId`, `z` from `@sidequest/core/mcp`
2. **Register:** Tools with Zod schemas and annotations
3. **Log:** With subsystems — `log.info(data, "subsystem")`
4. **Trace:** Correlation IDs on every log entry
5. **Format:** Support markdown (default) + JSON
6. **Errors:** Return `{ error, hint, isError: true }`
7. **Files:** Logs to `~/.claude/logs/<plugin>.jsonl`

Production example: @../../kit/CLAUDE.md
