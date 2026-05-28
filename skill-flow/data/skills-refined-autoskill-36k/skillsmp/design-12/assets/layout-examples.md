# Layout Examples

## Overview

This guide provides ready-to-use layout patterns using CSS Grid and Flexbox. Copy and adapt these patterns for common UI needs.

---

## When to Use Grid vs Flexbox

| Use Case | Tool | Why |
|----------|------|-----|
| Page-level structure | **Grid** | Named areas, predictable slots |
| Two-dimensional layouts | **Grid** | Rows AND columns matter |
| Card grids with equal sizing | **Grid** | Consistent cell sizes |
| Navigation menus | **Flexbox** | Items flow in one direction |
| Centering content | **Flexbox** | Simple alignment |
| Distributing space | **Flexbox** | Flexible item sizing |
| Unknown number of items | **Flexbox** | Wrapping behavior |

**Rule of thumb:** Grid for structure, Flexbox for flow.

---

## Page Layouts

### Classic Header-Main-Footer

```css
.page-layout {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.header { /* First row - auto height */ }
.main { /* Middle row - fills remaining space */ }
.footer { /* Last row - auto height */ }
```

```html
<div class="page-layout">
  <header class="header">Header</header>
  <main class="main">Main Content</main>
  <footer class="footer">Footer</footer>
</div>
```

---

### Sidebar Layout (Named Areas)

```css
.app-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  min-height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }

/* Mobile: Stack everything */
@media (max-width: 1023px) {
  .app-layout {
    grid-template-columns: 1fr;
    grid-template-areas:
      "header"
      "main"
      "sidebar"
      "footer";
  }
}
```

```html
<div class="app-layout">
  <header class="header">Header</header>
  <aside class="sidebar">Sidebar Navigation</aside>
  <main class="main">Main Content</main>
  <footer class="footer">Footer</footer>
</div>
```

---

### Three-Column Layout

```css
.three-col {
  display: grid;
  grid-template-columns: 200px 1fr 300px;
  grid-template-areas:
    "header header header"
    "left-sidebar main right-sidebar"
    "footer footer footer";
  gap: var(--space-lg);
  min-height: 100vh;
}

.header { grid-area: header; }
.left-sidebar { grid-area: left-sidebar; }
.main { grid-area: main; }
.right-sidebar { grid-area: right-sidebar; }
.footer { grid-area: footer; }

/* Tablet: Two columns */
@media (max-width: 1279px) {
  .three-col {
    grid-template-columns: 200px 1fr;
    grid-template-areas:
      "header header"
      "left-sidebar main"
      "right-sidebar main"
      "footer footer";
  }
}

/* Mobile: Single column */
@media (max-width: 767px) {
  .three-col {
    grid-template-columns: 1fr;
    grid-template-areas:
      "header"
      "main"
      "left-sidebar"
      "right-sidebar"
      "footer";
  }
}
```

---

## Content Layouts

### Card Grid (Equal Columns)

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-lg);
}

.card {
  display: grid;
  grid-template-rows: auto 1fr auto;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.card__image { /* Auto height */ }
.card__content { padding: var(--space-md); }
.card__footer { padding: var(--space-md); border-top: 1px solid var(--color-border); }
```

```html
<div class="card-grid">
  <article class="card">
    <img class="card__image" src="..." alt="...">
    <div class="card__content">
      <h3>Card Title</h3>
      <p>Card description...</p>
    </div>
    <footer class="card__footer">
      <button>Action</button>
    </footer>
  </article>
  <!-- More cards... -->
</div>
```

---

### Masonry-Style Grid (CSS Only)

```css
.masonry {
  columns: 3;
  column-gap: var(--space-lg);
}

.masonry-item {
  break-inside: avoid;
  margin-bottom: var(--space-lg);
}

@media (max-width: 1023px) {
  .masonry { columns: 2; }
}

@media (max-width: 640px) {
  .masonry { columns: 1; }
}
```

---

### Two-Column Content (Article Style)

```css
.article-layout {
  display: grid;
  grid-template-columns: 1fr min(65ch, 100%) 1fr;
}

.article-layout > * {
  grid-column: 2;
}

/* Full-bleed elements */
.article-layout .full-bleed {
  grid-column: 1 / -1;
  width: 100%;
}
```

---

## Component Layouts

### Card Internal Structure

```css
.product-card {
  display: grid;
  grid-template-areas:
    "image"
    "content"
    "price"
    "actions";
  grid-template-rows: 200px 1fr auto auto;
  gap: var(--space-md);
  padding: var(--space-md);
}

.product-card__image { grid-area: image; object-fit: cover; }
.product-card__content { grid-area: content; }
.product-card__price { grid-area: price; font-weight: bold; }
.product-card__actions { grid-area: actions; }
```

---

### Form Layout

```css
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-lg);
}

