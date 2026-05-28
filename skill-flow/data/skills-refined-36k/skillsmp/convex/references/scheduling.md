# Scheduling: Cron + Scheduler

## Cron Jobs (`convex/crons.ts`)

Basic pattern:

```ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";
import { internalAction } from "./_generated/server";

const empty = internalAction({
  args: {},
  handler: async (ctx, args) => {
    console.log("empty");
    return null;
  },
});

const crons = cronJobs();

// Run internal.crons.empty every 2 hours.
crons.interval("delete inactive users", { hours: 2 }, internal.crons.empty, {});

export default crons;
```

Rules:
- Use **only** `crons.interval` or `crons.cron` (skip `crons.hourly/daily/weekly` helpers)
- Cron functions should be **internal** (`internalQuery`, `internalMutation`, `internalAction`)
- If a cron calls an internal function in the same file, still import `internal` and call via `internal.*`

## `ctx.scheduler.runAfter`

From mutations or actions, you can enqueue scheduled jobs:

```ts
await ctx.scheduler.runAfter(
  1000, // delay ms
  internal.someFile.someInternalMutation,
  { someArg: "value" },
);
```

## Rules & Caveats

- **First arg must be a function reference**, not the function or a string
- Auth context **does not propagate** into scheduled jobs:
  - `getAuthUserId()` and `ctx.getUserIdentity()` will **always return null**
  - So scheduled jobs should usually call **internal** functions that don't rely on user identity
- Do not schedule jobs **too frequently** (not more than once every ~10 seconds for same thing)
- Use scheduled jobs sparingly (e.g. background cleanup, async follow-ups)
