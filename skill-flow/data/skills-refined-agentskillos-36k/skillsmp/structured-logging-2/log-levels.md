# Log Levels Guide

## Level Hierarchy

Pino uses a numeric severity system. Lower numbers = higher severity:

| Level | Number | Description |
|-------|--------|-------------|
| `fatal` | 60 | Application crash |
| `error` | 50 | Operation failed |
| `warn` | 40 | Warning condition |
| `info` | 30 | Normal operation |
| `debug` | 20 | Debug information |
| `trace` | 10 | Fine-grained trace |

When `LOG_LEVEL=info`, only `info`, `warn`, `error`, and `fatal` are logged.

## When to Use Each Level

### fatal

**Use for:** Unrecoverable errors that crash the application.

```typescript
// Database connection lost
logger.fatal({ error, dbHost }, "Lost database connection, shutting down");
process.exit(1);

// Critical configuration missing
logger.fatal({ missingVars: ["DATABASE_URL"] }, "Missing critical environment variables");
process.exit(1);

// Uncaught exception handler
process.on("uncaughtException", (error) => {
  logger.fatal({ error }, "Uncaught exception");
  process.exit(1);
});
```

### error

**Use for:** Operation failures that need attention but don't crash the app.

```typescript
// Database operation failed
logger.error({
  userId,
  errorCode: dbError.code,
  isRetryable: dbError.isRetryable,
  operation: "createUser"
}, "Failed to create user");

// External API failure
logger.error({
  service: "stripe",
  statusCode: response.status,
  endpoint: "/v1/charges"
}, "Payment processing failed");

// Validation error (unexpected)
logger.error({
  userId,
  invalidFields: ["email", "phone"]
}, "Data corruption detected");
```

### warn

**Use for:** Unexpected conditions that don't prevent operation.

```typescript
// Resource approaching limit
logger.warn({
  currentUsage: 8500,
  limit: 10000,
  resource: "apiCalls"
}, "API rate limit 85% reached");

// Deprecated feature usage
logger.warn({
  feature: "legacyAuth",
  userId,
  suggestedMigration: "Use OAuth instead"
}, "Deprecated authentication method used");

// Slow operation
logger.warn({
  operation: "queryUsers",
  durationMs: 5200,
  threshold: 3000
}, "Slow database query detected");

// Retry happening
logger.warn({
  attempt: 2,
  maxAttempts: 3,
  operation: "sendEmail"
}, "Retrying failed operation");

// Missing optional data
logger.warn({
  userId,
  missingField: "profilePicture"
}, "User profile incomplete");
```

### info

**Use for:** Normal, significant operations.

```typescript
// User actions
logger.info({ userId, action: "login" }, "User logged in");
logger.info({ userId, action: "logout" }, "User logged out");
logger.info({ userId, budgetId }, "Budget created");

// Server lifecycle
logger.info({ port: 3000 }, "Server started");
logger.info({}, "Server shutting down gracefully");

// Successful operations
logger.info({ userId, orderId }, "Order placed successfully");
logger.info({ jobId, recordsProcessed: 150 }, "Batch job completed");

// Configuration loaded
logger.info({
  logLevel: "info",
  environment: "production"
}, "Application configured");
```

### debug

**Use for:** Detailed information for debugging.

```typescript
// Request details
logger.debug({
  method: "POST",
  path: "/api/users",
  body: sanitizedBody,
  headers: safeHeaders
}, "Incoming request");

// Response details
logger.debug({
  statusCode: 200,
  responseTime: 45,
  path: "/api/users"
}, "Request completed");

// Variable state
logger.debug({
  userId,
  permissions: userPermissions,
  roles: userRoles
}, "User permissions loaded");

// Cache operations
logger.debug({
  key: "user:123",
  hit: true,
  ttl: 3600
}, "Cache lookup");

// Query details
logger.debug({
  collection: "users",
  filter: { status: "active" },
  limit: 10
}, "Executing database query");
```

### trace

**Use for:** Very fine-grained debugging (rarely used in production).

```typescript
// Function entry/exit
logger.trace({ fn: "processPayment", args: { amount, currency } }, "Entering");
logger.trace({ fn: "processPayment", result: "success" }, "Exiting");

// Loop iterations
items.forEach((item, index) => {
  logger.trace({ index, itemId: item.id }, "Processing item");
});

// Detailed state changes
logger.trace({
  stateBefore: oldState,
  stateAfter: newState,
  trigger: "userInput"
}, "State transition");
```

## Log Level by Environment

| Environment | Recommended Level | Reason |
|-------------|-------------------|--------|
| Development | `debug` | Full visibility for debugging |
| Test | `warn` | Only failures and warnings |
| Staging | `info` | Normal operations + issues |
| Production | `info` | Balance of visibility and volume |

```bash
# .env.local
LOG_LEVEL=debug

# .env.test
LOG_LEVEL=warn

# .env.staging
LOG_LEVEL=info

# .env.production
LOG_LEVEL=info
```

## Choosing the Right Level

### Decision Tree

```
Is the application crashing?
  YES → fatal
  NO ↓

Did an operation fail?
  YES → error
  NO ↓

Is this unexpected but not a failure?
  YES → warn
  NO ↓

Is this a significant normal event?
  YES → info
  NO ↓

Is this helpful for debugging?
  YES → debug
  NO ↓

Is this very detailed tracing?
  YES → trace
  NO → Don't log it
```

## Common Mistakes

### Over-logging at info

```typescript
// ❌ Too verbose for info
logger.info({ i }, "Processing item");  // In a loop of 10000 items

// ✅ Better
logger.debug({ i }, "Processing item");
logger.info({ totalProcessed: 10000 }, "Batch processing complete");
```

### Under-logging errors

```typescript
// ❌ Swallowing errors
try {
  await riskyOperation();
} catch (error) {
  return null;  // Error lost!
}

// ✅ Always log errors
try {
  await riskyOperation();
} catch (error) {
  logger.error({ error }, "Risky operation failed");
  return null;
}
```

### Wrong level for expected conditions

```typescript
// ❌ Error for expected "not found"
if (!user) {
  logger.error({ userId }, "User not found");  // This might be normal!
}

// ✅ Use warn or info depending on context
if (!user) {
  logger.warn({ userId }, "User not found");  // If unexpected
  // OR
  logger.info({ userId }, "User lookup returned no results");  // If normal
}
```

### Sensitive data in logs

```typescript
// ❌ Logging passwords/tokens
logger.info({ password, token }, "User credentials");

// ✅ Redact sensitive data
logger.info({
  hasPassword: !!password,
  tokenPrefix: token?.slice(0, 8)
}, "User credentials check");
```
