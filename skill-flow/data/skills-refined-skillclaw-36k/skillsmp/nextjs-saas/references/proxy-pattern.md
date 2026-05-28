# The Proxy Pattern

## Overview

The proxy pattern provides a unified authentication layer that handles API routes and UI routes differently:

- **API routes**: Return 401 JSON responses (never redirect)
- **UI routes**: Redirect to login page when unauthenticated

This separation is critical because API consumers (mobile apps, webhooks, external services) expect proper HTTP status codes, not HTML redirects.

## Architecture

```
Request
    │
    ▼
┌─────────────────┐
│    proxy.ts     │
│  (entry point)  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐  ┌──────────────┐
│ /api/* │  │ UI routes    │
└───┬────┘  └──────┬───────┘
    │              │
    ▼              ▼
┌────────────┐  ┌────────────────┐
│ apiAuth.ts │  │ middleware.ts  │
│ (401 JSON) │  │ (redirect)     │
└────────────┘  └────────────────┘
```

## Implementation

### proxy.ts (Entry Point)

```typescript
// proxy.ts
import { type NextRequest, NextResponse } from 'next/server'
import { updateSession } from '@/utils/supabase/middleware'
import { handleApiAuth } from '@/utils/supabase/apiAuth'

// Routes that don't require authentication
const PUBLIC_API_ROUTES = [
  '/api/health',
  '/api/auth/callback',
  '/api/webhooks/stripe',
  '/api/webhooks/replicate',
]

export async function proxy(request: NextRequest) {
  const pathname = request.nextUrl.pathname

  // Handle API routes - never redirect, return proper status codes
  if (pathname.startsWith('/api/')) {
    // Skip auth for public/webhook routes
    if (PUBLIC_API_ROUTES.some(route => pathname.startsWith(route))) {
      return NextResponse.next()
    }

    // Authenticate API requests
    return handleApiAuth(request)
  }

  // Handle UI routes - may redirect to login
  return await updateSession(request)
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization)
     * - favicon.ico
     * - Static assets (images, videos, fonts, etc)
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|mp4|webm|woff|woff2|ttf|otf|ico)$).*)',
  ],
}
```

### apiAuth.ts (API Route Handler)

```typescript
// utils/supabase/apiAuth.ts
import { NextRequest, NextResponse } from 'next/server'
import { createServerClient } from '@supabase/ssr'

/**
 * Handles authentication for API routes
 * Returns 401 JSON for unauthorized requests (never redirects)
 * Injects user info headers for downstream handlers
 */
export async function handleApiAuth(request: NextRequest) {
  const response = NextResponse.next()

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => {
            response.cookies.set(name, value, options)
          })
        },
      },
    }
  )

  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    // Return 401 JSON - API consumers expect this
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }

  // Inject user info for downstream route handlers
  response.headers.set('X-User-Id', user.id)
  response.headers.set('X-User-Email', user.email || '')

  return response
}
```

### middleware.ts (UI Route Handler)

```typescript
// utils/supabase/middleware.ts
import { createServerClient } from '@supabase/ssr'
import { type NextRequest, NextResponse } from 'next/server'

/**
 * Handles session refresh and auth redirects for UI routes
 * Redirects to login if unauthenticated
 */
export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          )
          supabaseResponse = NextResponse.next({
            request,
          })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  // IMPORTANT: Don't add logic between createServerClient and getUser()
  const { data: { user } } = await supabase.auth.getUser()

  // Public routes that don't require auth
  const publicRoutes = ['/login', '/auth', '/error', '/pricing', '/about']
  const isPublicRoute = publicRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  )

  if (!user && !isPublicRoute) {
    // Redirect to login for UI routes
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    return NextResponse.redirect(url)
  }

  return supabaseResponse
}
```

## Using Injected Headers in API Routes

The proxy injects `X-User-Id` and `X-User-Email` headers for authenticated requests:

```typescript
// app/api/projects/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/utils/supabase/server'

export async function GET(request: NextRequest) {
  // User info injected by proxy
  const userId = request.headers.get('X-User-Id')

  if (!userId) {
    // Shouldn't happen if proxy is configured correctly
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const supabase = await createClient()
  const { data, error } = await supabase
    .from('projects')
    .select('*')
    .eq('user_id', userId)

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json(data)
}
```

## Adding Public Routes

To add a new public API route (no auth required):

```typescript
// proxy.ts
const PUBLIC_API_ROUTES = [
  '/api/health',
  '/api/auth/callback',
  '/api/webhooks/stripe',
  '/api/webhooks/replicate',
  '/api/public/pricing',      // Add new public route
]
```

## Webhook Security

For webhook routes, validate using webhook signatures instead of session auth:

```typescript
// app/api/webhooks/stripe/route.ts
import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(request: NextRequest) {
  const body = await request.text()
  const signature = request.headers.get('stripe-signature')!

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    return NextResponse.json(
      { error: 'Invalid signature' },
      { status: 400 }
    )
  }

  // Handle webhook event...

  return NextResponse.json({ received: true })
}
```

## Why This Pattern?

### Problem: Unified Middleware Breaks API Consumers

A common mistake is using a single middleware that redirects all unauthenticated requests:

```typescript
// BAD: Redirects API requests
if (!user) {
  return NextResponse.redirect('/login')
}
```

This breaks:
- Mobile apps expecting JSON responses
- Webhook integrations
- External API consumers
- Frontend fetch calls (get HTML instead of JSON error)

### Solution: Route-Aware Authentication

The proxy pattern routes requests to appropriate handlers:

| Route Type | Unauthenticated Response |
|------------|--------------------------|
| `/api/*` | `401 { error: "Unauthorized" }` |
| UI routes | Redirect to `/login` |
| Public API | Pass through |
| Webhooks | Pass through (validate signature separately) |

## Testing the Proxy

```bash
# Test API auth - should return 401 JSON
curl -i http://localhost:3000/api/projects
# HTTP/1.1 401 Unauthorized
# {"error":"Unauthorized"}

# Test UI auth - should redirect
curl -i http://localhost:3000/dashboard
# HTTP/1.1 307 Temporary Redirect
# Location: /login

# Test public route - should pass through
curl -i http://localhost:3000/api/health
# HTTP/1.1 200 OK
```
