---
name: fullstory-page-properties
version: v3
description: Core concepts for Fullstory's Page Properties API (setProperties with type 'page'). Platform-agnostic guide covering page naming, session-scoped properties, the 1,000 pageName limit, and best practices. See SKILL-WEB.md and SKILL-MOBILE.md for implementation examples.
platforms:
  - web
  - ios
  - android
  - flutter
  - react-native
related_skills:
  - fullstory-element-properties
  - fullstory-user-properties
  - fullstory-analytics-events
  - universal-data-scoping-and-decoration
implementation_files:
  - SKILL-WEB.md
  - SKILL-MOBILE.md
---

# Fullstory Page Properties API

> **Implementation Files**: This document covers core concepts. For code examples, see:
> - [SKILL-WEB.md](./SKILL-WEB.md) — JavaScript/TypeScript (Browser)
> - [SKILL-MOBILE.md](./SKILL-MOBILE.md) — iOS, Android, Flutter, React Native

## Overview

Fullstory's Page Properties API allows developers to capture contextual information about the current page or screen that enriches sessions for search, filtering, segmentation, and journey analysis. Unlike user properties that persist across sessions, page properties are session-scoped and reset when the URL/screen changes.

Key use cases:
- **Page/Screen Naming**: Define semantic names that enrich ALL events on that page across Fullstory
- **Search Context**: Capture search terms and filters on results pages
- **Checkout State**: Track cart value, step number, coupon codes
- **Content Context**: Capture article categories, author, publish date
- **Dynamic State**: Record filters, sort orders, view modes

---

## Core Concepts

### Page Property Lifecycle

```
Page/Screen Load  →  setProperties(page)  →  Properties Active  →  Navigation  →  Properties Reset
        ↓                                            ↓
   Same page, call again                   Merged with existing props
```

### Key Behaviors

| Behavior | Description |
|----------|-------------|
| **Session-scoped** | Properties persist for the current page until navigation |
| **Merge on repeat calls** | Multiple calls on same page merge properties |
| **Reset on navigation** | Properties clear when URL/screen changes |
| **pageName special field** | Creates named Pages for use across Fullstory |

### Page Properties vs Other Property Types

| Type | Scope | Persists | Best For |
|------|-------|----------|----------|
| User Properties | User | Across sessions | User attributes, plan, role |
| Page Properties | Page/Screen | Until navigation | Page context, search, filters |
| Element Properties | Element | Interaction | Click-level context |
| Event Properties | Event | One event | Action-specific data |

---

## ⚠️ Critical: The 1,000 pageName Limit

Fullstory limits you to **1,000 unique `pageName` values**. Once exceeded, additional page names are silently ignored.

**The Strategy**: Use a **generic page name** + **properties for variations**.

```
❌ BAD: Unique pageName for every product
   pageName: "iPhone 15 Pro Max 256GB Space Black"
   pageName: "iPhone 15 Pro Max 512GB Natural Titanium"
   pageName: "Samsung Galaxy S24 Ultra 256GB..."
   → Exhausts 1,000 limit quickly!

✅ GOOD: Generic pageName + properties for context
   pageName: "Product Detail"
   + productName: "iPhone 15 Pro Max"
   + productCategory: "Smartphones"
   + productBrand: "Apple"
   + productPrice: 1199
```

| Scenario | ❌ Wrong (unique pageName) | ✅ Right (generic + properties) |
|----------|---------------------------|--------------------------------|
| Product pages | `"iPhone 15 Pro Detail"` | `pageName: "Product Detail"` + `productName` property |
| User profiles | `"John Smith's Profile"` | `pageName: "User Profile"` + `profileUserId` property |
| Article pages | `"How to Cook Pasta"` | `pageName: "Article"` + `articleTitle`, `articleCategory` properties |
| Search results | `"Search: blue shoes"` | `pageName: "Search Results"` + `searchTerm` property |
| Category pages | `"Men's Running Shoes"` | `pageName: "Category"` + `categoryName`, `categoryPath` properties |

> **Think of it this way**: `pageName` defines the **type** of page (e.g., "Product Detail", "Checkout", "Search Results"). Properties describe the **specific instance** (which product, what search term, etc.). This gives you unlimited variation tracking while staying well under the 1,000 limit.

---

## Why pageName Matters Across Fullstory

`pageName` and page properties aren't just for Journeys — they enrich **every event** that occurs on that page:

| Fullstory Feature | How Page Properties Help |
|-------------------|-------------------------|
| **Search** | Find sessions where `pageName = "Checkout"` AND `cartValue > 500` |
| **Segments** | Create segments like "Users who visited Product pages with priceRange = 'premium'" |
| **Funnels** | Build funnels using pageName steps: "Home → Category → Product Detail → Cart → Checkout" |
| **Journeys** | Map user flows across named pages |
| **Metrics** | Track conversion rates per page type, filter by page properties |
| **Dashboards** | Break down metrics by pageName or page properties |
| **Event Analysis** | Every click, rage click, error on a page carries the page context |

---

## Special Fields

| Field | Behavior |
|-------|----------|
| `pageName` | Creates a named Page used **across all of Fullstory**. Limited to 1,000 unique values. Takes precedence over URL-based page definitions. |

