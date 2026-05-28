---
name: fullstory-identify-users-web
version: v3
platform: web
sdk: fullstory-browser
description: JavaScript/TypeScript implementation guide for Fullstory's User Identification API. Includes API reference, code examples, and common patterns for web applications.
parent_skill: fullstory-identify-users
related_skills:
  - fullstory-identify-users
  - fullstory-anonymize-users
  - fullstory-user-properties
---

# Fullstory Identify Users — Web Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for identity linking, cookie behavior, and best practices.
>
> **Other Platforms**: See [SKILL-MOBILE.md](./SKILL-MOBILE.md) for iOS, Android, Flutter, React Native.

---

## API Reference

### Basic Syntax

```javascript
FS('setIdentity', {
  uid: string,           // Required: Your unique user identifier
  properties?: object,   // Optional: Additional user properties
  schema?: object        // Optional: Type inference for properties
});
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `uid` | string | **Yes** | A unique identifier for the user from your system. Must be stable and unique. Maximum 256 characters. |
| `properties` | object | No | Key/value pairs of additional user information |
| `schema` | object | No | Type hints for property values |

### Async Version

```javascript
try {
  await FS('setIdentityAsync', {
    uid: user.id,
    properties: { displayName: user.name }
  });
  console.log('Identity set successfully');
} catch (error) {
  console.error('Identity failed:', error);
}
```

### Anonymize (Logout)

```javascript
FS('setIdentity', { anonymous: true });
```

---

## ✅ GOOD Implementation Examples

### Example 1: Basic Login Identification

```javascript
// GOOD: Call setIdentity immediately after successful login
async function handleLogin(credentials) {
  try {
    const response = await authenticateUser(credentials);
    const user = response.user;
    
    // Identify user in Fullstory right after successful auth
    FS('setIdentity', {
      uid: user.id,  // Use stable database ID, not email
      properties: {
        displayName: user.fullName,
        email: user.email,
        accountType: user.plan,
        signupDate: user.createdAt  // ISO8601 format
      }
    });
    
    // Continue with login flow
    redirectToDashboard();
  } catch (error) {
    handleLoginError(error);
  }
}
```

**Why this is good:**
- ✅ Uses stable database ID as uid, not PII
- ✅ Called immediately after successful authentication
- ✅ Includes displayName for easy identification in Fullstory
- ✅ Includes email for searchability
- ✅ Adds business-relevant properties (accountType, signupDate)

### Example 2: Page Load with Existing Session (SPA/SSR)

```javascript
// GOOD: Check authentication state and identify on every page load
function initializeFullstory() {
  const currentUser = getCurrentAuthenticatedUser();
  
  if (currentUser && currentUser.id) {
    // User is logged in - identify them
    FS('setIdentity', {
      uid: currentUser.id,
      properties: {
        displayName: currentUser.name,
        email: currentUser.email,
        role: currentUser.role,
        companyId: currentUser.organizationId,
        plan: currentUser.subscription.plan,
        trialEndsAt: currentUser.subscription.trialEnd
      }
    });
  }
  // If not logged in, user remains anonymous (default state)
}

// Call on app initialization
document.addEventListener('DOMContentLoaded', initializeFullstory);
```

**Why this is good:**
- ✅ Handles both authenticated and anonymous states
- ✅ Calls on every page load to ensure identification survives navigation
- ✅ Includes organization context for B2B analytics
- ✅ Captures subscription data for segment analysis

### Example 3: React/Next.js Integration

```jsx
// GOOD: React hook for Fullstory identification
import { useEffect } from 'react';
import { useAuth } from './auth-context';

function useFullstoryIdentity() {
  const { user, isAuthenticated, isLoading } = useAuth();
  
  useEffect(() => {
    // Wait for auth state to be determined
    if (isLoading) return;
    
    if (isAuthenticated && user) {
      FS('setIdentity', {
        uid: user.id,
        properties: {
          displayName: `${user.firstName} ${user.lastName}`,
          email: user.email,
          role: user.role,
          teamSize: user.team?.memberCount,
          features: user.enabledFeatures,  // Array of strings
          lastLoginAt: new Date().toISOString()
        }
      });
    }
  }, [user, isAuthenticated, isLoading]);
}

