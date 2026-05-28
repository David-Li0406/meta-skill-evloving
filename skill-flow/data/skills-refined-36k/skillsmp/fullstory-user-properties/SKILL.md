---
name: fullstory-user-properties
version: v3
description: Core concepts for Fullstory's User Properties API (setProperties with type 'user'). Platform-agnostic guide covering property naming, type handling, special fields, and best practices. See SKILL-WEB.md and SKILL-MOBILE.md for implementation examples.
platforms:
  - web
  - ios
  - android
  - flutter
  - react-native
related_skills:
  - fullstory-identify-users
  - fullstory-page-properties
  - fullstory-analytics-events
  - universal-data-scoping-and-decoration
implementation_files:
  - SKILL-WEB.md
  - SKILL-MOBILE.md
---

# Fullstory User Properties API

> **Implementation Files**: This document covers core concepts. For code examples, see:
> - [SKILL-WEB.md](./SKILL-WEB.md) — JavaScript/TypeScript (Browser)
> - [SKILL-MOBILE.md](./SKILL-MOBILE.md) — iOS, Android, Flutter, React Native

## Overview

Fullstory's User Properties API allows developers to capture custom user data that enriches user profiles for search, filtering, segmentation, and analytics. Unlike `setIdentity` which links a session to a known user ID, user properties let you add or update attributes about **any** user — including anonymous users.

> **Important**: Every new browser/device starts as an anonymous user. You can set user properties on anonymous users *before* they ever identify. These properties persist across sessions and transfer when/if the user later identifies.

Key use cases:
- **Anonymous User Enrichment**: Add attributes before the user logs in (referral source, landing page, visitor type)
- **Progressive Profiling**: Update properties as you learn more about the user
- **Subscription/Plan Changes**: Track plan upgrades without re-identifying
- **Preference Tracking**: Store user settings and preferences
- **CRM Sync**: Mirror key CRM fields in Fullstory

---

## Core Concepts

### setIdentity vs setProperties (User)

| API | Purpose | When to Use | Works for Anonymous? |
|-----|---------|-------------|---------------------|
| `setIdentity` | Link session to a known user ID + optional initial properties | Login, authentication | No (converts anonymous → identified) |
| `setProperties` (user) | Add/update properties for the current user | **Anytime** — works for anonymous AND identified users | **Yes** ✅ |

> **Key Distinction**: Use `setIdentity` when you need to **link a session to a known user** (requires a `uid`). Use user properties when you just want to **add or update attributes** about the current user — this works for both identified AND anonymous users.

### Anonymous Users

Every user starts as anonymous, tracked via platform-specific mechanisms:

- **Web**: `fs_uid` first-party cookie (1-year expiry)
- **Mobile**: Device-based identifier persisted in app storage

Key behaviors:
- **Persistent across sessions**: As long as the identifier exists, all sessions are linked to the same anonymous user
- **Can receive user properties**: Add attributes to anonymous users before identification
- **Properties transfer on identification**: When identity is set, ALL previous sessions merge into the identified user
- **Searchable and segmentable**: Anonymous users work just like identified users in Fullstory

### When to Use Each

```
User logs in → setIdentity({ uid: "user_123", properties: { displayName: "Jane" } })
                ↓
User updates profile → setProperties (user) { plan: "pro" }
                ↓
User upgrades plan → setProperties (user) { plan: "enterprise" }
```

**For anonymous users** (not yet logged in):
- Use user properties to capture attributes like visitor type, referral source, landing page
- These properties persist and transfer when/if they later identify

### Property Persistence

- User properties persist across sessions
- Properties can be updated at any time
- New properties are added; existing properties are overwritten
- Properties cannot be deleted via the API (contact support)

### Special Fields

| Field | Behavior |
|-------|----------|
| `displayName` | Shown in session list and user card in Fullstory UI |
| `email` | Enables email-based search and HTTP API lookups |

---

## Supported Property Types

| Type | Description | Examples |
|------|-------------|----------|
| `str` | String value | "premium", "enterprise" |
| `strs` | Array of strings | ["admin", "beta-tester"] |
| `int` | Integer | 42, -5, 0 |
| `ints` | Array of integers | [1, 2, 3] |
| `real` | Float/decimal | 99.99, -3.14 |
| `reals` | Array of reals | [10.5, 20.0] |
| `bool` | Boolean | true, false |
| `bools` | Array of booleans | [true, false, true] |
| `date` | ISO8601 date | "2024-01-15T00:00:00Z" |
| `dates` | Array of dates | ["2024-01-01", "2024-02-01"] |

---

## Rate Limits

| Type | Limit |
|------|-------|
| Sustained | 30 calls per page/screen per minute |
| Burst | 10 calls per second |

---

## Property Naming Conventions

| Rule | Good | Bad |
|------|------|-----|
| Use snake_case or camelCase | `plan_tier`, `planTier` | `Plan-Tier`, `PLAN TIER` |
| Be descriptive | `subscription_status` | `ss` |
| Include units where relevant | `trial_days_remaining` | `trial` |
| Avoid PII in names | `user_segment` | `ssn`, `credit_card` |

---

## Best Practices

