---
name: testing-patterns
description: Comprehensive testing guide for ActionPhase covering the test pyramid (unit tests, API tests, component tests, E2E tests), TDD workflow, Test-Driven Development, regression testing, Playwright E2E patterns, React Testing Library component tests, Go table-driven tests, test fixtures, and the mandatory E2E checklist. Use when writing tests, debugging test failures, understanding testing strategy, or implementing test-driven development.
---

# Testing Patterns

## Purpose

Comprehensive guide to testing in ActionPhase, covering the testing pyramid, TDD workflow, and patterns for backend (Go), frontend (React/TypeScript), and E2E (Playwright) testing.

## When to Use This Skill

- Writing any type of test (unit, component, E2E)
- Debugging test failures
- Understanding the testing pyramid
- Implementing TDD workflow
- Fixing bugs (regression testing)
- Setting up test fixtures
- Understanding E2E testing rules

---

## Testing Philosophy

**"Tests are MANDATORY for all new features and bug fixes"**

**THE GOLDEN RULE**: E2E tests are the LAST step, NEVER the first!

---

## The Testing Pyramid

```
┌──────────────────────────────────┐
│  4. E2E Tests (Playwright)       │ ← Slow (20-30s each), expensive, LAST
│     ~30 tests                    │    Write ONLY after lower levels pass
├──────────────────────────────────┤
│  3. Component Tests (React)      │ ← Medium speed (~15-20s total)
│     1,022 tests                  │    Test user interactions
├──────────────────────────────────┤
│  2. API Integration Tests        │ ← Fast verification
│     (curl verification)          │    Verify endpoints work
├──────────────────────────────────┤
│  1. Unit Tests (Go/TypeScript)   │ ← Fastest (~300ms for mocks)
│     467 backend tests            │    Write FIRST, test behavior
└──────────────────────────────────┘

Total: 1,489 passing tests (100% pass rate)
```

**See**: [testing-pyramid.md](resources/testing-pyramid.md) for detailed explanation

---

## Quick Reference

### Backend Testing (Go)

**Unit Tests** (FAST - ~300ms):
```bash
just test-mocks        # Unit tests without database
```

**Integration Tests** (with database):
```bash
just test              # All tests (unit + integration)
just test-integration  # Integration tests only
```

**Patterns**:
- Table-driven tests with subtests
- Test database with automatic cleanup
- Mock interfaces for fast tests
- `testify/assert` and `testify/require`

**See**: [backend-testing.md](resources/backend-testing.md)

### Frontend Testing (React)

**Component Tests**:
```bash
just test-frontend           # Run all tests
just test-fe watch           # Watch mode
npm test -- Component.test.tsx  # Specific file
```

**Patterns**:
- React Testing Library (screen queries)
- MSW v2 for API mocking
- `renderWithProviders()` wrapper
- Test user interactions, not implementation

**See**: [frontend-testing.md](resources/frontend-testing.md)

### E2E Testing (Playwright)

**Run Tests**:
```bash
just e2e               # Headless (auto-loads fixtures)
just e2e-test headed   # Visible browser
just e2e-test ui       # Interactive UI mode
just e2e-test debug    # Debug mode
```

**CRITICAL**: E2E tests are the LAST step!

**See**: [e2e-testing.md](resources/e2e-testing.md)

---

## E2E Testing - Mandatory Checklist

**⚠️ BEFORE writing ANY E2E test, ALL four must pass:**

```bash
# 1. ✅ Backend unit test MUST pass
SKIP_DB_TESTS=true go test ./pkg/db/services -run TestFeature -v

# 2. ✅ API endpoint MUST return correct data
curl -X POST http://localhost:3000/api/v1/endpoint \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  -d '...' | jq '.expected_field'

# 3. ✅ Frontend component test MUST pass
npm test -- ComponentName.test.tsx

# 4. ✅ System verification MUST complete
curl -sf http://localhost:3000/health  # Backend running
curl -sf http://localhost:5173         # Frontend running
```

**ONLY after all four pass → Write E2E test**

**See**: [e2e-testing.md](resources/e2e-testing.md) for complete E2E guide

---

## Testing Workflow

### For New Features (TDD Approach)

