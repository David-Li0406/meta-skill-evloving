---
name: web-accessibility
description: WCAG 2.1 AA accessibility patterns for React applications
user-invocable: false
---

# Web Accessibility Skill

**Version:** 1.0
**Standard:** WCAG 2.1 Level AA

> Accessibility is not optional. These patterns ensure all users can use your application.

---

## Core Principles (POUR)

1. **Perceivable** — Users can perceive all content (see, hear, or feel it).
2. **Operable** — Users can operate all controls (keyboard, mouse, voice, etc.).
3. **Understandable** — Users can understand content and interface behavior.
4. **Robust** — Content works with current and future assistive technologies.

---

## Semantic HTML First

### Use the Right Element

```html
<!-- ✅ Good - Semantic elements -->
<header>Site header</header>
<nav>Navigation</nav>
<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
  <aside>Related content</aside>
</main>
<footer>Site footer</footer>

<!-- ❌ Bad - Div soup -->
<div class="header">Site header</div>
<div class="nav">Navigation</div>
<div class="main">
  <div class="article">
    <div class="title">Article Title</div>
    <div class="content">Content...</div>
  </div>
</div>
```

### Buttons vs Links

```jsx
// ✅ Button - Performs an action
<button onClick={handleSubmit}>Submit Form</button>
<button onClick={openModal}>Open Settings</button>

// ✅ Link - Navigates somewhere
<a href="/products">View Products</a>
<Link to="/checkout">Proceed to Checkout</Link>

// ❌ Bad - Wrong semantics
<div onClick={handleSubmit}>Submit Form</div>
<a onClick={openModal}>Open Settings</a>  {/* No href! */}
<button onClick={() => navigate('/products')}>View Products</button>
```

### Heading Hierarchy

```jsx
// ✅ Good - Proper hierarchy
<h1>Page Title</h1>
<section>
  <h2>Section Title</h2>
  <h3>Subsection</h3>
</section>
<section>
  <h2>Another Section</h2>
</section>

// ❌ Bad - Skipped levels
<h1>Page Title</h1>
<h3>Subsection</h3>  {/* Skipped h2! */}
<h5>Deep section</h5> {/* Skipped h4! */}
```

---

## Keyboard Navigation

### Focus Management

```css
/* Visible focus indicator */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Remove outline only for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

### Tab Order

```jsx
// ✅ Good - Logical tab order (follows DOM order)
<form>
  <label htmlFor="email">Email</label>
  <input id="email" type="email" />

  <label htmlFor="password">Password</label>
  <input id="password" type="password" />

  <button type="submit">Login</button>
</form>

// ❌ Bad - Jumpy tab order
<form>
  <button type="submit" tabIndex={1}>Login</button>
  <input tabIndex={3} />
  <input tabIndex={2} />
</form>
```

### Skip Links

```jsx
// At the very top of your app
function SkipLink() {
  return (
    <a href="#main-content" className="skip-link">
      Skip to main content
    </a>
  );
}

// CSS
.skip-link {
  position: absolute;
  top: -100%;
  left: var(--space-4);
  padding: var(--space-2) var(--space-4);
  background: var(--color-surface);
  z-index: var(--z-tooltip);
}

