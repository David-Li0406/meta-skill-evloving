---
name: fullstory-analytics-events-web
version: v3
platform: web
sdk: fullstory-browser
description: JavaScript/TypeScript implementation guide for Fullstory's Analytics Events API. Includes API reference, code examples, and common patterns for web applications.
parent_skill: fullstory-analytics-events
related_skills:
  - fullstory-analytics-events
  - fullstory-page-properties
  - fullstory-user-properties
---

# Fullstory Analytics Events — Web Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for event naming, property types, and best practices.
>
> **Other Platforms**: See [SKILL-MOBILE.md](./SKILL-MOBILE.md) for iOS, Android, Flutter, React Native.

---

## API Reference

### Basic Syntax

```javascript
FS('trackEvent', {
  name: string,          // Required: Event name (max 250 chars)
  properties: object,    // Required: Event properties (max 512KB)
  schema?: object        // Optional: Type hints for properties
});
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | **Yes** | Event name, max 250 characters |
| `properties` | object | **Yes** | Key/value pairs of event data |
| `schema` | object | No | Explicit type inference for properties |

### Async Version

For cases where you need confirmation the event was sent:

```javascript
try {
  await FS('trackEventAsync', {
    name: 'Order Completed',
    properties: {
      order_id: order.id,
      revenue: order.total
    }
  });
  console.log('Event sent successfully');
} catch (error) {
  console.error('Event failed:', error);
  // Fallback: queue for retry
}
```

---

## ✅ GOOD Implementation Examples

### Example 1: E-commerce — Product Added to Cart

```javascript
// GOOD: Comprehensive product add event
function handleAddToCart(product, quantity, source) {
  FS('trackEvent', {
    name: 'Product Added',
    properties: {
      // Product identification
      product_id: product.id,
      sku: product.sku,
      name: product.name,
      brand: product.brand,
      
      // Categorization
      category: product.category,
      subcategory: product.subcategory,
      
      // Pricing
      price: product.price,
      currency: 'USD',
      
      // Cart context
      quantity: quantity,
      cart_id: getCartId(),
      
      // Attribution
      position: product.listPosition,
      list_name: source.listName,
      
      // Product attributes
      variant: product.selectedVariant,
      size: product.selectedSize,
      color: product.selectedColor,
      
      // Promotion tracking
      coupon: getActiveCoupon(),
      
      // URLs for reference
      url: product.url,
      image_url: product.imageUrl
    },
    schema: {
      price: 'real',
      quantity: 'int',
      position: 'int'
    }
  });
}
```

**Why this is good:**
- ✅ Follows standard e-commerce event naming
- ✅ Includes product identification (id, sku)
- ✅ Captures pricing with currency
- ✅ Includes attribution context (position, list)
- ✅ Proper typing for numeric fields

### Example 2: SaaS — Feature Usage Tracking

```javascript
// GOOD: Track feature usage with context
function trackFeatureUsage(featureName, context = {}) {
  FS('trackEvent', {
    name: 'Feature Used',
    properties: {
      // Feature identification
      feature_name: featureName,
      feature_category: getFeatureCategory(featureName),
      
      // Usage context
      usage_context: context.trigger || 'direct',
      entry_point: context.entryPoint || window.location.pathname,
      
      // User's feature state
      is_first_use: !hasUsedFeature(featureName),
      times_used_today: getDailyUsageCount(featureName),
      times_used_total: getTotalUsageCount(featureName),
      
      // Session context
      session_feature_count: getSessionFeatureCount(),
      time_in_session: getTimeInSession(),
      
      // Feature-specific data
      ...context.metadata
    },
    schema: {
      is_first_use: 'bool',
      times_used_today: 'int',
      times_used_total: 'int',
      session_feature_count: 'int',
      time_in_session: 'int'
    }
  });
}

