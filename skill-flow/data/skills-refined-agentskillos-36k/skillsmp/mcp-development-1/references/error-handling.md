# Error Handling in MCP Servers

Comprehensive guide to designing, implementing, and testing robust error handling in MCP servers.

---

## Error Taxonomy

Define error types for consistent handling:

### Input Errors (Client fault)

```typescript
enum InputError {
  // Validation errors
  InvalidInput = "INVALID_INPUT",           // Data format wrong
  MissingRequired = "MISSING_REQUIRED",     // Required field absent
  OutOfRange = "OUT_OF_RANGE",             // Value exceeds limits

  // Pattern/syntax errors
  InvalidPattern = "INVALID_PATTERN",       // Bad regex
  InvalidQuery = "INVALID_QUERY",           // Query syntax wrong

  // Resource errors
  NotFound = "NOT_FOUND",                   // Resource doesn't exist
  Unauthorized = "UNAUTHORIZED"             // No permission
}
```

### System Errors (Server fault)

```typescript
enum SystemError {
  // Execution errors
  InternalError = "INTERNAL_ERROR",         // Unexpected failure
  Timeout = "TIMEOUT",                      // Operation too slow
  Unavailable = "UNAVAILABLE",              // Feature not available

  // Resource errors
  ResourceExhausted = "RESOURCE_EXHAUSTED", // Out of memory
  RateLimited = "RATE_LIMITED"             // Too many requests
}
```

### Recovery Errors (Degradation)

```typescript
enum RecoveryError {
  // Graceful fallback
  FallbackUsed = "FALLBACK_USED",           // Used fallback strategy
  Partial = "PARTIAL",                      // Partial results only
  Deprecated = "DEPRECATED"                 // Feature deprecated
}
```

---

## Error Response Format

### Standard Structure

```typescript
interface ErrorResponse {
  error: string;              // Human-readable message
  errorType?: string;         // Error category (InputError | SystemError)
  hint?: string;              // Recovery suggestion
  context?: string;           // Additional context
  isError: true;              // MCP protocol flag
}
```

### MCP Envelope

```typescript
return {
  content: [{
    type: "text",
    text: JSON.stringify({
      error: "File not found",
      errorType: "NOT_FOUND",
      hint: "Check the file path and verify the file exists",
      context: "Looking for: /path/to/file.txt",
      isError: true
    })
  }],
  isError: true
};
```

---

## Error Categories & Recovery

### Input Validation Errors

**When:** Client provides invalid input

**Pattern:**

```typescript
try {
  const validated = inputSchema.parse(args);
  // Continue with execution
} catch (error) {
  if (error instanceof z.ZodError) {
    const issue = error.issues[0];
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          error: `Invalid ${issue.path.join(".")}`,
          errorType: "INVALID_INPUT",
          hint: issue.message,
          isError: true
        })
      }],
      isError: true
    };
  }
  throw error;
}
```

**Recovery hints:**
- `"Check that query is at least 1 character"`
- `"Limit must be between 1 and 100"`
- `"Pattern is not valid regex"`

### Not Found Errors

**When:** Resource doesn't exist

**Pattern:**

```typescript
const result = await findResource(args.id);
if (!result) {
  return {
    content: [{
      type: "text",
      text: JSON.stringify({
        error: "Resource not found",
        errorType: "NOT_FOUND",
        hint: "Verify the ID exists and is still available",
        context: `ID: ${args.id}`,
        isError: true
      })
    }],
    isError: true
  };
}
```

**Recovery hints:**
- `"Check that the file exists in the repository"`
- `"Verify the function name is spelled correctly"`
- `"The resource may have been deleted"`

### Timeout Errors

**When:** Operation exceeds time limit

**Pattern:**

```typescript
const withTimeout = async (promise: Promise<T>, ms: number) => {
  return Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("Timeout")), ms)
    )
  ]);
};

try {
  const result = await withTimeout(expensiveOperation(), 30_000);
  // Continue
} catch (error) {
  if (error.message === "Timeout") {
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          error: "Operation timed out",
          errorType: "TIMEOUT",
          hint: "Try again with fewer results (limit=10) or smaller file set",
          isError: true
        })
      }],
      isError: true
    };
  }
  throw error;
}
```

**Recovery hints:**
- `"Try with smaller inputs (limit=10)"`
- `"Reduce file set or number of patterns"`
- `"Try again in a few moments"`

### Unavailable Feature Errors

**When:** Feature requires optional dependencies

**Pattern:**

```typescript
try {
  // Try primary implementation
  return await semanticSearch(args.query);
} catch (error) {
  const msg = error.message.toLowerCase();
  if (msg.includes("semantic") && msg.includes("not available")) {
    // Fall back to grep
    const grepResults = await grepSearch(args.query);
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          results: grepResults,
          recovery: "FALLBACK_USED",
          hint: "Using grep-based search. Install ML dependencies for semantic search: uv tool install 'cased-kit[ml]'"
        })
      }]
    };
  }
  throw error;
}
```

