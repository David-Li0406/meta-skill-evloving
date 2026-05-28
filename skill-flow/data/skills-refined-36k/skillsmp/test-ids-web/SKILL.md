---
name: test-ids-web
description: "WHAT: Test ID patterns with data-testid attribute for web testing. WHEN: E2E with Playwright/Cypress, component tests with Testing Library, targeting specific elements. KEYWORDS: data-testid, test ID, getByTestId, kebab-case, dynamic ID, testing-library, web, Playwright."
---

# Test IDs - Web

Test identifier patterns for web applications using `data-testid` attribute and @testing-library/react.

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns

## When to Use

Use test IDs for:
- E2E testing with tools like Playwright, Cypress
- Component testing with @testing-library/react
- Targeting specific elements in tests
- Stable selectors that don't break with UI changes

**Don't use test IDs for:**
- Production analytics (use dedicated tracking attributes)
- Styling or behavior hooks (use CSS classes or data attributes)

## Core Principles

### 1. data-testid Attribute

**Use data-testid (or data-test-id) attribute for test identifiers.**

✅ **Good:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.tsx:119
<Box
  as="button"
  role="checkbox"
  data-testid={`goalsPlanNumberOfPeople-${numberOfPeopleOption}`}
  onClick={() => setSelectedNumberOfPeople(numberOfPeopleOption)}
>
  {/* Content */}
</Box>
```

**Container with base ID:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.tsx:102
<Box
  data-test-id={`goalsPlanNumberOfPeople`}
  role="group"
  as="section"
>
  {/* Child elements */}
</Box>
```

❌ **Bad - Don't use testID (React Native syntax):**
```typescript
// This is React Native - don't use in web!
<View testID="my-component">
```

**Why:** `data-testid` is the HTML5 data attribute standard. React Testing Library uses this by default with `getByTestId()`.

**Note:** Both `data-testid` and `data-test-id` are used in the codebase, but `data-testid` (no hyphen) is the React Testing Library convention.

### 2. Naming Conventions

**Use kebab-case with descriptive, context-aware names.**

✅ **Good:**
```typescript
// Contextual naming
<Box data-testid="goalsPlanNumberOfPeople-justMe">

// Hierarchical with dots
<Button data-test-id="upm-playground.btn.submit">

// Semantic descriptive names
<circle data-test-id="radial-bg-circle">
<circle data-test-id="radial-progress-circle">

// Component-specific with state
<Box data-test-id="challenge-wrapper-card">
<Box data-test-id="card-content">
<Box data-test-id="title-container">
```

**Naming patterns:**
```typescript
// Context + entity
data-testid="goalsPlanNumberOfPeople"

// Context + entity + variant
data-testid="goalsPlanNumberOfPeople-justMe"
data-testid="goalsPlanNumberOfPeople-twoOfUs"

// Module + element + action
data-test-id="upm-playground.btn.submit"

// Feature + component + part
data-test-id="challenge-card-cta"
data-test-id="challenge-title"
data-test-id="circular-progress-text"

// Descriptive semantic names
data-test-id="progress-checkmark"
data-test-id="feedback-modal-heading"
data-test-id="radial-bg-circle"
```

**Why:** Descriptive names make tests readable and maintainable. Context prevents ID collisions.

### 3. Dynamic Test IDs

**Use template literals for dynamic test IDs with variables.**

✅ **Good:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.tsx:119
{numberOfPeopleOptions.map((numberOfPeopleOption, index) => (
  <Box
    key={index}
    data-testid={`goalsPlanNumberOfPeople-${numberOfPeopleOption}`}
  >
    {/* Content */}
  </Box>
))}
```

**Indexed test IDs:**
```typescript
// app/features/freebie-in-helloshare-challenge-card-feature/components/CircularProgressIndicator/index.tsx:54
{stepsArray.map((_, index) => (
  <StepCircleDivider
    key={index}
    data-test-id={`step-circle-divider-${index}`}
  />
))}
```

**Conditional suffix:**
```typescript
// app/features/freebie-in-helloshare-challenge-card-feature/components/FIHCardTasks.tsx:46
<Box
  data-test-id={`step-container-step-${stepIndex}${
    isCompleted ? '-completed' : ''
  }`}
