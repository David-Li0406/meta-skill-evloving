---
name: fullstory-user-consent-web
version: v3
platform: web
sdk: fullstory-browser
description: JavaScript implementation guide for Fullstory's User Consent APIs. Includes CMP integration, cookie consent banners, GDPR patterns, and comprehensive examples.
parent_skill: fullstory-user-consent
related_skills:
  - fullstory-user-consent
  - fullstory-capture-control
  - fullstory-identify-users
---

# Fullstory User Consent — Web Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for consent models, compliance guidance, and best practices.
>
> **Other Platforms**: See [SKILL-MOBILE.md](./SKILL-MOBILE.md) for iOS, Android, Flutter, React Native.

---

## API Reference

### Holistic Consent (Recommended for GDPR)

```javascript
// BEFORE Fullstory snippet - prevent capture on startup
window['_fs_capture_on_startup'] = false;

// AFTER user consents - start all capture
FS('start');

// If user later revokes consent - stop all capture
FS('shutdown');

// If user consents again
FS('restart');
```

### Element-Level Consent

```javascript
// Enable capture of elements marked "Capture with consent" in FS settings
FS('setIdentity', { consent: true });

// Disable capture of those specific elements
FS('setIdentity', { consent: false });

// Combine with user identification
FS('setIdentity', { 
  uid: 'user_123',
  consent: true,
  properties: { displayName: 'John' }
});
```

### Parameters

| Method | Effect |
|--------|--------|
| `_fs_capture_on_startup = false` | Prevent ALL capture until `FS('start')` |
| `FS('start')` | Begin capture (after delay) |
| `FS('shutdown')` | Stop all capture |
| `FS('restart')` | Resume capture after shutdown |
| `FS('setIdentity', { consent: true })` | Enable element-level consent capture |
| `FS('setIdentity', { consent: false })` | Disable element-level consent capture |

---

## ✅ GOOD Implementation Examples

### Example 1: GDPR Cookie Consent Banner

```javascript
// GOOD: Holistic consent for GDPR/cookie banners
// This approach delays ALL Fullstory capture until consent is given

// STEP 1: In your HTML, BEFORE the Fullstory snippet
// <script>window['_fs_capture_on_startup'] = false;</script>
// <script>/* Fullstory snippet here */</script>

// STEP 2: Your consent manager class
class GDPRConsentManager {
  constructor() {
    this.consentKey = 'fs_consent';
    this.initFromStorage();
  }
  
  initFromStorage() {
    const storedConsent = localStorage.getItem(this.consentKey);
    
    if (storedConsent === 'granted') {
      this.grantConsent();
    }
    // If denied or not set, Fullstory stays disabled
  }
  
  grantConsent() {
    localStorage.setItem(this.consentKey, 'granted');
    
    // Start ALL Fullstory capture
    FS('start');
    
    // If user is logged in, also identify them
    const currentUser = getCurrentUser();
    if (currentUser) {
      FS('setIdentity', {
        uid: currentUser.id,
        properties: {
          displayName: currentUser.name,
          email: currentUser.email
        }
      });
    }
    
    console.log('Fullstory capture started');
  }
  
  revokeConsent() {
    localStorage.setItem(this.consentKey, 'denied');
    
    // Stop ALL Fullstory capture
    FS('shutdown');
    
    console.log('Fullstory capture stopped');
  }
  
  hasConsent() {
    return localStorage.getItem(this.consentKey) === 'granted';
  }
}

// Initialize
const consent = new GDPRConsentManager();

// Wire up to consent banner
document.getElementById('accept-cookies').addEventListener('click', () => {
  consent.grantConsent();
  hideConsentBanner();
});

document.getElementById('decline-cookies').addEventListener('click', () => {
  consent.revokeConsent();
  hideConsentBanner();
});
```

**Why this is good:**
- ✅ Uses `_fs_capture_on_startup = false` to prevent ALL capture until consent
- ✅ Persists consent choice in localStorage
- ✅ Restores consent state on page load
- ✅ Handles logged-in users properly

