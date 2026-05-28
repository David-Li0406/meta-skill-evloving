---
name: vercel
description: |
  Manages Vercel deployment, edge functions, and serverless hosting configuration for Next.js applications.
  Use when: deploying to Vercel, configuring serverless functions, setting up environment variables, debugging deployment issues, or configuring redirects/rewrites/headers.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Vercel Skill

This project deploys to Vercel with automatic deployments on push to main. The site uses Next.js 15 App Router with serverless API routes for email handling via Resend. Configuration lives in `next.config.ts` (not `vercel.json`) since Next.js handles redirects, rewrites, and headers natively.

## Quick Start

### Deploy to Vercel

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

### Environment Variables

```bash
# Add environment variable via CLI
vercel env add RESEND_API_KEY

# Pull env vars to local .env.local
vercel env pull
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

### API Route (Serverless Function)

**When:** Creating backend endpoints for forms, webhooks, or data processing.

```typescript
// app/api/contact/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    // Validate and process
    return NextResponse.json({ success: true }, { status: 200 })
  } catch (error) {
    console.error('API error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
```

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
  }]
}
```

## See Also

- [patterns](references/patterns.md) - Deployment patterns and configuration
- [workflows](references/workflows.md) - Deployment workflows and debugging

## Related Skills

For Next.js App Router patterns, see the **nextjs** skill. For email sending with Resend, see the **resend** skill.

## Documentation Resources

> Fetch latest Vercel documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "vercel"
2. **Prefer website documentation** (IDs starting with `/websites/`) over source code repositories
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/websites/vercel` _(High reputation, 8716 code snippets)_

**Recommended Queries:**
- "vercel deployment configuration serverless functions"
- "vercel environment variables production preview"
- "vercel build logs troubleshooting errors"