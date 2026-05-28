---
name: design
description: Design and UI standards for accessibility, semantic HTML, and responsive layouts
user-invocable: false
---

# Design Skill

**Version:** 1.0
**Source:** Design Standards

> Non-negotiable design and user interface standards. These are not preferences—they are requirements.

---

## Core Principles

1. **Users First** — Prioritize user needs, workflows, and ease of use
2. **Meticulous Craft** — Precision and polish in every UI element
3. **Speed & Performance** — Fast load times, snappy interactions
4. **Simplicity & Clarity** — Clean interface, unambiguous labels
5. **Focus & Efficiency** — Help users achieve goals quickly
6. **Consistency** — Uniform design language throughout
7. **Accessibility (WCAG AA)** — Inclusive design for all users
8. **Opinionated Defaults** — Thoughtful defaults reduce decision fatigue

---

## Design System (Single Source of Truth)

### Critical Rules

1. **ALWAYS use design tokens** — NEVER use hardcoded values
2. **All values come from `/styles/global.css`** — Single source of truth
3. **No magic numbers** — Every color, spacing, size uses a CSS variable

### Examples

```css
/* ✅ Correct - Uses design tokens */
.button {
  padding: var(--space-sm) var(--space-md);
  font-size: var(--font-size-body);
  background: var(--color-primary);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
}

/* ❌ Wrong - Hardcoded values */
.button {
  padding: 8px 16px;           /* Use var(--space-sm) var(--space-md) */
  font-size: 14px;             /* Use var(--font-size-body) */
  background: #3B82F6;         /* Use var(--color-primary) */
  border-radius: 4px;          /* Use var(--radius-sm) */
}
```

### What the Design System Contains

- Complete color palette (neutrals, semantic, dark mode)
- Full typography scale (fonts, sizes, weights, line heights)
- Spacing system (8px base)
- Border radii
- Shadows
- Z-index layers
- Animation durations and easings
- Icon sizes
- Breakpoint values

---

## Semantic HTML

### Required Practices

1. Use semantic tags: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`
2. Buttons for actions (`<button>`), links for navigation (`<a>`)
3. Forms use `<form>`, `<label>`, `<input>`, `<select>`, `<textarea>`
4. Lists use `<ul>`, `<ol>`, `<li>` (not divs with bullets)
5. Headings follow hierarchy: `<h1>` → `<h2>` → `<h3>` (no skipping)
6. Images have descriptive `alt` text
7. Tables use proper markup for tabular data

### Examples

```html
<!-- ✅ Good - Semantic HTML -->
<article class="product-card">
  <header>
    <h2>Product Name</h2>
  </header>
  <img src="..." alt="Product description">
  <p>Product description goes here.</p>
  <footer>
    <button type="button">Add to Cart</button>
  </footer>
</article>

<!-- ❌ Bad - Non-semantic divs -->
<div class="prd-crd">
  <div class="hdr">
    <div class="ttl">Product Name</div>
  </div>
  <div class="img"></div>
  <div class="btn">Add to Cart</div>
</div>
```

---

## CSS Quality

### Formatting Rules

1. One property per line
2. Use design tokens (CSS variables), not hardcoded values
3. Logical property order: layout → positioning → box model → typography → visual → animations
4. Descriptive class names (BEM or semantic naming)
5. Generous spacing between rule sets
6. Comments for complex sections

### Example

```css
/* ✅ Good - Human-readable */
.product-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  padding: var(--space-lg);
  background-color: var(--color-neutral-50);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.product-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
  transition: all var(--duration-fast) var(--easing-standard);
}
```

---

## Component States (Required)

All interactive components MUST have these five states:

| State | Requirement | Example |
|-------|-------------|---------|
| **Default** | Base appearance | Normal button |
| **Hover** | Visual feedback on mouse over | Background darkens |
| **Active** | Visual feedback when pressed | Slight scale down |
| **Focus** | Clear focus indicator (keyboard nav) | Blue outline ring |
| **Disabled** | Visually distinct, non-interactive | Grayed out, low opacity |

---

## Layout Philosophy

### CSS Grid vs Flexbox

| Layout Need | Tool | Example |
|-------------|------|---------|
| Page structure | **Grid (named areas)** | Header, sidebar, main, footer |
| Section layout | **Grid (named areas)** | Two-column content, form layout |
| Component structure | **Grid (named areas)** | Card internals, modal layout |
| Navigation items | **Flexbox** | Top nav items, menu items |
| Gallery/flowing items | **Flexbox** | Image grid, card gallery, tag list |

**Default to Grid for structure.** Use Flexbox when items need to flow, distribute, or wrap.

### Grid with Named Areas (Primary Layout Method)

```css
#app-layout {
  display: grid;
  grid-template-columns: 200px 1fr;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  gap: var(--space-md);
}

