# WCAG 2.1 AA Compliance

WCAG (Web Content Accessibility Guidelines) configuration and rules enforced in the YourCompany web monorepo.

## Configuration

**Location**: `app/libs/a11y-jest/a11y.ts`

```typescript
import type { RunOptions } from 'axe-core';
import { axe } from 'jest-axe';

export const a11yConfig: RunOptions = {
  rules: {
    // Disabled rules
    'color-contrast': { enabled: false },

    // Media rules
    'audio-caption': { enabled: true },
    'video-caption': { enabled: true },
    'no-autoplay-audio': { enabled: true },

    // Viewport and orientation
    'meta-viewport-large': { enabled: true },
    'css-orientation-lock': { enabled: true },
    'meta-viewport': { enabled: true },
    'meta-refresh': { enabled: true },

    // Form and input rules
    label: { enabled: true },
    'select-name': { enabled: true },
    'input-image-alt': { enabled: true },
    'input-button-name': { enabled: true },
    'form-field-multiple-labels': { enabled: true },

    // Button rules
    'button-name': { enabled: true },

    // Link rules
    'link-name': { enabled: true },

    // Image rules
    'image-alt': { enabled: true },

    // ARIA rules
    'aria-required-attr': { enabled: true },
    'aria-valid-attr': { enabled: true },
    'aria-valid-attr-value': { enabled: true },
    'aria-allowed-attr': { enabled: true },
    'aria-roles': { enabled: true },
    'aria-required-children': { enabled: true },
    'aria-required-parent': { enabled: true },

    // Structure rules
    'duplicate-id-aria': { enabled: true },
    'frame-title': { enabled: true },
    'html-has-lang': { enabled: true },
    'html-xml-lang-mismatch': { enabled: true },
    bypass: { enabled: true },

    // Focus and navigation
    'scrollable-region-focusable': { enabled: true },
    'frame-focusable-content': { enabled: true },
    tabindex: { enabled: true },
    'focus-order-semantics': { enabled: true },

    // Visual rules
    blink: { enabled: true },
  },
  runOnly: {
    type: 'tag',
    values: ['wcag2a', 'wcag2aa'], // WCAG 2.1 Level A and AA
  },
};
```

## Compliance Level

The web monorepo targets **WCAG 2.1 Level AA** compliance:

- **Level A**: Basic web accessibility features (minimum)
- **Level AA**: Deals with the biggest barriers for disabled users (target)
- **Level AAA**: Highest level of accessibility (not targeted)

## Enabled Rules Reference

### Form & Input Rules

#### `label` ✅

**What**: All form inputs must have associated labels.

**Why**: Screen readers need labels to announce form field purposes.

```typescript
// ✅ PASS
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// ❌ FAIL
<div>Email</div>
<input type="email" />
```

#### `select-name` ✅

**What**: Select elements must have accessible names.

**Why**: Screen readers need to announce select dropdown purposes.

```typescript
// ✅ PASS
<label htmlFor="country">Country</label>
<select id="country">
  <option>USA</option>
</select>

// ❌ FAIL
<select>
  <option>USA</option>
</select>
```

#### `input-button-name` ✅

**What**: Input buttons must have discernible text.

**Why**: Screen readers need to announce button purposes.

```typescript
// ✅ PASS
<input type="submit" value="Submit Form" />
<input type="button" value="Cancel" aria-label="Cancel operation" />

// ❌ FAIL
<input type="button" />
```

### Button Rules

#### `button-name` ✅

**What**: Buttons must have discernible text.

**Why**: Users need to know what a button does before clicking it.

```typescript
// ✅ PASS
<button>Submit</button>
<button aria-label="Close dialog">×</button>

// ❌ FAIL
<button></button>
<button><span></span></button>
```

**Real example from web monorepo**:

```typescript
// Stepper.tsx:88
<NumberStepper.DecrementButton aria-label={`Decrease ${itemName} quantity`} />
```

### Link Rules

#### `link-name` ✅

**What**: Links must have discernible text.

**Why**: Screen readers need to announce link purposes and destinations.

