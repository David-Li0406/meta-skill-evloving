---
name: crude-functions-testing
description: Testing best practices for Crude Functions project - includes TestSetupBuilder usage patterns, test structure guidelines, mocking approaches, and anti-patterns to avoid. Use when writing or modifying tests in the Crude Functions codebase, or when questions arise about testing strategy, test setup, or test organization.
---

# Testing in Crude Functions

## Overview

This skill documents testing best practices specific to the Crude Functions project. Testing in this codebase follows a philosophy of **real infrastructure over mocks** - preferring real databases, migrations, and services when practical. The centerpiece is **TestSetupBuilder**, a fluent API for creating isolated test environments that mirror production initialization.

**Key Principles:**
- Use real infrastructure (database, migrations, services) via TestSetupBuilder for integration tests
- Use simple helper functions for focused unit tests
- Minimize mocking - only mock at boundaries (auth, external systems)
- Always cleanup resources with try-finally pattern
- Test pure functions separately without setup overhead

## TestSetupBuilder

**Location:** `src/test/test_setup_builder.ts`

### What It Is

TestSetupBuilder provides isolated test environments with:
- Real SQLite database (in-memory or temp file)
- Full migration execution
- Multiple services with automatic dependency resolution
- Deferred data insertion (API keys, routes, settings, users)
- Guaranteed cleanup

**Why it exists:** Mirrors production initialization flow from `main.ts` to prevent schema and initialization drift between tests and production.

### When to Use TestSetupBuilder

Use TestSetupBuilder for:
- **Integration tests** - Multiple services working together
- **Database-dependent tests** - Tests requiring real schema and migrations
- **Production flow validation** - Ensuring initialization matches production

### When NOT to Use TestSetupBuilder

Skip TestSetupBuilder for:
- **Pure function tests** - Logic with no infrastructure dependencies
- **Single-class unit tests** - Testing one service in isolation
- **Low-level utilities** - Simple helpers, validators, formatters

### How to Use TestSetupBuilder

#### Basic Pattern

```typescript
import { TestSetupBuilder } from "@/test/test_setup_builder.ts";
import { expect } from "@std/expect";

Deno.test("RoutesService.getAll returns empty array initially", async () => {
  const ctx = await TestSetupBuilder.create()
    .withAll()  // All services
    .build();

  try {
    const routes = await ctx.routesService.getAll();
    expect(routes).toEqual([]);
  } finally {
    await ctx.cleanup();  // Always cleanup
  }
});
```

#### Convenience Methods (Recommended)

```typescript
// Minimal - just metrics
.withMetrics()  // → ExecutionMetricsService + MetricsStateService

// Settings (auto-enables encryption)
.withSettings()  // → SettingsService + EncryptionService + HashService

// Logs (auto-enables settings)
.withLogs()  // → ConsoleLogService + SettingsService + encryption

// Secrets (auto-enables encryption)
.withSecrets()  // → SecretsService + EncryptionService

// Users (auto-enables auth)
.withUsers()  // → UserService + Auth + encryption

// Everything
.withAll()  // → All services
```

#### Individual Methods (Fine-Grained Control)

```typescript
.withExecutionMetricsService()
.withMetricsStateService()
.withEncryptionService()
.withHashService()
.withSettingsService()
.withConsoleLogService()
.withRoutesService()
.withFileService()
.withApiKeyService()
.withSecretsService()
.withAuth()
.withUserService()
```

#### Deferred Data Pattern

Create data during build phase with automatic dependency ordering:

```typescript
const ctx = await TestSetupBuilder.create()
  .withApiKeyGroup("management", "Admin keys")
  .withApiKey("management", "test-api-key-123")
  .withRoute("/hello", "hello.ts", { methods: ["GET"] })
  .withSetting("api.access-groups", "management")
  .build();

// All data created in correct order with FK constraints satisfied
const routes = await ctx.routesService.getAll();
expect(routes.length).toBe(1);
```

#### Auto-Dependency Resolution

TestSetupBuilder automatically enables dependent services:

