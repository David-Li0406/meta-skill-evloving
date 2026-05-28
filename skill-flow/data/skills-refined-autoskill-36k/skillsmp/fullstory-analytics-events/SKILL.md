---
name: fullstory-analytics-events
version: v3
description: Core concepts for Fullstory's Analytics Events API (trackEvent). Platform-agnostic guide covering event naming, property types, rate limits, and best practices. See SKILL-WEB.md and SKILL-MOBILE.md for implementation examples.
platforms:
  - web
  - ios
  - android
  - flutter
  - react-native
related_skills:
  - fullstory-page-properties
  - fullstory-user-properties
  - fullstory-element-properties
  - universal-data-scoping-and-decoration
  - fullstory-async-methods
  - fullstory-privacy-strategy
  - fullstory-ecommerce
  - fullstory-saas
  - fullstory-travel
  - fullstory-media-entertainment
implementation_files:
  - SKILL-WEB.md
  - SKILL-MOBILE.md
---

# Fullstory Analytics Events API

> **Implementation Files**: This document covers core concepts. For code examples, see:
> - [SKILL-WEB.md](./SKILL-WEB.md) — JavaScript/TypeScript (Browser)
> - [SKILL-MOBILE.md](./SKILL-MOBILE.md) — iOS, Android, Flutter, React Native

## Overview

Fullstory's Analytics Events API allows developers to send custom event data that captures meaningful user actions and business moments. Unlike automatic capture which records all interactions, `trackEvent` lets you define semantically meaningful events with rich context that can be used for:

- **Funnel Analysis**: Track conversion steps and drop-off points
- **Feature Adoption**: Measure feature usage and engagement
- **Business Metrics**: Capture revenue, conversions, and KPIs
- **User Journeys**: Define key moments in user workflows
- **Segmentation**: Create user segments based on behaviors

### Beyond the DOM

Analytics events are especially valuable for capturing **data that isn't visible in the DOM** or native view hierarchy:

- **Network/API Data**: AJAX response errors, correlation IDs, request header values, API latency
- **Framework Internals**: React component render times, Angular state errors, Vue lifecycle issues
- **Performance Metrics**: Time-to-interactive, lazy load completion, bundle load times
- **Background Processes**: WebSocket events, service worker activity, push notification delivery
- **Error Context**: Stack traces, error codes, failed validation details

This makes `trackEvent` the bridge between your application's internal state and Fullstory's observability.

---

## Core Concepts

### Events vs Properties vs Elements

| API | Purpose | Data Type | Example |
|-----|---------|-----------|---------|
| `trackEvent` | Discrete actions/moments | "What happened" | "Order Completed", "Feature Used" |
| `setProperties` (user) | User attributes | "Who they are" | plan: "enterprise" |
| `setProperties` (page) | Page context | "Where they are" | pageName: "Checkout" |
| Element Properties | Interaction context | "What they clicked" | productId: "SKU-123" |

### When to Use Events

**Key principle:** Events capture **moments in time**. Page properties capture **state that persists** across interactions.

✅ **Use trackEvent for:**
- Discrete actions that happen at a **specific point in time**
- Business-critical moments (purchases, signups, conversions)
- Feature usage tracking
- Funnel step completion
- Data not in the DOM (API responses, framework errors, performance metrics)
- Background process completions (data sync, file upload finished)

❌ **Don't use trackEvent for:**
- Clicks (Fullstory captures automatically)
- Page views (use page properties instead)
- User attributes (use user properties instead)
- High-frequency interactions (scroll, mouse move)
- **Stateful context** that applies to multiple interactions (use page properties)

### Events vs Page Properties: Point-in-Time vs State

| Scenario | Use Event | Use Page Property |
|----------|-----------|-------------------|
| API call failed at 2:03pm | ✅ `API Error Occurred` | ❌ |
| User is viewing product SKU-123 | ❌ | ✅ `productId: "SKU-123"` |
| Component took 850ms to render | ✅ `Slow Render Detected` | ❌ |
| User has 3 items in cart | ❌ | ✅ `cartItemCount: 3` |
| User completed checkout | ✅ `Order Completed` | ❌ |
| User is on the checkout flow | ❌ | ✅ `flowName: "checkout"` |

**Rule of thumb:** If the data remains true while the user interacts with the page, it's a page property. If it's something that *happened*, it's an event.

