---
name: analytics
description: "Use when implementing analytics, event tracking, or setting up dashboards. Covers privacy-first tracking, event patterns, and common analytics tools."
---

# Analytics Integration

## Overview

Analytics implementation patterns covering event tracking, privacy considerations, and dashboard setup. Focus on privacy-first approaches with actionable insights.

## When to Use

- Setting up analytics for a project
- Implementing custom event tracking
- Designing metrics dashboards
- Ensuring privacy compliance

## Quick Reference

| Provider | Privacy | Best For |
|----------|---------|----------|
| **Plausible** | Privacy-first, no cookies | Simple traffic analytics |
| **PostHog** | Self-hostable, feature flags | Product analytics, A/B tests |
| **Mixpanel** | Event-focused | User journey tracking |
| **Google Analytics** | Free, comprehensive | Traffic + conversions |
| **Vercel Analytics** | Edge, Web Vitals | Next.js performance |

---

## Privacy-First Setup

### Plausible (Recommended)

```typescript
// app/layout.tsx
import Script from 'next/script';

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <Script
          defer
          data-domain="yourdomain.com"
          src="https://plausible.io/js/script.js"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### Custom Events (Plausible)

```typescript
// lib/analytics.ts
export function trackEvent(name: string, props?: Record<string, string>) {
  if (typeof window !== 'undefined' && window.plausible) {
    window.plausible(name, { props });
  }
}

// Usage
trackEvent('Signup', { plan: 'pro' });
trackEvent('Feature Used', { feature: 'export' });
```

---

## PostHog Setup

### Installation

```typescript
// lib/posthog.ts
import posthog from 'posthog-js';

export function initPostHog() {
  if (typeof window !== 'undefined') {
    posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
      api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST,
      capture_pageview: false, // Manual control
      persistence: 'localStorage',
    });
  }
}

export { posthog };
```

### Provider Setup

```typescript
// app/providers.tsx
'use client';

import { useEffect } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';
import { initPostHog, posthog } from '@/lib/posthog';

export function AnalyticsProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    initPostHog();
  }, []);

  // Track page views
  useEffect(() => {
    if (pathname) {
      posthog.capture('$pageview', {
        $current_url: window.location.href,
      });
    }
  }, [pathname, searchParams]);

  return <>{children}</>;
}
```

### Event Tracking

```typescript
// Track events
posthog.capture('button_clicked', {
  button_name: 'signup',
  page: '/pricing',
});

// Identify users
posthog.identify(userId, {
  email: user.email,
  plan: user.plan,
});

// Feature flags
const showNewFeature = posthog.isFeatureEnabled('new-dashboard');
```

---

## Event Tracking Patterns

### Standard Events

```typescript
// lib/analytics.ts
type EventName =
  | 'page_view'
  | 'signup_started'
  | 'signup_completed'
  | 'feature_used'
  | 'checkout_started'
  | 'purchase_completed'
  | 'error_occurred';

interface EventProperties {
  page_view: { path: string; referrer?: string };
  signup_started: { method: 'email' | 'google' | 'github' };
  signup_completed: { method: string; plan?: string };
  feature_used: { feature: string; context?: string };
  checkout_started: { plan: string; price: number };
  purchase_completed: { plan: string; revenue: number };
  error_occurred: { error: string; context: string };
}

export function track<E extends EventName>(
  event: E,
  properties: EventProperties[E]
) {
  // Send to your analytics provider
  posthog.capture(event, properties);
}
```

### Conversion Funnel

```typescript
// Track funnel steps
track('signup_started', { method: 'email' });
// ... user completes form ...
track('signup_completed', { method: 'email', plan: 'free' });
// ... user adds payment ...
track('checkout_started', { plan: 'pro', price: 29 });
// ... payment succeeds ...
track('purchase_completed', { plan: 'pro', revenue: 29 });
```

### User Properties

```typescript
// Set user properties once identified
posthog.identify(user.id, {
  email: user.email,
  name: user.name,
  created_at: user.createdAt,
  plan: user.plan,
  company: user.company,
});

