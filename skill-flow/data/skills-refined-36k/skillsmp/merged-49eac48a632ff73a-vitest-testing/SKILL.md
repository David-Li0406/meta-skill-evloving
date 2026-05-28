---
name: vitest-testing
description: Use this skill for writing and configuring tests with Vitest, a modern TypeScript testing framework that supports assertions, mocking, coverage, and component testing for TypeScript projects.
---

# Vitest Testing Framework

## Overview

Vitest is a next-generation test framework powered by Vite, designed for modern TypeScript/JavaScript projects. It provides blazing-fast test execution through HMR-based test running, native ESM support, and first-class TypeScript integration.

**Key Features**:
- ⚡ **Vite-native**: Instant HMR-based test execution (10-100x faster than Jest)
- 🎯 **TypeScript-first**: Built-in TypeScript support, no configuration needed
- 🔄 **ESM-native**: Native ES modules, async/await, top-level await
- 🧪 **Jest-compatible**: Compatible API for easy migration
- 📸 **Snapshot testing**: Built-in snapshot support
- 🎨 **Component testing**: React Testing Library, Vue Test Utils integration
- 📊 **Coverage**: Built-in v8/c8 coverage (faster than Istanbul)
- 🌐 **UI mode**: Beautiful web UI for test debugging

## Quick Start

1. **Installation**:
   ```bash
   npm install -D vitest
   ```

2. **Basic Setup**:
   Create a `vitest.config.ts` file:
   ```typescript
   import { defineConfig } from 'vitest/config';

   export default defineConfig({
     test: {
       globals: true,
       environment: 'node', // or 'jsdom' for DOM testing
       coverage: {
         provider: 'v8',
         reporter: ['text', 'json', 'html'],
         exclude: ['node_modules/', 'dist/', '**/*.test.ts', '**/*.spec.ts'],
       },
       include: ['**/*.{test,spec}.{ts,tsx}'],
     },
   });
   ```

3. **Write Tests**:
   Example test structure:
   ```typescript
   import { describe, it, expect, beforeEach } from 'vitest';

   describe('Calculator', () => {
     let calculator: Calculator;

     beforeEach(() => {
       calculator = new Calculator();
     });

     it('adds two numbers correctly', () => {
       const result = calculator.add(2, 3);
       expect(result).toBe(5);
     });
   });
   ```

## Core Assertions

| Assertion | Purpose |
|-----------|---------|
| `toBe(value)` | Strict equality (===) |
| `toEqual(value)` | Deep equality |
| `toMatchObject(obj)` | Partial object match |
| `toContain(item)` | Array/string contains |
| `toThrow(error?)` | Function throws |
| `toMatchSnapshot()` | Snapshot testing |
| `toHaveBeenCalledWith()` | Mock call verification |

## Mocking

### Mocking Modules
```typescript
vi.mock('./api', () => ({ fetchUser: vi.fn() }));
```

### Spying on Methods
```typescript
const spy = vi.spyOn(object, 'method');
```

### Mock Implementation
```typescript
const mockFn = vi.fn().mockImplementation((x) => x * 2);
```

## React Testing Integration

### Setup React Testing Library
```bash
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

**vitest.config.ts** (React):
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
});
```

### React Component Testing
```typescript
import { render, screen } from '@testing-library/react';
import { Counter } from './Counter';

describe('Counter Component', () => {
  it('renders initial count', () => {
    render(<Counter initialCount={0} />);
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });
});
```

## Vue Testing Integration

### Setup Vue Test Utils
```bash
npm install -D @vue/test-utils @vitejs/plugin-vue
```

**vitest.config.ts** (Vue):
```typescript
import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'happy-dom',
  },
});
```

### Vue Component Testing
```typescript
import { mount } from '@vue/test-utils';
import Counter from './Counter.vue';

describe('Counter.vue', () => {
  it('renders initial count', () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 5 },
    });
    expect(wrapper.text()).toContain('Count: 5');
  });
});
```

## Coverage Configuration

### Advanced Coverage Setup
```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'dist/', '**/*.test.ts'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
      all: true,
    },
  },
});
```

## Best Practices

1. **Use globals: true** - Simpler imports, Jest-compatible.
2. **Prefer vi over jest** - Use Vitest-native API for new code.
3. **Use v8 coverage** - Faster than Istanbul, works with native ESM.
4. **Test in isolation** - Each test should be independent.
5. **Mock external dependencies** - Network, file system, timers.
6. **Use TypeScript** - Full type safety in tests.
7. **Run tests in CI mode** - Use `vitest run` for CI, not watch mode.

## Resources

- **Documentation**: [Vitest Documentation](https://vitest.dev)
- **API Reference**: [Vitest API](https://vitest.dev/api/)
- **Migration Guide**: [Vitest Migration Guide](https://vitest.dev/guide/migration.html)