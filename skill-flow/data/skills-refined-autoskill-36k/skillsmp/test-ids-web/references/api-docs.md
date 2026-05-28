# Test IDs - API Reference

**Testing Library Version**: @testing-library/react v13.4.0

## Official Documentation

- **Testing Library**: https://testing-library.com/docs/queries/bytestid
- **HTML data attributes**: https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes
- **Jest DOM**: https://github.com/testing-library/jest-dom

## data-testid Attribute

The `data-testid` HTML5 data attribute for test identifiers.

### Syntax

```typescript
// Standard (React Testing Library convention)
<element data-testid="test-identifier">

// Alternative (with hyphen - also works)
<element data-test-id="test-identifier">

// ❌ Wrong - React Native only
<View testID="test-identifier">
```

### Usage

```typescript
import { Box } from '@/libs/zest';

// Static test ID
<Box data-testid="my-component">
  Content
</Box>

// Dynamic test ID with template literal
<Box data-testid={`option-${id}`}>
  Option {id}
</Box>

// Conditional test ID
<Box data-testid={`card-${isActive ? 'active' : 'inactive'}`}>
  Card
</Box>

// Hierarchical test ID with dots
<Button.Primary data-test-id="checkout-page.footer.submit-button">
  Submit
</Button.Primary>
```

## Naming Conventions

### Naming Patterns

```typescript
// Context + entity
data-testid="goalsPlanNumberOfPeople"

// Context + entity + variant
data-testid="goalsPlanNumberOfPeople-justMe"
data-testid="goalsPlanNumberOfPeople-twoOfUs"

// Module + element + action (dot notation)
data-test-id="upm-playground.btn.submit"
data-test-id="checkout-page.footer.error-message"

// Feature + component + part
data-test-id="challenge-card-cta"
data-test-id="challenge-card-title"
data-test-id="circular-progress-text"

// Indexed elements
data-test-id="step-circle-divider-0"
data-test-id="step-circle-divider-1"

// State-based
data-test-id="step-container-step-0"
data-test-id="step-container-step-1-completed"

// Semantic descriptive
data-test-id="radial-bg-circle"
data-test-id="radial-progress-circle"
data-test-id="progress-checkmark"
```

### Naming Rules

- **Case**: Use kebab-case (lowercase with hyphens)
- **Prefixes**: Include context (page, feature, module)
- **Suffixes**: Add variant, state, or index
- **Separators**: Use `-` for words, `.` for hierarchy
- **Length**: Balance between descriptive and concise
- **Uniqueness**: Must be unique within component scope

**Good names:**
- `goalsPlanNumberOfPeople-justMe`
- `upm-playground.btn.submit`
- `challenge-card-cta`
- `step-container-step-2-completed`

**Bad names:**
- `btn` (too generic)
- `test` (meaningless)
- `component1` (unclear)
- `MyComponent` (not kebab-case)

## Testing Library Queries

### getByTestId()

Find element by test ID (throws error if not found).

```typescript
screen.getByTestId(id: string): HTMLElement;
```

**Usage:**
```typescript
const element = screen.getByTestId('my-component');
expect(element).toBeInTheDocument();
```

**Throws:** Error if element not found or multiple elements found.

### queryByTestId()

Find element by test ID (returns null if not found).

```typescript
screen.queryByTestId(id: string): HTMLElement | null;
```

**Usage:**
```typescript
const element = screen.queryByTestId('missing-element');
expect(element).not.toBeInTheDocument();
```

**Returns:** `null` if not found (no error thrown).

### findByTestId()

Async find element by test ID (waits for element to appear).

```typescript
screen.findByTestId(
  id: string,
  options?: {
    exact?: boolean;
    normalizer?: (text: string) => string;
  },
  waitForOptions?: {
    timeout?: number;
    interval?: number;
  }
): Promise<HTMLElement>;
```

**Usage:**
```typescript
// Default timeout (1000ms)
const element = await screen.findByTestId('async-element');

// Custom timeout
const slowElement = await screen.findByTestId(
  'slow-element',
  {},
  { timeout: 5000 }
);
```

