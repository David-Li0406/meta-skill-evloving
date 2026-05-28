---
name: tdd-workflow
description: Use this skill when developing new features, fixing bugs, or refactoring code to enforce test-driven development (TDD) principles, ensuring over 80% test coverage through unit, integration, and end-to-end (E2E) tests.
---

# Test-Driven Development (TDD) Workflow

This skill ensures that all code development adheres to TDD principles and maintains comprehensive test coverage.

## When to Activate

- Developing new features or functionalities
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints
- Creating new components

## Core Principles

### 1. Write Tests Before Code
Always write tests first, then implement the code to make the tests pass.

### 2. Coverage Requirements
- Minimum 80% coverage (unit + integration + E2E)
- Cover all edge cases
- Test error scenarios
- Validate boundary conditions

### 3. Types of Tests

#### Unit Tests
- Independent functions and utilities
- Component logic
- Pure functions
- Helper functions and utilities

#### Integration Tests
- API endpoints
- Database operations
- Service interactions
- External API calls

#### E2E Tests (Playwright)
- Key user flows
- Complete workflows
- Browser automation
- UI interactions

## TDD Workflow Steps

### Step 1: Write User Journeys
```
As a [role], I want to [action] so that [benefit]

Example:
As a user, I want to perform semantic market searches,
so that I can find relevant markets even without exact keywords.
```

### Step 2: Generate Test Cases
Create comprehensive test cases for each user journey:

```typescript
describe('Semantic Search', () => {
  it('returns relevant markets for query', async () => {
    // Test implementation
  });

  it('handles empty query gracefully', async () => {
    // Test edge case
  });

  it('falls back to substring search when Redis unavailable', async () => {
    // Test fallback behavior
  });

  it('sorts results by similarity score', async () => {
    // Test sorting logic
  });
});
```

### Step 3: Run Tests (They Should Fail)
```bash
npm test
# Tests should fail - we haven't implemented them yet
```

### Step 4: Implement Code
Write the minimal code necessary to make the tests pass:

```typescript
// Implementation guided by tests
export async function searchMarkets(query: string) {
  // Implementation goes here
}
```

### Step 5: Run Tests Again
```bash
npm test
# Tests should now pass
```

### Step 6: Refactor
Improve code quality while keeping tests green:
- Eliminate duplication
- Improve naming
- Optimize performance
- Enhance readability

### Step 7: Verify Coverage
```bash
npm run test:coverage
# Verify that coverage reaches 80%+
```

## Testing Patterns

### Unit Testing Pattern (Jest/Vitest)
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    fireEvent.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### API Integration Testing Pattern
```typescript
import { NextRequest } from 'next/server';
import { GET } from './route';

describe('GET /api/markets', () => {
  it('returns markets successfully', async () => {
    const request = new NextRequest('http://localhost/api/markets');
    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    // Additional assertions on data
  });
});
```