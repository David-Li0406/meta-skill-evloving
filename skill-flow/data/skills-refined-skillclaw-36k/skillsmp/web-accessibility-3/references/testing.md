# Testing Patterns

Automated accessibility testing with axe-core and jest-axe in the YourCompany web monorepo.

## Core Testing Library

**Location**: `app/libs/a11y-jest/`

The web monorepo provides two main testing functions:

### `checkA11y()` - Strict Testing

Use in tests that should **fail** if accessibility violations are found:

```typescript
import { checkA11y } from '@/libs/a11y-jest';

describe('MyComponent', () => {
  it('should render with no accessibility violations', async () => {
    const { container } = render(<MyComponent />);

    expect(screen.getByRole('button')).toBeInTheDocument();

    // This will FAIL the test if violations are found
    await checkA11y(container);
  });
});
```

### `checkA11yOutput()` - Reporting Only

Use for **reporting violations** without failing the test (used in CI/CD):

```typescript
import { checkA11yOutput } from '@/libs/a11y-jest';

describe('MyComponent', () => {
  it('should generate accessibility report', async () => {
    const { container } = render(<MyComponent />);

    // This generates a JSON report but doesn't fail the test
    await checkA11yOutput(container, expect.getState().currentTestName);
  });
});
```

**Key Differences**:

- `checkA11y()`: Uses `expect(results).toHaveNoViolations()` - **fails test**
- `checkA11yOutput()`: Only runs when `RUN_A11Y_CHECKS=1` env var is set - **reports only**

## Real Production Test Example

**Location**: `app/spaces/store/integration/shared/age-verification/index.test.tsx`

```typescript
import React from 'react';
import userEvent from '@testing-library/user-event';
import {
  render,
  waitFor,
  within,
  act,
  screen,
} from '@/spaces/store/integration/shared/utils';
import { checkA11yOutput } from '@/libs/a11y-jest';
import ItemsGrid from '@/food/shared/components/items-grid';
import { SaveButton } from '@/food/shared/components/save-button';

describe('Age Verification prompt', () => {
  const alcoholicItemId = '658c8904529576b8aa46b29d';

  it('should prompt the users when trying to add an alcoholic item', async () => {
    // Render component
    const { container } = render(
      <>
        <SaveButton onSaveSuccess={() => {}} />
        <ItemsGrid ids={[{ mainItemId: alcoholicItemId }]} />
      </>,
      {
        wrapperProps: {
          config: {
            ageVerificationOnAddEnabled: true,
          },
        },
      }
    );

    // Find add button by accessible label
    const addButton = await screen.findByLabelText(
      'Add BBQ Pulled Pork Nachos'
    );
    expect(addButton).toBeInTheDocument();

    // Wait for button to be ready
    await waitFor(() => expect(addButton).toBeInTheDocument());

    // Click the add button
    await act(async () => {
      userEvent.click(addButton);
    });

    // Verify prompt is shown
    await waitFor(() =>
      expect(screen.getByText('Are you above 18?')).toBeInTheDocument()
    );

    // Confirm age
    await act(async () => userEvent.click(screen.getByText('Yes I am 18+')));

    // Verify prompt is closed
    await waitFor(() =>
      expect(screen.queryByText('Are you above 18?')).not.toBeInTheDocument()
    );

    // Check accessibility AFTER all interactions
    await checkA11yOutput(container, expect.getState().currentTestName);
  });

  it('should prompt when subscribing to alcoholic item', async () => {
    const { getByText, getByRole, container } = render(
      <>
        <SaveButton onSaveSuccess={() => {}} />
        <ItemsGrid ids={[{ mainItemId: SUBSCRIBABLE_ALCOHOLIC_ADDON }]} />
      </>,
      {
        wrapperProps: {
          config: {
            ageVerificationOnAddEnabled: true,
          },
        },
      }
    );

    // Wait for component to render
    await waitFor(() =>
      expect(getByText(/Valentine's Charcuterie/i)).toBeInTheDocument()
    );

    // Find checkbox by role
    const checkbox = await waitFor(() => getByRole('checkbox'));
    await waitFor(() => expect(checkbox).toBeInTheDocument());

    // Click checkbox
    await act(async () => {
      userEvent.click(checkbox);
    });

    // Verify prompt
    await waitFor(() =>
      expect(screen.getByText('Are you above 18?')).toBeInTheDocument()
    );

    // Confirm
    await act(async () => userEvent.click(screen.getByText('Yes I am 18+')));

    // Verify subscription dialog
    await waitFor(() => expect(screen.getByRole('dialog')).toBeInTheDocument());
    await waitFor(() =>
      expect(
        within(screen.getByRole('dialog')).getByText('Subscribe to this item')
      ).toBeInTheDocument()
    );

    // Check accessibility
    await checkA11yOutput(container, expect.getState().currentTestName);
  });
});
```

