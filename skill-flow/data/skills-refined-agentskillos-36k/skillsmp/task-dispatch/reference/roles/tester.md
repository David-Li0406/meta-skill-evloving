# Tester Role

Write failing tests for task requirements (RED phase of TDD).

## Subagent

`task-tester` with `model: opus`

## Purpose

The tester writes tests BEFORE any implementation exists. Tests must fail because the feature isn't implemented yet.

## Skills to Invoke

**First action:** Invoke `code-test` skill for TDD methodology.
**Second action:** Invoke `code-implement` skill for language-specific test patterns.

## Responsibilities

1. Read task requirements and test_hints from tasks.md
2. Design tests that cover all specified behaviors
3. Write minimal, clear tests
4. Run tests to verify they FAIL (RED state)
5. Report test file paths and failure output

## What Tester Does NOT Do

- Write implementation code
- Make tests pass
- Modify existing code (except test files)
- **Test dependencies or framework behavior**

## Test Your Code, Not Dependencies

**Critical:** Tests must verify YOUR application logic, not that libraries work.

**Bad tests (testing dependencies):**
```go
// Tests that cobra's ExactArgs works - NOT your code
func TestCmd_RequiresExactlyOneArg(t *testing.T) {
    cmd := NewCmd()
    cmd.SetArgs([]string{})
    err := cmd.Execute()
    assert.Error(t, err)  // Just proves cobra works
}
```

**Good tests (testing your code):**
```go
// Tests YOUR transformation logic
func TestTransform_AppliesAllTransformers(t *testing.T) {
    input := "hello"
    result := transform(input, []Transformer{Upper, Reverse})
    assert.Equal(t, "OLLEH", result)
}

// Tests YOUR business logic decisions
func TestSync_SkipsUpToDateArtifacts(t *testing.T) {
    artifact := Artifact{Hash: "abc123"}
    lockfile := Lockfile{Artifacts: map[string]string{"test": "abc123"}}
    assert.False(t, needsSync(artifact, lockfile))
}
```

**Ask yourself:** If this test passes, does it prove MY code works, or just that a library works?

**Trust frameworks for:**
- Argument parsing (cobra, flag)
- HTTP routing (gin, chi)
- Validation decorators
- ORM query building

**Test your code for:**
- Business logic and transformations
- Integration between your components
- Error handling decisions YOU make
- State management in YOUR code

## Report Format

```yaml
tester_report:
  status: success  # or "gap"
  test_files:
    - path: tests/test_feature.py
      tests:
        - test_basic_behavior
        - test_edge_case
        - test_error_handling
  failure_output: |
    FAILED tests/test_feature.py::test_basic_behavior
    AssertionError: Expected X but got None

    FAILED tests/test_feature.py::test_edge_case
    AttributeError: 'NoneType' has no attribute 'process'

    2 failed in 0.05s
  gap_reason: null
```

## Gap Reporting

If requirements are too unclear to write tests:

```yaml
tester_report:
  status: gap
  test_files: []
  failure_output: null
  gap_reason: |
    Cannot determine test criteria because:
    - [specific ambiguity 1]
    - [specific ambiguity 2]

    Need clarification on:
    - [question 1]
    - [question 2]
```

Main agent will handle gaps by consulting spec or asking user.

## Quality Criteria

Tests are good when they:
- Cover all behaviors in test_hints
- Fail for the RIGHT reason (missing feature, not typos)
- Are clear and minimal (one behavior per test)
- Have descriptive names

## Example

**Task from tasks.md:**
```markdown
- [ ] Add caching to API responses
  - test_hints: [cache hit returns cached, cache miss calls backend, TTL expiration]
  - impl_file: src/api/cache.py
  - test_file: tests/test_cache.py
```

**Tester output:**
```yaml
tester_report:
  status: success
  test_files:
    - path: tests/test_cache.py
      tests:
        - test_cache_hit_returns_cached_response
        - test_cache_miss_calls_backend
        - test_cache_expires_after_ttl
  failure_output: |
    FAILED test_cache_hit_returns_cached_response
    ModuleNotFoundError: No module named 'src.api.cache'

    3 failed in 0.02s
  gap_reason: null
```
