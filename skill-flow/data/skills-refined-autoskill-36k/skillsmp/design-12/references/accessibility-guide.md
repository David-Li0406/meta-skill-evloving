# Accessibility Guide (WCAG AA)

## Overview

We follow WCAG 2.1 Level AA standards. This means our interfaces must be:
- **Perceivable** — Users can perceive the content
- **Operable** — Users can operate the interface
- **Understandable** — Users can understand the content
- **Robust** — Content works with assistive technologies

---

## Color Contrast

### Required Ratios

| Text Type | Minimum Ratio |
|-----------|---------------|
| Normal text (<18px) | 4.5:1 |
| Large text (≥18px or 14px bold) | 3:1 |
| UI components and graphics | 3:1 |

### Testing Tools

- Browser DevTools (Chrome, Firefox)
- WebAIM Contrast Checker
- axe DevTools extension

### Implementation

```css
/* ✅ Good - Sufficient contrast */
.text-primary {
  color: var(--color-neutral-900);  /* #111827 */
  background: var(--color-neutral-50); /* #f9fafb */
  /* Ratio: ~16:1 */
}

/* ❌ Bad - Insufficient contrast */
.text-muted {
  color: #9ca3af;  /* Gray-400 */
  background: #f9fafb;
  /* Ratio: ~2.5:1 - FAILS */
}
```

---

## Keyboard Navigation

### Requirements

1. All functionality available via keyboard
2. Logical tab order (follows visual order)
3. No keyboard traps
4. Focus visible at all times

### Key Bindings

| Key | Action |
|-----|--------|
| Tab | Move to next focusable element |
| Shift+Tab | Move to previous element |
| Enter | Activate buttons/links |
| Space | Activate buttons, toggle checkboxes |
| Arrow keys | Navigate within components |
| Escape | Close modals, dismiss menus |

### Focus Management

```css
/* ✅ Visible focus indicator */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* ❌ Never do this */
:focus {
  outline: none; /* Removes focus indicator! */
}
```

### Focus Trapping (Modals)

```javascript
// When modal opens:
// 1. Store previously focused element
// 2. Move focus to modal
// 3. Trap focus within modal
// 4. On close, return focus to previous element

const previouslyFocused = document.activeElement;
modal.querySelector('[autofocus]')?.focus();

modal.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
  if (e.key === 'Tab') trapFocus(e, modal);
});
```

---

## Screen Reader Support

### Semantic HTML First

```html
<!-- Screen readers understand this automatically -->
<nav aria-label="Main">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<main>
  <h1>Page Title</h1>
  <article>
    <h2>Article Title</h2>
    <p>Content...</p>
  </article>
</main>
```

### ARIA When Needed

```html
<!-- Live regions for dynamic content -->
<div aria-live="polite" aria-atomic="true">
  <!-- Announce changes to screen readers -->
  Cart updated: 3 items
</div>

<!-- Descriptions for complex elements -->
<button aria-describedby="delete-warning">Delete Account</button>
<p id="delete-warning" class="sr-only">
  This action cannot be undone. All data will be permanently deleted.
</p>

<!-- Current state indicators -->
<a href="/dashboard" aria-current="page">Dashboard</a>
```

### Screen Reader Only Content

```css
/* Visually hidden but available to screen readers */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## Forms

### Labels

Every input MUST have a visible, associated label:

```html
<!-- ✅ Correct - Label associated with input -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email">

<!-- ✅ Also correct - Wrapping label -->
<label>
  Email Address
  <input type="email" name="email">
</label>

<!-- ❌ Wrong - Placeholder as label -->
<input type="email" placeholder="Email Address">
```

### Error Messages

```html
<div class="form-group">
  <label for="password">Password</label>
  <input
    type="password"
    id="password"
    aria-describedby="password-error"
    aria-invalid="true"
  >
  <p id="password-error" class="error" role="alert">
    Password must be at least 8 characters
  </p>
</div>
```

### Required Fields

```html
<label for="name">
  Name
  <span aria-hidden="true">*</span>
  <span class="sr-only">(required)</span>
</label>
<input type="text" id="name" required aria-required="true">
```

---

## Images and Media

### Alt Text

```html
<!-- Informative image -->
<img src="graph.png" alt="Sales increased 25% from Q1 to Q4 2024">

<!-- Decorative image -->
<img src="decorative-line.svg" alt="" role="presentation">

<!-- Image as link -->
<a href="/home">
  <img src="logo.svg" alt="Company Name - Go to homepage">
</a>

<!-- Complex image -->
<figure>
  <img src="flowchart.png" alt="User registration flowchart" aria-describedby="flowchart-desc">
  <figcaption id="flowchart-desc">
    Step 1: Enter email. Step 2: Verify email...
  </figcaption>
</figure>
```

### Video and Audio

```html
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt" srclang="en" label="English">
  <track kind="descriptions" src="descriptions.vtt" srclang="en" label="Audio descriptions">
</video>
```

---

## Motion and Animation

### Respect User Preferences

```css
/* Reduce motion for users who prefer it */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Safe Animation Guidelines

- Keep animations under 5 seconds
- Avoid flashing content (>3 flashes per second)
- Provide pause/stop controls for auto-playing content
- Use subtle transitions (150-300ms)

---

## Testing Checklist

### Manual Testing

- [ ] Navigate entire page with keyboard only
- [ ] Test with screen reader (NVDA, VoiceOver, or JAWS)
- [ ] Zoom to 200% - content still usable
- [ ] Test with high contrast mode
- [ ] Test with reduced motion preference

### Automated Testing

- [ ] Run axe DevTools
- [ ] Run Lighthouse accessibility audit
- [ ] Run WAVE tool
- [ ] Check color contrast ratios

### Screen Reader Testing

| Platform | Screen Reader | Browser |
|----------|---------------|---------|
| Windows | NVDA | Firefox, Chrome |
| Windows | JAWS | Chrome |
| macOS | VoiceOver | Safari |
| iOS | VoiceOver | Safari |
| Android | TalkBack | Chrome |

---

## Common Issues

| Issue | Impact | Fix |
|-------|--------|-----|
| Missing alt text | Blind users can't understand images | Add descriptive alt |
| Low contrast | Hard to read for low vision | Increase contrast ratio |
| Missing labels | Screen reader users can't identify inputs | Add `<label>` elements |
| No focus indicators | Keyboard users can't see position | Add visible :focus styles |
| Keyboard trap | Users get stuck | Ensure escape routes |
| Auto-playing media | Distracting, can't control | Add pause/stop controls |
