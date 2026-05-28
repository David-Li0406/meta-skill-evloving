---
name: web-accessibility
description: "WHAT: Web accessibility with semantic HTML, ARIA attributes, and checkA11y testing. WHEN: forms, interactive elements, modals, dialogs, WCAG 2.1 AA compliance. KEYWORDS: ARIA, aria-label, semantic HTML, checkA11y, axe-core, WCAG, form label, keyboard, screen reader."
---

# Web Accessibility Patterns for React & Next.js

## Documentation

This skill provides web-specific accessibility patterns for the YourCompany web monorepo:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[Testing Patterns](./references/testing.md)** - Automated a11y testing with axe-core and jest-axe
- **[WCAG Guidelines](./references/wcag.md)** - WCAG 2.1 AA compliance rules and configuration

## Core Principles

**Provide semantic HTML, ARIA attributes, and automated accessibility testing for all components.** Use translated strings for labels and test with axe-core in Jest tests.

**Why**: Web accessibility ensures the application is usable by everyone, including users with visual, auditory, motor, or cognitive disabilities. WCAG 2.1 AA compliance is required by law in many jurisdictions and improves SEO and overall user experience.

## When to Use This Skill

Use these patterns when:

- Creating any interactive element (buttons, links, inputs, forms)
- Building forms with input fields and validation
- Implementing modals, dialogs, or overlays
- Adding images, icons, or media to the UI
- Creating custom interactive widgets (steppers, carousels, accordions)
- Writing Jest tests for React components
- Ensuring WCAG 2.1 Level AA compliance
- Testing components with screen readers (VoiceOver, NVDA, JAWS)

## Automated Accessibility Testing

### Import and Use checkA11y

**Always** include accessibility checks in component tests:

```typescript
import { checkA11y } from '@/libs/a11y-jest';

describe('MyComponent', () => {
  it('should render with no accessibility violations', async () => {
    const { container } = render(<MyComponent />);

    // Your assertions here
    expect(screen.getByRole('button')).toBeInTheDocument();

    // Always check accessibility
    await checkA11y(container);
  });
});
```

**Why**: `checkA11y()` runs axe-core automated accessibility tests against your component, catching WCAG 2.1 AA violations before they reach production.

### Using checkA11yOutput for Reporting

For generating accessibility reports (used in CI/CD):

```typescript
import { checkA11yOutput } from '@/libs/a11y-jest';

describe('Age Verification', () => {
  it('should prompt users when adding alcoholic items', async () => {
    const { container } = render(
      <>
        <SaveButton onSaveSuccess={() => {}} />
        <ItemsGrid ids={[{ mainItemId: alcoholicItemId }]} />
      </>
    );

    // Test interactions...
    await userEvent.click(addButton);

    // Generate accessibility report
    await checkA11yOutput(container, expect.getState().currentTestName);
  });
});
```

**Real example from**: `app/spaces/store/integration/shared/age-verification/index.test.tsx:78`

**Why**: `checkA11yOutput()` generates JSON reports for tracking accessibility violations across the codebase, used by GitHub Actions workflows for weekly accessibility scoring.

## ARIA Attributes and Semantic HTML

### Button Accessibility

**Always** provide descriptive `aria-label` for buttons, especially icon-only buttons:

```typescript
// ✅ GOOD: Descriptive aria-label for icon button
<NumberStepper.DecrementButton
  onClick={onDecrease}
  data-test-id="cart-quantity-btn-decrease"
  aria-label={`Decrease ${itemName} quantity`}
/>

// ✅ GOOD: Dynamic aria-label with disabled state
<NumberStepper.DecrementButton
  onClick={onDecrease}
  disabled={!canDecrease}
  aria-label={`Decrease ${itemName} quantity (disabled)`}
/>

// ❌ BAD: Missing aria-label on icon button
<button onClick={onDecrease}>
  <MinusIcon />
</button>

// ❌ BAD: Generic aria-label
<button aria-label="Decrease">
  <MinusIcon />
</button>
```

**Real example from**: `app/spaces/one-time-purchase/modules/main/components/cart/components/Stepper.tsx:82-89`

**Why**: Screen readers need descriptive labels to announce button purposes. Dynamic labels should include current state (enabled/disabled) and context (item name).

### Form Labels

**Always** associate labels with form inputs using `htmlFor` or wrap inputs with `<label>`:

```typescript
// ✅ GOOD: Label with htmlFor
<label htmlFor="email-input">
  Email Address
</label>
<input id="email-input" type="email" name="email" />

// ✅ GOOD: Wrapped input
<label>
  Email Address
  <input type="email" name="email" />
</label>

// ❌ BAD: Input without associated label
<div>Email Address</div>
<input type="email" name="email" />

// ❌ BAD: Using placeholder as label
<input type="email" placeholder="Email Address" />
```

