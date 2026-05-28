---
name: analytics-tracking
description: Event tracking with GA4 + PostHog, adding new events, and updating GTM. Use when implementing tracking, adding analytics events, or configuring GTM/PostHog. Keywords: analytics, tracking, GA4, PostHog, GTM, dataLayer, event, conversion, metrics, proxy, ad blocker.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.2"
  project: "stepleague"
  last_updated: "2026-01-26"
---

# Analytics Tracking Skill

## Overview

StepLeague uses a **dual-tracking architecture**:
- **GA4 (via GTM)**: Google Analytics for standard web analytics
- **PostHog SDK**: Session replay, feature flags, funnels, and product analytics

All events are pushed to both systems from a single `trackEvent()` call.

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                       analytics.ts                               │
│                                                                  │
│  trackEvent('event_name', { properties })                        │
│       │                                                          │
│       ├──────────────────▶ window.dataLayer.push() ──▶ GTM ──▶ GA4
│       │                                                          │
│       └──────────────────▶ posthog.capture() ──────────▶ PostHog │
└──────────────────────────────────────────────────────────────────┘
```

## Ad Blocker Bypass (First-Party Proxy)

Analytics requests are routed through first-party domain proxies to bypass ad blockers.
Ad blockers maintain lists of known tracking domains (posthog.com, googletagmanager.com).
By proxying through our own paths, these requests appear first-party and are not blocked.

**Expected improvement: 10-30% more events captured.**

```
Without proxy (blocked):
Browser → us.i.posthog.com (BLOCKED by uBlock/AdBlock)
Browser → www.googletagmanager.com (BLOCKED)

