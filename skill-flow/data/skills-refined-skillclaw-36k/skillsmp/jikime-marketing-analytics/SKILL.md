---
name: jikime-marketing-analytics
description: Analytics and tracking implementation specialist for setting up GA4, GTM, event tracking, UTM parameters, and conversion measurement.
version: 1.0.0
tags: ["marketing", "analytics", "tracking", "ga4", "gtm", "conversion"]
triggers:
  keywords: ["analytics", "tracking", "GA4", "Google Analytics", "GTM", "Tag Manager", "UTM", "event tracking", "conversion tracking", "분석", "추적", "트래킹"]
  phases: ["plan", "run"]
  agents: ["frontend", "backend"]
  languages: ["javascript", "typescript"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~7000
user-invocable: true
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
  - TodoWrite
---

# Analytics Tracking Implementation

## Quick Reference (30 seconds)

Analytics Implementation Specialist - Set up tracking that provides actionable insights for marketing and product decisions.

Core Principles:
- **Track for Decisions**: Every event should inform a decision
- **Start with Questions**: What do you need to know? Work backwards
- **Name Consistently**: Naming conventions matter, document everything
- **Maintain Quality**: Clean data > more data

Key Deliverables:
- Tracking plan documentation
- Event implementation
- UTM parameter strategy
- Debugging and validation

---

## Tracking Plan Framework

```
┌─────────────────────────────────────────────────────────────────┐
│  TRACKING PLAN STRUCTURE                                         │
├─────────────────────────────────────────────────────────────────┤
│  Event Name | Category | Properties | Trigger | Notes           │
│  ────────────────────────────────────────────────────────────   │
│  Example:                                                        │
│  signup_completed | Conversion | method, plan | Success page    │
└─────────────────────────────────────────────────────────────────┘
```

### Event Types

| Type | Description | Examples |
|------|-------------|----------|
| **Pageviews** | Automatic, enhanced with metadata | page_view |
| **User Actions** | Clicks, submissions, interactions | button_clicked, form_submitted |
| **System Events** | Completion, errors | signup_completed, error_occurred |
| **Conversions** | Goal completions | purchase_completed, trial_started |

---

## Event Naming Conventions

### Format (Recommended: Object-Action)

```javascript
// Object-Action format
signup_completed
button_clicked
form_submitted
article_read

// Category_Object_Action (for complex products)
checkout_payment_completed
blog_article_viewed
onboarding_step_completed
```

### Best Practices

| Practice | Good | Bad |
|----------|------|-----|
| Case | `signup_completed` | `SignupCompleted` |
| Specificity | `cta_hero_clicked` | `button_clicked` |
| Context | In properties | In event name |
| Characters | Lowercase, underscores | Spaces, special chars |

---

## Essential Events by Page Type

### Marketing Site

| Category | Events |
|----------|--------|
| **Navigation** | page_view, outbound_link_clicked, scroll_depth |
| **Engagement** | cta_clicked, video_played, form_started, form_submitted |
| **Conversion** | signup_started, signup_completed, demo_requested |

### Product/App

| Category | Events |
|----------|--------|
| **Onboarding** | signup_completed, onboarding_step_completed, first_key_action |
| **Core Usage** | feature_used, action_completed, session_started |
| **Monetization** | trial_started, pricing_viewed, purchase_completed |

### E-commerce

| Category | Events |
|----------|--------|
| **Browsing** | product_viewed, product_list_viewed, product_searched |
| **Cart** | product_added_to_cart, product_removed, cart_viewed |
| **Checkout** | checkout_started, checkout_step_completed, purchase_completed |

---

## Event Properties Reference

### Standard Properties

| Category | Properties |
|----------|------------|
| **Page** | page_title, page_location, page_referrer, content_group |
| **User** | user_id, user_type, account_id, plan_type |
| **Campaign** | source, medium, campaign, content, term |
| **Timing** | timestamp, session_duration, time_on_page |

### E-commerce Properties

```javascript
{
  product_id: 'SKU123',
  product_name: 'Product Name',
  category: 'Category',
  price: 99.99,
  quantity: 1,
  currency: 'USD'
}
```

---

## GA4 Implementation

### Configuration Checklist

```
□ One data stream per platform (web, iOS, Android)
□ Enhanced measurement enabled
□ Recommended events using Google's naming
□ Custom events for business-specific actions
□ Conversions marked in Admin > Events
□ Custom dimensions for segmentation
```

### Custom Events (GA4)

```javascript
// gtag.js
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});

// Google Tag Manager (dataLayer)
dataLayer.push({
  'event': 'signup_completed',
  'method': 'email',
  'plan': 'free'
});
```

### E-commerce Event

```javascript
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': 'T12345',
    'value': 99.99,
    'currency': 'USD',
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Product Name',
      'price': 99.99
    }]
  }
});
```

---

## Google Tag Manager Structure

### Container Organization

| Element | Best Practice |
|---------|---------------|
| **Tags** | GA4 Config (base), GA4 Events, Conversion pixels |
| **Triggers** | Page View, Click, Form Submission, Custom Events |
| **Variables** | Built-in (Click Text, URL), Data Layer, JavaScript |

### Best Practices

```
□ Use folders to organize
□ Consistent naming: Tag_Type_Description
□ Version notes on every publish
□ Preview mode for testing
□ Workspaces for collaboration
```

---

## UTM Parameter Strategy

### Standard Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| **utm_source** | Where traffic comes from | google, facebook, newsletter |
| **utm_medium** | Marketing medium | cpc, email, social |
| **utm_campaign** | Campaign name | spring_sale, product_launch |
| **utm_content** | Differentiate versions | hero_cta, sidebar_link |
| **utm_term** | Paid keywords | running+shoes |

### Naming Conventions

```
✓ Lowercase everything: google (not Google)
✓ Use underscores consistently: product_launch
✓ Be specific but concise: blog_footer_cta (not cta1)
✓ Include date where helpful: 2024_q1_promo
```

### UTM Documentation Template

| Campaign | Source | Medium | Content | Full URL | Owner | Date |
|----------|--------|--------|---------|----------|-------|------|
| ... | ... | ... | ... | ... | ... | ... |

---

## Debugging & Validation

### Testing Tools

| Tool | Purpose |
|------|---------|
| **GA4 DebugView** | Real-time event monitoring |
| **GTM Preview** | Test triggers/tags before publish |
| **Browser Extensions** | GA Debugger, Tag Assistant |

### Validation Checklist

```
□ Events firing on correct triggers
□ Property values populating correctly
□ No duplicate events
□ Works across browsers
□ Works on mobile
□ Conversions recorded correctly
□ User ID passing when logged in
□ No PII leaking
```

### Common Issues

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| Events not firing | Trigger misconfigured | Check trigger conditions |
| Wrong values | Variable not configured | Verify data layer |
| Duplicate events | Multiple containers/tags | Audit tag setup |

---

## Privacy & Compliance

### Considerations

```
□ Cookie consent required (EU/UK/CA)
□ No PII in analytics properties
□ Data retention settings configured
□ User deletion capabilities
□ Cross-device tracking consent
```

### Implementation

- **Consent Mode**: Wait for consent before tracking
- **Data Minimization**: Only collect what you need
- **IP Anonymization**: Enable where required
- **No PII in dimensions**: User IDs, not emails

---

## Tracking Plan Document Template

```markdown
# [Site/Product] Tracking Plan

## Overview
- Tools: GA4, GTM
- Last updated: [Date]
- Owner: [Name]

## Events

### Marketing Events
| Event Name | Description | Properties | Trigger |
|------------|-------------|------------|---------|
| signup_started | User initiates signup | source, page | Click signup CTA |
| signup_completed | User completes signup | method, plan | Success page |

### Product Events
[Similar table]

## Custom Dimensions
| Name | Scope | Parameter | Description |
|------|-------|-----------|-------------|
| user_type | User | user_type | Free, trial, paid |

## Conversions
| Conversion | Event | Counting | Google Ads |
|------------|-------|----------|------------|
| Signup | signup_completed | Once per session | Yes |

## UTM Convention
[Guidelines]
```

---

## Works Well With

Skills:
- `jikime-marketing-ab-test` - Experiment tracking
- `jikime-marketing-seo` - Organic traffic analysis
- `jikime-marketing-page-cro` - Conversion optimization using analytics data

---

Version: 1.0.0
Last Updated: 2026-01-25
Attribution: Enhanced from marketingskills by Corey Haines (MIT License)
