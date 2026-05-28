# CSS-First Patterns Reference

> Reduce JavaScript by 60-80% using native CSS features for interactivity.

---

## CSS-Only Accordion

```html
<details name="faq">
  <summary>Question 1</summary>
  <p>Answer content here.</p>
</details>
<details name="faq">
  <summary>Question 2</summary>
  <p>Answer content here.</p>
</details>
```

```css
details {
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  overflow: hidden;

  & + details {
    margin-top: -1px;
  }

  &::details-content {
    block-size: 0;
    overflow-y: clip;
    transition: block-size 0.3s, opacity 0.3s;
    opacity: 0;
  }

  &[open]::details-content {
    block-size: auto;
    opacity: 1;
  }
}

summary {
  padding: 1rem;
  cursor: pointer;
  list-style: none;

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

## CSS-Only Dark Mode

```css
:root {
  color-scheme: light dark;

  --bg: light-dark(#ffffff, #0a0a0a);
  --fg: light-dark(#1a1a1a, #f0f0f0);
  --surface: light-dark(#f5f5f5, #1a1a1a);
  --border: light-dark(#e0e0e0, #333);
  --accent: light-dark(#0066cc, #66b3ff);
}

body {
  background: var(--bg);
  color: var(--fg);
}
```

---

## CSS-Only Tabs

```html
<div class="tabs">
  <input type="radio" name="tabs" id="tab1" checked />
  <label for="tab1">Tab 1</label>
  <div class="panel">Panel 1 content</div>

  <input type="radio" name="tabs" id="tab2" />
  <label for="tab2">Tab 2</label>
  <div class="panel">Panel 2 content</div>
</div>
```

```css
.tabs {
  display: grid;
  grid-template-columns: repeat(2, auto) 1fr;
  grid-template-rows: auto 1fr;
}

.tabs input {
  display: none;
}

.tabs label {
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.tabs input:checked + label {
  border-color: var(--accent);
  color: var(--accent);
}

.tabs .panel {
  display: none;
  grid-column: 1 / -1;
  padding: 1rem;
}

.tabs input:checked + label + .panel {
  display: block;
}
```

---

## CSS-Only Toggle/Switch

```html
<label class="switch">
  <input type="checkbox" />
  <span class="track"></span>
  Enable notifications
</label>
```

```css
.switch {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.switch input {
  display: none;
}

.switch .track {
  width: 3rem;
  height: 1.5rem;
  background: var(--border);
  border-radius: 1rem;
  position: relative;
  transition: background 0.2s;

  &::before {
    content: "";
    position: absolute;
    width: 1.25rem;
    height: 1.25rem;
    background: white;
    border-radius: 50%;
    top: 0.125rem;
    left: 0.125rem;
    transition: translate 0.2s;
  }
}

.switch input:checked + .track {
  background: var(--accent);

  &::before {
    translate: 1.5rem 0;
  }
}
```

---

## CSS-Only Carousel (Scroll Snap)

```html
<div class="carousel">
  <div class="slide">Slide 1</div>
  <div class="slide">Slide 2</div>
  <div class="slide">Slide 3</div>
</div>
```

```css
.carousel {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-padding-inline: 1rem;
  padding: 1rem;

  /* Hide scrollbar */
  scrollbar-width: none;
  &::-webkit-scrollbar {
    display: none;
  }
}

.slide {
  flex: 0 0 min(100%, 20rem);
  scroll-snap-align: start;
  aspect-ratio: 16/9;
  background: var(--surface);
  border-radius: 0.5rem;
}
```

---

## :has() Parent Selector Patterns

```css
/* Form group with focused input */
.form-group:has(input:focus) {
  --ring: var(--accent);
  box-shadow: 0 0 0 2px var(--ring);
}

/* Card with image gets different layout */
.card:has(> img) {
  grid-template-rows: auto 1fr;
}

/* Label style when input is invalid */
.field:has(input:invalid:not(:placeholder-shown)) {
  label {
    color: var(--error);
  }
  input {
    border-color: var(--error);
  }
}

/* Navigation with active item */
.nav:has([aria-current="page"]) {
  border-bottom-color: var(--accent);
}
```

---

## Entry/Exit Animations

```css
[popover] {
  opacity: 0;
  transform: translateY(-0.5rem);
  transition: opacity 0.2s, transform 0.2s, display 0.2s allow-discrete, overlay
      0.2s allow-discrete;
}

[popover]:popover-open {
  opacity: 1;
  transform: translateY(0);
}

@starting-style {
  [popover]:popover-open {
    opacity: 0;
    transform: translateY(-0.5rem);
  }
}
```

---

## CSS-Only Modal Close on ::backdrop Click

```css
dialog {
  &::backdrop {
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
  }
}
```
```

---

## Checklist

- [ ] Use `<details>` for accordions
- [ ] Use `light-dark()` for color schemes
- [ ] Use `:has()` for parent selection
- [ ] Use `@starting-style` for entry animations
- [ ] Use `popover` for tooltips/menus
- [ ] Use `scroll-snap` for carousels

_Reference: [chrome.dev/css-wrapped-2024](https://chrome.dev/css-wrapped-2024/)_