**Throws:** Error if element not found after timeout.

### getAllByTestId()

Find all elements by test ID (throws error if none found).

```typescript
screen.getAllByTestId(id: string): HTMLElement[];
```

**Usage:**
```typescript
const elements = screen.getAllByTestId('list-item');
expect(elements).toHaveLength(3);
```

**Throws:** Error if no elements found.

### queryAllByTestId()

Find all elements by test ID (returns empty array if none found).

```typescript
screen.queryAllByTestId(id: string): HTMLElement[];
```

**Usage:**
```typescript
const elements = screen.queryAllByTestId('missing-items');
expect(elements).toHaveLength(0);
```

**Returns:** Empty array `[]` if not found.

### findAllByTestId()

Async find all elements by test ID (waits for elements to appear).

```typescript
screen.findAllByTestId(
  id: string,
  options?: {},
  waitForOptions?: {
    timeout?: number;
    interval?: number;
  }
): Promise<HTMLElement[]>;
```

**Usage:**
```typescript
const elements = await screen.findAllByTestId('async-list-item');
expect(elements).toHaveLength(5);
```

**Throws:** Error if no elements found after timeout.

## Query Method Selection

| Method | No Match | Multiple Matches | Await | Best For |
|--------|----------|------------------|-------|----------|
| getByTestId | Error | Return first | No | Immediate presence |
| getAllByTestId | Error | Return array | No | Multiple elements |
| queryByTestId | null | Return first | No | Absence check |
| queryAllByTestId | [] | Return array | No | Absence check (multiple) |
| findByTestId | Error | Return first | Yes | Async rendering |
| findAllByTestId | Error | Return array | Yes | Async multiple |

**When to use:**
- `getByTestId`: Element must be present immediately
- `queryByTestId`: Check element is NOT present (`expect(...).not.toBeInTheDocument()`)
- `findByTestId`: Element appears asynchronously (data loading, animations)

## Jest DOM Matchers

Custom matchers for test ID assertions.

### toHaveAttribute()

Assert element has specific attribute.

```typescript
expect(element).toHaveAttribute(
  attribute: string,
  value?: string | RegExp
): void;
```

**Usage:**
```typescript
const button = screen.getByTestId('submit-button');

// Check attribute exists
expect(button).toHaveAttribute('data-testid');

// Check attribute value
expect(button).toHaveAttribute('data-testid', 'submit-button');

// Regex match
expect(button).toHaveAttribute('data-testid', /submit/);
```

### toBeInTheDocument()

Assert element exists in document.

```typescript
expect(element).toBeInTheDocument(): void;
```

**Usage:**
```typescript
const element = screen.getByTestId('my-component');
expect(element).toBeInTheDocument();

const missing = screen.queryByTestId('missing');
expect(missing).not.toBeInTheDocument();
```

### toBeVisible()

Assert element is visible (not hidden).

```typescript
expect(element).toBeVisible(): void;
```

**Usage:**
```typescript
const element = screen.getByTestId('modal');
expect(element).toBeVisible();
```

## Dynamic Test IDs

### Template Literals

```typescript
// Variable interpolation
<Box data-testid={`option-${id}`}>

// Multiple variables
<Box data-testid={`card-${category}-${id}`}>

// With index
{items.map((item, index) => (
  <Box key={item.id} data-testid={`item-${index}`}>
    {item.name}
  </Box>
))}
```

### Conditional Test IDs

```typescript
// Ternary operator
<Box data-testid={`card-${isActive ? 'active' : 'inactive'}`}>

// With suffix
<Box data-testid={`step-${index}${isCompleted ? '-completed' : ''}`}>

// Boolean flag
<Box data-testid={`button-${disabled ? 'disabled' : 'enabled'}`}>
```

## Testing Patterns

### Query by Role + Verify Test ID

Combine accessible queries with test ID verification.

```typescript
// Find by semantic role
const buttons = await screen.findAllByRole('button');

// Verify specific test IDs
expect(buttons[0]).toHaveAttribute('data-testid', 'primary-action');
expect(buttons[1]).toHaveAttribute('data-testid', 'cancel-action');
```

