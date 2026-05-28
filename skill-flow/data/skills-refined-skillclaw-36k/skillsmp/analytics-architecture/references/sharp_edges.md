# Analytics Architecture - Sharp Edges

## Schema Less Tracking

### **Id**
schema-less-tracking
### **Summary**
Tracking events without a defined schema
### **Severity**
high
### **Situation**
  Everyone adds events. No naming convention. No property documentation.
  "button_click", "ButtonClick", "click_button" - all the same thing?
  Who knows. Data is unusable.
  
### **Why**
  Without a schema, events become inconsistent. Analysis becomes impossible.
  You'll have to clean up years of bad data or start over. Schema-first
  is cheaper than schema-never.
  
### **Solution**
  # Define tracking schema first:
  ```typescript
  // tracking-schema.ts
  export const events = {
    signupStarted: {
      name: 'signup_started',
      properties: {
        source: 'string',
        campaign: 'string?',
      },
    },
    signupCompleted: {
      name: 'signup_completed',
      properties: {
        userId: 'string',
        method: 'email' | 'google' | 'github',
      },
    },
  } as const;
  ```
  
  # Naming conventions:
  - snake_case for event names
  - past tense for completed actions
  - Noun + Verb pattern: signup_completed, payment_failed
  
  # Enforce with types:
  ```typescript
  function track<E extends keyof typeof events>(
    event: E,
    props: typeof events[E]['properties']
  ) { ... }
  ```
  
### **Symptoms**
  - Different naming conventions
  - No event documentation
  - What does this event mean?
  - Cannot reproduce analytics locally
### **Detection Pattern**


## Frontend Only Tracking

### **Id**
frontend-only-tracking
### **Summary**
Only tracking events from frontend
### **Severity**
high
### **Situation**
  All events from browser. User blocks JavaScript. Ad blocker installed.
  Incognito mode. 20-40% of your data is missing. Funnels don't add up.
  
### **Why**
  Frontend tracking is lossy. Ad blockers, privacy extensions, and network
  failures all cause data loss. Critical events should be tracked server-side
  where you have full control.
  
### **Solution**
  # Critical events server-side:
  - Payment completed
  - Signup completed
  - Subscription changed
  - Any irreversible action
  
  # Frontend for:
  - UI interactions
  - Navigation
  - Feature usage
  - Non-critical events
  
  # Hybrid approach:
  ```typescript
  // Server-side (reliable)
  await analytics.track({
    userId: user.id,
    event: 'payment_completed',
    properties: { amount: 99, plan: 'pro' },
  });
  
  // Client-side (best effort)
  analytics.track('pricing_page_viewed');
  ```
  
  # Segment server-side:
  Use analytics-node or HTTP API
  
### **Symptoms**
  - All events from client
  - 20%+ drop-off that doesn't make sense
  - Payment events don't match Stripe
  - Missing events from mobile app
### **Detection Pattern**


## Pii In Events

### **Id**
pii-in-events
### **Summary**
Tracking personally identifiable information in events
### **Severity**
critical
### **Situation**
  Email addresses in event properties. Phone numbers in user traits.
  IP addresses logged everywhere. GDPR request comes in. Can't delete.
  Compliance violation.
  
### **Why**
  Analytics data is hard to delete. PII in analytics creates privacy liability.
  GDPR/CCPA require ability to delete user data. If it's sprayed across
  event properties, you can't comply.
  
### **Solution**
  # Never track:
  - Email addresses
  - Phone numbers
  - Full names
  - IP addresses (usually)
  - Location (precise)
  - Any government ID
  
  # Use anonymous identifiers:
  ```typescript
  // BAD
  analytics.track('signup', { email: 'user@example.com' });
  
  // GOOD
  analytics.identify(userId);  // Anonymous ID
  analytics.track('signup', { method: 'email' });
  ```
  
  # Traits vs Properties:
  PII can go in identify() (can be deleted)
  Never in track() properties
  
  # Implement deletion:
  When user requests deletion,
  Delete from identify/user data
  Events stay (anonymized)
  
### **Symptoms**
  - Email/phone in event properties
  - Can't handle deletion requests
  - No PII audit of tracking
### **Detection Pattern**
track\([^)]*email|track\([^)]*phone

## Missing User Identification

### **Id**
missing-user-identification
### **Summary**
Not properly linking anonymous to known users
### **Severity**
high
### **Situation**
  User browses anonymously. Signs up. Anonymous history is lost. Can't
  see full funnel from first visit to signup to payment. Attribution broken.
  
### **Why**
  Users are anonymous before signup. If you don't link their anonymous ID
  to their user ID, you lose the pre-signup journey. This breaks attribution
  and funnel analysis.
  
