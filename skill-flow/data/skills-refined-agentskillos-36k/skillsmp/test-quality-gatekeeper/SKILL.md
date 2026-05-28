---
name: test-quality-gatekeeper
description: Assess whether tests actually protect the system from regressions. Use when reviewing test coverage, evaluating test quality, or identifying missing tests. Triggers on "test review", "test quality", "coverage gaps", "missing tests", "test assessment", "regression protection", "flaky tests", "test audit".
---

# Test Quality Gatekeeper

Assess whether tests actually protect the system from regressions. Focus on real protection, not just coverage metrics.

## Core Principle

:warning: **High coverage ≠ High protection.** A test suite with 90% coverage can still miss critical bugs if it only tests happy paths.

## When to Use

- Reviewing test coverage for a feature
- Evaluating test quality before release
- Identifying gaps in regression protection
- Assessing contract test coverage between services
- Reviewing smart contract test completeness
- Identifying flaky or unreliable tests

## Review Workflow

On EVERY invocation, execute these steps:

### Step 1: Map Critical Paths

Identify what MUST work for the system to be valuable:

```
Critical Paths:
├── Authentication flow (login, logout, session)
├── Core business logic (payments, trading, data processing)
├── Data integrity (writes, updates, deletes)
├── External integrations (APIs, webhooks, events)
└── Error handling (failures, retries, recovery)
```

### Step 2: Inventory Existing Tests

```bash
# Find test files
find . -name "*.test.ts" -o -name "*.spec.ts" -o -name "*_test.go" | head -50

# Count tests by type
grep -r "describe\|it\|test(" --include="*.test.ts" | wc -l

# Find test commands
grep -E "test|jest|vitest|pytest|go test" package.json Makefile 2>/dev/null
```

Categorize tests:
| Type | Count | Coverage |
|------|-------|----------|
| Unit tests | [count] | [what they cover] |
| Integration tests | [count] | [what they cover] |
| E2E tests | [count] | [what they cover] |
| Contract tests | [count] | [what they cover] |

### Step 3: Analyze Test Quality

For each critical path, ask:

| Question | Yes/No | Evidence |
|----------|--------|----------|
| Is the happy path tested? | | |
| Are failure cases tested? | | |
| Are edge cases tested? | | |
| Are boundary conditions tested? | | |
| Is error handling tested? | | |
| Are race conditions tested? | | |

### Step 4: Execute Checklist

See [CHECKLIST.md](CHECKLIST.md) for the complete test quality checklist.

## Output Format

### A) Coverage Map

```
┌─────────────────────────────────────────────────────────────┐
│                    TEST COVERAGE MAP                         │
├─────────────────────────────────────────────────────────────┤
│ Component          │ Happy │ Failure │ Edge │ Overall      │
├────────────────────┼───────┼─────────┼──────┼──────────────┤
│ Authentication     │  ✅   │   ⚠️    │  ❌  │ PARTIAL      │
│ Order Processing   │  ✅   │   ✅    │  ✅  │ GOOD         │
│ Payment Flow       │  ✅   │   ❌    │  ❌  │ WEAK         │
│ Data Export        │  ❌   │   ❌    │  ❌  │ MISSING      │
└─────────────────────────────────────────────────────────────┘
```

### B) Coverage Gaps by Severity

#### :red_circle: CRITICAL - Must Add Before Release

Gaps that could cause production incidents:

```
### Missing: [Test Description]

**Component:** [Component name]
**Risk:** [What could go wrong without this test]
**Suggested test:**
[Code example or description]
```

#### :orange_circle: HIGH - Add Soon

Gaps that could cause regressions:

```
### Missing: [Test Description]

**Component:** [Component name]
**Risk:** [What could go wrong]
**Suggested test:** [Description]
```

#### :yellow_circle: MEDIUM - Should Have

Gaps that reduce confidence:

```
### Missing: [Test Description]
**Component:** [Component name]
**Why:** [Reason this matters]
```

#### :white_circle: LOW - Nice to Have

```
- [Test suggestion]
- [Test suggestion]
```

### C) Tests That Give False Confidence

Tests that exist but don't actually protect:

```
### :warning: False Confidence: [Test Name]

**Location:** `path/to/test.ts:123`
**Problem:** [Why this test doesn't protect]
**Example:** [What could break despite this test passing]
**Fix:** [How to make it actually protective]
```

Common false confidence patterns:
- Tests that only check happy paths
- Tests with no assertions
- Tests that mock too much
- Tests that test implementation, not behavior
- Flaky tests that are ignored

### D) Concrete Tests to Add Next

Prioritized list of specific tests to write:

```
Priority 1 (This sprint):
1. [Test name] - [file to add it to]
   - Test that [behavior]
   - Assert [expected outcome]
   - Cover cases: [list edge cases]

Priority 2 (Next sprint):
2. [Test name]
   ...

Priority 3 (Backlog):
3. [Test name]
   ...
```

### E) Test Health Summary

```
┌─────────────────────────────────────────────────────────────┐
│                   TEST HEALTH SUMMARY                        │
├─────────────────────────────────────────────────────────────┤
│ Critical paths protected:     [X/Y] ([percentage]%)          │
│ Failure cases covered:        [X/Y] ([percentage]%)          │
│ Edge cases covered:           [X/Y] ([percentage]%)          │
│ Flaky tests identified:       [count]                        │
│ False confidence tests:       [count]                        │
├─────────────────────────────────────────────────────────────┤
│ VERDICT: [PROTECTED / PARTIALLY PROTECTED / AT RISK]         │
└─────────────────────────────────────────────────────────────┘
```

## Quick Commands

```bash
# Run tests with coverage
npm test -- --coverage
pytest --cov=src
go test -coverprofile=coverage.out ./...

# Find untested files
npm test -- --coverage --collectCoverageFrom='src/**/*.ts' | grep "0%"

# Find tests without assertions
grep -rn "it\|test(" --include="*.test.ts" -A 10 | grep -B 10 "expect\|assert" | grep -v "expect\|assert"

# Find skipped tests
grep -rn "\.skip\|xit\|xdescribe\|@pytest.mark.skip" --include="*.test.ts" --include="*.spec.ts"

# Find flaky test indicators
grep -rn "retry\|flaky\|intermittent\|sometimes" --include="*.test.ts"

# Check for TODO in tests
grep -rn "TODO\|FIXME\|HACK" --include="*.test.ts"
```

## Resources

- [CHECKLIST.md](CHECKLIST.md) - Complete test quality checklist
- [PATTERNS.md](PATTERNS.md) - Test anti-patterns and good examples
