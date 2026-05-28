# MCP Debugging Guide

## Debug Tools

### MCP Inspector
```bash
npx @modelcontextprotocol/inspector
```

### Logging
**Important**: Use `console.error` for logs (stdout is for protocol).

```typescript
function log(level: string, message: string, data?: any) {
  console.error(JSON.stringify({
    timestamp: new Date().toISOString(),
    level,
    message,
    ...(data && { data }),
  }));
}

// Usage
log("info", "Tool called", { tool: "sql_select", args });
log("error", "Query failed", { error: err.message });
```

## Common Issues

### 1. Server Doesn't Start

**Symptoms**: Claude can't connect to MCP

**Check**:
```bash
# Test manually
node build/index.js

# Check env vars
SQL_SERVER=localhost SQL_DATABASE=mydb node build/index.js
```

**Verify**:
- Path in config is absolute and correct
- Required environment variables are set
- No syntax errors in code

### 2. Tool Not Appearing

**Symptoms**: Tool registered but not available

**Check**:
- Tool registered BEFORE `server.connect()`
- Tool name is unique
- Zod schema is valid

```typescript
// Debug: List registered tools
console.error("[MCP] Registering tool:", toolName);
```

### 3. JSON Parse Error

**Symptoms**: `SyntaxError: Unexpected token`

**Causes**:
- Using `console.log()` instead of `console.error()`
- Non-JSON output mixed in stdout
- Encoding issues

**Fix**: Replace all `console.log` with `console.error`

### 4. Connection Timeout

**Symptoms**: Tool hangs then fails

**Solution**:
```typescript
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 30000);

try {
  const result = await operation({ signal: controller.signal });
  return result;
} finally {
  clearTimeout(timeout);
}
```

### 5. Zod Validation Error

**Symptoms**: `ZodError: Invalid input`

**Debug**:
```typescript
const result = schema.safeParse(input);
if (!result.success) {
  console.error("[MCP] Validation:", result.error.issues);
}
```

### 6. Database Connection Failed

**Checklist**:
- [ ] Environment variables correct?
- [ ] Firewall allows connection?
- [ ] SQL Server accepts TCP/IP?
- [ ] User has permissions?

```typescript
try {
  await sql.connect(config);
  console.error("[MCP] DB connected");
} catch (err) {
  console.error("[MCP] DB error:", err.message);
  console.error("[MCP] Config:", { ...config, password: "***" });
}
```

### 7. Memory Leak

**Symptoms**: Server slows down over time

**Check**:
- Connections being released to pool?
- Event listeners being removed?
- Large objects being cleared?

```typescript
// Monitor memory
setInterval(() => {
  const used = process.memoryUsage();
  console.error(`[MCP] Heap: ${Math.round(used.heapUsed / 1024 / 1024)}MB`);
}, 60000);
```

## Testing Checklist

- [ ] `ping` tool works
- [ ] All tools appear in Inspector
- [ ] Valid inputs return expected results
- [ ] Invalid inputs return clear errors
- [ ] Large results are paginated
- [ ] Timeouts work correctly
