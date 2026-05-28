---
name: fullstory-anonymize-users-web
version: v3
platform: web
sdk: fullstory-browser
description: JavaScript/TypeScript implementation guide for Fullstory's User Anonymization API. Includes API reference, code examples, and common patterns for logout handling and user switching in web applications.
parent_skill: fullstory-anonymize-users
related_skills:
  - fullstory-anonymize-users
  - fullstory-identify-users
  - fullstory-user-consent
---

# Fullstory Anonymize Users — Web Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for session lifecycle, when to anonymize, and best practices.
>
> **Other Platforms**: See [SKILL-MOBILE.md](./SKILL-MOBILE.md) for iOS, Android, Flutter, React Native.

---

## API Reference

### Basic Syntax

```javascript
FS('setIdentity', { anonymous: true });
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `anonymous` | boolean | **Yes** | Must be `true` to anonymize the user |

### Async Version

For cases where you need confirmation before navigation:

```javascript
await FS('setIdentityAsync', { anonymous: true });
```

### Rate Limits

| Type | Limit |
|------|-------|
| Sustained | 30 calls per page per minute |
| Burst | 10 calls per second |

---

## ✅ GOOD Implementation Examples

### Example 1: Basic Logout Handler

```javascript
// GOOD: Proper logout with Fullstory anonymization
async function handleLogout() {
  try {
    // 1. Call your backend logout endpoint
    await fetch('/api/auth/logout', { method: 'POST' });
    
    // 2. Clear local authentication state
    clearAuthTokens();
    clearUserState();
    
    // 3. Anonymize in Fullstory BEFORE redirecting
    FS('setIdentity', { anonymous: true });
    
    // 4. Redirect to login page
    window.location.href = '/login';
  } catch (error) {
    console.error('Logout failed:', error);
    // Still anonymize even if backend fails
    FS('setIdentity', { anonymous: true });
    window.location.href = '/login';
  }
}
```

**Why this is good:**
- ✅ Anonymizes before redirect
- ✅ Handles errors gracefully
- ✅ Clears local state before anonymizing
- ✅ Ensures next user won't be associated with previous user

### Example 2: React Logout with Auth Context

```jsx
// GOOD: React hook pattern for logout with Fullstory
import { useCallback } from 'react';
import { useAuth } from './auth-context';
import { useNavigate } from 'react-router-dom';

function useLogout() {
  const { clearAuth } = useAuth();
  const navigate = useNavigate();
  
  const logout = useCallback(async () => {
    // Track the logout action before anonymizing
    FS('trackEvent', {
      name: 'User Logged Out',
      properties: {
        logoutMethod: 'manual',
        sessionDuration: getSessionDuration()
      }
    });
    
    // Clear application auth state
    await clearAuth();
    
    // Anonymize the Fullstory session
    FS('setIdentity', { anonymous: true });
    
    // Navigate to home/login
    navigate('/login');
  }, [clearAuth, navigate]);
  
  return logout;
}

// Usage
function LogoutButton() {
  const logout = useLogout();
  return <button onClick={logout}>Sign Out</button>;
}
```

**Why this is good:**
- ✅ Tracks logout event before anonymizing (preserves attribution)
- ✅ Integrated with React ecosystem
- ✅ Reusable across components
- ✅ Clean navigation after logout

### Example 3: Account Switching

```javascript
// GOOD: Clean account switching with proper session boundaries
async function switchAccount(newAccountId) {
  const newUser = await fetchAccountDetails(newAccountId);
  
  // Track the switch event under current user
  FS('trackEvent', {
    name: 'Account Switch Initiated',
    properties: {
      targetAccountId: newAccountId
    }
  });
  
  // Step 1: Anonymize current session
  FS('setIdentity', { anonymous: true });
  
  // Step 2: Set up new account context
  await setupAccountContext(newUser);
  
  // Step 3: Identify as new user
  FS('setIdentity', {
    uid: newUser.id,
    properties: {
      displayName: newUser.name,
      email: newUser.email,
      accountType: newUser.type
    }
  });
  
  // Refresh UI
  window.location.reload();
}
```

**Why this is good:**
- ✅ Tracks event before identity change
- ✅ Cleanly separates sessions between accounts
- ✅ No data contamination between accounts
- ✅ New user gets fresh identification

### Example 4: Session Timeout Handler

```javascript
// GOOD: Handling session timeout with Fullstory
class SessionManager {
  constructor() {
    this.timeoutDuration = 30 * 60 * 1000; // 30 minutes
    this.timeoutId = null;
    this.lastActivity = Date.now();
  }
  