// Usage
trackFeatureUsage('advanced_export', {
  trigger: 'keyboard_shortcut',
  entryPoint: '/dashboard',
  metadata: {
    export_format: 'csv',
    row_count: 1500
  }
});
```

**Why this is good:**
- ✅ Tracks both feature and context
- ✅ Captures first-use for adoption analysis
- ✅ Includes frequency metrics
- ✅ Flexible metadata for feature-specific data

### Example 3: Subscription/Billing Events

```javascript
// GOOD: Track subscription lifecycle events
class SubscriptionTracker {
  
  trackTrialStarted(trial) {
    FS('trackEvent', {
      name: 'Trial Started',
      properties: {
        trial_plan: trial.plan,
        trial_duration_days: trial.durationDays,
        trial_features: trial.includedFeatures,
        source: trial.acquisitionSource,
        started_at: new Date().toISOString()
      },
      schema: {
        trial_duration_days: 'int',
        trial_features: 'strs',
        started_at: 'date'
      }
    });
  }
  
  trackSubscriptionStarted(subscription) {
    FS('trackEvent', {
      name: 'Subscription Started',
      properties: {
        plan_name: subscription.plan,
        plan_tier: subscription.tier,
        billing_cycle: subscription.billingCycle,
        price: subscription.price,
        currency: subscription.currency,
        seats: subscription.seats,
        mrr: subscription.mrr,
        arr: subscription.arr,
        trial_converted: subscription.wasTrialing,
        payment_method: subscription.paymentMethod,
        promo_code: subscription.promoCode
      },
      schema: {
        price: 'real',
        seats: 'int',
        mrr: 'real',
        arr: 'real',
        trial_converted: 'bool'
      }
    });
  }
  
  trackPlanChanged(change) {
    FS('trackEvent', {
      name: 'Plan Changed',
      properties: {
        from_plan: change.fromPlan,
        to_plan: change.toPlan,
        from_price: change.fromPrice,
        to_price: change.toPrice,
        price_change: change.toPrice - change.fromPrice,
        change_type: change.toPrice > change.fromPrice ? 'upgrade' : 'downgrade',
        from_seats: change.fromSeats,
        to_seats: change.toSeats,
        effective_date: change.effectiveDate,
        reason: change.reason
      },
      schema: {
        from_price: 'real',
        to_price: 'real',
        price_change: 'real',
        from_seats: 'int',
        to_seats: 'int',
        effective_date: 'date'
      }
    });
  }
  
  trackChurnEvent(churn) {
    FS('trackEvent', {
      name: 'Subscription Cancelled',
      properties: {
        plan_name: churn.plan,
        tenure_days: churn.tenureDays,
        lifetime_value: churn.ltv,
        cancel_reason: churn.reason,
        cancel_feedback: churn.feedback,
        was_paying: churn.wasPaying,
        final_mrr: churn.finalMrr,
        churn_type: churn.immediate ? 'immediate' : 'end_of_period'
      },
      schema: {
        tenure_days: 'int',
        lifetime_value: 'real',
        was_paying: 'bool',
        final_mrr: 'real'
      }
    });
  }
}
```

**Why this is good:**
- ✅ Captures full subscription lifecycle
- ✅ Includes revenue metrics (MRR, ARR, LTV)
- ✅ Tracks upgrade/downgrade patterns
- ✅ Captures churn reasons for analysis

### Example 4: Search and Discovery

```javascript
// GOOD: Track search behavior
function trackSearch(searchData) {
  FS('trackEvent', {
    name: 'Search Performed',
    properties: {
      // Query details
      search_term: searchData.query,
      search_type: searchData.type,  // 'keyword', 'filter', 'voice'
      
      // Results
      results_count: searchData.results.length,
      has_results: searchData.results.length > 0,
      
      // Filters applied
      filters_applied: Object.keys(searchData.filters),
      filter_count: Object.keys(searchData.filters).length,
      
      // Sorting
      sort_by: searchData.sortBy,
      sort_order: searchData.sortOrder,
      
      // Pagination
      page_number: searchData.page,
      results_per_page: searchData.perPage,
      
      // Performance
      response_time_ms: searchData.responseTime,
      
      // Context
      search_location: searchData.location,  // 'header', 'page', 'modal'
      is_refinement: searchData.isRefinement
    },
    schema: {
      results_count: 'int',
      has_results: 'bool',
      filters_applied: 'strs',
      filter_count: 'int',
      page_number: 'int',
      results_per_page: 'int',
      response_time_ms: 'int',
      is_refinement: 'bool'
    }
  });
}

