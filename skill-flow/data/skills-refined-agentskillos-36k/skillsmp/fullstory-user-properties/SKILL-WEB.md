---
name: fullstory-user-properties-web
version: v3
platform: web
sdk: fullstory-browser
description: JavaScript/TypeScript implementation guide for Fullstory's User Properties API. Includes API reference, code examples, and common patterns for web applications.
parent_skill: fullstory-user-properties
related_skills:
  - fullstory-user-properties
  - fullstory-identify-users
  - fullstory-page-properties
---

# Fullstory User Properties — Web Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for property types, special fields, and best practices.
>
> **Other Platforms**: See [SKILL-MOBILE.md](./SKILL-MOBILE.md) for iOS, Android, Flutter, React Native.

---

## API Reference

### Basic Syntax

```javascript
FS('setProperties', {
  type: 'user',
  properties: object,     // Required: Key/value pairs
  schema?: object         // Optional: Type hints
});
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | **Yes** | Must be `'user'` for user properties |
| `properties` | object | **Yes** | Key/value pairs of user data |
| `schema` | object | No | Explicit type inference for properties |

---

## ✅ GOOD Implementation Examples

### Example 1: Post-Identification Profile Enrichment

```javascript
// GOOD: Add properties after initial identification
// Step 1: Identify user on login (minimal properties)
FS('setIdentity', {
  uid: user.id,
  properties: {
    displayName: user.name,
    email: user.email
  }
});

// Step 2: Enrich with additional data once loaded
async function loadUserProfile() {
  const profile = await fetchUserProfile(user.id);
  
  FS('setProperties', {
    type: 'user',
    properties: {
      companyName: profile.company.name,
      companySize: profile.company.employeeCount,
      industry: profile.company.industry,
      role: profile.role,
      department: profile.department,
      signupSource: profile.attribution.source,
      referralCode: profile.attribution.referralCode
    }
  });
}
```

**Why this is good:**
- ✅ Quick identification on login (doesn't block on profile load)
- ✅ Rich data added once available
- ✅ Clean separation of concerns
- ✅ Properties available for segmentation

### Example 2: Subscription/Plan Updates

```javascript
// GOOD: Track subscription changes without re-identifying
async function handlePlanUpgrade(newPlan) {
  // Process the upgrade
  await processUpgrade(newPlan);
  
  // Update user properties to reflect new plan
  FS('setProperties', {
    type: 'user',
    properties: {
      plan: newPlan.name,
      planTier: newPlan.tier,
      monthlyPrice: newPlan.price,
      billingCycle: newPlan.billingCycle,
      planChangedAt: new Date().toISOString(),
      previousPlan: getCurrentPlan().name
    },
    schema: {
      monthlyPrice: 'real',
      planChangedAt: 'date'
    }
  });
  
  // Also track as an event for funnel analysis
  FS('trackEvent', {
    name: 'Plan Upgraded',
    properties: {
      fromPlan: getCurrentPlan().name,
      toPlan: newPlan.name,
      priceDifference: newPlan.price - getCurrentPlan().price
    }
  });
}
```

**Why this is good:**
- ✅ Updates user properties without re-identification
- ✅ Tracks both current state (property) and change (event)
- ✅ Uses schema for proper type handling
- ✅ Captures before/after for analysis

### Example 3: Progressive Profiling (Onboarding)

```javascript
// GOOD: Build up user profile through onboarding steps
class OnboardingFlow {
  
  // Step 1: Basic info collected
  completeBasicInfo(data) {
    FS('setProperties', {
      type: 'user',
      properties: {
        companyName: data.companyName,
        companySize: data.companySize,
        onboardingStep: 1,
        onboardingStartedAt: new Date().toISOString()
      },
      schema: {
        onboardingStep: 'int',
        onboardingStartedAt: 'date'
      }
    });
  }
  
