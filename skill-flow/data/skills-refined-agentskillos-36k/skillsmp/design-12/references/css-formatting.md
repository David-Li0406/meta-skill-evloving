# CSS Formatting Guide

## Overview

CSS should be written for humans first, machines second. Readable code is maintainable code.

---

## File Organization

### Structure

```css
/* =================================================================
   1. VARIABLES & CUSTOM PROPERTIES
   ================================================================= */

/* =================================================================
   2. RESET & BASE STYLES
   ================================================================= */

/* =================================================================
   3. TYPOGRAPHY
   ================================================================= */

/* =================================================================
   4. LAYOUT COMPONENTS
   ================================================================= */

/* =================================================================
   5. UI COMPONENTS
   ================================================================= */

/* =================================================================
   6. UTILITIES
   ================================================================= */

/* =================================================================
   7. MEDIA QUERIES (Mobile-First)
   ================================================================= */
```

### Section Comments

Use consistent section headers for major sections:

```css
/* =================================================================
   BUTTONS
   ================================================================= */

/* Primary buttons
   ----------------------------------------------------------------- */

.btn-primary { ... }

/* Secondary buttons
   ----------------------------------------------------------------- */

.btn-secondary { ... }
```

---

## Property Order

Order properties logically by category. This makes it easy to find and understand what a rule does.

### Recommended Order

```css
.component {
  /* 1. Layout */
  display: flex;
  flex-direction: column;
  grid-template-columns: 1fr 1fr;

  /* 2. Position */
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: var(--z-modal);

  /* 3. Box Model */
  width: 100%;
  max-width: var(--container-md);
  height: auto;
  margin: var(--space-md);
  padding: var(--space-lg);

  /* 4. Typography */
  font-family: var(--font-family-body);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-normal);
  line-height: var(--line-height-normal);
  text-align: left;
  color: var(--color-text);

  /* 5. Visual */
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  opacity: 1;

  /* 6. Animation */
  transition: all var(--duration-fast) var(--easing-standard);
  animation: fade-in var(--duration-normal);

  /* 7. Misc */
  cursor: pointer;
  pointer-events: auto;
  overflow: hidden;
}
```

### Property Categories Reference

| Category | Properties |
|----------|-----------|
| **Layout** | display, flex-*, grid-*, gap, align-*, justify-* |
| **Position** | position, top, right, bottom, left, z-index |
| **Box Model** | width, height, margin, padding, box-sizing |
| **Typography** | font-*, text-*, line-height, color, letter-spacing |
| **Visual** | background, border, border-radius, box-shadow, opacity |
| **Animation** | transition, animation, transform |
| **Misc** | cursor, pointer-events, overflow, visibility |

---

## Spacing & Formatting

### One Property Per Line

```css
/* ✅ Good */
.card {
  display: flex;
  flex-direction: column;
  padding: var(--space-md);
  background: var(--color-surface);
}

/* ❌ Bad - Multiple properties on one line */
.card { display: flex; flex-direction: column; padding: var(--space-md); }
```

### Consistent Indentation

Use 2 spaces for indentation (configurable, but be consistent).

```css
/* ✅ Consistent indentation */
.parent {
  display: flex;
}

.parent .child {
  flex: 1;
}

/* Nested (in preprocessors) */
.parent {
  display: flex;

  .child {
    flex: 1;
  }
}
```

### Blank Lines Between Rule Sets

```css
/* ✅ Breathing room between rules */
.header {
  padding: var(--space-lg);
  background: var(--color-primary);
}

.header__title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
}

.header__subtitle {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

/* ❌ Cramped - hard to scan */
.header {
  padding: var(--space-lg);
  background: var(--color-primary);
}
.header__title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
}
.header__subtitle {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}
```

### Space After Colons

```css
/* ✅ Space after colon */
.element {
  color: var(--color-text);
  margin: var(--space-md);
}

/* ❌ No space after colon */
.element {
  color:var(--color-text);
  margin:var(--space-md);
}
```

---

## Naming Conventions

### BEM (Block Element Modifier)

```css
/* Block */
.card { }

/* Element (double underscore) */
.card__header { }
.card__body { }
.card__footer { }

/* Modifier (double dash) */
.card--featured { }
.card--compact { }

/* Element with modifier */
.card__header--highlighted { }
```

### Semantic Names

```css
/* ✅ Semantic - describes purpose */
.navigation-primary { }
.button-submit { }
.alert-error { }
.form-field { }

/* ❌ Non-semantic - describes appearance */
.blue-box { }
.left-column { }
.big-text { }
```

### Utility Classes

For single-purpose utilities, use clear prefixes:

```css
/* Spacing utilities */
.mt-sm { margin-top: var(--space-sm); }
.mb-md { margin-bottom: var(--space-md); }
.p-lg { padding: var(--space-lg); }

/* Text utilities */
.text-center { text-align: center; }
.text-bold { font-weight: var(--font-weight-bold); }

/* Display utilities */
.d-none { display: none; }
.d-flex { display: flex; }

/* Visibility utilities */
.sr-only { /* screen reader only */ }
.visually-hidden { /* hidden but in DOM */ }
```

