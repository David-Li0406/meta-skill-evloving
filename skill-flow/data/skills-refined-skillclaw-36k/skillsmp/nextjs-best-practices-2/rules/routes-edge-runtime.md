---
title: Use Edge Runtime for Low-Latency Responses
impact: MEDIUM
impactDescription: Sub-50ms response times from global edge locations
tags: edge, runtime, latency, performance
---

## Use Edge Runtime for Low-Latency Responses

Edge runtime runs your code close to users for minimal latency. Use it for simple, fast operations that don't need Node.js APIs.

**Incorrect (Node.js for simple operations):**

```typescript
// app/api/geo/route.ts
// Default Node.js runtime - centralized, higher latency

export async function GET(request: Request) {
  const country = request.headers.get('x-vercel-ip-country')
  return Response.json({ country })
}
// Response time: 100-300ms depending on user location
```

**Correct (Edge runtime for speed):**

```typescript
// app/api/geo/route.ts
export const runtime = 'edge'

export async function GET(request: Request) {
  const country = request.headers.get('x-vercel-ip-country')
  return Response.json({ country })
}
// Response time: 10-50ms from nearest edge location
```

**Good Edge runtime use cases:**

```typescript
// Simple redirects/rewrites
export const runtime = 'edge'

export async function GET(request: Request) {
  const country = request.geo?.country || 'US'
  const url = new URL(request.url)
  url.pathname = `/${country.toLowerCase()}${url.pathname}`
  return Response.redirect(url)
}

// Feature flags
export const runtime = 'edge'

export async function GET(request: Request) {
  const userId = request.cookies.get('userId')?.value
  const variant = hashUserId(userId) % 2 === 0 ? 'A' : 'B'
  return Response.json({ variant })
}

// Authentication check
export const runtime = 'edge'

export async function POST(request: Request) {
  const token = request.headers.get('Authorization')
  const isValid = await verifyJWT(token) // Edge-compatible JWT
  return Response.json({ authenticated: isValid })
}
```

**When NOT to use Edge:**

```typescript
// ❌ File system access
import fs from 'fs' // Not available in Edge

// ❌ Native Node.js modules
import crypto from 'crypto' // Use Web Crypto API instead

// ❌ Database connections (usually)
import { db } from './db' // Unless using Edge-compatible DB

// ❌ Large computations
// Edge has CPU time limits

// ✓ Use Node.js runtime for these
export const runtime = 'nodejs' // Explicit Node.js
```

**Edge with database:**

```typescript
// Edge-compatible databases work
export const runtime = 'edge'

import { neon } from '@neondatabase/serverless'

export async function GET() {
  const sql = neon(process.env.DATABASE_URL!)
  const users = await sql`SELECT * FROM users LIMIT 10`
  return Response.json(users)
}
```

Reference: [Edge Runtime](https://nextjs.org/docs/app/building-your-application/rendering/edge-and-nodejs-runtimes)