  // Step 2: Use case selection
  completeUseCaseSelection(useCases) {
    FS('setProperties', {
      type: 'user',
      properties: {
        primaryUseCase: useCases.primary,
        secondaryUseCases: useCases.secondary,  // Array of strings
        onboardingStep: 2
      },
      schema: {
        secondaryUseCases: 'strs',
        onboardingStep: 'int'
      }
    });
  }
  
  // Step 3: Integration setup
  completeIntegrationSetup(integrations) {
    FS('setProperties', {
      type: 'user',
      properties: {
        connectedIntegrations: integrations.connected,
        integrationCount: integrations.connected.length,
        onboardingStep: 3
      },
      schema: {
        connectedIntegrations: 'strs',
        integrationCount: 'int',
        onboardingStep: 'int'
      }
    });
  }
  
  // Final step: Mark complete
  completeOnboarding() {
    FS('setProperties', {
      type: 'user',
      properties: {
        onboardingComplete: true,
        onboardingCompletedAt: new Date().toISOString(),
        onboardingStep: 4
      },
      schema: {
        onboardingComplete: 'bool',
        onboardingCompletedAt: 'date',
        onboardingStep: 'int'
      }
    });
  }
}
```

**Why this is good:**
- ✅ Builds profile incrementally
- ✅ Each step adds relevant properties
- ✅ Tracks progress via onboardingStep
- ✅ Enables segment analysis of drop-off points

### Example 4: Feature Usage Tracking

```javascript
// GOOD: Track feature adoption at user level
class FeatureUsageTracker {
  
  trackFeatureFirstUse(featureName) {
    const propertyName = `firstUsed_${featureName}`;
    
    FS('setProperties', {
      type: 'user',
      properties: {
        [propertyName]: new Date().toISOString()
      },
      schema: {
        [propertyName]: 'date'
      }
    });
  }
  
  updateFeatureEngagement(features) {
    FS('setProperties', {
      type: 'user',
      properties: {
        featuresUsed: features.used,
        mostUsedFeature: features.mostUsed,
        featureUsageScore: features.engagementScore,
        lastActiveFeature: features.lastUsed,
        lastFeatureUseAt: new Date().toISOString()
      },
      schema: {
        featuresUsed: 'strs',
        featureUsageScore: 'int',
        lastFeatureUseAt: 'date'
      }
    });
  }
}

// Usage
const tracker = new FeatureUsageTracker();
tracker.trackFeatureFirstUse('advanced_export');
tracker.updateFeatureEngagement({
  used: ['dashboard', 'reports', 'advanced_export'],
  mostUsed: 'reports',
  engagementScore: 85,
  lastUsed: 'advanced_export'
});
```

**Why this is good:**
- ✅ Tracks feature adoption dates
- ✅ Maintains engagement metrics
- ✅ Enables feature-based segmentation
- ✅ Supports adoption analysis

### Example 5: CRM Data Sync

```javascript
// GOOD: Sync key CRM fields to Fullstory
async function syncCRMData(userId) {
  const crmData = await fetchFromCRM(userId);
  
  FS('setProperties', {
    type: 'user',
    properties: {
      // Sales/Account info
      accountOwner: crmData.owner.name,
      accountStage: crmData.stage,
      dealValue: crmData.opportunity.value,
      closeDate: crmData.opportunity.expectedClose,
      
      // Health metrics
      healthScore: crmData.health.score,
      churnRisk: crmData.health.churnRisk,
      npsScore: crmData.health.nps,
      
      // Engagement
      lastContactDate: crmData.lastContact,
      meetingsScheduled: crmData.meetings.scheduled,
      supportTicketsOpen: crmData.support.openTickets,
      
      // Sync metadata
      crmSyncedAt: new Date().toISOString()
    },
    schema: {
      dealValue: 'real',
      closeDate: 'date',
      healthScore: 'int',
      churnRisk: 'real',
      npsScore: 'int',
      lastContactDate: 'date',
      meetingsScheduled: 'int',
      supportTicketsOpen: 'int',
      crmSyncedAt: 'date'
    }
  });
}
```

**Why this is good:**
- ✅ Bridges CRM and product analytics
- ✅ Enables sales context in session replay
- ✅ Supports health-based segmentation
- ✅ Tracks sync time for data freshness

### Example 6: Anonymous User Enrichment

```javascript
// GOOD: Add properties to anonymous users before they identify
function trackAnonymousVisitor() {
  // User lands on your site (anonymous - "User 4521" in Fullstory)
  FS('setProperties', {
    type: 'user',
    properties: {
      landing_page: window.location.pathname,
      referral_source: getUTMSource(),
      campaign: getUTMCampaign(),
      visitor_type: 'new'
    }
  });
}