/* Full width fields */
.form-grid .full-width {
  grid-column: 1 / -1;
}

/* Mobile: Single column */
@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
```

```html
<form class="form-grid">
  <div class="form-field">
    <label for="first">First Name</label>
    <input type="text" id="first">
  </div>
  <div class="form-field">
    <label for="last">Last Name</label>
    <input type="text" id="last">
  </div>
  <div class="form-field full-width">
    <label for="email">Email</label>
    <input type="email" id="email">
  </div>
  <div class="form-field full-width">
    <label for="message">Message</label>
    <textarea id="message"></textarea>
  </div>
</form>
```

---

### Modal Structure

```css
.modal {
  display: grid;
  grid-template-areas:
    "header"
    "body"
    "footer";
  grid-template-rows: auto 1fr auto;
  max-height: 90vh;
  width: min(500px, 90vw);
}

.modal__header {
  grid-area: header;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md);
  border-bottom: 1px solid var(--color-border);
}

.modal__body {
  grid-area: body;
  padding: var(--space-lg);
  overflow-y: auto;
}

.modal__footer {
  grid-area: footer;
  display: flex;
  justify-content: flex-end;
  gap: var(--space-sm);
  padding: var(--space-md);
  border-top: 1px solid var(--color-border);
}
```

---

## Flexbox Patterns

### Navigation Bar

```css
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md) var(--space-lg);
}

.navbar__brand {
  flex-shrink: 0;
}

.navbar__nav {
  display: flex;
  gap: var(--space-lg);
  list-style: none;
}

.navbar__actions {
  display: flex;
  gap: var(--space-sm);
}
```

```html
<nav class="navbar">
  <a class="navbar__brand" href="/">Logo</a>
  <ul class="navbar__nav">
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
    <li><a href="/products">Products</a></li>
  </ul>
  <div class="navbar__actions">
    <button>Login</button>
    <button>Sign Up</button>
  </div>
</nav>
```

---

### Centered Content

```css
/* Center horizontally and vertically */
.center-all {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

/* Center horizontally only */
.center-x {
  display: flex;
  justify-content: center;
}

/* Center vertically only */
.center-y {
  display: flex;
  align-items: center;
}
```

---

### Space Between Items

```css
/* Spread items to edges */
.spread {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Equal space around items */
.distribute {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
}
```

---

### Media Object (Icon + Content)

```css
.media {
  display: flex;
  gap: var(--space-md);
  align-items: flex-start;
}

.media__icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
}

.media__content {
  flex: 1;
  min-width: 0; /* Prevents overflow */
}
```

```html
<div class="media">
  <img class="media__icon" src="icon.svg" alt="">
  <div class="media__content">
    <h3>Title</h3>
    <p>Description text that might be long...</p>
  </div>
</div>
```

---

### Tag/Chip List

```css
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xs);
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--space-sm);
  background: var(--color-neutral-100);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
}
```

---

### Button Group

```css
.button-group {
  display: flex;
  gap: var(--space-sm);
}

/* Stacked on mobile */
@media (max-width: 640px) {
  .button-group {
    flex-direction: column;
  }

  .button-group .btn {
    width: 100%;
  }
}
```

---

## Utility Classes

```css
/* Flex utilities */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.items-center { align-items: center; }
.items-start { align-items: flex-start; }
.items-end { align-items: flex-end; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.justify-end { justify-content: flex-end; }

/* Gap utilities */
.gap-xs { gap: var(--space-xs); }
.gap-sm { gap: var(--space-sm); }
.gap-md { gap: var(--space-md); }
.gap-lg { gap: var(--space-lg); }
.gap-xl { gap: var(--space-xl); }

/* Grid utilities */
.grid { display: grid; }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
```

---

## Quick Reference

### Grid Properties

| Property | Purpose | Example |
|----------|---------|---------|
| `grid-template-columns` | Define column sizes | `200px 1fr 200px` |
| `grid-template-rows` | Define row sizes | `auto 1fr auto` |
| `grid-template-areas` | Name grid regions | `"header header"` |
| `gap` | Space between cells | `var(--space-md)` |
| `grid-column` | Span columns | `1 / -1` (full width) |
| `grid-row` | Span rows | `1 / 3` |

### Flexbox Properties

| Property | Purpose | Example |
|----------|---------|---------|
| `flex-direction` | Main axis direction | `row`, `column` |
| `justify-content` | Main axis alignment | `space-between` |
| `align-items` | Cross axis alignment | `center` |
| `flex-wrap` | Allow wrapping | `wrap` |
| `gap` | Space between items | `var(--space-md)` |
| `flex` | Item sizing | `1` (grow to fill) |
| `flex-shrink` | Prevent shrinking | `0` |
