# Actions & HTTP Endpoints

## Actions

Files containing actions that use Node modules should start with:

```ts
"use node";
```

Rules:
- **Only** actions in `"use node"` files (no queries/mutations)
- **Never** call `ctx.db` inside actions
  - Use `ctx.runQuery`, `ctx.runMutation`, `ctx.runAction`
- **No dynamic imports in queries/mutations** - only actions support `await import()`
  - Bad: `const { foo } = await import('./module');` inside a query/mutation
  - Good: `import { foo } from './module';` at top of file
  - Actions can use dynamic imports because they run in Node.js environment
- Use actions for:
  - Calling external APIs (OpenAI, Resend, etc.)
  - Long-running tasks (up to **10 minutes**)

Basic action:

```ts
import { action } from "./_generated/server";

export const exampleAction = action({
  args: {},
  handler: async (ctx, args) => {
    console.log("This action does not return anything");
    return null;
  },
});
```

## HTTP Endpoints (`httpAction`)

Define in `convex/http.ts` using `httpRouter`:

```ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

http.route({
  path: "/echo",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    const body = await req.bytes();
    return new Response(body, { status: 200 });
  }),
});

export default http;
```

Notes:
- Path is **exact** (`/api/someRoute` → route is exactly that)
- HTTP actions can stream up to **20MiB** out
