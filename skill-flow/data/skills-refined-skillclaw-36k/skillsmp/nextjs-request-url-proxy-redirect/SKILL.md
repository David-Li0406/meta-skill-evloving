---
name: nextjs-request-url-proxy-redirect
description: |
  Fix for NextResponse.redirect going to wrong host (localhost:8080) on Railway,
  Vercel, or containerized deployments. Use when: (1) redirects work locally but
  go to localhost in production, (2) console shows ERR_CONNECTION_REFUSED to
  localhost:8080 or similar internal URL, (3) using `new URL(path, request.url)`
  for redirects in Next.js API routes or middleware. The fix is to use
  NEXT_PUBLIC_APP_URL environment variable instead of request.url as the base URL.
author: Claude Code
version: 1.0.0
date: 2026-01-21
---

# Next.js request.url Returns Internal Proxy URL on Containerized Platforms

## Problem

When deploying Next.js to Railway, Vercel, or similar containerized platforms,
`request.url` in Edge runtime or API routes can return the internal proxy URL
(e.g., `http://localhost:8080`) instead of the public domain (e.g., `https://example.com`).

This causes `NextResponse.redirect(new URL(path, request.url))` to redirect users
to the internal URL, which fails with `ERR_CONNECTION_REFUSED`.

## Context / Trigger Conditions

- **Symptom**: Browser shows `ERR_CONNECTION_REFUSED` to `localhost:8080` or similar
- **Console errors**: `Failed to fetch RSC payload` followed by connection refused
- **Network tab**: Shows 307 redirect to `https://localhost:8080/...`
- **Environment**: Next.js deployed to Railway, Vercel, Docker, or any reverse proxy setup
- **Code pattern**: Using `new URL('/path', request.url)` for redirects

## Solution

Replace `request.url` with an environment variable for the public URL:

```typescript
// Before (broken on containerized platforms):
return NextResponse.redirect(
  new URL(`/not-found?code=${shortCode}`, request.url)
);

// After (works everywhere):
const baseUrl = process.env.NEXT_PUBLIC_APP_URL || "https://example.com";
return NextResponse.redirect(
  new URL(`/not-found?code=${shortCode}`, baseUrl)
);
```

For reusable code, create a helper:

```typescript
const getBaseUrl = () =>
  process.env.NEXT_PUBLIC_APP_URL || "https://example.com";
```

## Verification

1. Deploy the fix to production
2. Visit a URL that triggers the redirect
3. Verify the redirect goes to the public domain, not localhost
4. Check browser console for absence of `ERR_CONNECTION_REFUSED`

## Example

**File**: `app/[shortCode]/route.ts`

```typescript
// Add helper at module level
const getBaseUrl = () =>
  process.env.NEXT_PUBLIC_APP_URL || "https://clicktowa.com";

export async function GET(request: NextRequest, { params }) {
  const { shortCode } = await params;
  const baseUrl = getBaseUrl();

  // ... lookup logic ...

  if (!link) {
    // Use baseUrl instead of request.url
    return NextResponse.redirect(
      new URL(`/not-found?code=${encodeURIComponent(shortCode)}`, baseUrl)
    );
  }

  // ... rest of handler
}
```

## Notes

- This issue occurs because containerized platforms route traffic through internal
  load balancers/proxies. The `request.url` reflects the internal connection, not
  the original public request.

- Some platforms set headers like `X-Forwarded-Host` or `X-Original-Host`, but
  these aren't automatically used by `request.url`.

- The `NEXT_PUBLIC_` prefix makes the variable available in both client and server
  code, which is appropriate for the public URL.

- Always provide a sensible fallback in case the env var isn't set.

- This also affects `request.headers.get('host')` in some configurations—always
  prefer explicit environment variables for public URLs.

## Related Patterns

- Auth callback URLs should also use `NEXT_PUBLIC_APP_URL`
- OAuth redirect URIs need the public domain
- Sitemap and robots.txt generation should use the env var
- OpenGraph and canonical URLs should use the env var

## References

- [Next.js Environment Variables](https://nextjs.org/docs/app/building-your-application/configuring/environment-variables)
- [Railway Networking](https://docs.railway.app/reference/private-networking)
