# Baseline Features Reference

> Complete matrix of baseline web platform features for 2025, 2024, and 2023. Use the **newest** available feature that meets your baseline target.

---

## Baseline 2025 Features (Newly Available)

| Feature                 | Category | Use Case                         | Chrome | Firefox | Safari | Usage             |
| ----------------------- | -------- | -------------------------------- | ------ | ------- | ------ | ----------------- |
| `@scope`                | CSS      | Scoped styles without Shadow DOM | 118+   | 135+    | 17.4+  | Component styling |
| `::details-content`     | CSS      | Style/animate details content    | 131+   | 135+    | 18.2+  | Accordions        |
| `view-transition-class` | CSS      | Group view transitions           | 125+   | 135+    | 18.0+  | Navigation        |
| `scrollend` event       | JS       | Detect scroll completion         | 114+   | 109+    | 18.0+  | Infinite scroll   |
| `scrollbar-color`       | CSS      | Scrollbar theming                | 121+   | 64+     | 18.0+  | Custom scrollbars |
| `content-visibility`    | CSS      | Render optimization              | 85+    | 125+    | 18.0+  | Performance       |
| `dialog.requestClose()` | JS       | Close dialog with close event    | 132+   | 135+    | 18.2+  | Modal close       |

### @scope Example

```css
/* Scope styles to .card, but not inside .card-content */
@scope (.card) to (.card-content) {
  :scope {
    display: grid;
    gap: 1rem;
    padding: 1.5rem;
    border-radius: 0.75rem;
    background: var(--surface);
  }

  h2 {
    font-size: clamp(1.25rem, 3cqi, 2rem);
    margin: 0;
  }

  p {
    color: var(--text-muted);
    margin: 0;
  }
}
```

### ::details-content Example

```css
details {
  border: 1px solid var(--border);
  border-radius: 0.5rem;

  &::details-content {
    block-size: 0;
    overflow-y: clip;
    transition: block-size 0.3s ease, content-visibility 0.3s ease
        allow-discrete;
  }

  &[open]::details-content {
    block-size: auto;
  }
}

summary {
  padding: 1rem;
  cursor: pointer;
  list-style: none;

  &::marker {
    display: none;
  }

  &::after {
    content: "+";
    float: right;
    transition: rotate 0.3s;
  }
}

details[open] > summary::after {
  rotate: 45deg;
}
```

---

## Baseline 2024 Features

| Feature                | Category | Use Case                | Chrome | Firefox | Safari | Usage           |
| ---------------------- | -------- | ----------------------- | ------ | ------- | ------ | --------------- |
| Declarative Shadow DOM | HTML     | SSR web components      | 111+   | 123+    | 16.4+  | **REQUIRED**    |
| Popover API            | HTML     | Tooltips, menus, toasts | 114+   | 125+    | 17.0+  | **REQUIRED**    |
| `@starting-style`      | CSS      | Entry animations        | 117+   | 129+    | 17.5+  | Transitions     |
| `transition-behavior`  | CSS      | Discrete transitions    | 117+   | 129+    | 17.4+  | Display changes |
| `light-dark()`         | CSS      | Color scheme values     | 123+   | 120+    | 17.5+  | Dark mode       |
| `text-wrap: balance`   | CSS      | Balanced text lines     | 114+   | 121+    | 17.5+  | Headlines       |
| `@property`            | CSS      | Typed custom properties | 85+    | 128+    | 16.4+  | Animations      |
| Relative colors        | CSS      | Color manipulation      | 119+   | 128+    | 18.0+  | Themes          |

### Declarative Shadow DOM Example

```html
<my-tooltip>
  <template shadowrootmode="open">
    <style>
      :host {
        position: relative;
        display: inline-block;
      }

      .content {
        position: absolute;
        inset-area: top;
        margin-bottom: 0.5rem;
        padding: 0.5rem 0.75rem;
        background: var(--tooltip-bg, #333);
        color: var(--tooltip-fg, #fff);
        border-radius: 0.25rem;
        font-size: 0.875rem;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.2s;
      }

      :host(:hover) .content,
      :host(:focus-within) .content {
        opacity: 1;
      }
    </style>
    <slot></slot>
    <div class="content" role="tooltip">
      <slot name="tooltip">Tooltip text</slot>
    </div>
  </template>
  <button>Hover me</button>
  <span slot="tooltip">Custom tooltip content</span>
</my-tooltip>
```

### Popover API Example

```html
<!-- Auto-dismiss popover (menu, tooltip) -->
<button popovertarget="menu" popovertargetaction="toggle">Menu ▾</button>
<nav id="menu" popover>
  <a href="/home">Home</a>
  <a href="/about">About</a>
  <a href="/contact">Contact</a>
</nav>

<!-- Manual popover (toast, notification) -->
<div id="toast" popover="manual">
  Saved successfully!
  <button popovertarget="toast" popovertargetaction="hide">×</button>
</div>

<style>
  [popover] {
    margin: 0;
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    padding: 0;
    box-shadow: 0 4px 16px #0002;

    /* Entry animation */
    opacity: 0;
    transform: translateY(-0.5rem);
    transition: opacity 0.2s, transform 0.2s, display 0.2s allow-discrete, overlay
        0.2s allow-discrete;
  }

  [popover]:popover-open {
    opacity: 1;
    transform: translateY(0);
  }

  /* Starting style for entry */
  @starting-style {
    [popover]:popover-open {
      opacity: 0;
      transform: translateY(-0.5rem);
    }
  }
</style>
```

