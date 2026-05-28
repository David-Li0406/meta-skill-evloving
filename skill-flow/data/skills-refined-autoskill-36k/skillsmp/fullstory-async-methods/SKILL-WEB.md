---
name: fullstory-async-methods-web
version: v3
platform: web
sdk: fullstory-browser
description: JavaScript/TypeScript implementation guide for Fullstory's Asynchronous API methods. Includes API reference, Promise patterns, error handling, and common use cases.
parent_skill: fullstory-async-methods
related_skills:
  - fullstory-async-methods
  - fullstory-observe-callbacks
  - fullstory-identify-users
---

# Fullstory Async Methods — Web Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for when to use async vs sync and best practices.
>
> **Other Platforms**: See [SKILL-MOBILE.md](./SKILL-MOBILE.md) for mobile platform differences.

---

## API Reference

### Basic Syntax

```javascript
// Async/await pattern
const result = await FS('methodNameAsync', params);

// Promise pattern
FS('methodNameAsync', params)
  .then(result => { /* handle result */ });
```

### Available Methods

| Sync Method | Async Method | Returns |
|-------------|--------------|---------|
| `FS('getSession')` | `FS('getSessionAsync')` | Session URL string |
| `FS('setIdentity', {...})` | `FS('setIdentityAsync', {...})` | undefined |
| `FS('setProperties', {...})` | `FS('setPropertiesAsync', {...})` | undefined |
| `FS('trackEvent', {...})` | `FS('trackEventAsync', {...})` | undefined |
| `FS('shutdown')` | `FS('shutdownAsync')` | undefined |
| `FS('restart')` | `FS('restartAsync')` | undefined |
| `FS('log', {...})` | `FS('logAsync', {...})` | undefined |
| `FS('observe', {...})` | `FS('observeAsync', {...})` | Observer object |

---

## ✅ GOOD Implementation Examples

### Example 1: Get Session URL for Support

```javascript
// GOOD: Get session URL for support ticket
async function attachSessionToSupportTicket(ticketId) {
  try {
    const sessionUrl = await FS('getSessionAsync');
    
    // Attach to support ticket
    await updateSupportTicket(ticketId, {
      fullstoryUrl: sessionUrl,
      attachedAt: new Date().toISOString()
    });
    
    console.log('Session attached to ticket:', sessionUrl);
    return sessionUrl;
  } catch (error) {
    console.warn('Could not get Fullstory session:', error);
    // Continue without session URL - non-critical
    return null;
  }
}

// Usage
document.getElementById('help-button').addEventListener('click', async () => {
  const ticket = await createSupportTicket(userIssue);
  await attachSessionToSupportTicket(ticket.id);
  showTicketConfirmation(ticket);
});
```

**Why this is good:**
- ✅ Uses try/catch for error handling
- ✅ Gracefully handles Fullstory being unavailable
- ✅ Non-blocking failure (user can still submit ticket)
- ✅ Returns null on failure for caller to handle

### Example 2: Wait for Fullstory Before Critical Actions

```javascript
// GOOD: Ensure Fullstory is ready before identifying
async function initializeAnalytics(user) {
  try {
    // Wait for Fullstory to be ready
    await FS('setIdentityAsync', {
      uid: user.id,
      properties: {
        displayName: user.name,
        email: user.email
      }
    });
    
    console.log('User identified successfully');
    
    // Now safe to track initial events
    await FS('trackEventAsync', {
      name: 'Session Started',
      properties: {
        entryPage: window.location.pathname,
        referrer: document.referrer
      }
    });
    
    return true;
  } catch (error) {
    console.error('Fullstory initialization failed:', error);
    // Analytics failure shouldn't break the app
    return false;
  }
}

// Usage in app bootstrap
async function bootstrap() {
  const user = await authenticateUser();
  
  // Initialize analytics (don't block on failure)
  initializeAnalytics(user);
  
  // Continue app initialization
  renderApp();
}
```

