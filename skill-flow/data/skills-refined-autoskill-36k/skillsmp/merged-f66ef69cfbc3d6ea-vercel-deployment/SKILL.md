---
name: vercel-deployment
description: Use this skill when deploying and optimizing applications on Vercel's edge platform, including Next.js applications, edge functions, and preview deployments.
---

# Vercel Deployment Guide

Comprehensive guide for deploying and optimizing applications on Vercel's edge platform.

## When to Use

- Deploying Next.js, React, Vue, or static sites
- Setting up preview deployments for PRs
- Configuring edge and serverless functions
- Optimizing performance with edge caching
- Managing environment variables and secrets
- Setting up custom domains and SSL

## Core Concepts

### Vercel Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Vercel Edge Network                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Edge Middleware                       │   │
│  │              (Runs at edge, <1ms latency)                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│         ┌────────────────────┼────────────────────┐            │
│         │                    │                    │            │
│         ▼                    ▼                    ▼            │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │   Static    │     │  Serverless │     │    Edge     │      │
│  │   Assets    │     │  Functions  │     │  Functions  │      │
│  │   (CDN)     │     │  (Node.js)  │     │  (V8)       │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Function Types

| Type       | Runtime | Cold Start | Use Case                     |
|------------|---------|------------|-------------------------------|
| Serverless | Node.js | 250ms      | API routes, SSR              |
| Edge       | V8      | <1ms      | Auth, redirects, A/B         |
| Static     | N/A     | 0          | HTML, CSS, JS, images        |

## Project Configuration

### vercel.json

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm ci",
  "devCommand": "npm run dev",
  "regions": ["icn1", "hnd1", "iad1", "sfo1", "cdg1"],
  "functions": {
    "api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 30
    }
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" },
        { "key": "Cache-Control", "value": "s-maxage=60, stale-while-revalidate" }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/old-page",
      "destination": "/new-page",
      "permanent": true
    }
  ]
}
```

### next.config.js (Next.js)

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.example.com',
      },
    ],
    formats: ['image/avif', 'image/webp'],
  },
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on',
          },
        ],
      },
    ];
  },
  async rewrites() {
    return [
      {
        source: '/api/external/:path*',
        destination: `${process.env.API_URL}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
```

## Edge Functions

### Edge Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const country = request.geo?.country;
  if (country === 'KR' && !request.nextUrl.pathname.startsWith('/ko')) {
    return NextResponse.redirect(new URL('/ko', request.url));
  }
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'value');
  return response;
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
```

### Edge API Route

```typescript
// app/api/edge-function/route.ts
import { NextRequest } from 'next/server';

export const runtime = 'edge';
export const preferredRegion = ['icn1', 'hnd1'];

export async function GET(request: NextRequest) {
  const country = request.geo?.country;
  const city = request.geo?.city;

  return Response.json({
    message: `Hello!`,
    location: { country, city },
    timestamp: Date.now(),
  });
}
```

## Incremental Static Regeneration (ISR)

### Time-based Revalidation

```typescript
// src/app/posts/page.tsx
export const revalidate = 60; // Revalidate every 60 seconds

export default async function PostsPage() {
  const posts = await fetchPosts();
  return <PostList posts={posts} />;
}
```

### On-demand Revalidation

```typescript
// src/app/api/revalidate/route.ts
import { revalidateTag, revalidatePath } from 'next/cache';
import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  const { tag, path, secret } = await request.json();
  if (secret !== process.env.REVALIDATION_SECRET) {
    return Response.json({ error: 'Invalid secret' }, { status: 401 });
  }
  if (tag) {
    revalidateTag(tag);
  }
  if (path) {
    revalidatePath(path);
  }
  return Response.json({ revalidated: true, now: Date.now() });
}
```

## Environment Variables

### Configuration

```bash
# .env.local (local development)
DATABASE_URL="postgresql://..."
API_SECRET="secret-key"
NEXT_PUBLIC_APP_URL="http://localhost:3000"

# Production (set in Vercel dashboard)
DATABASE_URL="postgresql://prod..."
API_SECRET="prod-secret"
NEXT_PUBLIC_APP_URL="https://myapp.com"
```

## Deployment

```bash
# CLI commands for deployment
vercel              # Preview deployment
vercel --prod       # Production deployment
```

## Best Practices

- Use Edge Functions for auth/redirects
- Enable ISR for dynamic content
- Configure proper cache headers
- Use `next/image` for images
- Minimize client-side JavaScript
- Set up monitoring (Vercel Analytics)

## Related Skills

| Skill | Purpose |
|-------|---------|
| `jikime-framework-nextjs@14` | Next.js 14 App Router patterns |
| `jikime-platform-vercel-react` | React/Next.js performance optimization rules |

---

Last Updated: 2026-01-23
Version: 2.1.0