```
1. Write unit test (should FAIL)
   ↓
2. Implement feature
   ↓
3. Unit test passes
   ↓
4. Test API with curl (verify endpoint)
   ↓
5. Write component test (if UI feature)
   ↓
6. Component test passes
   ↓
7. Verify system running
   ↓
8. Write E2E test (LAST STEP)
```

**See**: [testing-pyramid.md](resources/testing-pyramid.md)

### For Bug Fixes (Mandatory Regression Testing)

```bash
# 1. Write test that reproduces bug (should FAIL)
go test ./pkg/db/services -run TestBugFix -v
# Output: FAIL ❌

# 2. Fix the bug in code
# (make changes)

# 3. Verify test passes
go test ./pkg/db/services -run TestBugFix -v
# Output: PASS ✅

# 4. Commit test and fix together
```

**See**: [bug-fix-workflow.md](resources/bug-fix-workflow.md)

---

## Key Commands

### Backend

```bash
just test              # All tests (467 tests)
just test-mocks        # Fast unit tests (~300ms)
just test-integration  # Database integration tests
just test-coverage     # Generate coverage report
just test-race         # Race condition detection
just test-run pattern  # Run specific test by name
just ci-test           # Full CI suite (lint + test + race)
```

### Frontend

```bash
just test-frontend     # All frontend tests (1,022 tests)
just test-fe watch     # Watch mode for development
just test-fe coverage  # With coverage report
npm test -- Component.test.tsx  # Specific file
```

### E2E

```bash
just e2e               # Run E2E tests (headless)
just e2e-test headed   # Visible browser
just e2e-test ui       # Interactive UI mode
just e2e-test debug    # Debug specific test
just e2e-test report   # View HTML report
just load-e2e          # Load E2E test fixtures
```

**See**: [test-commands.md](resources/test-commands.md) for complete reference

---

## Test Data & Fixtures

### Test Users

**All passwords**: `testpassword123`
**Important**: Usernames are case-sensitive (PascalCase!)

- **GM**: `TestGM` / `test_gm@example.com`
- **Player 1**: `TestPlayer1` / `test_player1@example.com`
- **Player 2**: `TestPlayer2` / `test_player2@example.com`
- **Player 3-5**: `TestPlayer3`, `TestPlayer4`, `TestPlayer5`
- **Audience**: `TestAudience` / `test_audience@example.com`

### Test Games

10 games with various states (recruiting, running, paused, completed)

**Key Test Games**:
- **Game 1**: Shadows Over Innsmouth (common room phase)
- **Game 2**: The Heist at Goldstone Bank (action submissions)
- **Game 6**: Chronicles of Westmarch (pagination testing - 11 phases)

### Fixture Commands

```bash
just test-fixtures     # Apply all fixtures
just load-e2e          # Load E2E fixtures (6 workers)
just test-data reload  # Reset and reload
```

**See**: [test-fixtures.md](resources/test-fixtures.md) for complete fixture documentation

---

## Common Anti-Patterns

### Backend

❌ **DON'T**: Hardcode test data
```go
userID := 123  // Hardcoded
```

✅ **DO**: Use fixtures
```go
user := testDB.CreateTestUser(t, "testuser", "test@example.com")
```

❌ **DON'T**: Skip cleanup
```go
// Test creates data but doesn't clean up
```

✅ **DO**: Use defer cleanup
```go
defer testDB.CleanupTables(t, "users", "games")
```

### Frontend

❌ **DON'T**: Test implementation details
```typescript
expect(component.state.count).toBe(1)  // Testing internal state
```

✅ **DO**: Test user interactions
```typescript
expect(screen.getByText('Count: 1')).toBeInTheDocument()
```

❌ **DON'T**: MSW double-wrapping
```typescript
http.get('/api/endpoint', () => {
  return HttpResponse.json({ data: mockData })  // ❌ axios wraps again
})
```

✅ **DO**: Return unwrapped data
```typescript
http.get('/api/endpoint', () => {
  return HttpResponse.json(mockData)  // ✅ axios wraps automatically
})
```

### E2E

❌ **DON'T**: Write E2E before unit tests
```typescript
// No unit test → straight to E2E ❌
```

✅ **DO**: Follow the pyramid
```bash
# Unit → API → Component → E2E ✅
```