```typescript
// ✅ PASS
<a href="/recipes">View Recipes</a>
<a href="/cart" aria-label="View shopping cart">
  <CartIcon />
</a>

// ❌ FAIL
<a href="/recipes"></a>
<a href="/cart"><CartIcon /></a>
```

### Image Rules

#### `image-alt` ✅

**What**: Images must have alt text.

**Why**: Screen readers need to describe images to visually impaired users.

```typescript
// ✅ PASS
<img src="recipe.jpg" alt="Chicken tikka masala recipe" />
<img src="decorative.jpg" alt="" /> // Decorative images

// ❌ FAIL
<img src="recipe.jpg" />
```

**Note**: Empty alt (`alt=""`) is valid for decorative images.

### ARIA Rules

#### `aria-required-attr` ✅

**What**: ARIA roles must have all required attributes.

**Why**: Incomplete ARIA implementation breaks screen reader functionality.

```typescript
// ✅ PASS
<div role="slider" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" />

// ❌ FAIL (missing required aria-valuenow)
<div role="slider" aria-valuemin="0" aria-valuemax="100" />
```

#### `aria-valid-attr` ✅

**What**: ARIA attributes must be valid.

**Why**: Invalid attributes are ignored by screen readers.

```typescript
// ✅ PASS
<button aria-label="Close">×</button>

// ❌ FAIL (aria-name is not a valid attribute)
<button aria-name="Close">×</button>
```

#### `aria-valid-attr-value` ✅

**What**: ARIA attributes must have valid values.

**Why**: Invalid values break screen reader announcements.

```typescript
// ✅ PASS
<button aria-pressed="true">Toggle</button>

// ❌ FAIL (aria-pressed must be "true" or "false", not "yes")
<button aria-pressed="yes">Toggle</button>
```

#### `aria-allowed-attr` ✅

**What**: ARIA attributes must be allowed for the element role.

**Why**: Using disallowed attributes can confuse screen readers.

```typescript
// ✅ PASS
<button aria-pressed="false">Toggle</button>

// ❌ FAIL (aria-checked is not allowed on button)
<button aria-checked="false">Toggle</button>
```

#### `aria-roles` ✅

**What**: ARIA roles must be valid.

**Why**: Invalid roles are ignored by screen readers.

```typescript
// ✅ PASS
<div role="dialog">...</div>

// ❌ FAIL (popup is not a valid role)
<div role="popup">...</div>
```

#### `aria-required-children` ✅

**What**: ARIA roles requiring children must have them.

**Why**: Proper structure is needed for screen reader navigation.

```typescript
// ✅ PASS
<div role="list">
  <div role="listitem">Item 1</div>
</div>

// ❌ FAIL (list must have listitem children)
<div role="list">
  <div>Item 1</div>
</div>
```

#### `aria-required-parent` ✅

**What**: ARIA roles requiring parent roles must have them.

**Why**: Proper hierarchy is needed for screen reader context.

```typescript
// ✅ PASS
<div role="list">
  <div role="listitem">Item</div>
</div>

// ❌ FAIL (listitem must have list parent)
<div>
  <div role="listitem">Item</div>
</div>
```

### Structure Rules

#### `html-has-lang` ✅

**What**: HTML element must have a lang attribute.

**Why**: Screen readers need to know the page language for correct pronunciation.

```html
<!-- ✅ PASS -->
<html lang="en">
  <!-- ❌ FAIL -->
  <html></html>
</html>
```

#### `frame-title` ✅

**What**: Frames and iframes must have title attributes.

**Why**: Screen readers need to announce frame purposes.

```typescript
// ✅ PASS
<iframe src="video.html" title="Product demonstration video" />

// ❌ FAIL
<iframe src="video.html" />
```

#### `bypass` ✅

**What**: Page must have a way to bypass repeated content.

**Why**: Keyboard users need to skip to main content without tabbing through navigation.

```typescript
// ✅ PASS
<a href="#main-content" className="skip-link">Skip to main content</a>
<nav>...</nav>
<main id="main-content">...</main>

// ❌ FAIL (no skip link present)
<nav>...</nav>
<main>...</main>
```

