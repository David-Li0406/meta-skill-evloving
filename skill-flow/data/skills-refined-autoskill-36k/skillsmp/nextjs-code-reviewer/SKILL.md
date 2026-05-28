---
name: nextjs-code-reviewer
description: Comprehensive code review guidelines for Next.js 15 App Router projects
---

# Next.js Code Review Guidelines

## App Router Structure

### File Organization

**Issues:**
- page.tsx missing in route directory (route won't work)
- layout.tsx not at app root (required)
- Client Component marked with 'use client' unnecessarily
- API route in wrong location (should be in app/api/)
- Special files (loading, error, not-found) in wrong location

**Verify:**
- Root layout.tsx exists and returns `<html>` and `<body>`
- Each route directory has page.tsx for that route
- loading.tsx and error.tsx placed at appropriate levels
- API routes follow app/api/* convention

### Server vs Client

**Critical Issues:**
- 'use client' on component that doesn't need it
- Server Component trying to use hooks
- Client Component doing data fetching (should be Server Component)
- Sensitive data (API keys, secrets) in Client Components

**Verify:**
- Default to Server Components
- 'use client' only for: hooks, event handlers, browser APIs, Context
- Data fetching in Server Components when possible
- Client Components receive data as props

## Data Fetching

### Server Components

**Issues:**
- Using useEffect for data fetching (should be async/await)
- Not handling errors with try-catch
- Fetching inside loops (N+1 problem)
- Not using Promise.all for parallel fetches
- Missing revalidation strategy

**Verify:**
- Async functions for data fetching
- Proper error handling
- Parallel fetching with Promise.all when possible
- Appropriate cache strategy (force-cache, no-store, revalidate)

### Client Components

**Issues:**
- Using fetch in useEffect instead of React Query
- Not handling loading and error states
- Race conditions in useEffect
- Missing error boundaries

**Verify:**
- React Query for client-side data fetching
- Loading, error, and success states all handled
- Proper query key structure
- Error boundaries in place

## Routing

### Dynamic Routes

**Issues:**
- Not validating params before use
- Not handling missing data (404 cases)
- Missing generateStaticParams for static export
- Params not properly typed

**Verify:**
- Params validated and typed correctly
- notFound() called for missing resources
- generateStaticParams implemented for SSG
- Type safety: `{ params: { slug: string } }`

### Navigation

**Issues:**
- Using `<a>` instead of `<Link>`
- Using router.push with full URL (should be relative)
- Not using prefetch for important links
- Client-side navigation for external links

**Verify:**
- `<Link>` component for internal navigation
- Relative paths in navigation
- `prefetch={true}` for critical routes
- `<a>` with `rel="noopener noreferrer"` for external links

## Loading States

### Suspense

**Issues:**
- No loading.tsx at route level
- No fallback for Suspense boundaries
- Loading state only shows after delay (missing instant feedback)
- Suspense boundaries too coarse-grained

**Verify:**
- loading.tsx provides meaningful loading UI
- Suspense boundaries around async components
- Instant loading feedback
- Multiple Suspense boundaries for granular loading

## Error Handling

### Error Boundaries

**Issues:**
- No error.tsx at route level
- Error component not marked 'use client'
- Error messages expose sensitive information
- No retry mechanism in error UI
- Not using error.digest for error tracking

**Verify:**
- error.tsx in place for each route segment
- 'use client' directive on error components
- User-friendly error messages
- Reset function provided to users
- Error logging/tracking implemented

### Not Found

**Issues:**
- 404 errors not handled gracefully
- notFound() not called for missing resources
- Generic 404 page for all routes

**Verify:**
- notFound() called when resource doesn't exist
- Custom not-found.tsx at route level if needed
- Clear messaging about what was not found

## API Routes

### Route Handlers

**Issues:**
- Not validating request body
- Missing error handling
- Not using proper HTTP status codes
- CORS not configured for cross-origin requests
- No rate limiting for public endpoints

**Verify:**
- Request validation with Zod or similar
- Proper error responses with status codes
- NextResponse.json() for responses
- CORS headers if needed
- Authentication checks before sensitive operations

### Security

**Critical Issues:**
- SQL injection vulnerabilities
- No authentication on protected routes
- API keys exposed in client code
- CSRF vulnerabilities in mutations
- No input sanitization

**Verify:**
- Parameterized queries (no string concatenation)
- Authentication middleware on protected routes
- Environment variables for secrets
- CSRF protection for mutations
- Input validation and sanitization

## Server Actions

### Implementation

**Issues:**
- 'use server' directive missing
- Not revalidating cache after mutations
- No error handling
- Not returning serializable data
- Complex logic in server action (should be in service layer)

**Verify:**
- 'use server' at file or function level
- revalidatePath() or revalidateTag() after data changes
- Try-catch with user-friendly error messages
- Returned data is JSON-serializable
- Business logic in separate service functions

## Metadata and SEO

### Metadata

**Issues:**
- No metadata exported
- Missing Open Graph tags
- No Twitter Card metadata
- Dynamic pages missing generateMetadata
- Duplicate titles across pages

**Verify:**
- Metadata object or generateMetadata function present
- Title, description, and OG tags complete
- Dynamic metadata for dynamic routes
- Unique, descriptive titles for each page
- Appropriate meta tags for social sharing

### Images

**Issues:**
- Using `<img>` instead of `<Image>`
- Missing alt text
- Not specifying width and height
- Not using priority for LCP images
- Remote images not configured in next.config.js

**Verify:**
- next/image for all images
- Descriptive alt text (or empty string if decorative)
- Width and height specified (or fill mode)
- priority prop on above-the-fold images
- Remote image domains configured

## Performance

### Bundle Size

**Issues:**
- Heavy libraries imported in Client Components
- No code splitting for large features
- All components in single file
- Not using dynamic imports for heavy components

**Verify:**
- Heavy dependencies in Server Components when possible
- Dynamic imports for large, conditional components
- Components split into separate files
- Bundle analysis done regularly

### Caching

**Issues:**
- No caching strategy defined
- Using no-store for everything (too aggressive)
- Not using revalidation for stale-while-revalidate
- Not leveraging Next.js automatic request deduplication

**Verify:**
- Appropriate cache strategy per request
- force-cache for static data
- revalidate for time-based freshness
- no-store only for user-specific or sensitive data

### Rendering

**Issues:**
- Not using Static Site Generation (SSG) when possible
- Generating all pages at build time (slow builds)
- Not implementing Incremental Static Regeneration (ISR)

**Verify:**
- generateStaticParams for known routes
- ISR (revalidate) for frequently changing content
- On-demand revalidation for critical updates

## TypeScript

### Type Safety

**Issues:**
- Params and searchParams not typed
- API route request/response not typed
- Server action return values not typed
- Using 'any' for Next.js types

**Verify:**
- PageProps interface for params and searchParams
- NextRequest and NextResponse properly typed
- Server actions have return type annotations
- Imported Next.js types used correctly

## Middleware

### Implementation

**Issues:**
- Heavy logic in middleware (runs on every request)
- Not returning NextResponse
- Middleware running on static assets
- No matcher config (runs on all routes)

**Verify:**
- Lightweight logic only (auth checks, redirects)
- NextResponse.next() or redirect returned
- Matcher excludes _next/static and other assets
- Matcher config specific to needed routes

## Internationalization

### next-intl

**Issues:**
- Locale not validated in params
- Messages not loaded for server components
- Hardcoded strings instead of translations
- Missing translations causing runtime errors

**Verify:**
- Locale param validated against supported locales
- getMessages() called in server components
- All user-facing text uses t() function
- Fallback locale configured

## Code Quality

### Best Practices

**Issues:**
- Mixing Server and Client code in same file
- Deep nesting of route groups
- No consistent naming convention
- Component files > 500 lines

**Verify:**
- Clear separation of Server and Client code
- Reasonable route group nesting (< 3 levels)
- Consistent file naming (kebab-case or PascalCase)
- Components split appropriately

## Review Checklist

### Critical

- [ ] Server/Client component separation correct
- [ ] No security vulnerabilities (auth, input validation)
- [ ] Error handling comprehensive
- [ ] Type safety maintained

### High Priority

- [ ] Loading states implemented
- [ ] SEO metadata complete
- [ ] Images optimized
- [ ] Caching strategy appropriate

### Medium Priority

- [ ] Code organization clean
- [ ] No console.logs left in
- [ ] Consistent code style
- [ ] Performance optimizations justified
