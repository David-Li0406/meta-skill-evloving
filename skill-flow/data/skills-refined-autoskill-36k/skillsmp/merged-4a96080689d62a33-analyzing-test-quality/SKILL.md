---
name: analyzing-test-quality
description: Use this skill to audit test quality with SRE-level scrutiny, identifying tautological tests, coverage gaming, weak assertions, and missing corner cases. It creates a structured improvement plan with tasks for enhancing test effectiveness.
---

# Testing Quality Analysis

## Overview

Audit test suites for real effectiveness, not vanity metrics. Identify tests that provide false confidence (tautological, mock-testing, line hitters) and missing corner cases. Create tasks for improvements.

**Core principle:** Tests must catch bugs, not inflate coverage metrics.

**CRITICAL MINDSET:** Assume tests were written by junior engineers optimizing for coverage metrics. Default to skeptical—a test is RED or YELLOW until proven GREEN.

**Announcement at start:** "I'm using analyzing-test-quality to audit these tests with SRE-level scrutiny."

## Rigidity Level

MEDIUM FREEDOM - Follow the analysis phases exactly. Categorization criteria (RED/YELLOW/GREEN) are rigid. Corner case discovery adapts to the specific codebase.

## Quick Reference

| Phase | Action | Output |
|-------|--------|--------|
| 1. Inventory | List all test files and functions | Test catalog |
| 2. Read Production Code | Read the actual code each test claims to test | Context for analysis |
| 3. Trace Call Paths | Verify tests exercise production, not mocks/utilities | Call path verification |
| 4. Categorize (Skeptical) | Apply RED/YELLOW/GREEN - default to harsher rating | Categorized tests |
| 5. Self-Review | Challenge every GREEN - would a senior SRE agree? | Validated categories |
| 6. Corner Cases | Identify missing edge cases per module | Gap analysis |
| 7. Prioritize | Rank by business criticality | Priority matrix |
| 8. Create Tasks | Create epic + tasks for improvements | Tracked improvement plan |

**MANDATORY:** Read production code BEFORE categorizing tests.

