# Accessibility Checklist (WCAG 2.1 AA)

## Perceivable

### 1.1 Text Alternatives

- [ ] **Images have alt text** - All `<img>` elements have meaningful `alt` attributes
- [ ] **Decorative images** - Use `alt=""` or CSS background for decorative images
- [ ] **Complex images** - Charts, diagrams have detailed descriptions
- [ ] **Icons** - Icon buttons have accessible names (aria-label or visually hidden text)

```html
<!-- ✅ Good -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2 2024">
<button aria-label="Close dialog">
  <svg>...</svg>
</button>

<!-- ❌ Bad -->
<img src="chart.png" alt="chart">
<img src="banner.jpg">  <!-- Missing alt -->
```

### 1.2 Time-based Media

- [ ] **Captions** - Videos have synchronized captions
- [ ] **Transcripts** - Audio content has text transcripts
- [ ] **Audio descriptions** - Complex visuals described in audio

### 1.3 Adaptable

- [ ] **Semantic HTML** - Use proper heading hierarchy (h1 → h2 → h3)
- [ ] **Lists** - Use `<ul>`, `<ol>`, `<dl>` for list content
- [ ] **Tables** - Data tables have headers (`<th>`) and scope
- [ ] **Landmarks** - Use `<main>`, `<nav>`, `<header>`, `<footer>`
- [ ] **Reading order** - DOM order matches visual order

```html
<!-- ✅ Good -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>
<main>
  <h1>Page Title</h1>
  <section aria-labelledby="section-heading">
    <h2 id="section-heading">Section</h2>
  </section>
</main>
```

### 1.4 Distinguishable

- [ ] **Color contrast** - Text: 4.5:1 ratio (3:1 for large text)
- [ ] **Not color alone** - Don't convey info by color alone
- [ ] **Resize text** - Works at 200% zoom
- [ ] **Text spacing** - Survives adjusted line/letter spacing
- [ ] **Reflow** - Content reflows at 320px width (no horizontal scroll)

```css
/* ✅ Good contrast */
.text { color: #333; background: #fff; }  /* 12.6:1 */

/* ❌ Poor contrast */
.text { color: #999; background: #fff; }  /* 2.8:1 */
```

## Operable

### 2.1 Keyboard Accessible

- [ ] **All functionality** - Everything works with keyboard alone
- [ ] **No keyboard traps** - Can always Tab away from elements
- [ ] **Visible focus** - Focus indicator always visible
- [ ] **Skip links** - "Skip to main content" link at top

```css
/* ✅ Good focus styles */
:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* ❌ Bad - removing focus */
:focus { outline: none; }
```

```html
<!-- Skip link -->
<a href="#main-content" class="skip-link">Skip to main content</a>
```

### 2.2 Enough Time

- [ ] **Adjustable timing** - Users can extend time limits
- [ ] **Pause/stop** - Moving content can be paused
- [ ] **No timeout** - Or warning with option to extend

### 2.3 Seizures

- [ ] **No flashing** - Nothing flashes more than 3 times/second

### 2.4 Navigable

- [ ] **Page titles** - Descriptive, unique `<title>` elements
- [ ] **Focus order** - Logical tab sequence
- [ ] **Link purpose** - Link text describes destination
- [ ] **Multiple ways** - Site map, search, or navigation
- [ ] **Headings** - Descriptive headings and labels
- [ ] **Focus visible** - Keyboard focus indicator visible

```html
<!-- ✅ Good link text -->
<a href="/pricing">View pricing plans</a>

<!-- ❌ Bad link text -->
<a href="/pricing">Click here</a>
<a href="/pricing">Read more</a>
```

### 2.5 Input Modalities

- [ ] **Target size** - Touch targets at least 44×44 CSS pixels
- [ ] **Motion actuation** - Alternatives to device motion
- [ ] **Pointer cancellation** - Can cancel accidental clicks

## Understandable

### 3.1 Readable

- [ ] **Page language** - `<html lang="en">`
- [ ] **Parts language** - `lang` attribute on foreign phrases

```html
<html lang="en">
<p>The French word <span lang="fr">bonjour</span> means hello.</p>
```

### 3.2 Predictable

- [ ] **No surprise changes** - Focus doesn't auto-change context
- [ ] **Consistent navigation** - Same position across pages
- [ ] **Consistent identification** - Same icons mean same things

### 3.3 Input Assistance

- [ ] **Error identification** - Errors clearly described in text
- [ ] **Labels** - All inputs have visible labels
- [ ] **Error suggestions** - Help users fix errors
- [ ] **Error prevention** - Confirm destructive actions

```html
<!-- ✅ Good form -->
<label for="email">Email address</label>
<input type="email" id="email" aria-describedby="email-error" aria-invalid="true">
<span id="email-error" role="alert">Please enter a valid email address</span>

<!-- ❌ Bad form -->
<input type="email" placeholder="Email">  <!-- No label -->
```

## Robust

### 4.1 Compatible

- [ ] **Valid HTML** - No duplicate IDs, proper nesting
- [ ] **ARIA correct** - Valid ARIA attributes and states
- [ ] **Status messages** - Use `role="status"` or `role="alert"`

```html
<!-- ✅ Correct ARIA -->
<button aria-expanded="false" aria-controls="menu">Menu</button>
<ul id="menu" hidden>...</ul>

<!-- Status message -->
<div role="status" aria-live="polite">Form saved successfully</div>
```

## Common Components

### Buttons

```html
<button type="button">Click me</button>

<!-- Icon button -->
<button type="button" aria-label="Delete item">
  <svg aria-hidden="true">...</svg>
</button>

<!-- Toggle button -->
<button type="button" aria-pressed="false">Bold</button>
```

### Forms

```html
<form>
  <div>
    <label for="name">Name (required)</label>
    <input type="text" id="name" required aria-required="true">
  </div>

  <fieldset>
    <legend>Preferred contact method</legend>
    <input type="radio" id="email" name="contact" value="email">
    <label for="email">Email</label>
    <input type="radio" id="phone" name="contact" value="phone">
    <label for="phone">Phone</label>
  </fieldset>
</form>
```

### Modals

```html
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Confirm deletion</h2>
  <p>Are you sure you want to delete this item?</p>
  <button type="button">Cancel</button>
  <button type="button">Delete</button>
</div>
```

### Tabs

```html
<div role="tablist" aria-label="Settings">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">
    General
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2">
    Security
  </button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  General settings content
</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Security settings content
</div>
```

## Testing Tools

| Tool | Purpose |
|------|---------|
| axe DevTools | Browser extension for automated testing |
| WAVE | Visual accessibility feedback |
| Lighthouse | Chrome DevTools audit |
| NVDA/VoiceOver | Screen reader testing |
| Colour Contrast Analyser | Manual contrast checking |

## Quick Checks

```bash
# Run axe on page
npx axe URL

# Lighthouse accessibility
npx lighthouse URL --only-categories=accessibility
```

## Testing Checklist

1. [ ] Tab through page - logical order, visible focus
2. [ ] Use screen reader - content makes sense
3. [ ] Zoom to 200% - nothing breaks
4. [ ] Check contrast - all text passes
5. [ ] Disable CSS - content still accessible
6. [ ] Check form errors - clearly communicated
