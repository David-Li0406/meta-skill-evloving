---
name: pwa-development
description: Use this skill when implementing Progressive Web App features for React and Svelte projects, including offline support, service workers, and caching strategies.
---

# PWA Development

Implement Progressive Web App features including service workers, caching strategies, offline support, and installation prompts for React and Svelte applications.

## When to Use This Skill

Use this skill when:
- Adding PWA capabilities to a web app
- Implementing offline support
- Creating service worker caching strategies
- Debugging PWA installation issues
- Handling iOS-specific PWA quirks
- Setting up push notifications

Do NOT use this skill when:
- Building backend APIs
- Working on requirements/design (use those skills first)
- Need complex offline-first architecture (design first)
- Building server-rendered apps without client-side caching needs

## Core Principle

**PWAs fail when offline behavior is an afterthought.** A PWA is not "add service worker to existing app." It's a fundamental architectural decision about data flow, caching, and connectivity failure.

## Diagnostic States

### P0: No PWA Setup

**Symptoms:** No manifest.json, no service worker, online-only

**Interventions:**
- Create manifest
- Add `<link rel="manifest">` to HTML head
- Generate minimal service worker

### P1: Basic Manifest Only

**Symptoms:** Manifest exists but service worker missing, breaks offline

**Key Questions:**
- What content MUST be available offline?
- What should always be fresh (network-first)?

**Interventions:**
- Implement app shell pattern
- Add offline fallback page

### P2: Caching Issues

**Symptoms:** Stale content, unexpected caching behavior

**Interventions:**
- Audit PWA configuration
- Map resources to strategies
- Add cache expiration and cleanup

### P3: Update Problems

**Symptoms:** Users stuck on old versions, multiple refreshes needed

**Interventions:**
- Implement skipWaiting/clients.claim appropriately
- Add update notification UI
- Handle "waiting" state properly

### P4: Offline Data Gaps

**Symptoms:** User actions lost offline, no sync indicator

**Interventions:**
- Implement IndexedDB for offline storage
- Add Background Sync API
- Create sync status UI

### P5: iOS Issues

**Symptoms:** Works on Android, breaks on iOS

**Interventions:**
- Review iOS quirks
- Add apple-mobile-web-app meta tags
- Handle storage eviction gracefully

### P6: Production Ready

**Indicators:** Lighthouse PWA 100, works offline, updates cleanly

## Caching Strategies

| Strategy | Use For | Behavior |
|----------|---------|----------|
| Cache First | Static assets, fonts | Serve from cache, update in background |
| Network First | API data, user content | Try network, fall back to cache |
| Stale While Revalidate | Semi-static content | Serve stale, update cache for next time |
| Network Only | Auth, real-time data | Always network, no caching |

## Available Scripts

| Script | Purpose |
|--------|---------|
| `generate-manifest.ts` | Create manifest.webmanifest |
| `generate-icons.ts` | Generate icon set from source |
| `generate-sw-config.ts` | Create service worker config |
| `audit-pwa.ts` | Validate PWA compliance |

## Common Issues

### Issue: Service Worker Not Updating

**Symptoms**: Old content served after deployment.

**Solution**:
1. Ensure `registerType: 'autoUpdate'` is set
2. Add update prompt component to notify users

### Issue: App Not Installable

**Symptoms**: No install prompt, Lighthouse fails installability.

**Solution**:
1. Verify manifest has all required fields
2. Ensure icons are at least 192x192 and 512x512
3. Serve over HTTPS (or localhost for development)

### Issue: Caching API Responses Causes Stale Data

**Symptoms**: Users see outdated data.

**Solution**:
1. Use `NetworkFirst` strategy for dynamic API endpoints
2. Implement cache versioning with expiration

### Issue: Push Notifications Not Working

**Symptoms**: Subscription succeeds but notifications don't arrive.

**Solution**:
1. Verify VAPID keys match between frontend and backend
2. Check service worker is active

## Additional Resources

### Related Skills

- **requirements-analysis** - Determine offline requirements
- **system-design** - PWA architecture decisions
- **frontend-design** - Design systems and component styling
- **web-search** - Research PWA best practices and browser support