// Track when user clicks a search result
function trackSearchResultClick(result, searchContext) {
  FS('trackEvent', {
    name: 'Search Result Clicked',
    properties: {
      search_term: searchContext.query,
      result_position: result.position,
      result_id: result.id,
      result_type: result.type,
      results_count: searchContext.totalResults,
      page_number: searchContext.page
    },
    schema: {
      result_position: 'int',
      results_count: 'int',
      page_number: 'int'
    }
  });
}
```

**Why this is good:**
- ✅ Captures search intent (query, filters)
- ✅ Tracks result quality (count, has_results)
- ✅ Measures performance (response_time)
- ✅ Connects searches to clicks

### Example 5: Form/Funnel Tracking

```javascript
// GOOD: Multi-step form/funnel tracking
class FunnelTracker {
  constructor(funnelName, steps) {
    this.funnelName = funnelName;
    this.steps = steps;
    this.startTime = null;
    this.stepTimes = {};
  }
  
  startFunnel(context = {}) {
    this.startTime = Date.now();
    
    FS('trackEvent', {
      name: `${this.funnelName} Started`,
      properties: {
        funnel_name: this.funnelName,
        total_steps: this.steps.length,
        entry_point: window.location.pathname,
        ...context
      },
      schema: {
        total_steps: 'int'
      }
    });
  }
  
  completeStep(stepIndex, stepData = {}) {
    const stepName = this.steps[stepIndex];
    const now = Date.now();
    const stepDuration = this.stepTimes[stepIndex - 1] 
      ? now - this.stepTimes[stepIndex - 1]
      : now - this.startTime;
    
    this.stepTimes[stepIndex] = now;
    
    FS('trackEvent', {
      name: `${this.funnelName} Step Completed`,
      properties: {
        funnel_name: this.funnelName,
        step_number: stepIndex + 1,
        step_name: stepName,
        total_steps: this.steps.length,
        step_duration_ms: stepDuration,
        time_in_funnel_ms: now - this.startTime,
        ...stepData
      },
      schema: {
        step_number: 'int',
        total_steps: 'int',
        step_duration_ms: 'int',
        time_in_funnel_ms: 'int'
      }
    });
  }
  
  completeFunnel(result = {}) {
    const totalDuration = Date.now() - this.startTime;
    
    FS('trackEvent', {
      name: `${this.funnelName} Completed`,
      properties: {
        funnel_name: this.funnelName,
        total_steps: this.steps.length,
        total_duration_ms: totalDuration,
        ...result
      },
      schema: {
        total_steps: 'int',
        total_duration_ms: 'int'
      }
    });
  }
  
  abandonFunnel(stepIndex, reason = 'unknown') {
    FS('trackEvent', {
      name: `${this.funnelName} Abandoned`,
      properties: {
        funnel_name: this.funnelName,
        abandoned_at_step: stepIndex + 1,
        abandoned_step_name: this.steps[stepIndex],
        total_steps: this.steps.length,
        time_in_funnel_ms: Date.now() - this.startTime,
        abandon_reason: reason
      },
      schema: {
        abandoned_at_step: 'int',
        total_steps: 'int',
        time_in_funnel_ms: 'int'
      }
    });
  }
}

// Usage
const checkoutFunnel = new FunnelTracker('Checkout', [
  'Cart Review',
  'Shipping Info',
  'Payment Info',
  'Confirmation'
]);

