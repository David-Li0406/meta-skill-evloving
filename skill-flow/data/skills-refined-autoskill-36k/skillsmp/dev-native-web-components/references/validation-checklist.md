# Validation Checklist

> Complete checklist for validating native web components before commit.

---

## Pre-Commit Checklist

### Shadow DOM

- [ ] Uses `<template shadowrootmode="open">` (DSD)
- [ ] Never uses `attachShadow()` imperatively
- [ ] Slots have meaningful names or fallback content
- [ ] Uses `::part()` for external styling hooks
- [ ] Light DOM content is SEO-friendly

### CSS Units

- [ ] No `px` for layout (spacing, sizing, fonts)
- [ ] `px` only for borders, shadows, outlines (≤ 3px)
- [ ] Uses `rem` for spacing scale
- [ ] Uses `clamp()` for fluid typography
- [ ] Uses `cqi`/`cqw` for container-relative sizing
- [ ] Uses `dvh`/`svh` for viewport height (not `vh`)

### Container Queries

- [ ] Components use `container-type: inline-size`
- [ ] `@container` rules for component breakpoints
- [ ] `@media` only for page-level layout

### Native Features

- [ ] Uses `<details>` for accordions
- [ ] Uses `popover` for tooltips/menus
- [ ] Uses `<dialog>` for modals
- [ ] Uses `light-dark()` for color schemes
- [ ] Uses `@starting-style` for entry animations

### Accessibility

- [ ] Semantic HTML elements used
- [ ] `alt` text on images (or `alt=""` for decorative)
- [ ] Form inputs have associated labels
- [ ] Interactive elements have `:focus-visible` styles
- [ ] Color contrast ≥ 4.5:1 (text), ≥ 3:1 (large text)
- [ ] `prefers-reduced-motion` respected
- [ ] Keyboard navigable (Tab, Enter, Escape)

### Performance

- [ ] LCP image has `fetchpriority="high"`
- [ ] Below-fold images have `loading="lazy"`
- [ ] Images have `width`/`height` or `aspect-ratio`
- [ ] Scripts use `defer` or `type="module"`
- [ ] Animations use only `transform`/`opacity`

### Progressive Enhancement

- [ ] Component renders without JavaScript
- [ ] JS enhances, doesn't break functionality
- [ ] Fallbacks for unsupported features

---

## E2E Testing

> For comprehensive E2E testing, use the `playwright-testing` skill.

### Component Testing Checklist

- [ ] Component renders correctly in all target browsers
- [ ] Shadow DOM content is queryable with `internal:shadow` selector
- [ ] Slots receive projected content
- [ ] Interactive states work (hover, focus, click)
- [ ] Responsive behavior triggers at correct container widths
- [ ] Accessibility tests pass (axe-core integration)

### Quick Test Commands

```bash
# Run Playwright tests
npx playwright test

# Run with UI mode
npx playwright test --ui

# Run accessibility tests
npx playwright test --grep @a11y

# Visual regression
npx playwright test --update-snapshots
```

### Shadow DOM Test Pattern

```typescript
import { test, expect } from '@playwright/test';

test('my-card renders DSD content', async ({ page }) => {
  await page.goto('/components/my-card');
  
  // Query shadow DOM
  const shadow = page.locator('my-card').locator('internal:shadow=.content');
  await expect(shadow).toBeVisible();
  
  // Check slotted content
  const title = page.locator('my-card h2[slot="title"]');
  await expect(title).toHaveText('Expected Title');
});
```

### Related Resources

- See `playwright-testing` skill for full testing setup
- See [debugging.md](debugging.md) for Playwright MCP Server usage

---

## Browser Testing

| Browser | Version | Tested |
| ------- | ------- | ------ |
| Chrome  | 120+    | [ ]    |
| Edge    | 120+    | [ ]    |
| Firefox | 121+    | [ ]    |
| Safari  | 17.2+   | [ ]    |

---

## Lighthouse Thresholds

| Category       | Minimum Score |
| -------------- | ------------- |
| Performance    | 90            |
| Accessibility  | 100           |
| Best Practices | 100           |
| SEO            | 100           |

---

## Quick Commands

```bash
# Validate HTML
npx html-validate *.html

# Check accessibility
npx pa11y http://localhost:3000

# Lighthouse audit
npx lighthouse http://localhost:3000 --view
```

---

## Common Issues

### ❌ Imperative Shadow DOM

```javascript
// WRONG
this.attachShadow({ mode: "open" });
```

**Fix**: Use `<template shadowrootmode="open">`

### ❌ Pixel Units for Layout

```css
/* WRONG */
padding: 16px;
font-size: 14px;
```

**Fix**: Use `rem` or `clamp()`

### ❌ Media Queries for Components

```css
/* WRONG */
@media (min-width: 768px) {
  .card {
    ...;
  }
}
```

**Fix**: Use `@container`

### ❌ Custom Modal Implementation

```html
<!-- WRONG -->
<div class="modal" aria-hidden="true"></div>
```

**Fix**: Use `<dialog>` or `popover`

### ❌ Missing Focus Styles

```css
/* WRONG */
button:focus {
  outline: none;
}
```

**Fix**: Add `:focus-visible` styles

---

## Validation Script

```javascript
// validate-component.js
const rules = [
  {
    name: "no-attachShadow",
    pattern: /attachShadow/,
    message: "Use DSD instead of attachShadow()",
  },
  {
    name: "no-px-layout",
    pattern: /(?:padding|margin|gap|font-size|width|height):\s*\d+px/,
    message: "Use rem/cqi instead of px for layout",
  },
  {
    name: "has-dsd",
    pattern: /<template\s+shadowrootmode/,
    required: true,
    message: "Missing Declarative Shadow DOM",
  },
];
```

---

_Use this checklist for every component before merge._