```typescript
// This...
.withSettings()

// Automatically enables:
// - EncryptionService (settings needs encryption)
// - HashService (encryption needs hashing)

// This...
.withLogs()

// Automatically enables:
// - ConsoleLogService
// - SettingsService (logs need settings)
// - EncryptionService + HashService (settings dependencies)
```

**Location:** Dependency graph defined in `src/test/dependency_graph.ts`

### Minimal Context Construction

Request only what you need:

```typescript
// Metrics test - only metrics services
const ctx = await TestSetupBuilder.create()
  .withMetrics()
  .build();

// Routes test - routes + file service (auto-enabled)
const ctx = await TestSetupBuilder.create()
  .withRoutes()
  .build();

// Full integration - everything
const ctx = await TestSetupBuilder.create()
  .withAll()
  .build();
```

## Test Structure Patterns

### File Naming

All test files follow pattern: `*_test.ts`

Example: `routes_service_test.ts`, `encryption_service_test.ts`

### Standard Test Organization

Organize tests in logical groups:

```typescript
// Group 1: Pure function validation (no DB needed)
Deno.test("validateRouteName accepts valid names", () => {
  expect(validateRouteName("hello")).toBe(true);
  expect(validateRouteName("hello-world")).toBe(true);
  expect(validateRouteName("hello_world")).toBe(true);
});

Deno.test("validateRouteName rejects invalid names", () => {
  expect(validateRouteName("")).toBe(false);
  expect(validateRouteName("Hello")).toBe(false);  // Uppercase
  expect(validateRouteName("hello world")).toBe(false);  // Space
});

// Group 2: Basic CRUD operations
Deno.test("RoutesService.addRoute creates new route", async () => {
  const ctx = await TestSetupBuilder.create().withRoutes().build();
  try {
    await ctx.routesService.addRoute("test", "test.ts", { methods: ["GET"] });
    const routes = await ctx.routesService.getAll();
    expect(routes.length).toBe(1);
  } finally {
    await ctx.cleanup();
  }
});

// Group 3: Edge cases and errors
Deno.test("RoutesService.addRoute rejects duplicate names", async () => {
  const ctx = await TestSetupBuilder.create().withRoutes().build();
  try {
    await ctx.routesService.addRoute("test", "test.ts", { methods: ["GET"] });
    await expect(
      ctx.routesService.addRoute("test", "other.ts", { methods: ["POST"] })
    ).rejects.toThrow("already exists");
  } finally {
    await ctx.cleanup();
  }
});

// Group 4: Concurrency and state management
Deno.test("concurrent rebuildIfNeeded calls share single rebuild", async () => {
  const ctx = await TestSetupBuilder.create().withRoutes().build();
  try {
    // Test concurrent access patterns
    const results = await Promise.all([
      ctx.routesService.rebuildIfNeeded(),
      ctx.routesService.rebuildIfNeeded(),
    ]);
    // Assertions about shared state
  } finally {
    await ctx.cleanup();
  }
});

// Group 5: Integration scenarios
Deno.test("full workflow: create route, execute, log metrics", async () => {
  const ctx = await TestSetupBuilder.create().withAll().build();
  try {
    // Multi-service integration test
  } finally {
    await ctx.cleanup();
  }
});
```

**Example:** See `src/routes/routes_service_test.ts` (722 lines covering all groups)

### Assertion Patterns

Use `@std/expect` from Deno standard library:

```typescript
import { expect } from "@std/expect";

// Basic assertions
expect(value).toBe(expectedValue);
expect(array).toEqual([1, 2, 3]);
expect(result).toBeUndefined();
expect(length).toBeGreaterThan(0);

// Promise rejections
await expect(promise).rejects.toThrow("error message");

// Object matching
expect(route).toEqual({
  name: "hello",
  fileName: "hello.ts",
  methods: ["GET"],
});
```

## Mocking Guidelines

Prefer **real implementations** over mocks. Only mock when necessary.

### Approach A: Simple Helper Functions (Preferred for Unit Tests)

For single-service or low-level tests, create lightweight test context helpers:

