---
name: vercel
description: Use this skill when deploying and configuring Next.js applications on Vercel, including serverless functions, environment variables, and managing deployment settings.
---

# Vercel Deployment Skill

This skill provides guidance on deploying and managing applications on Vercel, particularly for Next.js projects.

## Quick Start

```bash
# Install Vercel CLI
npm i -g vercel

# Link project (first time)
vercel link

# Deploy preview
vercel

# Deploy to production
vercel --prod

# Deploy with build logs visible
vercel deploy --logs
```

## Configuration

### Environment Variables

Add environment variables via the CLI:

```bash
vercel env add RESEND_API_KEY
```

Pull environment variables to local `.env.local`:

```bash
vercel env pull
```

### Vercel Configuration File

You can configure your project using `vercel.json` or `next.config.ts` for Next.js applications. Here’s an example of `vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1", "sfo1"],
  "functions": {
    "api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 30
    }
  },
  "rewrites": [
    { "source": "/api/:path*", "destination": "/api/:path*" },
    { "source": "/:path*", "destination": "/" }
  ],
  "headers": [
    {
      "source": "/api/:path*",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" }
      ]
    }
  ],
  "env": {
    "DATABASE_URL": "@database-url"
  }
}
```

## Serverless Functions

Create serverless functions using API routes in your Next.js application. Here’s an example:

```typescript
// app/api/contact/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    // Validate and process
    return NextResponse.json({ success: true }, { status: 200 });
  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| API Routes | Serverless functions | `app/api/contact/route.ts` |
| Environment vars | Server-side secrets | `process.env.RESEND_API_KEY` |
| Public env vars | Client-accessible | `NEXT_PUBLIC_GA_MEASUREMENT_ID` |
| Redirects | URL forwarding | `next.config.ts` → `redirects()` |
| Headers | Security headers | `next.config.ts` → `headers()` |

## Common Patterns

### Security Headers in next.config.ts

```typescript
async headers() {
  return [{
    source: '/:path*',
    headers: [
      { key: 'X-Frame-Options', value: 'DENY' },
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
    ],
  }];
}
```

## Additional Resources

- Refer to the [Vercel documentation](https://vercel.com/docs) for more detailed information on deployment and configuration options.