**Why**: Screen readers rely on properly associated labels to announce form field purposes. Placeholders alone are insufficient for accessibility.

### Interactive Element Roles

Use proper semantic HTML elements or provide explicit roles:

```typescript
// ✅ GOOD: Semantic button element
<button onClick={handleClick}>
  Submit
</button>

// ✅ GOOD: Link with proper href
<a href="/checkout">
  Proceed to Checkout
</a>

// ✅ GOOD: Div with explicit role and keyboard support
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
  aria-label="Open menu"
>
  ☰
</div>

// ❌ BAD: Div without role or keyboard support
<div onClick={handleClick}>
  Click me
</div>

// ❌ BAD: Link without href
<a onClick={handleClick}>
  Click me
</a>
```

**Why**: Semantic HTML elements provide built-in keyboard navigation and screen reader support. If using non-semantic elements, you must manually add role, tabIndex, and keyboard handlers.

## Component-Specific Patterns

### Number Steppers

Provide context-aware labels for stepper components:

```typescript
<NumberStepper size="sm" aria-label={`${itemName} quantity stepper`}>
  <NumberStepper.DecrementButton
    onClick={onDecrease}
    aria-label={`Decrease ${itemName} quantity`}
  />
  <NumberStepper.Value aria-label={`${itemName} quantity`}>
    {quantity}
  </NumberStepper.Value>
  <NumberStepper.IncrementButton
    onClick={onIncrease}
    aria-label={`Increase ${itemName} quantity`}
  />
</NumberStepper>
```

**Real example from**: `app/spaces/one-time-purchase/modules/main/components/cart/components/Stepper.tsx:82-135`

**Why**: Stepper components need labels for the container, each button, and the value display so screen readers can announce the full context.

### Disabled States

Communicate disabled states in aria-labels and provide tooltips for explanation:

```typescript
<Box
  aria-label={`Increase ${itemName} quantity (disabled)`}
  onMouseEnter={() => showTooltip()}
>
  <Tooltip
    content="Maximum quantity reached"
    trigger={
      <NumberStepper.IncrementButton
        disabled={!canIncrease}
        aria-label={`Increase ${itemName} quantity (disabled)`}
      />
    }
  />
</Box>
```

**Real example from**: `app/spaces/one-time-purchase/modules/main/components/cart/components/Stepper.tsx:136-168`

**Why**: Users need to understand why an element is disabled. Aria-labels should indicate disabled state, and tooltips should explain the reason.

### Modals and Dialogs

Use proper `role="dialog"` and manage focus:

```typescript
// ✅ GOOD: Proper dialog with role and aria-labelledby
<div
  role="dialog"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-description"
>
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-description">
    Are you sure you want to proceed?
  </p>
  <button onClick={handleConfirm}>Confirm</button>
  <button onClick={handleCancel}>Cancel</button>
</div>

// ❌ BAD: Generic div without dialog role
<div className="modal">
  <h2>Confirm Action</h2>
  <button onClick={handleConfirm}>Confirm</button>
</div>
```

**Why**: Screen readers need to know when a dialog is opened. Proper roles and aria-labelledby/describedby attributes provide context.

## Testing Patterns

### ESLint Enforcement

Enable the `a11y-jest/enforce-a11y-check-in-tests` rule in your module's `.eslintrc.json`:

```json
{
  "extends": ["../../../../.eslintrc.js"],
  "plugins": ["a11y-jest"],
  "rules": {
    "a11y-jest/enforce-a11y-check-in-tests": "warn"
  }
}
```

**From**: `scripts/eslint/plugins/a11y/README.md`

**Why**: This ESLint rule enforces that all React component tests include `checkA11y()` calls, ensuring accessibility testing is never forgotten.

### Test Examples

```typescript
// ✅ GOOD: Component test with accessibility check
describe('Button', () => {
  it('should render button with proper aria-label', async () => {
    const { container } = render(
      <Button onClick={jest.fn()} aria-label="Submit form">
        Submit
      </Button>
    );

    expect(
      screen.getByRole('button', { name: 'Submit form' })
    ).toBeInTheDocument();

    await checkA11y(container);
  });
});

// ✅ GOOD: Testing disabled state accessibility
describe('Stepper', () => {
  it('should have accessible disabled state', async () => {
    const { container } = render(
      <Stepper
        value={5}
        max={5}
        onIncrement={jest.fn()}
        onDecrement={jest.fn()}
      />
    );

    const incrementButton = screen.getByLabelText(/increase.*disabled/i);
    expect(incrementButton).toBeDisabled();

    await checkA11y(container);
  });
});

// ❌ BAD: Missing accessibility check
describe('Button', () => {
  it('should render button', () => {
    render(<Button>Submit</Button>);
    expect(screen.getByRole('button')).toBeInTheDocument();
    // Missing: await checkA11y(container);
  });
});
```

## WCAG 2.1 AA Rules Configuration

