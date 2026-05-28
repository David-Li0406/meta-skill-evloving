---
name: Analytics & Tracking
description: User behavior tracking, event logging, and analytics dashboards
---

# Analytics & Tracking Skill

## Analytics Providers

### Vercel Analytics (Recommended)
```bash
npm install @vercel/analytics
```

```jsx
// app/layout.js or _app.js
import { Analytics } from '@vercel/analytics/react';

export default function Layout({ children }) {
  return (
    <>
      {children}
      <Analytics />
    </>
  );
}
```

### PostHog (Self-hostable)
```bash
npm install posthog-js
```

```javascript
import posthog from 'posthog-js';

// Initialize
if (typeof window !== 'undefined') {
  posthog.init('YOUR_API_KEY', {
    api_host: 'https://app.posthog.com'
  });
}

// Track events
posthog.capture('game_started', {
  game_type: 'gto_trainer',
  difficulty: 'advanced'
});

// Identify users
posthog.identify(userId, {
  email: user.email,
  plan: user.plan
});
```

### Google Analytics 4
```jsx
import Script from 'next/script';

export default function Layout({ children }) {
  return (
    <>
      <Script src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX" />
      <Script id="google-analytics">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'G-XXXXXXX');
        `}
      </Script>
      {children}
    </>
  );
}
```

## Custom Event Tracking

### Event Logger
```javascript
// lib/analytics.js
export const analytics = {
  track: (event, properties = {}) => {
    // PostHog
    if (typeof window !== 'undefined' && window.posthog) {
      window.posthog.capture(event, properties);
    }
    
    // Supabase (custom logging)
    logEvent(event, properties);
  },
  
  page: (url) => {
    if (typeof window !== 'undefined' && window.posthog) {
      window.posthog.capture('$pageview', { url });
    }
  },
  
  identify: (userId, traits = {}) => {
    if (typeof window !== 'undefined' && window.posthog) {
      window.posthog.identify(userId, traits);
    }
  }
};

async function logEvent(event, properties) {
  await supabase.from('analytics_events').insert({
    event,
    properties,
    user_id: getCurrentUserId(),
    timestamp: new Date().toISOString(),
    session_id: getSessionId()
  });
}
```

### React Hook
```javascript
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { analytics } from '@/lib/analytics';

export function usePageTracking() {
  const router = useRouter();
  
  useEffect(() => {
    const handleRouteChange = (url) => analytics.page(url);
    router.events.on('routeChangeComplete', handleRouteChange);
    return () => router.events.off('routeChangeComplete', handleRouteChange);
  }, [router.events]);
}
```

## Key Events to Track

### Game Events
```javascript
analytics.track('game_started', { game_id, game_type, difficulty });
analytics.track('game_completed', { game_id, score, duration, correct_percentage });
analytics.track('level_up', { new_level, xp_earned });
analytics.track('achievement_unlocked', { achievement_id, achievement_name });
```

### Commerce Events
```javascript
analytics.track('store_viewed', {});
analytics.track('item_added_to_cart', { item_id, item_name, price });
analytics.track('checkout_started', { total_amount, items_count });
analytics.track('purchase_completed', { order_id, total_amount, payment_method });
```

### Engagement Events
```javascript
analytics.track('feature_used', { feature_name });
analytics.track('share_clicked', { content_type, platform });
analytics.track('referral_sent', { referral_code });
```

## Database Schema
```sql
CREATE TABLE analytics_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event TEXT NOT NULL,
  properties JSONB,
  user_id UUID REFERENCES auth.users,
  session_id TEXT,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  user_agent TEXT,
  ip_address INET
);

CREATE INDEX idx_events_timestamp ON analytics_events(timestamp);
CREATE INDEX idx_events_user ON analytics_events(user_id);
CREATE INDEX idx_events_event ON analytics_events(event);
```
