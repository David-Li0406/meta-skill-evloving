---
name: fullstory-capture-control-web
version: v3
platform: web
sdk: fullstory-browser
description: JavaScript/TypeScript implementation guide for Fullstory's Capture Control APIs (shutdown/restart). Includes API reference, code examples, and common patterns for controlling session capture in web applications.
parent_skill: fullstory-capture-control
related_skills:
  - fullstory-capture-control
  - fullstory-user-consent
  - fullstory-async-methods
---

# Fullstory Capture Control — Web Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for capture control concepts and best practices.
>
> **Other Platforms**: See [SKILL-MOBILE.md](./SKILL-MOBILE.md) for iOS, Android, Flutter, React Native.

---

## API Reference

### Shutdown

```javascript
// Stop capture (sync)
FS('shutdown');

// Async version
await FS('shutdownAsync');
```

### Restart

```javascript
// Resume capture (sync) — starts NEW session
FS('restart');

// Async version
await FS('restartAsync');
```

### Parameters

Both methods take no parameters.

### Return Values

| Method | Sync Return | Async Return |
|--------|-------------|--------------|
| `FS('shutdown')` | undefined | Promise (resolves when stopped) |
| `FS('restart')` | undefined | Promise (resolves when started) |

---

## ✅ GOOD Implementation Examples

### Example 1: Privacy Zone Manager

```javascript
// GOOD: Stop capture in sensitive areas
class PrivacyZoneManager {
  constructor() {
    this.isInPrivacyZone = false;
    this.userBeforeShutdown = null;
  }
  
  async enterPrivacyZone(zoneName) {
    if (this.isInPrivacyZone) return;
    
    // Store current user for re-identification later
    this.userBeforeShutdown = getCurrentUser();
    
    // Track the transition before shutdown
    FS('trackEvent', {
      name: 'Privacy Zone Entered',
      properties: { zone: zoneName }
    });
    
    // Shutdown capture
    await FS('shutdownAsync');
    this.isInPrivacyZone = true;
    
    console.log(`Entered privacy zone: ${zoneName}`);
  }
  
  async exitPrivacyZone(zoneName) {
    if (!this.isInPrivacyZone) return;
    
    // Restart capture
    await FS('restartAsync');
    this.isInPrivacyZone = false;
    
    // Re-identify user
    if (this.userBeforeShutdown) {
      FS('setIdentity', {
        uid: this.userBeforeShutdown.id,
        properties: {
          displayName: this.userBeforeShutdown.name,
          email: this.userBeforeShutdown.email
        }
      });
    }
    
    // Track the transition
    FS('trackEvent', {
      name: 'Privacy Zone Exited',
      properties: { zone: zoneName }
    });
    
    this.userBeforeShutdown = null;
    console.log(`Exited privacy zone: ${zoneName}`);
  }
}

// Usage
const privacyManager = new PrivacyZoneManager();
await privacyManager.enterPrivacyZone('payment-form');
// ... user completes payment ...
await privacyManager.exitPrivacyZone('payment-form');
```

### Example 2: SPA Route-Based Control

```javascript
// GOOD: Control capture based on route
const routeConfig = {
  '/dashboard': { capture: true },
  '/settings/security': { capture: false },
  '/admin': { capture: false },
  '/checkout/payment': { capture: false },
};

class RouteBasedCapture {
  constructor() {
    this.isCapturing = true;
    this.currentUser = null;
    this.setupRouteListener();
  }
  
  setupRouteListener() {
    window.addEventListener('popstate', () => this.handleRouteChange());
    
    const originalPushState = history.pushState;
    history.pushState = (...args) => {
      originalPushState.apply(history, args);
      this.handleRouteChange();
    };
  }
  
  async handleRouteChange() {
    const path = window.location.pathname;
    const config = this.getRouteConfig(path);
    
    if (config.capture && !this.isCapturing) {
      await this.startCapture();
    } else if (!config.capture && this.isCapturing) {
      await this.stopCapture();
    }
  }
  
  getRouteConfig(path) {
    for (const [route, config] of Object.entries(routeConfig)) {
      if (path === route || path.startsWith(route + '/')) {
        return config;
      }
    }
    return { capture: true }; // Default: capture
  }
  
  async startCapture() {
    await FS('restartAsync');
    this.isCapturing = true;
    
    // Re-identify
    this.currentUser = this.currentUser || getCurrentUser();
    if (this.currentUser) {
      FS('setIdentity', {
        uid: this.currentUser.id,
        properties: { displayName: this.currentUser.name }
      });
    }
  }
  
  async stopCapture() {
    this.currentUser = getCurrentUser();
    await FS('shutdownAsync');
    this.isCapturing = false;
  }
}
```

### Example 3: Development Controls

