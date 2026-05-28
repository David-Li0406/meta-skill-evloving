# Analytics Wide Event Patterns

Patterns for product analytics, A/B testing, conversion tracking, and business
metrics using wide events.

## Table of Contents

- [Event Naming Conventions](#event-naming-conventions)
- [Funnel Analytics](#funnel-analytics)
- [A/B Test Instrumentation](#ab-test-instrumentation)
- [Conversion Tracking](#conversion-tracking)
- [Business Metrics](#business-metrics)
- [Cohort Analysis](#cohort-analysis)
- [Query Patterns](#query-patterns)

## Event Naming Conventions

Use consistent, queryable naming:

```
{domain}_{object}_{action}
```

### Examples

| Event Name                  | Domain   | Object       | Action    |
| --------------------------- | -------- | ------------ | --------- |
| `checkout_cart_viewed`      | checkout | cart         | viewed    |
| `checkout_payment_started`  | checkout | payment      | started   |
| `checkout_payment_failed`   | checkout | payment      | failed    |
| `checkout_order_completed`  | checkout | order        | completed |
| `onboarding_step_completed` | onboard  | step         | completed |
| `feature_flag_evaluated`    | platform | feature_flag | evaluated |

### Naming Rules

1. **Use snake_case** - Consistent, queryable
2. **Use past tense for actions** - viewed, started, completed, failed
3. **Be specific** - `checkout_payment_failed` not just `payment_failed`
4. **Include domain prefix** - Enables `WHERE event_name LIKE 'checkout_%'`

## Funnel Analytics

### Funnel Event Structure

```typescript
interface FunnelEvent {
  event_type: "funnel_step";
  timestamp: string;

  // Funnel identification
  funnel_name: string; // e.g., "checkout", "onboarding", "upgrade"
  funnel_id: string; // Unique per funnel attempt
  step_number: number;
  step_name: string;
  step_result: "entered" | "completed" | "abandoned" | "failed";

  // Timing
  step_duration_ms?: number;
  funnel_duration_ms?: number;
  time_since_last_step_ms?: number;

  // Context
  entry_source?: string; // Where user entered funnel
  exit_reason?: string; // Why user abandoned
  error_code?: string;

  // Business context
  cart_value_cents?: number;
  item_count?: number;
  coupon_applied?: string;

  // User context
  user_id?: string;
  session_id: string;
  user_subscription?: string;
  is_first_time?: boolean;
}
```

### Funnel Tracker Implementation

```typescript
class FunnelTracker {
  private funnelId: string;
  private funnelName: string;
  private startTime: number;
  private lastStepTime: number;
  private currentStep: number = 0;

  constructor(funnelName: string, entrySource?: string) {
    this.funnelId = crypto.randomUUID();
    this.funnelName = funnelName;
    this.startTime = Date.now();
    this.lastStepTime = this.startTime;

    this.trackStep("funnel_started", "entered", { entry_source: entrySource });
  }

  advanceStep(stepName: string, metadata?: Record<string, unknown>) {
    this.currentStep++;
    this.trackStep(stepName, "completed", metadata);
    this.lastStepTime = Date.now();
  }

  failStep(
    stepName: string,
    errorCode: string,
    metadata?: Record<string, unknown>,
  ) {
    this.trackStep(stepName, "failed", { error_code: errorCode, ...metadata });
  }

  abandon(stepName: string, reason: string) {
    this.trackStep(stepName, "abandoned", { exit_reason: reason });
  }

  complete(metadata?: Record<string, unknown>) {
    this.trackStep("funnel_completed", "completed", metadata);
  }

  private trackStep(
    stepName: string,
    result: FunnelEvent["step_result"],
    metadata?: Record<string, unknown>,
  ) {
    const now = Date.now();

    sendEvent({
      event_type: "funnel_step",
      timestamp: new Date().toISOString(),
      funnel_name: this.funnelName,
      funnel_id: this.funnelId,
      step_number: this.currentStep,
      step_name: stepName,
      step_result: result,
      step_duration_ms: now - this.lastStepTime,
      funnel_duration_ms: now - this.startTime,
      ...contextManager.getContext(),
      ...metadata,
    });
  }
}

// Usage
const checkoutFunnel = new FunnelTracker("checkout", "product_page");
checkoutFunnel.advanceStep("cart_reviewed", {
  item_count: 3,
  cart_value_cents: 4999,
});
checkoutFunnel.advanceStep("shipping_entered");
checkoutFunnel.advanceStep("payment_entered", { payment_method: "card" });
checkoutFunnel.complete({ order_id: "ord_123", total_cents: 5499 });
```

## A/B Test Instrumentation

### Experiment Event Structure

```typescript
interface ExperimentEvent {
  event_type: "experiment_exposure" | "experiment_conversion";
  timestamp: string;

  // Experiment identification
  experiment_id: string;
  experiment_name: string;
  variant_id: string;
  variant_name: string;

  // Assignment context
  assignment_source: "server" | "client" | "edge";
  assignment_reason?: string; // "random", "override", "sticky"

  // Metrics (for conversion events)
  metric_name?: string;
  metric_value?: number;

  // Context at assignment time
  page_path?: string;
  user_subscription?: string;
  account_age_days?: number;

  // Session
  user_id?: string;
  session_id: string;
  anonymous_id?: string;
}
```

### Experiment Tracker

```typescript
class ExperimentTracker {
  private exposures: Map<string, { variant: string; timestamp: number }> =
    new Map();

  /**
   * Track when a user is exposed to an experiment variant.
   * Call this when the variant affects user experience (not just assignment).
   */
  trackExposure(
    experimentId: string,
    experimentName: string,
    variantId: string,
    variantName: string,
    metadata?: Record<string, unknown>,
  ) {
    // Deduplicate exposures per session
    const key = `${experimentId}:${variantId}`;
    if (this.exposures.has(key)) return;

    this.exposures.set(key, { variant: variantId, timestamp: Date.now() });

    sendEvent({
      event_type: "experiment_exposure",
      timestamp: new Date().toISOString(),
      experiment_id: experimentId,
      experiment_name: experimentName,
      variant_id: variantId,
      variant_name: variantName,
      assignment_source: "client",
      ...contextManager.getContext(),
      ...metadata,
    });
  }

  /**
   * Track a conversion metric for an experiment.
   * Automatically includes all experiments the user was exposed to.
   */
  trackConversion(
    metricName: string,
    metricValue: number = 1,
    metadata?: Record<string, unknown>,
  ) {
    // Track conversion for each active experiment
    for (const [key, exposure] of this.exposures) {
      const [experimentId] = key.split(":");

      sendEvent({
        event_type: "experiment_conversion",
        timestamp: new Date().toISOString(),
        experiment_id: experimentId,
        variant_id: exposure.variant,
        metric_name: metricName,
        metric_value: metricValue,
        time_since_exposure_ms: Date.now() - exposure.timestamp,
        ...contextManager.getContext(),
        ...metadata,
      });
    }
  }
}

export const experiments = new ExperimentTracker();

// Usage
experiments.trackExposure(
  "exp_new_checkout",
  "New Checkout Flow",
  "variant_b",
  "Simplified Form",
);

// Later, when conversion happens
experiments.trackConversion("checkout_completed", 1, {
  order_value_cents: 4999,
});
experiments.trackConversion("revenue_cents", 4999);
```

### Feature Flag Integration

```typescript
// Integration with feature flag SDKs
function evaluateFlag(flagKey: string, defaultValue: boolean): boolean {
  const result = featureFlagClient.evaluate(flagKey, defaultValue);

  // Track as experiment exposure
  experiments.trackExposure(
    `flag_${flagKey}`,
    flagKey,
    result ? "enabled" : "disabled",
    result ? "Treatment" : "Control",
  );

  return result;
}
```

## Conversion Tracking

### Conversion Event Structure

```typescript
interface ConversionEvent {
  event_type: "conversion";
  timestamp: string;

  // Conversion details
  conversion_type: string; // "purchase", "signup", "subscription", "upgrade"
  conversion_id: string;
  conversion_value_cents?: number;
  currency?: string;

  // Attribution
  first_touch_source?: string;
  first_touch_medium?: string;
  first_touch_campaign?: string;
  last_touch_source?: string;
  last_touch_medium?: string;
  last_touch_campaign?: string;
  attribution_window_days?: number;

  // Funnel context
  funnel_id?: string;
  funnel_duration_ms?: number;
  steps_completed?: number;

  // Product context
  product_ids?: string[];
  product_categories?: string[];
  is_first_purchase?: boolean;
  is_subscription?: boolean;

  // User context
  user_id: string;
  user_subscription_before?: string;
  user_subscription_after?: string;
  account_age_days?: number;
  previous_purchases_count?: number;
  lifetime_value_cents?: number;
}
```

### Server-Side Conversion Tracking

```typescript
async function trackConversion(
  userId: string,
  conversionType: string,
  valueCents: number,
  metadata: Record<string, unknown>,
) {
  const user = await getUser(userId);
  const attribution = await getAttribution(userId);

  const event: ConversionEvent = {
    event_type: "conversion",
    timestamp: new Date().toISOString(),
    conversion_type: conversionType,
    conversion_id: crypto.randomUUID(),
    conversion_value_cents: valueCents,
    currency: "USD",

    // Attribution
    first_touch_source: attribution.firstTouch?.source,
    first_touch_medium: attribution.firstTouch?.medium,
    first_touch_campaign: attribution.firstTouch?.campaign,
    last_touch_source: attribution.lastTouch?.source,
    last_touch_medium: attribution.lastTouch?.medium,
    last_touch_campaign: attribution.lastTouch?.campaign,

    // User context
    user_id: userId,
    account_age_days: daysSince(user.createdAt),
    is_first_purchase: user.purchaseCount === 0,
    previous_purchases_count: user.purchaseCount,
    lifetime_value_cents: user.lifetimeValue,

    ...metadata,
  };

  logger.info(event);
}
```

## Business Metrics

### Revenue Events

```typescript
interface RevenueEvent {
  event_type: "revenue";
  timestamp: string;

  // Transaction details
  transaction_id: string;
  transaction_type:
    | "purchase"
    | "subscription"
    | "renewal"
    | "refund"
    | "chargeback";
  gross_amount_cents: number;
  net_amount_cents: number;
  currency: string;
  tax_cents?: number;
  discount_cents?: number;

  // Payment
  payment_method: string;
  payment_provider: string;
  payment_status: "succeeded" | "pending" | "failed";

  // Product
  product_id?: string;
  product_name?: string;
  product_category?: string;
  sku?: string;
  quantity?: number;

  // Subscription specifics
  subscription_id?: string;
  subscription_plan?: string;
  billing_period?: "monthly" | "annual";
  mrr_impact_cents?: number;

  // User
  user_id: string;
  user_subscription?: string;
  is_new_customer?: boolean;
  lifetime_value_cents?: number;
}
```

### Subscription Lifecycle Events

```typescript
interface SubscriptionEvent {
  event_type: "subscription_change";
  timestamp: string;

  // Change details
  change_type:
    | "started"
    | "upgraded"
    | "downgraded"
    | "renewed"
    | "cancelled"
    | "expired"
    | "reactivated"
    | "trial_started"
    | "trial_converted"
    | "trial_expired";

  subscription_id: string;
  plan_before?: string;
  plan_after?: string;
  mrr_before_cents?: number;
  mrr_after_cents?: number;
  mrr_change_cents?: number;

  // Context
  cancellation_reason?: string;
  upgrade_path?: string; // e.g., "free_to_pro", "pro_to_enterprise"
  trial_length_days?: number;
  days_until_renewal?: number;

  // User
  user_id: string;
  account_age_days?: number;
  previous_plans?: string[];
}
```

## Cohort Analysis

### User Properties for Cohorting

```typescript
interface UserProperties {
  // Acquisition cohort
  signup_date: string;
  signup_week: string; // ISO week format
  signup_month: string;
  signup_source: string;
  signup_campaign?: string;

  // Behavioral cohort
  first_purchase_date?: string;
  first_subscription_date?: string;
  activation_date?: string;
  churn_date?: string;

  // Value cohort
  lifetime_value_tier: "low" | "medium" | "high" | "whale";
  purchase_frequency: "one_time" | "occasional" | "frequent" | "power";

  // Engagement cohort
  engagement_level: "dormant" | "casual" | "active" | "power";
  last_active_date: string;
  days_since_active: number;

  // Product cohort
  primary_use_case?: string;
  feature_adoption: string[]; // Features they've used
  subscription_tier: string;
}

function enrichEventWithCohorts(event: Record<string, unknown>, user: User) {
  event.cohort = {
    signup_week: getISOWeek(user.createdAt),
    signup_month: user.createdAt.toISOString().slice(0, 7),
    signup_source: user.acquisitionSource,
    lifetime_value_tier: getValueTier(user.lifetimeValue),
    engagement_level: getEngagementLevel(user),
    days_since_active: daysSince(user.lastActiveAt),
    subscription_tier: user.subscriptionTier,
  };
}
```

## Query Patterns

### Funnel Analysis

```sql
-- Checkout funnel conversion rate by step
SELECT
  step_name,
  step_number,
  COUNT(DISTINCT funnel_id) as attempts,
  COUNT(DISTINCT CASE WHEN step_result = 'completed' THEN funnel_id END) as completions,
  ROUND(100.0 * COUNT(DISTINCT CASE WHEN step_result = 'completed' THEN funnel_id END)
        / COUNT(DISTINCT funnel_id), 2) as conversion_rate
FROM events
WHERE event_type = 'funnel_step'
  AND funnel_name = 'checkout'
  AND timestamp > NOW() - INTERVAL '7 days'
GROUP BY step_name, step_number
ORDER BY step_number;

-- Drop-off analysis
SELECT
  step_name,
  exit_reason,
  COUNT(*) as count
FROM events
WHERE event_type = 'funnel_step'
  AND step_result = 'abandoned'
  AND funnel_name = 'checkout'
GROUP BY step_name, exit_reason
ORDER BY count DESC;
```

### A/B Test Analysis

```sql
-- Experiment results by variant
SELECT
  experiment_name,
  variant_name,
  COUNT(DISTINCT user_id) as users,
  COUNT(DISTINCT CASE WHEN event_type = 'experiment_conversion' THEN user_id END) as conversions,
  ROUND(100.0 * COUNT(DISTINCT CASE WHEN event_type = 'experiment_conversion' THEN user_id END)
        / COUNT(DISTINCT user_id), 2) as conversion_rate,
  SUM(CASE WHEN metric_name = 'revenue_cents' THEN metric_value ELSE 0 END) as total_revenue
FROM events
WHERE experiment_id = 'exp_new_checkout'
GROUP BY experiment_name, variant_name;
```

### Revenue Analysis

```sql
-- Daily revenue by subscription tier
SELECT
  DATE(timestamp) as date,
  user_subscription,
  SUM(gross_amount_cents) / 100.0 as revenue,
  COUNT(DISTINCT transaction_id) as transactions,
  COUNT(DISTINCT user_id) as customers
FROM events
WHERE event_type = 'revenue'
  AND transaction_type IN ('purchase', 'subscription', 'renewal')
  AND timestamp > NOW() - INTERVAL '30 days'
GROUP BY DATE(timestamp), user_subscription
ORDER BY date, revenue DESC;

-- MRR changes
SELECT
  DATE(timestamp) as date,
  change_type,
  SUM(mrr_change_cents) / 100.0 as mrr_change,
  COUNT(*) as changes
FROM events
WHERE event_type = 'subscription_change'
  AND timestamp > NOW() - INTERVAL '30 days'
GROUP BY DATE(timestamp), change_type
ORDER BY date;
```

### Cohort Retention

```sql
-- Weekly cohort retention
WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('week', MIN(timestamp)) as cohort_week
  FROM events
  WHERE event_type = 'page_view'
  GROUP BY user_id
),
activity AS (
  SELECT
    e.user_id,
    c.cohort_week,
    DATE_TRUNC('week', e.timestamp) as activity_week,
    (DATE_TRUNC('week', e.timestamp) - c.cohort_week) / 7 as weeks_since_signup
  FROM events e
  JOIN cohorts c ON e.user_id = c.user_id
  WHERE e.event_type = 'page_view'
)
SELECT
  cohort_week,
  weeks_since_signup,
  COUNT(DISTINCT user_id) as active_users
FROM activity
GROUP BY cohort_week, weeks_since_signup
ORDER BY cohort_week, weeks_since_signup;
```
