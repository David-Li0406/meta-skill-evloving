---
name: tdd-workflow
description: Execute RED-GREEN-REFACTOR test-driven development cycle
---

# TDD Workflow Skill

This skill implements the Test-Driven Development (TDD) cycle: RED → GREEN → REFACTOR.

## Purpose

Ensure all fixes are implemented following TDD principles, resulting in well-tested, high-quality code.

## When to Use

- Implementing any bug fix
- Adding new functionality
- Modifying existing behavior

## The TDD Cycle

```
    ┌─────────┐
    │   RED   │ Write a failing test
    └────┬────┘
         │
    ┌────▼────┐
    │  GREEN  │ Write minimal code to pass
    └────┬────┘
         │
    ┌────▼────┐
    │REFACTOR │ Clean up (optional)
    └────┬────┘
         │
         └────► Repeat if needed
```

## Process

### Phase 1: RED (Write Failing Test)

**Objective:** Create a test that reproduces the bug and fails.

1. **Identify Test Location**
   - Find existing test file OR
   - Create new test file following project conventions
   - Examples: `*.test.ts`, `*.spec.js`, `test_*.py`

2. **Write Test Case**
   ```typescript
   // Example: Testing null check for user session
   describe('AuthService', () => {
     it('should handle expired session gracefully', () => {
       const auth = new AuthService();
       const expiredSession = { user: undefined };
       
       // This should NOT throw an error
       expect(() => auth.getCurrentUser(expiredSession)).not.toThrow();
       expect(auth.getCurrentUser(expiredSession)).toBeNull();
     });
   });
   ```

3. **Run Tests - Verify Failure**
   ```bash
   npm test  # or pytest, jest, etc.
   ```
   
   ⚠️ **The test MUST fail** - if it passes, the bug isn't reproduced correctly

4. **Commit Test**
   ```bash
   git add <test-files>
   git commit -m "test: add test for [bug description]"
   ```

### Phase 2: GREEN (Implement Fix)

**Objective:** Write the minimum code to make the test pass.

1. **Implement Minimal Fix**
   ```typescript
   // Before
   getCurrentUser(session: Session): User {
     return session.user.id;  // Crashes on undefined
   }
   
   // After (minimal fix)
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
   
   ✅ **All tests MUST pass** - new test and existing tests

3. **Commit Fix**
   ```bash
   git add <source-files>
   git commit -m "fix: [description] ([issue-key])"
   ```

### Phase 3: REFACTOR (Optional)

**Objective:** Clean up code while keeping tests green.

1. **Identify Improvements**
   - Remove duplication
   - Improve naming
   - Extract methods/functions
   - Simplify logic

2. **Refactor in Small Steps**
   - Make one change at a time
   - Run tests after each change
   - Ensure all tests still pass

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

## Output Format

```json
{
  "phase": "red|green|refactor|complete",
  "test_results": {
    "new_tests": 2,
    "total_tests": 150,
    "passed": 150,
    "failed": 0
  },
  "commits": [
    {
      "phase": "red",
      "sha": "abc123",
      "message": "test: add test for expired session handling"
    },
    {
      "phase": "green",
      "sha": "def456",
      "message": "fix: add null check for user session (PROJ-123)"
    }
  ],
  "status": "success|failed",
  "errors": []
}
```

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

## Error Handling

| Situation | Action |
|-----------|--------|
| Can't find test file location | Follow project conventions or create new |
| Existing tests fail | Fix the root cause, don't skip tests |
| Tests pass on RED phase | Test isn't reproducing the bug correctly |
| Tests fail on GREEN phase | Fix is incomplete or incorrect |

## Important

- **NEVER skip the RED phase** - always start with a failing test
- **Keep changes minimal** in GREEN phase
- **Run tests frequently** - after every change
- **If stuck, ask for help** - don't force incorrect code
- **Tests are documentation** - make them readable