```javascript
// GOOD: Control capture for testing/development
const DevCaptureControls = {
  isOverridden: false,
  
  disableForSession() {
    sessionStorage.setItem('fs_disabled', 'true');
    FS('shutdown');
    this.isOverridden = true;
    console.log('Fullstory disabled for this session');
  },
  
  enableForSession() {
    sessionStorage.removeItem('fs_disabled');
    if (this.isOverridden) {
      FS('restart');
      this.isOverridden = false;
      console.log('Fullstory re-enabled');
    }
  },
  
  init() {
    if (sessionStorage.getItem('fs_disabled') === 'true') {
      FS('shutdown');
      this.isOverridden = true;
    }
    
    // URL param for easy testing
    if (new URLSearchParams(window.location.search).has('no_fullstory')) {
      this.disableForSession();
    }
  },
  
  setupKeyboardShortcut() {
    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.shiftKey && e.key === 'F') {
        this.isOverridden ? this.enableForSession() : this.disableForSession();
      }
    });
  }
};

DevCaptureControls.init();
DevCaptureControls.setupKeyboardShortcut();
```

### Example 4: React Hook

```jsx
// GOOD: React hook for capture control
import { useRef, useCallback, useEffect } from 'react';

function useCaptureControl() {
  const isCapturingRef = useRef(true);
  const userRef = useRef(null);
  
  const setUser = useCallback((user) => {
    userRef.current = user;
  }, []);
  
  const pause = useCallback(async () => {
    if (!isCapturingRef.current) return;
    await FS('shutdownAsync');
    isCapturingRef.current = false;
  }, []);
  
  const resume = useCallback(async () => {
    if (isCapturingRef.current) return;
    await FS('restartAsync');
    isCapturingRef.current = true;
    
    if (userRef.current) {
      FS('setIdentity', {
        uid: userRef.current.id,
        properties: { displayName: userRef.current.name }
      });
    }
  }, []);
  
  useEffect(() => {
    return () => { FS('shutdown'); };
  }, []);
  
  return { pause, resume, setUser };
}

// Privacy zone component
function PrivacyZone({ children }) {
  const { pause, resume } = useCaptureControl();
  
  useEffect(() => {
    pause();
    return () => resume();
  }, [pause, resume]);
  
  return children;
}

// Usage
function PaymentForm() {
  return (
    <PrivacyZone>
      <form>
        <CreditCardInput />
      </form>
    </PrivacyZone>
  );
}
```

---

## ❌ BAD Implementation Examples

### Example 1: Not Re-identifying After Restart

```javascript
// BAD: Forgot to re-identify
async function pauseAndResume() {
  await FS('shutdownAsync');
  // ... do work ...
  await FS('restartAsync');
  // BAD: User is now anonymous!
}
```

**CORRECTED:**
```javascript
async function pauseAndResume() {
  const user = getCurrentUser();
  await FS('shutdownAsync');
  // ... do work ...
  await FS('restartAsync');
  if (user) {
    FS('setIdentity', { uid: user.id, properties: { displayName: user.name } });
  }
}
```

### Example 2: Using Shutdown for Consent

```javascript
// BAD: Using shutdown instead of consent API
function handleConsentDeclined() {
  FS('shutdown');  // Wrong approach!
}
```

**CORRECTED:**
```javascript
// Use consent API for consent
function handleConsentDeclined() {
  FS('setIdentity', { consent: false });
}
```

### Example 3: Async in beforeunload

```javascript
// BAD: Async won't complete before unload
window.addEventListener('beforeunload', async () => {
  await FS('shutdownAsync');  // Won't complete!
});
```

**CORRECTED:**
```javascript
// Use sync version in beforeunload
window.addEventListener('beforeunload', () => {
  FS('shutdown');
});
```

### Example 4: Rapid Shutdown/Restart

```javascript
// BAD: Toggling too rapidly
document.addEventListener('scroll', () => {
  if (isInSensitiveArea()) {
    FS('shutdown');  // Called on every scroll!
  } else {
    FS('restart');   // Creates new session every scroll!
  }
});
```

**CORRECTED:**
```javascript
// Debounced state changes
let isCapturing = true;

const updateCaptureState = debounce(async () => {
  const shouldCapture = !isInSensitiveArea();
  
  if (shouldCapture && !isCapturing) {
    await FS('restartAsync');
    reidentifyUser();
    isCapturing = true;
  } else if (!shouldCapture && isCapturing) {
    await FS('shutdownAsync');
    isCapturing = false;
  }
}, 500);

document.addEventListener('scroll', updateCaptureState);
```

---

## Reference Links

- **Capture Data**: https://developer.fullstory.com/browser/fullcapture/capture-data/
- **Asynchronous Methods**: https://developer.fullstory.com/browser/asynchronous-methods/