**Key Patterns**:

- ✅ Use `findByLabelText()` to find elements by accessible labels
- ✅ Use `getByRole()` to find elements by semantic roles
- ✅ Test interactions completely before checking accessibility
- ✅ Pass test name to `checkA11yOutput()` for tracking
- ✅ Use `waitFor()` for async operations
- ✅ Check accessibility at the end of each test

## Testing with Options

### Enable Landmarks

```typescript
it('should have proper landmark regions', async () => {
  const { container } = render(<PageLayout />);

  // Enable landmark checking
  await checkA11y(container, {
    enableLandmarks: true,
  });
});
```

### Enable Real Timers

For components using `setTimeout` or animations:

```typescript
it('should handle delayed content', async () => {
  const { container } = render(<AnimatedComponent />);

  await waitFor(() => {
    expect(screen.getByText('Animated content')).toBeInTheDocument();
  });

  // Use real timers for axe-core
  await checkA11y(container, {
    enableTimeout: true,
  });
});
```

## ESLint Enforcement

**Location**: `scripts/eslint/plugins/a11y/README.md`

The web monorepo has a custom ESLint rule that enforces accessibility testing.

### Setup in Your Module

Create or update `.eslintrc.json` in your module:

```json
{
  "extends": ["../../../../.eslintrc.js"],
  "plugins": ["a11y-jest"],
  "rules": {
    "a11y-jest/enforce-a11y-check-in-tests": "warn"
  }
}
```

### What the Rule Checks

The rule validates that:

- ✅ All React component tests (`.test.tsx`, `.spec.tsx`) include `checkA11y()` calls
- ✅ Skips hook tests (files starting with 'use', containing 'Hook' or using 'renderHook')
- ✅ Skips Cypress tests (files using `cy.` commands)
- ✅ Ignores tests marked with `it.skip` or `test.skip`
- ✅ When `it.only` or `test.only` exist, only those tests are checked

### Correct Usage Examples

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

// ✅ GOOD: Multiple tests with accessibility checks
describe('Form', () => {
  it('should render form fields', async () => {
    const { container } = render(<Form />);
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    await checkA11y(container);
  });

  it('should show validation errors', async () => {
    const { container } = render(<Form />);
    userEvent.click(screen.getByRole('button', { name: 'Submit' }));
    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
    });
    await checkA11y(container);
  });
});

// ✅ GOOD: Testing with .only - accessibility check included
describe('Component', () => {
  it.only('should render correctly', async () => {
    const { container } = render(<Component />);
    await checkA11y(container);
  });
});
```

### Incorrect Usage Examples

```typescript
// ❌ BAD: Missing accessibility check
describe('Button', () => {
  it('should render button', () => {
    render(<Button>Submit</Button>);
    expect(screen.getByRole('button')).toBeInTheDocument();
    // Missing: await checkA11y(container);
  });
});

// ❌ BAD: Forgot to await
describe('Button', () => {
  it('should render button', async () => {
    const { container } = render(<Button>Submit</Button>);
    checkA11y(container); // Missing 'await'
  });
});