  startTimeout() {
    this.resetTimeout();
    document.addEventListener('click', () => this.resetTimeout());
    document.addEventListener('keypress', () => this.resetTimeout());
  }
  
  resetTimeout() {
    this.lastActivity = Date.now();
    if (this.timeoutId) clearTimeout(this.timeoutId);
    
    this.timeoutId = setTimeout(() => {
      this.handleSessionTimeout();
    }, this.timeoutDuration);
  }
  
  async handleSessionTimeout() {
    // Track timeout event while still identified
    FS('trackEvent', {
      name: 'Session Timeout',
      properties: {
        inactivityDuration: Date.now() - this.lastActivity,
        lastPage: window.location.pathname
      }
    });
    
    // Anonymize the session
    FS('setIdentity', { anonymous: true });
    
    // Clear auth and redirect
    clearAuthState();
    showTimeoutModal();
  }
}
```

**Why this is good:**
- ✅ Tracks timeout before anonymizing
- ✅ Captures useful debugging info
- ✅ Clean session boundary on timeout
- ✅ User feedback via modal

### Example 5: Privacy/Incognito Mode Toggle

```javascript
// GOOD: "Incognito mode" toggle for privacy-conscious users
class PrivacyManager {
  constructor() {
    this.isIncognitoMode = false;
    this.originalUserId = null;
  }
  
  async enableIncognitoMode(currentUserId) {
    // Store original user ID for potential re-identification
    this.originalUserId = currentUserId;
    this.isIncognitoMode = true;
    
    // Track before anonymizing
    FS('trackEvent', {
      name: 'Incognito Mode Enabled',
      properties: {}
    });
    
    // Anonymize - activity won't be linked to user
    FS('setIdentity', { anonymous: true });
    
    // Update UI
    showIncognitoIndicator();
  }
  
