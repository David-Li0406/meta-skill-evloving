---
name: javascript-testing
description: Use this skill when writing and running JavaScript or TypeScript tests, including unit tests for frontend frameworks like React, Svelte, or Vue, using Vitest or Jest.
---

# Skill body

## When to Activate

Activate this skill when:
- Writing JavaScript or TypeScript tests
- Testing components in frameworks like Svelte, React, or Vue
- Setting up Vitest or Jest configurations
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

## Vitest Setup (SvelteKit)

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
    render(Counter);
    const button = screen.getByRole('button');
    await fireEvent.click(button);
    expect(screen.getByText(/count is 1/i)).toBeInTheDocument();
});
```