### 1. Property Design

- **Set core properties in setIdentity**: displayName, email, and other stable attributes
- **Use setProperties for updates**: Don't re-identify just to update properties
- **Include business-relevant data**: plan, role, company, feature access
- **Use explicit types**: Specify schema for non-string values

### 2. Batching Updates

- **Batch rapid updates**: If updating multiple properties quickly, combine into one call
- **Consider debouncing**: For frequently changing data, debounce updates
- **Watch rate limits**: 30 calls/minute sustained, 10 calls/second burst

### 3. Property Categories

Recommended property categories for comprehensive user profiles:

| Category | Example Properties |
|----------|-------------------|
| Identity | displayName, email |
| Subscription | plan, planTier, billingCycle, mrr |
| Engagement | lastActiveAt, sessionCount, featureUsageScore |
| Business | companyName, companySize, industry, role |
| Lifecycle | signupDate, trialStartedAt, onboardingComplete |
| Attribution | referralSource, campaign, landingPage |
| Integration | 

### 4. Events + Properties

Track **both** the change (event) and the new state (property):

```
User upgrades plan:
  1. Event: "Plan Upgraded" with from_plan, to_plan, price_change
  2. Property: plan = "enterprise", planChangedAt = now
```

---

## Relationship with Other APIs

### setIdentity + setProperties Workflow

1. **setIdentity**: Called on login with core properties (displayName, email)
2. **setProperties (user)**: Called later to add/update attributes without re-identifying

### setProperties (user) vs setProperties (page)

| Type | Persistence | Use For |
|------|-------------|---------|
| User | Across sessions | Who they are (plan, role, company) |
| Page | Current session/page | Where they are (pageName, filters, view) |

### setProperties vs trackEvent

| API | Purpose | Example |
|-----|---------|---------|
| setProperties | Current state (what IS) | plan: "professional", seats: 10 |
| trackEvent | Actions/changes (what HAPPENED) | "Plan Upgraded" with from/to values |

---

## Troubleshooting

### Properties Not Appearing

| Symptom | Cause | Solution |
|---------|-------|----------|
| No properties in Fullstory | Missing type parameter | Always include `type: 'user'` (web) |
| Properties on wrong user | Called before identification | Verify user state before setting |
| Properties not persisting | Rate limits exceeded | Batch updates to avoid limits |

### Properties Show Wrong Values

| Symptom | Cause | Solution |
|---------|-------|----------|
| Wrong type | Value format doesn't match schema | Use clean values (no currency symbols, etc.) |
| Boolean as string | `"true"` instead of `true` | Use actual boolean type |
| Date not queryable | Not ISO8601 format | Use `YYYY-MM-DDTHH:mm:ssZ` format |

### displayName Keeps Getting Overwritten

| Symptom | Cause | Solution |
|---------|-------|----------|
| Name changes unexpectedly | Multiple places setting displayName | Only set in identification flow |
| Generic name appears | Automated scripts overwriting | Audit all property-setting code |

---

## Limits and Constraints

### Property Limits
- Check your Fullstory plan for specific limits
- Property names: alphanumeric, underscores, hyphens
- Avoid high-cardinality properties (unique values for every user)

### Value Requirements
- Strings: Must be valid UTF-8
- Numbers: Standard JSON number format
- Dates: ISO8601 format
- Arrays: Maximum length varies by plan

---

## Key Takeaways for Agent

When helping developers implement User Properties:

1. **Always emphasize**:
   - Include `type: 'user'` (web) or use the user properties method
   - Use schema for non-string types
   - Batch updates to respect rate limits
   - displayName and email have special behavior in UI

2. **Common mistakes to watch for**:
   - Missing type parameter (web)
   - Excessive call frequency
   - Type mismatches in values
   - Overwriting displayName accidentally
   - Using setProperties instead of setIdentity for initial identification

3. **Questions to ask developers**:
   - Will the user be anonymous or identified?
   - How often will these properties be updated?
   - What data types are these values?
   - Do you need to track the change as an event too?

4. **Platform routing**:
   - Web (JavaScript/TypeScript) → See SKILL-WEB.md
   - iOS (Swift/SwiftUI) → See SKILL-MOBILE.md § iOS
   - Android (Kotlin) → See SKILL-MOBILE.md § Android
   - Flutter (Dart) → See SKILL-MOBILE.md § Flutter
   - React Native → See SKILL-MOBILE.md § React Native

---

## Reference Links

- **User Properties (Web)**: https://developer.fullstory.com/browser/identification/set-user-properties/
- **User Properties (iOS)**: https://developer.fullstory.com/mobile/ios/identification/set-user-properties/
- **User Properties (Android)**: https://developer.fullstory.com/mobile/android/identification/set-user-properties/
- **User Properties (Flutter)**: https://developer.fullstory.com/mobile/flutter/identification/set-user-properties/
- **User Properties (React Native)**: https://developer.fullstory.com/mobile/react-native/identification/set-user-properties/
- **Custom Properties**: https://developer.fullstory.com/browser/custom-properties/
- **Help Center - Custom Properties**: https://help.fullstory.com/hc/en-us/articles/360020623234