---

## Event Naming Conventions

Fullstory recommends semantic event naming following industry standards:

```
[Object] [Action]

Examples:
- "Product Added"
- "Order Completed"
- "Feature Enabled"
- "Search Performed"
- "Video Played"
- "Subscription Started"
- "Trial Converted"
```

### Naming Rules

| Rule | Good | Bad |
|------|------|-----|
| Use Object + Action | "Product Added" | "click" |
| Be specific | "Checkout Started" | "action" |
| Use past tense for actions | "Order Completed" | "Order Complete" |
| Keep under 250 chars | "CTA Clicked" | "User clicked on the primary..." |
| Avoid redundancy | "Feature Used" | "Feature Feature Used" |

### Standard Event Names by Category

**E-commerce:**
- Product Viewed, Product Added, Product Removed
- Cart Viewed, Checkout Started, Order Completed
- Coupon Applied, Payment Failed

**SaaS:**
- Feature Used, Feature Enabled, Feature Disabled
- Trial Started, Trial Converted, Trial Expired
- Subscription Started, Plan Changed, Subscription Cancelled

**Engagement:**
- Search Performed, Search Result Clicked
- Content Viewed, Video Played, Video Completed
- Form Started, Form Completed, Form Abandoned

**Technical/System (non-DOM data):**
- API Error Occurred, API Call Completed
- Component Render Slow, Hydration Failed
- State Error Detected, Framework Exception
- WebSocket Disconnected, Sync Completed
- Performance Threshold Exceeded, Bundle Loaded

---

## Event Properties

Every event can include rich contextual properties that enable deep analysis.

### Property Naming

| Rule | Good | Bad |
|------|------|-----|
| Use snake_case | `product_id` | `productId`, `ProductID` |
| Be descriptive | `shipping_method` | `sm` |
| Include units | `duration_ms` | `duration` |
| Avoid PII | `user_segment` | `email` |

### Supported Property Types

| Type | Description | Examples |
|------|-------------|----------|
| `str` | String value | "blue", "premium" |
| `strs` | Array of strings | ["red", "blue", "green"] |
| `int` | Integer | 42, -5, 0 |
| `ints` | Array of integers | [1, 2, 3] |
| `real` | Float/decimal | 99.99, -3.14 |
| `reals` | Array of reals | [10.5, 20.0] |
| `bool` | Boolean | true, false |
| `bools` | Array of booleans | [true, false] |
| `date` | ISO8601 date | "2024-01-15T00:00:00Z" |
| `dates` | Array of dates | ["2024-01-01", "2024-02-01"] |

### Type Inference

Fullstory auto-infers types, but explicit schemas ensure accuracy:

| Value | Auto-Inferred | With Schema |
|-------|---------------|-------------|
| `"42"` | `str` | Can force to `int` |
| `42` | `int` | Confirmed `int` |
| `42.0` | `real` | Confirmed `real` |
| `"2024-01-15"` | `str` | Can force to `date` |

---

## Limits and Constraints

### Size Limits

| Limit | Value |
|-------|-------|
| Event name | Max 250 characters |
| Properties payload | Max 512KB |
| Property name | Max 256 characters |

### Rate Limits

| Type | Limit |
|------|-------|
| Sustained | 60 calls per user per page per minute |
| Burst | 40 calls per second |

### Array Handling

| Array Type | Indexed? | Notes |
|------------|----------|-------|
| Strings (`strs`) | ✅ Yes | Searchable |
| Integers (`ints`) | ✅ Yes | Searchable |
| Reals (`reals`) | ✅ Yes | Searchable |
| Booleans (`bools`) | ✅ Yes | Searchable |
| Dates (`dates`) | ✅ Yes | Searchable |
| Objects | ❌ No | NOT indexed (except Order Completed products) |

---

## Best Practices

### 1. Event Design Checklist

Before implementing an event, answer:

