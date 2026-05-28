---
name: tdd
description: Read when writing tests
---

# Test-Driven Development (TDD) Rules


## Philosophy
- DRY: Use data-driven tests with flat arrays, avoid repetition
- Pure functions only - avoid heavy mocking
- Co-locate `.test.ts` files next to source files
- Use `toModule(__filename)` for test names
- **CRITICAL: Fix bugs in source, never work around them in tests**

## Running Tests
- `npm test` - Type check + unit tests (slow, run once at the end)
- `npm run test:unit` - Unit tests only (fast)
- `npm run test:unit -- file` - Run specific file
- `npm run test:unit -- --testNamePattern="pattern"` - Run matching tests
- `npm run test:unit:min` - See only failures with the test name, expected and actual values. Good for adapting tests to match the expected and actual values. Your bread and butter.

## Template
```typescript
import { toModule, type FnTestCase } from 'src/util/tests'
import { describe, it, expect } from 'vitest'
import { divide } from './myModule'

describe(toModule(__filename), () => {
  describe('divide', () => {
    const cases: FnTestCase<typeof divide>[] = [
      { desc: 'normal division', input: { a: 10, b: 2 }, expected: 5 },
      { desc: 'throws when dividing by zero', input: { a: 10, b: 0 }, expected: 0, throws: 'Cannot divide by zero' },
    ]

    cases.forEach(({ desc, input, expected, throws }) => {
      it(`should handle ${desc}`, () => {
        if (throws) {
          expect(() => divide(input.a, input.b)).toThrow(throws)
        } else {
          expect(divide(input.a, input.b)).toBe(expected)
        }
      })
    })
  })
})
```

## Core Patterns

### 1. Test Utilities
```typescript
import { toModule, type FnTestCase, type TestCase } from 'src/util/tests'

// Prefer FnTestCase for automatic type inference
const cases: FnTestCase<typeof myFn>[] = [...]

// Use TestCase<Input, Output> when you need custom types
const cases: TestCase<string, boolean>[] = [...]

// Add custom properties via intersection
type CustomCase = TestCase<string, boolean> & { myProp: number }
const cases: CustomCase[] = [
  { desc: 'test', input: 'x', expected: true, myProp: 42 }
]
```

### 2. Flat Structure
**ONE array per function** - don't split into validCases, errorCases, edgeCases:
```typescript
// ✅ Good
const cases: FnTestCase<typeof fn>[] = [
  { desc: 'valid', input: 'test', expected: true },
  { desc: 'throws on null', input: null as any, throws: 'Error' },
]

// ❌ Bad
const validCases = [...]; const errorCases = [...]
```

### 3. Error Cases
Start desc with "throws when..." or "throws on...", add `throws: 'message'`, omit `expected`:
```typescript
// ✅ Good - no expected when throwing
{ desc: 'throws when dividing by zero', input: { a: 10, b: 0 }, throws: 'Cannot divide by zero' }

// ❌ TypeScript error - can't have both throws and expected
{ desc: 'throws', input: x, throws: 'Error', expected: 42 }
```

### 4. Avoid `as any`
Only use when testing truly invalid types (null, undefined, wrong shape):
```typescript
// ✅ Prefer - no as any needed
{ desc: 'throws when invalid', input: { a: 10, b: 0 }, throws: 'Error' }

// ⚠️ Only when needed
{ desc: 'throws on null', input: null as any, throws: 'Error' }
```

### 5. Dynamic Descriptions
Use ternaries in template literals for dynamic test names:
```typescript
it(`should ${expected ? 'accept' : 'reject'} ${desc}`, () => {
  expect(isValid(input)).toBe(expected)
})
```

## What to Test

### ✅ Test These
- Pure functions with deterministic input/output
- Math, string formatting, validation logic
- Data transformers and filters
- Error factories with edge cases (empty, null, boundaries)

### ❌ Avoid These
- Database operations requiring mocks
- External APIs, file I/O
- GraphQL resolvers with heavy context
- Complex async workflows

## Style Rules
- One flat array per function with ALL cases (valid, errors, edges)
- One `forEach` loop with `if (throws)` check
- Short constants at top: `const USER_ID = 'user123'`
- Minimize `as any` usage
- Keep test data minimal but realistic
- Use chai-style assertions: `.to.be.an('array')`, `.to.have.property()`, `.to.have.length()`
- Skip redundant type checks when comparing values: `.equal('value')` not `.be.a('string').and.equal('value')`
- Keep type checks only when checking type without comparison: `.be.a('string')` or `.be.a('number')`
- When asserting on object properties, use `.to.have.property('prop', value)` instead of `expect(obj.prop).toBe(value)` - this provides better error messages showing both the object and property name. For arrays/objects, use `.to.have.property('prop').that.deep.equals(value)`