checkoutFunnel.startFunnel({ cart_value: 150.00 });
checkoutFunnel.completeStep(0, { items_count: 3 });
checkoutFunnel.completeStep(1, { shipping_method: 'express' });
checkoutFunnel.completeStep(2, { payment_method: 'credit_card' });
checkoutFunnel.completeFunnel({ order_id: 'ORD-123', total: 165.00 });
```

**Why this is good:**
- ✅ Tracks full funnel journey
- ✅ Measures time per step
- ✅ Captures abandonment with context
- ✅ Reusable for any multi-step flow

---

## ❌ BAD Implementation Examples

### Example 1: Event Name Too Generic

```javascript
// BAD: Vague event names
FS('trackEvent', {
  name: 'click',  // BAD: Too generic
  properties: {
    element: 'button'
  }
});

FS('trackEvent', {
  name: 'action',  // BAD: Meaningless
  properties: {
    type: 'purchase'
  }
});
```

**Why this is bad:**
- ❌ "click" doesn't describe what happened
- ❌ Can't build meaningful funnels
- ❌ No semantic meaning
- ❌ Hard to analyze

**CORRECTED:**
```javascript
// GOOD: Semantic event names
FS('trackEvent', {
  name: 'Add to Cart Button Clicked',
  properties: {
    product_id: 'SKU-123',
    button_location: 'product_page'
  }
});

FS('trackEvent', {
  name: 'Order Completed',
  properties: {
    order_id: 'ORD-456',
    total: 99.99
  }
});
```

### Example 2: Missing Critical Properties

```javascript
// BAD: Order event without essential data
FS('trackEvent', {
  name: 'Order Completed',
  properties: {
    success: true  // This tells us almost nothing!
  }
});
```

**Why this is bad:**
- ❌ No order ID for reference
- ❌ No revenue data for metrics
- ❌ No product information
- ❌ Can't do meaningful analysis

**CORRECTED:**
```javascript
// GOOD: Comprehensive order event
FS('trackEvent', {
  name: 'Order Completed',
  properties: {
    order_id: order.id,
    revenue: order.total,
    currency: order.currency,
    item_count: order.items.length,
    shipping_method: order.shipping.method,
    payment_method: order.payment.method,
    coupon_code: order.coupon,
    discount_amount: order.discount,
    is_first_order: customer.orderCount === 1
  },
  schema: {
    revenue: 'real',
    item_count: 'int',
    discount_amount: 'real',
    is_first_order: 'bool'
  }
});
```

### Example 3: Type Mismatches

```javascript
// BAD: Wrong value formats
FS('trackEvent', {
  name: 'Product Purchased',
  properties: {
    price: '$49.99',           // BAD: Currency symbol
    quantity: '3 items',       // BAD: Text in number
    in_stock: 'yes',           // BAD: String instead of boolean
    purchase_date: 'today'     // BAD: Not ISO8601
  },
  schema: {
    price: 'real',
    quantity: 'int',
    in_stock: 'bool',
    purchase_date: 'date'
  }
});
```

**Why this is bad:**
- ❌ '$49.99' won't parse as real
- ❌ '3 items' won't parse as int
- ❌ 'yes' is not a valid boolean
- ❌ 'today' is not ISO8601

**CORRECTED:**
```javascript
// GOOD: Properly formatted values
FS('trackEvent', {
  name: 'Product Purchased',
  properties: {
    price: 49.99,
    currency: 'USD',
    quantity: 3,
    in_stock: true,
    purchase_date: new Date().toISOString()
  },
  schema: {
    price: 'real',
    quantity: 'int',
    in_stock: 'bool',
    purchase_date: 'date'
  }
});
```

### Example 4: Tracking Too Many Events

```javascript
// BAD: Tracking every micro-interaction
document.addEventListener('mousemove', (e) => {
  FS('trackEvent', {
    name: 'Mouse Moved',
    properties: { x: e.clientX, y: e.clientY }
  });
});

document.addEventListener('scroll', () => {
  FS('trackEvent', {
    name: 'Page Scrolled',
    properties: { position: window.scrollY }
  });
});
```

**Why this is bad:**
- ❌ Will hit rate limits immediately
- ❌ Drowns out meaningful events
- ❌ No analytical value
- ❌ Fullstory already captures these automatically

**CORRECTED:**
```javascript
// GOOD: Track meaningful scroll milestones only
const scrollMilestones = [25, 50, 75, 100];
let trackedMilestones = new Set();
let currentPagePath = window.location.pathname;
let isScrollTrackingInitialized = false;