**Why this is good:**
- ✅ Waits for identification to complete
- ✅ Sequential: identify before tracking events
- ✅ Handles errors gracefully
- ✅ Doesn't block app on analytics failure

### Example 3: Session URL in Error Reports with Timeout

```javascript
// GOOD: Include session URL in error logging with timeout
async function captureError(error, context = {}) {
  let sessionUrl = null;
  
  try {
    // Try to get session URL, but don't let it block error reporting
    sessionUrl = await Promise.race([
      FS('getSessionAsync'),
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Timeout')), 2000)
      )
    ]);
  } catch (e) {
    // Session URL unavailable - continue without it
  }
  
  // Send error to monitoring service
  await errorMonitor.captureException(error, {
    ...context,
    fullstoryUrl: sessionUrl,
    timestamp: new Date().toISOString()
  });
  
  // Also log to Fullstory if available
  if (typeof FS !== 'undefined') {
    FS('log', {
      level: 'error',
      msg: error.message
    });
  }
}

// Usage
window.addEventListener('error', (event) => {
  captureError(event.error, {
    source: 'window.onerror',
    filename: event.filename,
    lineno: event.lineno
  });
});
```

**Why this is good:**
- ✅ Timeout prevents hanging on unresponsive FS
- ✅ Error reporting continues without session URL
- ✅ Enriches error context when available
- ✅ Logs error to Fullstory too

### Example 4: Sequential Operations

```javascript
// GOOD: Ensure proper sequence of FS operations
async function completeCheckout(orderData) {
  try {
    // 1. First, ensure user is identified
    await FS('setIdentityAsync', {
      uid: orderData.userId,
      properties: {
        displayName: orderData.customerName,
        email: orderData.customerEmail
      }
    });
    
    // 2. Update user properties with purchase info
    await FS('setPropertiesAsync', {
      type: 'user',
      properties: {
        lifetimeValue: orderData.customerLTV,
        totalOrders: orderData.customerOrderCount,
        lastOrderAt: new Date().toISOString()
      }
    });
    
    // 3. Track the purchase event
    await FS('trackEventAsync', {
      name: 'Order Completed',
      properties: {
        orderId: orderData.id,
        revenue: orderData.total,
        itemCount: orderData.items.length
      }
    });
    
    // 4. Get session URL for order records
    const sessionUrl = await FS('getSessionAsync');
    
    // 5. Update order with session URL
    await saveOrderSessionUrl(orderData.id, sessionUrl);
    
    console.log('Checkout tracked successfully');
    
  } catch (error) {
    // Log but don't fail checkout
    console.error('Analytics tracking failed:', error);
  }
}
```

**Why this is good:**
- ✅ Operations happen in correct order
- ✅ User identified before properties set
- ✅ Event tracked after user data set
- ✅ Session URL captured at end
- ✅ Errors don't break checkout

### Example 5: Conditional Feature Based on FS Status

```javascript
// GOOD: Enable features only if Fullstory is working
class SessionReplayFeature {
  constructor() {
    this.isAvailable = false;
    this.sessionUrl = null;
  }
  
  async initialize() {
    try {
      // Check if Fullstory is capturing
      this.sessionUrl = await FS('getSessionAsync');
      this.isAvailable = true;
      return true;
    } catch (error) {
      this.isAvailable = false;
      console.info('Session replay feature unavailable:', error.message);
      return false;
    }
  }
  
  getShareableLink() {
    if (!this.isAvailable || !this.sessionUrl) {
      return null;
    }
    return this.sessionUrl;
  }
  
  renderShareButton() {
    if (!this.isAvailable) {
      return null; // Don't show button if FS unavailable
    }
    
    return `<button onclick="copySessionLink()">Share Session</button>`;
  }
}

// Usage
const sessionReplay = new SessionReplayFeature();

async function initializeUI() {
  await sessionReplay.initialize();
  
  if (sessionReplay.isAvailable) {
    showSessionReplayUI();
  }
}
```