// Update properties when they change
posthog.people.set({
  plan: 'pro',
  last_login: new Date().toISOString(),
});
```

---

## Privacy Considerations

### Cookie Consent

```typescript
// components/CookieConsent.tsx
'use client';

import { useState, useEffect } from 'react';

export function CookieConsent() {
  const [consent, setConsent] = useState<boolean | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem('analytics_consent');
    if (stored !== null) {
      setConsent(stored === 'true');
    }
  }, []);

  const handleConsent = (accepted: boolean) => {
    localStorage.setItem('analytics_consent', String(accepted));
    setConsent(accepted);

    if (accepted) {
      initAnalytics();
    }
  };

  if (consent !== null) return null;

  return (
    <div className="fixed bottom-4 right-4 bg-white p-4 rounded-lg shadow-lg">
      <p>We use analytics to improve your experience.</p>
      <div className="flex gap-2 mt-2">
        <button onClick={() => handleConsent(true)}>Accept</button>
        <button onClick={() => handleConsent(false)}>Decline</button>
      </div>
    </div>
  );
}
```

### Data Retention

```typescript
// Configure data retention
posthog.init(key, {
  persistence: 'localStorage', // or 'cookie', 'memory'
  persistence_name: 'ph_', // Custom prefix
  property_blacklist: ['email', 'phone'], // Never track
});
```

### GDPR Compliance

```typescript
// Right to deletion
async function handleDeleteRequest(userId: string) {
  // Delete from PostHog
  await fetch('https://app.posthog.com/api/person/', {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${POSTHOG_API_KEY}` },
    body: JSON.stringify({ distinct_id: userId }),
  });

  // Delete from your database
  await db.user.delete({ where: { id: userId } });
}
```

---

## Dashboard Setup

### Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **DAU/MAU** | Daily/Monthly active users | Growth trend |
| **Conversion Rate** | Signups to paid | > 2-5% |
| **Retention** | Users returning after X days | D1 > 40%, D7 > 20% |
| **ARPU** | Average revenue per user | Depends on model |
| **Churn** | Users leaving per month | < 5% |

### Custom Dashboard Query (PostHog)

```sql
-- Active users by day
SELECT
  toDate(timestamp) as date,
  count(DISTINCT distinct_id) as users
FROM events
WHERE event = '$pageview'
  AND timestamp > now() - interval 30 day
GROUP BY date
ORDER BY date
```

### Vercel Analytics (Next.js)

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

---

## Common Patterns

### A/B Testing (PostHog)

```typescript
// Get variant
const variant = posthog.getFeatureFlag('pricing-page-test');

// Track exposure
posthog.capture('$feature_flag_called', {
  $feature_flag: 'pricing-page-test',
  $feature_flag_response: variant,
});

// Render based on variant
return variant === 'control' ? <PricingA /> : <PricingB />;
```

### Error Tracking

```typescript
// Track errors with context
window.addEventListener('error', (event) => {
  track('error_occurred', {
    error: event.message,
    context: event.filename + ':' + event.lineno,
  });
});

// Track unhandled rejections
window.addEventListener('unhandledrejection', (event) => {
  track('error_occurred', {
    error: event.reason?.message || 'Unknown',
    context: 'unhandled_promise',
  });
});
```

---

## Red Flags - STOP

**Never:**
- Track PII without consent
- Send passwords or tokens to analytics
- Track on localhost in production code
- Ignore GDPR/CCPA requirements

**Always:**
- Implement cookie consent for EU users
- Anonymize IPs when possible
- Document what you track
- Provide opt-out mechanism
- Test tracking in development mode

---

## Integration

**Related skills:** frontend-design, payment-processing
**Tools:** PostHog, Plausible, Mixpanel, Google Analytics
