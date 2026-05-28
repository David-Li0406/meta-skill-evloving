---
name: fullstory-element-properties
version: v3
description: Core concepts for Fullstory's Element Properties API. Platform-agnostic guide covering API Defined Elements, property inheritance, schema types, and best practices. See SKILL-WEB.md and SKILL-MOBILE.md for implementation examples.
platforms:
  - web
  - ios
  - android
  - flutter
  - react-native
related_skills:
  - fullstory-page-properties
  - fullstory-user-properties
  - fullstory-analytics-events
  - universal-data-scoping-and-decoration
  - fullstory-privacy-controls
  - fullstory-ecommerce
  - fullstory-saas
implementation_files:
  - SKILL-WEB.md
  - SKILL-MOBILE.md
---

# Fullstory Element Properties API

> **Implementation Files**: This document covers core concepts. For code examples, see:
> - [SKILL-WEB.md](./SKILL-WEB.md) — JavaScript/TypeScript (Browser)
> - [SKILL-MOBILE.md](./SKILL-MOBILE.md) — iOS, Android, Flutter, React Native

## Overview

Fullstory's Element Properties API allows developers to capture custom properties on UI elements that can be used for search, filtering, grouping, and analytics. Unlike standard attributes which are only used for CSS selectors, element properties become first-class data points for analysis, similar to user properties, page properties, and event properties.

**Key capabilities:**
- Attach semantic business data to interactive elements
- Enable filtering and segmentation by element context
- Capture data on clicks, taps, and other interactions
- Inherit properties through element hierarchy

---

## Core Concepts

### API Defined Elements

- API Defined Elements provide a programmatic approach to defining Elements in Fullstory
- Once created, these elements can be used across Fullstory features for search and analysis
- Elements are defined using the `data-fs-element` attribute (web) or `FS.setAttribute` (mobile)
- Element names are permanently attached to their associated Element (though display name can change)

### Element Properties vs Attributes

| Type | Purpose | Searchable | Example |
|------|---------|------------|---------|
| **Attributes** | CSS selectors, element matching | ❌ No | `class="btn-primary"` |
| **Element Properties** | Filtering, grouping, analytics | ✅ Yes | `productId: "SKU-123"` |

### When to Use Element Properties

✅ **Good use cases:**
- E-commerce product data (SKUs, prices, categories)
- Form analytics (field names, validation states)
- Content tracking (article IDs, categories)
- A/B testing (variant names, experiment IDs)
- User segments (tier levels, feature flags)
- Navigation context (section names, page types)

❌ **Avoid for:**
- Technical/debug data (component versions, render timestamps)
- Styling information (CSS classes, style properties)
- Implementation details (framework internals, React keys)
- High cardinality data (unique timestamps, random IDs)
- Data already captured as user/page properties
- PII without proper consent handling

---

## ⭐ Critical: Property Inheritance (Parent ↔ Child)

This is one of the most powerful features of Element Properties:

**Two-way inheritance:**
- **Parent → Child**: Properties defined on a parent element are inherited by all child elements
- **Child → Parent**: When an action occurs on a parent element, it captures properties from all defined child elements

```
┌─────────────────────────────────────────────────────────────────────┐
│  FORM (element="checkout-form")                                      │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  SHIPPING SELECT (selectedShipping="express")                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  PAYMENT SELECT (selectedPayment="credit_card")              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  GIFT WRAP CHECKBOX (giftWrap="true")                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  SUBMIT BUTTON (element="submit-order")                      │   │
│  │  ───────────────────────────────────────────────────────     │   │
│  │  When clicked, captures ALL properties from siblings:        │   │
│  │  • selectedShipping: "express"                               │   │
│  │  • selectedPayment: "credit_card"                            │   │
│  │  • giftWrap: true                                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Why this matters for analytics:**
- The submit button (or any parent action element) automatically captures the state of all child properties at the moment of interaction
- You can create metrics like:
  - "Submit clicks WHERE selectedPayment = 'paypal'"
  - "Group submit clicks BY selectedShipping"
  - "Funnel: visits → checkout-form viewed → submit-order clicked WHERE giftWrap = true"

> **Key Insight**: Define element properties on individual form fields, and the submit button will automatically capture the full form state. This eliminates the need to manually aggregate form data.

---

## Supported Property Types

| Type | Description | Examples |
|------|-------------|----------|
| `str` | String value | "foo", "bar", "foo@bar" |
| `strs` | Array of strings | ["foo", "bar"] |
| `int` | Integer | 0, -123, 45 |
| `ints` | Array of integers | [0, 1, 2] |
| `real` | Float/decimal | 12.345, -0.5 |
| `reals` | Array of reals | [12.345, 1] |
| `bool` | Boolean | true, false, 1, 0, t, f |
| `bools` | Array of booleans | [true, false] |
| `date` | ISO8601 date/datetime | "2006-01-02T15:04:05Z" |
| `dates` | Array of dates | ["2006-01-02", "2006-01-02T15:04:05Z"] |

### Type Formatting Requirements

| Type | Correct | Incorrect |
|------|---------|-----------|
| `real` | `199.99` | `"$199.99"` (no currency symbols) |
| `int` | `5` | `"5 items"` (no units/text) |
| `bool` | `true` or `"true"` | `"yes"`, `"Yes"`, `"Y"` |
| `date` | `"2024-01-15T00:00:00Z"` | `"today"`, `"Jan 15"` |

---

## Limits and Constraints

### Global Limits

| Limit | Value |
|-------|-------|
| Active API Defined Elements | Max 1,000 (archived don't count) |
| Properties per single interaction | Max 50 unique |
| Properties across all interactions | Max 500 unique |

### Property Requirements

- **Property Names**: Use meaningful, readable names (no type suffix needed)
- **Property Values**: Must match the specified type
- **Cardinality**: High cardinality properties may be limited

### Best Practices for Limits

1. ✅ Focus on business-relevant properties only
2. ✅ Avoid debug/technical properties
3. ✅ Use property hierarchy to reduce duplication
4. ✅ Archive unused elements to free up quota
5. ✅ Monitor your property count

---

## Common Implementation Patterns

### Pattern 1: Container + Interactive Element

```
Container (e.g., product card)
  ├── Properties: productId, productName, price, category
  └── Button (e.g., "Add to Cart")
      └── Inherits all container properties
      └── Button interaction captures full product context