### Direct Query by Test ID

When role is unclear or multiple roles exist.

```typescript
const element = screen.getByTestId('complex-custom-component');
expect(element).toBeInTheDocument();
```

### Query Dynamic Test IDs

```typescript
// Query with string interpolation
const item = screen.getByTestId(`list-item-${id}`);

// Query indexed elements
const divider0 = screen.getByTestId('step-circle-divider-0');
const divider1 = screen.getByTestId('step-circle-divider-1');

// Query with state
const completedStep = screen.getByTestId('step-container-step-1-completed');
```

### Query with Regex

```typescript
// Partial match with regex
const elements = screen.getAllByTestId(/^step-container/);

// Case-insensitive match
const button = screen.getByTestId(/submit/i);
```

## User Interactions

### Click Events

```typescript
import userEvent from '@testing-library/user-event';
import { act } from '@testing-library/react';

const button = screen.getByTestId('submit-button');

await act(async () => {
  userEvent.click(button);
});

// Or with userEvent directly (automatically wraps in act)
await userEvent.click(button);
```

### Type Events

```typescript
const input = screen.getByTestId('email-input');

await userEvent.type(input, 'test@example.com');

expect(input).toHaveValue('test@example.com');
```

### Form Interactions

```typescript
// Fill form
const emailInput = screen.getByTestId('email-input');
const passwordInput = screen.getByTestId('password-input');
const submitButton = screen.getByTestId('submit-button');

await userEvent.type(emailInput, 'user@example.com');
await userEvent.type(passwordInput, 'password123');
await userEvent.click(submitButton);
```

## Async Testing

### Wait for Element to Appear

```typescript
// findByTestId automatically waits
const element = await screen.findByTestId('async-content');
expect(element).toBeInTheDocument();
```

### Wait for Element to Disappear

```typescript
import { waitFor } from '@testing-library/react';

// Wait for element to be removed
await waitFor(() => {
  expect(screen.queryByTestId('loading')).not.toBeInTheDocument();
});
```

### Custom Timeout

```typescript
// 5 second timeout
const element = await screen.findByTestId(
  'slow-element',
  {},
  { timeout: 5000 }
);
```

## Integration with Providers

### Render Helper Pattern

```typescript
import { QueryClient, QueryClientProvider } from 'react-query';

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={new QueryClient()}>
      <SystemCountryProvider systemCountry={SystemCountry.US}>
        {component}
      </SystemCountryProvider>
    </QueryClientProvider>
  );
};

it('renders with providers', () => {
  renderWithProviders(<MyComponent />);

  const element = screen.getByTestId('my-component');
  expect(element).toBeInTheDocument();
});
```

## Best Practices

1. **Prefer accessible queries:**
   - Use `getByRole()`, `getByLabelText()` first
   - Use `getByTestId()` as last resort

2. **Use descriptive names:**
   - Include context: `goalsPlanNumberOfPeople-justMe`
   - Not generic: `btn`, `test`, `component1`

3. **Use consistent conventions:**
   - Prefer `data-testid` over `data-test-id`
   - Use kebab-case consistently
   - Follow naming patterns

4. **Query efficiently:**
   - Use `getByTestId` for immediate elements
   - Use `findByTestId` for async elements
   - Use `queryByTestId` for absence checks

5. **Combine with roles:**
   - Query by role first
   - Verify test ID second
   - Better accessibility testing

## Common Pitfalls

1. **Using testID (React Native):**
   ```typescript
   // ❌ Wrong
   <View testID="component">

   // ✅ Correct
   <Box data-testid="component">
   ```

2. **Not using dynamic IDs:**
   ```typescript
   // ❌ Bad - hardcoded
   <Box data-testid="option-1">

   // ✅ Good - dynamic
   <Box data-testid={`option-${id}`}>
   ```

3. **Inconsistent naming:**
   ```typescript
   // ❌ Inconsistent
   <Box data-testid="MyComponent">
   <Box data-test-id="my_component">

   // ✅ Consistent
   <Box data-testid="my-component">
   <Box data-testid="my-other-component">
   ```
