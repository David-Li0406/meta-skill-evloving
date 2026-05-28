# Declarative Shadow DOM (DSD) Reference

> Use DSD as the **only** method for creating Shadow DOM. Never use imperative `attachShadow()`.

---

## Core Syntax

```html
<custom-element>
  <template shadowrootmode="open">
    <style>
      /* Scoped styles */
    </style>
    <slot></slot>
  </template>
  <!-- Light DOM content -->
</custom-element>
```

### shadowrootmode Values

| Value    | Description                   | Use Case                      |
| -------- | ----------------------------- | ----------------------------- |
| `open`   | Shadow root accessible via JS | Default for most components   |
| `closed` | Shadow root not accessible    | Security-sensitive components |

---

## Complete DSD Component

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>DSD Card Component</title>
    <style>
      :root {
        color-scheme: light dark;
        --bg: light-dark(#fff, #111);
        --fg: light-dark(#111, #fff);
        --surface: light-dark(#f8f8f8, #1a1a1a);
        --border: light-dark(#e0e0e0, #333);
        --radius: 0.75rem;
      }

      body {
        font-family: system-ui, sans-serif;
        background: var(--bg);
        color: var(--fg);
        padding: 2rem;
      }
    </style>
  </head>
  <body>
    <product-card>
      <template shadowrootmode="open">
        <style>
          :host {
            display: block;
            container-type: inline-size;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            overflow: hidden;
          }

          .layout {
            display: grid;
            gap: 1rem;
          }

          @container (width >= 25rem) {
            .layout {
              grid-template-columns: 10rem 1fr;
            }
          }

          .image-slot {
            aspect-ratio: 1;
            background: var(--border);
          }

          .content {
            padding: 1rem;
          }

          ::slotted(h2) {
            margin: 0 0 0.5rem;
            font-size: clamp(1rem, 3cqi, 1.5rem);
          }

          ::slotted(p) {
            margin: 0;
            color: var(--fg);
            opacity: 0.8;
          }

          ::slotted([slot="actions"]) {
            margin-top: 1rem;
          }
        </style>

        <div class="layout">
          <div class="image-slot">
            <slot name="image"></slot>
          </div>
          <div class="content">
            <slot></slot>
            <slot name="actions"></slot>
          </div>
        </div>
      </template>

      <!-- Light DOM content -->
      <img slot="image" src="/product.jpg" alt="Product" loading="lazy" />
      <h2>Product Name</h2>
      <p>Product description goes here with details.</p>
      <button slot="actions">Add to Cart</button>
    </product-card>
  </body>
</html>
```

---

## Slot Patterns

### Named Slots

```html
<my-card>
  <template shadowrootmode="open">
    <header><slot name="header"></slot></header>
    <main><slot></slot></main>
    <footer><slot name="footer"></slot></footer>
  </template>

  <h2 slot="header">Card Title</h2>
  <p>Default slot content</p>
  <button slot="footer">Action</button>
</my-card>
```

### Slot Fallback Content

```html
<template shadowrootmode="open">
  <slot name="icon">
    <!-- Fallback if no icon provided -->
    <svg aria-hidden="true"><!-- default icon --></svg>
  </slot>
  <slot>Default content if empty</slot>
</template>
```

### Styling Slotted Content

```css
/* Style elements assigned to slots */
::slotted(*) {
  /* Applies to all slotted elements */
}

::slotted(h2) {
  /* Only slotted h2 elements */
  margin: 0;
  font-size: 1.25rem;
}

::slotted([slot="actions"]) {
  /* Elements in the actions slot */
  display: flex;
  gap: 0.5rem;
}
```

---

## CSS Parts for External Styling

```html
<fancy-button>
  <template shadowrootmode="open">
    <style>
      button {
        all: unset;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        background: var(--button-bg, #0066cc);
        color: var(--button-fg, #fff);
        cursor: pointer;
        transition: background 0.2s;
      }

      button:hover {
        background: var(--button-bg-hover, #0052a3);
      }
    </style>
    <button part="button">
      <slot name="icon"></slot>
      <slot></slot>
    </button>
  </template>
  <span slot="icon">🛒</span>
  Add to Cart
</fancy-button>

<style>
  /* External styling via ::part() */
  fancy-button::part(button) {
    --button-bg: #22c55e;
    --button-bg-hover: #16a34a;
    font-weight: 600;
  }
</style>
```

### Exporting Parts from Nested Components

```html
<outer-component>
  <template shadowrootmode="open">
    <inner-component exportparts="button: inner-button"></inner-component>
  </template>
</outer-component>

<style>
  outer-component::part(inner-button) {
    /* Style the button inside inner-component */
  }
</style>
```

---

## SSR Hydration Pattern

```html
<!-- Server renders complete DSD -->
<counter-component data-count="5">
  <template shadowrootmode="open">
    <style>
      :host {
        display: inline-flex;
        gap: 0.5rem;
      }
      button {
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        border: 1px solid currentColor;
        background: transparent;
        cursor: pointer;
      }
      span {
        min-width: 3ch;
        text-align: center;
      }
    </style>
    <button data-action="decrement">−</button>
    <span>5</span>
    <button data-action="increment">+</button>
  </template>
</counter-component>

<script type="module">
  // Hydration - enhance existing DSD
  customElements.define(
    "counter-component",
    class extends HTMLElement {
      #count;

      connectedCallback() {
        // Shadow root already exists from DSD
        this.#count = parseInt(this.dataset.count || "0");

        // Add interactivity
        this.shadowRoot.addEventListener("click", (e) => {
          const action = e.target.dataset.action;
          if (action === "increment") this.#count++;
          if (action === "decrement") this.#count--;
          this.#render();
        });
      }

      #render() {
        this.shadowRoot.querySelector("span").textContent = this.#count;
      }
    }
  );
</script>
```

---

## When NOT to Use Shadow DOM

| Situation                                 | Use Instead                        |
| ----------------------------------------- | ---------------------------------- |
| Form elements that need native submission | Light DOM with `@scope`            |
| Content that needs SEO indexing           | Light DOM (slots ARE indexed)      |
| Simple styling scope                      | `@scope` at-rule                   |
| Third-party styling needed                | CSS custom properties + `::part()` |

### Alternative: @scope for Light DOM Components

```html
<div class="card">
  <h2>Card Title</h2>
  <p>Content</p>
</div>

<style>
  @scope (.card) {
    :scope {
      padding: 1rem;
      border: 1px solid var(--border);
      border-radius: 0.5rem;
    }

    h2 {
      margin: 0 0 0.5rem;
    }
    p {
      margin: 0;
      opacity: 0.8;
    }
  }
</style>
```

---

## DSD + Forms Pattern

```html
<form-field>
  <template shadowrootmode="open">
    <style>
      :host {
        display: grid;
        gap: 0.25rem;
      }

      ::slotted(label) {
        font-weight: 500;
        font-size: 0.875rem;
      }

      ::slotted(input) {
        padding: 0.5rem 0.75rem;
        border: 1px solid var(--border);
        border-radius: 0.375rem;
        font: inherit;
      }

      ::slotted(input:focus) {
        outline: 2px solid var(--accent);
        outline-offset: 2px;
      }

      .error {
        color: #dc2626;
        font-size: 0.75rem;
        display: none;
      }

      :host(:has(input:invalid:not(:placeholder-shown))) .error {
        display: block;
      }
    </style>

    <slot name="label"></slot>
    <slot name="input"></slot>
    <p class="error"><slot name="error">Invalid input</slot></p>
  </template>

  <label slot="label" for="email">Email</label>
  <input
    slot="input"
    type="email"
    id="email"
    name="email"
    placeholder="you@example.com"
    required
  />
  <span slot="error">Please enter a valid email</span>
</form-field>
```

---

## Browser Support

| Browser | DSD Support | Version |
| ------- | ----------- | ------- |
| Chrome  | ✅          | 111+    |
| Edge    | ✅          | 111+    |
| Firefox | ✅          | 123+    |
| Safari  | ✅          | 16.4+   |

**Baseline**: 2024 (Newly Available)

---

## Common Mistakes

### ❌ Using attachShadow()

```javascript
// WRONG - Never do this
class MyComponent extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" }); // ❌
  }
}
```

### ✅ Using DSD

```html
<my-component>
  <template shadowrootmode="open">
    <!-- Content -->
  </template>
</my-component>
```

### ❌ Expecting shadowRoot in constructor

```javascript
// WRONG - DSD shadow root exists before constructor
class MyComponent extends HTMLElement {
  constructor() {
    super();
    console.log(this.shadowRoot); // Already exists!
  }
}
```

### ✅ Using existing shadowRoot

```javascript
class MyComponent extends HTMLElement {
  connectedCallback() {
    // Shadow root from DSD already attached
    if (this.shadowRoot) {
      // Hydrate existing content
      this.shadowRoot
        .querySelector("button")
        .addEventListener("click", this.handleClick);
    }
  }
}
```

---

_Reference: [web.dev/declarative-shadow-dom](https://web.dev/articles/declarative-shadow-dom)_
