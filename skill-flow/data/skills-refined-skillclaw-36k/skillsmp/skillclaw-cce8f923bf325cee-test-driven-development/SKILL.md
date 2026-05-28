---
name: test-driven-development
description: Use this skill when implementing any feature or bugfix, before writing implementation code - write the test first, watch it fail, and write minimal code to pass; ensures tests actually verify behavior by requiring failure first.
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask your human partner):**
- Throwaway prototypes
- Generated code
- Configuration files

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If you find yourself writing implementation code before tests, STOP immediately. Delete the implementation and start over with TDD.

## Red-Green-Refactor Cycle

```dot
digraph tdd_cycle {
    rankdir=LR;
    red [label="RED\nWrite failing test", shape=box, style=filled, fillcolor="#ffcccc"];
    verify_red [label="Verify fails\ncorrectly", shape=diamond];
    green [label="GREEN\nMinimal code", shape=box, style=filled, fillcolor="#ccffcc"];
    verify_green [label="Verify passes\nAll green", shape=diamond];
    refactor [label="REFACTOR\nClean up", shape=box, style=filled, fillcolor="#ccccff"];
    next [label="Next", shape=ellipse];

    red -> verify_red;
    verify_red -> green [label="yes"];
    verify_red -> red [label="wrong\nfailure"];
    green -> verify_green;
    verify_green -> refactor [label="yes"];
    verify_green -> green [label="no"];
    refactor -> verify_green [label="stay\ngreen"];
    verify_green -> next;
    next -> red;
}
```

### Steps to Follow

1. **Write a Failing Test (RED phase)**: Create a test that demonstrates the desired behavior.
2. **Verify the Test Fails**: Ensure the test fails due to the behavior of the application, not due to the test itself.
3. **Write Minimal Code (GREEN phase)**: Implement the least amount of code necessary to make the test pass.
4. **Verify the Test Passes**: Confirm that the test now passes due to the behavior of the application.
5. **Refactor the Code**: Clean up the code while ensuring all tests still pass.

### Test Writing Guidelines

- Always test real behavior.
- Avoid writing tests that are just mocks or test implementation details.
- Focus on writing tests for integration boundaries.
- Only unit test utilities; production code must be end-to-end tested.

### Example Test

<Good>
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
</Good>

<Bad>
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock)
```
</Bad>