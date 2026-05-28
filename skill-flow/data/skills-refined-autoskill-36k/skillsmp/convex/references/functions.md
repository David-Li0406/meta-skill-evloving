# Functions

## Public vs Internal Functions

Convex functions are registered via helpers from `./_generated/server`:

**Public API** (callable from client / HTTP):
- `query`
- `mutation`
- `action`

**Internal-only** (callable only from other Convex functions):
- `internalQuery`
- `internalMutation`
- `internalAction`

```ts
import {
  query,
  mutation,
  internalQuery,
  internalMutation,
  internalAction,
} from "./_generated/server";
import { v } from "convex/values";
```

## When to Use Which

### query
- Read-only (no writes)
- Fast (< 1 second)
- Realtime subscriptions (via `useQuery`)

### mutation
- Database writes / transactions
- Short-lived (same 1 second constraint)

### action
- Long-running and/or network-heavy tasks
- Runs in Node runtime
- Can use arbitrary Node modules
- **No direct `ctx.db` access** (must use `ctx.runQuery` / `ctx.runMutation`)

### Internal variants
Same as above, but **not exposed** to clients.

## Function Registration

You **must** register functions like:

```ts
export const listMessages = query({
  args: { channelId: v.id("channels") },
  handler: async (ctx, args) => {
    // ...
  },
});
```

Rules:
- You **cannot** dynamically register functions via `api` or `internal`
- Every function needs **argument validators**
- If a JS function doesn't return anything, it implicitly returns `null`

## Calling Other Functions

From inside Convex functions:

- `ctx.runQuery(api.someFile.someQuery, args)`
- `ctx.runMutation(api.someFile.someMutation, args)`
- `ctx.runAction(api.someFile.someAction, args)`

Rules:
- You **must** pass a **function reference** (like `api.example.f`), not the function itself
- From **actions**, use `ctx.runQuery` / `ctx.runMutation` to talk to the DB – **never** `ctx.db`
- When calling another function from the **same file**, add a **type annotation** to avoid TypeScript circularity issues

Example:

```ts
import { api } from "./_generated/api";

export const f = query({
  args: { name: v.string() },
  handler: async (ctx, args) => {
    return "Hello " + args.name;
  },
});

export const g = query({
  args: {},
  handler: async (ctx, args) => {
    const result: string = await ctx.runQuery(api.example.f, { name: "Bob" });
    return null;
  },
});
```

## Function References via `api` and `internal`

The generated file `./_generated/api` exports:

```ts
import { api, internal } from "./_generated/api";
```

- For a public function `export const f = query(...)` in `convex/example.ts`:
  - Reference: `api.example.f`
- For an internal function `export const g = internalMutation(...)` in `convex/example.ts`:
  - Reference: `internal.example.g`
- Nested directories mirror the path: `convex/messages/access.ts` → `api.messages.access.h`

Use:
- `api.*` when called from client / other functions for **public** functions
- `internal.*` for **internal** functions from other Convex functions