// Simple throttle function (or use lodash/underscore)
function throttle(fn, delay) {
  let lastCall = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastCall >= delay) {
      lastCall = now;
      fn.apply(this, args);
    }
  };
}

// Reset tracking state on SPA navigation
function resetScrollTracking() {
  trackedMilestones = new Set();
  currentPagePath = window.location.pathname;
}

// Track scroll depth event with consistent property names
function trackScrollMilestone(milestone, isShortPage = false) {
  FS('trackEvent', {
    name: 'Scroll Depth Reached',
    properties: {
      depth_percent: milestone,
      page_path: currentPagePath,
      content_fit_in_viewport: isShortPage
    }
  });
}

// Handle short pages that fit entirely in viewport (fire 100% immediately)
function checkAndTrackShortPage() {
  // Guard against document.body not being ready
  if (!document.body) return;
  
  const scrollableHeight = document.body.scrollHeight - window.innerHeight;
  if (scrollableHeight <= 0) {
    // Page content fits in viewport - user can see 100%
    scrollMilestones.forEach(milestone => {
      if (!trackedMilestones.has(milestone)) {
        trackedMilestones.add(milestone);
        trackScrollMilestone(milestone, true);
      }
    });
  }
}

// Throttled scroll handler
const handleScroll = throttle(() => {
  // Guard against document.body not being ready
  if (!document.body) return;
  
  // Reset if page changed (SPA navigation fallback)
  if (window.location.pathname !== currentPagePath) {
    resetScrollTracking();
  }
  
  const scrollableHeight = document.body.scrollHeight - window.innerHeight;
  
  // Skip scroll tracking for short pages (handled by checkAndTrackShortPage)
  if (scrollableHeight <= 0) {
    return;
  }
  
  const scrollPercent = Math.round((window.scrollY / scrollableHeight) * 100);
  
  scrollMilestones.forEach(milestone => {
    if (scrollPercent >= milestone && !trackedMilestones.has(milestone)) {
      trackedMilestones.add(milestone);
      trackScrollMilestone(milestone, false);
    }
  });
}, 250);

// Initialize scroll tracking (call once)
function initScrollTracking() {
  if (isScrollTrackingInitialized) return; // Prevent duplicate listeners
  isScrollTrackingInitialized = true;
  
  window.addEventListener('load', checkAndTrackShortPage);
  window.addEventListener('scroll', handleScroll);
}

// Cleanup scroll tracking (call on SPA unmount)
function destroyScrollTracking() {
  if (!isScrollTrackingInitialized) return;
  isScrollTrackingInitialized = false;
  
  window.removeEventListener('load', checkAndTrackShortPage);
  window.removeEventListener('scroll', handleScroll);
  trackedMilestones = new Set();
}

// Initialize
initScrollTracking();

// For SPA frameworks, call in cleanup:
// React: useEffect(() => { initScrollTracking(); return destroyScrollTracking; }, []);
// Vue: onMounted(initScrollTracking); onUnmounted(destroyScrollTracking);
// For route changes: call resetScrollTracking() on navigation
```

### Example 5: Duplicate Events

```javascript
// BAD: Sending same event multiple times
function handleFormSubmit(formData) {
  // This might fire multiple times due to double-clicks or re-renders
  FS('trackEvent', {
    name: 'Form Submitted',
    properties: formData
  });
}

