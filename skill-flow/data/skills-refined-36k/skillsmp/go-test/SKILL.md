---
name: go-test
description: >
  Go testing patterns and best practices. Load when writing or running Go tests.
  Triggers: running tests, writing test files, test coverage, benchmarks,
  integration tests, table-driven tests, mocking, fixtures, or asking about
  Go testing patterns.
license: MIT
compatibility: opencode
---

# Go Testing

Run and write tests for Go projects following best practices.

## When This Skill MUST Be Used

**ALWAYS invoke this skill when the user's request involves ANY of these:**

- Running `go test` or asking to run tests
- Writing or modifying `*_test.go` files
- Setting up integration tests with databases
- Test coverage analysis
- Benchmarking Go code
- Mocking or test fixtures
- Table-driven tests
- Race condition detection
- Test structure (GIVEN-WHEN-THEN)

**If you're about to run or write Go tests, STOP and use this skill first.**

## Critical Safety Rules

**NEVER:**
- Run integration tests without checking for required env vars
- Skip the `-race` flag in CI/CD pipelines
- Leave test containers running after tests
- Commit code with failing tests
- Use `require`/`Fatal` inside goroutines (causes panic)
- Share mocks, loggers, or DB connections between parallel tests

**ALWAYS:**
- Use `t.Parallel()` for independent tests AND subtests
- Clean up test resources with `t.Cleanup()`
- Use build tags to separate unit and integration tests
- Check test coverage for new code
- Mark helper functions with `t.Helper()`

## Quick Reference

| Task | Command |
|------|---------|
| Run all tests | `go test ./...` |
| Verbose output | `go test -v ./...` |
| With coverage | `go test -cover ./...` |
| With race detection | `go test -race ./...` |
| Run specific test | `go test -run TestName ./...` |
| Run benchmarks | `go test -bench=. ./...` |
| Force re-run | `go test -count=1 ./...` |

---

# Test Structure: GIVEN-WHEN-THEN

- **GIVEN**: Setup and preconditions (use `require` - stop if setup fails)
- **WHEN**: Single action being tested (use `require` - stop if action fails)
- **THEN**: Assertions on results (use `assert` - see all failures)

**Critical**: Only ONE WHEN section per test. Multiple behaviors = multiple tests.

## require vs assert

| Phase | Use | Rationale |
|-------|-----|-----------|
| GIVEN | `require` | Stop if setup fails |
| WHEN | `require` | Stop if action fails |
| THEN | `assert` | See all failures |
| Goroutines | `assert` | NEVER use require (causes panic) |

**Goroutine Warning**: Never use `require`/`Fatal` inside goroutines, HTTP handlers, or callbacks - causes "FailNow called from non-test goroutine" panic.

---

# Parallel Execution

- Always use `t.Parallel()` in tests AND subtests
- Each test creates its own fixture - no shared state
- Subtests must NOT access parent test variables

**Forbidden Sharing:**
- Loggers, database connections, singletons
- File handles, network ports
- Mock expectations defined in parent scope

**Acceptable Sharing:**
- Read-only table data in table-driven tests
- Global constants, types, and functions

---

# File Naming

| Type | File Suffix | Package Declaration | Access |
|------|-------------|---------------------|--------|
| Public tests | `*_test.go` | `package foo_test` | Exported only (preferred) |
| Private tests | `*_internal_test.go` | `package foo` | All members |
| Integration | `*_integration_test.go` | `//go:build integration` | Real deps |

**Default**: Use public tests. Add private tests only for internal invariants or combinatorial explosion.

## Test Naming

- Functions: `Test<Type>_<Method>` (e.g., `TestUserService_CreateUser`)
- Subtests: Short, descriptive (e.g., `"with valid input"`, `"returns error"`)

---

# Table-Driven Tests

## When to Use

- Simple data variations (primitives only)
- Boundary conditions and validation
- 3-4 fields maximum in table struct

## The Simplicity Test

> "Can I understand what each test case does by looking at one line in the table?"

If NO, use separate tests instead.

## Anti-patterns (Never Put in Tables)

| Anti-pattern | Why Bad |
|--------------|---------|
| Mock expectations | Behavior, not data |
| Boolean flags | Creates different test logic |
| Setup/assertion functions | Hides complexity |
| Auto-generated templates | Generic, not thoughtful |

---

# Fixture Pattern

```go
type fixture struct {
    ctx      context.Context
    mockRepo *MockRepository
    sut      *Service
}

func newFixture(t *testing.T) *fixture {
    t.Helper()
    ctrl := gomock.NewController(t)
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    t.Cleanup(cancel)
    
    mockRepo := NewMockRepository(ctrl)
    return &fixture{
        ctx:      ctx,
        mockRepo: mockRepo,
        sut:      NewService(mockRepo),
    }
}
```

---

# Mocking

- Define interfaces in `interfaces.go`
- Add `//go:generate mockgen` directive
- Store mocks in `mock_test.go` with `package foo_test`
- `gomock.Any()` when values don't matter
- `gomock.Eq()` for exact matching in happy path
- Create new mock controller per test/subtest

---

# Must Constructor Pattern

For test helpers that panic on error (never in production):

```go
// Production: returns error
func NewCategoryID(value string) (CategoryID, error)

// Tests only: panics on error
func MustCategoryID(value string) CategoryID {
    id, err := NewCategoryID(value)
    if err != nil {
        panic(err)
    }
    return id
}
```

Standard library examples: `regexp.MustCompile`, `template.Must`

