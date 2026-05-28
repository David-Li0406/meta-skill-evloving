---
name: javascript-testing-patterns
description: Use this skill when implementing comprehensive testing strategies for JavaScript/TypeScript applications, including unit tests, integration tests, and end-to-end tests with Jest and Vitest.
---

# JavaScript Testing Patterns

Comprehensive guide for implementing robust testing strategies in JavaScript/TypeScript applications using modern testing frameworks and best practices.

## When to Use This Skill

- Setting up test infrastructure for new projects
- Writing unit tests for functions and classes
- Creating integration tests for APIs and services
- Implementing end-to-end tests for user flows
- Mocking external dependencies and APIs
- Testing React, Vue, or other frontend components
- Implementing test-driven development (TDD)
- Setting up continuous testing in CI/CD pipelines

## Testing Frameworks

### Jest - Full-Featured Testing Framework

**Setup:**

```typescript
// jest.config.ts
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  collectCoverageFrom: ['src/**/*.ts', '!src/**/*.d.ts', '!src/**/*.interface.ts'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
};

export default config;
```

### Vitest - Fast, Vite-Native Testing

**Setup:**

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['**/*.d.ts', '**/*.config.ts', '**/dist/**'],
    },
    setupFiles: ['./src/test/setup.ts'],
  },
});
```

## Unit Testing Patterns

### Pattern 1: Testing Pure Functions

```typescript
// utils/calculator.ts
export function add(a: number, b: number): number {
  return a + b;
}

export function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error('Division by zero');
  }
  return a / b;
}

// utils/calculator.test.ts
import { describe, it, expect } from 'vitest';
import { add, divide } from './calculator';

describe('Calculator', () => {
  describe('add', () => {
    it('should add two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('should handle zero', () => {
      expect(add(0, 5)).toBe(5);
    });
  });

  describe('divide', () => {
    it('should throw error when dividing by zero', () => {
      expect(() => divide(10, 0)).toThrow('Division by zero');
    });
  });
});
```

### Pattern 2: Testing Classes

```typescript
describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  describe('create', () => {
    it('should create a new user', () => {
      const user = { id: '1', name: 'John', email: 'john@example.com' };
      const created = service.create(user);

      expect(created).toEqual(user);
    });
  });
});
```