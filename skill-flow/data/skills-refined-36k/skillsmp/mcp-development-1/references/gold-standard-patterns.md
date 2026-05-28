# Gold Standard Patterns

9 production-validated patterns from Kit plugin (18 tools, 1780 lines).

---

## Table of Contents

1. [Declarative Tool Registration](#pattern-1-declarative-tool-registration)
2. [Correlation ID Tracing](#pattern-2-correlation-id-tracing)
3. [Structured Error Responses](#pattern-3-structured-error-responses)
4. [Response Format Switching](#pattern-4-response-format-switching)
5. [File Logging Configuration](#pattern-5-file-logging-configuration)
6. [MCP Annotations](#pattern-6-mcp-annotations)
7. [No Nested Package.json](#pattern-7-no-nested-packagejson)
8. [Dual Logging](#pattern-8-dual-logging-mcp-protocol--file)
9. [Separation of Concerns](#pattern-9-separation-of-concerns)

---

## Pattern 1: Declarative Tool Registration

Register tools with Zod schemas and MCP annotations for type-safe validation:

```typescript
tool(
  "kit_index_find",
  {
    description: `Find symbol definitions from PROJECT_INDEX.json (token-efficient).

Searches the pre-built index instead of scanning files. Great for:
- Finding where a function/class/type is defined
- Quick symbol lookup without reading source files

NOTE: Requires PROJECT_INDEX.json. Run kit_index_prime first if not present.`,
    inputSchema: {
      symbol_name: z.string().describe('Symbol name to search for. Example: "executeKitGrep"'),
      index_path: z.string().optional().describe("Path to PROJECT_INDEX.json"),
      response_format: z.enum(["markdown", "json"]).optional()
        .describe("Output format: 'markdown' (default) or 'json'"),
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async (args) => { /* handler */ }
);
```

**Pitfalls:**
- Forgetting `.describe()` → LLMs don't understand parameters
- Missing `response_format` → Users can't choose format
- Wrong annotations → LLMs use tool incorrectly

---

## Pattern 2: Correlation ID Tracing

Generate unique IDs per request, attach to all log entries:

```typescript
async (args: Record<string, unknown>) => {
  const { pattern, response_format } = args as { pattern: string; response_format?: string };

  const cid = createCorrelationId();
  const startTime = Date.now();
  log.info({ cid, tool: "kit_grep", args: { pattern } }, "grep");

  try {
    const result = await executeGrep(pattern);
    log.info({ cid, tool: "kit_grep", success: true, durationMs: Date.now() - startTime }, "grep");
    return { content: [{ type: "text", text: formatResult(result) }] };
  } catch (error) {
    log.error({ cid, tool: "kit_grep", error: error.message }, "grep");
    throw error;
  }
}
```

**Key:** Generate correlation ID FIRST, include in EVERY log entry.

---

## Pattern 3: Structured Error Responses

Return consistent error objects with `isError` flag and recovery hints:

```typescript
{
  error: "PROJECT_INDEX.json not found",
  hint: "Run kit_index_prime first to generate the index",
  isError: true
}
```

**Return format:**
```typescript
return {
  content: [{ type: "text", text: JSON.stringify({ error, hint, isError: true }) }],
  isError: true  // Top-level flag
};
```

**Pitfalls:**
- Returning plain strings → Machines can't detect errors
- Missing `isError: true` → Consumers can't detect failures
- Generic messages → Users don't know how to fix

---

## Pattern 4: Response Format Switching

Support both markdown (human) and JSON (machine) via `response_format`:

```typescript
const format = response_format === "json"
  ? ResponseFormat.JSON
  : ResponseFormat.MARKDOWN;

return {
  content: [{ type: "text", text: formatResults(result, format) }]
};
```

**Why:** 40-60% token savings with JSON format.

**Best Practice:** Use enum type internally:
```typescript
enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json"
}
```

---

## Pattern 5: File Logging Configuration

Configure subsystem-based hierarchical logging:

```typescript
startServer("kit", {
  version: "1.0.0",
  fileLogging: {
    enabled: true,
    subsystems: ["grep", "semantic", "symbols", "ast", "commit"],
    level: "debug",
    maxSize: 10_000_000,  // 10MB
    maxFiles: 5
  }
});
```

**Logs written to:** `~/.claude/logs/<plugin>.jsonl`

**View logs:**
```bash
tail -f ~/.claude/logs/kit.jsonl | jq
cat ~/.claude/logs/kit.jsonl | jq 'select(.cid == "abc123")'
```

---

## Pattern 6: MCP Annotations

Add behavioral hints to tools:

| Annotation | Meaning | Example |
|------------|---------|---------|
| `readOnlyHint: true` | No side effects | Search, query tools |
| `destructiveHint: true` | Deletes/modifies data | Delete, remove tools |
| `idempotentHint: true` | Safe to retry | Most read operations |
| `openWorldHint: true` | Touches external systems | API calls |

**Example:**
```typescript
// Read-only tool
annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }

// Destructive tool
annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: false, openWorldHint: true }
```

---

## Pattern 7: No Nested Package.json

**NEVER** create package.json inside MCP server directories:

```
plugins/kit/
├── mcp/
│   └── index.ts      ✅ CORRECT
├── package.json      ✅ All dependencies here
```

**Wrong:**
```
plugins/kit/
├── mcp/
│   └── package.json  ❌ Breaks MCP discovery
```

**Why:** Nested package.json breaks Claude Code's MCP server discovery. See commits `8e8069b`, `b6bb797`.

---

## Pattern 8: Dual Logging (MCP Protocol + File)

`log.info()` from `@sidequest/core/mcp` automatically logs to both:
1. MCP protocol (visible in Claude Desktop inspector)
2. File (`~/.claude/logs/<plugin>.jsonl`)

```typescript
log.info({ cid, tool: "kit_grep", args: { pattern } }, "grep");
// Logs to both destinations with same correlation ID
```

---

## Pattern 9: Separation of Concerns

Keep MCP server code separate from business logic:

```
src/index.ts          → Business logic (pure functions, testable)
mcp/index.ts          → MCP layer (validation, logging, formatting)
```

**Business Logic (pure function):**
```typescript
// src/index.ts
export async function executeIndexFind(symbolName: string, indexPath?: string): Promise<Result> {
  // Pure function - no MCP dependencies, easily testable
}
```

**MCP Layer (thin wrapper):**
```typescript
// mcp/index.ts
tool("kit_index_find", { /* schema */ }, async (args) => {
  const cid = createCorrelationId();
  log.info({ cid, tool: "kit_index_find" }, "symbols");

  const result = await executeIndexFind(symbol_name, index_path);  // Call pure function

  return { content: [{ type: "text", text: formatResult(result) }] };
});
```

**Benefits:**
- Business logic testable without MCP server
- MCP layer only handles validation, logging, formatting
- Reusable in CLI, tests, other contexts

---

## Summary

| Pattern | Purpose |
|---------|---------|
| 1. Declarative Registration | Type-safe tool definitions |
| 2. Correlation ID Tracing | Request tracking across logs |
| 3. Structured Errors | Machine-parseable error responses |
| 4. Response Format Switching | Markdown + JSON support |
| 5. File Logging | Persistent debugging logs |
| 6. MCP Annotations | LLM behavioral hints |
| 7. No Nested Package.json | Avoid MCP discovery issues |
| 8. Dual Logging | Protocol + file persistence |
| 9. Separation of Concerns | Testable architecture |

For complete production examples, see @./kit-case-study.md.
