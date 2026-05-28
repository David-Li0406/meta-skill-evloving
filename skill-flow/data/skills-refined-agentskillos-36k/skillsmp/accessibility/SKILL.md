---
name: accessibility
description: WCAG 2.1 accessibility guidelines and implementation patterns. Use when creating UI components, validating color contrast, implementing keyboard navigation, or ensuring screen reader compatibility.
allowed-tools: Read, Edit, Bash(npm:*, npx:*, python3:*)
---

# Accessibility (WCAG 2.1) Guidelines

Domain knowledge for building accessible web interfaces.

## When to Use

Apply this knowledge when:
- Creating or modifying UI components
- Choosing or validating color combinations
- Implementing interactive elements
- Adding images, media, or dynamic content
- Testing for accessibility compliance
- Responding to accessibility audit findings

## Key Concepts

### WCAG Conformance Levels

| Level | Description | Target |
|-------|-------------|--------|
| **A** | Minimum accessibility | Required |
| **AA** | Standard accessibility | **This template's target** |
| **AAA** | Enhanced accessibility | Optional |

### The Four Principles (POUR)

1. **Perceivable** - Users can perceive content
2. **Operable** - Users can navigate and interact
3. **Understandable** - Content is readable and predictable
4. **Robust** - Works with assistive technologies

## Color Contrast Requirements

### WCAG AA Minimum Ratios

| Content Type | Minimum Ratio | Example |
|--------------|---------------|---------|
| Normal text (< 18px) | **4.5:1** | Body copy |
| Large text (>= 18px bold or >= 24px) | **3:1** | Headings |
| UI components & graphics | **3:1** | Buttons, icons |
| Non-essential decorative | No requirement | Background patterns |

### Calculating Contrast

```bash
# This template includes a validator
npm run validate:design
```

**Manual Check Formula**:
```
Contrast Ratio = (L1 + 0.05) / (L2 + 0.05)
Where L1 = lighter color luminance, L2 = darker
```

### Safe Color Combinations

```yaml
# In your {domain}.yaml
design:
  colors:
    # High contrast text colors
    text: "#1F2937"           # Dark gray on white: 12.6:1
    text-muted: "#6B7280"     # Medium gray on white: 5.0:1

    # Background combinations
    background: "#FFFFFF"
    surface: "#F9FAFB"        # Subtle distinction

    # Interactive elements
    primary: "#2563EB"        # Blue on white: 4.5:1
    primary-hover: "#1D4ED8"  # Darker for hover: 6.4:1
```

### Common Contrast Failures

```css
/* WRONG: Fails AA (2.5:1) */
.light-text {
  color: #9CA3AF; /* Gray 400 */
  background: #FFFFFF;
}

/* CORRECT: Passes AA (5.0:1) */
.muted-text {
  color: #6B7280; /* Gray 500 */
  background: #FFFFFF;
}
```

## Keyboard Navigation

### Focus Requirements

All interactive elements MUST be:
1. Reachable via Tab key
2. Visually focused (visible outline)
3. Activatable via Enter/Space

**Focus Styles**:

```css
/* WRONG: Never remove focus entirely */
*:focus {
  outline: none;
}

/* CORRECT: Custom but visible focus */
*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Remove outline only for mouse users */
*:focus:not(:focus-visible) {
  outline: none;
}
```

### Keyboard Patterns

| Element | Keys | Action |
|---------|------|--------|
| Link/Button | Enter | Activate |
| Button | Space | Activate |
| Checkbox | Space | Toggle |
| Radio group | Arrow keys | Select |
| Dropdown | Arrow keys | Navigate |
| Modal | Escape | Close |
| Tab panel | Arrow keys | Switch tabs |

### Skip Links

```astro
<!-- First focusable element on page -->
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<nav>...</nav>

<main id="main-content" tabindex="-1">
  ...
</main>

<style>
  .skip-link {
    position: absolute;
    left: -9999px;
    z-index: 999;
    padding: 1rem;
    background: var(--color-background);
  }

  .skip-link:focus {
    left: 1rem;
    top: 1rem;
  }
</style>
```

