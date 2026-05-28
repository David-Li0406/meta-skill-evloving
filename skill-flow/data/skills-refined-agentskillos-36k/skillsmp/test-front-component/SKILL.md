---
name: test-front-component
description: Creates unit tests for React frontend components using Vitest and React Testing Library, following accessibility-first best practices.
---

# Frontend Component Testing Skill

This skill provides instructions and best practices for testing React components in the Verseau frontend using Vitest and React Testing Library.

## Tech Stack

- **Testing Framework**: Vitest
- **Component Testing**: `@testing-library/react`
- **User Interactions**: `@testing-library/user-event` (preferred) or `fireEvent`
- **Matchers**: `@testing-library/jest-dom/vitest`
- **Environment**: jsdom

## Core Principles

### 1. Test Structure (AAA Pattern)

Structure tests using Arrange-Act-Assert:

```typescript
it('loads and displays greeting', async () => {
  // ARRANGE - setup the component
  const user = userEvent.setup();
  render(<MyComponent prop="value" />);

  // ACT - perform user interactions
  await user.click(screen.getByRole('button', { name: /submit/i }));

  // ASSERT - verify the expected outcome
  expect(screen.getByRole('heading')).toHaveTextContent('Success');
});
```

### 2. Query Priority (Accessibility-First)

Use queries in this priority order to write accessible tests:

1. **`getByRole`** - Top preference for most elements (buttons, headings, links, etc.)
   ```typescript
   screen.getByRole('button', { name: /submit/i });
   screen.getByRole('heading', { level: 1 });
   screen.getByRole('link', { name: /learn more/i });
   ```

2. **`getByLabelText`** - Preferred for form fields
   ```typescript
   screen.getByLabelText('Email');
   screen.getByLabelText(/mot de passe/i);
   ```

3. **`getByPlaceholderText`** - Only if no label exists
   ```typescript
   screen.getByPlaceholderText('Search...');
   ```

4. **`getByText`** - For non-interactive elements (divs, spans, paragraphs)
   ```typescript
   screen.getByText(/bienvenue/i);
   screen.getByText('Erreur détectée');
   ```

5. **`getByDisplayValue`** - For form elements with filled-in values
   ```typescript
   screen.getByDisplayValue('current value');
   ```

6. **`getByAltText`** - For images
   ```typescript
   screen.getByAltText('Logo de l\'application');
   ```

7. **`getByTestId`** - Last resort when other queries aren't possible
   ```typescript
   screen.getByTestId('custom-element');
   ```

### 3. Query Types

| Query Type | No Match | 1 Match | >1 Match | Async |
|------------|----------|---------|----------|-------|
| `getBy...` | Throws | Returns | Throws | No |
| `queryBy...` | Returns null | Returns | Throws | No |
| `findBy...` | Throws | Returns | Throws | Yes |
| `getAllBy...` | Throws | Returns [] | Returns [] | No |
| `queryAllBy...` | Returns [] | Returns [] | Returns [] | No |
| `findAllBy...` | Throws | Returns [] | Returns [] | Yes |

**Usage Guidelines:**
- Use `getBy*` for elements that should be present immediately
- Use `queryBy*` to assert an element is NOT present: `expect(screen.queryByText('Error')).not.toBeInTheDocument()`
- Use `findBy*` for elements that appear asynchronously (returns Promise)
- Use `*All*` variants when multiple elements are expected

### 4. User Interactions

**Prefer `userEvent` over `fireEvent`:**

`userEvent` simulates realistic user behavior with proper event sequences, whereas `fireEvent` only dispatches single DOM events.

```typescript
import userEvent from '@testing-library/user-event';

it('should handle user input', async () => {
  const user = userEvent.setup();
  render(<Form />);

  // Type in an input field
  await user.type(screen.getByLabelText('Email'), 'test@example.com');

  // Click a button
  await user.click(screen.getByRole('button', { name: /submit/i }));

  // Select from dropdown
  await user.selectOptions(screen.getByRole('combobox'), 'option1');

  // Keyboard interactions
  await user.keyboard('{Enter}');
});
```

**Use `fireEvent` only when:**
- `userEvent` doesn't support the specific interaction
- Testing specific low-level DOM events

```typescript
import { fireEvent } from '@testing-library/react';

// fireEvent for specific cases
fireEvent.scroll(container, { target: { scrollY: 100 } });
```

### 5. Scoping with `within`

Use `within` to query within a specific container:

```typescript
import { render, screen, within } from '@testing-library/react';

it('should find elements within container', () => {
  render(<DataTable />);

  const row = screen.getByRole('row', { name: /john doe/i });
  const editButton = within(row).getByRole('button', { name: /edit/i });

  expect(editButton).toBeInTheDocument();
});
```

### 6. Helper Functions

Create reusable helper functions for common queries or actions:

```typescript
// Extract common queries as helper functions at the top of the file
const getStatCard = (label: string) => {
  const labelElement = screen.getByText(label);
  const container = labelElement.closest('.fr-col') as HTMLElement;
  expect(container).toBeInTheDocument();
  return container;
};

const clickButton = (name: string | RegExp) => {
  const button = screen.getByRole('button', { name });
  fireEvent.click(button);
};

const expectStatCardCount = (label: string, count: string) => {
  const statCard = getStatCard(label);
  const countElement = within(statCard).getByText(count);
  expect(countElement).toHaveClass('fr-h2', 'fr-mb-0');
  return countElement;
};
```

## File Organization

- Place test files alongside the component: `MyComponent.spec.tsx`
- Every component in `apps/front/src/components` **MUST** have a corresponding `.spec.tsx` file
- Use `describe` blocks to group related tests
- Use `it` for individual test cases with descriptive names

## Template

```tsx
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { MyComponent } from './MyComponent';

// Helper functions at the top
const getSubmitButton = () => screen.getByRole('button', { name: /submit/i });

describe('MyComponent', () => {
  // Test fixture data
  const defaultProps = {
    title: 'Test Title',
    onSubmit: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders null when no data is provided', () => {
    const { container } = render(<MyComponent {...defaultProps} data={[]} />);
    expect(container.firstChild).toBeNull();
  });

  it('renders the title and main elements', () => {
    render(<MyComponent {...defaultProps} data={['item1']} />);

    expect(screen.getByRole('heading', { name: /test title/i })).toBeInTheDocument();
    expect(getSubmitButton()).toBeEnabled();
  });

  it('calls onSubmit when form is submitted', async () => {
    const user = userEvent.setup();
    render(<MyComponent {...defaultProps} data={['item1']} />);

    await user.click(getSubmitButton());

    expect(defaultProps.onSubmit).toHaveBeenCalledTimes(1);
  });

  it('disables submit button during loading', () => {
    render(<MyComponent {...defaultProps} data={['item1']} isLoading />);

    expect(getSubmitButton()).toBeDisabled();
  });

  it('shows error message when validation fails', async () => {
    const user = userEvent.setup();
    render(<MyComponent {...defaultProps} data={['item1']} />);

    // Leave required field empty and submit
    await user.click(getSubmitButton());

    expect(screen.getByRole('alert')).toHaveTextContent(/champ requis/i);
  });

  describe('with async data', () => {
    it('shows loading state initially', () => {
      render(<MyComponent {...defaultProps} isLoading />);

      expect(screen.getByText(/chargement/i)).toBeInTheDocument();
    });

    it('displays data after loading', async () => {
      render(<MyComponent {...defaultProps} data={['result']} />);

      expect(await screen.findByText('result')).toBeInTheDocument();
    });
  });
});
```

## Common Matchers (jest-dom)

```typescript
// Presence
expect(element).toBeInTheDocument();
expect(element).not.toBeInTheDocument();

// State
expect(element).toBeEnabled();
expect(element).toBeDisabled();
expect(element).toBeVisible();
expect(element).toBeChecked();

// Content
expect(element).toHaveTextContent('text');
expect(element).toHaveValue('value');
expect(element).toHaveDisplayValue('display');

// Attributes & Classes
expect(element).toHaveAttribute('href', '/path');
expect(element).toHaveClass('fr-btn', 'fr-btn--primary');
expect(element).toHaveStyle({ color: 'red' });

// Accessibility
expect(element).toHaveAccessibleName('Submit form');
expect(element).toHaveAccessibleDescription('Click to submit');
```

## Testing DSFR Components

DSFR components use specific class patterns. Use role-based queries when possible:

```typescript
// Button
screen.getByRole('button', { name: /envoyer/i });

// Input with label
screen.getByLabelText('Identifiant');

// Alert/Notice
screen.getByRole('alert');

// Accordion - click the button to expand
const accordionButton = screen.getByRole('button', { name: /voir les détails/i });
await user.click(accordionButton);
expect(screen.getByText('Contenu détaillé')).toBeVisible();

// Modal/Dialog
screen.getByRole('dialog');

// Navigation links
screen.getByRole('link', { name: /accueil/i });
```

## Running Tests

```bash
# Run all frontend tests
npm run test --workspace=apps/front

# Run tests in watch mode
npm run test -- --watch --workspace=apps/front

# Run specific test file
npm run test -- ControleGroup.spec.tsx --workspace=apps/front

# Run with coverage
npm run test -- --coverage --workspace=apps/front
```

## Common Pitfalls

1. **Don't use container queries unless necessary** - Prefer `screen` queries for better test readability
2. **Don't use `data-testid` as first choice** - Use accessible queries first (role, label, text)
3. **Always await `userEvent` methods** - They return Promises
4. **Use `findBy*` for async content** - Not `getBy*` with `waitFor`
5. **Reset mocks between tests** - Use `vi.clearAllMocks()` in `beforeEach`
6. **Don't test implementation details** - Test behavior from the user's perspective
7. **Avoid regex in class assertions** - Use `toHaveClass('fr-btn', 'fr-btn--primary')` not regex matching
