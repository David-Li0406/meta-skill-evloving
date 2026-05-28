---
name: test-driven-development
description: Use when implementing features or fixing bugs - enforces RED-GREEN-REFACTOR cycle requiring tests to fail before writing code
---

# Test-Driven Development

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Announce at start:** "I'm using gambit:test-driven-development to implement this with the RED-GREEN-REFACTOR cycle."

## Rigidity Level

LOW FREEDOM - Follow these exact steps in order. Do not adapt.

Violating the letter of the rules is violating the spirit of the rules.

## Quick Reference

| Phase | Action | Command Example | Expected Result |
|-------|--------|-----------------|-----------------|
| **RED** | Write failing test | `go test ./...` | FAIL (feature missing) |
| **Verify RED** | Confirm correct failure | Check error message | "function not found" or assertion fails |
| **GREEN** | Write minimal code | Implement feature | Test passes |
| **Verify GREEN** | All tests pass | `go test ./...` | All green, no warnings |
| **REFACTOR** | Clean up code | Improve while green | Tests still pass |
| **COMMIT** | Commit increment | `git commit` | Behavior captured |

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring with behavior changes
- Any production code

**Exceptions (ask your human partner):**
- Throwaway prototypes (will be deleted)
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Process

### 1. RED - Write Failing Test

Write one minimal test showing what should happen.

**Good example:**
```go
func TestRetryOperation_RetriesThreeTimes(t *testing.T) {
    attempts := 0
    operation := func() error {
        attempts++
        if attempts < 3 {
            return errors.New("fail")
        }
        return nil
    }

    err := RetryOperation(operation)

    assert.NoError(t, err)
    assert.Equal(t, 3, attempts)
}
```

**Bad example:**
```go
func TestRetry(t *testing.T) {
    mock := &MockOperation{}
    mock.On("Do").Return(nil)
    RetryOperation(mock.Do)
    mock.AssertCalled(t, "Do")
}
```
Vague name, tests mock not code.

**Requirements:**
- Test one behavior only ("and" in name? Split it)
- Clear name describing behavior
- Use real code (no mocks unless unavoidable)

### 2. Verify RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
go test ./path/to/package -run TestName
```

Confirm:
- Test **fails** (not errors with syntax issues)
- Failure message is expected ("function not found" or assertion fails)
- Fails because feature missing (not typos)

**If test passes:** You're testing existing behavior. Fix the test.
**If test errors:** Fix syntax error, re-run until it fails correctly.

### 3. GREEN - Write Minimal Code

Write simplest code to pass the test. Nothing more.

**Good example:**
```go
func RetryOperation(fn func() error) error {
    var lastErr error
    for i := 0; i < 3; i++ {
        if err := fn(); err != nil {
            lastErr = err
            continue
        }
        return nil
    }
    return lastErr
}
```

**Bad example (YAGNI):**
```go
func RetryOperation(fn func() error, opts ...RetryOption) error {
    config := &RetryConfig{
        MaxRetries: 3,
        Backoff:    ExponentialBackoff,
        OnRetry:    nil,
    }
    // Don't add features the test doesn't require!
}
```

Don't add features, refactor other code, or "improve" beyond the test.

### 4. Verify GREEN - Watch It Pass

**MANDATORY.**

```bash
go test ./path/to/package -run TestName
```

Confirm:
- New test passes
- All other tests still pass
- No errors or warnings

**If test fails:** Fix code, not test.
**If other tests fail:** Fix now before proceeding.

### 5. REFACTOR - Clean Up

**Only after green:**
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

### 6. Commit

After green, commit the increment:

```bash
git add path/to/test.go path/to/implementation.go
git commit -m "feat(module): add retry operation with 3 attempts"
```

**Commit message should describe the behavior, not the test.**

### 7. Repeat

Next failing test for next feature.

## Workflow Checklists

### For Each New Feature

- [ ] Write one failing test (RED)
- [ ] Run test, confirm it fails correctly (expected reason)
- [ ] Write minimal code to pass (GREEN)
- [ ] Run test, confirm it passes
- [ ] Run ALL tests, confirm no regressions
- [ ] Refactor if needed (staying green)
- [ ] Commit

### For Each Bug Fix

- [ ] Write test reproducing the bug (RED)
- [ ] Run test, confirm it fails (reproduces bug)
- [ ] Fix the bug (minimal change)
- [ ] Run test, confirm it passes (bug fixed)
- [ ] Run ALL tests, confirm no regressions
- [ ] Commit

### For Each Refactoring

- [ ] Confirm tests exist and pass BEFORE refactoring
- [ ] Make one small refactoring change
- [ ] Run tests, confirm still green
- [ ] Repeat until refactoring complete
- [ ] Commit

## Why Order Matters

**"I'll write tests after to verify it works"**

Tests written after code pass immediately. Passing immediately proves nothing:
- Might test wrong thing
- Might test implementation, not behavior
- Might miss edge cases you forgot
- You never saw it catch the bug

Test-first forces you to see the test fail, proving it actually tests something.

**"I already manually tested all the edge cases"**

Manual testing is ad-hoc. You think you tested everything but:
- No record of what you tested
- Can't re-run when code changes
- Easy to forget cases under pressure
- "It worked when I tried it" ≠ comprehensive

Automated tests are systematic. They run the same way every time.

**"Deleting X hours of work is wasteful"**

Sunk cost fallacy. The time is already gone. Your choice now:
- Delete and rewrite with TDD (X more hours, high confidence)
- Keep it and add tests after (30 min, low confidence, likely bugs)

The "waste" is keeping code you can't trust.

**"TDD is dogmatic, being pragmatic means adapting"**

TDD IS pragmatic:
- Finds bugs before commit (faster than debugging after)
- Prevents regressions (tests catch breaks immediately)
- Documents behavior (tests show how to use code)
- Enables refactoring (change freely, tests catch breaks)

"Pragmatic" shortcuts = debugging in production = slower.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for existing code. |

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

## Testing Anti-Patterns

When adding mocks or test utilities, avoid these patterns:

### Never Test Mock Behavior

```go
// BAD: Testing that mock exists
func TestHandler(t *testing.T) {
    mock := &MockService{}
    handler := NewHandler(mock)
    assert.NotNil(t, handler.service) // Tests mock, not behavior
}