### Focus Trapping (Modals)

```javascript
function trapFocus(element) {
  const focusable = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  element.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
}
```

## Screen Reader Considerations

### Semantic HTML

```html
<!-- WRONG: Divs with no meaning -->
<div class="header">
  <div class="nav">...</div>
</div>
<div class="content">...</div>
<div class="footer">...</div>

<!-- CORRECT: Semantic elements -->
<header>
  <nav aria-label="Main">...</nav>
</header>
<main>...</main>
<footer>...</footer>
```

### ARIA Labels

**When to Use ARIA**:
1. When HTML semantics are insufficient
2. For dynamic content updates
3. For complex widgets

```astro
<!-- Icon buttons need labels -->
<button aria-label="Close menu">
  <svg><!-- X icon --></svg>
</button>

<!-- Landmark regions with multiple instances -->
<nav aria-label="Main navigation">...</nav>
<nav aria-label="Footer navigation">...</nav>

<!-- Custom widgets -->
<div
  role="tablist"
  aria-label="Product information"
>
  <button role="tab" aria-selected="true">Details</button>
  <button role="tab" aria-selected="false">Reviews</button>
</div>
```

### Live Regions

For dynamic content updates:

```astro
<!-- Polite: Announced after current speech -->
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

<!-- Assertive: Interrupts immediately (use sparingly) -->
<div aria-live="assertive" role="alert">
  {errorMessage}
</div>

<!-- DynamicContent component includes this -->
<DynamicContent
  endpoint="/api/data"
  ariaLabel="Comments section"
/>
```

### Hiding Decorative Content

```html
<!-- Hide from screen readers -->
<img src="decorative-line.svg" alt="" aria-hidden="true" />

<!-- OR use CSS background -->
<div class="decorative-bg"></div>
```

## Forms Accessibility

### Labels

```html
<!-- WRONG: No label association -->
<input type="email" placeholder="Email" />

<!-- CORRECT: Explicit label -->
<label for="email">Email address</label>
<input type="email" id="email" />

<!-- CORRECT: Implicit label -->
<label>
  Email address
  <input type="email" />
</label>
```

### Error Messages

```astro
<div class="form-field">
  <label for="email">Email</label>
  <input
    type="email"
    id="email"
    aria-invalid={hasError}
    aria-describedby={hasError ? "email-error" : undefined}
  />
  {hasError && (
    <p id="email-error" class="error" role="alert">
      Please enter a valid email address
    </p>
  )}
</div>
```

### Required Fields

```html
<label for="name">
  Name <span aria-hidden="true">*</span>
  <span class="sr-only">(required)</span>
</label>
<input type="text" id="name" required aria-required="true" />
```

## Images and Media

### Alt Text Guidelines

| Image Type | Alt Text |
|------------|----------|
| Informative | Describe content and purpose |
| Decorative | `alt=""` (empty) |
| Functional (link/button) | Describe action |
| Complex (charts) | Brief alt + long description |
| Text in image | Include all text |

```html
<!-- Informative -->
<img src="team.jpg" alt="Our team of 5 engineers at the 2024 conference" />

<!-- Decorative -->
<img src="divider.svg" alt="" />

<!-- Functional -->
<a href="/home">
  <img src="logo.svg" alt="Return to homepage" />
</a>

<!-- Complex -->
<figure>
  <img
    src="chart.png"
    alt="Sales increased 45% in Q4"
    aria-describedby="chart-desc"
  />
  <figcaption id="chart-desc">
    Detailed breakdown: Q1: $100k, Q2: $120k, Q3: $110k, Q4: $160k
  </figcaption>
</figure>
```

### Video Captions

```html
<video controls>
  <source src="video.mp4" type="video/mp4" />
  <track
    kind="captions"
    src="captions.vtt"
    srclang="en"
    label="English"
    default
  />
</video>
```

## Testing Tools and Methods

### Automated Testing