// Usage in App component
function App() {
  useFullstoryIdentity();
  
  return <AppContent />;
}
```

**Why this is good:**
- ✅ Waits for auth state to stabilize before identifying
- ✅ Re-runs when user state changes
- ✅ Handles loading states properly
- ✅ Captures feature flags for segmentation
- ✅ Updates lastLoginAt for recency tracking

### Example 4: OAuth/SSO Callback Handling

```javascript
// GOOD: Identify user after OAuth callback
async function handleOAuthCallback() {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');
  
  if (!code) {
    redirectToLogin();
    return;
  }
  
  try {
    // Exchange code for tokens and user info
    const { user, tokens } = await exchangeOAuthCode(code);
    
    // Store tokens
    setAuthTokens(tokens);
    
    // Identify in Fullstory BEFORE redirecting away
    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        email: user.email,
        authProvider: 'google',  // Track SSO provider
        ssoOrganization: user.hostedDomain
      }
    });
    
    // Now safe to redirect
    redirectToDashboard();
  } catch (error) {
    handleOAuthError(error);
  }
}
```

**Why this is good:**
- ✅ Identifies user before any redirects
- ✅ Captures authentication provider for analytics
- ✅ Handles SSO organization context
- ✅ Proper error handling flow

### Example 5: With Explicit Schema Types

```javascript
// GOOD: Using schema for explicit type control
FS('setIdentity', {
  uid: 'usr_a1b2c3d4e5',
  properties: {
    displayName: 'Sarah Johnson',
    email: 'sarah.johnson@company.com',
    accountBalance: 1500.50,
    loginCount: 42,
    isPremium: true,
    signupDate: '2023-06-15T00:00:00Z',
    permissions: ['read', 'write', 'admin']
  },
  schema: {
    accountBalance: 'real',
    loginCount: 'int',
    isPremium: 'bool',
    signupDate: 'date',
    permissions: 'strs'
  }
});
```

**Why this is good:**
- ✅ Explicit schema ensures proper type handling
- ✅ Enables numeric comparisons in Fullstory search
- ✅ Boolean enables is/is-not filtering
- ✅ Date enables time-based queries
- ✅ String array enables "contains" searches

---

## ❌ BAD Implementation Examples

### Example 1: Using Email as UID

```javascript
// BAD: Using email as the unique identifier
FS('setIdentity', {
  uid: user.email,  // BAD: PII as uid
  properties: {
    displayName: user.name
  }
});
```

**Why this is bad:**
- ❌ Email is PII — exposes it in Fullstory URLs and exports
- ❌ Email can change when user updates their email address
- ❌ May cause session linking issues if email is reused
- ❌ Violates privacy best practices

**CORRECTED:**
```javascript
// GOOD: Use stable database ID
FS('setIdentity', {
  uid: user.id,  // Stable, non-PII identifier
  properties: {
    displayName: user.name,
    email: user.email  // Email as a searchable property, not the uid
  }
});
```

### Example 2: Identifying Before Authentication Completes

```javascript
// BAD: Calling setIdentity before auth is confirmed
function handleLoginClick() {
  const credentials = getFormCredentials();
  
  // BAD: Identifying with form data before server confirms identity
  FS('setIdentity', {
    uid: credentials.username,
    properties: {
      email: credentials.email
    }
  });
  
  // This might fail - user isn't actually authenticated yet!
  authenticateUser(credentials);
}
```

**Why this is bad:**
- ❌ Identifies user before authentication succeeds
- ❌ If login fails, wrong identity is associated with session
- ❌ Username from form may not match actual user ID
- ❌ Creates data integrity issues

**CORRECTED:**
```javascript
// GOOD: Only identify after successful authentication
async function handleLoginClick() {
  const credentials = getFormCredentials();
  
  try {
    const response = await authenticateUser(credentials);
    
    // Only identify AFTER server confirms auth
    FS('setIdentity', {
      uid: response.user.id,
      properties: {
        displayName: response.user.name,
        email: response.user.email
      }
    });
    
    redirectToDashboard();
  } catch (error) {
    // Login failed - user remains anonymous
    showLoginError(error);
  }
}
```

### Example 3: Attempting to Change Identity

```javascript
// BAD: Trying to switch users without proper anonymization
function switchUserAccount(newUser) {
  // This will cause a session split, not update the identity!
  FS('setIdentity', {
    uid: newUser.id,
    properties: {
      displayName: newUser.name
    }
  });
}
```

**Why this is bad:**
- ❌ Cannot change identity of an already-identified user
- ❌ Causes automatic session split (may be unexpected)
- ❌ Creates confusing user journey in Fullstory
- ❌ May fragment analytics data

**CORRECTED:**
```javascript
// GOOD: Properly handle account switching
async function switchUserAccount(newUser) {
  // First, anonymize the current session
  FS('setIdentity', { anonymous: true });
  
  // Then identify as the new user (starts fresh session)
  FS('setIdentity', {
    uid: newUser.id,
    properties: {
      displayName: newUser.name,
      email: newUser.email
    }
  });
}
```

### Example 4: Calling setIdentity on Every Interaction

```javascript
// BAD: Over-calling setIdentity
function handleButtonClick(buttonId) {
  // BAD: Don't call setIdentity on every interaction!
  FS('setIdentity', {
    uid: currentUser.id,
    properties: {
      displayName: currentUser.name,
      lastAction: buttonId  // Trying to track actions via identity
    }
  });
  
  performAction(buttonId);
}
```

**Why this is bad:**
- ❌ Wastes rate limit quota (30 calls/minute max)
- ❌ May hit burst limit (10 calls/second)
- ❌ Properties on identity shouldn't track transient actions
- ❌ Misuse of API — should use trackEvent for actions

**CORRECTED:**
```javascript
// GOOD: Identify once, use events for actions
// On page load / auth
FS('setIdentity', {
  uid: currentUser.id,
  properties: {
    displayName: currentUser.name,
    email: currentUser.email
  }
});

