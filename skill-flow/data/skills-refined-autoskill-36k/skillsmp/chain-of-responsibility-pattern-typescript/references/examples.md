# Chain of Responsibility Examples (TypeScript)

## Example 1: Guard chain with early-exit

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

await runChain([auth, rateLimit, validate], { userId: "u1", ip: "ok", payload: { name: "a" } });
```

## Example 2: Transform/enrichment chain

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

## CoR vs Middleware vs Decorator vs Strategy (tiny sketches)

```ts
// CoR: handlers can stop or pass
const handlers = [(ctx: any) => ({ type: "continue", ctx }), (ctx: any) => ({ type: "handled", value: ctx })];

// Middleware: framework contract with next()
function mw(ctx: any, next: () => Promise<void>) { return next(); }

// Decorator: wrappers that always delegate
class Decorator { constructor(private inner: { run(): void }) {} run() { this.inner.run(); } }

// Strategy: swap one algorithm
interface Strategy { run(x: number): number; }
```
