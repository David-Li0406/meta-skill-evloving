---
name: vercel-deploy
description: Use this skill to deploy applications to Vercel with edge functions, serverless functions, and Incremental Static Regeneration (ISR).
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
  const country = request.geo?.country || 'US';

  if (country === 'DE') {
    return NextResponse.redirect(new URL('/de', request.url));
  }

  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'my-value');

  return response;
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### 3. Serverless Functions

```typescript
// app/api/users/route.ts - Node.js Runtime (default)
import { NextRequest, NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function GET(request: NextRequest) {
  const users = await db.user.findMany({
    take: 10,
    orderBy: { createdAt: 'desc' },
  });

  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  const user = await db.user.create({
    data: body,
  });

  return NextResponse.json(user, { status: 201 });
}
```

### 4. Incremental Static Regeneration (ISR)

```typescript
// app/posts/[slug]/page.tsx
import { notFound } from 'next/navigation';

export const revalidate = 60;

export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

export default async function PostPage({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);

  if (!post) {
    notFound();
  }

  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  );
}
```

### 5. On-Demand Revalidation

```typescript
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const { secret, path, tag } = await request.json();

  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: 'Invalid secret' }, { status: 401 });
  }

  if (path) {
    revalidatePath(path);
    return NextResponse.json({ revalidated: true, path });
  }

  if (tag) {
    revalidateTag(tag);
    return NextResponse.json({ revalidated: true, tag });
  }

  return NextResponse.json({ error: 'Missing path or tag' }, { status: 400 });
}
```

## Deployment Commands

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Link existing project
vercel link

# Pull environment variables
vercel env pull .env.local

# Set environment variable
vercel env add STRIPE_SECRET_KEY production

# View deployment logs
vercel logs <deployment-url>

# Inspect deployment
vercel inspect <deployment-url>

# Rollback deployment
vercel rollback
```

## Environment Variables

```bash
# .env.local (local development)
DATABASE_URL="postgresql://..."
STRIPE_SECRET_KEY="sk_test_..."
NEXT_PUBLIC_API_URL="http://localhost:3000/api"

# Production (set via CLI or dashboard)
vercel env add DATABASE_URL production
vercel env add STRIPE_SECRET_KEY production preview
```

### Environment Variable Patterns

```typescript
// lib/env.ts - Type-safe environment variables
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  NEXT_PUBLIC_API_URL: z.string().url(),
  NODE_ENV: z.enum(['development', 'production', 'test']),
});

export const env = envSchema.parse(process.env);
```

## Performance Optimization

### 1. Image Optimization

```typescript
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.cloudinary.com',
      },
    ],
    formats: ['image/avif', 'image/webp'],
  },
};

// Usage
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>
```

### 2. Caching Strategies

```typescript
// Fetch with caching
const data = await fetch('https://api.example.com/data', {
  next: {
    revalidate: 3600, // Cache for 1 hour
    tags: ['data'], // Tag for on-demand revalidation
  },
});

// No caching (always fresh)
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store',
});

// Force cache (never refetch)
const data = await fetch('https://api.example.com/data', {
  cache: 'force-cache',
});
```

### 3. Bundle Analysis

```bash
# Install bundle analyzer
npm install @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // your config
});

# Run analysis
ANALYZE=true npm run build
```

## Domain Configuration

```bash
# Add custom domain
vercel domains add example.com

# Add subdomain
vercel domains add api.example.com

# Configure DNS
# Add A record: 76.76.21.21
# Add AAAA record: 2606:4700:3037::ac43:a07b
# Add CNAME for www: cname.vercel-dns.com
```

## Monitoring & Logs

```typescript
// Vercel Analytics
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}

// Speed Insights
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

## Common Issues & Solutions

### Build Errors

```bash
# Clear cache and rebuild
vercel --force

# Check build logs
vercel logs --follow
```

### Environment Variables Not Available

```typescript
// Client-side variables must be prefixed with NEXT_PUBLIC_
// Server-side: DATABASE_URL (only on server)
// Client-side: NEXT_PUBLIC_API_URL (both)
```

### Function Timeout

```typescript
// Increase timeout in vercel.json
{
  "functions": {
    "app/api/slow-operation/route.ts": {
      "maxDuration": 60 // Max 60s on Pro, 300s on Enterprise
    }
  }
}
```

## Source

This skill extends patterns from [Vercel's agent-skills](https://github.com/vercel-labs/agent-skills) and [Vercel documentation](https://vercel.com/docs).