With proxy (bypasses blockers):
Browser → /ingest/* → Vercel rewrite → us.i.posthog.com (NOT blocked)
Browser → /gtm/* → Vercel rewrite → googletagmanager.com (NOT blocked)
```

### Proxy Configuration

| Service | Proxy Path | Original Host |
|---------|------------|---------------|
| PostHog | `/ingest/*` | `us.i.posthog.com` |
| PostHog Static | `/ingest/static/*` | `us-assets.i.posthog.com/static` |
| GTM | `/gtm/*` | `www.googletagmanager.com` |
| GA4 | `/ga/*` | `www.google-analytics.com` |

**Key Files:**
- `next.config.js` - Rewrite rules that proxy requests
- `src/lib/analytics/proxyConfig.ts` - Central registry of proxy configurations
- `PostHogProvider.tsx` - Uses `/ingest` as api_host
- `GoogleTagManager.tsx` - Loads GTM from `/gtm/gtm.js`

### Adding New Analytics Services

1. Add entry to `ANALYTICS_PROXIES` in `src/lib/analytics/proxyConfig.ts`
2. Add corresponding rewrite rules in `next.config.js`
3. Update the service's initialization to use the proxy path

## Key Files

| File | Purpose |
|------|---------|
| `src/lib/analytics.ts` | Main tracking library with all event methods |
| `src/components/analytics/PostHogProvider.tsx` | PostHog SDK initialization via `/ingest` proxy |
| `src/components/analytics/GoogleTagManager.tsx` | GTM loading via `/gtm` proxy |
| `src/lib/analytics/proxyConfig.ts` | Central registry of proxy configurations |
| `src/lib/consent/cookieConsent.ts` | Cookie consent helpers |
| `src/lib/__tests__/analytics.test.ts` | Test suite for analytics events |
| `next.config.js` | Vercel rewrite rules for analytics proxies |

## Critical Rules

> [!WARNING]
> **Always follow these rules when adding analytics tracking:**

### 1. Event Naming
- Use `snake_case` for event names: `league_created`, NOT `leagueCreated`
- Use past tense verbs: `submitted`, `created`, `clicked`
- Max 40 characters
- **Never use reserved prefixes**: `ga_`, `firebase_`, `google_`

### 2. Dual-Push Architecture
- **Never call PostHog or GTM directly** - always use `trackEvent()` from `analytics.ts`
- This ensures events go to both GA4 and PostHog automatically
- The `analytics` object exports all event methods

### 3. User Identification
- `identifyUser()` is called after login (handled in AuthProvider)
- `clearUser()` is called on logout (handled in `analytics.logout()`)
- **Never track PII** (emails, names) in event properties

### 4. Consent Compliance
- Analytics only fire after user grants consent via cookie banner
- Never bypass the consent check in PostHogProvider
- Consent state is managed by `vanilla-cookieconsent`

### 5. Testing New Events
- Add tests to `src/lib/__tests__/analytics.test.ts`
- Test both dataLayer push and PostHog capture calls
- See existing tests for `proxyClaimed` and `highFiveSent` as examples

## Recently Added Events (Jan 2026)

| Event | Purpose | Parameters |
|-------|---------|------------|
| `proxy_claimed` | Tracks when a proxy user claims their profile | `proxy_id`, `submission_count`, `league_count` |
| `high_five_sent` | Tracks high-five engagement interactions | `recipient_id`, `action` (send/remove) |

---

## Share Funnel Tracking (PRD-51)

Social sharing is a key growth driver. Track the full funnel:

### Share Events

| Event | When Fired | Parameters |
|-------|------------|------------|
| `share_intent` | User opens share modal | `card_type`, `metric_type`, `source` |
| `share` | User completes share action | `content_type`, `item_id`, `method` (platform) |
| `share_link_click` | Recipient clicks shared link | `short_code`, `card_type`, `referrer` |
| `share_conversion` | Recipient signs up after clicking share | `short_code`, `card_type` |

### Implementation Pattern

```typescript
// Track share intent (modal opened)
analytics.shareIntent = (cardType: string, metricType: string, source: string) => {
  trackEvent('share_intent', {
    card_type: cardType,        // 'daily', 'weekly', 'streak', etc.
    metric_type: metricType,    // 'steps', 'calories', etc.
    source: source,             // 'stats_hub', 'post_submission', 'milestone'
    category: 'social',
    action: 'open_modal',
  });
};

// Track share completion (existing analytics.share method)
analytics.share = (contentType: string, itemId: string, method: string) => {
  trackEvent('share', {
    content_type: contentType,
    item_id: itemId,
    method: method,  // 'whatsapp', 'twitter', 'copy', 'native'
    category: 'social',
    action: 'share',
  });
};

// Track shared link clicks (on share landing page)
analytics.shareLinkClick = (shortCode: string, cardType: string) => {
  trackEvent('share_link_click', {
    short_code: shortCode,
    card_type: cardType,
    referrer: document.referrer,
    category: 'social',
    action: 'click',
  });
};
```

### UTM Parameter Conventions

Always add UTM parameters to share URLs:

```typescript
const shareUrl = new URL(baseUrl);
shareUrl.searchParams.set('utm_source', 'share');
shareUrl.searchParams.set('utm_medium', platform);    // 'whatsapp', 'twitter', 'copy'
shareUrl.searchParams.set('utm_campaign', cardType);  // 'daily', 'streak', 'challenge'
```

### PostHog Funnel Configuration

Create a funnel in PostHog to track conversion:

```
share_intent → share → share_link_click → share_conversion
```

### A/B Testing Share Cards

Use PostHog experiments to test:
- Different card designs (theme variants)
- Message templates
- CTA button text
- Share prompt timing

```typescript
const variant = useFeatureFlagVariantKey('share-card-experiment');
// 'control', 'variant_a', 'variant_b'

// Track which variant was shown
analytics.trackEvent('share_experiment_shown', {
  experiment: 'share-card-experiment',
  variant: variant,
});
```

## Adding a New Tracking Event

### Step 1: Add event to `analytics.ts`

```typescript
// In src/lib/analytics.ts, add to the `analytics` object:

export const analytics = {
    // ... existing events ...

    // Add your new event:
    myNewEvent: (someParam: string, anotherParam: number) => {
        trackEvent('my_new_event', {
            some_param: someParam,
            another_param: anotherParam,
            category: 'engagement',  // or 'conversion', 'navigation', etc.
            action: 'click',
        });
    },
};
```

### Step 2: Use it in your component

```typescript
import { analytics } from '@/lib/analytics';

function MyComponent() {
    const handleClick = () => {
        analytics.myNewEvent('value', 123);
    };
    return <button onClick={handleClick}>Do Thing</button>;
}
```

### Step 3: Done! (Usually)

The event now flows to **both GA4 and PostHog automatically**. No GTM changes needed!

## When GTM Updates ARE Required

You only need to update GTM if you want to:

1. **Create a GA4 "Key Event"** - Mark the event as a conversion in GA4
2. **Add custom dimensions** - Register new parameters in GA4
3. **Create GTM triggers** - Fire other tags based on this event

### GTM Manual Steps (if needed)

1. Log into [Google Tag Manager](https://tagmanager.google.com/)
2. Create a **Custom Event Trigger** with Event Name = `my_new_event`
3. Create a **GA4 Event Tag** that fires on this trigger
4. Add the event to GA4 as a "Key Event" if it's a conversion

> **Tell the user**: "To complete the tracking setup, you'll need to add a Custom Event trigger in GTM for `my_new_event` and optionally mark it as a Key Event in GA4."

## Event Naming Conventions

- Use **snake_case**: `league_created`, `steps_submitted`
- Use **past tense verbs**: `submitted`, `created`, `clicked`
- Max 40 characters
- No special prefixes: avoid `ga_`, `firebase_`, `google_`

## Parameter Naming

- Use **snake_case**: `league_id`, `step_count`
- Reuse existing parameters when possible
- Standard parameters: `user_id`, `league_id`, `method`, `category`, `action`, `component`

## User Identification

Handled automatically by `AuthProvider`:

```typescript
// In AuthProvider after login:
identifyUser(user.id, { display_name: user.display_name });

// On logout:
clearUser();
```

## Consent Requirements

Both GTM and PostHog respect the cookie consent banner. Analytics only load after `analytics` category consent is granted.

## PostHog Features Available

- **Session Replay**: Automatically recorded for all consented users
- **Feature Flags**: Use `posthogFeatureFlag('flag-name')` to check flags
- **Funnels**: Configure in PostHog dashboard based on events
- **A/B Testing**: Create experiments in PostHog, check variants with feature flags

## Removing GTM PostHog Tag

After this SDK integration, the "PostHog Tracking" custom HTML tag in GTM should be removed to avoid duplicate tracking.

**Steps:**
1. Go to [GTM](https://tagmanager.google.com/) → Your Container
2. Find "PostHog Tracking" tag (Custom HTML)
3. Delete it
4. Publish new container version

## Troubleshooting

### Events not showing in PostHog
1. Check consent was granted
2. Check `NEXT_PUBLIC_POSTHOG_KEY` is set
3. Check browser console for `[PostHog]` logs in development

### Events not in GA4
1. Check GTM Preview mode to see if events fire
2. Verify GA4 DebugView shows the event
3. Ensure GTM has a tag configured for this event

## Environment Variables

```env
# GA4 via GTM
NEXT_PUBLIC_GTM_ID=GTM-XXXXXXX

# PostHog SDK
NEXT_PUBLIC_POSTHOG_KEY=phc_your_key_here
NEXT_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com
```

## MCP Servers for AI-Assisted Analytics Management

> **For a full list of available MCP servers and project-wide configuration, see [AGENTS.md](../../../AGENTS.md).**

Three MCP servers are configured for managing analytics via AI:

### GTM MCP Server (Stape) ✅ Write Access

**Purpose**: Create, modify, and delete GTM tags, triggers, variables, and containers.

**StepLeague Account**: `6331302038` (StepLeague)

**Capabilities**:
- Create/update/delete tags, triggers, variables
- Manage containers and workspaces
- Audit GTM configuration
- Set up GA4 event tags programmatically
- Preview and publish container versions

**Authentication**: OAuth-based (browser popup on first use)

**Example usages**:
- "List all GTM containers in my account"
- "Create a new GA4 event tag for `league_created` with a custom event trigger"
- "List all tags in the StepLeague container"
- "Get the live version of the container"

### GA4 MCP Server (Stape) 📊 Read-only

**Purpose**: Query GA4 reports and property information.

**StepLeague Property**: `517956149` (StepLeague WebApp, Account: `378957957`)

**Capabilities**:
- Run core reports (page views, sessions, conversions)
- Run realtime reports
- Get account summaries and property details
- List Google Ads links
- Get custom dimensions and metrics

**Authentication**: OAuth-based (browser popup on first use, same as GTM)

**Example usages**:
- "Get my GA4 account summaries"
- "What were my top 10 pages by sessions last week?"
- "Show realtime active users on the site"
- "Run a report of page views for the last 30 days"

### PostHog MCP Server 📊 Full Access

**Purpose**: Manage PostHog analytics, feature flags, experiments, and insights.

**Capabilities**:
- Create/update/query insights and dashboards
- Manage feature flags (create, update, delete)
- Create and monitor A/B test experiments
- Query event data and user analytics
- Manage surveys and actions
- Search PostHog documentation

**Authentication**: API key-based (configured in `.vscode/mcp.json`)

**Example usages**:
- "Get all feature flags in the project"
- "Create a new A/B test for the signup flow"
- "What are my top events in the last 7 days?"
- "Create an insight showing daily active users"

---

## Related Skills

- **`testing-patterns`** - Write tests for analytics events (see `analytics.test.ts` for examples)
- **`auth-patterns`** - User identification flow integrates with analytics
- **`project-updates`** - Document new events in AGENTS.md and CHANGELOG.md
- **`error-handling`** - Track error events alongside regular analytics
- **`social-sharing`** - Share hook patterns and OG image generation
