# Test IDs - Implementation Patterns

Implementation patterns and anti-patterns for test IDs in web applications.

## Pattern: Use data-testid (Web Standard)

Use the web standard data-testid attribute.

✅ **Good:**
```typescript
import { Box } from '@/libs/zest';

<Box data-testid="my-component">
  Content
</Box>

// Query in test
const element = screen.getByTestId('my-component');
expect(element).toBeInTheDocument();
```

❌ **Bad:**
```typescript
// Don't use testID (React Native syntax)
<View testID="my-component">
  Content
</View>

// Don't use className for test selection
<div className="my-component-test">
const element = container.querySelector('.my-component-test');
```

**Why:** `data-testid` is:
- HTML5 data attribute standard
- React Testing Library convention
- Separate from styling
- Won't break when CSS changes

## Pattern: Contextual Naming

Include context in test ID names.

✅ **Good:**
```typescript
// Context + entity
<Box data-testid="goalsPlanNumberOfPeople">

// Context + entity + variant
<Box data-testid="goalsPlanNumberOfPeople-justMe">
<Box data-testid="goalsPlanNumberOfPeople-twoOfUs">

// Feature + component + part
<Box data-testid="challenge-card-title">
<Box data-testid="challenge-card-cta">
```

❌ **Bad:**
```typescript
// Too generic
<Box data-testid="component">
<Box data-testid="button">
<Box data-testid="title">

// No context
<Box data-testid="option1">
<Box data-testid="option2">
```

**Why:** Contextual names:
- Prevent ID collisions
- More readable tests
- Self-documenting
- Easier to maintain

## Pattern: Kebab-Case Convention

Use kebab-case (lowercase with hyphens).

✅ **Good:**
```typescript
<Box data-testid="my-component">
<Box data-testid="submit-button">
<Box data-testid="email-input">
<Box data-testid="goals-plan-number-of-people">
```

❌ **Bad:**
```typescript
// PascalCase
<Box data-testid="MyComponent">

// camelCase
<Box data-testid="submitButton">

// snake_case
<Box data-testid="email_input">

// SCREAMING_CASE
<Box data-testid="SUBMIT_BUTTON">
```

**Why:** kebab-case:
- HTML attribute convention
- More readable in HTML
- Consistent with CSS classes
- Standard in web development

## Pattern: Dynamic Test IDs with Template Literals

Use template literals for dynamic test IDs.

✅ **Good:**
```typescript
// Variable interpolation
{options.map((option, index) => (
  <Box
    key={index}
    data-testid={`option-${option.value}`}
  >
    {option.label}
  </Box>
))}

// Index-based
{items.map((item, index) => (
  <Box
    key={item.id}
    data-testid={`list-item-${index}`}
  >
    {item.name}
  </Box>
))}

// Multiple variables
<Box data-testid={`card-${category}-${id}`}>
```

❌ **Bad:**
```typescript
// Hardcoded IDs in loop
{options.map((option) => (
  <Box data-testid="option">  // Same ID for all!
    {option.label}
  </Box>
))}

// String concatenation instead of template literal
<Box data-testid={'option-' + option.value}>
```

**Why:** Template literals:
- Create unique IDs for list items
- Enable individual targeting
- More maintainable
- Type-safe with TypeScript

## Pattern: Hierarchical Test IDs

Use dots for hierarchical relationships.

✅ **Good:**
```typescript
// Module + element + action
<Button.Primary data-test-id="upm-playground.btn.submit">

// Page + section + element
<Box data-test-id="checkout-page.footer.submit-button">
<Box data-test-id="checkout-page.footer.error-message">

// Feature + component + part
<Box data-test-id="challenge-card.header.title">
<Box data-test-id="challenge-card.content.description">
```

❌ **Bad:**
```typescript
// Flat naming without hierarchy
<Button data-testid="submit-button">
<Box data-testid="error-message">

// Unclear relationship
<Box data-testid="checkout-submit">
<Box data-testid="checkout-error">
```

**Why:** Hierarchical naming:
- Shows component structure
- Prevents naming conflicts
- Groups related elements
- More maintainable

## Pattern: State-Based Test IDs

Include state in test IDs when relevant.

