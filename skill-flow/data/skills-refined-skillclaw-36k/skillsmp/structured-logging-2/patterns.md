# Logging Patterns

## Child Loggers

Create module-specific loggers with persistent context:

```typescript
// features/budget/server/db/budgets.ts
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "budget-db" });

// All logs automatically include { module: "budget-db" }
logger.info({ budgetId }, "Budget created");
// Output: { module: "budget-db", budgetId: "123", msg: "Budget created" }
```

### Nested Child Loggers

```typescript
const moduleLogger = createLogger({ module: "payments" });

async function processPayment(orderId: string) {
  // Add more context for this operation
  const paymentLogger = moduleLogger.child({ orderId });

  paymentLogger.info({ amount: 100 }, "Processing payment");
  // Output: { module: "payments", orderId: "456", amount: 100, msg: "Processing payment" }
}
```

## Request Context

### Add Request ID

```typescript
// middleware or API route
import { headers } from "next/headers";
import { createLogger } from "~/lib/logger";

export async function GET() {
  const headersList = await headers();
  const requestId = headersList.get("x-request-id") || crypto.randomUUID();

  const logger = createLogger({
    module: "api",
    requestId
  });

  logger.info({ path: "/api/users" }, "Request started");

  // ... handle request

  logger.info({ statusCode: 200, durationMs: 45 }, "Request completed");
}
```

### User Context

```typescript
import { auth } from "@clerk/nextjs/server";
import { createLogger } from "~/lib/logger";

export async function serverAction() {
  const { userId } = await auth();

  const logger = createLogger({
    module: "user-actions",
    userId: userId ?? "anonymous"
  });

  logger.info({ action: "updateProfile" }, "Action started");
}
```

## Error Logging Patterns

### Database Errors

```typescript
import { categorizeDbError, DbError } from "~/lib/firebase/errors";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "user-db" });

export async function getUserById(id: string): Promise<[DbError | null, User | null]> {
  try {
    const doc = await db.collection("users").doc(id).get();

    if (!doc.exists) {
      logger.warn({ userId: id }, "User not found");
      return [DbError.notFound("User"), null];
    }

    return [null, transformUser(doc)];
  } catch (error) {
    const dbError = categorizeDbError(error, "User");

    logger.error({
      userId: id,
      errorCode: dbError.code,
      isRetryable: dbError.isRetryable,
      isNotFound: dbError.isNotFound
    }, "Database error");

    return [dbError, null];
  }
}
```

### External Service Errors

```typescript
const logger = createLogger({ module: "stripe" });

async function createCharge(amount: number, currency: string) {
  try {
    logger.debug({ amount, currency }, "Creating charge");

    const charge = await stripe.charges.create({ amount, currency });

    logger.info({
      chargeId: charge.id,
      amount,
      currency
    }, "Charge created successfully");

    return charge;
  } catch (error) {
    if (error instanceof Stripe.errors.StripeCardError) {
      logger.warn({
        code: error.code,
        decline_code: error.decline_code,
        amount
      }, "Card declined");
    } else {
      logger.error({
        errorType: error.constructor.name,
        message: error.message,
        amount
      }, "Stripe error");
    }
    throw error;
  }
}
```

### Validation Errors

```typescript
const logger = createLogger({ module: "validation" });

export function validateUserInput(data: unknown) {
  const result = userSchema.safeParse(data);

  if (!result.success) {
    logger.warn({
      errors: result.error.flatten().fieldErrors,
      inputKeys: Object.keys(data as object)
    }, "Validation failed");

    return { valid: false, errors: result.error.flatten() };
  }

  return { valid: true, data: result.data };
}
```

## Performance Logging

### Operation Duration

```typescript
const logger = createLogger({ module: "performance" });

async function slowOperation() {
  const startTime = performance.now();

  try {
    const result = await doExpensiveWork();

    const durationMs = Math.round(performance.now() - startTime);

    if (durationMs > 1000) {
      logger.warn({ durationMs, operation: "slowOperation" }, "Slow operation detected");
    } else {
      logger.debug({ durationMs, operation: "slowOperation" }, "Operation completed");
    }

    return result;
  } catch (error) {
    const durationMs = Math.round(performance.now() - startTime);
    logger.error({ durationMs, error }, "Operation failed");
    throw error;
  }
}
```

