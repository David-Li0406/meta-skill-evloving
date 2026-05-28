---
name: fullstory-stable-selectors
version: v3
description: Platform-agnostic guide for implementing stable, semantic identifiers in web and mobile applications. Solves the dynamic identifier problem across all platforms. Core concepts apply universally; see SKILL-WEB.md for web implementation and SKILL-MOBILE.md for iOS, Android, Flutter, and React Native patterns.
platforms: [web, ios, android, flutter, react-native]
implementation_files: [SKILL-WEB.md, SKILL-MOBILE.md]
related_skills:
  - fullstory-element-properties
  - fullstory-privacy-controls
  - fullstory-getting-started
  - fullstory-test-automation
  - universal-data-scoping-and-decoration
---

# Fullstory Stable Selectors

> **📱 Platform-Specific Implementation**: This document covers core concepts. For implementation details, see:
> - **Web (JavaScript/TypeScript)**: [SKILL-WEB.md](./SKILL-WEB.md) — React, Vue, Angular, Svelte, Next.js, and more
> - **Mobile**: [SKILL-MOBILE.md](./SKILL-MOBILE.md) — iOS, Android, Flutter, React Native

---

## Overview

Modern applications—both web and mobile—often have **dynamic, unpredictable element identifiers** that change across builds, deployments, or even at runtime. This creates challenges for:

1. **Fullstory**: Reliable search, defined elements, heatmaps
2. **Automated Testing**: Stable E2E test selectors
3. **Computer User Agents (CUA)**: AI agents navigating your interface
4. **Accessibility Tools**: Programmatic element identification

**The Solution**: Add stable, semantic identifiers that describe **what** the element is, not how it's rendered.

---

## The Universal Problem

### Web: Dynamic CSS Classes

```html
<!-- What your code looks like -->
<button className={styles.primaryButton}>Add to Cart</button>

<!-- What renders in the browser -->
<button class="Button_primaryButton__x7Ks2">Add to Cart</button>
                                    ↑
                        This hash changes every build!
```

### Mobile: Dynamic View IDs

```
iOS View Hierarchy:
UIButton (0x7f8b4c0123a0)    ← Memory address changes every launch
  └── "Add to Cart"

Android View Tree:
Button (id: view-12345)       ← Auto-generated, unstable
  └── "Add to Cart"

React Native Bridge:
ReactButton (nativeID: rn_7)  ← Bridge-generated, changes on re-render
```

### Impact Across Platforms

| Tool | Web Problem | Mobile Problem |
|------|-------------|----------------|
| **Fullstory** | CSS selectors break | View tree queries unreliable |
| **E2E Testing** | Cypress/Playwright tests brittle | Detox/Espresso tests break |
| **AI Agents (CUA)** | Cannot find elements | Cannot navigate reliably |
| **Automation** | Scripts fail on deploy | Scripts fail on app update |

---

## Why This Matters for AI Agents (CUA)

