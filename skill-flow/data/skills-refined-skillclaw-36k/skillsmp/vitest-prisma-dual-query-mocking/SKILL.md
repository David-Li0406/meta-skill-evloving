---
name: vitest-prisma-dual-query-mocking
description: |
  Mock Prisma/ZenStack queries when code uses both findFirst and findUnique on the same model.
  Use when: (1) Tests fail with "Cannot read property of undefined", (2) Code queries same
  model with different methods (findFirst for search, findUnique for exact match), (3) Mock
  returns undefined for one query type, (4) Single mockImplementation doesn't cover all cases.
  Covers Vitest + Prisma/ZenStack testing patterns with multiple query methods.
author: Claude Code
version: 1.0.0
date: 2026-01-23
---

# Vitest Prisma Dual Query Mocking

## Problem

When code uses both `findFirst` and `findUnique` on the same Prisma/ZenStack model, a single
mock implementation doesn't work correctly. One query returns the mocked data while the other
returns `undefined`, causing test failures.

## Context / Trigger Conditions

- Test error: "Cannot read properties of undefined (reading 'value')" or similar
- Code uses `db.model.findFirst({ where: {...} })` for one query
- Code uses `db.model.findUnique({ where: { composite_key: {...} } })` for another query
- Both queries target the same model (e.g., `userPreference`)
- Single mock like `mockDb.model.findFirst = vi.fn().mockResolvedValue(data)` doesn't cover both
- Tests pass individually but fail when both queries run in same test

**Example failing test**:
```typescript
// This mock only works for findFirst, not findUnique
mockDb.userPreference.findFirst = vi.fn().mockResolvedValue({
  userId,
  key: "email.notification.messaging",
  value: "true",
});

// This query works
const enabled = await db.userPreference.findFirst({ where: { userId, key: "..." } });

// This query returns undefined (not mocked)
const cooldown = await db.userPreference.findUnique({
  where: { userId_key: { userId, key: "..." } }
});

console.log(cooldown); // undefined - causes test failure
```

## Solution

Create separate mock implementations for each query method, each checking the query parameters
to return appropriate data.

### Pattern 1: Separate Mocks for Each Method

```typescript
import { vi, beforeEach, it, expect } from "vitest";

// Mock database client
const mockDb = {
  userPreference: {
    findFirst: vi.fn(),
    findUnique: vi.fn(),
  },
} as unknown as typeof db;

beforeEach(() => {
  vi.clearAllMocks();
});

it("should handle dual query pattern", async () => {
  const userId = "test-user-id";

  // Mock findFirst for enabled/disabled check
  mockDb.userPreference.findFirst = vi.fn().mockImplementation(({ where }) => {
    if (where.key === "email.notification.messaging") {
      return Promise.resolve({
        userId,
        key: "email.notification.messaging",
        value: "true",
      });
    }
    return Promise.resolve(null);
  });

  // Mock findUnique for composite key lookup (separate implementation)
  mockDb.userPreference.findUnique = vi.fn().mockImplementation(({ where }) => {
    if (where.userId_key?.key === "email.notification.messaging.lastSent") {
      return Promise.resolve({
        userId,
        key: "email.notification.messaging.lastSent",
        value: new Date().toISOString(),
      });
    }
    return Promise.resolve(null);
  });

  // Both queries now work correctly
  const result = await myFunction(mockDb, userId);

  expect(mockDb.userPreference.findFirst).toHaveBeenCalledWith({
    where: { userId, key: "email.notification.messaging" },
  });
  expect(mockDb.userPreference.findUnique).toHaveBeenCalledWith({
    where: {
      userId_key: {
        userId,
        key: "email.notification.messaging.lastSent",
      },
    },
  });
});
```

### Pattern 2: Conditional Mock Based on Query Structure

```typescript
it("should mock based on query structure", async () => {
  // Single mock that handles both query types
  mockDb.userPreference.findFirst = vi.fn().mockImplementation(({ where }) => {
    // Route based on query structure
    if (where.key === "specific.key") {
      return Promise.resolve({ userId, key: where.key, value: "data" });
    }
    return Promise.resolve(null);
  });

  mockDb.userPreference.findUnique = vi.fn().mockImplementation(({ where }) => {
    // Check for composite key pattern
    if (where.userId_key) {
      const key = where.userId_key.key;
      return Promise.resolve({ userId, key, value: "data" });
    }
    return Promise.resolve(null);
  });
});
```

### Pattern 3: Using Vitest Mock Libraries

For complex scenarios, use specialized mocking libraries:

