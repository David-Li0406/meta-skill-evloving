# WCAG 2.1 AA Checklist

## Perceivable

### 1.1 Text Alternatives

| Criterion | Requirement | Check |
|-----------|-------------|-------|
| 1.1.1 Non-text Content | All images have alt text | `<img alt="...">` |
| | Decorative images have empty alt | `<img alt="" role="presentation">` |
| | Complex images have long description | Link to description or `aria-describedby` |

```html
<!-- Informative image -->
<img src="chart.png" alt="Sales increased 25% in Q4 2024">

<!-- Decorative image -->
<img src="divider.png" alt="" role="presentation">

<!-- Complex image -->
<img src="diagram.png" alt="System architecture" aria-describedby="diagram-desc">
<div id="diagram-desc">Detailed description...</div>
```

### 1.2 Time-based Media

| Criterion | Requirement |
|-----------|-------------|
| 1.2.1 Audio-only/Video-only | Provide transcript or audio description |
| 1.2.2 Captions | Provide captions for video |
| 1.2.3 Audio Description | Provide audio description for video |
| 1.2.5 Audio Description (Prerecorded) | Same as 1.2.3 at AA level |

### 1.3 Adaptable

| Criterion | Requirement | Check |
|-----------|-------------|-------|
| 1.3.1 Info and Relationships | Use semantic HTML | `<nav>`, `<main>`, `<aside>` |
| | Tables have headers | `<th scope="col/row">` |
| | Forms have labels | `<label for="id">` |
| 1.3.2 Meaningful Sequence | Reading order is logical | Check with CSS disabled |
| 1.3.3 Sensory Characteristics | Don't rely only on shape, size, color | "Click the red button on the left" |

```html
<!-- Good: semantic structure -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>
<main>
  <h1>Page Title</h1>
  <article>...</article>
</main>

<!-- Good: labeled form -->
<label for="email">Email address</label>
<input type="email" id="email" required>
```

### 1.4 Distinguishable

| Criterion | Requirement | Ratio |
|-----------|-------------|-------|
| 1.4.1 Use of Color | Color not only means of conveying info | N/A |
| 1.4.3 Contrast (Minimum) | Text contrast ratio | 4.5:1 (normal), 3:1 (large) |
| 1.4.4 Resize Text | Text can resize to 200% | No loss of content |
| 1.4.5 Images of Text | Use real text, not images | Exceptions: logos |
| 1.4.10 Reflow | Content reflows at 320px | No horizontal scroll |
| 1.4.11 Non-text Contrast | UI components and graphics | 3:1 |
| 1.4.12 Text Spacing | Supports custom spacing | No loss of content |
| 1.4.13 Content on Hover/Focus | Dismissible, hoverable, persistent | Tooltips, dropdowns |

```css
/* Good: sufficient contrast */
.text { color: #333; background: #fff; } /* 12.6:1 */
.button { color: #fff; background: #0066cc; } /* 5.1:1 */

/* Good: respects user text spacing */
p {
  line-height: 1.5;      /* At least 1.5x font size */
  letter-spacing: 0.12em; /* At least 0.12x */
  word-spacing: 0.16em;   /* At least 0.16x */
  /* No overflow:hidden on text containers */
}
```

## Operable

### 2.1 Keyboard Accessible

| Criterion | Requirement | Check |
|-----------|-------------|-------|
| 2.1.1 Keyboard | All functionality via keyboard | Tab through page |
| 2.1.2 No Keyboard Trap | Focus can leave all components | Test modals, widgets |
| 2.1.4 Character Key Shortcuts | Single character shortcuts can be turned off | Or require modifier |

```html
<!-- Good: keyboard accessible custom button -->
<div role="button" tabindex="0"
     onkeydown="if(event.key==='Enter'||event.key===' ')activate()">
  Click me
</div>

<!-- Better: just use a button -->
<button onclick="activate()">Click me</button>
```

### 2.2 Enough Time