>
```

**Why:** Dynamic IDs allow testing of generated lists and conditional states.

### 4. Testing with @testing-library/react

**Query elements by test ID and assert with toHaveAttribute.**

✅ **Good:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:68
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

it('renders options with correct test ids', async () => {
  renderComponent();

  let options = await screen.findAllByRole('checkbox');
  expect(options.length).toBe(3);

  expect(options[0]).toHaveAttribute(
    'data-testid',
    'goalsPlanNumberOfPeople-justMe'
  );
  expect(options[1]).toHaveAttribute(
    'data-testid',
    'goalsPlanNumberOfPeople-twoOfUs'
  );
  expect(options[2]).toHaveAttribute(
    'data-testid',
    'goalsPlanNumberOfPeople-groupFamily'
  );

  await act(async () => {
    userEvent.click(options[2]);
  });

  options = await screen.findAllByRole('checkbox');
  expect(options[2]).toHaveAttribute('aria-checked', 'true');
});
```

**Why:** Combining role queries with test ID assertions provides accessible, stable tests.

### 5. Integration Test Pattern

**Wrap components in providers for integration tests.**

✅ **Good:**
```typescript
// app/data-access/CONTRIBUTING.md:274
import { render } from '@testing-library/react';
import IntegrationTestProvider from '../test-utils/IntegrationTestProvider';

const TestComponent: React.FC = () => {
  const { data } = useCustomerInfo({});

  return <div data-test-id="email">{data?.email}</div>;
};

render(
  <IntegrationTestProvider>
    <TestComponent />
  </IntegrationTestProvider>
);
```

**With multiple providers:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:26
const renderComponent = () =>
  render(
    <QueryClientProvider client={new QueryClient()}>
      <ServerEnvProvider>
        <SystemCountryProvider systemCountry={SystemCountry.FJ}>
          <LocalStorageProvider>
            <SingleQuestionPageProvider>
              <QuestionnaireConfigProvider>
                <NumberOfPeopleProvider>
                  <NumberOfPeopleStep
                    onGoalsPlanRecommendationSelectionChange={onSelectionChange}
                  />
                </NumberOfPeopleProvider>
              </QuestionnaireConfigProvider>
            </SingleQuestionPageProvider>
          </LocalStorageProvider>
        </SystemCountryProvider>
      </ServerEnvProvider>
    </QueryClientProvider>
  );
```

**Why:** Providers supply necessary context (React Query, state, config) for components to function in tests.

## Advanced Patterns

### Hierarchical Test IDs

```typescript
// Dot notation for hierarchy
<Box data-test-id="checkout-page.footer.submit-button">
<Box data-test-id="checkout-page.footer.error-message">

// Nested context
<Box data-test-id="challenge-card">
  <Box data-test-id="challenge-card-header">
    <Text data-test-id="challenge-card-title">
  </Box>
  <Box data-test-id="challenge-card-content">
</Box>
```

### State-Based Test IDs

```typescript
// Conditional state in ID
<Box
  data-testid={`card-${isActive ? 'active' : 'inactive'}`}
>

// Status suffix
<Box data-testid={`step-${index}-${status}`}>
```

### SVG and Icon Test IDs

```typescript
// app/features/freebie-in-helloshare-challenge-card-feature/components/CircularProgressIndicator/index.tsx:38
<Svg viewBox={`0 0 ${externalRadius * 2} ${externalRadius * 2}`}>
  <Background
    data-test-id="radial-bg-circle"
  />
  <Progress
    data-test-id="radial-progress-circle"
  />
</Svg>

// Icon elements
<CheckmarkOutline16 data-test-id="progress-checkmark" />
<BoxClosedOutline24 data-test-id="progress-box" />
```

### Form Element Test IDs

```typescript
// Input fields
<input data-testid="email-input" type="email" />
<input data-testid="password-input" type="password" />

// Buttons with action context
<button data-test-id="submit-button">
<button data-test-id="cancel-button">