**Why this is good:**
- ✅ Graceful degradation when FS unavailable
- ✅ Feature flag based on actual FS status
- ✅ No broken UI if FS blocked
- ✅ Clear availability check

---

## ❌ BAD Implementation Examples

### Example 1: Blocking App on Fullstory

```javascript
// BAD: Blocking application startup on Fullstory
async function startApp() {
  // This will hang if Fullstory is blocked!
  const sessionUrl = await FS('getSessionAsync');
  
  // App never starts if FS fails
  renderApp();
}
```

**Why this is bad:**
- ❌ App hangs if Fullstory blocked by ad blocker
- ❌ Promise may never resolve
- ❌ Critical path depends on non-critical service

**CORRECTED:**

```javascript
// GOOD: Non-blocking initialization
async function startApp() {
  // Start app immediately
  renderApp();
  
  // Initialize analytics separately
  try {
    await Promise.race([
      FS('getSessionAsync'),
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Timeout')), 5000)
      )
    ]);
    enableAnalyticsFeatures();
  } catch (error) {
    console.warn('Fullstory unavailable, continuing without analytics');
  }
}
```

### Example 2: Missing Error Handling

```javascript
// BAD: No error handling for async call
async function trackPurchase(order) {
  const sessionUrl = await FS('getSessionAsync');  // May throw!
  saveSessionToOrder(order.id, sessionUrl);  // Never runs if above fails
  
  await FS('trackEventAsync', {  // Also may throw
    name: 'Purchase',
    properties: { orderId: order.id }
  });
}
```

**Why this is bad:**
- ❌ Unhandled promise rejection
- ❌ Subsequent code won't run on failure
- ❌ No graceful degradation

**CORRECTED:**

```javascript
// GOOD: Proper error handling
async function trackPurchase(order) {
  let sessionUrl = null;
  
  try {
    sessionUrl = await FS('getSessionAsync');
  } catch (error) {
    console.warn('Could not get session URL:', error);
  }
  
  if (sessionUrl) {
    saveSessionToOrder(order.id, sessionUrl);
  }
  
  try {
    await FS('trackEventAsync', {
      name: 'Purchase',
      properties: { 
        orderId: order.id,
        hasSessionUrl: !!sessionUrl
      }
    });
  } catch (error) {
    console.warn('Could not track purchase event:', error);
  }
}
```

### Example 3: Race Condition

```javascript
// BAD: Race condition between identify and track
async function onLogin(user) {
  // These run in parallel - trackEvent may fire before identity!
  FS('setIdentityAsync', { uid: user.id });
  FS('trackEventAsync', { name: 'Login' });
}
```

**Why this is bad:**
- ❌ Event may fire before identity is set
- ❌ Event could be attributed to anonymous user

**CORRECTED:**

```javascript
// GOOD: Sequential with proper awaiting
async function onLogin(user) {
  // First identify
  await FS('setIdentityAsync', { 
    uid: user.id,
    properties: { displayName: user.name }
  });
  
  // Then track event (now properly attributed)
  await FS('trackEventAsync', { 
    name: 'Login',
    properties: { method: 'password' }
  });
}

// OR: For non-critical, use sync versions (they queue properly)
function onLogin(user) {
  FS('setIdentity', { uid: user.id });  // Queued first
  FS('trackEvent', { name: 'Login' });  // Queued second
  // Fullstory processes queue in order
}
```

### Example 4: Unnecessary Async Usage

```javascript
// BAD: Using async when you don't need the result
async function handleButtonClick() {
  // Don't need to await fire-and-forget events
  await FS('trackEventAsync', {
    name: 'Button Clicked',
    properties: { buttonId: 'submit' }
  });
  
  // User waits unnecessarily
  proceedWithAction();
}
```

**Why this is bad:**
- ❌ Adds unnecessary latency to user action
- ❌ User waits for analytics to complete
- ❌ No value from awaiting (result not used)

**CORRECTED:**