// Later, when user creates an account and logs in
function handleSignup(user) {
  FS('setIdentity', {
    uid: user.id,
    properties: {
      displayName: user.name,
      email: user.email
    }
  });
  // The anonymous properties (landing_page, referral_source, campaign) 
  // are now attached to the identified user
}
```

**Why this is good:**
- ✅ Captures attribution data before identification
- ✅ Properties persist and transfer on identification
- ✅ Enables full-funnel attribution analysis

---

## ❌ BAD Implementation Examples

### Example 1: Using setProperties Instead of setIdentity

```javascript
// BAD: Trying to use setProperties for initial identification
FS('setProperties', {
  type: 'user',
  properties: {
    uid: user.id,  // This won't work!
    displayName: user.name,
    email: user.email
  }
});
```

**Why this is bad:**
- ❌ setProperties doesn't establish identity
- ❌ uid as a property doesn't link sessions
- ❌ User remains anonymous
- ❌ Misunderstanding of API purpose

**CORRECTED:**
```javascript
// GOOD: Use setIdentity for identification
FS('setIdentity', {
  uid: user.id,
  properties: {
    displayName: user.name,
    email: user.email
  }
});
```

### Example 2: Missing Type Parameter

```javascript
// BAD: Missing type parameter
FS('setProperties', {
  properties: {
    plan: 'premium'
  }
  // Missing type: 'user'!
});
```

**Why this is bad:**
- ❌ Missing required `type` parameter
- ❌ API call will fail or behave unexpectedly
- ❌ Easy to miss in testing

**CORRECTED:**
```javascript
// GOOD: Include type parameter
FS('setProperties', {
  type: 'user',  // Required!
  properties: {
    plan: 'premium'
  }
});
```

### Example 3: Excessive Calls

```javascript
// BAD: Calling setProperties too frequently
function handleFormFieldChange(fieldName, value) {
  // BAD: This fires on every keystroke!
  FS('setProperties', {
    type: 'user',
    properties: {
      [`form_${fieldName}`]: value
    }
  });
}
```

**Why this is bad:**
- ❌ Will hit rate limits (30/min, 10/sec)
- ❌ Wastes API calls on intermediate states
- ❌ Transient form data isn't good for user properties

**CORRECTED:**
```javascript
// GOOD: Batch updates on form submission
function handleFormSubmit(formData) {
  // Set meaningful final values
  FS('setProperties', {
    type: 'user',
    properties: {
      preferredContact: formData.contactMethod,
      marketingOptIn: formData.optIn,
      timezone: formData.timezone
    }
  });
  
  // Track the form submission as event
  FS('trackEvent', {
    name: 'Preferences Updated',
    properties: formData
  });
}
```

### Example 4: Type Mismatches

```javascript
// BAD: Incorrect value formats
FS('setProperties', {
  type: 'user',
  properties: {
    accountBalance: '$1,234.56',   // BAD: Formatted currency
    loginCount: 'forty-two',       // BAD: Written number
    isPremium: 'yes',              // BAD: String instead of boolean
    signupDate: 'January 15, 2024' // BAD: Not ISO8601
  },
  schema: {
    accountBalance: 'real',
    loginCount: 'int',
    isPremium: 'bool',
    signupDate: 'date'
  }
});
```

**Why this is bad:**
- ❌ Values don't match declared types
- ❌ Parsing will fail
- ❌ Properties won't be queryable correctly

**CORRECTED:**
```javascript
// GOOD: Properly formatted values
FS('setProperties', {
  type: 'user',
  properties: {
    accountBalance: 1234.56,
    currency: 'USD',  // Separate field for formatting
    loginCount: 42,
    isPremium: true,
    signupDate: '2024-01-15T00:00:00Z'
  },
  schema: {
    accountBalance: 'real',
    loginCount: 'int',
    isPremium: 'bool',
    signupDate: 'date'
  }
});
```

### Example 5: Overwriting Important Properties

```javascript
// BAD: Carelessly overwriting displayName
function updateLastActivity() {
  FS('setProperties', {
    type: 'user',
    properties: {
      displayName: 'Active User',  // BAD: Overwrites the real name!
      lastActivityAt: new Date().toISOString()
    }
  });
}
```

**Why this is bad:**
- ❌ Overwrites displayName with generic value
- ❌ Loses actual user name in Fullstory UI
- ❌ Makes sessions hard to identify

**CORRECTED:**
```javascript
// GOOD: Only update intended properties
function updateLastActivity() {
  FS('setProperties', {
    type: 'user',
    properties: {
      lastActivityAt: new Date().toISOString(),
      isRecentlyActive: true
    },
    schema: {
      lastActivityAt: 'date',
      isRecentlyActive: 'bool'
    }
  });
}
```

---

## Common Implementation Patterns

### Pattern 1: Property Manager Class

```javascript
// Centralized user property management
class UserPropertyManager {
  constructor() {
    this.pendingProperties = {};
    this.flushTimeout = null;
  }
  
