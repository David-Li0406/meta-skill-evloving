# Segment Cdp - Sharp Edges

## Anonymous ID Persists Until Explicit Reset

### **Id**
anonymous-id-persistence
### **Severity**
medium
### **Description**
  Analytics.js generates an anonymousId on first page load and persists it
  in localStorage. This ID survives across sessions and even browser restarts.
  After logout, the previous user's anonymous history can merge with the
  next user if you don't reset.
  
### **Wrong Way**
  // User logs out but anonymous ID stays
  async function handleLogout() {
    await signOut();
    router.push('/login');
    // BUG: Next user who logs in will inherit
    // the previous user's anonymous tracking history!
  }
  
  // User B logs in on User A's device
  async function handleLogin(userId) {
    await signIn(userId);
    analytics.identify(userId);  // Merges A's history with B!
  }
  
### **Right Way**
  // Reset analytics on logout
  async function handleLogout() {
    await signOut();
  
    // Reset Segment state
    analytics.reset();  // Clears anonymousId and user traits
  
    router.push('/login');
  }
  
  // Clean login flow
  async function handleLogin(userId) {
    // Reset first in case previous user
    analytics.reset();
  
    await signIn(userId);
  
    // Fresh identify for this user
    analytics.identify(userId, {
      email: user.email,
    });
  }
  
### **Detection Patterns**
  - signOut.*(?!.*reset)
  - logout.*(?!.*analytics\.reset)
### **References**
  - https://segment.com/docs/connections/sources/catalog/libraries/website/javascript/#reset-or-logout

## Device Mode Bypasses Protocols Blocking

### **Id**
device-mode-blocking
### **Severity**
high
### **Description**
  Segment's Protocols can block non-conforming events, but this only works
  in cloud mode. Device-mode destinations (loaded in browser) receive events
  directly and bypass blocking. Mobile device-mode also bypasses blocking.
  
### **Wrong Way**
  // Relying on Protocols to block bad data
  // But using device-mode destinations...
  
  // In Segment UI:
  // Mixpanel: Device Mode ✓
  // Amplitude: Device Mode ✓
  
  // Bad events still reach these destinations!
  analytics.track('Invalid Event That Should Be Blocked', {
    missing: 'required_fields',
  });
  
### **Right Way**
  // 1. Use cloud-mode destinations when possible
  // In Segment UI, disable device mode for destinations
  
  // 2. Implement client-side validation
  function validateEvent(event: string, properties: object): boolean {
    // Validate against your tracking plan
    const schema = trackingPlan[event];
    if (!schema) {
      console.warn(`Unknown event: ${event}`);
      return false;
    }
  
    for (const required of schema.required) {
      if (!(required in properties)) {
        console.warn(`Missing required property: ${required}`);
        return false;
      }
    }
  
    return true;
  }
  
  function safeTrack(event: string, properties: object) {
    if (!validateEvent(event, properties)) {
      // Log violation locally
      console.error('Tracking plan violation', { event, properties });
      return;
    }
  
    analytics.track(event, properties);
  }
  
### **Detection Patterns**
  - analytics\.track(?!.*validate)
### **References**
  - https://segment.com/docs/protocols/

## HTTP API Has Strict Size Limits

### **Id**
batch-size-limits
### **Severity**
medium
### **Description**
  The HTTP API has size limits:
  - 32 KB per individual API request
  - 500 KB per batch request
  - 32 KB per event within a batch
  
  Large properties (like full page content) will fail silently or error.
  
### **Wrong Way**
  // Sending too much data
  analytics.track('Content Viewed', {
    page_content: document.body.innerHTML,  // Could be > 32KB!
    full_response: await fetch('/api/data').then(r => r.json()),  // Large
  });
  
  // Batch with too many events
  await httpBatch(thousandsOfEvents);  // May exceed 500KB
  
### **Right Way**
  // Limit property sizes
  function truncateString(str: string, maxLength: number = 1000): string {
    return str.length > maxLength ? str.slice(0, maxLength) + '...' : str;
  }
  
  analytics.track('Content Viewed', {
    page_title: document.title,
    page_url: window.location.href,
    // Send summary, not full content
    content_preview: truncateString(document.body.innerText, 500),
    word_count: document.body.innerText.split(/\s+/).length,
  });
  
  // Chunk batch requests
  async function batchTrack(events: any[]) {
    const BATCH_SIZE = 100;  // Stay well under limits
    const chunks = [];
  
    for (let i = 0; i < events.length; i += BATCH_SIZE) {
      chunks.push(events.slice(i, i + BATCH_SIZE));
    }
  
    for (const chunk of chunks) {
      await httpBatch(chunk);
    }
  }
  
