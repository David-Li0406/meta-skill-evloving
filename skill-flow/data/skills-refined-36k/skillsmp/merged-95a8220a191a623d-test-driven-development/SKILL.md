---
name: test-driven-development
description: Use this skill when implementing features, fixing bugs, or refactoring code by following the Red-Green-Refactor cycle.
---

# Test-Driven Development (TDD)

## Core Principle

Write tests BEFORE writing implementation code. Follow the RED → GREEN → REFACTOR cycle.

## When to Use This Skill

- Adding new features
- Fixing bugs
- Refactoring existing code
- User requests new functionality
- Implementing planned tasks

## The Iron Law

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

Writing tests after code is NOT TDD. It's test-after-development (TAD) and misses TDD's benefits.

## Why TDD?

**Benefits:**
- Catches bugs early (before they exist)
- Forces you to think through design
- Creates better APIs (you're the first user)
- Provides a safety net for refactoring
- Documentation through examples
- Higher confidence in changes

**Without TDD:**
- "It works on my machine" syndrome
- Fear of refactoring (might break things)
- Bugs discovered in production
- Unclear requirements until you code
- No safety net

## The RED → GREEN → REFACTOR Cycle

### 🔴 RED: Write a Failing Test

1. Think about what you want the code to do.
2. Write a test that describes that behavior.
3. Run the test - it MUST fail.
4. Confirm it fails for the RIGHT reason.

**Why it must fail first:**
- Proves the test actually tests something.
- Confirms test setup is correct.
- Verifies you're testing the right thing.

### 🟢 GREEN: Make the Test Pass

1. Write the MINIMAL code to make the test pass.
2. Don't worry about perfect code yet.
3. Hardcoding is okay at this stage.
4. Just make it green.

**Why minimal:**
- Keeps you focused.
- Prevents over-engineering.
- Faster feedback loop.

### 🔵 REFACTOR: Improve the Code

1. Now that the test passes, improve the code.
2. Remove duplication.
3. Improve naming.
4. Optimize if needed.
5. Keep tests passing.

**Why separate refactoring:**
- Tests provide a safety net.
- Can't break functionality if tests pass.
- Cleaner code without fear.

## TDD Protocol

### Step 1: Announce TDD Usage

```
I'm using the test-driven-development skill to implement this feature.

Following RED → GREEN → REFACTOR cycle.
```

### Step 2: RED - Write Failing Test

Write a minimal test showing what should happen. For example:

```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

### Step 3: GREEN - Make Test Pass

Write the simplest code to pass the test. For example:

```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```

### Step 4: REFACTOR - Clean Up

After green only:
- Remove duplication.
- Improve names.
- Extract helpers.

Keep tests green. Don't add behavior.

## TDD Best Practices

### Test Naming

**Good names:**
- `test_user_can_register_with_valid_data`
- `test_registration_fails_with_invalid_email`

**Bad names:**
- `test_auth` (too vague)
- `test_1` (meaningless)

### Test Independence

Each test should be completely independent. Avoid shared state between tests.

## TDD Anti-Patterns to Avoid

- Writing Tests After Code
- Testing Implementation Details
- Making Tests Pass Too Quickly

## Verification Checklist

Before marking work complete:
- [ ] Every new function has a test.
- [ ] Watched each test fail before implementing.
- [ ] Wrote minimal code to pass each test.
- [ ] All tests pass.
- [ ] Output pristine (no errors, warnings).

## Authority

This skill is based on:
- Kent Beck's Test-Driven Development by Example
- Industry best practice: TDD proven to reduce bugs by 40-80%
- Professional standard: Used by major tech companies.

## Your Commitment

When implementing features:
- [ ] I will write tests BEFORE code.
- [ ] I will follow RED → GREEN → REFACTOR.
- [ ] I will see tests fail before making them pass.
- [ ] I will refactor while keeping tests green.

---

**Bottom Line**: TDD seems slower at first but is actually faster. Tests catch bugs immediately, not in production. Write tests first, always.