- [ ] **What question does this answer?** (e.g., "How many users complete checkout?")
- [ ] **What properties enable analysis?** (e.g., order_id, revenue, item_count)
- [ ] **How often will it fire?** (Watch rate limits)
- [ ] **Is it redundant?** (Don't duplicate auto-captured data)

### 2. Property Design Principles

- **Include identifiers**: order_id, product_id, feature_name
- **Include context**: source, entry_point, page_name
- **Include metrics**: revenue, quantity, duration_ms
- **Include state**: is_first_order, is_trial, status

### 3. Deduplication

For events that might fire multiple times (form submissions, button clicks):

```
Strategy: Track a unique key (e.g., order_id) and skip if seen recently
```

### 4. Timing Events

For events with duration (video watched, form completed):

```
Strategy: Track start time, calculate duration on completion
Include: duration_ms, completed (bool), cancel_reason (if abandoned)
```

---

## Troubleshooting

### Events Not Appearing

| Symptom | Cause | Solution |
|---------|-------|----------|
| No events in Fullstory | SDK not loaded | Verify SDK initialization |
| Events truncated | Name > 250 chars | Shorten event name |
| Events dropped | Rate limit exceeded | Throttle high-frequency events |
| Events missing | Properties > 512KB | Reduce payload size |

### Properties Not Indexed

| Symptom | Cause | Solution |
|---------|-------|----------|
| Can't search by property | Wrong type | Use explicit schema |
| Property shows as string | Number in quotes | Pass actual number |
| Date not queryable | Wrong format | Use ISO8601 format |
| Array not searchable | Array of objects | Flatten to primitive arrays |

### Common Type Mistakes

| Wrong | Right | Issue |
|-------|-------|-------|
| `"$99.99"` | `99.99` | Currency symbol in number |
| `"3 items"` | `3` | Text in number |
| `"yes"` | `true` | String instead of boolean |
| `"today"` | `"2024-01-15T00:00:00Z"` | Not ISO8601 |

---

## Fullstory Search Examples

### Find Events by Name

```
Event where name = "Order Completed"
```

### Filter by Property

```
Event where name = "Order Completed" and revenue > 100
```

### Find Events with Specific Value

```
Event where name = "Feature Used" and feature_name = "advanced_export"
```

### Combine with User Properties

```
Event where name = "Order Completed" and user.plan = "enterprise"
```

### Find Abandoned Funnels

```
Event where name = "Checkout Abandoned" and abandoned_at_step = 2
```

---

## Key Takeaways for Agent

When helping developers implement Analytics Events:

1. **Always emphasize**:
   - Use semantic event names (Object + Action)
   - Include meaningful properties
   - Use schema for non-string types
   - Don't track what Fullstory captures automatically
   - **Events = moments in time; Page properties = persistent state**
   - **Events are ideal for non-DOM point-in-time data** (API errors, performance failure events, framework internals)

2. **Common mistakes to watch for**:
   - Generic event names ("click", "action")
   - Missing critical properties (order_id, revenue)
   - Type format mismatches
   - Over-tracking micro-interactions
   - Using events for stateful data describing a page or user (should be page or user properties)
   - Using page properties for point-in-time occurrences (should be events)

3. **Questions to ask developers**:
   - What business questions will this event answer?
   - What properties are needed for segmentation?
   - How often will this event fire?
   - Is this redundant with auto-captured data?
   - **Is this a moment in time, or state that persists?**
   - **Is this data visible in the DOM, or only in code?**

4. **Platform routing**:
   - Web (JavaScript/TypeScript) → See SKILL-WEB.md
   - iOS (Swift/SwiftUI) → See SKILL-MOBILE.md § iOS
   - Android (Kotlin) → See SKILL-MOBILE.md § Android
   - Flutter (Dart) → See SKILL-MOBILE.md § Flutter
   - React Native → See SKILL-MOBILE.md § React Native

---

## Reference Links

- **Analytics Events (Web)**: https://developer.fullstory.com/browser/capture-events/analytics-events/
- **Analytics Events (iOS)**: https://developer.fullstory.com/mobile/ios/capture-events/analytics-events/
- **Analytics Events (Android)**: https://developer.fullstory.com/mobile/android/capture-events/analytics-events/
- **Analytics Events (Flutter)**: https://developer.fullstory.com/mobile/flutter/capture-events/analytics-events/
- **Analytics Events (React Native)**: https://developer.fullstory.com/mobile/react-native/capture-events/analytics-events/
- **Custom Properties**: https://developer.fullstory.com/browser/custom-properties/
- **Help Center - Custom Events**: https://help.fullstory.com/hc/en-us/articles/360020623274