  // Queue properties for batched update
  queue(properties, schema = {}) {
    Object.assign(this.pendingProperties, properties);
    
    // Debounce to batch rapid updates
    if (this.flushTimeout) clearTimeout(this.flushTimeout);
    this.flushTimeout = setTimeout(() => this.flush(), 1000);
  }
  
  // Immediately send properties
  flush() {
    if (Object.keys(this.pendingProperties).length === 0) return;
    
    FS('setProperties', {
      type: 'user',
      properties: this.pendingProperties
    });
    
    this.pendingProperties = {};
    this.flushTimeout = null;
  }
  
  // Update specific category of properties
  updateEngagement(data) {
    this.queue({
      lastActiveAt: new Date().toISOString(),
      sessionCount: data.sessionCount,
      pageViewsTotal: data.pageViews
    });
  }
  
  updateSubscription(plan) {
    // Subscription updates are important - flush immediately
    FS('setProperties', {
      type: 'user',
      properties: {
        plan: plan.name,
        planTier: plan.tier,
        planUpdatedAt: new Date().toISOString()
      }
    });
  }
}
```

### Pattern 2: Property Sync on Page Load

```javascript
// Sync important properties on each page load
async function syncUserProperties() {
  const user = await getCurrentUser();
  if (!user) return;
  
  // Fetch latest data
  const [profile, subscription, usage] = await Promise.all([
    fetchProfile(user.id),
    fetchSubscription(user.id),
    fetchUsageStats(user.id)
  ]);
  
  // Sync to Fullstory
  FS('setProperties', {
    type: 'user',
    properties: {
      // Profile
      displayName: profile.fullName,
      email: profile.email,
      role: profile.role,
      
      // Subscription
      plan: subscription.plan,
      planStatus: subscription.status,
      mrr: subscription.mrr,
      
      // Usage
      lastLoginAt: usage.lastLogin,
      totalLogins: usage.loginCount,
      daysActive: usage.activeDays
    },
    schema: {
      mrr: 'real',
      lastLoginAt: 'date',
      totalLogins: 'int',
      daysActive: 'int'
    }
  });
}

