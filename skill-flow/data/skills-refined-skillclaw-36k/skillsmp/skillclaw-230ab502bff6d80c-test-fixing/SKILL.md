---
name: test-fixing
description: Use this skill when you need to systematically identify and fix all failing tests in a codebase, especially after running a test suite that reports failures.
---

# Test Fixing

Systematically identify and fix all failing tests using smart grouping strategies.

## When to Use

- Explicitly asks to fix tests ("fix these tests", "make tests pass")
- Reports test failures ("tests are failing", "test suite is broken")
- Completes implementation and wants tests passing
- Mentions CI/CD failures due to tests

## Systematic Approach

### 1. Initial Test Run

Run `make test` to identify all failing tests.

Analyze output for:

- Total number of failures
- Error types and patterns
- Affected modules/files

### 2. Smart Error Grouping

Group similar failures by:

- **Error type**: ImportError, AttributeError, AssertionError, etc.
- **Module/file**: Same file causing multiple test failures
- **Root cause**: Missing dependencies, API changes, refactoring impacts

Prioritize groups by:

- Number of affected tests (highest impact first)
- Dependency order (fix infrastructure before functionality)

### 3. Systematic Fixing Process

For each group (starting with highest impact):

1. **Identify root cause**

   - Read relevant code
   - Check recent changes with `git diff`
   - Understand the error pattern

2. **Implement fix**

   - Use Edit tool for code changes
   - Follow project conventions
   - Make minimal, focused changes

3. **Verify fix**

   - Run a subset of tests for this group
   - Use pytest markers or file patterns:
     ```bash
     uv run pytest tests/path/to/test_file.py -v
     uv run pytest -k "pattern" -v
     ```
   - Ensure group passes before moving on

4. **Move to next group**

### 4. Fix Order Strategy

**Infrastructure first:**

- Import errors
- Missing dependencies
- Configuration issues

**Then API changes:**

- Function signature changes
- Module reorganization
- Renamed variables/functions

**Finally, logic issues:**

- Assertion failures
- Business logic bugs
- Edge case handling

### 5. Final Verification

After all groups are fixed:

- Run the complete test suite: `make test`
- Verify no regressions
- Check test coverage remains intact

## Best Practices

- Fix one group at a time
- Run focused tests after each fix
- Use `git diff` to understand recent changes
- Look for patterns in failures
- Don't move to the next group until the current one passes