**Recovery hints:**
- `"Install optional dependencies: npm install ml-library"`
- `"Enable feature in config file"`
- `"Upgrade to latest version for this feature"`

### Permission/Authorization Errors

**When:** User lacks permission

**Pattern:**

```typescript
const canAccess = await checkPermission(args.resource);
if (!canAccess) {
  return {
    content: [{
      type: "text",
      text: JSON.stringify({
        error: "Permission denied",
        errorType: "UNAUTHORIZED",
        hint: "Contact repository administrator to grant access",
        context: `Resource: ${args.resource}`,
        isError: true
      })
    }],
    isError: true
  };
}
```

**Recovery hints:**
- `"Contact your administrator for access"`
- `"Check your authentication credentials"`
- `"This operation requires elevated privileges"`

---

## Error Handling Patterns

### Pattern 1: Try/Catch with Recovery

```typescript
async (args, _extra: unknown) => {
  const cid = createCorrelationId();

  try {
    // Attempt primary strategy
    const result = await primaryStrategy(args);
    return formatSuccess(result);
  } catch (primaryError) {
    logger.warn("Primary strategy failed", { cid, error: primaryError });

    // Try fallback
    try {
      const fallbackResult = await fallbackStrategy(args);
      logger.info("Fallback succeeded", { cid, strategy: "fallback" });
      return formatSuccess(fallbackResult, { fallback: true });
    } catch (fallbackError) {
      // Both failed - return error
      logger.error("All strategies failed", { cid, errors: [primaryError, fallbackError] });
      return formatError("Operation failed", "INTERNAL_ERROR");
    }
  }
}
```

### Pattern 2: Type Guard for Success/Failure

```typescript
type Success<T> = { ok: true; data: T };
type Failure = { ok: false; error: string; hint?: string };
type Result<T> = Success<T> | Failure;

const isSuccess = <T>(result: Result<T>): result is Success<T> => result.ok;

// In handler
const result = await execute(args);
if (!isSuccess(result)) {
  return formatError(result.error, "INTERNAL_ERROR", result.hint);
}

// Safely use result.data
return formatSuccess(result.data);
```

### Pattern 3: Custom Error Class

```typescript
class ToolError extends Error {
  constructor(
    message: string,
    public errorType: string,
    public hint?: string,
    public context?: string
  ) {
    super(message);
    this.name = "ToolError";
  }

  toMCP() {
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          error: this.message,
          errorType: this.errorType,
          hint: this.hint,
          context: this.context,
          isError: true
        })
      }],
      isError: true
    };
  }
}

// Usage
if (!validated) {
  throw new ToolError(
    "Invalid query",
    "INVALID_INPUT",
    "Query must be at least 1 character"
  );
}

// In handler
try {
  // ...
} catch (error) {
  if (error instanceof ToolError) {
    return error.toMCP();
  }
  // Generic error
  return formatError(error.message, "INTERNAL_ERROR");
}
```

### Pattern 4: Validator with Detailed Feedback

```typescript
const validateInput = (args: unknown): Result<Validated> => {
  const parsed = inputSchema.safeParse(args);

  if (!parsed.success) {
    const issue = parsed.error.issues[0];
    return {
      ok: false,
      error: `Invalid ${issue.path.join(".")}`,
      hint: issue.message
    };
  }

  // Additional business logic validation
  if (parsed.data.limit > parsed.data.maxLimit) {
    return {
      ok: false,
      error: "Limit exceeds maximum",
      hint: `Max limit is ${parsed.data.maxLimit}`
    };
  }

  return { ok: true, data: parsed.data };
};

// In handler
const validation = validateInput(args);
if (!validation.ok) {
  return formatError(validation.error, "INVALID_INPUT", validation.hint);
}

const result = await execute(validation.data);
```

---

## Logging Errors with Context

### Structured Error Logging

```typescript
const cid = createCorrelationId();

try {
  const result = await operation(args);
  logger.info("Operation succeeded", { cid, durationMs: elapsed });
  return formatSuccess(result);
} catch (error) {
  logger.error("Operation failed", {
    cid,
    tool: "my_tool",
    error: error.message,
    stack: error instanceof Error ? error.stack : undefined,
    args: sanitize(args),  // Remove sensitive data!
    durationMs: elapsed
  });

  return formatError(error.message, "INTERNAL_ERROR");
}

// Helper to remove sensitive data
function sanitize(obj: any) {
  if (typeof obj !== "object") return obj;
  const sanitized = { ...obj };
  delete sanitized.password;
  delete sanitized.token;
  delete sanitized.apiKey;
  return sanitized;
}
```

### Correlation ID Tracing

```
Request: { cid: "a1b2c3d4", event: "request_start", tool: "search" }
Validation: { cid: "a1b2c3d4", event: "validation_start", args_valid: true }
Execution: { cid: "a1b2c3d4", event: "execute_start", strategy: "primary" }
Error: { cid: "a1b2c3d4", event: "error", message: "Timeout" }
Fallback: { cid: "a1b2c3d4", event: "fallback_start", strategy: "grep" }
Success: { cid: "a1b2c3d4", event: "response_complete", durationMs: 250 }
```

