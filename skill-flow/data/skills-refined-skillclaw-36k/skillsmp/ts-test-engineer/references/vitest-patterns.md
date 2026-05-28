# Vitest Patterns Reference

Advanced patterns and configuration for Vitest.

## Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./vitest.setup.ts'],
    include: ['**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      exclude: ['node_modules', '**/*.d.ts', '**/*.config.*'],
    },
  },
});
```

## Setup File

```typescript
// vitest.setup.ts
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock IntersectionObserver
vi.stubGlobal('IntersectionObserver', vi.fn(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
})));
```

## Custom Matchers

```typescript
// vitest.setup.ts
import { expect } from 'vitest';

expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () =>
        pass
          ? `expected ${received} not to be within range ${floor} - ${ceiling}`
          : `expected ${received} to be within range ${floor} - ${ceiling}`,
    };
  },

  toBeValidEmail(received: string) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const pass = emailRegex.test(received);
    return {
      pass,
      message: () =>
        pass
          ? `expected ${received} not to be a valid email`
          : `expected ${received} to be a valid email`,
    };
  },
});

// Type declaration
declare module 'vitest' {
  interface Assertion<T> {
    toBeWithinRange(floor: number, ceiling: number): T;
    toBeValidEmail(): T;
  }
}
```

## Test Factories

```typescript
// test/factories/user.ts
import { faker } from '@faker-js/faker';

export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.string.uuid(),
    email: faker.internet.email(),
    name: faker.person.fullName(),
    role: 'user',
    createdAt: faker.date.past(),
    ...overrides,
  };
}

export function createAdmin(overrides: Partial<User> = {}): User {
  return createUser({ role: 'admin', ...overrides });
}

// Usage
const user = createUser();
const admin = createAdmin({ name: 'Admin User' });
```

## Parameterized Tests

```typescript
describe('validateEmail', () => {
  it.each([
    ['test@example.com', true],
    ['user.name@domain.org', true],
    ['invalid', false],
    ['@nodomain.com', false],
    ['spaces in@email.com', false],
  ])('validateEmail(%s) = %s', (email, expected) => {
    expect(validateEmail(email)).toBe(expected);
  });
});

// With objects for complex cases
describe('calculatePrice', () => {
  it.each`
    price   | quantity | discount | expected
    ${100}  | ${1}     | ${0}     | ${100}
    ${100}  | ${2}     | ${10}    | ${180}
    ${50}   | ${3}     | ${25}    | ${112.5}
  `('price=$price qty=$quantity discount=$discount% = $expected',
    ({ price, quantity, discount, expected }) => {
      expect(calculatePrice(price, quantity, discount)).toBe(expected);
    }
  );
});
```

## Mocking Patterns

### Module Mocks
```typescript
// Mock entire module
vi.mock('./api', () => ({
  fetchUser: vi.fn(),
  updateUser: vi.fn(),
}));

// Partial mock (keep some real implementations)
vi.mock('./utils', async () => {
  const actual = await vi.importActual('./utils');
  return {
    ...actual,
    generateId: vi.fn(() => 'mock-id'),
  };
});
```

### Timer Mocks
```typescript
describe('debounce', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should debounce calls', () => {
    const fn = vi.fn();
    const debounced = debounce(fn, 100);

    debounced();
    debounced();
    debounced();

    expect(fn).not.toHaveBeenCalled();

    vi.advanceTimersByTime(100);

    expect(fn).toHaveBeenCalledOnce();
  });
});
```

### Date Mocks
```typescript
describe('formatRelativeTime', () => {
  beforeEach(() => {
    vi.setSystemTime(new Date('2024-01-15T10:00:00Z'));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should show "just now" for recent times', () => {
    const date = new Date('2024-01-15T09:59:30Z');
    expect(formatRelativeTime(date)).toBe('just now');
  });
});
```

## Testing Async Patterns

### Promises
```typescript
it('should resolve with data', async () => {
  const result = await fetchData();
  expect(result).toMatchObject({ id: expect.any(String) });
});

it('should reject on error', async () => {
  await expect(fetchInvalidData()).rejects.toThrow('Not found');
});
```

### Callbacks
```typescript
it('should call callback with result', () => {
  return new Promise<void>((resolve) => {
    processData('input', (result) => {
      expect(result).toBe('processed');
      resolve();
    });
  });
});

// Or with vi.fn()
it('should call callback', async () => {
  const callback = vi.fn();
  await processData('input', callback);
  expect(callback).toHaveBeenCalledWith('processed');
});
```

## Snapshot Testing (Use Sparingly)

```typescript
// Inline snapshots - easier to review
it('should format user', () => {
  const formatted = formatUser(createUser({ name: 'John', role: 'admin' }));

  expect(formatted).toMatchInlineSnapshot(`
    {
      "displayName": "John (Admin)",
      "initials": "J",
    }
  `);
});

// File snapshots for large outputs
it('should generate config', () => {
  const config = generateConfig(options);
  expect(config).toMatchSnapshot();
});
```

## Test Organization

```typescript
describe('OrderService', () => {
  describe('createOrder', () => {
    describe('with valid input', () => {
      it('should create order', () => {});
      it('should calculate total', () => {});
      it('should apply discount', () => {});
    });

    describe('with invalid input', () => {
      it('should reject empty cart', () => {});
      it('should reject negative quantities', () => {});
    });
  });

  describe('cancelOrder', () => {
    it('should cancel pending order', () => {});
    it('should not cancel shipped order', () => {});
  });
});
```
