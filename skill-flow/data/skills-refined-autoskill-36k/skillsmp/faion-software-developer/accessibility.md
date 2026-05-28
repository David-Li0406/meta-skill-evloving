---
id: accessibility
name: "Accessibility"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Accessibility

## Overview

Accessibility (a11y) ensures web applications are usable by people with disabilities, including visual, auditory, motor, and cognitive impairments. Following accessibility standards improves usability for everyone and is often legally required.

## When to Use

- All web development (should be default practice)
- Public-facing applications
- Enterprise software (legal compliance)
- Government and education websites
- E-commerce (broader market reach)

## Key Principles

- **Perceivable**: Information must be presentable in ways users can perceive
- **Operable**: Interface components must be operable
- **Understandable**: Information and UI must be understandable
- **Robust**: Content must be robust enough for assistive technologies

## Best Practices

### Semantic HTML

```html
<!-- BAD: Div soup without semantics -->
<div class="header">
  <div class="nav">
    <div class="nav-item" onclick="goHome()">Home</div>
    <div class="nav-item" onclick="goProducts()">Products</div>
  </div>
</div>
<div class="content">
  <div class="title">Welcome</div>
  <div class="text">Some content here</div>
</div>

<!-- GOOD: Semantic HTML -->
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/products">Products</a></li>
    </ul>
  </nav>
</header>
<main>
  <article>
    <h1>Welcome</h1>
    <p>Some content here</p>
  </article>
</main>
```

### ARIA Labels and Roles

```tsx
// Button with clear purpose
<button
  aria-label="Close dialog"
  aria-describedby="dialog-description"
  onClick={onClose}
>
  <CloseIcon aria-hidden="true" />
</button>

// Form with proper labeling
<form aria-labelledby="form-title">
  <h2 id="form-title">Contact Us</h2>

  <div>
    <label htmlFor="name">Full Name</label>
    <input
      id="name"
      type="text"
      aria-required="true"
      aria-invalid={errors.name ? "true" : "false"}
      aria-describedby={errors.name ? "name-error" : undefined}
    />
    {errors.name && (
      <span id="name-error" role="alert">
        {errors.name}
      </span>
    )}
  </div>

  <div>
    <label htmlFor="email">Email Address</label>
    <input
      id="email"
      type="email"
      aria-required="true"
      aria-invalid={errors.email ? "true" : "false"}
    />
  </div>

  <button type="submit">Send Message</button>
</form>

// Live regions for dynamic content
<div
  role="status"
  aria-live="polite"
  aria-atomic="true"
>
  {statusMessage}
</div>

<div
  role="alert"
  aria-live="assertive"
>
  {errorMessage}
</div>

// Navigation landmarks
<nav aria-label="Main">...</nav>
<nav aria-label="Footer">...</nav>

// Custom interactive component
<div
  role="button"
  tabIndex={0}
  aria-pressed={isPressed}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }}
>
  Toggle Feature
</div>
```

### Keyboard Navigation

```tsx
import { useRef, useState, useEffect } from 'react';

// Focus management in modals
function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      // Store current focus
      previousFocus.current = document.activeElement as HTMLElement;

      // Focus first focusable element in modal
      const focusable = modalRef.current?.querySelector<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      focusable?.focus();

      // Trap focus within modal
      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape') {
          onClose();
        }
        if (e.key === 'Tab') {
          trapFocus(e, modalRef.current!);
        }
      };

      document.addEventListener('keydown', handleKeyDown);
      return () => document.removeEventListener('keydown', handleKeyDown);
    } else {
      // Restore focus when modal closes
      previousFocus.current?.focus();
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <h2 id="modal-title">Modal Title</h2>
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  );
}

function trapFocus(event: KeyboardEvent, container: HTMLElement) {
  const focusableElements = container.querySelectorAll<HTMLElement>(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusableElements[0];
  const last = focusableElements[focusableElements.length - 1];

  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}

// Roving tabindex for composite widgets
function TabList({ tabs, activeTab, onSelect }) {
  const [focusIndex, setFocusIndex] = useState(0);
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([]);

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    let newIndex = index;

    switch (e.key) {
      case 'ArrowRight':
        newIndex = (index + 1) % tabs.length;
        break;
      case 'ArrowLeft':
        newIndex = (index - 1 + tabs.length) % tabs.length;
        break;
      case 'Home':
        newIndex = 0;
        break;
      case 'End':
        newIndex = tabs.length - 1;
        break;
      default:
        return;
    }

    e.preventDefault();
    setFocusIndex(newIndex);
    tabRefs.current[newIndex]?.focus();
  };

  return (
    <div role="tablist">
      {tabs.map((tab, index) => (
        <button
          key={tab.id}
          ref={(el) => (tabRefs.current[index] = el)}
          role="tab"
          aria-selected={activeTab === tab.id}
          aria-controls={`panel-${tab.id}`}
          tabIndex={focusIndex === index ? 0 : -1}
          onClick={() => onSelect(tab.id)}
          onKeyDown={(e) => handleKeyDown(e, index)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
```

