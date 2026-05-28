---
name: ui-ux-pro-max
description: Use this skill when you need comprehensive guidance on UI/UX design for web and mobile applications, including style selection, color palettes, typography, and accessibility.
---

# Skill body

## Overview

The UI/UX Pro Max skill provides a comprehensive design guide for web and mobile applications. It includes a searchable database of styles, color palettes, font pairings, chart types, and UX guidelines across various technology stacks.

## When to Apply

Reference these guidelines when:
- Designing new UI components or pages
- Choosing color palettes and typography
- Reviewing code for UX issues
- Building landing pages or dashboards
- Implementing accessibility requirements

## Rule Categories by Priority

| Priority | Category | Impact | Domain |
|----------|----------|--------|--------|
| 1 | Accessibility | CRITICAL | `ux` |
| 2 | Touch & Interaction | CRITICAL | `ux` |
| 3 | Performance | HIGH | `ux` |
| 4 | Layout & Responsive | HIGH | `ux` |
| 5 | Typography & Color | MEDIUM | `typography`, `color` |
| 6 | Animation | MEDIUM | `ux` |
| 7 | Style Selection | MEDIUM | `style`, `product` |
| 8 | Charts & Data | LOW | `chart` |

## Quick Reference

### 1. Accessibility (CRITICAL)

- **Color Contrast**: Minimum 4.5:1 ratio for normal text
- **Focus States**: Visible focus rings on interactive elements
- **Alt Text**: Descriptive alt text for meaningful images
- **ARIA Labels**: Use aria-label for icon-only buttons
- **Keyboard Navigation**: Tab order matches visual order
- **Form Labels**: Use label with for attribute

### 2. Touch & Interaction (CRITICAL)

- **Touch Target Size**: Minimum 44x44px touch targets
- **Hover vs Tap**: Use click/tap for primary interactions
- **Loading Buttons**: Disable button during async operations
- **Error Feedback**: Clear error messages near the problem
- **Cursor Pointer**: Use pointer cursor for clickable elements

## How to Use This Skill

When a user requests UI/UX work (design, build, create, implement, review, fix, improve), follow this workflow:

### Step 1: Analyze User Requirements

Extract key information from the user request:
- **Product Type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style Keywords**: Minimal, playful, professional, elegant, dark mode, etc.
- **Industry**: Healthcare, fintech, gaming, education, etc.
- **Stack**: React, Vue, Next.js, or default to `html-tailwind`

### Step 2: Search Relevant Domains

Use the search functionality to gather comprehensive information. Search until you have enough context.

```bash
python3 search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**Recommended Search Order**:
1. **Product** - Get style recommendations for product type
2. **Style** - Get detailed style guide (colors, effects, frameworks)
3. **Typography** - Get font pairings with Google Fonts imports
4. **Color** - Get color palette (Primary, Secondary, CTA, Background, Text, Border)
5. **Landing** - Get page structure (if landing page)
6. **Chart** - Get chart recommendations (if dashboard)