### **Detection Patterns**
  - innerHTML|innerText.*analytics
  - JSON\.stringify.*analytics
### **References**
  - https://segment.com/docs/connections/sources/catalog/libraries/server/http-api/#max-request-size

## Track Calls Without Identify Are Anonymous

### **Id**
identify-before-track
### **Severity**
high
### **Description**
  If you call track() before identify(), events are associated with
  anonymousId only. After identify(), events link to userId, but
  previous anonymous events may not merge in all destinations.
  
### **Wrong Way**
  // User takes actions before logging in
  analytics.track('Product Viewed', { product_id: '123' });
  analytics.track('Added to Cart', { product_id: '123' });
  
  // Later, user signs up
  analytics.identify(userId, { email });
  analytics.track('Signed Up');
  
  // The Product Viewed and Added to Cart events
  // may not be attributed to this user in some destinations!
  
### **Right Way**
  // Track anonymous events (they'll have anonymousId)
  analytics.track('Product Viewed', { product_id: '123' });
  analytics.track('Added to Cart', { product_id: '123' });
  
  // On signup, identify first
  async function handleSignup(user) {
    // Identify merges anonymous history with user
    analytics.identify(user.id, {
      email: user.email,
      created_at: new Date().toISOString(),
    });
  
    // Then track signup event
    analytics.track('Signed Up', {
      signup_method: 'email',
    });
  
    // Some destinations need explicit alias for full merge
    // (check destination documentation)
    analytics.alias(user.id);
  }
  
  // For destinations that need it, also call from server
  // to ensure merge happens
  serverIdentify(userId, traits);
  
### **Detection Patterns**
  - track.*\n.*identify
### **References**
  - https://segment.com/docs/connections/spec/identify/

## Write Key in Client is Visible (But Intentional)

### **Id**
write-key-exposure
### **Severity**
low
### **Description**
  The write key in Analytics.js is visible in browser source.
  This is by design - write keys are meant for sending data, not reading.
  However, attackers could send fake events. Use server-side validation
  for critical business events.
  
### **Wrong Way**
  // Trusting client-side revenue tracking
  analytics.track('Purchase Completed', {
    revenue: 999999,  // User could modify this in console!
    order_id: 'fake_order',
  });
  
  // Trusting for subscription status
  analytics.identify(userId, {
    plan: 'enterprise',  // User claims enterprise!
  });
  
### **Right Way**
  // Track revenue server-side from webhook/database
  // app/api/webhooks/stripe/route.ts
  export async function POST(req) {
    const event = await req.json();
  
    if (event.type === 'checkout.session.completed') {
      // Server-side - can't be faked
      serverTrack(
        event.data.object.client_reference_id,
        'Purchase Completed',
        {
          revenue: event.data.object.amount_total / 100,
          order_id: event.data.object.id,
        }
      );
    }
  }
  
  // Server-side identify from auth system
  async function updateUserPlan(userId: string, plan: string) {
    await db.user.update({ where: { id: userId }, data: { plan }});
  
    // Server-side identify - trusted
    serverIdentify(userId, {
      plan,
      plan_updated_at: new Date().toISOString(),
    });
  }
  
### **Detection Patterns**
  - analytics\.track.*revenue|purchase|payment
  - analytics\.identify.*plan.*enterprise|premium
### **References**
  - https://segment.com/docs/connections/sources/catalog/libraries/website/javascript/#security

## Events May Be Lost on Page Navigation

### **Id**
flushing-on-page-unload
### **Severity**
medium
### **Description**
  Analytics.js batches events and sends them asynchronously.
  If user navigates away before flush, events can be lost.
  Use sendBeacon API or flush before navigation.
  
### **Wrong Way**
  // User clicks link immediately after action
  function handleCheckoutClick() {
    analytics.track('Checkout Started');  // Might not send!
    window.location.href = '/checkout';  // Navigates immediately
  }
  