| Criterion | Requirement |
|-----------|-------------|
| 2.2.1 Timing Adjustable | User can turn off, adjust, or extend time limits |
| 2.2.2 Pause, Stop, Hide | Moving content can be paused |

### 2.3 Seizures and Physical Reactions

| Criterion | Requirement |
|-----------|-------------|
| 2.3.1 Three Flashes or Below | No content flashes more than 3 times/second |

### 2.4 Navigable

| Criterion | Requirement | Check |
|-----------|-------------|-------|
| 2.4.1 Bypass Blocks | Skip navigation link | First focusable element |
| 2.4.2 Page Titled | Descriptive page title | `<title>Page - Site</title>` |
| 2.4.3 Focus Order | Logical focus order | Tab through page |
| 2.4.4 Link Purpose | Link text describes destination | Not "click here" |
| 2.4.5 Multiple Ways | Multiple ways to find pages | Nav + search + sitemap |
| 2.4.6 Headings and Labels | Descriptive headings | Clear hierarchy |
| 2.4.7 Focus Visible | Focus indicator visible | `:focus` styles |

```html
<!-- Good: skip link -->
<a href="#main" class="skip-link">Skip to main content</a>
<nav>...</nav>
<main id="main">...</main>

<!-- Good: descriptive link -->
<a href="/products">View all products</a>

<!-- Bad: non-descriptive -->
<a href="/products">Click here</a>
```

### 2.5 Input Modalities

| Criterion | Requirement |
|-----------|-------------|
| 2.5.1 Pointer Gestures | Multi-point gestures have single-point alternative |
| 2.5.2 Pointer Cancellation | Down-event doesn't trigger, or can be aborted |
| 2.5.3 Label in Name | Visible label is in accessible name |
| 2.5.4 Motion Actuation | Motion input has UI alternative |

## Understandable

### 3.1 Readable

| Criterion | Requirement | Check |
|-----------|-------------|-------|
| 3.1.1 Language of Page | Page language declared | `<html lang="en">` |
| 3.1.2 Language of Parts | Language changes marked | `<span lang="fr">` |

### 3.2 Predictable

| Criterion | Requirement |
|-----------|-------------|
| 3.2.1 On Focus | Focus doesn't change context |
| 3.2.2 On Input | Input doesn't change context unexpectedly |
| 3.2.3 Consistent Navigation | Navigation consistent across pages |
| 3.2.4 Consistent Identification | Same functions identified consistently |

### 3.3 Input Assistance

| Criterion | Requirement | Check |
|-----------|-------------|-------|
| 3.3.1 Error Identification | Errors identified and described | Clear error messages |
| 3.3.2 Labels or Instructions | Labels or instructions provided | Form fields labeled |
| 3.3.3 Error Suggestion | Suggest corrections | "Did you mean...?" |
| 3.3.4 Error Prevention | Review before submit (legal, financial) | Confirmation step |

```html
<!-- Good: accessible error -->
<label for="email">Email</label>
<input type="email" id="email" aria-invalid="true" aria-describedby="email-error">
<span id="email-error" role="alert">Please enter a valid email address</span>
```

## Robust

### 4.1 Compatible

| Criterion | Requirement | Check |
|-----------|-------------|-------|
| 4.1.1 Parsing | Valid HTML | W3C validator |
| 4.1.2 Name, Role, Value | All UI components have accessible name/role | ARIA when needed |
| 4.1.3 Status Messages | Status announced without focus | `role="alert"`, `aria-live` |

```html
<!-- Good: status message announced -->
<div role="alert" aria-live="polite">
  Your changes have been saved.
</div>
```

## Testing Tools

```bash
# Automated testing
npx axe-core-cli https://example.com
npx pa11y https://example.com

# Browser extensions
# - axe DevTools
# - WAVE
# - Accessibility Insights

# Manual testing
# - Keyboard-only navigation
# - Screen reader (VoiceOver, NVDA, JAWS)
# - Browser zoom to 200%
# - Windows High Contrast Mode
```
