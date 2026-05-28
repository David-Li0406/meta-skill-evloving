---
name: davenov:cc:expert-nextjs-16
description: Build Next.js 16 applications with modern patterns. Covers Cache Components, proxy.ts, Server/Client Components, Server Actions, and DevTools MCP integration.
---

<objective>
Build Next.js 16 applications from scaffolding through deployment using modern patterns: Cache Components with explicit 'use cache', proxy.ts for routing, Data Access Layer for auth, and Server/Client Component boundaries. Supports full lifecycle: build, debug, test, optimize, ship.
</objective>

<essential_principles>

<principle name="cache-components-are-explicit">
Next.js 16 defaults to NO caching. All dynamic code runs at request time unless you explicitly opt in.

Enable with:
```js
// next.config.js
const nextConfig = { cacheComponents: true }
```

Then use `'use cache'` directive to cache specific components/functions:
```tsx
async function CachedData() {
  'use cache'
  const data = await db.query(...)
  return <div>{data}</div>
}
```

Control cache lifetime with `cacheLife()` and tag for revalidation with `cacheTag()`.
</principle>

<principle name="proxy-replaces-middleware">
`proxy.ts` replaces `middleware.ts` in Next.js 16. It runs on Node.js runtime (NOT Edge).

**Migration:** Rename `middleware.ts` → `proxy.ts`, rename export to `proxy`.

**Proxy is ONLY for:**
- Rewrites
- Redirects
- Headers
- High-level traffic control (e.g., redirect users without session cookie)

**Proxy is NOT for:**
- Authentication logic (use Data Access Layer)
- Database calls
- Complex business logic
- Session management

Use Server Layout Guards or Data Access Layer (DAL) for auth checks.
</principle>

<principle name="server-client-component-boundary">
Server Components are default. Add `'use client'` only when needed for:
- Event handlers (onClick, onChange)
- useState, useEffect, useReducer
- Browser-only APIs (localStorage, window)

**Pattern:** Fetch data in Server Components, pass to Client Components as props.

```tsx
// Server Component (default)
export default async function Page() {
  const data = await getData()
  return <ClientButton data={data} />
}

// Client Component
'use client'
export function ClientButton({ data }) {
  return <button onClick={() => handleClick(data)}>Click</button>
}
```

Push `'use client'` boundary as low as possible in component tree.
</principle>

<principle name="data-access-layer-for-auth">
Never rely on proxy/middleware for authentication. Use Data Access Layer (DAL) pattern:

```tsx
// lib/dal.ts
export async function getUser() {
  const session = await verifySession()
  if (!session) redirect('/login')
  return session.user
}

// Any page/component
export default async function Dashboard() {
  const user = await getUser() // Auth check happens here
  return <div>Welcome {user.name}</div>
}
```

This ensures auth is verified at every data access point, not just at route level.
</principle>

<principle name="turbopack-is-default">
Turbopack is the default bundler in Next.js 16. Benefits:
- 10x faster Fast Refresh
- 2-5x faster production builds

No configuration needed. Webpack is still available via `--webpack` flag if needed.
</principle>

</essential_principles>

<quick_start>
**What would you like to do?**

1. Build a new Next.js 16 app
2. Debug an existing app
3. Add a feature
4. Write/run tests
5. Optimize performance
6. Ship/deploy
7. Migrate from Next.js 15
8. Something else

**Wait for response before proceeding.**
</quick_start>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "new", "create", "build", "start", "scaffold" | `workflows/build-new-app.md` |
| 2, "broken", "fix", "debug", "crash", "bug", "error" | `workflows/debug-app.md` |
| 3, "add", "feature", "implement", "change" | `workflows/add-feature.md` |
| 4, "test", "tests", "TDD", "coverage" | `workflows/write-tests.md` |
| 5, "slow", "optimize", "performance", "fast", "bundle" | `workflows/optimize-performance.md` |
| 6, "ship", "release", "deploy", "publish", "vercel", "docker" | `workflows/ship-app.md` |
| 7, "migrate", "upgrade", "from 15", "migration" | `workflows/migrate-from-15.md` |
| 8, other | Clarify, then select workflow or references |

**After reading the workflow, follow it exactly.**
</routing>

<verification_loop>
After every change:

```bash
# 1. Does it build?
npm run build

# 2. Do types pass?
npx tsc --noEmit

# 3. Does it run?
npm run dev
# Then check http://localhost:3000

# 4. Do tests pass? (if applicable)
npm test
```

Report to user:
- "Build: OK" or "Build: X errors"
- "Types: OK" or "Types: X errors"
- "Dev server: Running at localhost:3000"
</verification_loop>

<reference_index>

**Architecture:**
- architecture.md - Project structure, App Router patterns, route groups
- server-client-components.md - When to use Server vs Client Components

**Core Features:**
- cache-components.md - use cache, cacheLife, cacheTag, revalidation
- proxy.md - proxy.ts patterns, migration from middleware
- server-actions.md - Form handling, mutations, optimistic updates
- data-fetching.md - Fetching patterns, streaming, Suspense

**Authentication & Security:**
- authentication.md - Auth patterns, DAL, Server Layout Guards
- security.md - CSP, CORS, CVE mitigations, Server Action security

**Performance:**
- performance.md - React Compiler, bundle optimization, Turbopack
- image-optimization.md - next/image, formats, sizing
- font-optimization.md - next/font, preloading, subsetting

**Development:**
- devtools-mcp.md - AI-assisted debugging, MCP integration
- testing.md - Unit tests, integration tests, E2E with Playwright

**Deployment:**
- deployment-vercel.md - Zero-config Vercel deployment
- deployment-docker.md - Docker containerization, multi-stage builds
- deployment-self-hosted.md - Node.js server, standalone output

**Migration:**
- migration-from-15.md - Breaking changes, codemods, upgrade path

</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| build-new-app.md | Create new Next.js 16 app from scratch |
| debug-app.md | Find and fix bugs using DevTools MCP |
| add-feature.md | Add features using Next.js 16 patterns |
| write-tests.md | Write and run tests |
| optimize-performance.md | Profile and speed up the app |
| ship-app.md | Deploy to Vercel, Docker, or self-hosted |
| migrate-from-15.md | Upgrade from Next.js 15 |
</workflows_index>

<success_criteria>
A well-built Next.js 16 app:
- Uses `cacheComponents: true` with explicit `use cache` directives
- Uses `proxy.ts` only for routing (NOT auth)
- Has clear Server/Client Component boundaries
- Uses Data Access Layer for authentication
- Builds without errors
- Has TypeScript strict mode enabled
- Passes all tests
- Scores well on Core Web Vitals
</success_criteria>