✅ **Good:**
```typescript
// Conditional suffix
<Box
  data-testid={`step-${index}${isCompleted ? '-completed' : ''}`}
>

// State in ID
<Box data-testid={`card-${isActive ? 'active' : 'inactive'}`}>

// Status suffix
<Box data-testid={`task-${status}`}>
// Generates: task-pending, task-completed, task-failed
```

❌ **Bad:**
```typescript
// Same ID regardless of state
<Box data-testid="step">
<Box data-testid="card">

// State not reflected in test ID
<Box data-testid="task" className={status}>
```

**Why:** State-based IDs:
- Enable state-specific testing
- Self-documenting state
- Easier to query specific states
- Better test clarity

## Pattern: Query by Role First, Verify Test ID Second

Combine accessible queries with test ID verification.

✅ **Good:**
```typescript
it('verifies options have correct test ids', async () => {
  render(<Component />);

  // Query by accessible role
  const options = await screen.findAllByRole('checkbox');

  // Verify test IDs
  expect(options[0]).toHaveAttribute('data-testid', 'option-1');
  expect(options[1]).toHaveAttribute('data-testid', 'option-2');
  expect(options[2]).toHaveAttribute('data-testid', 'option-3');
});
```

❌ **Bad:**
```typescript
it('queries only by test id', () => {
  render(<Component />);

  // Skips accessible queries
  const option1 = screen.getByTestId('option-1');
  const option2 = screen.getByTestId('option-2');
  const option3 = screen.getByTestId('option-3');
});
```

**Why:** Role-first approach:
- Tests accessibility
- Ensures proper ARIA attributes
- Test IDs as secondary verification
- Better user experience testing

## Pattern: Use findByTestId for Async Elements

Use findBy queries for elements that appear asynchronously.

✅ **Good:**
```typescript
it('waits for async element', async () => {
  render(<AsyncComponent />);

  // findByTestId automatically waits
  const element = await screen.findByTestId('async-content');
  expect(element).toBeInTheDocument();
});
```

❌ **Bad:**
```typescript
it('fails with getByTestId', () => {
  render(<AsyncComponent />);

  // getByTestId doesn't wait - will throw error
  const element = screen.getByTestId('async-content');
  expect(element).toBeInTheDocument();
});
```

**Why:** `findByTestId`:
- Waits for element to appear
- Handles async rendering
- No manual waiting needed
- More reliable tests

## Pattern: Use queryByTestId for Absence Checks

Use queryBy to check element is not present.

✅ **Good:**
```typescript
it('element is not present', () => {
  render(<Component />);

  // queryByTestId returns null if not found
  const element = screen.queryByTestId('hidden-element');
  expect(element).not.toBeInTheDocument();
});
```

❌ **Bad:**
```typescript
it('checks absence with getBy', () => {
  render(<Component />);

  // getByTestId throws error if not found
  expect(() => screen.getByTestId('hidden-element')).toThrow();
});
```

**Why:** `queryByTestId`:
- Returns null (no error)
- Better for absence checks
- More readable intent
- Cleaner assertions

## Pattern: Consistent Naming Across Components

Use consistent naming patterns across similar components.

✅ **Good:**
```typescript
// Consistent pattern: component-action
<Button.Primary data-testid="login-submit">Submit</Button.Primary>
<Button.Primary data-testid="signup-submit">Sign Up</Button.Primary>
<Button.Primary data-testid="checkout-submit">Complete Order</Button.Primary>

// Consistent pattern: component-field
<input data-testid="login-email" type="email" />
<input data-testid="login-password" type="password" />
<input data-testid="signup-email" type="email" />
<input data-testid="signup-password" type="password" />
```

❌ **Bad:**
```typescript
// Inconsistent naming
<Button.Primary data-testid="submit-login">Submit</Button.Primary>
<Button.Primary data-testid="signupBtn">Sign Up</Button.Primary>
<Button.Primary data-testid="complete-order-button">Complete Order</Button.Primary>

// No pattern
<input data-testid="email-login" type="email" />
<input data-testid="passwordField" type="password" />
<input data-testid="SignupEmail" type="email" />
```

**Why:** Consistent naming:
- Easier to remember
- More maintainable
- Self-documenting
- Reduces cognitive load

## Pattern: Parent-Child Test ID Relationships