**Benefit:** Grep all logs by correlation ID to see exact timeline.

---

## Testing Error Paths

### Test Invalid Input

```typescript
test("rejects empty query", async () => {
  const result = await callTool("search", { query: "" });

  expect(result.isError).toBe(true);
  const response = JSON.parse(result.content[0].text);
  expect(response.error).toContain("empty");
  expect(response.hint).toBeDefined();
});

test("rejects invalid limit", async () => {
  const result = await callTool("search", {
    query: "test",
    limit: 101  // Max is 100
  });

  expect(result.isError).toBe(true);
  const response = JSON.parse(result.content[0].text);
  expect(response.errorType).toBe("OUT_OF_RANGE");
});
```

### Test Not Found

```typescript
test("returns NOT_FOUND for missing resource", async () => {
  const result = await callTool("getFile", {
    path: "/nonexistent/file.txt"
  });

  expect(result.isError).toBe(true);
  const response = JSON.parse(result.content[0].text);
  expect(response.errorType).toBe("NOT_FOUND");
  expect(response.hint).toContain("verify");
});
```

### Test Timeout

```typescript
test("times out for slow operation", async () => {
  const result = await callToolWithTimeout("slowTool", args, 100);  // 100ms timeout

  expect(result.isError).toBe(true);
  const response = JSON.parse(result.content[0].text);
  expect(response.errorType).toBe("TIMEOUT");
  expect(response.hint).toContain("fewer results");
});
```

### Test Fallback

```typescript
test("falls back gracefully when primary fails", async () => {
  // Mock primary strategy failure
  mockPrimaryStrategy.mockRejectedValue(
    new Error("semantic search not available")
  );

  const result = await callTool("search", { query: "test" });

  expect(result.isError).toBe(false);
  const response = JSON.parse(result.content[0].text);
  expect(response.fallback).toBe(true);
  expect(response.hint).toContain("semantic");
});
```

---

## Error Response Checklist

Before shipping error handling, verify:

- ✅ **Human-readable message** - User understands what went wrong
- ✅ **Error type** - Categorized (InputError | SystemError | RecoveryError)
- ✅ **Recovery hint** - Suggests how to fix or try again
- ✅ **Context** - Includes relevant details (path, ID, etc.)
- ✅ **isError flag** - Set to true
- ✅ **Logging** - Error logged with correlation ID
- ✅ **Test coverage** - Error path has tests
- ✅ **No sensitive data** - No passwords, tokens, etc. in response

---

## Best Practices

### 1. Fail Fast

```typescript
// ✓ Good: Validate early
const validated = inputSchema.parse(args);
if (!validated) throw new ToolError("Invalid", "INVALID_INPUT");

// ✗ Bad: Validate late
const result = await expensiveOperation(args);
// Only then check if result is valid
```

### 2. Provide Recovery Hints

```typescript
// ✓ Good
throw new ToolError(
  "File not found",
  "NOT_FOUND",
  "Check the file exists and path is correct"
);

// ✗ Bad
throw new Error("File not found");  // No context!
```

### 3. Log with Context

```typescript
// ✓ Good
logger.error("Operation failed", {
  cid,
  tool: "search",
  error: error.message,
  args: sanitizedArgs,
  durationMs: elapsed
});

// ✗ Bad
console.error(error);  // No context
```

### 4. Support response_format in Errors

```typescript
// ✓ Good: Respect format even in errors
const format = args.response_format || "markdown";
const text = format === "json"
  ? JSON.stringify({ error: "...", isError: true })
  : `# Error\n\n${errorMessage}`;

// ✗ Bad: Always JSON
const text = JSON.stringify({ error: "..." });
```

### 5. Don't Expose Implementation Details

```typescript
// ✓ Good: Safe error
throw new ToolError(
  "Database connection failed",
  "UNAVAILABLE",
  "Try again in a moment"
);

// ✗ Bad: Leaks internals
throw new Error("MySQL connection timeout at 192.168.1.1:3306");
```

---

## Error Handling Checklist

Before production:

- ✅ All error paths return `{ isError: true }`
- ✅ All errors have recovery hints
- ✅ Sensitive data filtered from logs
- ✅ Correlation IDs link all related logs
- ✅ Error types categorized consistently
- ✅ response_format respected in errors
- ✅ Fallback strategies implemented
- ✅ Error paths tested
- ✅ Timeout budgets appropriate
- ✅ No generic "Error" thrown

---

## Summary

Robust error handling requires:

1. **Classification** - Define error types
2. **Recovery** - Provide hints for fixing
3. **Context** - Include relevant details
4. **Logging** - Use correlation IDs
5. **Testing** - Test error paths
6. **User focus** - Clear, actionable messages

**Key principle:** Make errors helpful, not cryptic.

For examples, study Kit plugin error handling:
@./kit-case-study.md#error-handling-taxonomy