```typescript
import { createPrismaMock } from 'prisma-mock-vitest';
import { beforeEach, expect, test } from 'vitest';

let client: PrismaClient;

beforeEach(async () => {
  client = await createPrismaMock();
});

test("automated mocking handles both queries", async () => {
  // Library automatically handles findFirst, findUnique, and other methods
  const result = await myFunction(client, userId);
  expect(result).toBeDefined();
});
```

## Verification

1. **Check Mock Calls**: Verify both mocks are called with correct parameters
   ```typescript
   expect(mockDb.model.findFirst).toHaveBeenCalledTimes(1);
   expect(mockDb.model.findUnique).toHaveBeenCalledTimes(1);
   ```

2. **Test Isolation**: Each mock should only respond to its specific query pattern
   ```typescript
   // findFirst should not respond to composite key queries
   const result = await mockDb.model.findFirst({
     where: { userId_key: { userId, key } }
   });
   expect(result).toBeNull(); // Should not match
   ```

3. **Return Value Validation**: Ensure mocked data structure matches Prisma schema
   ```typescript
   const data = await mockDb.model.findUnique({ where: { id: "123" } });
   expect(data).toHaveProperty("id");
   expect(data).toHaveProperty("userId");
   ```

## Example

**Real-World Scenario**: Email preference system checking both enabled state and cooldown.

```typescript
// Code being tested
async function shouldSendEmail(db: DB, userId: string) {
  // Query 1: Check if notifications are enabled (findFirst)
  const preference = await db.userPreference.findFirst({
    where: { userId, key: "email.notification.messaging" }
  });

  if (preference?.value !== "true") {
    return { send: false };
  }

  // Query 2: Check cooldown timestamp (findUnique with composite key)
  const cooldown = await db.userPreference.findUnique({
    where: {
      userId_key: {
        userId,
        key: "email.notification.messaging.lastSent",
      },
    },
  });

  if (cooldown) {
    const lastSent = new Date(cooldown.value);
    // Check if within cooldown period...
  }

  return { send: true };
}

// Test with separate mocks
it("should check both enabled state and cooldown", async () => {
  const thirtyMinutesAgo = new Date(Date.now() - 30 * 60 * 1000);

  // Mock findFirst (enabled check)
  mockDb.userPreference.findFirst = vi.fn().mockImplementation(({ where }) => {
    if (where.key === "email.notification.messaging") {
      return Promise.resolve({
        userId: "test-user",
        key: "email.notification.messaging",
        value: "true", // Enabled
      });
    }
    return Promise.resolve(null);
  });

  // Mock findUnique (cooldown check)
  mockDb.userPreference.findUnique = vi.fn().mockImplementation(({ where }) => {
    if (where.userId_key?.key === "email.notification.messaging.lastSent") {
      return Promise.resolve({
        userId: "test-user",
        key: "email.notification.messaging.lastSent",
        value: thirtyMinutesAgo.toISOString(), // Recent send
      });
    }
    return Promise.resolve(null);
  });

  const result = await shouldSendEmail(mockDb, "test-user");

  expect(result.send).toBe(false); // Blocked by cooldown
  expect(mockDb.userPreference.findFirst).toHaveBeenCalledTimes(1);
  expect(mockDb.userPreference.findUnique).toHaveBeenCalledTimes(1);
});
```

## Notes

- **Query Structure Matters**: `findFirst` uses `where: { field: value }`, `findUnique` uses
  `where: { uniqueConstraint: { field: value } }` - check this in mocks
- **Mock Isolation**: Each mock should ONLY respond to its specific query pattern
- **Clear All Mocks**: Always call `vi.clearAllMocks()` in `beforeEach` to prevent test pollution
- **Type Safety**: Use `as unknown as typeof db` to satisfy TypeScript when creating mock objects
- **Library Options**: Consider `prisma-mock-vitest`, `vitest-prisma-mock`, or `prisma-mock`
  for complex scenarios instead of manual mocking
- **Debugging**: Log `where` parameter in mockImplementation to see what queries are being made
- **Common Mistake**: Mocking only `findFirst` when code also uses `findUnique` (or vice versa)

## References

- [The Ultimate Guide to Testing with Prisma: Mocking Prisma Client](https://www.prisma.io/blog/testing-series-1-8eRB5p0Y8o)
- [GitHub - prisma-mock-vitest](https://github.com/james-elicx/prisma-mock-vitest)
- [Testing with Prisma Discussion](https://github.com/prisma/prisma/discussions/2083)
- [The Ultimate Guide to Testing with Prisma: Unit Testing](https://www.prisma.io/blog/testing-series-2-xPhjjmIEsM)
