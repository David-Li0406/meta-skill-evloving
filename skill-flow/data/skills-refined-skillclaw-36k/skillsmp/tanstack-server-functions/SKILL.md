---
name: tanstack-server-functions
description: Use this when implementing TanStack Start server functions and middleware (validation, auth, redirects, request context) in the Cloudflare Workers runtime.
---

# TanStack Start server functions + middleware

Use this skill when you need server-only logic in `apps/user-application` that’s callable from routes/components, with full type-safety.

## Where things go (this repo)

- Server functions: `apps/user-application/src/core/functions/*`
- Middleware: `apps/user-application/src/core/middleware/*`
- Server entry (Cloudflare Worker): `apps/user-application/src/server.ts`

## Server function basics (upstream)

Server functions are defined with `createServerFn` from `@tanstack/react-start`.

- GET (default): `createServerFn().handler(...)`
- POST (mutations): `createServerFn({ method: "POST" }).handler(...)`

They accept a single input parameter (usually passed as `{ data: ... }` from the client) and should validate input at the boundary.

### Validation

Upstream supports passing a schema directly:

- `createServerFn({ method: "POST" }).inputValidator(MyZodSchema).handler(...)`

This repo also commonly uses:

- `.inputValidator((data: z.infer<typeof Schema>) => Schema.parse(data))`

Validated input is available as `ctx.data` inside `.handler(...)`.

## Middleware composition

Use `createMiddleware` from `@tanstack/react-start`.

- `type: "function"` applies to specific server functions.
- `type: "request"` applies more broadly (request lifecycle).

Pattern used in this repo:

- Create middleware in `apps/user-application/src/core/middleware/*` that adds `context`.
- Create a `baseFunction = createServerFn().middleware([...])`.
- Build functions off the base.

Examples already in-repo:

- Auth middleware: `apps/user-application/src/core/middleware/auth.ts`
- Polar SDK middleware: `apps/user-application/src/core/middleware/polar.ts`
- Example server function: `apps/user-application/src/core/functions/example-functions.ts`

## Auth + request access (this repo)

- Better Auth is wired in the Cloudflare worker entry: `apps/user-application/src/server.ts`.
- Use `getRequest()` from `@tanstack/react-start/server` in middleware to read the current request.
- Auth middleware throws on missing session (see `protectedFunctionMiddleware`).

## Errors, redirects, not-found (upstream)

- Throw `new Error("...")` for serializable errors.
- Throw `redirect({ to: "/login" })` from `@tanstack/react-router` for auth flows.
- Throw `notFound()` from `@tanstack/react-router` when a resource is missing.

## Request utilities (upstream)

From `@tanstack/react-start/server`:

- `getRequest()` / `getRequestHeader()` for request inspection
- `setResponseHeader()` / `setResponseStatus()` for custom responses
- `getRequestIP()` for IP (already used in `apps/user-application/src/core/functions/payments.ts`)

## Static server functions (upstream, experimental)

Use `staticFunctionMiddleware` from `@tanstack/start-static-server-functions`:

- `createServerFn({ method: "GET" }).middleware([staticFunctionMiddleware]).handler(...)`

Important: `staticFunctionMiddleware` must be the final middleware.

## Cloudflare bindings

- Access bindings via `import { env } from "cloudflare:workers"`.
- Use `.dev.vars` for local secrets in `apps/user-application`.

## Client integration (TanStack Query)

Server functions can be passed directly to TanStack Query:

- `useMutation({ mutationFn: myServerFn })`
- `useQuery({ queryFn: () => myServerFn({ data: ... }) })`

This repo includes a demo at `apps/user-application/src/components/demo/middleware-demo.tsx`.