Computer User Agents—AI systems that interact with digital interfaces—rely on stable, semantic identifiers to understand and navigate your application.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  HOW CUAs "SEE" YOUR INTERFACE                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ❌ BRITTLE (AI struggles):                                             │
│                                                                         │
│     Web: <button class="sc-3d8f2a btn_primary__xK7n2">                 │
│     iOS: UIButton at memory 0x7f8b4c0123a0                             │
│     Android: view-12345                                                 │
│                                                                         │
│  ✅ SEMANTIC (AI understands):                                          │
│                                                                         │
│     Web: data-component="ProductCard" data-element="purchase-button"   │
│     iOS: accessibilityIdentifier = "ProductCard.purchase-button"       │
│     Android: testTag = "ProductCard.purchase-button"                   │
│                                                                         │
│  The AI can now reliably:                                               │
│  • Find "the purchase button in ProductCard"                           │
│  • Understand the action it will trigger                               │
│  • Maintain stable automation across deployments                        │
└─────────────────────────────────────────────────────────────────────────┘
```

**Stable selectors provide CUAs with:**
- ✅ Consistent element identification across builds
- ✅ Semantic understanding of element purpose
- ✅ Hierarchical context (component → element relationship)
- ✅ Action hints for interaction planning

---

## The Universal Solution

Add stable identifiers that survive build changes and runtime variations:

| Platform | Stable Identifier Mechanism |
|----------|----------------------------|
| **Web** | `data-component`, `data-element`, `data-action` attributes |
| **iOS** | `accessibilityIdentifier` property |
| **Android (Kotlin)** | `contentDescription` or resource ID |
| **Android (Compose)** | `testTag` modifier, `semantics` |
| **React Native** | `testID` prop |
| **Flutter** | `Key`, `Semantics` widget |

**The naming conventions are the same across all platforms** — only the implementation mechanism differs.

---

## Core Concepts

### The Identifier Taxonomy

#### Primary Identifiers (Required)

| Concept | Purpose | Naming Convention | Example |
|---------|---------|-------------------|---------|
| **Component** | Component/screen boundary | PascalCase | `ProductCard`, `CheckoutForm` |
| **Element** | Element role within component | kebab-case | `add-to-cart`, `price-display` |

#### Extended Identifiers (Recommended for CUA/AI)

| Concept | Purpose | When to Use |
|---------|---------|-------------|
| **Action** | Describes what happens on interaction | Buttons, links, toggles |
| **State** | Current state of the element | Expandable, toggleable elements |
| **Variant** | Visual or functional variant | A/B tests, feature flags |

### Identifier Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SEMANTIC HIERARCHY (applies to all platforms)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Component: "CheckoutForm"                      ← Component boundary    │
│  │                                                                      │
│  ├── Element: "shipping-section"                ← Structural element   │
│  │   ├── Element: "address-input"               ← Interactive element  │
│  │   └── Element: "city-input"                                         │
│  │                                                                      │
│  ├── Element: "payment-section"                                        │
│  │   └── Element: "card-input"                                         │
│  │       Action: "capture-payment"              ← Action hint for AI   │
│  │                                                                      │
│  └── Element: "submit-button"                                          │
│      Action: "complete-purchase"                ← Action hint for AI   │
│      State: "enabled|disabled|loading"          ← Current state        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Platform Implementation Quick Reference

| Concept | Web | iOS | Android | React Native | Flutter |
|---------|-----|-----|---------|--------------|---------|
| Component | `data-component="X"` | `accessibilityIdentifier = "X"` | `testTag("X")` | `testID="X"` | `Key("X")` |
| Element | `data-element="x"` | `.x` suffix | `.x` suffix | `.x` suffix | `.x` suffix |
| Combined | `data-component="ProductCard"` + `data-element="add-to-cart"` | `"ProductCard.add-to-cart"` | `"ProductCard.add-to-cart"` | `"ProductCard.add-to-cart"` | `Key("ProductCard.add-to-cart")` |

---

## Naming Conventions (Universal)

These naming conventions apply to **all platforms**.

### Formal Naming Grammar

```
┌─────────────────────────────────────────────────────────────────────────┐
│  NAMING GRAMMAR                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Component: [Namespace.]<Domain><Type>                                  │
│                                                                         │
│    Examples:                                                            │
│    • ProductCard         (simple)                                       │
│    • CheckoutPaymentForm (domain + type)                               │
│    • Checkout.PaymentForm (namespaced for micro-frontends/modules)     │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Element: <subject>-<descriptor>[-<qualifier>]                          │
│                                                                         │
│    Examples:                                                            │
│    • add-to-cart         (action verb)                                  │
│    • product-image       (subject + type)                              │
│    • shipping-address-input (subject + descriptor + type)              │
│    • nav-item-products   (type + qualifier)                            │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Action: <verb>[-<object>]                                              │
│                                                                         │
│    Examples:                                                            │
│    • add-item                                                           │
│    • submit-form                                                        │
│    • toggle-menu                                                        │
│    • expand-details                                                     │
│    • navigate-next                                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Component Names

Use **PascalCase** matching your component/class/screen names:

```
✅ GOOD: Matches component names
• ProductCard
• CheckoutForm
• NavigationHeader
• UserProfileDropdown

✅ GOOD: Namespaced for modules
• Checkout.PaymentForm
• Catalog.ProductCard

❌ BAD: Generic names
• Container
• Wrapper
• Component
• View
• Screen
```

### Element Names

Use **kebab-case** describing the element's purpose:

```
✅ GOOD: Describes purpose
• add-to-cart
• email-input
• product-image
• price-display
• main-navigation

✅ GOOD: Qualified names for disambiguation
• billing-address-line1
• shipping-address-line1

❌ BAD: Describes appearance or position
• blue-button
• big-button
• button-1
• first-button
• left-sidebar
```

### Action Names

Use **verb-first kebab-case** describing the outcome:

```
✅ GOOD: Clear action verbs
• add-item
• submit-order
• toggle-filter
• navigate-category
• expand-details

❌ BAD: Nouns or unclear
• cart
• click-handler
• button-action
```

---

## What to Annotate

### Always Annotate

- ✅ **Buttons and tappable elements** — Primary interaction points
- ✅ **Form inputs** — Text fields, selects, checkboxes, toggles
- ✅ **Links and navigation items** — Navigation paths
- ✅ **Cards and list items** — Items in repeating content
- ✅ **Modals and dialog triggers** — State-changing interactions
- ✅ **Tab and accordion controls** — Content switchers

### Skip Annotation For

- ❌ **Pure layout containers** — Unless interactive
- ❌ **Styling wrappers** — Divs/Views for styling only
- ❌ **Text-only elements** — Unless key analytics content

---

## Best Practices

### 1. Annotate at Development Time

Add identifiers as you write components, not as an afterthought. This ensures complete coverage.

### 2. Document Your Conventions