### light-dark() Example

```css
:root {
  color-scheme: light dark;

  /* Automatically switches based on color-scheme */
  --bg: light-dark(#ffffff, #0a0a0a);
  --fg: light-dark(#1a1a1a, #f0f0f0);
  --surface: light-dark(#f5f5f5, #1a1a1a);
  --border: light-dark(#e0e0e0, #333);
  --accent: light-dark(#0066cc, #66b3ff);
  --text-muted: light-dark(#666, #999);
}

body {
  background: var(--bg);
  color: var(--fg);
}
```

---

## Baseline 2023 Features

| Feature           | Category | Use Case                   | Chrome | Firefox | Safari | Usage               |
| ----------------- | -------- | -------------------------- | ------ | ------- | ------ | ------------------- |
| Container queries | CSS      | Component-level responsive | 105+   | 110+    | 16.0+  | **REQUIRED**        |
| `:has()`          | CSS      | Parent/sibling selector    | 105+   | 121+    | 15.4+  | State-based styling |
| Subgrid           | CSS      | Nested grid alignment      | 117+   | 71+     | 16.0+  | Complex layouts     |
| CSS Nesting       | CSS      | Nested selectors           | 120+   | 117+    | 17.2+  | Organization        |
| `inert` attribute | HTML     | Disable regions            | 102+   | 112+    | 15.5+  | Focus management    |
| `<dialog>`        | HTML     | Modal dialogs              | 37+    | 98+     | 15.4+  | Modal UI            |
| `color-mix()`     | CSS      | Color blending             | 111+   | 113+    | 16.2+  | Dynamic colors      |

### Container Queries Example

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card {
  display: grid;
  gap: 1rem;
  padding: 1rem;
}

/* Small card (< 20rem) */
@container card (width < 20rem) {
  .card {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .card-image {
    aspect-ratio: 16/9;
    order: -1;
  }
}

/* Medium card (20rem - 40rem) */
@container card (20rem <= width < 40rem) {
  .card {
    grid-template-columns: 8rem 1fr;
    align-items: start;
  }
}

/* Large card (>= 40rem) */
@container card (width >= 40rem) {
  .card {
    grid-template-columns: 12rem 1fr auto;
    align-items: center;
  }

  .card-actions {
    display: flex;
    gap: 0.5rem;
  }
}
```

### :has() Example

```css
/* Style form when input is focused */
.form-group:has(input:focus) {
  --ring-color: var(--accent);
  box-shadow: 0 0 0 2px var(--ring-color);
}

/* Style label when input is invalid */
.form-group:has(input:invalid) label {
  color: var(--error);
}

/* Card with image gets different layout */
.card:has(img) {
  grid-template-rows: auto 1fr;
}

/* Navigation item with active child */
.nav-item:has(> a[aria-current="page"]) {
  border-bottom: 2px solid var(--accent);
}
```

---

## Feature Detection

```javascript
// Check for DSD support
const hasDSD = "shadowRootMode" in HTMLTemplateElement.prototype;

// Check for popover support
const hasPopover = "popover" in HTMLElement.prototype;

// Check for anchor positioning (NOT Baseline - use with caution)
const hasAnchor = CSS.supports("anchor-name", "--test");

// Check for @scope
const hasScope = CSS.supports("selector(:scope)");

// Check for container queries
const hasCQ = CSS.supports("container-type", "inline-size");

// Check for :has()
const hasHas = CSS.supports("selector(:has(*))");
```

---

## Browser Support Table

| Browser | Baseline 2025 | Baseline 2024 | Baseline 2023 |
| ------- | ------------- | ------------- | ------------- |
| Chrome  | 132+          | 125+          | 120+          |
| Edge    | 132+          | 125+          | 120+          |
| Firefox | 135+          | 128+          | 121+          |
| Safari  | 18.2+         | 17.4+         | 16.4+         |

---

## Migration Patterns

### From CSS Variables to @property

```css
/* Before */
:root {
  --hue: 200;
}

/* After: Typed custom property */
@property --hue {
  syntax: "<number>";
  initial-value: 200;
  inherits: true;
}

/* Now can animate! */
.element {
  --hue: 200;
  background: hsl(var(--hue) 70% 50%);
  transition: --hue 0.5s;
}

.element:hover {
  --hue: 280;
}
```

### From Media Queries to Container Queries

```css
/* Before: Page-level breakpoints */
@media (min-width: 768px) {
  .card {
    flex-direction: row;
  }
}

/* After: Component-level breakpoints */
.card-wrapper {
  container-type: inline-size;
}

@container (width > 30rem) {
  .card {
    flex-direction: row;
  }
}
```

---

_Reference: [webstatus.dev](https://webstatus.dev), [web.dev/baseline](https://web.dev/baseline)_