Use related IDs for parent-child elements.

✅ **Good:**
```typescript
<Box data-testid="challenge-card">
  <Box data-testid="challenge-card-header">
    <Text data-testid="challenge-card-title">Title</Text>
  </Box>
  <Box data-testid="challenge-card-content">
    <Text data-testid="challenge-card-description">Description</Text>
  </Box>
</Box>
```

❌ **Bad:**
```typescript
// No relationship in names
<Box data-testid="card">
  <Box data-testid="header-section">
    <Text data-testid="text1">Title</Text>
  </Box>
  <Box data-testid="main-content">
    <Text data-testid="text2">Description</Text>
  </Box>
</Box>
```

**Why:** Related IDs:
- Shows component structure
- Easier to query related elements
- Self-documenting hierarchy
- Better maintainability

## Anti-Pattern: Using testID (React Native)

Don't use testID attribute (React Native syntax).

❌ **Bad:**
```typescript
// React Native syntax - doesn't work in web
<View testID="my-component">
  Content
</View>

// Query won't work
const element = screen.getByTestId('my-component'); // Fails!
```

✅ **Good:**
```typescript
// Web standard
<Box data-testid="my-component">
  Content
</Box>

// Query works
const element = screen.getByTestId('my-component'); // Success!
```

**Why:** `testID` is React Native only:
- Not recognized by React Testing Library
- Not a valid HTML attribute
- Tests will fail
- Use `data-testid` for web

## Anti-Pattern: Generic Test IDs

Avoid generic, non-descriptive test IDs.

❌ **Bad:**
```typescript
<Box data-testid="component">
<Box data-testid="button">
<Box data-testid="text">
<Box data-testid="container">
<Box data-testid="wrapper">
```

✅ **Good:**
```typescript
<Box data-testid="login-form">
<Box data-testid="submit-button">
<Box data-testid="error-message">
<Box data-testid="user-profile-card">
<Box data-testid="navigation-menu-wrapper">
```

**Why:** Generic IDs:
- Cause naming conflicts
- Not self-documenting
- Hard to maintain
- Poor test readability

## Anti-Pattern: Using IDs Without Context

Don't use IDs that are too specific without context.

❌ **Bad:**
```typescript
// No context
<Box data-testid="option-1">
<Box data-testid="option-2">
<Box data-testid="option-3">

// Test is unclear
const option = screen.getByTestId('option-1'); // Which option?
```

✅ **Good:**
```typescript
// With context
<Box data-testid="meal-plan-option-1">
<Box data-testid="meal-plan-option-2">
<Box data-testid="meal-plan-option-3">

// Test is clear
const option = screen.getByTestId('meal-plan-option-1'); // Clear!
```

**Why:** Contextual IDs:
- Self-documenting
- Prevent naming conflicts
- More maintainable
- Better test readability

## Anti-Pattern: Hardcoded IDs in Loops

Don't use hardcoded test IDs in loops.

❌ **Bad:**
```typescript
{items.map((item) => (
  // All elements have same ID!
  <Box data-testid="list-item">
    {item.name}
  </Box>
))}
```

✅ **Good:**
```typescript
{items.map((item, index) => (
  // Unique ID for each element
  <Box data-testid={`list-item-${index}`}>
    {item.name}
  </Box>
))}

// Or with item ID
{items.map((item) => (
  <Box data-testid={`list-item-${item.id}`}>
    {item.name}
  </Box>
))}
```

**Why:** Dynamic IDs:
- Create unique identifiers
- Enable individual targeting
- Avoid ID collisions
- Better testing

## Summary

**Key Patterns:**
- Use `data-testid` (NOT `testID`)
- Use kebab-case consistently
- Include context in names
- Use template literals for dynamic IDs
- Use dots for hierarchy
- Include state when relevant
- Query by role first, verify test ID second
- Use `findByTestId` for async elements
- Use `queryByTestId` for absence checks
- Maintain consistent naming patterns
- Use parent-child relationships

**Anti-Patterns to Avoid:**
- Using `testID` (React Native)
- Generic IDs without context
- Inconsistent naming conventions
- Hardcoded IDs in loops
- Not using template literals
- Missing context in names
- Using IDs as primary query method
- Querying by className or XPath
