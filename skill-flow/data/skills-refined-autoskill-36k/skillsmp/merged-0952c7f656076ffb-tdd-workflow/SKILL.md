---
name: tdd-workflow
description: Use this skill to implement the Test-Driven Development (TDD) cycle, ensuring high-quality code through the RED-GREEN-REFACTOR process.
---

# Test-Driven Development (TDD) Workflow

This skill outlines the principles and practices of Test-Driven Development (TDD), emphasizing the RED-GREEN-REFACTOR cycle.

## Purpose

Ensure all code changes are made following TDD principles, resulting in well-tested, maintainable code.

## When to Use

- Starting a new complex feature
- Fixing a bug (write a test to reproduce first)
- Refactoring existing code
- Designing APIs

## The TDD Cycle

```
🔴 RED → Write a failing test
    ↓
🟢 GREEN → Write minimal code to pass
    ↓
🔵 REFACTOR → Improve code quality
    ↓
   Repeat...
```

## TDD Phases

### Phase 1: RED (Write Failing Test)

**Objective:** Create a test that reproduces the bug and fails.

1. **Identify Test Location**
   - Find existing test file or create a new one following project conventions.

2. **Write Test Case**
   ```typescript
   // Example: Testing null check for user session
   describe('AuthService', () => {
     it('should handle expired session gracefully', () => {
       const auth = new AuthService();
       const expiredSession = { user: undefined };
       expect(() => auth.getCurrentUser(expiredSession)).not.toThrow();
       expect(auth.getCurrentUser(expiredSession)).toBeNull();
     });
   });
   ```

3. **Run Tests - Verify Failure**
   ```bash
   npm test  # or appropriate test command
   ```
   ⚠️ **The test MUST fail** - if it passes, the bug isn't reproduced correctly.

4. **Commit Test**
   ```bash
   git add <test-files>
   git commit -m "test: add test for [bug description]"
   ```

### Phase 2: GREEN (Implement Fix)

**Objective:** Write the minimum code to make the test pass.

1. **Implement Minimal Fix**
   ```typescript
   getCurrentUser(session: Session): User | null {
     if (!session.user) {
       return null;
     }
     return session.user.id;
   }
   ```

2. **Run Tests - Verify Passing**
   ```bash
   npm test
   ```
   ✅ **All tests MUST pass** - new test and existing tests.

3. **Commit Fix**
   ```bash
   git add <source-files>
   git commit -m "fix: [description] ([issue-key])"
   ```

### Phase 3: REFACTOR (Optional)

**Objective:** Clean up code while keeping tests green.

1. **Identify Improvements**
   - Remove duplication, improve naming, extract methods, simplify logic.

2. **Refactor in Small Steps**
   - Make one change at a time, run tests after each change.

3. **Commit Refactoring** (if significant)
   ```bash
   git add <files>
   git commit -m "refactor: [description]"
   ```

## Verification Checklist

Before completing the TDD cycle:

- [ ] New test(s) written and passing
- [ ] All existing tests still pass
- [ ] Code follows project patterns
- [ ] No linting errors
- [ ] Commits use conventional format

## Common Patterns

### Testing for Exceptions
```typescript
it('should throw on invalid input', () => {
  expect(() => validateEmail('')).toThrow('Email required');
});
```

### Testing Async Code
```typescript
it('should fetch user data', async () => {
  const user = await userService.fetch('123');
  expect(user.name).toBe('John');
});
```

### Testing Edge Cases
```typescript
it('should handle null input', () => { /* ... */ });
it('should handle empty array', () => { /* ... */ });
it('should handle max value', () => { /* ... */ });
```

## Important Principles

- **NEVER skip the RED phase** - always start with a failing test.
- **Keep changes minimal** in the GREEN phase.
- **Run tests frequently** - after every change.
- **If stuck, ask for help** - don't force incorrect code.
- **Tests are documentation** - make them readable.

## TDD Best Practices

- Use the Arrange-Act-Assert (AAA) structure in every test.
- Write only enough code to make the test pass (YAGNI principle).
- Focus on behavior, not implementation details.

## Conclusion

TDD is a powerful methodology that enhances code quality and maintainability. By following the RED-GREEN-REFACTOR cycle, developers can ensure that their code is well-tested and robust.