---

## Rate Limits

| Type | Limit |
|------|-------|
| Sustained | 30 calls per page per minute |
| Burst | 10 calls per second |

---

## Property Limits

| Limit | Value |
|-------|-------|
| Properties per page | 50 unique properties (exclusive of pageName) |
| Properties across all pages | 500 unique properties |
| Unique pageName values | 1,000 site-wide |

---

## Best Practices

### 1. pageName Strategy

- **Set pageName first**: Include pageName on the initial setProperties call
- **Use generic names**: Aim for 10-50 unique pageNames, not thousands
- **Don't change pageName**: Once set on a page, subsequent pageName values are ignored
- **Store variations in properties**: Product names, article titles, user IDs go in properties

### 2. Property Categories

Recommended property categories by page type:

| Page Type | Recommended Properties |
|-----------|----------------------|
| Search Results | searchTerm, resultsCount, activeFilters, sortBy |
| Product Detail | productId, productName, category, price, inStock |
| Checkout | checkoutStep, cartValue, itemCount, hasCoupon |
| Article/Content | articleId, category, author, publishDate, readTime |
| Dashboard | activeView, dateRange, selectedFilters |

### 3. Navigation Handling

- **Web SPAs**: Re-set page properties on every route change
- **Mobile**: Set properties on each screen appearance
- **Properties reset automatically**: On URL/screen change, start fresh

### 4. Events + Page Properties

All events on a page inherit its context:

```
Page: Product Detail (productId: SKU-123, price: 99.99)
  ↓
Event: "Add to Cart" ← automatically searchable by page context
Event: "Image Zoomed" ← knows which product
Error Event ← tied to specific product page
```

---

## Page Properties vs Events

| Scenario | Use Page Property | Use Event |
|----------|-------------------|-----------|
| User is viewing product SKU-123 | ✅ `productId: "SKU-123"` | ❌ |
| User clicked "Add to Cart" | ❌ | ✅ `Product Added` |
| Search results show 50 items | ✅ `resultsCount: 50` | ❌ |
| User applied a filter | ✅ Update `activeFilters` | ✅ `Filter Applied` event |
| User is on checkout step 2 | ✅ `checkoutStep: 2` | ❌ |
| User completed checkout | ❌ | ✅ `Order Completed` |

**Rule of thumb**: Page properties describe **state that persists while on the page**. Events capture **moments in time**.

---

## Troubleshooting

### pageName Not Showing in Journeys

| Cause | Solution |
|-------|----------|
| pageName never set | Always include pageName in initial call |
| Exceeded 1,000 limit | Use generic names, check count in Fullstory |
| Trying to change pageName | Once set, subsequent values are ignored |

### Properties Not Persisting

| Cause | Solution |
|-------|----------|
| Navigation occurred | Re-set properties after each navigation |
| Wrong type parameter | Verify `type: 'page'` (web) |
| Page refreshed | Properties reset on refresh |

### SPA/Screen Navigation Not Tracked

| Cause | Solution |
|-------|----------|
| Not calling on navigation | Listen for route/screen changes |
| Only setting on initial load | Hook into router events |
| Route change not detected | Use platform-specific navigation listeners |

---

## Key Takeaways for Agent

When helping developers implement Page Properties:

1. **Always emphasize**:
   - Include pageName — it enriches ALL events on that page
   - Use generic pageName values (max 1,000) + properties for variations
   - Re-set properties on every navigation (SPA/mobile)
   - Page properties enable filtering across Search, Segments, Funnels, Metrics, and Dashboards

2. **Common mistakes to watch for**:
   - Missing pageName property
   - Dynamic pageName values (product names, user names)
   - Changing pageName on same page (subsequent calls ignored)
   - User data in page properties (should be user properties)
   - Not handling navigation in SPAs/mobile apps

3. **Questions to ask developers**:
   - Is this a SPA or traditional page navigation?
   - What page/screen types do you have?
   - What context is relevant to each page type?
   - Do you need this data in Journeys/Funnels?

4. **Platform routing**:
   - Web (JavaScript/TypeScript) → See SKILL-WEB.md
   - iOS (Swift/SwiftUI) → See SKILL-MOBILE.md § iOS
   - Android (Kotlin) → See SKILL-MOBILE.md § Android
   - Flutter (Dart) → See SKILL-MOBILE.md § Flutter
   - React Native → See SKILL-MOBILE.md § React Native

---

## Reference Links

- **Page Properties (Web)**: https://developer.fullstory.com/browser/set-page-properties/
- **Page Properties (iOS)**: https://developer.fullstory.com/mobile/ios/capture-data/set-page-properties/
- **Page Properties (Android)**: https://developer.fullstory.com/mobile/android/capture-data/set-page-properties/
- **Page Properties (Flutter)**: https://developer.fullstory.com/mobile/flutter/capture-data/set-page-properties/
- **Page Properties (React Native)**: https://developer.fullstory.com/mobile/react-native/capture-data/set-page-properties/
- **Custom Properties**: https://developer.fullstory.com/browser/custom-properties/
- **Help Center - Page Properties**: https://help.fullstory.com/hc/en-us/articles/360020623454
