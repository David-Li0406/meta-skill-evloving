# Vercel Patterns Reference

## Contents
- Configuration Patterns
- API Route Patterns
- Environment Variable Patterns
- Anti-Patterns

---

## Configuration Patterns

### Next.js Native Configuration (This Project)

This project uses `next.config.ts` for all routing configuration. Do NOT create a `vercel.json` file—Next.js handles everything.

```typescript
// next.config.ts - This project's actual configuration
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    unoptimized: true,  // Simpler static hosting
    remotePatterns: [{ protocol: 'https', hostname: '**' }],
  },
  
  async rewrites() {
    return [{
      source: '/public/:path*',
      destination: '/:path*',
    }];
  },
  
  async redirects() {
    return [{
      source: '/compare',
      destination: '/resources/compare',
      permanent: true,  // 308 redirect
    }];
  },
  
  async headers() {
    return [{
      source: '/:path*',
      headers: [
        { key: 'X-Frame-Options', value: 'DENY' },
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
      ],
    }];
  },
};

export default nextConfig;
```

### When to Use vercel.json

Only use `vercel.json` for Vercel-specific features not available in Next.js config:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "crons": [{
    "path": "/api/cron",
    "schedule": "0 5 * * *"
  }],
  "functions": {
    "app/api/heavy-task/route.ts": {
      "maxDuration": 60,
      "memory": 1024
    }
  }
}
```

---

## API Route Patterns

### Standard API Route Structure

```typescript
// app/api/contact/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { firstName, lastName, email, message } = body

    // 1. Validate required fields
    if (!firstName || !lastName || !email || !message) {
      return NextResponse.json(
        { error: 'All fields are required' },
        { status: 400 }
      )
    }

    // 2. Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        { error: 'Invalid email format' },
        { status: 400 }
      )
    }

    // 3. Process request (send email, save to DB, etc.)
    const { error } = await resend.emails.send({
      from: 'noreply@xop.ai',
      to: ['matt@xop.ai'],
      subject: `Contact from ${firstName}`,
      html: `<p>${message}</p>`
    })

    if (error) {
      console.error('Resend error:', error)
      return NextResponse.json({ error: 'Failed to send' }, { status: 500 })
    }

    // 4. Log and return success
    console.log('Contact submitted:', { firstName, email, timestamp: new Date().toISOString() })
    return NextResponse.json({ success: true }, { status: 200 })

  } catch (error) {
    console.error('API error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
```

### Dynamic Route Parameters

```typescript
// app/api/pdf/[slug]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ slug: string }> }
) {
  const { slug } = await params  // Must await in Next.js 15
  
  const validSlugs = ['engineer-app-v4', 'teams-chatbot']
  if (!validSlugs.includes(slug)) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 })
  }
  
  // Process valid slug...
}
```

---

## Environment Variable Patterns

### Server vs Client Variables

```typescript
// Server-only (API routes, server components)
process.env.RESEND_API_KEY  // Secret, never exposed

// Client-accessible (requires NEXT_PUBLIC_ prefix)
process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID
```

### Conditional Rendering Based on Env

```typescript
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID && (
          <GoogleAnalytics measurementId={process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID} />
        )}
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

---

## Anti-Patterns

### WARNING: Hardcoded URLs in API Routes

**The Problem:**

```typescript
// BAD - Hardcoded URL breaks in different environments
const downloadUrl = 'https://xopweb.vercel.app/guide.pdf'
```

**Why This Breaks:**
1. Preview deployments get unique URLs (xopweb-abc123.vercel.app)
2. Custom domains differ from Vercel URLs
3. Local development uses localhost

**The Fix:**

```typescript
// GOOD - Use environment variable with fallback
const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://xop.ai'
const downloadUrl = `${baseUrl}/guide.pdf`
```

### WARNING: Missing Error Handling in API Routes

**The Problem:**

```typescript
// BAD - Unhandled errors crash the function
export async function POST(request: NextRequest) {
  const body = await request.json()
  await sendEmail(body)  // If this throws, 500 with no context
  return NextResponse.json({ success: true })
}
```

**Why This Breaks:**
1. Uncaught errors return generic 500s with no debugging info
2. No logging means blind debugging in production
3. Partial failures leave system in unknown state

**The Fix:**

```typescript
// GOOD - Wrap in try/catch, log errors, return appropriate status
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { error } = await sendEmail(body)
    if (error) {
      console.error('Email send failed:', error)
      return NextResponse.json({ error: 'Failed to send' }, { status: 500 })
    }
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('API error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
```

### WARNING: Exposing Secrets via NEXT_PUBLIC_ Prefix

**The Problem:**

```typescript
// BAD - This exposes your API key to the browser!
const resend = new Resend(process.env.NEXT_PUBLIC_RESEND_API_KEY)
```

**Why This Breaks:**
1. `NEXT_PUBLIC_` variables are bundled into client JavaScript
2. Anyone can view source and steal your API keys
3. Attackers can make requests on your behalf

**The Fix:**

```typescript
// GOOD - Keep secrets server-side only
// In API route (server-side):
const resend = new Resend(process.env.RESEND_API_KEY)  // No NEXT_PUBLIC_

// Client calls API route, never touches secret
await fetch('/api/contact', { method: 'POST', body: JSON.stringify(data) })