### Focus & Navigation Rules

#### `tabindex` ✅

**What**: tabindex values must be -1 or 0.

**Why**: Positive tabindex values create unpredictable tab order.

```typescript
// ✅ PASS
<div tabIndex={0}>Focusable</div>
<div tabIndex={-1}>Programmatically focusable</div>

// ❌ FAIL
<div tabIndex={1}>Wrong</div>
```

#### `scrollable-region-focusable` ✅

**What**: Scrollable regions must be keyboard accessible.

**Why**: Keyboard users need to scroll content without a mouse.

```typescript
// ✅ PASS
<div role="region" tabIndex={0} aria-label="Scrollable content" style={{ overflow: 'auto' }}>
  Long content...
</div>

// ❌ FAIL (missing tabIndex)
<div role="region" style={{ overflow: 'auto' }}>
  Long content...
</div>
```

### Viewport Rules

#### `meta-viewport` ✅

**What**: Viewport meta tag must not disable zooming.

**Why**: Users with low vision need to zoom in to read content.

```html
<!-- ✅ PASS -->
<meta name="viewport" content="width=device-width, initial-scale=1" />

<!-- ❌ FAIL (user-scalable=no prevents zooming) -->
<meta name="viewport" content="width=device-width, user-scalable=no" />
```

## Disabled Rules

### `color-contrast` ❌ (Currently Disabled)

**What**: Text must have sufficient color contrast (4.5:1 for normal text, 3:1 for large text).

**Why disabled**: Automated tools produce many false positives. Manual verification is more reliable.

**Manual checking required**: Use tools like:

- Chrome DevTools Contrast Checker
- WebAIM Contrast Checker (https://webaim.org/resources/contrastchecker/)
- Axe DevTools browser extension

```typescript
// Good contrast examples (need manual verification):
// Black text on white: 21:1 ✅
// #333 text on white: 12.6:1 ✅
// #666 text on white: 5.7:1 ✅
// #999 text on white: 2.8:1 ❌ (fails)
```

## GitHub Actions Integration

**PR Accessibility Check**: `.github/workflows/pr_accessibility_scores_check.yml`

```yaml
env:
  THRESHOLD: 50 # Blocks PR if score drops below 50
  ACCESSIBILITY_WEEKLY_SCORE_FILE_PATH: '.accessibility-weekly-score.json'
```

**Weekly Report**: `.github/workflows/cron_accessibility_weekly_score_update.yml`

Generates reports at:

```
https://hf-ui-assets.s3.eu-west-1.amazonaws.com/assets/a11y-web-reports/a11y-report.html
```

## Compliance Tracking

The web monorepo tracks:

- **Violations by team** (using `.claim.json` ownership)
- **Violations by rule** (which WCAG rules are most violated)
- **Weekly trends** (improving or degrading over time)
- **PR impact** (whether PR increases or decreases violations)

**Data stored in**:

- Google Sheets: https://docs.google.com/spreadsheets/d/1A0F9Y-WpeaFerbNb1eXjPCD-dTi8y51AkDUseCRcB1w/edit?gid=39388577
- JSON reports: `app/libs/a11y-jest/report/a11y-check-results-YYYY-MM-DD.json`

## Resources

- **WCAG 2.1 Quick Reference**: https://www.w3.org/WAI/WCAG21/quickref/
- **axe-core Rule Descriptions**: https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md
- **Deque University**: https://dequeuniversity.com/rules/axe/4.4/ (detailed rule documentation)
- **WebAIM**: https://webaim.org/ (accessibility resources)

## Testing Your Compliance

Run accessibility tests locally:

```bash
# Run all tests with accessibility checks
yarn test

# Generate accessibility report
RUN_A11Y_CHECKS=1 yarn test

# Check specific component
yarn test MyComponent.test.tsx
```

View generated report:

```
app/libs/a11y-jest/report/a11y-check-results-YYYY-MM-DD.json
```

Or view HTML report (when available):

```
app/libs/a11y-jest/report/a11y-report.html
```
