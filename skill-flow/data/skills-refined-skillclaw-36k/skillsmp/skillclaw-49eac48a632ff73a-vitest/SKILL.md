---
name: vitest
description: Use this skill when writing or configuring tests for TypeScript projects with Vitest, leveraging its fast performance and built-in features for assertions, mocking, and coverage.
---

# Vitest Testing Framework

## Overview

Vitest is a modern testing framework designed for TypeScript/JavaScript projects, providing fast test execution through Vite's HMR, native ESM support, and first-class TypeScript integration. It is compatible with Jest, making migration easy.

## Quick Start

1. **Installation**:
   ```bash
   npm install -D vitest
   ```

2. **Configuration**:
   Create a `vitest.config.ts` file:
   ```typescript
   import { defineConfig } from 'vitest/config';

   export default defineConfig({
     test: {
       globals: true,           // Use describe/it/expect globally
       environment: 'node',     // or 'jsdom' for DOM testing
       coverage: {
         provider: 'v8',        // or 'istanbul'
         reporter: ['text', 'json', 'html'],
         exclude: [
           'node_modules/',
           'dist/',
           '**/*.test.ts',
           '**/*.spec.ts',
         ],
       },
       include: ['**/*.{test,spec}.{ts,tsx}'],
       exclude: ['node_modules', 'dist', '.idea', '.git', '.cache'],
     },
   });
   ```

3. **Write Tests**:
   Create a test file (e.g., `calculator.test.ts`):
   ```typescript
   import { describe, it, expect, vi, beforeEach } from 'vitest';

   describe('Calculator', () => {
     beforeEach(() => {
       vi.clearAllMocks();
     });

     it('adds numbers correctly', () => {
       expect(add(2, 3)).toBe(5);
     });

     it('handles async operations', async () => {
       const result = await fetchData();
       expect(result).toMatchObject({ id: 1 });
     });

     it('mocks dependencies', () => {
       const mockFn = vi.fn().mockReturnValue(42);
       expect(mockFn()).toBe(42);
       expect(mockFn).toHaveBeenCalledOnce();
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

```typescript
// Mock module
vi.mock('./api', () => ({ fetchUser: vi.fn() }));

// Spy on method
const spy = vi.spyOn(object, 'method');

// Mock implementation
mockFn.mockImplementation((x) => x * 2);
mockFn.mockResolvedValue({ data: [] });
mockFn.mockRejectedValue(new Error('fail'));
```

## CLI Commands

- `vitest` - Watch mode
- `vitest run` - Single run
- `vitest run --coverage` - With coverage
- `vitest --workspace` - Monorepo mode