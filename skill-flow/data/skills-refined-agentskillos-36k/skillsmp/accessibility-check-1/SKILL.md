---
name: accessibility-check
description: Web accessibility audit workflow for WCAG compliance
license: MIT
---

# Accessibility Check Skill

Use this skill when auditing or improving web accessibility compliance.

## When to Use

- Building new UI components
- Auditing existing features
- Before major releases
- After accessibility complaints
- Regular a11y reviews

## WCAG 2.1 Levels

| Level | Description | Target |
|-------|-------------|--------|
| A | Minimum accessibility | Required |
| AA | Standard compliance | **Recommended** |
| AAA | Enhanced accessibility | Ideal |

## Quick Checks

### 1. Keyboard Navigation

```bash
# Test without mouse:
# - Tab through all interactive elements
# - Shift+Tab to go backwards
# - Enter/Space to activate
# - Arrow keys for menus/selections
# - Escape to close modals
```

```typescript
// ✅ All interactive elements must be focusable
<button onClick={handleClick}>Click me</button>

// ❌ Bad: Div with click handler
<div onClick={handleClick}>Click me</div>

// ✅ If you must use div, add proper attributes
<div 
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
>
  Click me
</div>
```

### 2. Screen Reader Testing

```bash
# macOS: VoiceOver
# Cmd + F5 to toggle
# Ctrl + Option + arrows to navigate

# Windows: NVDA (free)
# Download from nvaccess.org

# Chrome: ChromeVox extension
```

### 3. Color Contrast

```css
/* Minimum contrast ratios */
/* Normal text (< 18px): 4.5:1 */
/* Large text (≥ 18px or 14px bold): 3:1 */

/* ❌ Bad: Low contrast */
.text {
  color: #999;
  background: #fff;  /* 2.8:1 ratio */
}

/* ✅ Good: Sufficient contrast */
.text {
  color: #595959;
  background: #fff;  /* 7:1 ratio */
}
```

## Common Issues & Fixes

### Images

```tsx
// ❌ Bad: No alt text
<img src="product.jpg" />

// ✅ Good: Descriptive alt
<img src="product.jpg" alt="Red wireless headphones" />

// ✅ Good: Decorative image
<img src="divider.svg" alt="" role="presentation" />

// ✅ Good: Complex image
<figure>
  <img src="chart.png" alt="Q4 sales chart" aria-describedby="chart-desc" />
  <figcaption id="chart-desc">
    Sales increased 45% from October to December, 
    with November showing the highest growth.
  </figcaption>
</figure>
```

### Forms

```tsx
// ❌ Bad: No label
<input type="email" placeholder="Email" />

// ✅ Good: Visible label
<label htmlFor="email">Email address</label>
<input type="email" id="email" />

// ✅ Good: With error
<label htmlFor="email">Email address</label>
<input 
  type="email" 
  id="email"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">
  Please enter a valid email address
</span>

// ✅ Good: Required field
<label htmlFor="name">
  Name <span aria-hidden="true">*</span>
</label>
<input type="text" id="name" required aria-required="true" />
```

### Buttons & Links

```tsx
// ❌ Bad: Icon-only button
<button><Icon name="close" /></button>

// ✅ Good: With accessible name
<button aria-label="Close dialog">
  <Icon name="close" aria-hidden="true" />
</button>

// ❌ Bad: Vague link
<a href="/docs">Click here</a>

// ✅ Good: Descriptive link
<a href="/docs">Read the documentation</a>

// ✅ Good: Link that opens new tab
<a href="/external" target="_blank" rel="noopener noreferrer">
  External site
  <span className="sr-only">(opens in new tab)</span>
</a>
```

### Headings

```tsx
// ❌ Bad: Skipped levels
<h1>Page Title</h1>
<h3>Section</h3>  {/* Skipped h2! */}

// ✅ Good: Sequential levels
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

### Focus Management

```tsx
// ✅ Visible focus styles
button:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

// ✅ Focus trap in modal
import { FocusTrap } from '@headlessui/react';

function Modal({ children }) {
  return (
    <FocusTrap>
      <div role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <h2 id="modal-title">Modal Title</h2>
        {children}
      </div>
    </FocusTrap>
  );
}

// ✅ Return focus after close
const triggerRef = useRef();

function openModal() {
  triggerRef.current = document.activeElement;
  setIsOpen(true);
}

function closeModal() {
  setIsOpen(false);
  triggerRef.current?.focus();
}
```

### Skip Links

```tsx
// Add at top of page
<a href="#main-content" className="skip-link">
  Skip to main content
</a>

<nav aria-label="Main navigation">...</nav>

<main id="main-content" tabIndex={-1}>
  ...
</main>

// CSS
.skip-link {
  position: absolute;
  left: -9999px;
  z-index: 999;
}

.skip-link:focus {
  left: 50%;
  transform: translateX(-50%);
  top: 10px;
  padding: 8px 16px;
  background: #000;
  color: #fff;
}
```

### Live Regions

```tsx
// Announce dynamic updates
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Urgent announcements
<div role="alert">
  Error: Your session has expired.
</div>

// Loading states
function SearchResults({ isLoading, results }) {
  return (
    <>
      <div aria-live="polite" className="sr-only">
        {isLoading ? 'Loading results...' : `Found ${results.length} results`}
      </div>
      {/* Visual content */}
    </>
  );
}
```

## Testing Tools

```bash
# Automated testing
npm install @axe-core/react jest-axe

# In development (console warnings)
import React from 'react';
import ReactDOM from 'react-dom';
import axe from '@axe-core/react';

if (process.env.NODE_ENV !== 'production') {
  axe(React, ReactDOM, 1000);
}

# In tests
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('should have no a11y violations', async () => {
  const { container } = render(<MyComponent />);
  expect(await axe(container)).toHaveNoViolations();
});
```

### Browser Extensions

| Tool | Purpose |
|------|---------|
| axe DevTools | Comprehensive testing |
| WAVE | Visual evaluation |
| HeadingsMap | Heading structure |
| Landmarks | ARIA landmarks |

## Screen Reader Only CSS

```css
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

## Audit Checklist

### Perceivable
- [ ] Images have alt text
- [ ] Videos have captions
- [ ] Color is not the only indicator
- [ ] Text has sufficient contrast

### Operable
- [ ] All functions work with keyboard
- [ ] No keyboard traps
- [ ] Skip links provided
- [ ] Focus indicator visible
- [ ] No time limits (or adjustable)

### Understandable
- [ ] Language is declared
- [ ] Navigation is consistent
- [ ] Error messages are clear
- [ ] Labels are descriptive

### Robust
- [ ] Valid HTML
- [ ] ARIA used correctly
- [ ] Works with assistive tech
- [ ] Name, role, value exposed

## Report Template

```markdown
## Accessibility Audit

### Summary
- Issues found: 12
- Critical: 3
- Serious: 5
- Moderate: 4

### Critical Issues

#### Missing form labels
**Location**: Login form
**WCAG**: 1.3.1, 4.1.2
**Impact**: Screen reader users cannot identify fields

**Fix**:
```html
<label for="email">Email</label>
<input id="email" type="email">
```

### Recommendations
1. Add eslint-plugin-jsx-a11y
2. Include a11y in PR checklist
3. Test with screen reader monthly
```
