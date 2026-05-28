---
name: javascript-unit-testing
description: Use this skill when writing and running unit tests for JavaScript/TypeScript projects using Vitest or Jest, including component testing and configuration setup.
---

# JavaScript/TypeScript Unit Testing Skill

## When to Activate

Activate this skill when:
- Writing JavaScript or TypeScript unit tests
- Testing Svelte, React, or Vue components
- Setting up Vitest or Jest configuration
- Working with mocks, spies, or test utilities
- Running tests or checking coverage

## Framework Selection

| Use Case | Framework |
|----------|-----------|
| SvelteKit, Vite projects | **Vitest** (recommended) |
| Non-Vite projects, React Native | **Jest** |

## Framework Detection

Before running tests, detect the framework:
- Check imports in test files
- Check configuration files: `vitest.config.*`, `jest.config.*`
- Check `package.json` dependencies (workspace-specific in monorepos)
- Grep test scripts in `package.json`

## Quick Commands

### Vitest
```bash
npx vitest              # Watch mode
npx vitest run          # Single run (CI)
npx vitest run --coverage
npx vitest --ui         # Visual UI
```

### Jest
```bash
pnpm test
pnpm test --watch
pnpm test --coverage
```

## Running Tests

Run relevant tests only unless explicitly requested:
```bash
pnpm run test path/to/file.test.ts
# For monorepos: cd apps/demo-app && pnpm run test path/to/file.test.ts
```

For all tests, use the `test` script in the closest `package.json`:
```bash
pnpm run test
# For monorepos: cd apps/demo-app && pnpm run test
```

## Test Structure: AAA Pattern

```typescript
import { describe, it, expect, beforeEach } from 'vitest';

describe('UserService', () => {
    let userService: UserService;

    beforeEach(() => {
        userService = new UserService();
    });

    it('should create a new user with valid data', () => {
        // Arrange
        const email = 'test@example.com';
        const password = 'secure_pass123';

        // Act
        const result = userService.register(email, password);

        // Assert
        expect(result.success).toBe(true);
        expect(result.user.email).toBe(email);
    });
});
```

## Mocking

### Vitest
```typescript
import { vi } from 'vitest';

vi.mock('./api', () => ({
    fetchUser: vi.fn()
}));

vi.mocked(fetchUser).mockResolvedValue({ id: 1, name: 'John' });
```

### Jest
```typescript
jest.mock('./api', () => ({
    fetchUser: jest.fn()
}));
```

## Component Testing (Svelte)

```typescript
import { render, screen, fireEvent } from '@testing-library/svelte';
import Counter from './Counter.svelte';

it('should increment count on click', async () => {
    render(Counter, { props: { initialCount: 0 } });

    const button = screen.getByRole('button', { name: /increment/i });
    await fireEvent.click(button);

    expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

## Common Assertions

```typescript
// Equality
expect(value).toBe(expected);           // Strict ===
expect(value).toEqual(expected);        // Deep equality

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeNull();

// Arrays/Objects
expect(array).toContain(item);
expect(obj).toHaveProperty('key');

// Exceptions
expect(() => fn()).toThrow('error');

// Async
await expect(promise).resolves.toBe(value);
await expect(promise).rejects.toThrow();
```

## Query Priority (Testing Library)

1. `getByRole` - Accessible queries (best)
2. `getByLabelText` - Form fields
3. `getByPlaceholderText` - Inputs
4. `getByText` - Non-interactive elements
5. `getByTestId` - Last resort

## Directory Structure

```
src/
├── lib/
│   ├── components/
│   │   ├── Button.svelte
│   │   └── Button.test.ts
│   └── utils/
│       ├── format.ts
│       └── format.test.ts
└── tests/
    ├── setup.ts
    └── integration/
```

## SvelteKit Testing

### Load Functions
```typescript
import { load } from './+page.server';

it('should fetch posts', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve([{ id: 1 }])
    });

    const result = await load({ fetch: mockFetch } as any);
    expect(result.posts).toHaveLength(1);
});
```

### Form Actions
```typescript
import { actions } from './+page.server';

it('should validate login', async () => {
    const formData = new FormData();
    formData.set('email', 'test@example.com');

    const request = new Request('http://localhost', {
        method: 'POST',
        body: formData
    });

    const result = await actions.default({ request } as any);
    expect(result.success).toBe(true);
});
```

## Related Resources

See `AgentUsage/testing_javascript.md` for complete documentation including:
- Jest configuration
- Async testing patterns
- SvelteKit-specific patterns
- CI/CD integration