  async disableIncognitoMode() {
    if (!this.originalUserId) return;
    
    this.isIncognitoMode = false;
    
    // Re-identify user
    const user = await getCurrentUser();
    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        email: user.email
      }
    });
    
    // Track re-enablement
    FS('trackEvent', {
      name: 'Incognito Mode Disabled',
      properties: {}
    });
    
    hideIncognitoIndicator();
    this.originalUserId = null;
  }
}
```

**Why this is good:**
- ✅ Gives users control over tracking
- ✅ Maintains ability to re-identify
- ✅ Clear user feedback
- ✅ Events tracked at session boundaries

---

## ❌ BAD Implementation Examples

### Example 1: Forgetting to Anonymize on Logout

```javascript
// BAD: No Fullstory anonymization on logout
function handleLogout() {
  clearAuthTokens();
  clearUserState();
  window.location.href = '/login';
  // Missing FS('setIdentity', { anonymous: true })!
}
```

**Why this is bad:**
- ❌ Next user's activity may be attributed to previous user
- ❌ Session continues under wrong identity
- ❌ Data integrity issues in analytics
- ❌ Privacy concern if sharing device

**CORRECTED:**
```javascript
// GOOD: Include Fullstory anonymization
function handleLogout() {
  clearAuthTokens();
  clearUserState();
  
  // Anonymize before redirect
  FS('setIdentity', { anonymous: true });
  
  window.location.href = '/login';
}
```

### Example 2: Anonymizing After Redirect

```javascript
// BAD: Anonymizing after navigation starts
function handleLogout() {
  window.location.href = '/login';
  
  // BAD: This may never execute - page is already navigating!
  FS('setIdentity', { anonymous: true });
}
```

**Why this is bad:**
- ❌ Navigation starts before anonymization
- ❌ FS call may not complete
- ❌ Session may not properly close

**CORRECTED:**
```javascript
// GOOD: Anonymize BEFORE navigation
async function handleLogout() {
  // Anonymize first
  await FS('setIdentityAsync', { anonymous: true });
  
  // Then navigate
  window.location.href = '/login';
}
```

### Example 3: Anonymizing Repeatedly

```javascript
// BAD: Calling anonymize multiple times
function handleLogout() {
  // Excessive calls
  FS('setIdentity', { anonymous: true });
  FS('setIdentity', { anonymous: true });
  FS('setIdentity', { anonymous: true });
  
  window.location.href = '/login';
}
```

**Why this is bad:**
- ❌ Wastes API call quota
- ❌ Creates unnecessary session splits
- ❌ May hit rate limits
- ❌ No benefit from multiple calls

**CORRECTED:**
```javascript
// GOOD: Single anonymization call
function handleLogout() {
  FS('setIdentity', { anonymous: true });
  window.location.href = '/login';
}
```

### Example 4: Using Wrong Parameter

```javascript
// BAD: Wrong ways to anonymize
FS('setIdentity', { uid: null });           // BAD: uid shouldn't be null
FS('setIdentity', { uid: 'anonymous' });    // BAD: This identifies as user "anonymous"!
FS('setIdentity', { uid: '' });             // BAD: Empty string uid
FS('setIdentity', {});                      // BAD: Missing required parameters
```

**Why this is bad:**
- ❌ `uid: null` may cause errors
- ❌ `uid: 'anonymous'` creates an identified user named "anonymous"
- ❌ Empty string uid is invalid
- ❌ Empty object doesn't anonymize

**CORRECTED:**
```javascript
// GOOD: Proper anonymization syntax
FS('setIdentity', { anonymous: true });
```

### Example 5: Missing Event Tracking Before Anonymize

```javascript
// BAD: Missing opportunity to track logout event
function handleLogout() {
  // Just anonymizing without capturing useful data
  FS('setIdentity', { anonymous: true });
  window.location.href = '/login';
}
```

**Why this is bad:**
- ❌ No record of intentional logout vs session timeout
- ❌ Can't analyze logout patterns
- ❌ Loses attribution for the logout event itself

**CORRECTED:**
```javascript
// GOOD: Track event before anonymizing
function handleLogout() {
  // Track while still identified
  FS('trackEvent', {
    name: 'User Logged Out',
    properties: {
      logoutMethod: 'user_initiated',
      pageAtLogout: window.location.pathname
    }
  });
  
  // Then anonymize
  FS('setIdentity', { anonymous: true });
  window.location.href = '/login';
}
```

### Example 6: Using Anonymization to Hide Errors

```javascript
// BAD: Using anonymization to "hide" errors
function handleError(error) {
  // Don't use anonymization to hide error attribution!
  FS('setIdentity', { anonymous: true });
  console.error(error);
}
```

**Why this is bad:**
- ❌ Loses error attribution to user for debugging
- ❌ Makes it harder to help affected users
- ❌ Misuse of anonymization API
- ❌ Creates confusing session boundaries

**CORRECTED:**
```javascript
// GOOD: Log errors while identified, only anonymize on logout
function handleError(error) {
  // Track the error - attribution helps debugging!
  FS('trackEvent', {
    name: 'Application Error',
    properties: {
      errorMessage: error.message,
      errorCode: error.code,
      page: window.location.pathname
    }
  });
  
  // Show error UI without anonymizing
  showErrorMessage(error);
}
```

---

## Common Implementation Patterns

### Pattern 1: Centralized Logout Service

```javascript
// Centralized logout service
class LogoutService {
  static async logout(options = {}) {
    const { 
      trackEvent = true,
      redirectUrl = '/login',
      reason = 'user_initiated'
    } = options;
    
    // Track logout if requested
    if (trackEvent) {
      FS('trackEvent', {
        name: 'User Logged Out',
        properties: {
          reason: reason,
          sessionDuration: getSessionDuration()
        }
      });
    }
    
    // Backend logout
    try {
      await fetch('/api/logout', { method: 'POST' });
    } catch (e) {
      console.warn('Backend logout failed:', e);
    }
    
    // Clear client state
    clearAuthTokens();
    clearUserState();
    clearLocalStorage();
    
    // Anonymize Fullstory
    FS('setIdentity', { anonymous: true });
    
    // Redirect
    if (redirectUrl) {
      window.location.href = redirectUrl;
    }
  }
}