### Color and Contrast

```css
/* Minimum contrast ratios (WCAG 2.1 AA)
   - Normal text: 4.5:1
   - Large text (18px+ or 14px+ bold): 3:1
   - UI components and graphics: 3:1
*/

:root {
  /* Color palette with accessible contrast */
  --color-text-primary: #1a1a1a;      /* High contrast on white */
  --color-text-secondary: #4a4a4a;    /* Still meets 4.5:1 */
  --color-text-on-primary: #ffffff;   /* White on brand color */

  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f5f5f5;

  --color-brand: #0066cc;             /* Meets 4.5:1 on white */
  --color-brand-dark: #004c99;        /* For hover states */

  --color-error: #c62828;             /* Red that meets contrast */
  --color-success: #2e7d32;           /* Green that meets contrast */

  /* Focus indicators */
  --focus-ring: 2px solid var(--color-brand);
  --focus-ring-offset: 2px;
}

/* Never use color alone to convey information */
.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-indicator.success {
  color: var(--color-success);
}

.status-indicator.success::before {
  content: "✓";  /* Icon in addition to color */
}

.status-indicator.error {
  color: var(--color-error);
}

.status-indicator.error::before {
  content: "✕";
}

/* Focus visible styles */
:focus {
  outline: none;
}

:focus-visible {
  outline: var(--focus-ring);
  outline-offset: var(--focus-ring-offset);
}

/* Skip link for keyboard users */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-brand);
  color: var(--color-text-on-primary);
  padding: 0.5rem 1rem;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### Images and Media

```tsx
// Images with meaningful alt text
<img
  src="/product-photo.jpg"
  alt="Red wireless headphones with noise cancellation"
/>

// Decorative images
<img
  src="/decorative-border.svg"
  alt=""
  role="presentation"
/>

// Complex images with long description
<figure>
  <img
    src="/quarterly-sales-chart.png"
    alt="Bar chart showing quarterly sales"
    aria-describedby="chart-description"
  />
  <figcaption id="chart-description">
    Q1 sales: $1.2M, Q2: $1.5M, Q3: $1.8M, Q4: $2.1M.
    Total growth of 75% year over year.
  </figcaption>
</figure>

// Video with captions and transcript
<video controls>
  <source src="/product-demo.mp4" type="video/mp4" />
  <track
    kind="captions"
    src="/product-demo-captions.vtt"
    srclang="en"
    label="English"
    default
  />
  <track
    kind="captions"
    src="/product-demo-captions-uk.vtt"
    srclang="uk"
    label="Ukrainian"
  />
</video>

// Audio with transcript link
<audio controls aria-describedby="audio-transcript">
  <source src="/podcast-episode.mp3" type="audio/mpeg" />
</audio>
<a id="audio-transcript" href="/transcripts/episode-1">
  Read transcript