#header { grid-area: header; }
#sidebar { grid-area: sidebar; }
#main { grid-area: main; }
#footer { grid-area: footer; }
```

### White Space

- Use ample negative space to improve clarity
- Consistent spacing using design tokens

---

## Accessibility (WCAG AA)

### Required Standards

1. **Color Contrast**
   - Normal text: 4.5:1 minimum
   - Large text (18px+): 3:1 minimum

2. **Keyboard Navigation**
   - All functionality available via keyboard
   - Logical tab order
   - Focus indicators visible

3. **Screen Reader Support**
   - Proper ARIA labels
   - Semantic HTML
   - Skip links for navigation

4. **Form Labels**
   - All inputs have associated labels
   - Error messages linked to inputs

### Respect User Preferences

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Responsive Design

### Mobile-First Breakpoints

```css
/* Mobile: 0-640px (base styles, no media query needed) */

/* Tablet: 641px and up */
@media (min-width: 641px) { }

/* Desktop: 1024px and up */
@media (min-width: 1024px) { }

/* Large Desktop: 1280px and up */
@media (min-width: 1280px) { }
```

**Never use:** `@media (max-width: ...)` — Always use min-width (mobile-first)

### Container max-widths

- Mobile: 100% (with padding)
- Tablet: 640px
- Desktop: 1024px
- Large: 1280px

---

## Premium UI Philosophy

We follow S-Tier SaaS standards (Stripe, Airbnb, Linear):

- Sophisticated typography with perfect spacing
- Premium color palettes with subtle gradients
- Purposeful animations (150-300ms)
- Delightful micro-interactions
- Meticulous attention to detail

**Goal:** Make every interface feel premium. Subtle sophistication over flashy effects.

---

## Anti-Patterns (DO NOT DO THESE)

| Anti-Pattern | Why Bad | Do Instead |
|--------------|---------|------------|
| **Floating labels** | Confusing | Labels above inputs |
| **Inline validation** | Annoying | Validate on blur/submit |
| **Generic error messages** | Unhelpful | Specific, actionable errors |
| **Tooltips for critical info** | Easy to miss | Show directly |
| **Disabled buttons without explanation** | Frustrating | Show why disabled |
| **Custom scrollbars** | Inconsistent UX | System scrollbars |
| **Hamburger menu on desktop** | Hides navigation | Full nav on desktop |

---

## Quick Reference Checklist

### Design System

- [ ] ALL values use design tokens
- [ ] No magic numbers or hardcoded colors
- [ ] Design system is source of truth

### Semantic HTML

- [ ] Semantic tags used appropriately
- [ ] Buttons for actions, links for navigation
- [ ] Heading hierarchy followed
- [ ] Alt text on all images

### CSS

- [ ] Human-readable formatting
- [ ] Design tokens used throughout
- [ ] Logical property order

### Component States

- [ ] Default state implemented
- [ ] Hover state implemented
- [ ] Active state implemented
- [ ] Focus state implemented
- [ ] Disabled state implemented

### Accessibility

- [ ] Color contrast meets WCAG AA
- [ ] Keyboard navigation works
- [ ] Screen reader tested
- [ ] Focus indicators visible
- [ ] Form labels present

### Responsive

- [ ] Mobile-first approach
- [ ] Standard breakpoints used
- [ ] Works on all screen sizes

### Anti-Patterns Avoided

- [ ] No floating labels
- [ ] No inline validation
- [ ] No generic errors
- [ ] No tooltips for critical info
- [ ] No unexplained disabled buttons
- [ ] No custom scrollbars
- [ ] No hamburger on desktop

---

## References

- `references/semantic-html.md` — Complete semantic HTML guide
- `references/css-formatting.md` — CSS best practices
- `references/accessibility-guide.md` — WCAG AA compliance
- `references/responsive-breakpoints.md` — Responsive design patterns

## Assets

- `assets/component-states-checklist.md` — State implementation guide
- `assets/anti-patterns.md` — Detailed anti-pattern explanations
- `assets/layout-examples.md` — CSS Grid and Flexbox examples

## Scripts

- `scripts/validate_design_tokens.py` — Check for hardcoded values
- `scripts/check_accessibility.py` — Basic a11y validation
