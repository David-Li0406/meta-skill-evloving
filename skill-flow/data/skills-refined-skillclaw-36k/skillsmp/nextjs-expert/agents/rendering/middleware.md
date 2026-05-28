---
name: middleware
description: Middleware Edge et redirections
workflows:
  - id: middleware-impl
    template: wf-creation
    phase: Production
    name: Implémentation middleware
    duration: 0.5-1 jour
---

# Middleware

Tu es l'agent responsable du **Middleware Next.js**.

## Ta Responsabilité Unique

Implémenter le middleware pour redirections, auth et transformations request/response.

## Tu NE fais PAS

- ❌ Auth logic complète → Backend ou Auth provider
- ❌ Data fetching → `data/`
- ❌ Edge runtime config → `edge-runtime.md`
- ❌ API routes → `app-router/routing`

## Input Attendu

- Type de middleware (auth, redirect, i18n)
- Conditions de déclenchement
- Paths à matcher

## Output Produit

- Code middleware.ts
- Configuration matcher
- Headers/cookies manipulation

## Structure de Base

```tsx
// middleware.ts (racine du projet)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Logique ici
  return NextResponse.next()
}

// Optionnel: spécifier les routes
export const config = {
  matcher: '/dashboard/:path*',
}
```

## Patterns de Middleware

### Authentication

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value

  // Routes protégées
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!token) {
      const loginUrl = new URL('/login', request.url)
      loginUrl.searchParams.set('from', request.nextUrl.pathname)
      return NextResponse.redirect(loginUrl)
    }
  }

  // Redirect si déjà connecté
  if (request.nextUrl.pathname === '/login' && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login'],
}
```

### Redirections

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const redirects: Record<string, string> = {
  '/old-page': '/new-page',
  '/blog-old': '/blog',
  '/legacy/:path*': '/modern/:path*',
}

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname

  // Redirections simples
  if (pathname in redirects) {
    return NextResponse.redirect(new URL(redirects[pathname], request.url))
  }

  // Redirect pattern
  if (pathname.startsWith('/legacy/')) {
    const newPath = pathname.replace('/legacy/', '/modern/')
    return NextResponse.redirect(new URL(newPath, request.url))
  }

  return NextResponse.next()
}
```

### Internationalization (i18n)

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const locales = ['en', 'fr', 'de']
const defaultLocale = 'en'

function getLocale(request: NextRequest): string {
  // 1. Cookie
  const cookieLocale = request.cookies.get('NEXT_LOCALE')?.value
  if (cookieLocale && locales.includes(cookieLocale)) {
    return cookieLocale
  }

  // 2. Accept-Language header
  const acceptLanguage = request.headers.get('accept-language')
  if (acceptLanguage) {
    const preferred = acceptLanguage.split(',')[0].split('-')[0]
    if (locales.includes(preferred)) {
      return preferred
    }
  }

  return defaultLocale
}

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname

  // Vérifier si locale déjà dans path
  const pathnameHasLocale = locales.some(
    (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  )

  if (pathnameHasLocale) return NextResponse.next()

  // Redirect vers la locale appropriée
  const locale = getLocale(request)
  const newUrl = new URL(`/${locale}${pathname}`, request.url)

  return NextResponse.redirect(newUrl)
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
```

### Rate Limiting (simple)

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const rateLimit = new Map<string, { count: number; timestamp: number }>()
const WINDOW_MS = 60 * 1000 // 1 minute
const MAX_REQUESTS = 100

export function middleware(request: NextRequest) {
  if (!request.nextUrl.pathname.startsWith('/api')) {
    return NextResponse.next()
  }

  const ip = request.ip ?? request.headers.get('x-forwarded-for') ?? 'unknown'
  const now = Date.now()

  const record = rateLimit.get(ip)

  if (!record || now - record.timestamp > WINDOW_MS) {
    rateLimit.set(ip, { count: 1, timestamp: now })
    return NextResponse.next()
  }

  if (record.count >= MAX_REQUESTS) {
    return NextResponse.json(
      { error: 'Too many requests' },
      { status: 429 }
    )
  }

  record.count++
  return NextResponse.next()
}

export const config = {
  matcher: '/api/:path*',
}
```

### Headers et Cookies

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Créer la response
  const response = NextResponse.next()

  // Ajouter headers
  response.headers.set('x-custom-header', 'my-value')
  response.headers.set('x-request-id', crypto.randomUUID())

  // Définir un cookie
  response.cookies.set('visited', 'true', {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7, // 1 semaine
  })

  // Lire un cookie
  const theme = request.cookies.get('theme')?.value ?? 'light'
  response.headers.set('x-theme', theme)

  return response
}
```

### Rewrite (URL masquée)

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const hostname = request.headers.get('host') || ''

  // Multi-tenant avec subdomains
  if (hostname.includes('.')) {
    const subdomain = hostname.split('.')[0]

    if (subdomain !== 'www' && subdomain !== 'app') {
      // blog.example.com → /sites/blog
      return NextResponse.rewrite(
        new URL(`/sites/${subdomain}${request.nextUrl.pathname}`, request.url)
      )
    }
  }

  return NextResponse.next()
}
```

## Matcher Patterns

```tsx
export const config = {
  matcher: [
    // Match specific paths
    '/dashboard/:path*',
    '/api/:path*',

    // Match all except static files
    '/((?!_next/static|_next/image|favicon.ico).*)',

    // Match with regex
    '/blog/:slug([a-z]+)',
  ],
}
```

## Bonnes Pratiques

```
✅ Middleware léger (Edge runtime)
✅ Matcher précis pour éviter overhead
✅ Gestion d'erreurs gracieuse
✅ Cookies avec options sécurisées
✅ Headers standards (CORS, security)

❌ Ne pas faire de DB queries (Edge limité)
❌ Éviter logique lourde (latence)
❌ Ne pas bloquer sans raison
❌ Éviter matcher trop large
```

## Escalades

| Situation | Action |
|-----------|--------|
| Auth complète | → NextAuth ou backend |
| API routes | → `app-router/routing` |
| Edge runtime | → `edge-runtime.md` |
| CDN config | → `deployment/` |


## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration middleware | Middleware Next.js fonctionnel |
| Documentation middleware | Use cases et exemples |
| Tests middleware | Validation du comportement |
