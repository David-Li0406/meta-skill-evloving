# flywheel-convex

Convex backend TDD loop for TypeScript functions.

## philosophy

> "test the function, not the framework"

convex-test provides isolated function testing. use it for mutations, queries, and actions.

## prerequisites

| requirement | check |
|-------------|-------|
| convex | `npx convex --version` |
| convex-test | `grep convex-test package.json` |
| vitest | `grep vitest package.json` |

## setup

```bash
# install convex-test
pnpm add -D convex-test

# verify config
cat convex/vitest.config.ts
```

## flywheel sequence

### 1. discover

```bash
# list functions
fd -e ts . convex --exclude _generated | outline -c --format=yaml

# list existing tests
fd -e test.ts . convex
```

### 2. write test first

establish test infrastructure with reusable helpers:

```typescript
// __tests__/setup.ts
import { convexTest } from 'convex-test';
import type { Id } from '../convex/_generated/dataModel';
import schema from '../convex/schema';
import { modules } from '../test-setup/convex.setup';

export type TestContext = ReturnType<typeof convexTest<typeof schema>>;

export function createTestContext(): TestContext {
  return convexTest(schema, modules);
}

// reusable test data helpers
export async function withTestUser(
  t: TestContext,
  overrides: Partial<{ clerkId: string; email: string }> = {}
): Promise<{ userId: Id<'users'>; clerkId: string }> {
  const clerkId = overrides.clerkId ?? `test-${Date.now()}`;
  const userId = await t.run(async (ctx) => {
    return await ctx.db.insert('users', {
      clerkId,
      email: overrides.email ?? `${clerkId}@test.com`,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    });
  });
  return { userId, clerkId };
}
```

then write tests using helpers:

```typescript
// __tests__/messages.test.ts
import { describe, expect, it } from 'vitest';
import { api } from '../convex/_generated/api';
import { createTestContext, withTestUser } from './setup';

describe('messages', () => {
  it('creates a message', async () => {
    const t = createTestContext();
    const { clerkId } = await withTestUser(t);

    await t.mutation(api.messages.send, {
      content: 'Hello',
      userId: clerkId,
    });

    const messages = await t.query(api.messages.list, {});
    expect(messages).toHaveLength(1);
    expect(messages[0].content).toBe('Hello');
  });
});
```

### 3. run tests

```bash
# all convex tests
pnpm vitest convex

# specific file
pnpm vitest convex/messages.test.ts

# watch mode
pnpm vitest convex --watch
```

### 4. implement function

```typescript
// convex/messages.ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const send = mutation({
  args: { content: v.string(), userId: v.id("users") },
  handler: async (ctx, { content, userId }) => {
    return await ctx.db.insert("messages", {
      content,
      userId,
      createdAt: Date.now(),
    });
  },
});

export const list = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("messages").collect();
  },
});
```

### 5. verify & iterate

```bash
# run test
pnpm vitest convex/messages.test.ts

# if passing, run full suite
pnpm vitest convex

# deploy code
npx convex deploy -y
```

### ⚠️ CRITICAL: Dev vs Prod CLI Targeting

**`npx convex run` defaults to DEV. Use `--prod` for production data.**

```bash
# DEV (default)
npx convex run myFunction '{}'

# PROD (always add --prod for production data operations)
npx convex run myFunction '{}' --prod

# Verify both match after seeding/migrations
npx convex run debug:check '{}'         # DEV
npx convex run debug:check '{}' --prod  # PROD
```

## copilot integration

use copilot for convex function analysis:

```bash
copilot -p --model gemini-3-pro --workspace $(pwd) "
Convex function review.

Schema: $(cat convex/schema.ts)
Function: $(cat convex/$FILE.ts)
Test: $(cat convex/$FILE.test.ts)

Check:
1. Type safety with schema
2. Edge cases in test
3. Index usage for queries

Output JSON:
{
  \"issues\": [\"issue1\", \"issue2\"],
  \"missing_tests\": [\"edge case 1\"],
  \"confidence\": 0-10
}
"
```

## test patterns

### authenticated context

```typescript
test("requires auth", async () => {
  const t = convexTest(schema);

  // without auth - should throw
  await expect(
    t.mutation(api.messages.send, { content: "hi" })
  ).rejects.toThrow();

  // with auth
  const asUser = t.withIdentity({ subject: "user123" });
  await asUser.mutation(api.messages.send, { content: "hi" });
});
```

### scheduled functions

```typescript
test("scheduled job runs", async () => {
  const t = convexTest(schema);

  await t.mutation(api.jobs.schedule, {});

  // advance time
  await t.finishInProgressScheduledFunctions();

  // verify side effect
  const results = await t.query(api.jobs.getResults, {});
  expect(results).toHaveLength(1);
});
```

## common issues

| symptom | likely cause | fix |
|---------|--------------|-----|
| type error | schema mismatch | update schema or function |
| test isolation | shared state | use fresh convexTest() |
| missing _generated | not generated | `npx convex dev --once` |
| auth error | missing identity | use withIdentity() |

## frontend patterns

### discriminated union for loading states

use QueryState type for hooks consuming Convex queries:

```typescript
// hooks/use-data.ts
export type QueryState<T> =
  | { status: "loading"; data: undefined }
  | { status: "ready"; data: T }
  | { status: "empty"; data: T };

function createQueryState<T>(result: T | undefined): QueryState<T> {
  if (result === undefined) return { status: "loading", data: undefined };
  if (Array.isArray(result) && result.length === 0) return { status: "empty", data: result };
  return { status: "ready", data: result };
}

export function useItems(): QueryState<Doc<"items">[]> {
  const items = useQuery(api.items.list, {});
  return createQueryState(items);
}
```

consume in components:

```tsx
function ItemList() {
  const itemsState = useItems();

  if (itemsState.status === 'loading') {
    return <Skeleton className="h-32 w-full" />;
  }

  if (itemsState.status === 'empty') {
    return <EmptyState />;
  }

  return itemsState.data.map(item => <ItemCard key={item._id} item={item} />);
}
```

## projects

| project | path | convex dir |
|---------|------|------------|
| arbor | ~/Developer/arbor/arbor-xyz | packages/backend/convex |
| ascii | ~/Developer/ascii/ascii-xyz | packages/backend/convex |
| koto | ~/Developer/koto/koto-xyz | packages/backend/convex |
| kumori | ~/Developer/kumori/kumori-xyz | packages/backend/convex |
| webs | ~/Developer/webs/webs-xyz | packages/backend/convex |

## anti-patterns

- **testing without schema**: always import schema
- **shared test state**: each test gets fresh convexTest()
- **skipping TDD**: write test before function
- **ignoring types**: convex-test is fully typed
- **`convex run` without `--prod`**: data goes to DEV only, not production
- **not verifying after deployment**: DEV and PROD environments can drift