```typescript
interface TestContext {
  service: MyService;
  cleanup: () => void;
}

function createTestContext(): TestContext {
  const tempDir = Deno.makeTempDirSync();
  const service = new MyService({ path: tempDir });

  return {
    service,
    cleanup: () => {
      Deno.removeSync(tempDir, { recursive: true });
    },
  };
}

// Optional: Wrapper helper to reduce boilerplate
async function withTestContext(
  testFn: (ctx: TestContext) => void | Promise<void>
): Promise<void> {
  const ctx = createTestContext();
  try {
    await testFn(ctx);
  } finally {
    ctx.cleanup();
  }
}

// Usage
Deno.test("MyService processes data correctly", async () => {
  await withTestContext(async ({ service }) => {
    const result = await service.process("data");
    expect(result).toBe("processed");
  });
});
```

**When to use:** Low-level utilities, encryption tests, file I/O tests

**Examples:**
- `src/env/env_isolator_test.ts` - Environment isolation tests
- `src/encryption/key_storage_service_test.ts` - File-based key storage tests

### Approach B: Real Services via TestSetupBuilder (Preferred for Integration)

For multi-service tests, use TestSetupBuilder to get real implementations:

```typescript
Deno.test("Routes and files work together", async () => {
  const ctx = await TestSetupBuilder.create()
    .withRoutes()  // Also enables FileService
    .build();

  try {
    // Use real services - no mocking needed
    await ctx.fileService.createFile("hello.ts", "export default ...");
    await ctx.routesService.addRoute("hello", "hello.ts", { methods: ["GET"] });

    const routes = await ctx.routesService.getAll();
    expect(routes.length).toBe(1);
  } finally {
    await ctx.cleanup();
  }
});
```

**When to use:** Integration tests, multi-service scenarios

**Examples:**
- `src/routes/routes_service_test.ts` - Routes with file service
- `src/logs/console_log_service_test.ts` - Logs with settings and routes

### Approach C: Manual Mocks (Only When Necessary)

For external boundaries (auth, external APIs), create focused manual mocks:

```typescript
function createMockAuth(options: { authenticated: boolean }): Auth {
  return {
    api: {
      getSession: () => {
        if (options.authenticated) {
          return {
            user: { id: "test-user", email: "test@example.com" },
            session: { id: "test-session", token: "test-token" },
          };
        }
        return null;
      },
    },
  } as unknown as Auth;
}

// Usage
Deno.test("Middleware rejects unauthenticated requests", async () => {
  const auth = createMockAuth({ authenticated: false });
  const app = new Hono();
  app.use(requireAuth(auth));

  const res = await app.request("/protected");
  expect(res.status).toBe(401);
});
```

**When to use:** Authentication, external APIs, third-party services

**Example:** `src/auth/auth_middleware_test.ts` - Auth middleware tests

### General Mocking Principle

**Preference order:**
1. **Real services** (via TestSetupBuilder) - Best for integration
2. **Simple helpers** (lightweight context) - Best for unit tests
3. **Manual mocks** (only at boundaries) - Last resort

## Best Practices

### Always Use Try-Finally Cleanup

```typescript
Deno.test("Example test", async () => {
  const ctx = await TestSetupBuilder.create().withAll().build();
  try {
    // Test logic here
    expect(result).toBe(value);
  } finally {
    await ctx.cleanup();  // ALWAYS cleanup, even on failure
  }
});
```

**Why:** Ensures database connections, temp directories, and file handles are released.

### Request Only Needed Services

```typescript
// Bad - requests everything when only needing metrics
const ctx = await TestSetupBuilder.create().withAll().build();

// Good - minimal context
const ctx = await TestSetupBuilder.create().withMetrics().build();
```

**Why:** Faster tests, clearer dependencies, less setup overhead.

### Use Deferred Data for FK Constraints

```typescript
// Good - route created during build with file dependency satisfied
const ctx = await TestSetupBuilder.create()
  .withRoute("/hello", "hello.ts", { methods: ["GET"] })
  .build();

// Bad - manual creation risks FK violations
const ctx = await TestSetupBuilder.create().withRoutes().build();
await ctx.routesService.addRoute("hello", "hello.ts", { methods: ["GET"] });
// Risk: File might not exist, FK constraint fails
```

