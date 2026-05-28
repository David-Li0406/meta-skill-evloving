---
name: vercel-deployment-management
description: Use this skill for deploying and configuring Next.js applications on Vercel, including serverless functions, environment variables, and debugging deployment issues.
---

# Vercel Deployment Management

Deploy and manage applications on Vercel's edge network, utilizing features like serverless functions, environment variables, and automatic deployments.

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
vercel env add <VARIABLE_NAME>

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

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| API Routes | Serverless functions | `app/api/contact/route.ts` |
| Environment vars | Server-side secrets | `process.env.RESEND_API_KEY` |
| Public env vars | Client-accessible | `NEXT_PUBLIC_GA_MEASUREMENT_ID` |
| Redirects | URL forwarding | `next.config.ts` → `redirects()` |
| Headers | Security headers | `next.config.ts` → `headers()` |

## Resources

- **Vercel Docs**: https://vercel.com/docs
- **Next.js on Vercel**: https://vercel.com/docs/frameworks/nextjs

## Related Skills

For Next.js App Router patterns, see the **nextjs** skill. For email sending with Resend, see the **resend** skill.