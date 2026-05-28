---
name: web-design-and-ui-guidelines
description: Use this skill for implementing modern web design principles, focusing on responsive layouts, accessibility, and UI standards.
---

# Web Design and UI Guidelines

This skill encompasses modern web design principles, including responsive layouts, accessibility, and user interface standards.

## When to Use

- Creating polished web interfaces
- Improving accessibility
- Implementing responsive design patterns
- Establishing visual hierarchy and UI standards

## Core Principles

1. **Users First** — Prioritize user needs, workflows, and ease of use.
2. **Meticulous Craft** — Ensure precision and polish in every UI element.
3. **Speed & Performance** — Aim for fast load times and snappy interactions.
4. **Simplicity & Clarity** — Maintain a clean interface with unambiguous labels.
5. **Focus & Efficiency** — Help users achieve goals quickly.
6. **Consistency** — Use a uniform design language throughout.
7. **Accessibility (WCAG AA)** — Design inclusively for all users.
8. **Opinionated Defaults** — Thoughtful defaults reduce decision fatigue.

## Design System (Single Source of Truth)

### Critical Rules

- **ALWAYS use design tokens** — Avoid hardcoded values.
- **All values come from a single source** — Use a designated CSS file for consistency.
- **No magic numbers** — Every value should utilize a CSS variable.

### Semantic HTML Practices

- Use semantic tags: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`.
- Ensure buttons are used for actions and links for navigation.
- Follow proper heading hierarchy and provide descriptive `alt` text for images.

### CSS Quality

- One property per line.
- Use design tokens, not hardcoded values.
- Maintain logical property order and use descriptive class names.

### Component States (Required)

All interactive components must have the following states:

| State | Requirement |
|-------|-------------|
| **Default** | Base appearance |
| **Hover** | Visual feedback on mouse over |
| **Active** | Visual feedback when pressed |
| **Focus** | Clear focus indicator for keyboard navigation |
| **Disabled** | Visually distinct, non-interactive |

### Accessibility (WCAG AA)

#### Required Standards

1. **Color Contrast** — Ensure minimum contrast ratios for text.
2. **Keyboard Navigation** — All functionality should be accessible via keyboard.
3. **Screen Reader Support** — Use proper ARIA labels and semantic HTML.
4. **Form Labels** — Ensure all inputs have associated labels.

### Responsive Design

#### Mobile-First Breakpoints

```css
/* Mobile: 0-640px (base styles) */

/* Tablet: 641px and up */
@media (min-width: 641px) { }

/* Desktop: 1024px and up */
@media (min-width: 1024px) { }

/* Large Desktop: 1280px and up */
@media (min-width: 1280px) { }
```

### Anti-Patterns (DO NOT DO THESE)

| Anti-Pattern | Why Bad | Do Instead |
|--------------|---------|------------|
| **Floating labels** | Confusing | Labels above inputs |
| **Inline validation** | Annoying | Validate on blur/submit |
| **Generic error messages** | Unhelpful | Specific, actionable errors |

### Quick Reference Checklist

- [ ] ALL values use design tokens.
- [ ] Semantic tags used appropriately.
- [ ] Color contrast meets WCAG AA standards.
- [ ] Mobile-first approach implemented.

## References

- `references/semantic-html.md` — Complete semantic HTML guide.
- `references/css-formatting.md` — CSS best practices.
- `references/accessibility-guide.md` — WCAG AA compliance.
- `references/responsive-breakpoints.md` — Responsive design patterns.

## Assets

- `assets/component-states-checklist.md` — State implementation guide.
- `assets/anti-patterns.md` — Detailed anti-pattern explanations.
- `assets/layout-examples.md` — CSS Grid and Flexbox examples.

## Scripts

- `scripts/validate_design_tokens.py` — Check for hardcoded values.
- `scripts/check_accessibility.py` — Basic accessibility validation.