---

# Deterministic Tests

Inject all nondeterminism:

| Source | Solution |
|--------|----------|
| `time.Now()` | `Clock` interface |
| `uuid.New()` | `UUIDGenerator` interface |
| Random numbers | Injectable generator |

---

# Contract Testing (Marshal/Unmarshal)

- Use raw JSON strings as the "contract"
- Don't use internal types for both encode and decode
- Use `testify.JSONEq()` for comparison
- Store JSON contracts in `testdata/` directory

---

# Testing Conversion Layers

What to test in HTTP/gRPC handlers:
1. Request unmarshaling and argument passing
2. Error translation (domain errors -> protocol errors)
3. Response marshaling

Pattern: Mock domain layer, verify exact arguments, verify error codes.

---

# Coverage

| Type | Goal | Build Tag |
|------|------|-----------|
| Unit tests | 100% (all deps mocked) | None |
| Integration tests | As appropriate | `integration` |

---

# Running Tests

## Basic Commands

```bash
# Unit tests only
go test ./...

# Unit tests with verbose output
go test -v ./...

# Unit tests with coverage
go test -cover ./...

# Unit tests with coverage report
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## Running Single Tests

```bash
# Run specific test by name
go test -v -run TestOrderRepository ./internal/infra/mysqlrepo/...

# Run tests matching pattern
go test -v -run "TestOrder.*" ./...

# Run specific subtest
go test -v -run "TestOrderRepository/creates_order" ./...
```

---

# Integration Tests

Integration tests typically use build tags to separate from unit tests:

```bash
# Run integration tests (requires database)
go test -tags=integration -v ./...

# Run integration tests for specific package
go test -tags=integration -v ./internal/infra/mysqlrepo/...

# With database DSN
TEST_MYSQL_DSN="root:pass@tcp(localhost:3306)/testdb?parseTime=true" \
  go test -tags=integration -v ./...
```

## Docker-based Database for Tests

```bash
# Start MySQL container
docker run -d --name test-mysql \
  -e MYSQL_ROOT_PASSWORD=pass \
  -e MYSQL_DATABASE=testdb \
  -p 3306:3306 \
  mysql:8

# Wait for MySQL to be ready
until docker exec test-mysql mysqladmin ping -h localhost --silent; do
  sleep 1
done

# Run integration tests
TEST_MYSQL_DSN="root:pass@tcp(localhost:3306)/testdb?parseTime=true" \
  go test -tags=integration -v ./...

# Clean up
docker rm -f test-mysql
```

## Integration Test Setup

```go
//go:build integration

package mysqlrepo_test

import (
    "os"
    "testing"
)

func TestMain(m *testing.M) {
    dsn := os.Getenv("TEST_MYSQL_DSN")
    if dsn == "" {
        // Skip integration tests if DSN not set
        os.Exit(0)
    }
    
    // Setup database connection
    // Run migrations if needed
    
    code := m.Run()
    
    // Cleanup
    
    os.Exit(code)
}
```

---

# Coverage

```bash
# Generate coverage profile
go test -coverprofile=coverage.out ./...

# View coverage in terminal
go tool cover -func=coverage.out

# View coverage in browser
go tool cover -html=coverage.out

# Coverage for specific packages
go test -coverprofile=coverage.out -coverpkg=./internal/... ./...
```

---

# Race Detection

```bash
# Run tests with race detector
go test -race ./...

# Race detection with specific test
go test -race -run TestConcurrentAccess ./...
```

---

# Benchmarks

```bash
# Run all benchmarks
go test -bench=. ./...

# Run specific benchmark
go test -bench=BenchmarkOrderCreation ./internal/domain/order/...

# Benchmarks with memory allocation stats
go test -bench=. -benchmem ./...

# Run benchmark multiple times
go test -bench=. -count=5 ./...
```

---

# Test Caching

```bash
# Force re-run (disable cache)
go test -count=1 ./...

# Clean test cache
go clean -testcache
```

---

# Makefile Targets

```makefile
.PHONY: test test-unit test-integration test-coverage

test: test-unit

test-unit:
	go test -v -race ./...

test-integration:
	go test -tags=integration -v ./...

test-coverage:
	go test -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html
```

---

# Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Tests skipped | Missing env vars | Set `TEST_MYSQL_DSN` etc. |
| Connection refused | DB not running | Start container, wait for ready |
| Race detected | Concurrent access | Add mutex or redesign |
| Flaky tests | Shared state / timing | Use `t.Parallel()`, fix timing |
| Slow tests | No parallelization | Add `t.Parallel()` |
| Cache issues | Stale results | Use `-count=1` or clean cache |
| "FailNow from non-test goroutine" | `require` in goroutine | Use `assert` instead |

---

# Example Requests

| User Request | Action |
|--------------|--------|
| "Run the tests" | `go test -v ./...` |
| "Run tests with coverage" | `go test -cover ./...` then `go tool cover -html` |
| "Run only integration tests" | `go test -tags=integration -v ./...` |
| "Check for race conditions" | `go test -race ./...` |
| "Run a specific test" | `go test -v -run TestName ./path/...` |
| "Benchmark this function" | `go test -bench=BenchmarkName -benchmem ./...` |
| "Why are tests slow?" | Check for missing `t.Parallel()`, use `-p 1` for isolation |
| "Write a test for this function" | Use GIVEN-WHEN-THEN structure with fixture pattern |
| "Should I use table-driven tests?" | Only if simple data variations, 3-4 fields max |
