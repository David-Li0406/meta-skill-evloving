---
name: vercel-deployment-management
description: Use this skill for deploying and configuring applications on Vercel, including Next.js apps, serverless functions, and environment variables.
---

# Vercel Deployment Management

Deploy and manage applications on Vercel's edge network, including Next.js applications, serverless functions, and environment variable configurations.

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

### `vercel.json` Example

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
  },
  "crons": [
    {
      "path": "/api/daily-job",
      "schedule": "0 0 * * *"
    }
  ]
}
```

### Environment Variables

```bash
# Add environment variable via CLI
vercel env add DATABASE_URL production

# Pull env vars to local .env.local
vercel env pull
```

## Serverless Functions

### API Route Example

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

## Edge Functions

```typescript
// api/edge.ts
export const config = {
  runtime: 'edge',
};

export default function handler(request: Request) {
  return new Response(JSON.stringify({ message: 'Hello from Edge!' }), {
    headers: { 'content-type': 'application/json' },
  });
}
```

## Security Headers in `next.config.ts`

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

## Resources

- **Vercel Docs**: https://vercel.com/docs
- **Next.js on Vercel**: https://vercel.com/docs/frameworks/nextjs

## Related Skills

For Next.js App Router patterns, see the **nextjs** skill. For email sending with Resend, see the **resend** skill.