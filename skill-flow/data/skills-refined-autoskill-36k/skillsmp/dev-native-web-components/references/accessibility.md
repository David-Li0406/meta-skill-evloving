# Accessibility Reference

> Ensure WCAG 2.2 AA compliance with semantic HTML, ARIA, and focus management.

---

## Semantic HTML First

```html
<!-- ✅ CORRECT: Semantic structure -->
<article>
  <header>
    <h2>Article Title</h2>
    <time datetime="2024-12-25">Dec 25, 2024</time>
  </header>
  <section>
    <p>Content...</p>
  </section>
  <footer>
    <address>By <a href="/author">Author</a></address>
  </footer>
</article>

<!-- ❌ WRONG: Div soup -->
<div class="article">
  <div class="header">...</div>
</div>
```

---

## Landmark Roles (Implicit)

| Element     | Role                |
| ----------- | ------------------- |
| `<header>`  | banner (top-level)  |
| `<nav>`     | navigation          |
| `<main>`    | main                |
| `<aside>`   | complementary       |
| `<footer>`  | contentinfo         |
| `<section>` | region (if labeled) |
| `<article>` | article             |
| `<form>`    | form (if labeled)   |

---

## Focus Management

### Visible Focus

```css
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* Remove default, keep visible */
:focus:not(:focus-visible) {
  outline: none;
}
```

### Focus Order

```html
<!-- Natural tab order -->
<button>First</button>
<button>Second</button>

<!-- Skip link -->
<a href="#main" class="skip-link">Skip to content</a>

<style>
  .skip-link {
    position: absolute;
    top: -100%;

    &:focus {
      top: 0;
    }
  }
</style>
```

### Inert Attribute

```html
<!-- Disable region from focus/interaction -->
<div inert>
  <button>Can't focus this</button>
</div>
```

---

## ARIA When Needed

### Don't Use ARIA If HTML Exists

```html
<!-- ❌ WRONG: Redundant ARIA -->
<button role="button">Click</button>

<!-- ✅ CORRECT: Native element -->
<button>Click</button>
```

### Required ARIA Patterns

```html
<!-- Live region for updates -->
<div role="status" aria-live="polite">3 items in cart</div>

<!-- Tab panel -->
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel1">Tab 1</button>
</div>
<div role="tabpanel" id="panel1">Content</div>

<!-- Menu -->
<nav aria-label="Main">
  <ul role="menubar">
    <li role="none">
      <a role="menuitem" href="/">Home</a>
    </li>
  </ul>
</nav>
```

---

## Color Contrast

```css
:root {
  /* WCAG AA: 4.5:1 for text, 3:1 for large text */
  --text: light-dark(#1a1a1a, #f0f0f0); /* High contrast */
  --text-muted: light-dark(#666, #999); /* Secondary */
  --bg: light-dark(#fff, #0a0a0a);
}

/* Never rely on color alone */
.error {
  color: var(--error);
  /* Also use icon/text */
  &::before {
    content: "⚠️ ";
  }
}
```

---

## Interactive Elements

### Buttons vs Links

```html
<!-- Button: Action on current page -->
<button onclick="save()">Save</button>

<!-- Link: Navigation to URL -->
<a href="/settings">Settings</a>

<!-- ❌ WRONG: Link as button -->
<a href="#" onclick="save()">Save</a>
```

### Touch Targets

```css
/* Minimum 44x44px touch target */
button,
a {
  min-width: 44px;
  min-height: 44px;
  padding: 0.75rem 1rem;
}
```

---

## Forms Accessibility

```html
<form>
  <div class="field">
    <label for="email">Email</label>
    <input
      type="email"
      id="email"
      name="email"
      aria-describedby="email-hint email-error"
      required
    />
    <p id="email-hint" class="hint">We'll never share your email.</p>
    <p id="email-error" class="error" hidden>Please enter valid email.</p>
  </div>

  <fieldset>
    <legend>Notification preferences</legend>
    <label>
      <input type="checkbox" name="notify" value="email" />
      Email notifications
    </label>
  </fieldset>
</form>
```

---

## Images

```html
<!-- Informative image -->
<img src="chart.png" alt="Sales increased 50% in Q4" />

<!-- Decorative image -->
<img src="decoration.png" alt="" role="presentation" />

<!-- Complex image -->
<figure>
  <img src="diagram.png" alt="System architecture" />
  <figcaption>Detailed description of the diagram...</figcaption>
</figure>
```

---

## Motion & Animations

```css
/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Testing Checklist

- [ ] Tab through entire page - logical order?
- [ ] All interactive elements have visible focus?
- [ ] Can use with keyboard only?
- [ ] Screen reader announces content correctly?
- [ ] Color contrast passes (4.5:1 / 3:1)?
- [ ] Images have appropriate alt text?
- [ ] Forms have labels and error messages?
- [ ] Reduced motion respected?

---

## Tools

| Tool           | Purpose                     |
| -------------- | --------------------------- |
| axe DevTools   | Browser extension           |
| Lighthouse     | Chrome DevTools             |
| WAVE           | Web accessibility evaluator |
| NVDA/VoiceOver | Screen readers              |

_Reference: [web.dev/learn/accessibility](https://web.dev/learn/accessibility)_
