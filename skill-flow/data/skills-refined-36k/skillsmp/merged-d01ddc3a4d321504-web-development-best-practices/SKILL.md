---
name: web-development-best-practices
description: Use this skill when writing semantic HTML and safe JavaScript for interactive web applications.
---

# Semantic HTML Guidelines

1. **Semantic Tags**: Use `<main>`, `<nav>`, `<header>`, `<footer>`, `<section>`, `<article>`. Avoid `<div>` for structural elements.
2. **Headings**: Ensure a logical heading hierarchy (H1 -> H2 -> H3).
3. **Alt Text**: All images must have descriptive `alt` attributes or empty `alt` for decorative images.

# Safe DOM Manipulation in JavaScript

## Rules

1. **Selectors**: Use `document.getElementById` for IDs (performance) and `querySelector` for classes.
2. **Content Modification**:
   - **FORBIDDEN**: `innerHTML` when inserting user data (risk of XSS).
   - **RECOMMENDED**: Use `textContent` for text, `classList` for styles.
   - For creating complex structures, use `document.createElement` and `appendChild` or `<template>` elements.
3. **Events**:
   - Use named functions for event handlers to allow removal (`removeEventListener`).
   - Apply event delegation for lists and dynamic elements.

## Accessibility (WCAG 2.2)

1. **Dragging Movements (2.5.7)**: If implementing Drag-and-Drop (e.g., list sorting), you MUST add "Up"/"Down" buttons or a context menu for reordering without dragging (single pointer alternative).

## Safe Event Listener Template

```javascript
const btn = document.getElementById("action-btn");
if (btn) {
  btn.addEventListener("click", handleClick);
}

function handleClick(event) {
  // logic
}
```