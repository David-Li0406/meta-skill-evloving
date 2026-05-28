---
name: fullstory-async-methods
version: v3
description: Core concepts for Fullstory's Asynchronous API methods. Covers the Async suffix pattern, Promise handling, error handling, and when to use async vs fire-and-forget. Note - this pattern is web-only; mobile platforms use different mechanisms.
platforms:
  - web
related_skills:
  - fullstory-observe-callbacks
  - fullstory-identify-users
  - fullstory-analytics-events
  - fullstory-capture-control
implementation_files:
  - SKILL-WEB.md
  - SKILL-MOBILE.md
---

# Fullstory Asynchronous Methods API

> **Implementation Files**: This document covers core concepts. For code examples, see:
> - [SKILL-WEB.md](./SKILL-WEB.md) — JavaScript/TypeScript (Browser)
> - [SKILL-MOBILE.md](./SKILL-MOBILE.md) — Platform differences for iOS, Android, Flutter, React Native

> **Note**: The `Async` suffix pattern is specific to the **web/browser SDK**. Mobile SDKs use different asynchronous mechanisms (completion handlers, delegates, listeners).

## Overview

Fullstory's Browser API provides asynchronous versions of all methods by appending `Async` to the method name. These async methods return Promise-like objects that resolve when Fullstory has started and the action completes. This is essential for:

- **Initialization Waiting**: Wait for Fullstory to fully bootstrap before taking actions
- **Session URL Retrieval**: Get the session replay URL for logging, support tickets, etc.
- **Error Handling**: Know if an API call succeeded or failed
- **Sequential Operations**: Ensure operations complete in order
- **Conditional Logic**: Take action based on Fullstory state

---

## Core Concepts

### Sync vs Async Methods

| Method Type | Returns | Use When |
|-------------|---------|----------|
| `FS('methodName')` | undefined | Fire-and-forget, don't need result |
| `FS('methodNameAsync')` | Promise-like | Need result, error handling, or sequencing |

### Promise-like Object

The object returned from async methods:
- Can be `await`ed
- Supports `.then()` chaining
- **Important**: `.catch()` may not work in older browsers without Promise polyfill
- May reject if Fullstory fails to initialize

### Available Async Methods

Every FS method has an async variant:

| Sync Method | Async Method |
|-------------|--------------|
| `FS('setIdentity', {...})` | `FS('setIdentityAsync', {...})` |
| `FS('setProperties', {...})` | `FS('setPropertiesAsync', {...})` |
| `FS('trackEvent', {...})` | `FS('trackEventAsync', {...})` |
| `FS('getSession')` | `FS('getSessionAsync')` |
| `FS('shutdown')` | `FS('shutdownAsync')` |
| `FS('restart')` | `FS('restartAsync')` |
| `FS('log', {...})` | `FS('logAsync', {...})` |
| `FS('observe', {...})` | `FS('observeAsync', {...})` |

---

## Return Values

| Method | Resolves With |
|--------|---------------|
| `getSessionAsync` | Session URL string |
| `setIdentityAsync` | undefined (completion signal) |
| `setPropertiesAsync` | undefined |
| `trackEventAsync` | undefined |
| `shutdownAsync` | undefined |
| `restartAsync` | undefined |
| `observeAsync` | Observer object with `.disconnect()` |

---

## Rejection Scenarios

The Promise may reject when:
- Malformed or missing configuration (no `_fs_org`)
- User on unsupported browser
- Error in `rec/settings` or `rec/page` calls
- Organization over quota
- Fullstory script blocked by ad blocker (may not reliably reject)

---

## When to Use Async vs Sync

### Use Async When:

| Scenario | Why |
|----------|-----|
| Need session URL | Must wait for URL to be available |
| Error handling needed | Need to know if call failed |
| Sequential operations | Must ensure order of operations |
| Conditional logic | Need result to decide next action |
| Initialization checks | Need to know when FS is ready |

### Use Sync (Fire-and-Forget) When:

| Scenario | Why |
|----------|-----|
| Simple event tracking | Don't need confirmation |
| Non-critical operations | Failure is acceptable |
| Performance critical paths | Don't want to add latency |
| Rapid-fire events | Queueing handles order |
| User-facing actions | Don't delay user experience |

---

## Best Practices

### 1. Always Use Timeouts

```javascript
// Prevent hanging if Fullstory is blocked
const result = await Promise.race([
  FS('getSessionAsync'),
  new Promise((_, reject) => 
    setTimeout(() => reject(new Error('Timeout')), 5000)
  )
]);
```

### 2. Don't Block Critical Paths

```javascript
// BAD: App hangs if FS blocked
await FS('getSessionAsync');
renderApp();

// GOOD: App starts immediately
renderApp();
FS('getSessionAsync').then(url => enrichWithSession(url));
```

### 3. Use try/catch, Not .catch()

```javascript
// GOOD: Works reliably
try {
  const url = await FS('getSessionAsync');
} catch (error) {
  // Handle error
}

// RISKY: .catch() may not work in older browsers
FS('getSessionAsync')
  .then(url => {})
  .catch(err => {});  // May fail silently
```

### 4. Handle Sequencing Correctly

```javascript
// GOOD: Sequential operations
await FS('setIdentityAsync', { uid: user.id });
await FS('trackEventAsync', { name: 'Login' });

// BAD: Race condition
FS('setIdentityAsync', { uid: user.id });
FS('trackEventAsync', { name: 'Login' });  // May fire before identity!
```

---

## Troubleshooting

### Promise Never Resolves

| Cause | Solution |
|-------|----------|
| Fullstory blocked by ad blocker | Use timeout wrapper |
| Script failed to load | Check network tab |
| Network issues | Implement fallback behavior |

### Rejection Errors

| Cause | Solution |
|-------|----------|
| Missing `_fs_org` | Check Fullstory setup |
| Unsupported browser | Verify browser compatibility |
| Over quota | Check Fullstory account |

### .catch() Not Working

| Cause | Solution |
|-------|----------|
| No native Promise | Use async/await with try/catch |
| Promise-like limitations | Use `.then()` with error callback |

---

## Key Takeaways for Agent

When helping developers with Async Methods:

1. **Always emphasize**:
   - Use timeouts to prevent hanging
   - Handle rejections gracefully
   - Don't block critical paths on FS
   - Use try/catch, not .catch()

2. **Common mistakes to watch for**:
   - Blocking app startup on FS
   - Missing error handling
   - Using async when sync would work
   - Race conditions between calls
   - .catch() without polyfill check

3. **Questions to ask developers**:
   - Do you need the result?
   - Is this on a critical path?
   - What should happen if FS fails?
   - Is proper sequencing required?

4. **Platform routing**:
   - Web (JavaScript/TypeScript) → See SKILL-WEB.md
   - Mobile platforms → See SKILL-MOBILE.md for platform-specific patterns

---

## Reference Links

- **Asynchronous Methods**: https://developer.fullstory.com/browser/asynchronous-methods/
- **Get Session Details**: https://developer.fullstory.com/browser/get-session-details/
- **Callbacks and Delegates**: https://developer.fullstory.com/browser/fullcapture/callbacks-and-delegates/
