---
name: vitest
description: Write and run tests with Vitest for Vite-based projects. Use when testing Astro components, JavaScript modules, or any Vite project requiring fast, modern testing.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Vitest Skill

Fast, Vite-native testing framework with Jest-compatible API.

## Why Vitest

| Feature | Benefit |
|---------|---------|
| Vite-powered | Instant HMR, same config as app |
| Jest-compatible | Familiar API, easy migration |
| ESM-first | Native ES modules support |
| TypeScript | Out-of-the-box support |
| Watch mode | Smart re-runs on file changes |

## Project Setup

```bash
# Install
npm install -D vitest

# With UI and coverage
npm install -D vitest @vitest/ui @vitest/coverage-v8
```

```json
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage"
  }
}
```

## Configuration

```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // Test file patterns
    include: ['**/*.{test,spec}.{js,ts}'],
    exclude: ['node_modules', 'dist'],

    // Environment
    environment: 'node', // or 'jsdom', 'happy-dom'

    // Global setup
    globals: true, // Use describe/it/expect without imports

    // Coverage
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'test/'],
    },

    // Timeouts
    testTimeout: 10000,
    hookTimeout: 10000,
  },
});
```

### Shared Config with Vite

```javascript
// vitest.config.js
import { defineConfig, mergeConfig } from 'vitest/config';
import viteConfig from './vite.config.js';

export default mergeConfig(viteConfig, defineConfig({
  test: {
    environment: 'jsdom',
  },
}));
```

## Writing Tests

### Basic Test Structure

```javascript
// src/utils.test.js
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { formatDate, calculateTotal } from './utils.js';

describe('formatDate', () => {
  it('should format date in US locale', () => {
    const date = new Date('2024-01-15');
    expect(formatDate(date)).toBe('January 15, 2024');
  });

  it('should handle invalid date', () => {
    expect(() => formatDate('invalid')).toThrow('Invalid date');
  });
});

describe('calculateTotal', () => {
  it('should sum array of numbers', () => {
    expect(calculateTotal([1, 2, 3])).toBe(6);
  });

  it('should return 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });
});
```

### Setup and Teardown

```javascript
import { describe, it, expect, beforeAll, afterAll, beforeEach, afterEach } from 'vitest';

describe('Database tests', () => {
  let db;

  beforeAll(async () => {
    // Run once before all tests
    db = await connectToTestDatabase();
  });

  afterAll(async () => {
    // Run once after all tests
    await db.close();
  });

  beforeEach(async () => {
    // Run before each test
    await db.clear();
  });

  afterEach(() => {
    // Run after each test
  });

  it('should insert record', async () => {
    await db.insert({ name: 'Test' });
    const records = await db.findAll();
    expect(records).toHaveLength(1);
  });
});
```

## Assertions

```javascript
import { expect } from 'vitest';

// Equality
expect(value).toBe(expected);           // Strict equality (===)
expect(value).toEqual(expected);        // Deep equality
expect(value).toStrictEqual(expected);  // Deep + type equality

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeGreaterThanOrEqual(3);
expect(value).toBeLessThan(5);
expect(value).toBeCloseTo(0.3, 5);      // Floating point

// Strings
expect(value).toMatch(/pattern/);
expect(value).toContain('substring');

// Arrays
expect(array).toContain(item);
expect(array).toHaveLength(3);
expect(array).toEqual(expect.arrayContaining([1, 2]));

// Objects
expect(obj).toHaveProperty('key');
expect(obj).toHaveProperty('nested.key', value);
expect(obj).toMatchObject({ key: value });

// Exceptions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('error message');
expect(() => fn()).toThrow(ErrorClass);

// Async
await expect(promise).resolves.toBe(value);
await expect(promise).rejects.toThrow();
```

## Mocking

### Functions

```javascript
import { vi, describe, it, expect } from 'vitest';

describe('mocking', () => {
  it('should mock function', () => {
    const mockFn = vi.fn();

    mockFn('arg1', 'arg2');

    expect(mockFn).toHaveBeenCalled();
    expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  it('should mock return value', () => {
    const mockFn = vi.fn()
      .mockReturnValue('default')
      .mockReturnValueOnce('first')
      .mockReturnValueOnce('second');

    expect(mockFn()).toBe('first');
    expect(mockFn()).toBe('second');
    expect(mockFn()).toBe('default');
  });

  it('should mock implementation', () => {
    const mockFn = vi.fn((x) => x * 2);

    expect(mockFn(5)).toBe(10);
  });
});
```

