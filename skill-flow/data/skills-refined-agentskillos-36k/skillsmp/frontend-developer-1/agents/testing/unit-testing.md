---
name: Unit Testing Expert
description: Expert en tests unitaires - Jest, Vitest, mocking, coverage
workflows:
  - id: unit-test-setup
    template: wf-creation
    phase: Production
    name: Setup tests unitaires
    duration: 0.5 jour
  - id: unit-test-evolution
    template: wf-evolution
    phase: Réalisation
    name: Ajout tests unitaires
    duration: ongoing
    recurrence: par feature
---

# Agent Unit Testing

## Responsabilité

Maîtriser les outils et patterns de tests unitaires JavaScript/TypeScript.

## Tu NE fais PAS

- ❌ Tester les composants UI (render, interactions) → `component-testing.md`
- ❌ Écrire des tests E2E (browser, Playwright) → `e2e-testing.md`
- ❌ Définir la stratégie de test globale → skill `testing-process`
- ❌ Configurer le CI/CD pour les tests → skill `devops`

## Configuration Vitest

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    include: ['src/**/*.{test,spec}.{js,ts,jsx,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'src/test/'],
    },
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});
```

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

afterEach(() => {
  cleanup();
});
```

## Configuration Jest

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss)$': 'identity-obj-proxy',
  },
  transform: {
    '^.+\\.(ts|tsx)$': ['ts-jest', { useESM: true }],
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/test/**',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

## Structure des Tests

### Pattern AAA (Arrange, Act, Assert)

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { calculateTotal, formatCurrency } from './utils';

describe('calculateTotal', () => {
  // Arrange - données communes
  const items = [
    { price: 10, quantity: 2 },
    { price: 5, quantity: 3 },
  ];

  it('should calculate total correctly', () => {
    // Act
    const result = calculateTotal(items);

    // Assert
    expect(result).toBe(35);
  });

  it('should return 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('should handle single item', () => {
    const single = [{ price: 10, quantity: 1 }];
    expect(calculateTotal(single)).toBe(10);
  });
});

describe('formatCurrency', () => {
  it.each([
    [1000, '$1,000.00'],
    [999.99, '$999.99'],
    [0, '$0.00'],
    [-100, '-$100.00'],
  ])('should format %d as %s', (input, expected) => {
    expect(formatCurrency(input)).toBe(expected);
  });
});
```

### Test de fonctions async

```typescript
import { describe, it, expect, vi } from 'vitest';
import { fetchUser, processData } from './api';

describe('async functions', () => {
  it('should fetch user data', async () => {
    const user = await fetchUser('123');

    expect(user).toEqual({
      id: '123',
      name: expect.any(String),
    });
  });

  it('should handle errors', async () => {
    await expect(fetchUser('invalid')).rejects.toThrow('User not found');
  });

  it('should process data with callback', () => {
    return new Promise<void>((resolve) => {
      processData((result) => {
        expect(result).toBeDefined();
        resolve();
      });
    });
  });
});
```

## Mocking

### Mock de modules

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchUsers } from './userService';
import * as api from './api';

// Mock le module entier
vi.mock('./api');

describe('userService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should fetch and transform users', async () => {
    // Arrange
    const mockUsers = [{ id: '1', name: 'John' }];
    vi.mocked(api.get).mockResolvedValue(mockUsers);

    // Act
    const result = await fetchUsers();

    // Assert
    expect(api.get).toHaveBeenCalledWith('/users');
    expect(result).toEqual(mockUsers);
  });

  it('should handle API errors', async () => {
    vi.mocked(api.get).mockRejectedValue(new Error('Network error'));

    await expect(fetchUsers()).rejects.toThrow('Network error');
  });
});
```

### Mock partiel

```typescript
import { vi } from 'vitest';

// Mock partiel - garde les vraies implémentations
vi.mock('./utils', async () => {
  const actual = await vi.importActual<typeof import('./utils')>('./utils');
  return {
    ...actual,
    expensiveOperation: vi.fn(() => 'mocked'),
  };
});
```

### Spy sur méthodes

```typescript
import { describe, it, expect, vi } from 'vitest';

describe('spies', () => {
  it('should spy on console.log', () => {
    const consoleSpy = vi.spyOn(console, 'log');

    console.log('test message');

    expect(consoleSpy).toHaveBeenCalledWith('test message');
    consoleSpy.mockRestore();
  });

  it('should spy on object method', () => {
    const obj = {
      method: () => 'original',
    };

    const spy = vi.spyOn(obj, 'method').mockReturnValue('mocked');

    expect(obj.method()).toBe('mocked');
    expect(spy).toHaveBeenCalled();
  });
});
```

### Mock de timers

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { debounce, delay } from './timing';

describe('timing functions', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should delay execution', async () => {
    const callback = vi.fn();

    delay(callback, 1000);

    expect(callback).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1000);

    expect(callback).toHaveBeenCalledTimes(1);
  });

  it('should debounce calls', () => {
    const fn = vi.fn();
    const debounced = debounce(fn, 300);

    debounced();
    debounced();
    debounced();

    expect(fn).not.toHaveBeenCalled();

    vi.runAllTimers();

    expect(fn).toHaveBeenCalledTimes(1);
  });
});
```

## Test de Hooks React

```typescript
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { useCounter, useAsync } from './hooks';

describe('useCounter', () => {
  it('should initialize with default value', () => {
    const { result } = renderHook(() => useCounter());

    expect(result.current.count).toBe(0);
  });

  it('should initialize with custom value', () => {
    const { result } = renderHook(() => useCounter(10));

    expect(result.current.count).toBe(10);
  });

  it('should increment', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('should update on rerender with new props', () => {
    const { result, rerender } = renderHook(
      ({ initial }) => useCounter(initial),
      { initialProps: { initial: 0 } }
    );

    expect(result.current.count).toBe(0);

    rerender({ initial: 10 });

    // Selon l'implémentation du hook
    expect(result.current.count).toBe(10);
  });
});

describe('useAsync', () => {
  it('should handle async data', async () => {
    const mockFetch = vi.fn().mockResolvedValue({ data: 'test' });

    const { result } = renderHook(() => useAsync(mockFetch));

    expect(result.current.isLoading).toBe(true);

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.data).toEqual({ data: 'test' });
  });
});
```

## Matchers Courants

```typescript
// Égalité
expect(value).toBe(exact); // ===
expect(value).toEqual(deepEqual); // deep equality
expect(value).toStrictEqual(strictDeep); // + undefined props

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Nombres
expect(num).toBeGreaterThan(3);
expect(num).toBeGreaterThanOrEqual(3);
expect(num).toBeLessThan(5);
expect(num).toBeCloseTo(0.3, 5); // floating point

// Strings
expect(str).toMatch(/pattern/);
expect(str).toContain('substring');

// Arrays
expect(arr).toContain(item);
expect(arr).toContainEqual({ id: 1 });
expect(arr).toHaveLength(3);

// Objects
expect(obj).toHaveProperty('key');
expect(obj).toHaveProperty('nested.key', 'value');
expect(obj).toMatchObject({ partial: 'match' });

// Exceptions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('message');
expect(() => fn()).toThrow(ErrorClass);

// Mock assertions
expect(mock).toHaveBeenCalled();
expect(mock).toHaveBeenCalledTimes(2);
expect(mock).toHaveBeenCalledWith(arg1, arg2);
expect(mock).toHaveBeenLastCalledWith(arg);
```

## Couverture de Code

```bash
# Vitest
vitest run --coverage

# Jest
jest --coverage
```

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
      ],
      thresholds: {
        lines: 80,
        branches: 80,
        functions: 80,
        statements: 80,
      },
    },
  },
});
```

## Mots-clés de routage

`Jest`, `Vitest`, `test unitaire`, `unit test`, `mock`, `spy`, `stub`, `coverage`, `expect`, `describe`, `it`, `beforeEach`, `afterEach`

## Livrables

| Livrable | Description |
|----------|-------------|
| Suite de tests unitaires | Fichiers .test.ts avec tests pour utils et fonctions métier |
| Configuration Vitest/Jest | Setup des tests avec coverage et mocks |
| Rapport de couverture | Coverage report HTML avec seuils configurés |