// ❌ BAD: Using .only without accessibility check
describe('Component', () => {
  it.only('should render correctly', () => {
    render(<Component />);
    // Missing checkA11y
  });
});
```

## Running Accessibility Tests

### Local Development

Run tests normally:

```bash
yarn test MyComponent.test.tsx
```

### Generate Accessibility Reports

Run with environment variable to generate JSON reports:

```bash
RUN_A11Y_CHECKS=1 yarn test
```

This generates: `app/libs/a11y-jest/report/a11y-check-results-YYYY-MM-DD.json`

### CI/CD Pipeline

The GitHub Actions workflow automatically runs accessibility checks:

**Workflow**: `.github/workflows/pr_accessibility_scores_check.yml`

```yaml
- name: Check if PR is blocked (based on Author and Accessibility Weekly Score)
  env:
    FILE_PATH: .accessibility-weekly-score.json
  run: |
    bun ./.github/workflows/scripts/accessibility-weekly-scores/pr-check/is_pr_blocked.mjs

- name: Post PR comment with the accessibility weekly score
  run: |
    bun ./.github/workflows/scripts/accessibility-weekly-scores/pr-check/pr_blocked_comment.mjs
  env:
    THRESHOLD: 50
    SLACK_CHANNEL: '#web-ci, #squad-consumer-acceleration'
```

**What it does**:

- Runs accessibility checks on PRs
- Blocks PRs if accessibility score drops below 50
- Posts PR comments with violation breakdown
- Tracks scores in Google Sheets

## Test Coverage Best Practices

### Test All Interactive States

```typescript
describe('Button states', () => {
  it('should be accessible when enabled', async () => {
    const { container } = render(<Button onClick={jest.fn()}>Click</Button>);
    await checkA11y(container);
  });

  it('should be accessible when disabled', async () => {
    const { container } = render(
      <Button onClick={jest.fn()} disabled>
        Click
      </Button>
    );
    await checkA11y(container);
  });

  it('should be accessible in loading state', async () => {
    const { container } = render(
      <Button onClick={jest.fn()} isLoading>
        Click
      </Button>
    );
    await checkA11y(container);
  });
});
```

### Test Form Validation

```typescript
describe('Form validation', () => {
  it('should be accessible with no errors', async () => {
    const { container } = render(<Form />);
    await checkA11y(container);
  });

  it('should be accessible with validation errors', async () => {
    const { container } = render(<Form />);

    // Trigger validation
    userEvent.click(screen.getByRole('button', { name: 'Submit' }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
    });

    await checkA11y(container);
  });
});
```

### Test Modal/Dialog States

```typescript
describe('Modal', () => {
  it('should be accessible when closed', async () => {
    const { container } = render(<Modal isOpen={false} />);
    await checkA11y(container);
  });

  it('should be accessible when open', async () => {
    const { container } = render(<Modal isOpen={true} />);

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    await checkA11y(container);
  });
});
```

## Debugging Test Failures

When `checkA11y()` fails, you'll see detailed violation information:

```
Expected the HTML found at $('.selector') to have no violations:

<button>Click</button>

Received:

"Buttons must have discernible text" (button-name)
  Ensures buttons have discernible text
  Help: https://dequeuniversity.com/rules/axe/4.4/button-name
  Elements:
    - button
```

**Common fixes**:

1. Add `aria-label` to the button
2. Add visible text content
3. Ensure icon-only buttons have proper labels
4. Check that disabled states are properly communicated

## Configuration Location

**File**: `app/libs/a11y-jest/a11y.ts`

```typescript
export const a11yConfig: RunOptions = {
  rules: {
    'color-contrast': { enabled: false }, // Disabled (too many false positives)
    label: { enabled: true },
    'button-name': { enabled: true },
    'link-name': { enabled: true },
    'image-alt': { enabled: true },
    'aria-required-attr': { enabled: true },
    'aria-valid-attr-value': { enabled: true },
    // ... more rules
  },
  runOnly: {
    type: 'tag',
    values: ['wcag2a', 'wcag2aa'], // WCAG 2.1 Level AA
  },
};
```

This configuration is used by both `checkA11y()` and `checkA11yOutput()`.
