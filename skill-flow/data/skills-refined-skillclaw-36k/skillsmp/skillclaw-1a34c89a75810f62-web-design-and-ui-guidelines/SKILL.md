---
name: web-design-and-ui-guidelines
description: Use this skill when you need to create accessible, responsive web interfaces that adhere to modern design principles and standards.
---

# Web Design and UI Guidelines

Modern web design principles for responsive layouts, accessibility, and visual hierarchy, combined with UI standards for semantic HTML and performance.

## When to Use

- Creating polished web interfaces
- Improving accessibility
- Implementing responsive design patterns
- Making visual hierarchy decisions
- Following non-negotiable design and UI standards

## Core Principles

1. **Users First** — Prioritize user needs, workflows, and ease of use.
2. **Meticulous Craft** — Ensure precision and polish in every UI element.
3. **Speed & Performance** — Aim for fast load times and snappy interactions.
4. **Simplicity & Clarity** — Maintain a clean interface with unambiguous labels.
5. **Focus & Efficiency** — Help users achieve their goals quickly.
6. **Consistency** — Use a uniform design language throughout.
7. **Accessibility (WCAG AA)** — Design inclusively for all users.
8. **Opinionated Defaults** — Thoughtful defaults reduce decision fatigue.

## Design System (Single Source of Truth)

### Critical Rules

1. **ALWAYS use design tokens** — NEVER use hardcoded values.
2. **All values come from `/styles/global.css`** — Maintain a single source of truth.
3. **No magic numbers** — Every color, spacing, size should use a CSS variable.

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

## Semantic HTML

### Required Practices

1. Use semantic tags: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`.
2. Use buttons for actions (`<button>`), links for navigation (`<a>`).
3. Forms should use `<form>`, `<label>`, `<input>`, `<select>`, `<textarea>`.
4. Lists should use `<ul>`, `<ol>`, `<li>` (not divs with bullets).
5. Headings should follow hierarchy: `<h1>` → `<h2>` → `<h3>` (no skipping).
6. Images must have descriptive `alt` text.
7. Tables should use proper markup for tabular data.

### Examples

```html
<!-- Example of semantic HTML -->
<article>
  <header>
    <h1>Article Title</h1>
  </header>
  <section>
    <h2>Section Title</h2>
    <p>This is a paragraph in the section.</p>
  </section>
  <footer>
    <p>Published on <time datetime="2023-01-01">January 1, 2023</time></p>
  </footer>
</article>
```