```javascript
// GOOD: Fire-and-forget for events
function handleButtonClick() {
  // Don't await - fire and forget
  FS('trackEvent', {
    name: 'Button Clicked',
    properties: { buttonId: 'submit' }
  });
  
  // Proceed immediately
  proceedWithAction();
}
```

---

## Common Patterns

### Pattern 1: Safe Async Wrapper

```javascript
// Wrapper for safe FS async calls with timeout
async function safeFS(method, params, options = {}) {
  const { timeout = 5000, fallback = null } = options;
  
  // Check if FS exists
  if (typeof FS === 'undefined') {
    console.warn(`FS not available for ${method}`);
    return fallback;
  }
  
  try {
    const result = await Promise.race([
      FS(method, params),
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error(`FS ${method} timeout`)), timeout)
      )
    ]);
    return result;
  } catch (error) {
    console.warn(`FS ${method} failed:`, error.message);
    return fallback;
  }
}

// Usage
const sessionUrl = await safeFS('getSessionAsync', undefined, {
  timeout: 3000,
  fallback: null
});

await safeFS('trackEventAsync', {
  name: 'Page View',
  properties: { page: '/home' }
});
```

### Pattern 2: Initialization Status Manager

```javascript
// Track Fullstory initialization status
class FSStatusManager {
  constructor() {
    this.status = 'pending';
    this.sessionUrl = null;
    this.error = null;
    this.callbacks = [];
  }
  
  async initialize() {
    try {
      this.sessionUrl = await FS('getSessionAsync');
      this.status = 'ready';
      this.callbacks.forEach(cb => cb(this.sessionUrl));
    } catch (error) {
      this.status = 'failed';
      this.error = error;
    }
    
    return this.status === 'ready';
  }
  
  onReady(callback) {
    if (this.status === 'ready') {
      callback(this.sessionUrl);
    } else if (this.status === 'pending') {
      this.callbacks.push(callback);
    }
  }
  
  isReady() {
    return this.status === 'ready';
  }
  
  getSessionUrl() {
    return this.sessionUrl;
  }
}

// Global instance
const fsStatus = new FSStatusManager();
fsStatus.initialize();

// Use anywhere
fsStatus.onReady((url) => {
  console.log('FS ready with session:', url);
});
```

### Pattern 3: React Hook

```jsx
import { useState, useEffect, useCallback } from 'react';

function useFullstoryAsync() {
  const [sessionUrl, setSessionUrl] = useState(null);
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    if (typeof FS === 'undefined') {
      setError(new Error('Fullstory not available'));
      return;
    }
    
    let cancelled = false;
    
    async function initialize() {
      try {
        const url = await Promise.race([
          FS('getSessionAsync'),
          new Promise((_, reject) => 
            setTimeout(() => reject(new Error('Timeout')), 10000)
          )
        ]);
        
        if (!cancelled) {
          setSessionUrl(url);
          setIsReady(true);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err);
        }
      }
    }
    
    initialize();
    
    return () => {
      cancelled = true;
    };
  }, []);
  
  const trackEvent = useCallback(async (name, properties) => {
    if (typeof FS === 'undefined') return;
    
    try {
      await FS('trackEventAsync', { name, properties });
    } catch (err) {
      console.warn('Failed to track event:', err);
    }
  }, []);
  
  return { sessionUrl, isReady, error, trackEvent };
}

// Usage
function SupportWidget() {
  const { sessionUrl, isReady } = useFullstoryAsync();
  
  return (
    <button disabled={!isReady}>
      Contact Support
      {sessionUrl && ' (Session attached)'}
    </button>
  );
}
```

---

## Reference Links

- **Asynchronous Methods**: https://developer.fullstory.com/browser/asynchronous-methods/
- **Get Session Details**: https://developer.fullstory.com/browser/get-session-details/
- **Callbacks and Delegates**: https://developer.fullstory.com/browser/fullcapture/callbacks-and-delegates/