❌ **DON'T**: Multiple concerns in one test
```typescript
test('feature works', async () => {
  // Tests autocomplete + submission + rendering + validation ❌
})
```

✅ **DO**: One concern per test
```typescript
test('autocomplete appears when typing @', async () => {
  // Only tests autocomplete ✅
})
```

❌ **DON'T**: Arbitrary timeouts
```typescript
await page.waitForTimeout(3000)  // ❌ Flaky
```

✅ **DO**: Explicit waits
```typescript
await page.waitForSelector('[data-testid="element"]')  // ✅ Reliable
```

**See**: [anti-patterns.md](resources/anti-patterns.md) for complete list

---

## Coverage Targets

### Current Status

- **Backend**: 75.0% coverage (467 tests) - Target: 80%
- **Frontend**: ~60% coverage (1,022 tests) - Target: 60% ✅ **MET**
- **E2E**: 30 test files covering critical user journeys
- **Pass Rate**: 100% ✅

### Quality Gates

- ✅ 100% pass rate on main
- ✅ All critical paths covered
- ✅ Regression tests for all known bugs
- ✅ Test execution < 5 minutes

**See**: [coverage-targets.md](resources/coverage-targets.md)

---

## Real Code Examples

### Code Examples

**Backend** - Table-driven tests with testDB fixtures
**Frontend** - Component tests with RTL + MSW
**E2E** - Playwright tests with auth helpers

**See**: [real-examples.md](resources/real-examples.md) for more examples

---

## Navigation Guide

| Need to... | Read this |
|------------|-----------|
| Understand testing pyramid and workflow | [testing-pyramid.md](resources/testing-pyramid.md) |
| Write backend unit/integration tests | [backend-testing.md](resources/backend-testing.md) |
| Write frontend component/hook tests | [frontend-testing.md](resources/frontend-testing.md) |
| Write E2E tests with Playwright | [e2e-testing.md](resources/e2e-testing.md) |
| Use test fixtures and test data | [test-fixtures.md](resources/test-fixtures.md) |
| Find testing commands | [test-commands.md](resources/test-commands.md) |
| Avoid common mistakes | [anti-patterns.md](resources/anti-patterns.md) |
| Check coverage targets | [coverage-targets.md](resources/coverage-targets.md) |
| Fix bugs with TDD | [bug-fix-workflow.md](resources/bug-fix-workflow.md) |
| See real code examples | [real-examples.md](resources/real-examples.md) |

---

## Related Skills & Context

### Skills
- **backend-dev-guidelines** - Backend implementation patterns
- **frontend-dev-guidelines** - Frontend component patterns
- **route-tester** - API endpoint testing with curl
- **game-domain** - Game state testing scenarios
- **test-fixtures** - Test data management

### Context Files
- `.claude/context/TESTING.md` - Primary testing reference (comprehensive)
- `.claude/context/TEST_DATA.md` - Test fixtures overview
- `/docs/testing/COVERAGE_STATUS.md` - Current coverage metrics
- `/docs/testing/E2E_QUICK_START.md` - E2E quick reference
- `/docs/adrs/007-testing-strategy.md` - Testing strategy decisions

---

## Quick Start

**New to testing in ActionPhase?** Read in this order:

1. [testing-pyramid.md](resources/testing-pyramid.md) - Understand the approach
2. [backend-testing.md](resources/backend-testing.md) OR [frontend-testing.md](resources/frontend-testing.md) - Your domain
3. [test-fixtures.md](resources/test-fixtures.md) - Set up test data
4. [e2e-testing.md](resources/e2e-testing.md) - E2E patterns (read BEFORE writing E2E tests!)

**Writing tests?**
- [test-commands.md](resources/test-commands.md) - Find the right command
- [real-examples.md](resources/real-examples.md) - Copy patterns from working code

**Debugging?**
- [anti-patterns.md](resources/anti-patterns.md) - Check common mistakes
- [bug-fix-workflow.md](resources/bug-fix-workflow.md) - TDD approach to bugs

---

**Skill Status**: COMPLETE ✅
**Line Count**: < 500 ✅
**Progressive Disclosure**: 10 resource files ✅
**Coverage**: Complete testing pyramid, all test types, TDD workflow ✅