### **Right Way**
  // Option 1: Wait for track to complete
  async function handleCheckoutClick() {
    await analytics.track('Checkout Started');
    window.location.href = '/checkout';
  }
  
  // Option 2: Use sendBeacon for navigation events
  function trackWithBeacon(event: string, properties: object) {
    const payload = JSON.stringify({
      type: 'track',
      event,
      properties,
      userId: analytics.user().id(),
      anonymousId: analytics.user().anonymousId(),
      timestamp: new Date().toISOString(),
    });
  
    navigator.sendBeacon(
      'https://api.segment.io/v1/track',
      new Blob([payload], { type: 'application/json' })
    );
  }
  
  // Option 3: Flush before unload
  window.addEventListener('beforeunload', () => {
    analytics.flush();
  });
  
  // Option 4: For Next.js router
  import { useRouter } from 'next/navigation';
  
  function useTrackNavigation() {
    const router = useRouter();
  
    return async (event: string, properties: object, href: string) => {
      await analytics.track(event, properties);
      router.push(href);
    };
  }
  
### **Detection Patterns**
  - track.*location\.href
  - track.*router\.push
  - track.*window\.location
### **References**
  - https://segment.com/docs/connections/sources/catalog/libraries/website/javascript/#batching

## Timestamps Without Timezone Cause Analytics Issues

### **Id**
timestamp-timezone-issues
### **Severity**
medium
### **Description**
  If you send timestamps without timezone info, Segment assumes UTC.
  But your destinations might interpret them in local time, causing
  off-by-hours issues in daily reports.
  
### **Wrong Way**
  // Ambiguous timestamp
  analytics.track('Order Placed', {
    order_time: '2024-01-15 14:30:00',  // What timezone?
  });
  
  // Using local date without ISO format
  analytics.track('Event', {
    created: new Date().toString(),  // "Mon Jan 15 2024 14:30:00 GMT-0800"
  });
  
### **Right Way**
  // Always use ISO 8601 with timezone
  analytics.track('Order Placed', {
    order_time: new Date().toISOString(),  // "2024-01-15T22:30:00.000Z"
  });
  
  // Or explicit timezone offset
  analytics.track('Order Placed', {
    order_time: '2024-01-15T14:30:00-08:00',  // Clear timezone
  });
  
  // For server-side, always use UTC
  serverTrack(userId, 'Order Placed', {
    order_time: new Date().toISOString(),
    user_local_time: userTimezone ? formatInTimeZone(new Date(), userTimezone) : undefined,
  });
  
### **Detection Patterns**
  - new Date\(\)\.toString\(\)
  - \d{4}-\d{2}-\d{2} \d{2}:\d{2}(?!.*[+-]\d{2})
### **References**
  - https://segment.com/docs/connections/spec/common/#timestamps

## Tracking Before Consent Violates GDPR

### **Id**
gdpr-consent-tracking
### **Severity**
high
### **Description**
  Analytics.js loads and starts tracking immediately.
  For GDPR compliance, you must delay loading until consent.
  Use Segment's consent management or load conditionally.
  
### **Wrong Way**
  // Analytics.js in <head> - tracks before consent
  <script>
    !function(){/* segment snippet */}();
    analytics.load('WRITE_KEY');
    analytics.page();  // Tracking immediately!
  </script>
  
  // Cookie banner shows but tracking already happened
  
### **Right Way**
  // Option 1: Conditional loading
  function loadAnalytics() {
    if (hasUserConsent()) {
      analytics.load('WRITE_KEY');
      analytics.page();
    }
  }
  
  // Show consent UI first, then load
  function handleConsentAccept() {
    saveConsentPreference(true);
    loadAnalytics();
  }
  
  // Option 2: Use Segment's consent wrapper
  import { createWrapper } from '@segment/analytics-consent-wrapper-onetrust';
  
  const wrapper = createWrapper();
  analytics.load('WRITE_KEY', { wrapper });
  
  // Option 3: Load disabled, enable on consent
  analytics.load('WRITE_KEY', {
    integrations: {
      'Segment.io': false,  // Disabled by default
    },
  });
  
  function onConsent() {
    // Enable tracking after consent
    analytics.identify(userId, traits, {
      integrations: { 'Segment.io': true },
    });
  }
  
### **Detection Patterns**
  - analytics\.load.*analytics\.page(?!.*consent)
  - analytics\.load(?!.*wrapper|consent)
### **References**
  - https://segment.com/docs/privacy/consent-management/