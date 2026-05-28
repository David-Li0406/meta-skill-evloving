# Testing with convex-test

The `convex-test` library provides a mock implementation of the Convex backend for fast automated testing.

## Setup

Install dependencies:

```bash
npm install --save-dev convex-test vitest @edge-runtime/vm
```

Add to `package.json`:

```json
"scripts": {
  "test": "vitest",
  "test:once": "vitest run",
  "test:coverage": "vitest run --coverage --coverage.reporter=text"
}
```

Create `vitest.config.ts`:

```ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "edge-runtime",
    server: { deps: { inline: ["convex-test"] } },
  },
});
```

## Basic Test Structure

```ts
import { convexTest } from "convex-test";
import { describe, it, expect } from "vitest";
import { api, internal } from "./_generated/api";
import schema from "./schema";

describe("posts", () => {
  it("returns empty array when no posts exist", async () => {
    const t = convexTest(schema, modules);
    const posts = await t.query(api.posts.list);
    expect(posts).toEqual([]);
  });

  it("creates and lists posts", async () => {
    const t = convexTest(schema, modules);

    await t.mutation(api.posts.create, { title: "Hello", content: "World" });

    const posts = await t.query(api.posts.list);
    expect(posts).toHaveLength(1);
    expect(posts[0].title).toBe("Hello");
  });
});

const modules = import.meta.glob("./**/*.ts");
```

**Key points:**

- Always pass `schema` to `convexTest()` for proper validation and typing
- The `modules` glob must be defined in the test file for Vite's module resolution
- Each test gets a fresh mock database—no cleanup needed

## Calling Functions

```ts
const t = convexTest(schema, modules);

// Queries
const result = await t.query(api.myFile.myQuery, { arg: "value" });

// Mutations
await t.mutation(api.myFile.myMutation, { arg: "value" });

// Actions
await t.action(api.myFile.myAction, { arg: "value" });

// Internal functions work the same way
await t.mutation(internal.myFile.internalMutation, { arg: "value" });
```

## Direct Data Manipulation with `t.run`

Use `t.run` to set up test data or inspect state without needing declared functions:

```ts
test("setup and inspect data", async () => {
  const t = convexTest(schema, modules);

  // Insert test data directly
  const taskId = await t.run(async (ctx) => {
    return await ctx.db.insert("tasks", { text: "Test task", done: false });
  });

  // Call your function
  await t.mutation(api.tasks.complete, { id: taskId });

  // Verify the result
  const task = await t.run(async (ctx) => {
    return await ctx.db.get(taskId);
  });
  expect(task?.done).toBe(true);
});
```

## Testing HTTP Actions

```ts
test("http endpoint", async () => {
  const t = convexTest(schema, modules);

  const response = await t.fetch("/api/webhook", {
    method: "POST",
    body: JSON.stringify({ event: "test" }),
  });

  expect(response.status).toBe(200);
  const data = await response.json();
  expect(data.success).toBe(true);
});
```

## Testing Scheduled Functions

Use Vitest's fake timers to control time:

```ts
import { vi } from "vitest";

test("scheduled function executes", async () => {
  vi.useFakeTimers();

  const t = convexTest(schema, modules);

  // Call function that schedules something
  await t.mutation(api.tasks.scheduleReminder, { delayMs: 10000 });

  // Advance time past the scheduled time
  vi.advanceTimersByTime(11000);

  // Wait for in-progress scheduled functions to complete
  await t.finishInProgressScheduledFunctions();

  // Or wait for ALL scheduled functions (including chains):
  // await t.finishAllScheduledFunctions(vi.runAllTimers);

  // Assert the scheduled function's effect
  const reminders = await t.query(api.tasks.listReminders);
  expect(reminders).toHaveLength(1);

  vi.useRealTimers();
});
```

## Testing Authenticated Functions

Use `t.withIdentity` to simulate authenticated users:

```ts
test("user-specific data", async () => {
  const t = convexTest(schema, modules);

  // Create identity with custom attributes
  const asSarah = t.withIdentity({ name: "Sarah", email: "sarah@example.com" });
  const asLee = t.withIdentity({ name: "Lee" });

  // Sarah creates a task
  await asSarah.mutation(api.tasks.create, { text: "Sarah's task" });

  // Sarah sees her task
  const sarahsTasks = await asSarah.query(api.tasks.myTasks);
  expect(sarahsTasks).toHaveLength(1);

  // Lee sees no tasks
  const leesTasks = await asLee.query(api.tasks.myTasks);
  expect(leesTasks).toHaveLength(0);
});
```

`issuer`, `subject`, and `tokenIdentifier` are auto-generated if not provided.

## Mocking Fetch Calls

```ts
import { vi } from "vitest";

test("action calling external API", async () => {
  const t = convexTest(schema, modules);

  vi.stubGlobal(
    "fetch",
    vi.fn(async () => ({
      ok: true,
      json: async () => ({ data: "mocked response" }),
    }) as Response),
  );

  const result = await t.action(api.external.callApi);
  expect(result).toBe("mocked response");

  vi.unstubAllGlobals();
});
```

## Asserting Errors

```ts
test("validation error", async () => {
  const t = convexTest(schema, modules);

  await expect(async () => {
    await t.mutation(api.messages.send, { body: "" });
  }).rejects.toThrowError("Message body cannot be empty");
});
```

## Limitations

The mock differs from the real Convex backend:

- **No limits enforced** – size and time limits aren't checked
- **Simplified text search** – returns all docs with matching prefix, no relevance sorting
- **Simplified vector search** – correct results but no efficient index
- **No cron jobs** – trigger cron handlers manually from tests
- **Different runtime** – Vitest uses Edge Runtime mock, not actual Convex runtime
- **ID format differs** – don't rely on specific ID formats

For testing against a real Convex backend, see the Convex docs on testing with a local backend.
