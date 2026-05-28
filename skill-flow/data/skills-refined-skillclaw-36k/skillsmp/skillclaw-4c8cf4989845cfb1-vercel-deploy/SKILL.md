---
name: vercel-deploy
description: Use this skill when you need to deploy applications to Vercel, utilizing edge functions, serverless capabilities, and Incremental Static Regeneration (ISR).
---

# Vercel Deploy

Deploy applications to Vercel with edge functions, serverless functions, ISR, and optimal configuration for performance.

## When to Use

- Deploying Next.js applications
- Setting up edge functions for low-latency responses
- Configuring ISR (Incremental Static Regeneration)
- Serverless API deployments
- Setting up preview deployments
- Configuring custom domains and environment variables

## Core Concepts

### 1. Project Configuration (vercel.json)

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "regions": ["iad1", "sfo1"],
  "functions": {
    "app/api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 30
    }
  },
  "crons": [
    {
      "path": "/api/cron/daily-cleanup",
      "schedule": "0 0 * * *"
    }
  ],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" },
        { "key": "Cache-Control", "value": "s-maxage=60, stale-while-revalidate" }
      ]
    }
  ],
  "rewrites": [
    { "source": "/blog/:slug", "destination": "/posts/:slug" }
  ],
  "redirects": [
    { "source": "/old-page", "destination": "/new-page", "permanent": true }
  ]
}
```

### 2. Edge Functions

```typescript
// app/api/hello/route.ts - Edge Runtime
export const runtime = 'edge';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const name = searchParams.get('name') || 'World';

  return new Response(JSON.stringify({ message: `Hello, ${name}!` }), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=300',
    },
  });
}

// Middleware (always runs on edge)
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Geo-based routing
  const country = request.geo?.country || 'US';

  if (country === 'DE') {
    return NextResponse.redirect(new URL('/de', request.url));
  }

  // Add custom headers
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'my-value');

  return response;
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/imag']
}
```