// Without proper deduplication
submitButton.addEventListener('click', handleFormSubmit);
form.addEventListener('submit', handleFormSubmit);  // Double event!
```

**Why this is bad:**
- ❌ Same event fires twice
- ❌ Inflates metrics
- ❌ Creates confusing analytics

**CORRECTED:**
```javascript
// GOOD: Deduplicate events
const eventTracker = {
  recentEvents: new Map(),
  
  track(name, properties, dedupeKey = null) {
    const key = dedupeKey || `${name}-${JSON.stringify(properties)}`;
    const now = Date.now();
    const lastSent = this.recentEvents.get(key);
    
    // Don't send if same event sent within 1 second
    if (lastSent && (now - lastSent) < 1000) {
      return;
    }
    
    this.recentEvents.set(key, now);
    
    FS('trackEvent', {
      name,
      properties
    });
  }
};

// Usage
function handleFormSubmit(formData) {
  eventTracker.track('Form Submitted', formData, formData.formId);
}
```

---

## Common Implementation Patterns

### Pattern 1: Event Tracking Service

```javascript
// Centralized event tracking with validation
class EventTracker {
  constructor() {
    this.eventSchemas = new Map();
  }
  
  // Register event schema for validation
  registerEvent(name, schema) {
    this.eventSchemas.set(name, schema);
  }
  
  // Track event with automatic schema
  track(name, properties) {
    const schema = this.eventSchemas.get(name);
    
    const eventPayload = {
      name,
      properties: {
        ...properties,
        tracked_at: new Date().toISOString(),
        page_url: window.location.href
      }
    };
    
    if (schema) {
      eventPayload.schema = schema;
    }
    
    FS('trackEvent', eventPayload);
  }
}

// Setup
const tracker = new EventTracker();

tracker.registerEvent('Order Completed', {
  revenue: 'real',
  item_count: 'int',
  is_first_order: 'bool'
});

// Usage
tracker.track('Order Completed', {
  order_id: 'ORD-123',
  revenue: 99.99,
  item_count: 3,
  is_first_order: false
});
```

### Pattern 2: E-commerce Event Library

```javascript
// Standard e-commerce events
const ecommerceEvents = {
  
  productViewed(product) {
    FS('trackEvent', {
      name: 'Product Viewed',
      properties: {
        product_id: product.id,
        sku: product.sku,
        name: product.name,
        category: product.category,
        price: product.price,
        currency: product.currency,
        brand: product.brand,
        variant: product.variant
      },
      schema: { price: 'real' }
    });
  },
  
  productAdded(product, cartId, quantity = 1) {
    FS('trackEvent', {
      name: 'Product Added',
      properties: {
        product_id: product.id,
        sku: product.sku,
        name: product.name,
        category: product.category,
        price: product.price,
        currency: product.currency,
        quantity: quantity,
        cart_id: cartId
      },
      schema: { price: 'real', quantity: 'int' }
    });
  },
  
  checkoutStarted(cart) {
    FS('trackEvent', {
      name: 'Checkout Started',
      properties: {
        cart_id: cart.id,
        value: cart.total,
        currency: cart.currency,
        item_count: cart.items.length,
        coupon: cart.coupon
      },
      schema: { value: 'real', item_count: 'int' }
    });
  },
  
  orderCompleted(order) {
    FS('trackEvent', {
      name: 'Order Completed',
      properties: {
        order_id: order.id,
        revenue: order.revenue,
        tax: order.tax,
        shipping: order.shipping,
        total: order.total,
        currency: order.currency,
        item_count: order.items.length,
        coupon: order.coupon,
        discount: order.discount,
        payment_method: order.paymentMethod
      },
      schema: {
        revenue: 'real',
        tax: 'real',
        shipping: 'real',
        total: 'real',
        item_count: 'int',
        discount: 'real'
      }
    });
  }
};
```

### Pattern 3: Timed Event Tracking

```javascript
// Track events with timing
class TimedEventTracker {
  timers = new Map();
  
  start(eventName, properties = {}) {
    this.timers.set(eventName, {
      startTime: Date.now(),
      properties
    });
  }
  
  complete(eventName, additionalProperties = {}) {
    const timer = this.timers.get(eventName);
    if (!timer) return;
    
    const duration = Date.now() - timer.startTime;
    
    FS('trackEvent', {
      name: eventName,
      properties: {
        ...timer.properties,
        ...additionalProperties,
        duration_ms: duration,
        completed: true
      },
      schema: {
        duration_ms: 'int',
        completed: 'bool'
      }
    });
    
    this.timers.delete(eventName);
  }
  