```

### Pattern 2: Form + Fields

```
Form Container
  ├── Properties: formType, formStep, userTier
  ├── Field 1
  │   ├── Inherits form properties
  │   └── Own properties: fieldName, isRequired, fieldType
  ├── Field 2
  │   └── Same pattern
  └── Submit Button
      └── Inherits form properties + captures all field properties
```

### Pattern 3: List Items

```
List Container
  ├── Properties: listType, totalItems, filterApplied
  └── List Item (repeated)
      ├── Inherits list properties
      └── Own properties: itemId, itemName, position
```

---

## Implementation Order (Critical)

For all platforms, follow this order:

1. **Set attribute values FIRST**
2. **Set the properties schema SECOND**
3. **Name the element LAST** (with `data-fs-element` or equivalent)

Setting the schema before values may cause timing issues with property capture.

---

## Best Practices

### Property Design

| Do | Don't |
|----|-------|
| Use clean numeric values | Include currency symbols ($, €) |
| Use boolean true/false | Use "yes"/"no" strings |
| Use ISO8601 for dates | Use human-readable dates |
| Use `name` override for readability | Use raw attribute names |
| Focus on business-relevant data | Capture debug/technical data |

### Mobile-Specific Considerations

- **Handle view/cell reuse**: Clear old attributes before setting new ones
- **Track applied attributes**: Maintain a list for cleanup
- **Use lifecycle methods**: `prepareForReuse()` (iOS), `onBindViewHolder` (Android)
- **Convert types to strings**: Mobile SDKs expect string values for all attributes

---

## Troubleshooting

### Properties Not Appearing

| Symptom | Common Causes | Solutions |
|---------|---------------|-----------|
| No properties captured | Schema set before values | Always set values before schema |
| No properties captured | Invalid JSON in schema | Use proper JSON builders, not manual strings |
| No properties captured | Attribute doesn't exist | Verify all schema attributes exist |
| No properties captured | Hit property limits | Check 50/500 limits |

### Wrong Values Captured (Mobile)

| Symptom | Common Causes | Solutions |
|---------|---------------|-----------|
| Stale data | View/cell reuse not handled | Implement `prepareForReuse` or clear in bind |
| Old attributes remain | Attributes not cleared | Track and clear previous attributes |
| Wrong timing | Attributes set at wrong lifecycle point | Set in appropriate lifecycle methods |

### Type Conversion Errors

| Symptom | Common Causes | Solutions |
|---------|---------------|-----------|
| Numbers show as strings | Values contain non-numeric chars | Strip formatting before setting |
| Booleans show as strings | Using "yes"/"no" | Use "true"/"false" strings |
| Dates not queryable | Wrong format | Use ISO8601 format |

---

## Pre-Deployment Checklist

- [ ] All attribute values are set before the schema
- [ ] All referenced attributes in schema actually exist
- [ ] Numeric values are clean (no symbols, units, text)
- [ ] Boolean values use "true"/"false" or "1"/"0"
- [ ] Date values are in ISO8601 format
- [ ] JSON schema is valid (no syntax errors)
- [ ] Property names are meaningful and use `name` override
- [ ] Types match the actual data (real for decimals, int for whole numbers)
- [ ] Cell/view reuse is handled (mobile only)
- [ ] Elements are named with `data-fs-element` (web) or equivalent (mobile)

---

## Key Takeaways for Agent

When helping developers implement Element Properties:

1. **Always emphasize**:
   - Set attribute values BEFORE schema
   - Use clean, unformatted values (no "$", "items", "Yes/No")
   - Match types correctly (real for decimals, int for integers, bool for booleans)
   - Provide meaningful property names via `name` override

2. **Common mistakes to watch for**:
   - Schema set before values
   - Formatted numbers ("$10.99", "5 items")
   - "Yes"/"No" for booleans
   - Manual JSON string construction (mobile)
   - No cell/view reuse handling (mobile)
   - Over-capturing technical/debug data

3. **Questions to ask developers**:
   - What data is business-relevant?
   - Is this element in a recycling container? (mobile)
   - Are there parent elements that should have properties?
   - What analytics questions need to be answered?

4. **Platform routing**:
   - Web (JavaScript/HTML) → See SKILL-WEB.md
   - iOS (Swift/SwiftUI) → See SKILL-MOBILE.md § iOS
   - Android (Kotlin/Java) → See SKILL-MOBILE.md § Android
   - Flutter (Dart) → See SKILL-MOBILE.md § Flutter
   - React Native → See SKILL-MOBILE.md § React Native

---

## Reference Links

- **Browser API**: https://developer.fullstory.com/browser/fullcapture/set-element-properties/
- **Android API**: https://developer.fullstory.com/mobile/android/fullcapture/set-element-properties/
- **iOS API**: https://developer.fullstory.com/mobile/ios/fullcapture/set-element-properties/
- **Flutter API**: https://developer.fullstory.com/mobile/flutter/fullcapture/set-element-properties/
- **React Native API**: https://developer.fullstory.com/mobile/react-native/fullcapture/set-element-properties/
- **Help Center**: https://help.fullstory.com/hc/en-us/articles/24236341468311-Extracted-Element-Properties