</a>
```

### Forms and Validation

```tsx
function AccessibleForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const errorSummaryRef = useRef<HTMLDivElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors = validateForm();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      // Focus error summary
      errorSummaryRef.current?.focus();
    } else {
      // Submit form
      setSubmitted(true);
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      {/* Error summary at top of form */}
      {Object.keys(errors).length > 0 && (
        <div
          ref={errorSummaryRef}
          role="alert"
          tabIndex={-1}
          className="error-summary"
        >
          <h2>There are {Object.keys(errors).length} errors in the form</h2>
          <ul>
            {Object.entries(errors).map(([field, message]) => (
              <li key={field}>
                <a href={`#${field}`}>{message}</a>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="form-group">
        <label htmlFor="email">
          Email Address
          <span aria-hidden="true">*</span>
          <span className="visually-hidden">(required)</span>
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          aria-required="true"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? "email-error" : "email-hint"}
        />
        <span id="email-hint" className="hint">
          We'll never share your email
        </span>
        {errors.email && (
          <span id="email-error" className="error" role="alert">
            {errors.email}
          </span>
        )}
      </div>

      <div className="form-group">
        <fieldset>
          <legend>
            Notification Preferences
            <span className="visually-hidden">(required, select one)</span>
          </legend>
          <div>
            <input
              type="radio"
              id="notify-email"
              name="notify"
              value="email"
              required
            />
            <label htmlFor="notify-email">Email</label>
          </div>
          <div>
            <input
              type="radio"
              id="notify-sms"
              name="notify"
              value="sms"
            />
            <label htmlFor="notify-sms">SMS</label>
          </div>
        </fieldset>
      </div>

      <button type="submit">
        Submit
        <span aria-live="polite" className="visually-hidden">
          {submitted ? "Form submitted successfully" : ""}
        </span>
      </button>
    </form>
  );
}
```

### Testing Accessibility

```typescript
// Jest + Testing Library
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(<MyComponent />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have proper heading hierarchy', () => {
    render(<Page />);

    const headings = screen.getAllByRole('heading');
    // Check h1 exists and is first
    expect(headings[0]).toHaveAttribute('aria-level', '1');
  });

  it('should have accessible form labels', () => {
    render(<ContactForm />);

    const emailInput = screen.getByLabelText(/email/i);
    expect(emailInput).toBeInTheDocument();
    expect(emailInput).toHaveAttribute('type', 'email');
  });

  it('should announce errors to screen readers', async () => {
    render(<ContactForm />);

    // Submit empty form
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    // Check for alert role
    const alert = screen.getByRole('alert');
    expect(alert).toHaveTextContent(/email is required/i);
  });

  it('should be keyboard navigable', async () => {
    render(<Navigation />);

    // Tab to first link
    await userEvent.tab();
    expect(screen.getByRole('link', { name: /home/i })).toHaveFocus();

    // Tab to second link
    await userEvent.tab();
    expect(screen.getByRole('link', { name: /products/i })).toHaveFocus();
  });
});
```

```yaml
# Lighthouse CI for automated accessibility audits
# .github/workflows/a11y.yml
name: Accessibility

on: [push, pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build
        run: npm run build

      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          configPath: ./lighthouserc.json
          uploadArtifacts: true

# lighthouserc.json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:accessibility": ["error", { "minScore": 0.9 }],
        "color-contrast": "error",
        "document-title": "error",
        "html-has-lang": "error",
        "image-alt": "error",
        "link-name": "error"
      }
    }
  }
}
```

### Common Patterns

```css
/* Visually hidden but accessible to screen readers */
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

/* Reduced motion for users who prefer it */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  :root {
    --color-text-primary: #000000;
    --color-bg-primary: #ffffff;
    --color-brand: #0000cc;
  }
}
```

## Anti-patterns

- **Div with onclick**: Use buttons for interactive elements
- **Placeholder as label**: Placeholders disappear when typing
- **Color-only indicators**: Always add text/icons
- **Auto-playing media**: Respect user preferences
- **Disabled focus outlines**: Make them better, not invisible
- **Inaccessible custom components**: Use native elements or ARIA properly

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WAI-ARIA Practices](https://www.w3.org/WAI/ARIA/apg/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
- [Inclusive Components](https://inclusive-components.design/)
- [Deque University](https://dequeuniversity.com/)