// For tracking actions - use trackEvent instead
function handleButtonClick(buttonId) {
  FS('trackEvent', {
    name: 'Button Clicked',
    properties: {
      buttonId: buttonId,
      buttonSection: getButtonSection(buttonId)
    }
  });
  
  performAction(buttonId);
}
```

### Example 5: Missing displayName and email

```javascript
// BAD: Minimal identification with no useful properties
FS('setIdentity', {
  uid: user.id
  // No properties at all!
});
```

**Why this is bad:**
- ❌ No displayName — sessions show cryptic ID in Fullstory UI
- ❌ No email — can't search users via email
- ❌ No business context — can't segment users effectively
- ❌ Wastes the opportunity to enrich user data

**CORRECTED:**
```javascript
// GOOD: Rich user context
FS('setIdentity', {
  uid: user.id,
  properties: {
    displayName: user.fullName || user.username,
    email: user.email,
    role: user.role,
    plan: user.subscriptionPlan,
    companyName: user.organization?.name,
    signupDate: user.createdAt
  }
});
```

### Example 6: Type Mismatches in Properties

```javascript
// BAD: Wrong value formats for intended types
FS('setIdentity', {
  uid: 'usr_123',
  properties: {
    displayName: 'John Doe',
    loginCount: '42',           // BAD: String instead of number
    accountBalance: '$150.00',  // BAD: Currency symbol in number
    isPremium: 'yes',           // BAD: Should be boolean
    signupDate: 'June 15 2023'  // BAD: Not ISO8601 format
  },
  schema: {
    loginCount: 'int',
    accountBalance: 'real',
    isPremium: 'bool',
    signupDate: 'date'
  }
});
```

**Why this is bad:**
- ❌ loginCount '42' won't parse correctly as int
- ❌ '$150.00' won't parse as real due to $ symbol
- ❌ 'yes' is not a valid boolean value
- ❌ Date format won't be recognized

**CORRECTED:**
```javascript
// GOOD: Properly formatted values
FS('setIdentity', {
  uid: 'usr_123',
  properties: {
    displayName: 'John Doe',
    loginCount: 42,                    // Number type
    accountBalance: 150.00,            // Clean number
    currency: 'USD',                   // Currency as separate field
    isPremium: true,                   // Boolean type
    signupDate: '2023-06-15T00:00:00Z' // ISO8601 format
  },
  schema: {
    loginCount: 'int',
    accountBalance: 'real',
    isPremium: 'bool',
    signupDate: 'date'
  }
});
```

---

## Common Implementation Patterns

### Pattern 1: Multi-Account Application

```javascript
// For apps where users can switch between accounts
class FullstoryIdentityManager {
  currentUserId = null;
  