### **Solution**
  # The identify flow:
  ```typescript
  // 1. Anonymous tracking (auto ID)
  analytics.track('pricing_viewed');
  
  // 2. On signup, alias + identify
  analytics.alias(userId);  // Links anonymous to user
  analytics.identify(userId, {
    createdAt: new Date(),
    plan: 'free',
  });
  
  // 3. Future events have full history
  analytics.track('feature_used');
  ```
  
  # Key moments to identify:
  - Signup completion
  - Login
  - Any authenticated action
  
  # Reset on logout:
  ```typescript
  analytics.reset();  // New anonymous ID
  ```
  
### **Symptoms**
  - Pre-signup journey missing
  - Can't attribute signups to campaigns
  - Anonymous and known users seem different
### **Detection Pattern**


## Attribution Oversimplification

### **Id**
attribution-oversimplification
### **Summary**
Using last-click attribution for everything
### **Severity**
medium
### **Situation**
  User sees ad. Comes back via blog. Signs up from email. Last-click says
  email gets credit. Ad budget cut. Growth drops.
  
### **Why**
  Last-click attribution is simple but wrong. It credits the last touch,
  ignoring the journey. Multi-touch attribution is harder but necessary
  for real understanding.
  
### **Solution**
  # Track the full journey:
  ```typescript
  // Store first touch
  const firstTouch = localStorage.getItem('first_touch') ||
    storeFirstTouch({ source, campaign, medium });
  
  // Store last touch
  const lastTouch = { source, campaign, medium, timestamp };
  
  // On conversion, send both
  analytics.track('signup_completed', {
    firstTouch,
    lastTouch,
    touchCount: getTouchCount(),
  });
  ```
  
  # UTM parameters:
  Always capture and store:
  - utm_source
  - utm_medium
  - utm_campaign
  - utm_content
  - utm_term
  
  # Attribution models:
  - First touch: Awareness credit
  - Last touch: Conversion credit
  - Linear: Equal credit
  - Time decay: Recent weighted
  
### **Symptoms**
  - Only last click stored
  - No first touch attribution
  - Marketing channels fight for credit
  - Can't see full funnel
### **Detection Pattern**


## Funnel Definition Drift

### **Id**
funnel-definition-drift
### **Summary**
Funnel definitions changing over time, breaking trends
### **Severity**
high
### **Situation**
  Funnel step renamed. Query updated. Historical comparison broken.
  "Did we improve or did the definition change?" No one knows.
  
### **Why**
  Funnels are comparisons over time. If definitions change, comparisons
  are meaningless. You're comparing apples to oranges. Historical analysis
  requires stable definitions.
  
### **Solution**
  # Version your definitions:
  ```typescript
  // funnels.ts
  export const signupFunnel = {
    version: '2024-01',
    steps: [
      { event: 'landing_page_viewed' },
      { event: 'signup_started' },
      { event: 'email_verified' },
      { event: 'onboarding_completed' },
    ],
  };
  ```
  
  # When changing:
  - Keep old version for historical
  - Create new version for new analysis
  - Document the change
  
  # In analysis:
  Always note which funnel version
  Don't compare across versions
  
### **Symptoms**
  - Funnel definitions in wiki/docs only
  - The number looks different now
  - Historical trends meaningless
### **Detection Pattern**


## Sampling Without Awareness

### **Id**
sampling-without-awareness
### **Summary**
Using sampled data without accounting for it
### **Severity**
medium
### **Situation**
  Analytics tool samples data at 10%. "We had 1000 signups!" Actually 10,000.
  Decisions made on wrong numbers. Budgets wrong. Forecasts broken.
  
### **Why**
    High-volume analytics tools sample by default. If you don't know you're
  looking at sampled data, your numbers are 10x off. Some analyses don't
  work with sampled data at all.
  
### **Solution**
  # Know your sampling:
  - Google Analytics 4: Samples at high volume
  - Mixpanel: Samples on free tier
  - Amplitude: Samples on high volume
  
  # For exact counts:
  - Track critical events server-side
  - Use data warehouse for exact queries
  - Pay for unsampled data if needed
  
  # When presenting:
  Always note if data is sampled
  Extrapolate carefully
  
### **Symptoms**
  - Numbers don't match between tools
  - Unaware of sampling thresholds
  - The analytics are wrong
### **Detection Pattern**


## Event Bloat

### **Id**
event-bloat
### **Summary**
Tracking too many events without hierarchy
### **Severity**
medium
### **Situation**
  500 events tracked. Most never queried. Analytics bill growing. When
  you need insight, you can't find the right event. Noise drowns signal.
  