```bash
# Lighthouse accessibility audit
npm run lighthouse

# axe-core (via browser extension or CLI)
npx @axe-core/cli https://localhost:4321

# This template's built-in checks
npm run validate:design  # Color contrast
npm run test            # Includes a11y linting
```

### Manual Testing Checklist

1. **Keyboard Only**
   - [ ] Tab through entire page
   - [ ] All interactive elements reachable
   - [ ] Focus visible at all times
   - [ ] Logical tab order

2. **Screen Reader**
   - [ ] Test with VoiceOver (Mac) or NVDA (Windows)
   - [ ] Page title announced
   - [ ] Headings navigable
   - [ ] Links make sense out of context
   - [ ] Form labels announced

3. **Visual**
   - [ ] Zoom to 200% - content still usable
   - [ ] Disable CSS - content still readable
   - [ ] Color not sole indicator of meaning

### Browser DevTools

```
Chrome: Lighthouse > Accessibility
Firefox: Accessibility Inspector
Safari: Audit tab > Accessibility
```

## Project-Specific Implementation

### Validation Hooks

This template validates accessibility automatically:

```bash
# Pre-commit checks contrast ratios
npm run validate:design

# CI pipeline runs Lighthouse with thresholds
# See: .github/workflows/ci.yml
# Accessibility score must be >= 95
```

### DynamicContent Accessibility

```astro
<!-- The DynamicContent component handles: -->
<!-- - aria-live for updates -->
<!-- - aria-busy during loading -->
<!-- - role="region" with label -->

<DynamicContent
  endpoint="/api/comments"
  ariaLabel="Comments section"  <!-- Always provide this -->
  skeleton="shimmer"
/>
```

### Design Tokens Validation

```yaml
# {domain}.yaml - Validated for contrast
design:
  colors:
    primary: "#2563EB"      # Checked against background
    text: "#1F2937"         # Must meet 4.5:1
    text-muted: "#6B7280"   # Must meet 4.5:1
```

## Common Mistakes

### 1. Missing Focus Styles

```css
/* WRONG */
button:focus { outline: none; }

/* CORRECT */
button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

### 2. Using Color Alone for Meaning

```html
<!-- WRONG -->
<span class="text-red">Error</span>

<!-- CORRECT -->
<span class="text-red" role="alert">
  <svg aria-hidden="true"><!-- Error icon --></svg>
  Error: Invalid email
</span>
```

### 3. Missing Heading Hierarchy

```html
<!-- WRONG: Skipping levels -->
<h1>Page Title</h1>
<h3>Section</h3>

<!-- CORRECT: Sequential -->
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

### 4. Click-Only Interactions

```javascript
// WRONG: Mouse only
element.addEventListener('click', handler);

// CORRECT: Keyboard accessible
element.addEventListener('click', handler);
element.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    handler(e);
  }
});

// OR use semantic elements
<button onclick={handler}>Click me</button>
```

### 5. Autoplaying Media

```html
<!-- WRONG: Autoplays with sound -->
<video autoplay>

<!-- CORRECT: Autoplay only if muted -->
<video autoplay muted>

<!-- BEST: Let user control -->
<video controls>
```

## Quick Reference

### Minimum Requirements (AA)

- [ ] 4.5:1 contrast for normal text
- [ ] 3:1 contrast for large text and UI
- [ ] All functionality keyboard accessible
- [ ] Focus visible on all elements
- [ ] Images have alt text
- [ ] Form fields have labels
- [ ] Page has title and lang attribute
- [ ] Heading hierarchy is logical
- [ ] Links are distinguishable

### ARIA Quick Rules

1. Don't use ARIA if HTML works
2. Don't change native semantics
3. All interactive ARIA controls must be keyboard accessible
4. Don't use `role="presentation"` or `aria-hidden="true"` on focusable elements
5. All interactive elements must have accessible names

## Related

- Validator: `scripts/validate-design-tokens.py`
- CI Check: `.github/workflows/ci.yml`
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- ARIA Patterns: https://www.w3.org/WAI/ARIA/apg/patterns/