  cancel(eventName, reason = 'cancelled') {
    const timer = this.timers.get(eventName);
    if (!timer) return;
    
    const duration = Date.now() - timer.startTime;
    
    FS('trackEvent', {
      name: eventName,
      properties: {
        ...timer.properties,
        duration_ms: duration,
        completed: false,
        cancel_reason: reason
      },
      schema: {
        duration_ms: 'int',
        completed: 'bool'
      }
    });
    
    this.timers.delete(eventName);
  }
}

// Usage
const timedTracker = new TimedEventTracker();

timedTracker.start('Video Watched', { video_id: 'VID-123' });
// ... user watches video ...
timedTracker.complete('Video Watched', { percent_watched: 85 });
```

### Pattern 4: TypeScript Types

```typescript
// Type-safe event tracking
interface EventSchema {
  [key: string]: 'str' | 'strs' | 'int' | 'ints' | 'real' | 'reals' | 'bool' | 'bools' | 'date' | 'dates';
}

interface TrackEventPayload {
  name: string;
  properties: Record<string, unknown>;
  schema?: EventSchema;
}

// Typed event definitions
interface OrderCompletedProperties {
  order_id: string;
  revenue: number;
  currency: string;
  item_count: number;
  is_first_order: boolean;
}

function trackOrderCompleted(props: OrderCompletedProperties): void {
  FS('trackEvent', {
    name: 'Order Completed',
    properties: props,
    schema: {
      revenue: 'real',
      item_count: 'int',
      is_first_order: 'bool'
    }
  });
}
```

---

## Framework Integration

### React

```jsx
// Custom hook for event tracking
function useEventTracker() {
  const track = useCallback((name, properties, schema) => {
    FS('trackEvent', { name, properties, schema });
  }, []);
  
  return { track };
}

// Usage in component
function CheckoutButton({ cart }) {
  const { track } = useEventTracker();
  
  const handleCheckout = () => {
    track('Checkout Started', {
      cart_id: cart.id,
      value: cart.total,
      item_count: cart.items.length
    }, {
      value: 'real',
      item_count: 'int'
    });
    
    navigate('/checkout');
  };
  
  return <button onClick={handleCheckout}>Checkout</button>;
}
```

### Vue

```javascript
// Plugin for Vue 3
export const FullstoryPlugin = {
  install(app) {
    app.config.globalProperties.$trackEvent = (name, properties, schema) => {
      FS('trackEvent', { name, properties, schema });
    };
    
    app.provide('trackEvent', (name, properties, schema) => {
      FS('trackEvent', { name, properties, schema });
    });
  }
};

// Usage in component
<script setup>
import { inject } from 'vue';

const trackEvent = inject('trackEvent');

function handleAddToCart(product) {
  trackEvent('Product Added', {
    product_id: product.id,
    price: product.price
  }, {
    price: 'real'
  });
}
</script>
```

### Angular

```typescript
// Service for Angular
@Injectable({ providedIn: 'root' })
export class FullstoryService {
  trackEvent(name: string, properties: object, schema?: object): void {
    FS('trackEvent', { name, properties, schema });
  }
}

// Usage in component
@Component({ ... })
export class CheckoutComponent {
  constructor(private fs: FullstoryService) {}
  
  onCheckoutStart(cart: Cart): void {
    this.fs.trackEvent('Checkout Started', {
      cart_id: cart.id,
      value: cart.total,
      item_count: cart.items.length
    }, {
      value: 'real',
      item_count: 'int'
    });
  }
}
```

---

## Reference Links

- **Analytics Events (Web)**: https://developer.fullstory.com/browser/capture-events/analytics-events/
- **Custom Properties**: https://developer.fullstory.com/browser/custom-properties/
- **Async Methods**: https://developer.fullstory.com/browser/methods/async-methods/