### **Why**
  More events isn't better. Each event is maintenance burden, cost, and
  complexity. The marginal event is usually not worth it. Track what you'll
  actually analyze.
  
### **Solution**
  # Event hierarchy:
  - Critical (5-10): Core user actions
  - Important (20-30): Key feature usage
  - Nice-to-have: Track if needed
  
  # Before adding an event:
  1. What question will this answer?
  2. How often will we query it?
  3. Can we derive this from existing events?
  
  # Regular audit:
  - Which events are never queried?
  - Which events are redundant?
  - Archive or remove unused
  
  # Event budgeting:
  Set max number of events
  Force prioritization
  
### **Symptoms**
  - 100+ events tracked
  - No idea what most events mean
  - Analytics costs growing fast
  - Can't find the right event
### **Detection Pattern**


## Session Definition Mismatch

### **Id**
session-definition-mismatch
### **Summary**
Different tools defining sessions differently
### **Severity**
medium
### **Situation**
  Google Analytics says 50,000 sessions. Mixpanel says 30,000. Amplitude
  says 40,000. Which is right? None. They define sessions differently.
  
### **Why**
  Session is not a standard concept. Each tool has different timeout,
  different session start rules, different handling of tabs. Comparing
  sessions across tools is meaningless.
  
### **Solution**
  # Know your tool's session rules:
  - GA4: 30 min inactivity timeout
  - Mixpanel: 30 min by default, configurable
  - Amplitude: Configurable
  
  # Custom session tracking:
  ```typescript
  // Define your own session logic
  const SESSION_TIMEOUT = 30 * 60 * 1000; // 30 min
  function getOrCreateSession() {
    const stored = sessionStorage.getItem('session');
    if (stored && Date.now() - stored.lastActive < SESSION_TIMEOUT) {
      return stored.id;
    }
    return createNewSession();
  }
  ```
  
  # When comparing:
  Use same tool for apples-to-apples
  Or use custom session ID everywhere
  
### **Symptoms**
  - Session counts don't match across tools
  - "Our sessions went up/down" but not really
  - Confusion about what a session means
### **Detection Pattern**


## No Analytics Testing

### **Id**
no-analytics-testing
### **Summary**
Not testing that analytics events actually fire
### **Severity**
high
### **Situation**
  Shipped new feature. Tracking code looks right. 2 weeks later, realize events never fired. Lost 2 weeks of data. Can't analyze launch impact.
  
### **Why**
  Analytics code breaks silently. No errors, just missing data. If you
  don't test that events fire, you won't know until it's too late.
  
### **Solution**
  # Before shipping:
  - Open browser dev tools
  - Check network tab for analytics calls
  - Verify payload is correct
  
  # Automated testing:
  ```typescript
  // Mock analytics in tests
  const mockTrack = jest.fn();
  analytics.track = mockTrack;
  
  // Perform action
  fireEvent.click(signupButton);
  
  // Verify event
  expect(mockTrack).toHaveBeenCalledWith(
    'signup_started',
    expect.objectContaining({ source: 'pricing_page' })
  );
  ```
  
  # Real-time debugging:
  - Segment debugger
  - PostHog toolbar
  - Mixpanel live view
  
### **Symptoms**
  - The events stopped working
  - Missing data discovered weeks later
  - No analytics tests in CI
### **Detection Pattern**


## Metric Definition Ambiguity

### **Id**
metric-definition-ambiguity
### **Summary**
Key metrics defined differently by different people
### **Severity**
medium
### **Situation**
  CEO asks for DAU. Marketing says 50,000. Product says 30,000. Engineering
  says 40,000. All are "right" with different definitions. Chaos.
  
### **Why**
    Metrics without definitions are meaningless. "Active" means different things
  to different people. Without a single source of truth, everyone is right
  and everyone is wrong.
  
### **Solution**
  # Central metric definitions:
  ```markdown
  # metrics.md
  
  ## Daily Active Users (DAU)
  Definition: Unique users who performed at least one core action in a day
  Core actions: login, create, edit, purchase
  NOT included: page views only, password reset
  
  ## Monthly Recurring Revenue (MRR)
  Definition: Sum of all active subscriptions, normalized to monthly
  Includes: All paid plans
  Excludes: One-time payments, usage overages
  ```
  
  # Single source of truth:
  - One person owns each metric definition
  - Changes require explicit update
  - Dashboards reference the definition
  
  # When asked for a metric:
  "Here's DAU by the standard definition. That definition is: [...]"
  
### **Symptoms**
  - Different numbers for same metric
  - What does active mean?
  - Debates about correct number
### **Detection Pattern**
