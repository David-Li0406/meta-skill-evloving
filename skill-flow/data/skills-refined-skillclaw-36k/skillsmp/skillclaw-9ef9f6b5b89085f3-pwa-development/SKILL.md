---
name: pwa-development
description: Use this skill when you need to implement Progressive Web App features in React or Svelte projects, such as adding offline support, creating service workers, or optimizing caching strategies.
---

# PWA Development

Implement Progressive Web App features including service workers, caching strategies, offline support, and installation prompts for React and Svelte applications.

## When to Use This Skill

Use this skill when:
- Creating a new PWA or converting an existing app to a PWA
- Adding offline capabilities to a web application
- Implementing install prompts and app-like experiences
- Setting up push notifications
- Debugging PWA installation issues
- Handling iOS-specific PWA quirks

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
- Create a manifest file and add `<link rel="manifest">` to HTML head.
- Generate a minimal service worker.

### P1: Basic Manifest Only

**Symptoms:** Manifest exists but service worker is missing, breaks offline

**Key Questions:**
- What content MUST be available offline?
- What should always be fresh (network-first)?

**Interventions:**
- Implement app shell pattern and add offline fallback page.

### P2: Caching Issues

**Symptoms:** Stale content, unexpected caching behavior

**Interventions:**
- Audit caching strategies and map resources accordingly.
- Add cache expiration and cleanup.

### P3: Update Problems

**Symptoms:** Users stuck on old versions, multiple refreshes needed

**Interventions:**
- Implement skipWaiting/clients.claim appropriately.
- Add update notification UI and handle "waiting" state properly.

### P4: Offline Data Gaps

**Symptoms:** User actions lost offline, no sync indicator

**Interventions:**
- Ensure proper synchronization of user actions when connectivity is restored.