---

## Design Tokens Usage

### ALWAYS Use Variables

```css
/* ✅ Uses design tokens */
.component {
  padding: var(--space-md);
  font-size: var(--font-size-body);
  color: var(--color-text-primary);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  transition: all var(--duration-fast) var(--easing-standard);
}

/* ❌ Hardcoded values */
.component {
  padding: 16px;           /* Should be var(--space-md) */
  font-size: 14px;         /* Should be var(--font-size-body) */
  color: #333333;          /* Should be var(--color-text-primary) */
  background: #ffffff;     /* Should be var(--color-surface) */
  border-radius: 8px;      /* Should be var(--radius-md) */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);  /* Should be var(--shadow-sm) */
  transition: all 150ms ease; /* Should use duration and easing vars */
}
```

### Acceptable Exceptions

These values may be hardcoded:
- `0` (zero needs no variable)
- `100%`, `50%` (percentage values for layouts)
- `1px` (minimum border width)
- `auto` (automatic sizing)
- `none`, `inherit`, `initial` (CSS keywords)

```css
.element {
  margin: 0;                    /* Zero is fine */
  width: 100%;                  /* Percentage is fine */
  border: 1px solid var(--color-border);  /* 1px border is fine */
  height: auto;                 /* CSS keywords are fine */
}
```

---

## Selector Best Practices

### Specificity

Keep specificity low. Avoid !important.

```css
/* ✅ Low specificity - easy to override */
.button { }
.button.is-active { }

/* ❌ High specificity - hard to override */
div.container section.content article.post button.button { }
#unique-button { }
.button { color: blue !important; }
```

### Avoid Over-Qualification

```css
/* ✅ Sufficient specificity */
.nav-link { }

/* ❌ Over-qualified */
ul.nav li.nav-item a.nav-link { }
```

### Avoid Tag Selectors for Styling

```css
/* ✅ Class-based styling */
.article-content p { }
.article-content blockquote { }

/* ❌ Global tag styles (except in resets) */
p { margin: 1em 0; }  /* Affects ALL paragraphs */
```

---

## Media Queries

### Mobile-First (min-width)

```css
/* Base styles (mobile) */
.grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

/* Tablet and up */
@media (min-width: 641px) {
  .grid {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .grid__item {
    flex-basis: calc(50% - var(--space-md));
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .grid__item {
    flex-basis: calc(33.333% - var(--space-md));
  }
}
```

### Grouping Media Queries

**Option 1:** Media queries at the end (by breakpoint)

```css
/* All base styles first */
.header { ... }
.nav { ... }
.content { ... }

/* Then all tablet adjustments */
@media (min-width: 641px) {
  .header { ... }
  .nav { ... }
  .content { ... }
}

/* Then all desktop adjustments */
@media (min-width: 1024px) {
  .header { ... }
  .nav { ... }
  .content { ... }
}
```

**Option 2:** Media queries inline (by component)

```css
.header {
  padding: var(--space-sm);
}

@media (min-width: 641px) {
  .header {
    padding: var(--space-md);
  }
}

@media (min-width: 1024px) {
  .header {
    padding: var(--space-lg);
  }
}
```

---

## Comments

### When to Comment

```css
/* ✅ Comment for complex calculations */
.container {
  /* 100vw minus sidebar (240px) minus gutters (2 × 16px) */
  max-width: calc(100vw - 240px - 32px);
}

/* ✅ Comment for workarounds/hacks */
.element {
  /* Safari fix for flexbox gap support */
  margin: calc(var(--space-md) / 2 * -1);
}

/* ✅ Comment for magic numbers that can't be avoided */
.tooltip {
  /* Arrow size is 8px, offset centers it */
  left: calc(50% - 4px);
}
```

### When NOT to Comment

```css
/* ❌ Obvious - comment adds nothing */
.button {
  /* Set the background color */
  background: var(--color-primary);

  /* Add padding */
  padding: var(--space-md);
}
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `!important` everywhere | Specificity wars | Reduce selector specificity |
| Deeply nested selectors | Hard to override | Flatten with BEM |
| ID selectors for styling | Too specific | Use classes |
| Inline styles | Can't reuse/override | Use classes |
| Magic numbers | No meaning | Use design tokens |
| Vendor prefixes manually | Easy to miss | Use Autoprefixer |
| Duplicate declarations | Bloat | Extract to shared class |

---

## Checklist

Before committing CSS:

- [ ] All values use design tokens (no hardcoded colors, sizes, spacing)
- [ ] Properties are ordered logically
- [ ] Selectors are as simple as possible
- [ ] No `!important` unless absolutely necessary
- [ ] Comments explain "why", not "what"
- [ ] Media queries use min-width (mobile-first)
- [ ] Classes use semantic BEM-style naming
- [ ] No duplicate declarations
- [ ] File is organized with clear sections