**Core Questions for Each Test:**
1. What bug would this catch? (If you can't name one → RED)
2. Does it exercise PRODUCTION code or a mock/test utility? (Mock → RED or YELLOW)
3. Could code break while test passes? (If yes → YELLOW or RED)
4. Meaningful assertion on PRODUCTION output? (`!= nil` or testing fixtures → weak)

## When to Use

**Use this skill when:**
- Production bugs appear despite high test coverage
- Suspecting coverage gaming or tautological tests
- Before major refactoring (ensure tests catch regressions)
- Onboarding to unfamiliar codebase (assess test quality)
- Planning test improvement initiatives

**Don't use when:**
- Writing new tests (use test-driven-development)
- Just need to run tests (use test-runner agent)

## The Process

### Announcement

**Announce:** "I'm using analyzing-test-quality to audit test quality with SRE-level scrutiny."

---

## Phase 1: Test Inventory

Create complete catalog of tests to analyze.

```bash
# Find all test files (adapt pattern to language)
fd "_test.go" .
fd ".test.ts" .
fd "test_*.py" .

# Count tests per module
for dir in internal/*/; do
  count=$(rg -c "func Test" "$dir" 2>/dev/null | wc -l)
  echo "$dir: $count tests"
done
```

---

## Phase 2: Read Production Code First

**MANDATORY:** Before categorizing ANY test, you MUST:

1. **Read the production code** the test claims to exercise
2. **Understand what the production code actually does**
3. **Trace the test's call path** to verify it reaches production code

**Why this matters:** Junior engineers commonly:
- Create test utilities and test THOSE instead of production code
- Set up mocks that determine the test outcome (mock-testing-mock)
- Write assertions on values defined IN THE TEST, not from production
- Copy patterns from examples without understanding the actual code

**If you haven't read production code, you WILL miscategorize tests as GREEN when they're YELLOW or RED.**

---

## Phase 3: Categorize Each Test (Skeptical Default)

**Assume every test is RED or YELLOW until you have concrete evidence it's GREEN.**

### RED FLAGS - Must Remove or Replace

**Tautological Tests** (pass by definition)

```go
// RED: Verifies non-optional return is not nil
func TestBuilderReturnsValue(t *testing.T) {
    result := NewBuilder().Build()
    assert.NotNil(t, result) // Always passes - return type guarantees this
}
```

**Mock-Testing Tests** (test the mock, not production)

```go
// RED: Only verifies mock was called, not actual behavior
func TestServiceFetchesData(t *testing.T) {
    mockAPI := &MockAPI{}
    mockAPI.On("Fetch").Return([]Data{}, nil)
    service := NewService(mockAPI)
    service.GetData()
    mockAPI.AssertCalled(t, "Fetch") // Tests mock, not service logic
}
```

**Line Hitters** (execute without asserting)

```go
// RED: Calls function, doesn't verify outcome
func TestProcessorRuns(t *testing.T) {
    processor := NewProcessor()
    processor.Run() // No assertion - just verifies no crash
}
```

**Evergreen/Liar Tests** (always pass)

```go
// RED: Catches and ignores exceptions
func TestParserHandlesInput(t *testing.T) {
    defer func() {
        recover() // Swallowed - test passes even on panic
    }()
    parser.Parse(input)
    assert.True(t, true) // Always passes
}
```

### YELLOW FLAGS - Must Strengthen

**Happy Path Only**

```go
// YELLOW: Only tests valid input
func TestParseValidJSON(t *testing.T) {
    result, err := Parse(`{"name": "test"}`)
    assert.NoError(t, err)
    assert.Equal(t, "test", result.Name)
}
// Missing: empty string, malformed JSON, deeply nested, unicode, huge payload
```

**Weak Assertions**

```go
// YELLOW: Assertion too weak
func TestFetchReturnsData(t *testing.T) {
    result, _ := Fetch("/api/users")
    assert.NotNil(t, result)          // Should verify actual content
    assert.Greater(t, len(result), 0) // Should verify exact count or specific items
}
```

### GREEN FLAGS - Exceptional Quality Required

**GREEN is the EXCEPTION, not the rule.** A test is GREEN only if ALL of the following are true:

1. **Exercises actual PRODUCTION code** - Not a mock, not a test utility
2. **Has precise assertions** - Exact values, not `!= nil` or `> 0`
3. **Would fail if production breaks** - You can name the specific bug it catches
4. **Tests behavior, not implementation** - Won't break on valid refactoring

**Before marking ANY test GREEN, you MUST state:**
- "This test exercises [specific production code path]"
- "It would catch [specific bug] because [reason]"
- "The assertion verifies [exact production behavior], not a test fixture"

---

## Phase 4: Mandatory Self-Review

**Before finalizing ANY categorization, complete this checklist:**

For each GREEN test:
- [ ] Did I read the PRODUCTION code this test exercises?
- [ ] Does the test call PRODUCTION code or a test utility/mock?
- [ ] Can I name the SPECIFIC BUG this test would catch?
- [ ] If production code broke, would this test DEFINITELY fail?
- [ ] Am I being too generous because the test "looks reasonable"?

For each YELLOW test:
- [ ] Should this actually be RED? Is there ANY bug-catching value here?
- [ ] Is the weakness fundamental (tests a mock) or fixable (weak assertion)?
- [ ] If I changed this to RED, would I lose any bug-catching ability?

**If you have ANY doubt about a GREEN, downgrade to YELLOW.**
**If you have ANY doubt about a YELLOW, consider RED.**

---

## Phase 5: Corner Case Discovery

For each module, identify missing corner case tests:

### Input Validation Corner Cases

| Category | Examples | Tests to Add |
|----------|----------|--------------|
| Empty values | `""`, `[]`, `{}`, `nil` | test_empty_X_rejected/handled |
| Boundary values | 0, -1, MAX_INT, MAX_LEN | test_boundary_X_handled |
| Unicode | RTL, emoji, combining chars, null byte | test_unicode_X_preserved |
| Injection | SQL: `'; DROP`, XSS: `<script>`, cmd: `; rm` | test_injection_X_escaped |
| Malformed | truncated JSON, invalid UTF-8, wrong type | test_malformed_X_error |

### State Corner Cases

| Category | Examples | Tests to Add |
|----------|----------|--------------|
| Uninitialized | Use before init, double init | test_uninitialized_X_error |
| Already closed | Use after close, double close | test_closed_X_error |
| Concurrent | Parallel writes, read during write | test_concurrent_X_safe |
| Re-entrant | Callback calls same method | test_reentrant_X_safe |

### Integration Corner Cases

| Category | Examples | Tests to Add |
|----------|----------|--------------|
| Network | timeout, connection refused, DNS fail | test_network_X_timeout |
| Partial response | truncated, corrupted, slow | test_partial_response_handled |
| Rate limiting | 429, quota exceeded | test_rate_limit_handled |
| Service errors | 500, 503, malformed response | test_service_error_handled |

---

## Phase 6: Prioritize by Business Impact

| Priority | Criteria | Action Timeline |
|----------|----------|-----------------|
| P0 - Critical | Auth, payments, data integrity | This sprint |
| P1 - High | Core business logic, user-facing features | Next sprint |
| P2 - Medium | Internal tools, admin features | Backlog |
| P3 - Low | Utilities, non-critical paths | As time permits |

---

## Phase 7: Create Tasks for Improvements

**Create epic:**

```
TaskCreate
  subject: "Epic: Test Quality Improvement"
  description: |
    ## Goal
    Improve test effectiveness by removing tautological tests, strengthening weak tests,
    and adding missing corner case coverage.

    ## Requirements (IMMUTABLE)
    - All RED tests removed or replaced with meaningful tests
    - All YELLOW tests strengthened with proper assertions
    - All P0 missing corner cases covered

    ## Success Criteria
    - [ ] No tautological tests remain
    - [ ] All tests verify production behavior, not mock behavior
    - [ ] P0 modules have edge case coverage
    - [ ] Tests document what bug they catch

    ## Anti-patterns (FORBIDDEN)
    - Adding tests that only check `!= nil`
    - Adding tests that verify mock behavior
    - Adding happy-path-only tests
    - Leaving tautological tests "for coverage"
  activeForm: "Planning test quality improvement"
```

**Create subtasks:**

```
TaskCreate
  subject: "Remove tautological tests from auth module"
  description: |
    ## Tests to Remove
    - auth_test.go:45 - TestUserExists (tautological: verifies non-optional != nil)
    - auth_test.go:67 - TestEnumHasCases (tautological: compiler checks this)

    ## Success Criteria
    - [ ] All listed tests deleted
    - [ ] No new tautological tests introduced
    - [ ] Test suite still passes
    - [ ] Coverage may decrease (this is expected and good)
  activeForm: "Removing tautological tests"
```

```
TaskCreate
  subject: "Add corner case tests for auth validation"
  description: |
    ## Tests to Add
    - test_empty_password_rejected - prevents auth bypass
    - test_unicode_username_preserved - prevents encoding corruption
    - test_concurrent_login_safe - prevents session corruption

    ## Implementation (TDD)
    For each test:
    1. Write failing test first (RED)
    2. Verify test fails for the right reason
    3. Test catches the specific bug listed

    ## Success Criteria
    - [ ] All corner case tests written and passing
    - [ ] Each test documents the bug it catches
    - [ ] No tautological tests added
  activeForm: "Adding auth corner case tests"
```

---

## Output Format

```markdown
# Test Effectiveness Analysis: [Project Name]

## Executive Summary

| Metric | Count | % |
|--------|-------|---|
| Total tests analyzed | N | 100% |
| RED (remove/replace) | N | X% |
| YELLOW (strengthen) | N | X% |
| GREEN (keep) | N | X% |
| Missing corner cases | N | - |

**Overall Assessment:** [CRITICAL / NEEDS WORK / ACCEPTABLE / GOOD]

## Detailed Findings

### RED Tests (Must Remove/Replace)

| Test | File:Line | Problem | Action |
|------|-----------|---------|--------|

### YELLOW Tests (Must Strengthen)

| Test | File:Line | Current | Recommended |
|------|-----------|---------|-------------|

### GREEN Tests (Exemplars)

[List 3-5 tests that exemplify good testing practices]

## Missing Corner Cases by Module

### Module: auth/ - Priority: P0

| Corner Case | Bug Risk | Recommended Test |
|-------------|----------|------------------|

## Tasks Created

| Task ID | Subject | Priority |
|---------|---------|----------|
| [id] | Remove tautological tests from auth | P0 |
| [id] | Strengthen weak assertions in api | P1 |
| [id] | Add corner case tests for auth | P0 |
```

## Anti-patterns

**Don't:**
- Mark tests GREEN because they "look reasonable" (verify call paths)
- Trust test names and comments (code doesn't lie, comments do)
- Give benefit of the doubt (junior engineers don't deserve it)
- Rush categorization (read production code FIRST)
- Mark YELLOW when it's actually RED (if mock determines outcome, it's RED)

**Do:**
- Read production code before categorizing ANY test
- Trace call paths to verify production code is exercised
- Apply skeptical default (RED/YELLOW until proven GREEN)
- Complete self-review checklist for all GREEN classifications
- Create actionable Tasks for improvements

## Verification Checklist

Before completing analysis:

**Analysis Quality (MANDATORY):**
- [ ] Read production code for EVERY test before categorizing
- [ ] Traced call paths to verify tests exercise production, not mocks/utilities
- [ ] Applied skeptical default (assumed RED/YELLOW, required proof for GREEN)
- [ ] Completed self-review checklist for ALL GREEN tests
- [ ] Each GREEN test has explicit justification

**Per module:**
- [ ] All tests categorized (RED/YELLOW/GREEN)
- [ ] RED tests have specific removal/replacement actions
- [ ] YELLOW tests have specific strengthening actions
- [ ] Corner cases identified (empty, unicode, concurrent, error)
- [ ] Priority assigned (P0/P1/P2/P3)

**Task Integration:**
- [ ] Created epic for test quality improvement
- [ ] Created tasks for each category (remove, strengthen, add)
- [ ] Set task dependencies

## Integration

**This skill is called by:**
- User request to audit test quality
- Before major refactoring efforts
- When coverage is high but bugs slip through

**This skill creates:**
- Tasks for removing RED tests
- Tasks for strengthening YELLOW tests
- Tasks for adding missing corner cases

**Workflow:**
```
analyzing-test-quality
    → Analyze tests
    → Create improvement Tasks
executing-plans
    → Implement improvements with TDD
verification
    → Verify improvements complete
```

## The Bottom Line

**Coverage measures execution, not assertion quality.**

A test that passes without catching bugs is worse than no test—it creates false confidence.

Audit ruthlessly. GREEN is the exception.