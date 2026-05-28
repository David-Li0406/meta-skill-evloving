---
name: javascript-testing
description: Use this skill when writing and running JavaScript/TypeScript tests for frontend projects using Vitest or Jest, including unit tests, mocking, and component testing.
---

# JavaScript/TypeScript Testing Skill

## When to Activate

Activate this skill when:
- Writing JavaScript or TypeScript tests
- Testing Svelte, React, or Vue components
- Setting up Vitest or Jest configuration
- Working with mocks, spies, or test utilities
- Running tests or checking coverage

## Framework Selection

| Use Case | Framework |
|----------|-----------|
| SvelteKit, Vite projects | **Vitest** (recommended) |
| Non-Vite projects, React Native | **Jest** |

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

## Test Structure: AAA Pattern

```typescript
import { describe, it, expect, beforeEach } from 'vitest';

describe('UserService', () => {
    let userService: UserService;

    beforeEach(() => {
        userService = new UserService();
    });

    it('should create a new user with valid data', () => {
        const email = 'test@example.com';
        const password = 'secure_pass123';
        const result = userService.register(email, password);
        expect(result.success).toBe(true);
        expect(result.user.email).toBe(email);
    });
});
```

## Setup

### Vitest Setup (SvelteKit)
```typescript
// vite.config.ts
import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
    plugins: [sveltekit()],
    test: {
        include: ['src/**/*.{test,spec}.{js,ts}'],
        globals: true,
        environment: 'jsdom',
        setupFiles: ['./src/tests/setup.ts'],
    }
});
```

### Jest Setup
```bash
# JavaScript
npm install --save-dev jest

# TypeScript
npm install --save-dev jest ts-jest @types/jest
npx ts-jest config:init

# React
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

### Configuration (jest.config.js)
```javascript
module.exports = {
  testEnvironment: 'node', // or 'jsdom' for browser
  preset: 'ts-jest',
  testMatch: ['**/__tests__/**/*.test.[jt]s?(x)'],
  collectCoverageFrom: ['src/**/*.{js,ts,tsx}', '!src/**/*.d.ts'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss)$': 'identity-obj-proxy'
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest'
  }
};
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

## Best Practices
1. **Test behavior, not implementation** - Focus on what, not how.
2. **Use descriptive names** - Clear test descriptions.
3. **One assertion per test** - When possible.
4. **Arrange-Act-Assert** - Structure tests clearly.
5. **Mock external dependencies** - Isolate units.
6. **Use beforeEach for setup** - DRY test code.
7. **Clean up after tests** - Prevent test pollution.
8. **Run tests in watch mode** - Faster feedback.
9. **Maintain high coverage** - But focus on quality.
10. **Use snapshot tests wisely** - For UI components.

## Related Resources
See `AgentUsage/testing_javascript.md` for complete documentation including:
- Jest configuration
- Async testing patterns
- SvelteKit-specific patterns
- CI/CD integration