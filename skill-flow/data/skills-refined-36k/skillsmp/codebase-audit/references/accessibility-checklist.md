# Accessibility Checklist

Reference for: Codebase Audit

Quick reference for detecting accessibility (a11y) issues in web applications.

## Why Accessibility Matters

- **15% of the world** has some form of disability
- **Legal requirement** in many jurisdictions (ADA, Section 508, WCAG)
- **Better UX for everyone** (keyboard nav, clear labels, etc.)
- **SEO benefits** (semantic HTML, alt text)

## Quick Detection Commands

```bash
# Images without alt text
grep -rn "<img" --include="*.jsx" --include="*.tsx" --include="*.vue" --include="*.html" . | grep -v 'alt='

# Buttons without labels
grep -rn "<button" --include="*.jsx" --include="*.tsx" --include="*.vue" . | grep -v 'aria-label'

# Form inputs without labels
grep -rn "<input" --include="*.jsx" --include="*.tsx" --include="*.html" . | grep -v 'aria-label\|<label'

# Interactive elements without keyboard support
grep -rn "onClick" --include="*.jsx" --include="*.tsx" . | grep -v "onKeyDown\|onKeyPress" | head -20

# Missing lang attribute
grep -rn "<html" --include="*.html" --include="*.jsx" --include="*.tsx" . | grep -v 'lang='

# Low contrast text
grep -rn "color.*#[a-fA-F0-9]" --include="*.css" --include="*.scss" . | head -20
```

## 1. Semantic HTML

**Issue:** Using divs/spans instead of semantic elements.

### Detection

```bash
# Clickable divs (should be buttons)
grep -rn "<div.*onClick" --include="*.jsx" --include="*.tsx" .

# Custom select elements
grep -rn "role=\"listbox\"" --include="*.jsx" --include="*.tsx" .
```

### Bad vs Good

```jsx
// ❌ Bad: Non-semantic
<div onClick={handleSubmit}>Submit</div>

// ✓ Good: Semantic button
<button onClick={handleSubmit}>Submit</button>

// ❌ Bad: Div navigation
<div className="nav">
  <div onClick={goHome}>Home</div>
</div>

// ✓ Good: Semantic nav
<nav>
  <a href="/">Home</a>
</nav>
```

## 2. Images and Media

### Alt Text

**Rule:** All images need alt text (empty alt="" for decorative).

```jsx
// ❌ Bad: Missing alt
<img src="logo.png" />

// ✓ Good: Descriptive alt
<img src="logo.png" alt="Company Logo" />

// ✓ Good: Empty alt for decorative
<img src="decoration.png" alt="" />
```

### Detection

```bash
# Find images without alt
grep -rn "<img" --include="*.jsx" --include="*.tsx" --include="*.html" . | grep -v 'alt=' | head -20

# Find images with bad alt text
grep -rn 'alt="image\|alt="picture\|alt="photo"' --include="*.jsx" --include="*.tsx" .
```

### Video and Audio

```jsx
// ❌ Bad: No captions
<video src="tutorial.mp4" />

// ✓ Good: With captions and transcript
<video src="tutorial.mp4">
  <track kind="captions" src="captions.vtt" srclang="en" />
</video>
```

## 3. Keyboard Navigation

**Rule:** All interactive elements must be keyboard accessible.

### Tab Index

```jsx
// ❌ Bad: Positive tabindex (messes with natural order)
<button tabIndex={1}>Click me</button>

// ❌ Bad: Non-interactive element made interactive
<div tabIndex={0} onClick={handleClick}>Click</div>

// ✓ Good: Button (naturally focusable)
<button onClick={handleClick}>Click me</button>

// ✓ Good: Making custom widget focusable
<div role="button" tabIndex={0} onClick={handleClick} onKeyDown={handleKeyDown}>
  Custom Button
</div>
```

### Keyboard Handlers

