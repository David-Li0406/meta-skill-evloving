# Slot Patterns Reference

> Deep dive into slot patterns for Declarative Shadow DOM components.

---

## Slot Basics

Slots allow light DOM content to be projected into Shadow DOM templates.

```html
<my-card>
  <template shadowrootmode="open">
    <div class="card">
      <slot></slot> <!-- Default slot -->
    </div>
  </template>
  
  <!-- Light DOM content projected into slot -->
  <h2>Card Title</h2>
  <p>Card description</p>
</my-card>
```

---

## Named Slots

Use named slots to project content to specific locations.

```html
<article-card>
  <template shadowrootmode="open">
    <style>
      :host { display: grid; gap: 1rem; }
      header { border-bottom: 1px solid var(--border); }
      footer { border-top: 1px solid var(--border); }
    </style>
    
    <header><slot name="header"></slot></header>
    <main><slot></slot></main>
    <footer><slot name="footer"></slot></footer>
  </template>
  
  <h2 slot="header">Article Title</h2>
  <p>Main content goes in default slot</p>
  <nav slot="footer">
    <a href="/prev">Previous</a>
    <a href="/next">Next</a>
  </nav>
</article-card>
```

### Slot Assignment Rules

| Rule | Description |

|------|-------------|
| `slot="name"` on element | Assigns element to named slot |
| No `slot` attribute | Goes to default (unnamed) slot |
| Multiple elements same slot | All projected in order |
| No matching slot | Content not rendered |

---

## Fallback Content

Slots can have fallback content shown when no content is projected.

```html
<user-avatar>
  <template shadowrootmode="open">
    <style>
      .avatar {
        width: 3rem;
        height: 3rem;
        border-radius: 50%;
        background: var(--surface);
        display: grid;
        place-items: center;
      }
      ::slotted(img) {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
      }
    </style>
    
    <div class="avatar">
      <slot>
        <!-- Fallback: shown if no image provided -->
        <svg aria-hidden="true" viewBox="0 0 24 24" width="24" height="24">
          <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
        </svg>
      </slot>
    </div>
  </template>
  
  <!-- With image -->
  <img src="avatar.jpg" alt="User name">
</user-avatar>

<!-- Without image (shows fallback) -->
<user-avatar></user-avatar>
```

---

## Styling Slotted Content

Use `::slotted()` to style projected content from within Shadow DOM.

```css
/* Style ALL slotted elements */
::slotted(*) {
  margin: 0;
}

/* Style specific elements */
::slotted(h2) {
  font-size: clamp(1.25rem, 3cqi, 2rem);
  color: var(--heading);
}

/* Style by attribute */
::slotted([slot="actions"]) {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

/* Style by class (works!) */
::slotted(.highlight) {
  background: var(--accent);
}
```

### ::slotted() Limitations

| Works | Doesn't Work |

|-------|--------------|
| `::slotted(p)` | `::slotted(p span)` — No descendants |
| `::slotted(.class)` | `::slotted(p):hover` — No pseudo-classes after |
| `::slotted([attr])` | Complex selectors inside |

**Rule**: `::slotted()` only selects **direct children** of the host element, not their descendants.

---

## Slot Change Detection

Listen for content changes with the `slotchange` event.

> **Note**: `slotchange` requires JavaScript. See `minimal-javascript.md` (coming soon) for implementation patterns.

### slotchange API Reference

| Method | Description |

|--------|-------------|
| `slot.assignedNodes()` | Get all assigned nodes (including text) |
| `slot.assignedElements()` | Get only element nodes |
| `slot.assignedElements({ flatten: true })` | Get elements including fallback content |

_Reference: [MDN slotchange event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLSlotElement/slotchange_event)_

---

## Nested Slots (Slot Forwarding)

Components can forward slots to nested components.

```html
<!-- Outer component -->
<modal-dialog>
  <template shadowrootmode="open">
    <dialog>
      <header><slot name="title"></slot></header>
      <div class="content">
        <!-- Forward default slot to inner component -->
        <scroll-container>
          <slot></slot>
        </scroll-container>
      </div>
      <footer><slot name="actions"></slot></footer>
    </dialog>
  </template>
  
  <h2 slot="title">Dialog Title</h2>
  <p>This content passes through modal-dialog's default slot into scroll-container</p>
  <button slot="actions">Close</button>
</modal-dialog>

<!-- Inner component (scroll-container) -->
<template shadowrootmode="open">
  <style>
    :host { display: block; max-height: 60vh; overflow-y: auto; }
  </style>
  <slot></slot> <!-- Receives forwarded content -->
</template>
```

---

## Multi-Slot Patterns

### Card with Multiple Sections

```html
<feature-card>
  <template shadowrootmode="open">
    <style>
      :host {
        display: grid;
        grid-template-rows: auto 1fr auto;
        container-type: inline-size;
        border: 1px solid var(--border);
        border-radius: 0.75rem;
        overflow: hidden;
      }
      .media { aspect-ratio: 16/9; background: var(--surface); }
      .body { padding: 1rem; }
      .actions { 
        padding: 1rem; 
        border-top: 1px solid var(--border);
        display: flex;
        gap: 0.5rem;
      }
      
      @container (width < 20rem) {
        .actions { flex-direction: column; }
      }
    </style>
    
    <div class="media"><slot name="media"></slot></div>
    <div class="body">
      <slot name="title"></slot>
      <slot></slot>
    </div>
    <div class="actions"><slot name="actions"></slot></div>
  </template>
  
  <img slot="media" src="feature.jpg" alt="Feature" loading="lazy">
  <h3 slot="title">Feature Name</h3>
  <p>Feature description with details.</p>
  <button slot="actions">Learn More</button>
  <button slot="actions">Try It</button>
</feature-card>
```

### Conditional Slot Visibility

Use `:has()` to hide empty slot containers.

```css
/* Hide section if slot has no content */
.actions:not(:has(::slotted(*))) {
  display: none;
}

/* Alternative: use :empty on slotted content wrapper */
.actions:has(slot:empty) {
  display: none;
}
```

**Note**: This requires checking `assignedElements().length` since CSS can't truly detect empty slots.

---

## Slot with :has() Patterns

```css
/* Card layout changes when media slot has content */
:host(:has([slot="media"])) {
  grid-template-columns: 8rem 1fr;
}

/* Highlight when required field slot has invalid input */
:host(:has(slot[name="input"] ::slotted(:invalid))) {
  --border-color: var(--error);
}
```

---

## Common Slot Anti-Patterns

### ❌ Expecting Descendants in ::slotted()

```css
/* WRONG: Can't style descendants of slotted elements */
::slotted(div span) {
  color: red;
}

/* ✅ CORRECT: Style from light DOM or use CSS custom properties */
my-component span {
  color: red;
}
```

### ❌ Multiple Default Slots

```html
<!-- WRONG: Only one default slot allowed -->
<template shadowrootmode="open">
  <slot></slot>
  <slot></slot> <!-- Second one gets nothing -->
</template>
```

### ❌ Modifying Slotted Elements from Shadow DOM JS

Don't modify light DOM from Shadow DOM JavaScript. Instead, use custom events to communicate state changes back to the parent.

_See `minimal-javascript.md` (coming soon) for event communication patterns._

---

## Checklist

- [ ] Use named slots for structured content
- [ ] Provide fallback content for optional slots
- [ ] Use `::slotted()` only for direct children styling
- [ ] Listen to `slotchange` for dynamic content
- [ ] Forward slots correctly in nested components
- [ ] Use `:has()` with slotted selectors for conditional styling

---

_Reference: [MDN Using templates and slots](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_templates_and_slots)_