### Example 2: CMP Integration (OneTrust)

```javascript
// GOOD: Integrate with OneTrust CMP
class OneTrustIntegration {
  static init() {
    // Listen for OneTrust consent changes
    window.OptanonWrapper = function() {
      const consentGroups = OnetrustActiveGroups || '';
      
      // Check if analytics category is consented
      // C0002 is typically the analytics category - verify your setup
      if (consentGroups.includes('C0002')) {
        FS('start');
        OneTrustIntegration.identifyIfLoggedIn();
      } else {
        FS('shutdown');
      }
    };
    
    // Also handle initial state
    if (typeof OnetrustActiveGroups !== 'undefined') {
      window.OptanonWrapper();
    }
  }
  
  static identifyIfLoggedIn() {
    const user = getCurrentUser();
    if (user) {
      FS('setIdentity', {
        uid: user.id,
        properties: { displayName: user.name }
      });
    }
  }
}

// Initialize
OneTrustIntegration.init();
```

### Example 3: CookieBot Integration

```javascript
// GOOD: Integrate with CookieBot CMP
class CookieBotIntegration {
  static init() {
    window.addEventListener('CookiebotOnAccept', () => {
      if (Cookiebot.consent.statistics) {
        FS('start');
        CookieBotIntegration.identifyIfLoggedIn();
      }
    });
    
    window.addEventListener('CookiebotOnDecline', () => {
      FS('shutdown');
    });
    
    // Check initial state
    if (typeof Cookiebot !== 'undefined' && Cookiebot.consent) {
      if (Cookiebot.consent.statistics) {
        FS('start');
        CookieBotIntegration.identifyIfLoggedIn();
      }
    }
  }
  
  static identifyIfLoggedIn() {
    const user = getCurrentUser();
    if (user) {
      FS('setIdentity', {
        uid: user.id,
        properties: { displayName: user.name }
      });
    }
  }
}

// Initialize
CookieBotIntegration.init();
```

### Example 4: React Consent Hook

```jsx
// GOOD: React hook for consent management
import { useState, useEffect, useCallback, createContext, useContext } from 'react';

const ConsentContext = createContext(null);

export function ConsentProvider({ children }) {
  const [consentStatus, setConsentStatus] = useState(() => {
    return localStorage.getItem('analytics_consent');
  });
  
  useEffect(() => {
    // Sync with Fullstory on mount and changes
    if (consentStatus === 'granted') {
      FS('start');
    } else if (consentStatus === 'denied') {
      FS('shutdown');
    }
  }, [consentStatus]);
  
  const grantConsent = useCallback(() => {
    localStorage.setItem('analytics_consent', 'granted');
    setConsentStatus('granted');
  }, []);
  
  const denyConsent = useCallback(() => {
    localStorage.setItem('analytics_consent', 'denied');
    setConsentStatus('denied');
  }, []);
  
  const resetConsent = useCallback(() => {
    localStorage.removeItem('analytics_consent');
    setConsentStatus(null);
  }, []);
  
  return (
    <ConsentContext.Provider value={{
      consentStatus,
      hasConsent: consentStatus === 'granted',
      needsConsent: consentStatus === null,
      grantConsent,
      denyConsent,
      resetConsent
    }}>
      {children}
    </ConsentContext.Provider>
  );
}

export function useConsent() {
  return useContext(ConsentContext);
}

// Consent Banner Component
function ConsentBanner() {
  const { needsConsent, grantConsent, denyConsent } = useConsent();
  
  if (!needsConsent) return null;
  
  return (
    <div className="consent-banner">
      <p>We use session recording to improve your experience.</p>
      <div className="consent-buttons">
        <button onClick={grantConsent}>Accept</button>
        <button onClick={denyConsent}>Decline</button>
      </div>
    </div>
  );
}
```

### Example 5: Consent with User Identification

