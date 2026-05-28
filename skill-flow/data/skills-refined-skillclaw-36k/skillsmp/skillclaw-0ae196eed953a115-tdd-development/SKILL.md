---
name: tdd-development
description: Use this skill when you want to implement code following Test-Driven Development (TDD) principles.
---

# TDD Development Skill

This skill is activated when the user wants to implement code. It ensures that all code is written following TDD.

## Required Cycle

### 1. RED - Write a Failing Test

```typescript
describe('MinhaFuncao', () => {
  it('should fazer X quando Y', () => {
    const result = minhaFuncao(input);
    expect(result).toBe(expected);
  });
});
```

**Rules:**
- Write the test BEFORE the code.
- The test MUST fail initially.
- The test defines the expected behavior.
- Commit: `test: add test for <feature>`

### 2. GREEN - Implement Minimum

```typescript
function minhaFuncao(input: Input): Output {
  // MINIMAL implementation to pass the test
  return expected;
}
```

**Rules:**
- Implement ONLY what is necessary to pass.
- Do not add extra functionalities.
- Do not optimize prematurely.
- Commit: `feat: implement <feature>`

### 3. REFACTOR - Improve

```typescript
function minhaFuncao(input: Input): Output {
  // Improved, cleaner code
  const processed = processInput(input);
  return formatOutput(processed);
}
```

**Rules:**
- Improve without changing behavior.
- Tests MUST continue to pass.
- Remove duplications.
- Improve names.
- Commit: `refactor: improve <what was improved>`

## Testing Patterns

Refer to `patterns/test-patterns.md` for examples.

## Anti-Patterns

### DO NOT DO:

```typescript
// Implement first, test later
function feature() { ... }

// Test that tests implementation, not behavior
it('should call methodX', () => {
  expect(spy).toHaveBeenCalled();
});

// Test that depends on other tests
it('should do B after A', () => {
  // Depends on the state of the previous test
});
```

### DO:

```typescript
// Test first, implement later
it('should return X when Y', () => { ... });
function feature() { ... }

// Test that tests behavior
it('should return valid user', () => {
  expect(result.email).toBe('test@example.com');
});

// Independent test
beforeEach(() => { /* clean setup */ });
it('should do B', () => { ... });
```

## Outputs

- Tests in `*.test.ts` or `*.spec.ts`
- Code in corresponding files
- Incremental commits following the standard