### Test Pure Functions Separately

```typescript
// No setup needed - test pure validation logic directly
Deno.test("validateEmail accepts valid emails", () => {
  expect(validateEmail("user@example.com")).toBe(true);
  expect(validateEmail("invalid")).toBe(false);
});
```

**Why:** Faster, simpler, no cleanup overhead.

### Async/Await Properly

```typescript
// Good - proper async/await
await expect(
  routesService.addRoute("duplicate", "test.ts", { methods: ["GET"] })
).rejects.toThrow("already exists");

// Bad - missing await on async assertion
expect(
  routesService.addRoute("duplicate", "test.ts", { methods: ["GET"] })
).rejects.toThrow("already exists");  // Won't work!
```

### Comprehensive Concurrency Coverage

For services with concurrent access patterns, test thoroughly:

```typescript
Deno.test("concurrent writes are serialized", async () => {
  const ctx = await TestSetupBuilder.create().withRoutes().build();
  try {
    const writes = Array.from({ length: 10 }, (_, i) =>
      ctx.routesService.addRoute(`route${i}`, `file${i}.ts`, { methods: ["GET"] })
    );

    await Promise.all(writes);

    const routes = await ctx.routesService.getAll();
    expect(routes.length).toBe(10);  // All writes succeeded
  } finally {
    await ctx.cleanup();
  }
});
```

## Anti-Patterns to Avoid

### ❌ No Test-Only Methods in Production Code

```typescript
// Bad - polluting production class with test-only method
class RoutesService {
  async getAllForTesting() {  // ❌
    return this.getAll();
  }
}

// Good - use public API
const routes = await routesService.getAll();
```

### ❌ No Excessive Mocking of Internal Services

```typescript
// Bad - mocking internal service instead of using real one
const mockFileService = {
  getFile: () => Promise.resolve("content"),
};

// Good - use TestSetupBuilder for real services
const ctx = await TestSetupBuilder.create()
  .withRoutes()  // Includes real FileService
  .build();
```

### ❌ No Skipped Cleanup

```typescript
// Bad - missing cleanup on early return
Deno.test("Bad test", async () => {
  const ctx = await TestSetupBuilder.create().withAll().build();
  if (someCondition) {
    return;  // ❌ Leaked resources!
  }
  await ctx.cleanup();
});

// Good - try-finally ensures cleanup
Deno.test("Good test", async () => {
  const ctx = await TestSetupBuilder.create().withAll().build();
  try {
    if (someCondition) {
      return;  // ✅ Cleanup still happens
    }
  } finally {
    await ctx.cleanup();
  }
});
```

### ❌ No Hardcoded Schemas in Tests

```typescript
// Bad - duplicating schema in test
await db.exec(`
  CREATE TABLE routes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
  );
`);

// Good - use migrations via TestSetupBuilder
const ctx = await TestSetupBuilder.create()
  .withRoutes()  // Uses real migrations
  .build();
```

**Exception:** Tests for migration logic itself may use inline schemas for comparison.

### ❌ No Timing-Dependent Assertions

```typescript
// Bad - arbitrary timeout
await new Promise(resolve => setTimeout(resolve, 100));
expect(processCompleted).toBe(true);  // ❌ Flaky!

// Good - await the actual promise
await processPromise;
expect(processCompleted).toBe(true);  // ✅ Deterministic
```

## Related Files

- **TestSetupBuilder:** `src/test/test_setup_builder.ts`
- **Type definitions:** `src/test/types.ts`
- **Service factories:** `src/test/service_factories.ts`
- **Dependency graph:** `src/test/dependency_graph.ts`

## Example Test Files

- **Integration test:** `src/routes/routes_service_test.ts` (722 lines, comprehensive)
- **Unit test (helper pattern):** `src/env/env_isolator_test.ts`
- **Unit test (encryption):** `src/encryption/encryption_service_test.ts`
- **Manual mocking:** `src/auth/auth_middleware_test.ts`
- **Deferred data pattern:** `src/logs/console_log_service_test.ts`