// Form containers
<form data-testid="login-form">
```

## Testing Patterns

### Query by Role + Assert Test ID

```typescript
// Find by semantic role, verify by test ID
const buttons = await screen.findAllByRole('button');
expect(buttons[0]).toHaveAttribute('data-testid', 'primary-action');
```

### Direct Query by Test ID

```typescript
// When role is not clear or multiple roles exist
const element = screen.getByTestId('custom-complex-component');
expect(element).toBeInTheDocument();
```

### User Interactions

```typescript
import userEvent from '@testing-library/user-event';

// Click interaction
const button = screen.getByTestId('submit-button');
await act(async () => {
  userEvent.click(button);
});

// Type interaction
const input = screen.getByTestId('email-input');
await userEvent.type(input, 'test@example.com');
```

### Async Queries

```typescript
// Wait for element to appear
const element = await screen.findByTestId('async-content');

// With custom timeout
const slowElement = await screen.findByTestId('slow-content', {}, {
  timeout: 5000,
});
```

## File Organization

```
components/
└── MyComponent/
    ├── MyComponent.tsx       # Component with test IDs
    ├── MyComponent.spec.tsx  # Unit tests
    ├── MyComponent.test.tsx  # Integration tests
    └── index.ts              # Exports
```

## Common Mistakes

1. **Using testID instead of data-testid** - testID is React Native syntax
2. **Hardcoding test IDs without context** - Use descriptive, prefixed names
3. **Not using template literals** - Dynamic IDs need interpolation
4. **Inconsistent naming** - Stick to kebab-case convention
5. **Over-specific IDs** - Balance between specific and maintainable
6. **Missing test IDs in key interaction points** - Add IDs to all testable elements
7. **Using data-test-id and data-testid inconsistently** - Prefer `data-testid` for React Testing Library

## Quick Reference

### Basic Test ID

```typescript
import { Box } from '@/libs/zest';

<Box data-testid="my-component">
  {/* Content */}
</Box>
```

### Dynamic Test ID

```typescript
<Box data-testid={`option-${index}`}>
  {/* Content */}
</Box>

<Box data-testid={`card-${id}-${status}`}>
  {/* Content */}
</Box>
```

### Testing Pattern

```typescript
import { render, screen } from '@testing-library/react';

it('renders component', () => {
  render(<MyComponent />);

  const element = screen.getByTestId('my-component');
  expect(element).toBeInTheDocument();
  expect(element).toHaveAttribute('data-testid', 'my-component');
});
```

### With User Interaction

```typescript
import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

it('handles click', async () => {
  render(<MyComponent />);

  const button = screen.getByTestId('submit-button');

  await act(async () => {
    userEvent.click(button);
  });

  expect(mockHandler).toHaveBeenCalled();
});
```

### Multiple Providers

```typescript
const renderWithProviders = (component) =>
  render(
    <QueryClientProvider client={queryClient}>
      <SystemCountryProvider systemCountry={SystemCountry.US}>
        {component}
      </SystemCountryProvider>
    </QueryClientProvider>
  );

it('renders with context', () => {
  renderWithProviders(<MyComponent />);
  expect(screen.getByTestId('my-component')).toBeInTheDocument();
});
```

## Naming Guidelines

### Good Names

- `goalsPlanNumberOfPeople-justMe` - Context + entity + variant
- `upm-playground.btn.submit` - Module + element + action
- `challenge-card-cta` - Feature + component + part
- `radial-progress-circle` - Descriptive semantic name
- `step-container-step-2-completed` - State + index + status

### Bad Names

- `btn` - Too generic
- `test` - Not descriptive
- `component1` - Meaningless
- `the-button` - Unclear purpose
- `MyComponent` - Not kebab-case

## React Testing Library Standard

**Preferred**: `data-testid` (no hyphen between test and id)

```typescript
// ✅ Preferred - React Testing Library standard
<Box data-testid="my-component">

// ⚠️ Also works but less conventional
<Box data-test-id="my-component">

// ❌ Wrong - React Native only
<View testID="my-component">
```

**Why**: React Testing Library's `getByTestId()` looks for `data-testid` by default. Using the standard convention ensures consistency across the codebase.