// Usage
await LogoutService.logout();
await LogoutService.logout({ reason: 'session_timeout', redirectUrl: '/timeout' });
```

### Pattern 2: Multi-Tenant Application

```javascript
// For apps with workspace/tenant switching
class TenantManager {
  async switchTenant(newTenantId) {
    const currentUser = getCurrentUser();
    
    // Track switch under current context
    FS('trackEvent', {
      name: 'Tenant Switch',
      properties: {
        fromTenant: currentUser.tenantId,
        toTenant: newTenantId
      }
    });
    
    // Start fresh session for new tenant context
    FS('setIdentity', { anonymous: true });
    
    // Update tenant context
    await loadTenantContext(newTenantId);
    
    // Re-identify with new tenant context
    FS('setIdentity', {
      uid: currentUser.id,
      properties: {
        displayName: currentUser.name,
        email: currentUser.email,
        tenantId: newTenantId,
        tenantName: await getTenantName(newTenantId)
      }
    });
  }
}
```

### Pattern 3: Kiosk/Shared Device Mode

```javascript
// For shared devices like kiosks
class KioskMode {
  sessionTimeout = 5 * 60 * 1000; // 5 minutes
  
  async startSession(user) {
    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        deviceMode: 'kiosk',
        locationId: getKioskLocation()
      }
    });
    
    // Auto-logout after timeout
    setTimeout(() => this.endSession(), this.sessionTimeout);
  }
  
  async endSession() {
    FS('trackEvent', {
      name: 'Kiosk Session Ended',
      properties: {
        endReason: 'timeout',
        location: getKioskLocation()
      }
    });
    
    FS('setIdentity', { anonymous: true });
    
    // Reset to welcome screen
    showWelcomeScreen();
  }
}
```

### Pattern 4: TypeScript Types

```typescript
// Type definitions for anonymization
interface AnonymizePayload {
  anonymous: true;
}

interface IdentifyPayload {
  uid: string;
  properties?: Record<string, unknown>;
}

type SetIdentityPayload = AnonymizePayload | IdentifyPayload;

// Type-safe logout function
async function logout(): Promise<void> {
  const payload: AnonymizePayload = { anonymous: true };
  await FS('setIdentityAsync', payload);
}
```

---

## Framework Integration

### React

```jsx
// Custom hook for logout with Fullstory
import { useCallback } from 'react';

export function useFullstoryLogout() {
  return useCallback(async (reason = 'user_initiated') => {
    FS('trackEvent', {
      name: 'User Logged Out',
      properties: { reason }
    });
    
    await FS('setIdentityAsync', { anonymous: true });
  }, []);
}
```

### Vue

```javascript
// Composable for Vue 3
import { inject } from 'vue';

export function useLogout() {
  const router = useRouter();
  
  async function logout(reason = 'user_initiated') {
    FS('trackEvent', {
      name: 'User Logged Out',
      properties: { reason }
    });
    
    FS('setIdentity', { anonymous: true });
    
    await router.push('/login');
  }
  
  return { logout };
}
```

### Angular

```typescript
// Service for Angular
@Injectable({ providedIn: 'root' })
export class AuthService {
  constructor(private router: Router) {}
  
  async logout(reason: string = 'user_initiated'): Promise<void> {
    FS('trackEvent', {
      name: 'User Logged Out',
      properties: { reason }
    });
    
    FS('setIdentity', { anonymous: true });
    
    await this.router.navigate(['/login']);
  }
}
```

---

## Reference Links

- **Anonymize Users**: https://developer.fullstory.com/browser/identification/anonymize-users/
- **Identify Users**: https://developer.fullstory.com/browser/identification/identify-users/
- **Async Methods**: https://developer.fullstory.com/browser/methods/async-methods/
- **Help Center**: https://help.fullstory.com/hc/en-us/articles/360020623514-Anonymizing-Users
