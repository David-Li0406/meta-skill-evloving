# TDD Debugging Workflow

Bug found? Never fix without a test. The test proves the fix and prevents regression.

## The Workflow

```
BUG FOUND → REPRODUCE IN TEST → WATCH FAIL → FIX → WATCH PASS → DONE
```

## Step 1: Capture the Bug

Before touching any code, document the bug precisely:

```markdown
**Bug:** [What's broken]
**Steps to reproduce:** [How to trigger]
**Expected:** [What should happen]
**Actual:** [What happens instead]
**Error/Stack:** [Any error messages or stack traces]
```

Example:
```markdown
**Bug:** Empty email accepted in signup form
**Steps:** Submit form with email=""
**Expected:** Error "Email required"
**Actual:** Form submits, creates invalid user
**Error:** None (silent failure)
```

## Step 2: Write Failing Test

Translate the bug into a test that fails the same way.

### Test Structure

```typescript
test('describes the expected behavior that is currently broken', async () => {
  // ARRANGE: Set up conditions that trigger the bug
  const input = /* buggy input */;

  // ACT: Execute the code path
  const result = await functionUnderTest(input);

  // ASSERT: Verify the expected (correct) behavior
  expect(result).toBe(/* what SHOULD happen */);
});
```

### Example: Empty Email Bug

```typescript
test('rejects empty email with validation error', async () => {
  // ARRANGE
  const formData = { email: '', password: 'valid123' };

  // ACT
  const result = await submitSignupForm(formData);

  // ASSERT
  expect(result.success).toBe(false);
  expect(result.error).toBe('Email required');
});
```

### Common Bug Categories

| Bug Type | Test Focus |
|----------|------------|
| Validation bypass | Test with invalid input, assert rejection |
| Null/undefined handling | Test with missing data, assert graceful handling |
| Race condition | Test concurrent operations, assert consistency |
| Off-by-one | Test boundary values, assert correct bounds |
| State corruption | Test state after operations, assert integrity |
| Error swallowing | Test error path, assert error surfaces |

## Step 3: Verify RED

**MANDATORY. Never skip.**

Run the test and confirm it fails:

```bash
npm test path/to/test.test.ts
```

### Checklist

- [ ] Test fails (not errors on syntax/import)
- [ ] Failure message matches expected behavior
- [ ] Failure reproduces the actual bug

### If Test Passes Immediately

You either:
1. **Wrote wrong test** - Test doesn't trigger the bug
2. **Bug already fixed** - Someone else fixed it
3. **Testing wrong code path** - Bug is elsewhere

**Action:** Don't proceed. Investigate why test passes when bug exists.

### If Test Errors (Not Fails)

Fix the error first:
- Import issues
- Type errors
- Setup problems

Then re-run until you get a proper failure.

## Step 4: Fix the Bug

Write minimal code to make the test pass.

### The Fix

```typescript
// BEFORE (buggy)
function submitSignupForm(data: FormData) {
  return createUser(data.email, data.password);
}

// AFTER (fixed)
function submitSignupForm(data: FormData) {
  if (!data.email?.trim()) {
    return { success: false, error: 'Email required' };
  }
  return createUser(data.email, data.password);
}
```

### Rules

- **Minimal change** - Fix only what's needed
- **No refactoring** - That's a separate step
- **No "while I'm here"** - Stay focused on the bug

## Step 5: Verify GREEN

Run test again:

```bash
npm test path/to/test.test.ts
```

### Checklist

- [ ] Bug test passes
- [ ] All other tests still pass
- [ ] No warnings or errors in output

### If Other Tests Fail

Fix them now. The bug fix may have exposed other issues:
- Related bugs
- Tests that depended on buggy behavior
- Integration points affected

## Step 6: Refactor (Optional)

Only after green:
- Clean up the fix
- Extract helpers if needed
- Improve names

Keep tests green. Don't add behavior.

## Edge Case Discovery

One bug often reveals others. After fixing, ask:

| Question | Action |
|----------|--------|
| Other invalid inputs? | Add tests for: null, undefined, whitespace, special chars |
| Boundary conditions? | Add tests for: empty arrays, max values, zero |
| Related code paths? | Check similar validation/handling elsewhere |
| Error messages? | Verify all error paths have useful messages |

### Example Expansion

```typescript
// Original bug test
test('rejects empty email', ...);

// Discovered edge cases
test('rejects whitespace-only email', async () => {
  const result = await submitSignupForm({ email: '   ', password: 'valid' });
  expect(result.error).toBe('Email required');
});

test('rejects null email', async () => {
  const result = await submitSignupForm({ email: null, password: 'valid' });
  expect(result.error).toBe('Email required');
});
```

## Integration with Debugging Skills

When a debugging skill identifies a bug:

1. **Pause debugging** - Don't fix in debug session
2. **Document bug** - Capture reproduction steps
3. **Write test first** - Use this workflow
4. **Verify fix** - Test proves fix works
5. **Return to debugging** - Continue if more bugs exist

### Referencing from Debugging Skills

Other skills can reference this workflow:

```markdown
## When Bug is Found

Before fixing, follow the TDD debugging workflow:
See: test-driven-development/references/debugging-workflow.md

1. Capture the bug precisely
2. Write failing test that reproduces it
3. Verify test fails correctly
4. Fix with minimal code
5. Verify test passes
6. Check for edge cases
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Fix first, test later | Test passes immediately, proves nothing | Delete fix, write test, then fix |
| Test passes on first run | Not testing the bug | Debug why test doesn't trigger bug |
| Skip verify RED | Can't prove test catches bug | Always watch fail first |
| Over-fix | Introduces new bugs | Minimal change only |
| No edge cases | Related bugs remain | Ask "what else could break?" |

## Quick Reference

```
1. CAPTURE: Document bug (what, steps, expected, actual)
2. TEST: Write failing test that reproduces bug
3. VERIFY RED: Run test, confirm correct failure
4. FIX: Minimal code to pass test
5. VERIFY GREEN: Run test, confirm pass + no regressions
6. EXPAND: Check edge cases, add more tests if needed
```

**Never fix a bug without a failing test first.**