// GOOD: Test real behavior
func TestHandler_ProcessesRequest(t *testing.T) {
    service := NewTestService()
    handler := NewHandler(service)
    result, err := handler.Process("data")
    assert.NoError(t, err)
    assert.Equal(t, expected, result)
}
```

### Never Add Test-Only Methods to Production

```go
// BAD: Reset() only used in tests
type Connection struct { pool *Pool }
func (c *Connection) Reset() { c.pool.Clear() } // Dangerous in production!

// GOOD: Test utilities handle cleanup
// test_utils.go
func CleanupConnection(c *Connection) {
    c.pool.ClearTestData()
}
```

### Never Mock Without Understanding

Before mocking any method:
1. Ask: "What side effects does the real method have?"
2. Ask: "Does this test depend on any of those side effects?"
3. If depends on side effects: Mock at lower level, not this method

## Example: Bug Fix with TDD

**Bug:** Empty email accepted when it should be rejected.

**RED:**
```go
func TestSubmitForm_RejectsEmptyEmail(t *testing.T) {
    result := SubmitForm(FormData{Email: ""})
    assert.Equal(t, "Email required", result.Error)
}
```

**Verify RED:**
```bash
$ go test ./... -run TestSubmitForm_RejectsEmptyEmail
FAIL: expected "Email required", got ""
```

**GREEN:**
```go
func SubmitForm(data FormData) FormResult {
    if strings.TrimSpace(data.Email) == "" {
        return FormResult{Error: "Email required"}
    }
    // ... rest of form processing
    return FormResult{}
}
```

**Verify GREEN:**
```bash
$ go test ./... -run TestSubmitForm_RejectsEmptyEmail
PASS
```

**REFACTOR:** Extract validation if multiple fields need it.

## Language-Specific Commands

### Go
```bash
go test ./...                           # All tests
go test ./path/to/package -run TestName # Single test
go test ./... -v                        # Verbose output
go test ./... -cover                    # With coverage
```

### TypeScript (Vitest)
```bash
npm test                               # All tests
npm test -- -t "test name"             # Single test
npm test -- --coverage                 # With coverage
```

### Rust
```bash
cargo test                             # All tests
cargo test test_name                   # Single test
cargo test -- --nocapture              # With output
```

### Python
```bash
pytest                                 # All tests
pytest -k "test_name"                  # Single test
pytest --cov                           # With coverage
```

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test **fail** before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass with no warnings
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered
- [ ] No test-only methods added to production classes

**Can't check all boxes?** You skipped TDD. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Integration

**This skill is called by:**
- `gambit:executing-plans` (when implementing tasks)
- `gambit:fixing-bugs` (write failing test reproducing bug)

**This skill calls:**
- `gambit:verification` (running tests to verify)
- test-runner agent (run tests, return summary only)

**Workflow:**
```
Write failing test (RED)
    → Verify it fails for right reason
    → Write minimal code (GREEN)
    → Verify all tests pass
    → Refactor (stay green)
    → Commit
    → Next test
```

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without your human partner's permission.
