---
name: structured-logging
version: 1.0.0
lastUpdated: 2026-01-18
description: Structured logging patterns with Pino for Next.js applications. Covers log levels, context enrichment, child loggers, and production best practices.
tags: [logging, pino, observability, debugging, monitoring]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
context: fork
agent: general-purpose
user-invocable: true
examples:
  - How to add logging to a server action
  - What log level should I use
  - Create a child logger with context
  - Log errors with stack traces
---

# Structured Logging Skill

Structured logging patterns with Pino for Next.js applications.

> **Reference Files:**
> - [pino-setup.md](./pino-setup.md) - Logger configuration
> - [log-levels.md](./log-levels.md) - When to use each level
> - [patterns.md](./patterns.md) - Common logging patterns
> - [examples.md](./examples.md) - Practical examples

## Project Configuration

The logger is configured in `lib/logger.ts`:

```typescript
import pino from "pino";

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  transport:
    process.env.NODE_ENV === "development"
      ? {
          target: "pino-pretty",
          options: {
            colorize: true,
            translateTime: "SYS:standard",
            ignore: "pid,hostname"
          }
        }
      : undefined,
  formatters: {
    level: (label) => ({ level: label.toUpperCase() })
  },
  timestamp: pino.stdTimeFunctions.isoTime
});

export function createLogger(context: Record<string, unknown>) {
  return logger.child(context);
}

export default logger;
```

## Quick Start

### Basic Logging

```typescript
import logger from "~/lib/logger";

// Simple message
logger.info("Server started");

// With context object
logger.info({ port: 3000 }, "Server started");

// Error logging
logger.error({ error, userId }, "Failed to process request");
```

### Module-Specific Logger

```typescript
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "user-service" });

// All logs include { module: "user-service" }
logger.info({ userId: "123" }, "User created");
// Output: { module: "user-service", userId: "123", msg: "User created" }
```

## Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| `fatal` | App crash, unrecoverable | Database connection lost |
| `error` | Operation failed | User creation failed |
| `warn` | Unexpected but recoverable | Rate limit approaching |
| `info` | Normal operations | User logged in |
| `debug` | Development details | Request payload |
| `trace` | Fine-grained debugging | Function entry/exit |

### Usage

```typescript
logger.fatal({ error }, "Database connection lost, shutting down");
logger.error({ userId, errorCode: error.code }, "Failed to update user");
logger.warn({ requestCount, limit }, "Rate limit 80% reached");
logger.info({ userId }, "User logged in successfully");
logger.debug({ payload }, "Processing request");
logger.trace({ functionName: "processData" }, "Entering function");
```

## Key Patterns

### Always Log Context Objects First

```typescript
// ✅ Good - context object first, then message
logger.info({ userId, action: "login" }, "User authenticated");

// ❌ Bad - no context
logger.info("User authenticated");

// ❌ Bad - string interpolation
logger.info(`User ${userId} authenticated`);
```

### Error Logging

```typescript
import { categorizeDbError, DbError } from "~/lib/firebase/errors";

try {
  await updateUser(userId, data);
} catch (error) {
  const dbError = categorizeDbError(error, "User");

  logger.error({
    userId,
    errorCode: dbError.code,
    isRetryable: dbError.isRetryable,
    operation: "updateUser"
  }, "Failed to update user");

  return [dbError, null];
}
```

### Database Operations

```typescript
const logger = createLogger({ module: "user-db" });

export async function getUserById(id: string) {
  logger.debug({ userId: id }, "Fetching user");

  try {
    const user = await db.collection("users").doc(id).get();

    if (!user.exists) {
      logger.warn({ userId: id }, "User not found");
      return [DbError.notFound("User"), null];
    }

    logger.info({ userId: id }, "User fetched successfully");
    return [null, transformUser(user)];
  } catch (error) {
    const dbError = categorizeDbError(error, "User");
    logger.error({
      userId: id,
      errorCode: dbError.code,
      isRetryable: dbError.isRetryable
    }, "Database error fetching user");
    return [dbError, null];
  }
}
```

### Server Actions

```typescript
const logger = createLogger({ module: "user-actions" });

export async function updateProfile(data: ProfileData): ActionResponse {
  const { userId } = await auth();

  if (!userId) {
    logger.warn({ action: "updateProfile" }, "Unauthorized access attempt");
    return { success: false, error: "Unauthorized" };
  }

  logger.info({ userId, action: "updateProfile" }, "Starting profile update");

  const [error] = await updateUserProfile(userId, data);

  if (error) {
    logger.error({
      userId,
      errorCode: error.code,
      action: "updateProfile"
    }, "Profile update failed");
    return { success: false, error: error.message };
  }

  logger.info({ userId, action: "updateProfile" }, "Profile updated successfully");
  return { success: true, data: null };
}
```

## Environment Configuration

```bash
# .env.local
LOG_LEVEL=debug  # Development: see all logs

# .env.production
LOG_LEVEL=info   # Production: info and above
```

## File Locations

| Purpose | Location |
|---------|----------|
| Logger setup | `lib/logger.ts` |
| Feature loggers | Create in feature modules |
| Log level config | `data/env/server.ts` |

## Related Skills

- `firebase-firestore` - Database logging patterns
- `server-actions` - Action logging patterns
- `t3-env-validation` - LOG_LEVEL configuration