// Run on app initialization
initApp().then(syncUserProperties);
```

### Pattern 3: Event-Driven Property Updates

```javascript
// Update properties based on key events
const eventPropertyMap = {
  'trial_started': (event) => ({
    trialStartedAt: new Date().toISOString(),
    trialPlan: event.plan,
    isTrialing: true
  }),
  
  'trial_converted': (event) => ({
    trialConvertedAt: new Date().toISOString(),
    isTrialing: false,
    isPaying: true,
    plan: event.plan
  }),
  
  'trial_expired': (event) => ({
    trialExpiredAt: new Date().toISOString(),
    isTrialing: false,
    isPaying: false
  }),
  
  'feature_enabled': (event) => ({
    [`feature_${event.feature}_enabled`]: true,
    [`feature_${event.feature}_enabledAt`]: new Date().toISOString()
  })
};

function handleBusinessEvent(eventName, eventData) {
  // Track the event
  FS('trackEvent', {
    name: eventName,
    properties: eventData
  });
  
  // Update user properties if mapping exists
  const propertyUpdater = eventPropertyMap[eventName];
  if (propertyUpdater) {
    FS('setProperties', {
      type: 'user',
      properties: propertyUpdater(eventData)
    });
  }
}
```

### Pattern 4: React Hook

```jsx
import { useCallback } from 'react';

export function useUserProperties() {
  const setProperties = useCallback((properties, schema = {}) => {
    FS('setProperties', {
      type: 'user',
      properties,
      schema
    });
  }, []);
  
  const updatePlan = useCallback((plan) => {
    setProperties({
      plan: plan.name,
      planTier: plan.tier,
      planUpdatedAt: new Date().toISOString()
    }, {
      planUpdatedAt: 'date'
    });
  }, [setProperties]);
  
  const updateEngagement = useCallback((metrics) => {
    setProperties({
      lastActiveAt: new Date().toISOString(),
      sessionCount: metrics.sessions,
      featureUsageScore: metrics.score
    }, {
      lastActiveAt: 'date',
      sessionCount: 'int',
      featureUsageScore: 'int'
    });
  }, [setProperties]);
  
  return { setProperties, updatePlan, updateEngagement };
}
```

### Pattern 5: Vue Plugin

```javascript
// plugins/fullstory-properties.js
export const UserPropertiesPlugin = {
  install(app) {
    app.config.globalProperties.$setUserProperties = (properties, schema = {}) => {
      FS('setProperties', {
        type: 'user',
        properties,
        schema
      });
    };
  }
};

// Usage in component
export default {
  methods: {
    updateUserPlan(plan) {
      this.$setUserProperties({
        plan: plan.name,
        planTier: plan.tier
      });
    }
  }
}
```

### Pattern 6: Angular Service

```typescript
@Injectable({ providedIn: 'root' })
export class UserPropertiesService {
  
  setProperties(properties: Record<string, any>, schema?: Record<string, string>): void {
    FS('setProperties', {
      type: 'user',
      properties,
      ...(schema && { schema })
    });
  }
  
  updateSubscription(subscription: Subscription): void {
    this.setProperties({
      plan: subscription.plan,
      planTier: subscription.tier,
      mrr: subscription.mrr,
      billingCycle: subscription.billingCycle
    }, {
      mrr: 'real'
    });
  }
  
  updateOnboardingProgress(step: number, complete: boolean): void {
    this.setProperties({
      onboardingStep: step,
      onboardingComplete: complete,
      ...(complete && { onboardingCompletedAt: new Date().toISOString() })
    }, {
      onboardingStep: 'int',
      onboardingComplete: 'bool',
      onboardingCompletedAt: 'date'
    });
  }
}
```

---

## Reference Links

- **Set User Properties**: https://developer.fullstory.com/browser/identification/set-user-properties/
- **Custom Properties**: https://developer.fullstory.com/browser/custom-properties/
- **Identify Users**: https://developer.fullstory.com/browser/identification/identify-users/
- **Help Center - Custom Properties**: https://help.fullstory.com/hc/en-us/articles/360020623234
