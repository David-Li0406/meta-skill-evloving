---
name: bug-report
description: |
  Streamlined bug fixing workflow that creates GitHub issues, writes reproducible tests, finds fixes, and commits changes.
  Use when a user reports a bug and wants to: (1) Create a GitHub issue, (2) Write a test that reproduces the bug,
  (3) Find and implement a fix (with user iteration), (4) Commit with the issue number.
  Triggers: "fix this bug", "there's a bug", "I found an issue", "bug report", "something's broken", etc.
---

# Bug Report Skill

Streamlined workflow to handle bug reports from discovery through resolution and commit.

## Workflow

1. **Create Issue** - Create GitHub issue from bug description
2. **Reproduce** - Write test that reproduces the bug
3. **Investigate** - Understand root cause
4. **Fix** - Implement fix and validate test passes
5. **Iterate** - Collaborate with user on fix if needed
6. **Commit** - Commit with issue number reference

## Step 1: Create GitHub Issue

Use `gh issue create` to create the issue with a clear title and description:

```bash
gh issue create \
  --title "Bug: [brief description]" \
  --body "[Full bug description, reproduction steps, expected vs actual behavior]"
```

The command returns the issue number (e.g., `#123`). Store this for the commit message.

## Step 2: Write Reproducer Test

Create a test that demonstrates the bug:

- **Location**: Add to relevant test file or create new test file in `__tests__/`
- **Pattern**: Test should fail with current code, pass after fix
- **Name**: Include the issue number in test name: `test('should handle X correctly (fixes #123)', ...)`
- **Run**: `npm run test` to verify test fails

Example structure:
```typescript
test('should handle edge case correctly (fixes #123)', () => {
  // Setup that triggers the bug
  const result = functionWithBug(input);

  // Expected behavior
  expect(result).toEqual(expectedValue);
});
```

## Step 3: Investigate Root Cause

Locate the bug:

1. Read the error message from the failing test
2. Use the test to trace through the code
3. Identify where the logic diverges from expected behavior
4. Check for: off-by-one errors, missing validation, type mismatches, logic errors

## Step 4: Implement Fix

Fix the bug and verify:

1. Modify the code to fix the issue
2. Run `npm run test` - reproducer test should now pass
3. Run full test suite to ensure no regressions: `npm run test:run`
4. If working with configs: run `npm run test:configs` to validate

## Step 5: Iterate with User

If fix needs validation or you hit blockers:

- Show the user the proposed fix with context
- Ask for feedback on the approach
- Adjust based on user input
- Re-run tests to confirm fix

## Step 6: Commit

Create commit with issue number:

```bash
git add .
git commit -m "fix: [brief description] (fixes #123)"
```

Include the issue number in parentheses. The full message should explain **why** the fix addresses the issue.

Example: `fix: validate gross_annual input before calculation (fixes #123)`

## Tips

- **Test-Driven**: Always write failing test before implementing fix
- **Single Issue**: Keep fix focused on one bug; if you discover others, create separate issues
- **Verify**: Run all relevant test suites (unit tests, config tests) before committing
- **Clear Messages**: Commit message should explain the problem and why the fix solves it