```jsx
// ❌ Bad: Only onClick
<div onClick={handleClick}>Click me</div>

// ✓ Good: Click + keyboard support
<button
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
>
  Click me
</button>
```

### Detection

```bash
# Find onClick without keyboard handler
grep -rn "onClick" --include="*.jsx" --include="*.tsx" . | grep -v "onKeyDown\|onKeyPress" | head -20

# Find positive tabindex
grep -rn 'tabIndex.*[1-9]' --include="*.jsx" --include="*.tsx" .
```

## 4. Forms

### Labels

**Rule:** Every form input needs an associated label.

```jsx
// ❌ Bad: No label
<input type="text" name="email" />

// ✓ Good: Associated label
<label htmlFor="email">Email</label>
<input type="text" id="email" name="email" />

// ✓ Good: aria-label
<input type="text" name="email" aria-label="Email address" />

// ✓ Good: Wrapping label
<label>
  Email
  <input type="text" name="email" />
</label>
```

### Error Messages

```jsx
// ❌ Bad: Visual-only error
<input type="text" className="error" />
<span className="error-text">Invalid email</span>

// ✓ Good: Aria-described error
<input
  type="text"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">Invalid email</span>
```

### Detection

```bash
# Inputs without labels
grep -rn "<input" --include="*.jsx" --include="*.tsx" --include="*.html" . | grep -v 'aria-label\|<label\|htmlFor' | head -20

# Forms without fieldset/legend
grep -rn "<form" --include="*.jsx" --include="*.tsx" . | head -10
```

## 5. ARIA (Accessible Rich Internet Applications)

### When to Use ARIA

**Rule:** No ARIA is better than bad ARIA. Use semantic HTML first.

```jsx
// ❌ Bad: Unnecessary ARIA
<button role="button" aria-label="Submit">Submit</button>

// ✓ Good: Button is already a button
<button>Submit</button>

// ✓ Good: ARIA when needed
<div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
  <h2 id="dialog-title">Confirmation</h2>
</div>
```

### Common ARIA Roles

| Role | Use Case | Example |
|------|----------|---------|
| `alert` | Important message | `<div role="alert">Error occurred</div>` |
| `dialog` | Modal window | `<div role="dialog" aria-modal="true">` |
| `navigation` | Nav section | `<div role="navigation">` (use `<nav>`) |
| `button` | Custom button | `<div role="button">` (use `<button>`) |
| `tablist` | Tabs widget | `<div role="tablist">` |

### Common ARIA Attributes

```jsx
// aria-label: Accessible name
<button aria-label="Close dialog">×</button>

// aria-labelledby: Reference to label element
<section aria-labelledby="section-title">
  <h2 id="section-title">About</h2>
</section>

// aria-describedby: Additional description
<input aria-describedby="password-requirements" />
<div id="password-requirements">Must be 12+ characters</div>

// aria-live: Dynamic content
<div aria-live="polite">Loading...</div>

// aria-hidden: Hide from screen readers
<span aria-hidden="true">★</span>

// aria-expanded: Collapsible state
<button aria-expanded="false" aria-controls="menu">Menu</button>
```

### Detection

```bash
# Find missing ARIA labels on interactive elements
grep -rn 'role="button"\|role="link"' --include="*.jsx" --include="*.tsx" . | grep -v 'aria-label'

// Find aria-hidden on interactive elements (bad)
grep -rn 'aria-hidden="true"' --include="*.jsx" --include="*.tsx" . | grep 'button\|input\|a href'
```

## 6. Color and Contrast

**Rule:** Don't rely on color alone, ensure sufficient contrast.

### Contrast Ratios (WCAG AA)

- **Normal text:** 4.5:1 minimum
- **Large text (18pt+):** 3:1 minimum
- **UI components:** 3:1 minimum

### Detection

```bash
# Find color-only indicators
grep -rn "color:.*red\|color:.*green" --include="*.css" --include="*.scss" . | head -20

# Find low contrast (manual check required)
grep -rn "color.*#[a-fA-F0-9].*background.*#[a-fA-F0-9]" --include="*.css" .
```