  identify(user) {
    if (this.currentUserId && this.currentUserId !== user.id) {
      // Different user - must anonymize first
      this.anonymize();
    }
    
    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        email: user.email
      }
    });
    
    this.currentUserId = user.id;
  }
  
  anonymize() {
    FS('setIdentity', { anonymous: true });
    this.currentUserId = null;
  }
  
  updateProperties(properties) {
    // Use setProperties for property-only updates
    FS('setProperties', {
      type: 'user',
      properties: properties
    });
  }
}
```

### Pattern 2: Progressive Identification (Guest Checkout)

```javascript
// For apps with guest checkout → account creation flow
class ProgressiveIdentification {
  
  // During guest checkout - don't identify yet
  handleGuestCheckout(cart) {
    // User remains anonymous
    // Track the checkout event instead
    FS('trackEvent', {
      name: 'Guest Checkout Started',
      properties: {
        cartValue: cart.total,
        itemCount: cart.items.length
      }
    });
  }
  
  // When guest creates account after checkout
  handleAccountCreation(user) {
    // NOW identify them - this links all prior anonymous activity
    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        email: user.email,
        accountCreatedDuringCheckout: true
      }
    });
  }
}
```

### Pattern 3: Vue Plugin

```javascript
// plugins/fullstory.js
export const FullstoryPlugin = {
  install(app) {
    app.config.globalProperties.$fsIdentify = (user) => {
      if (user && user.id) {
        FS('setIdentity', {
          uid: user.id,
          properties: {
            displayName: user.name,
            email: user.email
          }
        });
      }
    };
    
    app.config.globalProperties.$fsAnonymize = () => {
      FS('setIdentity', { anonymous: true });
    };
  }
};
```

### Pattern 4: Angular Service

```typescript
@Injectable({ providedIn: 'root' })
export class FullstoryService {
  private currentUserId: string | null = null;
  
  identify(user: User): void {
    if (this.currentUserId && this.currentUserId !== user.id) {
      this.anonymize();
    }
    
    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        email: user.email,
        role: user.role
      }
    });
    
    this.currentUserId = user.id;
  }
  
  anonymize(): void {
    FS('setIdentity', { anonymous: true });
    this.currentUserId = null;
  }
}
```

---

## Integration with Other APIs

### Identification + User Properties

```javascript
// setIdentity can include properties
FS('setIdentity', {
  uid: user.id,
  properties: {
    displayName: user.name,
    email: user.email,
    plan: 'starter'  // Initial plan at signup
  }
});

// Later, update properties without re-identifying
// (user upgraded their plan)
FS('setProperties', {
  type: 'user',
  properties: {
    plan: 'professional',
    upgradedAt: new Date().toISOString()
  }
});
```

### Identification + Events

```javascript
// Identify user
FS('setIdentity', {
  uid: user.id,
  properties: { displayName: user.name }
});

// Events are automatically linked to identified user
FS('trackEvent', {
  name: 'Feature Used',
  properties: {
    featureName: 'Advanced Export',
    exportFormat: 'CSV'
  }
});
```

### Identification + Page Properties

```javascript
// User identity
FS('setIdentity', {
  uid: user.id,
  properties: { displayName: user.name }
});

// Page context (separate concern)
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Dashboard',
    dashboardView: 'analytics'
  }
});
```

---

## Reference Links

- **Identify Users**: https://developer.fullstory.com/browser/identification/identify-users/
- **Anonymize Users**: https://developer.fullstory.com/browser/identification/anonymize-users/
- **Set User Properties**: https://developer.fullstory.com/browser/identification/set-user-properties/
- **Custom Properties**: https://developer.fullstory.com/browser/custom-properties/
