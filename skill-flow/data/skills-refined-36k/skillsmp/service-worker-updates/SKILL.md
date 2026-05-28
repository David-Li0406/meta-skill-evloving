---
name: service-worker-updates
description: Guide for modifying service worker caching. Edit sw-template.js (not sw.js), run yarn prebuild after changes.
---

# Service Worker Updates Skill

## Purpose

Guide for modifying the service worker caching strategy. Prevent common mistakes that break offline functionality.

## ⚠️ CRITICAL: Never Edit public/sw.js Directly

The `public/sw.js` file is **generated** and will be **overwritten**.

**Always edit**: `public/sw-template.js`

## How Service Worker Generation Works

```text
public/sw-template.js  →  scripts/generate-sw.mjs  →  public/sw.js
       (source)              (build script)           (generated)
```

The build script:

1. Reads `sw-template.js`
2. Replaces `{{API_ORIGIN}}` placeholder with `NEXT_PUBLIC_API_URL` origin
3. Writes output to `public/sw.js`

## When to Run Regeneration

Run `yarn prebuild` after changing `sw-template.js`:

```bash
# After editing sw-template.js
yarn prebuild

# Or just run dev (includes prebuild)
yarn dev
```

**Note**: `yarn build` alone does NOT run prebuild. Environment-specific builds (`build:development|staging|production`) do include it.

## Service Worker Template Structure

```javascript
// public/sw-template.js
const API_ORIGIN = "{{API_ORIGIN}}"; // Replaced at build time

// Workbox 7 configuration
importScripts(
  "https://storage.googleapis.com/workbox-cdn/releases/7.0.0/workbox-sw.js"
);

const { registerRoute } = workbox.routing;
const { CacheFirst, NetworkFirst, StaleWhileRevalidate } = workbox.strategies;

// Cache strategies for different routes
registerRoute(
  ({ url }) => url.origin === API_ORIGIN && url.pathname.startsWith("/api/"),
  new NetworkFirst({ cacheName: "api-cache" })
);
```

## Caching Strategies

| Strategy               | Use Case                | Example        |
| ---------------------- | ----------------------- | -------------- |
| `CacheFirst`           | Static assets, images   | Fonts, icons   |
| `NetworkFirst`         | API calls, dynamic data | Events, news   |
| `StaleWhileRevalidate` | Balance freshness/speed | Category lists |

## Adding New Cache Rules

### 1. Edit Template

```javascript
// public/sw-template.js

// Add new route
registerRoute(
  ({ url }) => url.pathname.startsWith("/new-feature/"),
  new StaleWhileRevalidate({
    cacheName: "new-feature-cache",
    matchOptions: { ignoreVary: true }, // REQUIRED for Next.js App Router
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 24 * 60 * 60, // 24 hours
      }),
    ],
  })
);
```

### 2. Regenerate

```bash
yarn prebuild
```

### 3. Test

```bash
yarn dev
# Check DevTools > Application > Service Workers
```

## Common Patterns

### Cache API Responses

```javascript
registerRoute(
  ({ url }) => url.origin === API_ORIGIN && url.pathname.includes("/events"),
  new NetworkFirst({
    cacheName: "events-cache",
    networkTimeoutSeconds: 3,
    matchOptions: { ignoreVary: true }, // REQUIRED for Next.js App Router
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 100,
        maxAgeSeconds: 60 * 60, // 1 hour
      }),
    ],
  })
);
```

### Cache Static Assets

```javascript
registerRoute(
  ({ request }) => request.destination === "image",
  new CacheFirst({
    cacheName: "images-cache",
    matchOptions: { ignoreVary: true }, // REQUIRED for Next.js App Router
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
      }),
    ],
  })
);
```

### Offline Fallback

```javascript
// Offline page fallback
workbox.routing.setCatchHandler(async ({ event }) => {
  if (event.request.destination === "document") {
    return caches.match("/offline");
  }
  return Response.error();
});
```

## Environment Variable

The `{{API_ORIGIN}}` placeholder is replaced with the origin from `NEXT_PUBLIC_API_URL`:

```bash
# .env
NEXT_PUBLIC_API_URL=https://api.example.com/v1

# Results in sw.js:
const API_ORIGIN = "https://api.example.com";
```

## Debugging Service Worker

1. **Chrome DevTools** > Application > Service Workers
2. Check "Update on reload" during development
3. Use "Bypass for network" to test without caching
4. Clear storage if seeing stale behavior

## ⚠️ CRITICAL: Always Use `ignoreVary: true`

Next.js App Router adds `Vary` headers (`rsc`, `next-router-state-tree`, `next-router-prefetch`, etc.) to responses. Without `ignoreVary: true`, **service worker cache matching** fails because these headers differ between request types (RSC navigation vs client fetch vs direct load).

**Note**: This addresses Workbox service worker cache matching, not the underlying Next.js dynamic route issue (which relates to `Cache-Control: private/no-store` when Server Components call `headers()` or `cookies()`). The `ignoreVary: true` option allows the SW to treat the same URL as one cache entry regardless of Vary header differences.

**Always add `matchOptions` with `ignoreVary: true`:**

```javascript
new workbox.strategies.StaleWhileRevalidate({
  cacheName: "my-cache",
  matchOptions: {
    ignoreVary: true, // REQUIRED for Next.js App Router compatibility
  },
  plugins: [
    /* ... */
  ],
});
```

**Without this**, the same URL may be fetched multiple times and cached as separate entries, causing:

- Wasted bandwidth
- Slower navigation (false cache misses)
- Unreliable offline behavior

## Common Mistakes

1. **Editing sw.js directly** → Changes lost on rebuild
2. **Forgetting yarn prebuild** → Template changes not applied
3. **Wrong API_ORIGIN** → Cache rules don't match
4. **Too aggressive caching** → Users see stale data
5. **No cache expiration** → Cache grows forever
6. **Missing `ignoreVary: true`** → Cache misses due to Next.js `Vary` headers

## Checklist for SW Changes

- [ ] Editing `sw-template.js` (not `sw.js`)?
- [ ] Running `yarn prebuild` after changes?
- [ ] Using appropriate cache strategy?
- [ ] Setting cache expiration limits?
- [ ] Adding `matchOptions: { ignoreVary: true }` to strategies?
- [ ] Testing in DevTools > Application?
- [ ] Testing offline behavior?

## Files to Reference

- [public/sw-template.js](public/sw-template.js) - Source template (EDIT THIS)
- [public/sw.js](public/sw.js) - Generated output (DO NOT EDIT)
- [scripts/generate-sw.mjs](scripts/generate-sw.mjs) - Build script
- [app/offline/page.tsx](app/offline/page.tsx) - Offline fallback page