### Good Practices

```jsx
// ❌ Bad: Color-only error indication
<input style={{ borderColor: 'red' }} />

// ✓ Good: Multiple indicators
<input
  style={{ borderColor: 'red' }}
  aria-invalid="true"
  aria-describedby="error"
/>
<span id="error">
  <Icon name="error" />
  Email is required
</span>
```

## 7. Focus Management

### Visible Focus Indicators

```css
/* ❌ Bad: Removing focus outline */
*:focus {
  outline: none;
}

/* ✓ Good: Custom but visible focus */
button:focus {
  outline: 2px solid #0066CC;
  outline-offset: 2px;
}
```

### Focus Trapping (Modals)

```jsx
// ✓ Good: Focus trap in modal
function Modal({ isOpen, onClose }) {
  const modalRef = useRef();

  useEffect(() => {
    if (isOpen) {
      // Trap focus inside modal
      const focusableElements = modalRef.current.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];

      firstElement?.focus();

      const handleTab = (e) => {
        if (e.key === 'Tab') {
          if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
          } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      };

      document.addEventListener('keydown', handleTab);
      return () => document.removeEventListener('keydown', handleTab);
    }
  }, [isOpen]);

  return isOpen && <div role="dialog" ref={modalRef}>...</div>;
}
```

## 8. Screen Reader Testing

### Test Commands

```bash
# macOS VoiceOver
# CMD + F5 to enable
# Control + Option + arrow keys to navigate

# Windows Narrator
# WIN + CTRL + ENTER to enable
# CAPS + arrow keys to navigate
```

### What to Test

- Can you navigate using only keyboard?
- Are all interactive elements announced?
- Do error messages get announced?
- Can you complete forms without mouse?
- Do modals trap focus properly?

## 9. Common Patterns

### Skip Links

```jsx
// ✓ Good: Skip to main content link
<a href="#main" className="skip-link">Skip to main content</a>
<main id="main">...</main>

/* CSS */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### Loading States

```jsx
// ✓ Good: Accessible loading state
<button disabled aria-busy="true">
  <span aria-live="polite" aria-atomic="true">
    Loading...
  </span>
</button>
```

### Dynamic Content

```jsx
// ✓ Good: Announce dynamic updates
<div aria-live="polite" aria-atomic="true">
  {messages.length} new messages
</div>
```

## 10. Automated Testing Tools

### Axe DevTools

```bash
# Install
npm install --save-dev @axe-core/cli axe-core

# Run audit
npx axe https://localhost:3000
```

### Lighthouse

```bash
# Run accessibility audit
lighthouse https://example.com --only-categories=accessibility
```

### Pa11y

```bash
# Install
npm install -g pa11y

# Run audit
pa11y https://example.com
```

### Integration Tests

```javascript
// Jest + axe-core
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('should have no a11y violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## Priority Levels

| Level | Issues | Fix Timeline |
|-------|--------|-------------|
| **Critical** | Keyboard trap, missing form labels, no alt on meaningful images | Immediately |
| **High** | Low contrast, missing ARIA, focus indicators | Next sprint |
| **Medium** | Semantic HTML issues, missing skip links | Soon |
| **Low** | Redundant ARIA, minor contrast issues | Backlog |

## Quick Checklist

- [ ] All images have alt text
- [ ] All form inputs have labels
- [ ] Keyboard navigation works everywhere
- [ ] Focus indicators are visible
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] No content is conveyed by color alone
- [ ] Page has proper heading hierarchy (h1, h2, h3...)
- [ ] Skip link to main content exists
- [ ] All interactive elements are keyboard accessible
- [ ] Screen reader announces all important information
- [ ] Error messages are associated with inputs
- [ ] Modals trap focus properly
- [ ] Dynamic content updates are announced

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
