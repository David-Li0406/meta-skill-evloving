# RTL CSS Styling Reference

## Base RTL Stylesheet

```css
/* app/assets/stylesheets/rtl.css */

/* Base RTL styles */
[dir="rtl"] {
  text-align: right;
}

/* Flip flexbox and grid directions */
[dir="rtl"] .flex-row {
  flex-direction: row-reverse;
}

[dir="rtl"] .grid {
  direction: rtl;
}

/* Form alignment */
[dir="rtl"] .form-label {
  text-align: right;
}

[dir="rtl"] .form-input {
  text-align: right;
}

/* Keep certain inputs LTR */
[dir="rtl"] input[type="email"],
[dir="rtl"] input[type="url"],
[dir="rtl"] input[type="tel"],
[dir="rtl"] input[type="number"],
[dir="rtl"] input[dir="ltr"] {
  direction: ltr;
  text-align: left;
}

/* Navigation */
[dir="rtl"] .nav {
  flex-direction: row-reverse;
}

[dir="rtl"] .nav-item {
  margin-left: 0;
  margin-right: 1rem;
}

/* Buttons with icons */
[dir="rtl"] .btn-icon-start {
  flex-direction: row-reverse;
}

[dir="rtl"] .btn-icon-start svg {
  margin-left: 0.5rem;
  margin-right: 0;
}

/* Tables */
[dir="rtl"] table {
  direction: rtl;
}

[dir="rtl"] th,
[dir="rtl"] td {
  text-align: right;
}

/* Numbers in tables stay LTR for readability */
[dir="rtl"] .numeric,
[dir="rtl"] .currency,
[dir="rtl"] .date {
  direction: ltr;
  text-align: left;
}

/* Pagination */
[dir="rtl"] .pagination {
  flex-direction: row-reverse;
}

/* Sidebar */
[dir="rtl"] .sidebar {
  right: 0;
  left: auto;
  border-left: 1px solid var(--border-color);
  border-right: none;
}

/* Dropdowns */
[dir="rtl"] .dropdown-menu {
  right: 0;
  left: auto;
  text-align: right;
}

/* Modals */
[dir="rtl"] .modal-close {
  right: auto;
  left: 1rem;
}

/* Icons that should flip */
[dir="rtl"] .icon-arrow-left {
  transform: scaleX(-1);
}

[dir="rtl"] .icon-arrow-right {
  transform: scaleX(-1);
}

/* Margins and paddings - use logical properties */
.container {
  margin-inline-start: auto;
  margin-inline-end: auto;
  padding-inline-start: 1rem;
  padding-inline-end: 1rem;
}

/* Border radius for RTL */
[dir="rtl"] .rounded-start {
  border-radius: 0 0.25rem 0.25rem 0;
}

[dir="rtl"] .rounded-end {
  border-radius: 0.25rem 0 0 0.25rem;
}
```

---

## Tailwind RTL Logical Properties

```css
/* Tailwind RTL support with logical properties */
/* app/assets/stylesheets/tailwind-rtl.css */

/* Use with Tailwind - these utilities support both directions */
.ms-auto { margin-inline-start: auto; }
.me-auto { margin-inline-end: auto; }
.ms-0 { margin-inline-start: 0; }
.me-0 { margin-inline-end: 0; }
.ms-1 { margin-inline-start: 0.25rem; }
.me-1 { margin-inline-end: 0.25rem; }
.ms-2 { margin-inline-start: 0.5rem; }
.me-2 { margin-inline-end: 0.5rem; }
.ms-4 { margin-inline-start: 1rem; }
.me-4 { margin-inline-end: 1rem; }

.ps-0 { padding-inline-start: 0; }
.pe-0 { padding-inline-end: 0; }
.ps-1 { padding-inline-start: 0.25rem; }
.pe-1 { padding-inline-end: 0.25rem; }
.ps-2 { padding-inline-start: 0.5rem; }
.pe-2 { padding-inline-end: 0.5rem; }
.ps-4 { padding-inline-start: 1rem; }
.pe-4 { padding-inline-end: 1rem; }

.start-0 { inset-inline-start: 0; }
.end-0 { inset-inline-end: 0; }

.text-start { text-align: start; }
.text-end { text-align: end; }

.border-s { border-inline-start-width: 1px; }
.border-e { border-inline-end-width: 1px; }

.rounded-s { border-start-start-radius: 0.25rem; border-end-start-radius: 0.25rem; }
.rounded-e { border-start-end-radius: 0.25rem; border-end-end-radius: 0.25rem; }
```

---

## CSS Logical Properties Quick Reference

| Physical Property | Logical Property |
|-------------------|------------------|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `padding-right` | `padding-inline-end` |
| `left` | `inset-inline-start` |
| `right` | `inset-inline-end` |
| `text-align: left` | `text-align: start` |
| `text-align: right` | `text-align: end` |
| `border-left` | `border-inline-start` |
| `border-right` | `border-inline-end` |

---

## Elements That Should Stay LTR

Always keep these elements LTR even in RTL layouts:

1. **Email addresses**: `<input type="email" dir="ltr">`
2. **URLs**: `<input type="url" dir="ltr">`
3. **Phone numbers**: `<input type="tel" dir="ltr">`
4. **Numbers/Currency**: `<span dir="ltr">$1,234.56</span>`
5. **Code snippets**: `<code dir="ltr">`
6. **Technical identifiers**: Order IDs, SKUs, etc.

---

## Bidirectional Text Tips

```html
<!-- Use dir="auto" for user-generated content -->
<input type="text" dir="auto" />

<!-- Explicit direction for mixed content -->
<p>Your order number is <span dir="ltr">ORD-12345</span></p>

<!-- Arabic text wrapper -->
<span dir="rtl">مرحبًا بك</span>
```
