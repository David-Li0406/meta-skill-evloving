---
name: chain-of-responsibility-pattern-typescript
description: Composable handler chains for checks/pipelines with early-exit; TS/Node-friendly functional or object handlers, runtime ordering, and trade-offs vs middleware/decorator/strategy.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Chain of Responsibility (TypeScript)

## Intent

Route a request through a sequence of handlers where each can handle, transform, or short-circuit processing.

## When to use

- Sequential validation/auth checks are required.
- Early exit is necessary when a handler rejects or fully handles.
- Handler order must be configurable at runtime.
- Different contexts need different subsets of handlers.
- You want reusable handlers across flows.
- You need to add/remove steps without changing the caller.
- You want a composable pipeline with explicit stop/continue semantics.

## When NOT to use

- A single algorithm swap is enough (Strategy).
- All stages must always run (simple pipeline).
- It’s overkill for two small steps.
- The sequence is fixed and centralized forever.
- You need a different interface (Adapter).
- You need explicit stacking of behavior (Decorator).
- The flow would be clearer as one function.

## Recommended TS shapes

- Functional handlers + explicit Result union (preferred).
- Object handlers with `handle()` (alternative).
- Optional base class (brief) for teams that prefer it.

## Example 1: Guard chain (auth → rate limit → validate)

```ts
type Ctx = { userId: string | null; ip: string; payload: { name?: string } };

type Result =
  | { type: "continue"; ctx: Ctx }
  | { type: "handled"; message: string }
  | { type: "error"; message: string };

type Handler = (ctx: Ctx) => Result | Promise<Result>;

const auth: Handler = (ctx) =>
  ctx.userId ? { type: "continue", ctx } : { type: "error", message: "unauthorized" };

const rateLimit: Handler = (ctx) =>
  ctx.ip === "blocked" ? { type: "error", message: "rate limited" } : { type: "continue", ctx };

const validate: Handler = (ctx) =>
  ctx.payload.name ? { type: "continue", ctx } : { type: "error", message: "name required" };

async function runChain(handlers: Handler[], ctx: Ctx): Promise<Result> {
  let current = ctx;
  for (const h of handlers) {
    const res = await h(current);
    if (res.type === "continue") current = res.ctx;
    else return res;
  }
  return { type: "handled", message: "ok" };
}

const result = await runChain([auth, rateLimit, validate], { userId: "u1", ip: "ok", payload: { name: "a" } });
```

## Example 2: Transform chain (normalize → enrich → route)

```ts
type Ctx = { raw: string; normalized?: string; enriched?: string; route?: string };

type Result = { type: "continue"; ctx: Ctx } | { type: "handled"; message: string };

type Handler = (ctx: Ctx) => Result;

const normalize: Handler = (ctx) => ({ type: "continue", ctx: { ...ctx, normalized: ctx.raw.trim().toLowerCase() } });
const enrich: Handler = (ctx) => ({ type: "continue", ctx: { ...ctx, enriched: `${ctx.normalized}-enriched` } });
const route: Handler = (ctx) => ({ type: "handled", message: `route:${ctx.enriched}` });

function runChain(handlers: Handler[], ctx: Ctx): Result {
  let current = ctx;
  for (const h of handlers) {
    const res = h(current);
    if (res.type === "continue") current = res.ctx;
    else return res;
  }
  return { type: "handled", message: "done" };
}

runChain([normalize, enrich, route], { raw: " Hello " });
```

## Example 3: Handle-or-pass chain

```ts
type Ctx = { id: string };

type Result = { type: "handled"; value: string } | { type: "continue" };

type Handler = (ctx: Ctx) => Result;

const fromCache: Handler = (ctx) => (ctx.id === "hit" ? { type: "handled", value: "cache" } : { type: "continue" });
const fromDb: Handler = (ctx) => ({ type: "handled", value: "db" });

function firstHandler(handlers: Handler[], ctx: Ctx): Result {
  for (const h of handlers) {
    const res = h(ctx);
    if (res.type === "handled") return res;
  }
  return { type: "handled", value: "none" };
}

firstHandler([fromCache, fromDb], { id: "miss" });
```

## Testing strategy (pragmatic)

- Unit test handlers in isolation.
- Integration test a composed chain with a fixed order.
- Avoid time-based flakiness by isolating rate limits/timeouts.

## Common pitfalls

- Unclear stop conditions.
- Hidden shared state between handlers.
- Async double-calls of handlers.
- Order dependency not documented.
- Handler doing too much (god handler).
- Mixed error semantics (exceptions vs Result).
- Chains that grow without composition discipline.
- Overusing CoR for simple flows.

## Checklist for refactors

- Define ctx shape explicitly.
- Define Result union and stop/continue semantics.
- Keep handlers small and independent.
- Compose chain in one place (composition root).
- Make stop conditions explicit.
- Test each handler and a full chain.
- Document handler order and why it matters.
- Avoid shared mutable state across handlers.

## Output expectations

When invoked, produce:
- Chain ordering and handler list.
- ctx/result types and stop conditions.
- Wiring plan and tests.