.skip-link:focus {
  top: var(--space-4);
}
```

### Keyboard Shortcuts

```jsx
// Listen for keyboard events
function SearchModal({ isOpen, onClose }) {
  useEffect(() => {
    function handleKeyDown(e) {
      if (e.key === 'Escape') {
        onClose();
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
      return () => document.removeEventListener('keydown', handleKeyDown);
    }
  }, [isOpen, onClose]);

  // ...
}
```

---

## Focus Trapping (Modals)

### Modal Pattern

```jsx
import { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';

function Modal({ isOpen, onClose, title, children }) {
  const modalRef = useRef(null);
  const previousFocus = useRef(null);

  useEffect(() => {
    if (isOpen) {
      // Store current focus
      previousFocus.current = document.activeElement;

      // Focus the modal
      modalRef.current?.focus();

      // Trap focus inside modal
      const modal = modalRef.current;
      const focusableElements = modal?.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      const firstElement = focusableElements?.[0];
      const lastElement = focusableElements?.[focusableElements.length - 1];

      function handleTab(e) {
        if (e.key !== 'Tab') return;

        if (e.shiftKey && document.activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }

      modal?.addEventListener('keydown', handleTab);
      return () => modal?.removeEventListener('keydown', handleTab);
    } else {
      // Restore focus when closing
      previousFocus.current?.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return createPortal(
    <div className="modal-backdrop" onClick={onClose}>
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className="modal"
        onClick={(e) => e.stopPropagation()}
        tabIndex={-1}
      >
        <h2 id="modal-title">{title}</h2>
        {children}
        <button onClick={onClose} aria-label="Close modal">
          ×
        </button>
      </div>
    </div>,
    document.body
  );
}
```

---

## ARIA Usage

### When to Use ARIA

**First rule of ARIA:** Don't use ARIA if you can use native HTML.

```jsx
// ❌ Unnecessary ARIA
<div role="button" tabIndex={0} onClick={handleClick}>
  Click me
</div>

// ✅ Just use a button
<button onClick={handleClick}>Click me</button>
```

### Essential ARIA Patterns

```jsx
// Labeling
<button aria-label="Close menu">×</button>
<input aria-labelledby="name-label helper-text" />

// Descriptions
<button aria-describedby="delete-warning">Delete Account</button>
<p id="delete-warning">This action cannot be undone.</p>

// States
<button aria-pressed={isActive}>Toggle</button>
<button aria-expanded={isOpen} aria-controls="menu">Menu</button>
<div id="menu" aria-hidden={!isOpen}>Menu content</div>

// Live regions (for dynamic content)
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>
```

### Common ARIA Roles

| Role | Use Case |
|------|----------|
| `alert` | Important messages (errors, warnings) |
| `alertdialog` | Modal requiring user response |
| `dialog` | Modal dialogs |
| `navigation` | Navigation sections |
| `search` | Search forms |
| `tablist`, `tab`, `tabpanel` | Tab interfaces |
| `menu`, `menuitem` | Dropdown menus |
| `status` | Status updates (loading, saving) |

---

## Forms

### Labels

```jsx
// ✅ Explicit label association
<label htmlFor="email">Email Address</label>
<input id="email" type="email" />

// ✅ Implicit association (wrapped)
<label>
  Email Address
  <input type="email" />
</label>

// ❌ Bad - No association
<span>Email Address</span>
<input type="email" />
```

### Error Messages

```jsx
function FormField({ id, label, error, ...props }) {
  const errorId = `${id}-error`;

  return (
    <div className="form-field">
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        aria-invalid={!!error}
        aria-describedby={error ? errorId : undefined}
        {...props}
      />
      {error && (
        <p id={errorId} className="error-message" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
```

### Required Fields

```jsx
<label htmlFor="name">
  Name <span aria-hidden="true">*</span>
  <span className="visually-hidden">(required)</span>
</label>
<input id="name" required aria-required="true" />
```

---

## Color and Contrast

### Minimum Contrast Ratios

| Text Type | Ratio | Example |
|-----------|-------|---------|
| Normal text (< 18px) | 4.5:1 | Body copy |
| Large text (≥ 18px or 14px bold) | 3:1 | Headings |
| UI components | 3:1 | Buttons, inputs |

### Don't Rely on Color Alone

```jsx
// ❌ Bad - Color is only indicator
<span style={{ color: error ? 'red' : 'green' }}>
  {error ? 'Invalid' : 'Valid'}
</span>

// ✅ Good - Color + icon + text
<span className={error ? 'error' : 'success'}>
  {error ? (
    <>
      <ErrorIcon aria-hidden="true" /> Invalid: {error}
    </>
  ) : (
    <>
      <CheckIcon aria-hidden="true" /> Valid
    </>
  )}
</span>
```

---

## Images and Media

### Alt Text

```jsx
// Informative image
<img src="chart.png" alt="Sales increased 40% from January to March" />

// Decorative image
<img src="divider.png" alt="" role="presentation" />

// Complex image
<figure>
  <img src="diagram.png" alt="Architecture diagram" aria-describedby="diagram-desc" />
  <figcaption id="diagram-desc">
    The system consists of three layers: presentation, business logic, and data.
    {/* Full description */}
  </figcaption>
</figure>
```

### SVG Icons

```jsx
// Decorative icon (with visible text)
<button>
  <SearchIcon aria-hidden="true" />
  Search
</button>

// Standalone icon (needs label)
<button aria-label="Search">
  <SearchIcon aria-hidden="true" />
</button>

// Icon with title
<svg role="img" aria-labelledby="icon-title">
  <title id="icon-title">Search</title>
  <path d="..." />
</svg>
```

---

## Dynamic Content

### Loading States

```jsx
function ProductList() {
  const { data, loading, error } = useQuery(GET_PRODUCTS);

  if (loading) {
    return (
      <div role="status" aria-live="polite">
        <Spinner aria-hidden="true" />
        <span className="visually-hidden">Loading products...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div role="alert">
        Error loading products. Please try again.
      </div>
    );
  }

  return (
    <ul aria-label="Products">
      {data.products.map(product => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  );
}
```

### Live Regions

```jsx
// Polite - Waits for user to finish current task
<div aria-live="polite" aria-atomic="true">
  {saveStatus} {/* "Saving...", "Saved!", etc. */}
</div>

// Assertive - Interrupts immediately (use sparingly)
<div aria-live="assertive" role="alert">
  {errorMessage}
</div>
```

---

## Reduced Motion

```css
/* Respect user preference */
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

```jsx
// In React
function AnimatedComponent() {
  const prefersReducedMotion = window.matchMedia(
    '(prefers-reduced-motion: reduce)'
  ).matches;

  return (
    <motion.div
      animate={{ opacity: 1 }}
      transition={{
        duration: prefersReducedMotion ? 0 : 0.3,
      }}
    />
  );
}
```

---

## Visually Hidden Text

```css
.visually-hidden {
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

```jsx
// Use for screen reader only content
<button>
  <TrashIcon aria-hidden="true" />
  <span className="visually-hidden">Delete item</span>
</button>

<a href="/products">
  View all products
  <span className="visually-hidden"> in the catalog</span>
</a>
```

---

## Testing Accessibility

### Automated Testing

```typescript
// jest + jest-axe
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('has no accessibility violations', async () => {
  const { container } = render(<ProductCard product={mockProduct} />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Manual Testing Checklist

- [ ] Navigate entire page with keyboard only
- [ ] Use screen reader (VoiceOver, NVDA)
- [ ] Zoom to 200% - still usable?
- [ ] Check with browser accessibility inspector
- [ ] Test with high contrast mode
- [ ] Test with reduced motion enabled

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Divs for everything** | No semantics for AT | Use semantic HTML |
| **tabIndex > 0** | Breaks natural tab order | Remove positive tabIndex |
| **Outline: none** | No focus indicator | Use :focus-visible |
| **ARIA overuse** | Complex, error-prone | Native HTML first |
| **Color-only meaning** | Invisible to colorblind | Add icons, text |
| **Auto-playing media** | Disorienting, annoying | User-initiated only |
| **Mouse-only interactions** | Excludes keyboard users | Add keyboard handlers |
| **Missing alt text** | Images invisible to SR | Describe or mark decorative |
| **Non-descriptive links** | "Click here" is useless | Descriptive link text |

---

## Checklist

### Semantic HTML
- [ ] Correct heading hierarchy
- [ ] Buttons for actions, links for navigation
- [ ] Semantic landmarks (header, nav, main, footer)
- [ ] Lists use ul/ol/li

### Keyboard
- [ ] All interactive elements focusable
- [ ] Visible focus indicators
- [ ] Logical tab order
- [ ] Skip link present
- [ ] Modals trap focus

### Screen Readers
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Error messages linked to inputs
- [ ] Dynamic content uses live regions
- [ ] Icons have accessible names

### Visual
- [ ] Color contrast meets 4.5:1
- [ ] Color is not only indicator
- [ ] Works at 200% zoom
- [ ] Reduced motion respected

### Forms
- [ ] All inputs labeled
- [ ] Required fields indicated
- [ ] Errors clearly identified
- [ ] Error messages helpful

---

## Resources

- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [axe DevTools Browser Extension](https://www.deque.com/axe/devtools/)
- [VoiceOver User Guide](https://support.apple.com/guide/voiceover/welcome/mac)
- [NVDA Screen Reader](https://www.nvaccess.org/download/)