Create a team style guide covering:
- Component naming patterns
- Element naming patterns
- Required annotations
- Platform-specific implementation

### 3. Combine with Privacy Controls

Stable identifiers and privacy controls work together:
- Annotate sensitive elements for searchability
- Apply privacy masking/exclusion for data protection
- Both serve complementary purposes

### 4. Use Consistent Depth

Don't over-nest annotations:

```
✅ GOOD: Flat, specific identifiers
ProductCard
  └── add-to-cart

❌ BAD: Unnecessarily deep
App
  └── MainContent
        └── ProductSection
              └── ProductCard
                    └── add-to-cart
```

### 5. Use Business Identifiers, Not Positions

For lists and repeating content:

```
✅ GOOD: Business identifier
product-item with productId="SKU-123"

❌ BAD: Position-based
item-0, item-1, item-2
```

---

## Integration with Accessibility

Stable selectors complement accessibility attributes:

| Attribute Type | Purpose | Audience |
|----------------|---------|----------|
| **Stable identifiers** | Programmatic targeting | Fullstory, Tests, AI Agents |
| **Accessibility labels** | Human-readable description | Screen readers, AI understanding |
| **Semantic roles** | Element type/behavior | Accessibility, AI categorization |

**Best Practice**: Use BOTH stable identifiers AND accessibility attributes. They serve complementary purposes.

---

## Troubleshooting

### Identifiers Not Working

**Common issues across all platforms:**
1. Identifier not set on the element (verify in inspector/debugger)
2. Typos in identifier names
3. Build tools stripping identifiers in production
4. Conditional rendering removing elements

### Too Many Search Results

**Problem:** Searching for "button" returns hundreds of results

**Solution:** Be more specific with hierarchical identifiers:
- Use `ProductCard.add-to-cart` not just `add-to-cart`
- Combine component + element for unique targeting

### Identifiers Stripped in Production

**Check platform-specific build configurations:**
- Web: Verify `data-*` attributes aren't removed by minifiers
- Mobile: Ensure debug-only code isn't stripping identifiers

---

## KEY TAKEAWAYS FOR AGENT

When helping developers implement stable selectors:

### Platform Routing

1. **Detect platform first** — Web vs iOS vs Android vs React Native vs Flutter
2. **Route to implementation file** — SKILL-WEB.md or SKILL-MOBILE.md
3. **Use consistent naming** — Same taxonomy applies to all platforms

### Core Principles (All Platforms)

1. **Name by purpose, not appearance**: "add-to-cart" not "blue-button"
2. **Use hierarchical identifiers**: Component.element pattern
3. **Annotate interactive elements**: Buttons, inputs, links, cards in lists
4. **Combine with accessibility**: Stable IDs + ARIA/accessibility labels
5. **Business IDs, not positions**: `productId="SKU-123"` not `item-0`

### Questions to Ask Developers

1. "What platform(s) are you building for?" (Web, iOS, Android, React Native, Flutter)
2. "Are your element identifiers stable across builds?"
3. "What elements do you need to reliably find in Fullstory?"
4. "Do you have a naming convention for components/screens?"
5. "Are you using E2E testing tools?"
6. "Is AI/automation tooling on your roadmap?"

### Implementation Checklist (All Platforms)

```markdown
Phase 1: Core Implementation
□ Identify interactive elements that need tracking
□ Establish naming convention (Component.element pattern)
□ Add component identifiers to screens/component roots
□ Add element identifiers to buttons, inputs, links, cards
□ Use specific, purpose-based names
□ Verify identifiers survive production build
□ Test in Fullstory search

Phase 2: AI/CUA Readiness
□ Add action hints to interactive elements
□ Add state indicators for stateful elements
□ Ensure accessibility attributes complement stable IDs
□ Document naming conventions for team consistency

Phase 3: Enterprise Scale
□ Implement type-safe identifier helpers
□ Add namespace prefixes for modules/teams
□ Add variant tracking for A/B tests
□ Configure E2E tools to use stable identifiers
```

---

## REFERENCE LINKS

### Fullstory Documentation
- **Element Properties**: ../core/fullstory-element-properties/SKILL.md
- **Privacy Controls**: ../core/fullstory-privacy-controls/SKILL.md
- **Test Automation**: ./fullstory-test-automation/SKILL.md

### Platform-Specific Implementation
- **Web Implementation**: [SKILL-WEB.md](./SKILL-WEB.md)
- **Mobile Implementation**: [SKILL-MOBILE.md](./SKILL-MOBILE.md)

### Accessibility Standards
- **WAI-ARIA Authoring Practices**: https://www.w3.org/WAI/ARIA/apg/
- **iOS Accessibility**: https://developer.apple.com/accessibility/
- **Android Accessibility**: https://developer.android.com/guide/topics/ui/accessibility

---

*This skill provides the universal foundation for stable selectors across all platforms. See SKILL-WEB.md for web implementation and SKILL-MOBILE.md for mobile implementation.*
