---
name: test-driven-development
description: "Use when implementing any feature, bugfix, or code change. Invoke BEFORE writing implementation code. The Iron Law - no production code without a failing test first."
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**The Iron Law:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST

**Violating the letter of the rules IS violating the spirit of the rules.**

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

Thinking "skip TDD just this once"? Stop. That's rationalization.

## Red-Green-Refactor Cycle

```
RED: Write failing test
  |
  v
VERIFY RED: Confirm fails correctly (not errors, not typos)
  |
  v
GREEN: Write minimal code to pass
  |
  v
VERIFY GREEN: Confirm all tests pass
  |
  v
REFACTOR: Clean up (stay green)
  |
  v
REPEAT: Next failing test
```

### RED - Write Failing Test

Write one minimal test showing what should happen.

**Good Example:**
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
Clear name, tests real behavior, one thing.

**Bad Example:**
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```
Vague name, tests mock behavior not real code.

**Requirements:**
- One behavior per test
- Clear, descriptive name
- Real code (no mocks unless unavoidable)

### VERIFY RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
npm test path/to/test.test.ts
# or: pytest test_file.py::test_name
# or: go test -run TestName
```

Confirm:
- Test FAILS (not errors)
- Failure message is expected
- Fails because feature is missing (not typos)

**Test passes?** You're testing existing behavior. Fix the test.

**Test errors?** Fix error, re-run until it fails correctly.

### GREEN - Write Minimal Code

Write the simplest code to pass the test. Nothing more.

**Good Example:**
```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```
Just enough to pass.

**Bad Example:**
```typescript
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
  }
): Promise<T> {
  // YAGNI - You Ain't Gonna Need It
}
```
Over-engineered. Don't add features not required by tests.

### VERIFY GREEN - Watch It Pass

**MANDATORY.**

```bash
npm test path/to/test.test.ts
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

**Test fails?** Fix code, not test.

**Other tests fail?** Fix now.

### REFACTOR - Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

## Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | One thing. "and" in name? Split it. | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes behavior | `test('test1')` |
| **Shows intent** | Demonstrates desired API | Obscures what code should do |
| **Real code** | Tests actual implementation | Tests mock behavior |

## Common Rationalizations (And Why They're Wrong)

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc is not systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to the test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD is faster than debugging. Pragmatic = test-first. |
| "Manual test is faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for existing code you touch. |
| "TDD is dogmatic" | TDD IS pragmatic: finds bugs before commit, prevents regressions. |

## Red Flags - STOP and Start Over

If you find yourself:
- Writing code before test
- Writing test after implementation
- Test passes immediately (no red phase)
- Can't explain why test failed
- Adding tests "later"
- Rationalizing "just this once"
- Saying "I already manually tested it"
- Saying "Tests after achieve the same purpose"
- Saying "It's about spirit not ritual"
- Keeping code as "reference" to adapt
- Saying "Already spent X hours, deleting is wasteful"
- Saying "TDD is dogmatic, I'm being pragmatic"
- Saying "This is different because..."

**All of these mean: Delete the code. Start over with TDD.**

## Example: Bug Fix

**Bug:** Empty email accepted

**RED**
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Verify RED**
```bash
$ npm test
FAIL: expected 'Email required', got undefined
```

**GREEN**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...existing code
}
```

**Verify GREEN**
```bash
$ npm test
PASS
```

**REFACTOR**
Extract validation for multiple fields if needed.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Debugging Integration

Bug found? Write a failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.

**Never fix bugs without a test.**

## Testing Anti-Patterns

Avoid these common mistakes:

1. **Testing mock behavior** - Test real components, not mock existence
2. **Test-only methods in production** - Put cleanup methods in test utilities
3. **Mocking without understanding** - Know side effects before mocking
4. **Incomplete mocks** - Mirror real API structure completely
5. **Over-complex mocks** - Consider integration tests instead

**The Iron Laws:**
- NEVER test mock behavior
- NEVER add test-only methods to production classes
- NEVER mock without understanding dependencies

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

**Can't check all boxes? You skipped TDD. Start over.**

## The Bottom Line

```
Production code -> test exists and failed first
Otherwise -> not TDD
```

No exceptions without your human partner's explicit permission.

## Integration

**Always loaded:** This is a Process skill, loaded at session start.

**Pairs with:**
- **verification** - Verify tests pass before claiming complete
- **debug** - TDD approach to bug fixes
- **subagent-driven-development** - Sub-agents follow TDD
