# Analytics Architecture

## Patterns


---
  #### **Name**
Event Taxonomy Design
  #### **Description**
Structured naming convention for all events and properties
  #### **When**
Starting analytics implementation or standardizing existing tracking
  #### **Example**
    Format: object_action
    Examples:
      - button_clicked
      - form_submitted
      - page_viewed
      - subscription_upgraded
    
    Properties:
      - Use snake_case
      - Include context: page_path, referrer, user_id
      - Add timestamps: created_at, completed_at
    

---
  #### **Name**
Track Events Not Pageviews
  #### **Description**
Event-based tracking captures user behavior better than pageviews
  #### **When**
Implementing analytics for modern web apps
  #### **Example**
    // Bad: Only pageview tracking
    trackPageview('/dashboard');
    
    // Good: Meaningful events
    track('dashboard_viewed', { section: 'overview' });
    track('metric_card_clicked', { metric: 'mrr' });
    track('filter_applied', { filter_type: 'date_range' });
    

---
  #### **Name**
User Identification Flow
  #### **Description**
Proper user identification and aliasing across anonymous → authenticated
  #### **When**
Implementing user tracking in authentication flows
  #### **Example**
    // 1. Anonymous user
    analytics.identify(anonymousId);
    
    // 2. User signs up
    analytics.alias(userId, anonymousId);
    analytics.identify(userId, {
      email, name, plan
    });
    
    // 3. All future events
    analytics.track('feature_used', { feature: 'export' });
    

---
  #### **Name**
Funnel Tracking with Entry Points
  #### **Description**
Track funnel steps with clear entry points for analysis
  #### **When**
Implementing conversion funnel tracking
  #### **Example**
    // Track where users entered funnel
    track('signup_started', {
      entry_point: 'hero_cta' | 'pricing_page' | 'blog_post',
      source: utm_source,
      medium: utm_medium
    });
    
    track('signup_step_completed', { step: 2, method: 'email' });
    track('signup_completed', { plan: 'pro' });
    

---
  #### **Name**
Privacy-First Implementation
  #### **Description**
Respect user privacy and regulatory requirements from day one
  #### **When**
Implementing any analytics system
  #### **Example**
    // Respect DNT header
    if (navigator.doNotTrack === '1') return;
    
    // Allow opt-out
    if (userHasOptedOut()) return;
    
    // Anonymize IP addresses
    analytics.load('key', { ip: false });
    
    // Don't track PII unless explicitly consented
    track('purchase', { amount, currency }); // Good
    // Never: { email, address, ssn }
    

---
  #### **Name**
Experimentation Schema
  #### **Description**
Track experiments with variant exposure
  #### **When**
Running A/B tests or feature flags
  #### **Example**
    // On variant assignment
    track('experiment_viewed', {
      experiment_id: 'new_checkout_flow',
      variant: 'control' | 'variant_a',
      user_id,
      timestamp
    });
    
    // On conversion
    track('experiment_converted', {
      experiment_id: 'new_checkout_flow',
      variant: 'variant_a'
    });
    

## Anti-Patterns


---
  #### **Name**
Track Everything Everywhere
  #### **Description**
Instrumenting every possible event without clear questions
  #### **Why**
Data overload, expensive, hard to find signal in noise
  #### **Instead**
    Start with key questions you need answered.
    Track events that inform decisions.
    Add tracking when you realize you need data.
    

---
  #### **Name**
Inconsistent Event Names
  #### **Description**
No naming standard, events named differently by different devs
  #### **Why**
Cannot aggregate similar events, analysis nightmare
  #### **Instead**
    Document taxonomy. Code review tracking changes.
    Use constants: EVENTS.BUTTON_CLICKED not 'button clicked'.
    Generate types from schema for type safety.
    

---
  #### **Name**
Missing Context Properties
  #### **Description**
Events without enough context to answer questions
  #### **Why**
Cannot segment or understand behavior without context
  #### **Instead**
    Always include: user_id, session_id, timestamp, page_path.
    Add business context: plan_type, feature_flags_enabled.
    Consider future questions, not just current needs.
    

---
  #### **Name**
Client-Side Only Tracking
  #### **Description**
All analytics events tracked only from client
  #### **Why**
Ad blockers, client errors, bot traffic skew data
  #### **Instead**
    Critical events (signup, purchase) tracked server-side.
    Client events for UX interactions.
    Reconcile both sources for accuracy.
    

---
  #### **Name**
No Event Validation
  #### **Description**
Shipping tracking without testing it actually works
  #### **Why**
Silent failures mean missing data you cannot recover
  #### **Instead**
    Test in development with analytics debuggers.
    Monitor event volumes and alert on drops.
    Validate schema on every event send.
    

---
  #### **Name**
Ignoring Bot Traffic
  #### **Description**
Not filtering bot and crawler traffic from analytics
  #### **Why**
Inflated metrics, wrong decisions based on fake users
  #### **Instead**
    Filter known bots (User-Agent).
    Anomaly detection for bot-like behavior.
    Separate dashboards for all traffic vs. human traffic.
    