```javascript
// GOOD: Handle consent and identification together
class FullstoryManager {
  constructor() {
    this.consentGranted = false;
    this.currentUser = null;
  }
  
  onConsentGranted() {
    this.consentGranted = true;
    FS('start');
    
    if (this.currentUser) {
      this.identifyUser(this.currentUser);
    }
  }
  
  onConsentDenied() {
    this.consentGranted = false;
    FS('shutdown');
  }
  
  onUserLogin(user) {
    this.currentUser = user;
    
    if (this.consentGranted) {
      this.identifyUser(user);
    }
  }
  
  onUserLogout() {
    this.currentUser = null;
    
    if (this.consentGranted) {
      FS('setIdentity', { anonymous: true });
    }
  }
  
  identifyUser(user) {
    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        email: user.email,
        plan: user.plan
      }
    });
  }
}

const fsManager = new FullstoryManager();

// Wire up to your auth system
authService.on('login', (user) => fsManager.onUserLogin(user));
authService.on('logout', () => fsManager.onUserLogout());

// Wire up to consent banner
consentBanner.on('accept', () => fsManager.onConsentGranted());
consentBanner.on('decline', () => fsManager.onConsentDenied());
```

---

## ❌ BAD Implementation Examples

### Example 1: Capturing Before Consent

```javascript
// BAD: Capturing without checking consent first
// Fullstory immediately starts capturing when snippet loads
// User hasn't consented yet!

// Later, user clicks "Decline"
FS('setIdentity', { consent: false });  // Too late - already captured data!
```

**CORRECTED:**
```javascript
// GOOD: Configure snippet to wait for consent
window['_fs_capture_on_startup'] = false;

// Then enable capture only after consent
document.getElementById('accept').addEventListener('click', () => {
  FS('start');
});
```

### Example 2: Not Persisting Consent

```javascript
// BAD: Consent not persisted
document.getElementById('accept').addEventListener('click', () => {
  FS('start');
  // Consent not saved! On next page, user is asked again
});
```

**CORRECTED:**
```javascript
// GOOD: Persist and restore consent
document.getElementById('accept').addEventListener('click', () => {
  localStorage.setItem('fs_consent', 'granted');
  FS('start');
});

// On page load
if (localStorage.getItem('fs_consent') === 'granted') {
  FS('start');
}
```

### Example 3: No Way to Withdraw Consent

```javascript
// BAD: Once granted, user can't withdraw consent
consentBanner.on('accept', () => {
  localStorage.setItem('consent', 'granted');
  FS('start');
  // No settings page to change this!
});
```

**CORRECTED:**
```javascript
// GOOD: Provide withdrawal mechanism in settings
function withdrawConsent() {
  localStorage.setItem('consent', 'denied');
  FS('shutdown');
  showConfirmation('Session recording has been disabled.');
}
```

### Example 4: Ignoring CMP Status

```javascript
// BAD: Not respecting CMP decisions
// OneTrust says analytics is declined, but:
FS('start');  // BAD: Overriding CMP decision
```

**CORRECTED:**
```javascript
// GOOD: Respect CMP decisions
window.OptanonWrapper = function() {
  const groups = OnetrustActiveGroups || '';
  
  if (groups.includes('C0002')) {
    FS('start');
  } else {
    FS('shutdown');
  }
};
```

---

## Snippet Configuration

To require consent before capture, configure the Fullstory snippet:

```html
<script>
window['_fs_capture_on_startup'] = false;  // Don't capture until consent
window['_fs_org'] = 'YOUR_ORG_ID';
window['_fs_script'] = 'edge.fullstory.com/s/fs.js';
// ... rest of snippet
</script>
```

Then call `FS('start')` when consent is granted.

---

## Reference Links

- **User Consent**: https://developer.fullstory.com/browser/fullcapture/user-consent/
- **Capture Data**: https://developer.fullstory.com/browser/fullcapture/capture-data/
- **Help Center - Consent Mode**: https://help.fullstory.com/hc/en-us/articles/360020623374