### Modules

```javascript
import { vi, describe, it, expect } from 'vitest';

// Mock entire module
vi.mock('./api.js', () => ({
  fetchUser: vi.fn(() => Promise.resolve({ id: 1, name: 'Test' })),
}));

// Import after mocking
import { fetchUser } from './api.js';
import { getUserName } from './user.js';

describe('getUserName', () => {
  it('should return user name', async () => {
    const name = await getUserName(1);
    expect(name).toBe('Test');
    expect(fetchUser).toHaveBeenCalledWith(1);
  });
});
```

### Spies

```javascript
import { vi, describe, it, expect } from 'vitest';

describe('spies', () => {
  it('should spy on method', () => {
    const obj = {
      method: (x) => x + 1,
    };

    const spy = vi.spyOn(obj, 'method');

    obj.method(5);

    expect(spy).toHaveBeenCalledWith(5);
    expect(spy).toHaveReturnedWith(6);

    spy.mockRestore();
  });
});
```

### Timers

```javascript
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('timers', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should handle setTimeout', () => {
    const callback = vi.fn();

    setTimeout(callback, 1000);

    expect(callback).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1000);

    expect(callback).toHaveBeenCalled();
  });

  it('should run all timers', () => {
    const callback = vi.fn();

    setTimeout(callback, 1000);
    setTimeout(callback, 2000);

    vi.runAllTimers();

    expect(callback).toHaveBeenCalledTimes(2);
  });
});
```

## DOM Testing

```javascript
// vitest.config.js
export default defineConfig({
  test: {
    environment: 'happy-dom', // or 'jsdom'
  },
});
```

```javascript
// src/components/Button.test.js
import { describe, it, expect } from 'vitest';

describe('Button component', () => {
  it('should render button with text', () => {
    document.body.innerHTML = '<button id="btn">Click me</button>';

    const button = document.getElementById('btn');

    expect(button).not.toBeNull();
    expect(button.textContent).toBe('Click me');
  });

  it('should handle click event', () => {
    document.body.innerHTML = '<button id="btn">Click</button>';

    const button = document.getElementById('btn');
    let clicked = false;

    button.addEventListener('click', () => {
      clicked = true;
    });

    button.click();

    expect(clicked).toBe(true);
  });
});
```

## Async Testing

```javascript
import { describe, it, expect } from 'vitest';

describe('async tests', () => {
  // Return promise
  it('should resolve promise', () => {
    return fetchData().then((data) => {
      expect(data).toBe('data');
    });
  });

  // Async/await
  it('should await async function', async () => {
    const data = await fetchData();
    expect(data).toBe('data');
  });

  // Resolves/rejects
  it('should resolve with value', async () => {
    await expect(fetchData()).resolves.toBe('data');
  });

  it('should reject with error', async () => {
    await expect(fetchBadData()).rejects.toThrow('Error');
  });
});
```

## Snapshot Testing

```javascript
import { describe, it, expect } from 'vitest';

describe('snapshots', () => {
  it('should match snapshot', () => {
    const user = { id: 1, name: 'Test', createdAt: new Date('2024-01-01') };

    expect(user).toMatchSnapshot();
  });

  it('should match inline snapshot', () => {
    const result = formatOutput(data);

    expect(result).toMatchInlineSnapshot(`
      {
        "formatted": true,
        "value": "test",
      }
    `);
  });
});
```

Update snapshots:
```bash
vitest -u
```

## Test Filtering

```bash
# Run specific file
vitest src/utils.test.js

# Run tests matching pattern
vitest --grep "should format"

# Run only failed tests
vitest --changed

# Run in watch mode
vitest --watch
```

## Coverage

```javascript
// vitest.config.js
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.js'],
      exclude: ['src/**/*.test.js', 'src/**/*.spec.js'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
});
```

```bash
# Run with coverage
vitest run --coverage
```

## Integration with Astro

```javascript
// vitest.config.js
import { getViteConfig } from 'astro/config';

export default getViteConfig({
  test: {
    include: ['**/*.test.js'],
  },
});
```

## Checklist

Before committing:

- [ ] All tests pass: `npm test`
- [ ] Coverage meets thresholds
- [ ] New code has corresponding tests
- [ ] Mocks are restored after tests
- [ ] No `.only` or `.skip` left in tests
- [ ] Async tests properly awaited

## Related Skills

- **unit-testing** - General testing patterns
- **astro** - Testing Astro components
- **javascript-author** - Code patterns to test
- **build-tooling** - Vite configuration