### Batch Operations

```typescript
const logger = createLogger({ module: "batch" });

async function processBatch(items: Item[]) {
  const startTime = performance.now();
  let successCount = 0;
  let errorCount = 0;

  logger.info({ totalItems: items.length }, "Starting batch processing");

  for (const item of items) {
    try {
      await processItem(item);
      successCount++;
    } catch (error) {
      errorCount++;
      logger.debug({ itemId: item.id, error }, "Item processing failed");
    }
  }

  const durationMs = Math.round(performance.now() - startTime);

  logger.info({
    totalItems: items.length,
    successCount,
    errorCount,
    durationMs,
    itemsPerSecond: Math.round((items.length / durationMs) * 1000)
  }, "Batch processing completed");
}
```

## Lifecycle Logging

### Server Startup

```typescript
// app/layout.tsx or instrumentation.ts
import logger from "~/lib/logger";
import { env } from "~/data/env/server";

logger.info({
  nodeEnv: env.NODE_ENV,
  logLevel: env.LOG_LEVEL,
  version: process.env.npm_package_version
}, "Application starting");
```

### Graceful Shutdown

```typescript
process.on("SIGTERM", () => {
  logger.info({}, "Received SIGTERM, shutting down gracefully");

  // Cleanup operations
  server.close(() => {
    logger.info({}, "Server closed");
    process.exit(0);
  });
});

process.on("SIGINT", () => {
  logger.info({}, "Received SIGINT, shutting down");
  process.exit(0);
});
```

## Security Logging

### Authentication Events

```typescript
const logger = createLogger({ module: "auth" });

export function logAuthEvent(event: AuthEvent) {
  const baseContext = {
    userId: event.userId,
    ip: event.ip,
    userAgent: event.userAgent?.slice(0, 100)  // Truncate
  };

  switch (event.type) {
    case "login_success":
      logger.info({ ...baseContext, method: event.method }, "User logged in");
      break;
    case "login_failure":
      logger.warn({
        ...baseContext,
        reason: event.reason,
        attemptCount: event.attemptCount
      }, "Login failed");
      break;
    case "logout":
      logger.info(baseContext, "User logged out");
      break;
    case "password_reset":
      logger.info({ ...baseContext, initiated: true }, "Password reset initiated");
      break;
  }
}
```

### Sensitive Data Redaction

```typescript
function redactSensitive(obj: Record<string, unknown>): Record<string, unknown> {
  const sensitiveKeys = ["password", "token", "secret", "apiKey", "creditCard"];

  return Object.fromEntries(
    Object.entries(obj).map(([key, value]) => {
      if (sensitiveKeys.some(sk => key.toLowerCase().includes(sk.toLowerCase()))) {
        return [key, "[REDACTED]"];
      }
      if (typeof value === "object" && value !== null) {
        return [key, redactSensitive(value as Record<string, unknown>)];
      }
      return [key, value];
    })
  );
}

// Usage
logger.info(redactSensitive({ email, password, token }), "User credentials received");
// Output: { email: "user@example.com", password: "[REDACTED]", token: "[REDACTED]" }
```

## Structured Context Standards

### Recommended Context Fields

| Field | Type | When to Use |
|-------|------|-------------|
| `userId` | string | User-initiated actions |
| `requestId` | string | HTTP requests |
| `operation` | string | Named operations |
| `durationMs` | number | Timed operations |
| `errorCode` | string | Error responses |
| `isRetryable` | boolean | Error categorization |
| `statusCode` | number | HTTP responses |
| `path` | string | API endpoints |
| `method` | string | HTTP methods |

### Consistent Naming

```typescript
// ✅ Consistent
logger.info({ userId, budgetId, amount }, "Budget updated");
logger.info({ userId, orderId, amount }, "Order placed");

// ❌ Inconsistent
logger.info({ user_id, budget, amt }, "Budget updated");
logger.info({ uid, order_id, orderAmount }, "Order placed");
```