The web monorepo enforces these axe-core rules:

**Enabled Rules**:

- `label` - Form elements must have labels
- `button-name` - Buttons must have discernible text
- `link-name` - Links must have discernible text
- `image-alt` - Images must have alt text
- `input-button-name` - Input buttons must have discernible text
- `aria-*` - All ARIA attribute rules (required-attr, valid-attr-value, etc.)
- `html-has-lang` - HTML element must have lang attribute
- `frame-title` - Frames must have title attribute
- `meta-viewport` - Viewport meta tag must not disable zooming

**Disabled Rules**:

- `color-contrast` - Currently disabled (manual review required)

**Configuration location**: `app/libs/a11y-jest/a11y.ts:25-68`

**Why**: These rules ensure WCAG 2.1 Level AA compliance. Color contrast is disabled because automated testing has many false positives and requires manual verification.

## Translation Integration

Always use translated strings for user-facing labels:

```typescript
import { useT9n } from '@/libs/translation';

const MyComponent = () => {
  const { translateRaw } = useT9n('feature-name');

  return (
    <button
      onClick={handleClick}
      aria-label={translateRaw('feature-name.button.aria-label')}
    >
      {translateRaw('feature-name.button.text')}
    </button>
  );
};
```

**Why**: Accessibility labels must be translated for international users using screen readers in different languages.

## Common Anti-Patterns

### ❌ Missing aria-label on icon-only buttons

```typescript
// BAD
<button onClick={handleClose}>
  <CloseIcon />
</button>

// GOOD
<button onClick={handleClose} aria-label="Close dialog">
  <CloseIcon />
</button>
```

### ❌ Using div/span for interactive elements without proper ARIA

```typescript
// BAD
<div onClick={handleClick}>Click me</div>

// GOOD
<button onClick={handleClick}>Click me</button>

// ACCEPTABLE (if semantic HTML can't be used)
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={handleKeyDown}
  aria-label="Perform action"
>
  Click me
</div>
```

### ❌ Missing form labels

```typescript
// BAD
<input type="email" placeholder="Email" />

// GOOD
<label htmlFor="email-input">Email</label>
<input id="email-input" type="email" />
```

### ❌ Forgetting to test accessibility

```typescript
// BAD
it('should render component', () => {
  render(<MyComponent />);
  expect(screen.getByRole('button')).toBeInTheDocument();
  // Missing checkA11y!
});

// GOOD
it('should render component', async () => {
  const { container } = render(<MyComponent />);
  expect(screen.getByRole('button')).toBeInTheDocument();
  await checkA11y(container);
});
```

## GitHub Actions Integration

The web monorepo includes automated accessibility workflows:

- **PR Accessibility Score Check** (`.github/workflows/pr_accessibility_scores_check.yml`)

  - Blocks PRs if accessibility score drops below 50%
  - Posts PR comments with accessibility score breakdown
  - Controlled by feature toggle: `./toggles/block_ci_based_accessibility_weekly_score`
  - Uses Bun scripts: `.github/workflows/scripts/accessibility-weekly-scores/pr-check/`

- **Daily Accessibility Report by Squad** (`.github/workflows/cron_accessibilty_report_by_squad.yml`)
  - Runs Cypress accessibility tests daily at 23:00 UTC
  - Generates reports by squad
  - Excludes squads: `client-platform`, `pep-project`, `zest`

**Why**: Automated checks ensure accessibility standards are maintained and violations are caught before merging to production.

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [axe-core Rules](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
- [jest-axe Documentation](https://github.com/nickcolley/jest-axe)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

## Quick Reference

### Must-Have Checklist

- [ ] All interactive elements have descriptive labels
- [ ] Form inputs have associated `<label>` elements
- [ ] Images have alt text (or empty alt for decorative)
- [ ] Buttons have `aria-label` or visible text
- [ ] Custom widgets have proper ARIA roles
- [ ] Keyboard navigation works (Tab, Enter, Space, Escape)
- [ ] Tests include `await checkA11y(container)`
- [ ] ESLint rule `a11y-jest/enforce-a11y-check-in-tests` is enabled

### Common ARIA Attributes

- `aria-label` - Provides accessible name for elements
- `aria-labelledby` - References another element for label
- `aria-describedby` - References another element for description
- `aria-hidden` - Hides element from screen readers
- `aria-live` - Announces dynamic content changes
- `aria-expanded` - Indicates expanded/collapsed state
- `aria-pressed` - Indicates button pressed state
- `aria-disabled` - Indicates disabled state
- `role` - Defines element type for assistive technologies

### Keyboard Support

- `tabIndex={0}` - Makes element focusable
- `tabIndex={-1}` - Removes from tab order (programmatic focus only)
- Handle `Enter` and `Space` for button-like elements
- Handle `Escape` for closing dialogs/menus
- Handle arrow keys for navigation in lists/menus
