---
name: go-testing
description: >
  Testing patterns and conventions. Use when writing tests, reviewing
  test coverage, or organizing test infrastructure.
  Triggers: _test.go, TestXxx, t.Run, table-driven tests, black-box testing,
  package name_test, test coverage, t.Fatal, t.Error, t.Errorf.
  File patterns: tests/**/*.go, *_test.go
---

# Go Testing

## When This Skill Applies

- Writing new tests
- Reviewing test coverage
- Organizing test files
- Implementing table-driven tests
- Validating test success criteria

## Principles

### 1. Black-Box Testing

All tests use `package <name>_test` and import the package being tested:

```go
package config_test

import (
    "testing"

    "github.com/JaimeStill/agent-lab/internal/config"
)

func TestLoad(t *testing.T) {
    cfg, err := config.Load()
    if err != nil {
        t.Fatalf("Load() failed: %v", err)
    }

    if cfg == nil {
        t.Fatal("Load() returned nil config")
    }
}
```

**Rationale**: Tests only public API, ensuring the package works correctly from an external perspective.

### 2. Table-Driven Tests

Use table-driven tests for parameterized scenarios:

```go
func TestLoad_Scenarios(t *testing.T) {
    tests := []struct {
        name      string
        setup     func()
        cleanup   func()
        expectErr bool
    }{
        {
            name:      "loads base config",
            setup:     func() {},
            cleanup:   func() {},
            expectErr: false,
        },
        {
            name: "invalid duration returns error",
            setup: func() {
                os.Setenv("SERVER_READ_TIMEOUT", "invalid")
            },
            cleanup: func() {
                os.Unsetenv("SERVER_READ_TIMEOUT")
            },
            expectErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            tt.setup()
            defer tt.cleanup()

            _, err := config.Load()
            if tt.expectErr && err == nil {
                t.Error("expected error but got nil")
            }
            if !tt.expectErr && err != nil {
                t.Errorf("unexpected error: %v", err)
            }
        })
    }
}
```

### 3. Test Organization

Tests live in `tests/` directory mirroring source structure:

```
tests/
├── cmd_server/           # Server integration tests
├── internal_agents/      # Agents domain tests
├── internal_config/      # Config package tests
├── internal_documents/   # Documents domain tests
├── internal_providers/   # Providers domain tests
├── internal_storage/     # Storage system tests
├── internal_workflows/   # Workflows domain tests
├── pkg_handlers/         # HTTP handlers tests
├── pkg_openapi/          # OpenAPI package tests
├── pkg_pagination/       # Pagination package tests
├── pkg_query/            # Query builder tests
└── pkg_repository/       # Repository helpers tests
```

**File naming**: `<file>_test.go`

### 4. Coverage Success Criteria

Testing success is measured by coverage of critical paths, not arbitrary percentages:

- **Happy paths** - Normal operation flows work correctly
- **Security paths** - Input validation, path traversal prevention, injection protection
- **Error types** - Domain errors are defined and distinguishable
- **Integration points** - Lifecycle hooks, system boundaries, external dependencies

### 5. Acceptable Uncovered Code

Some code paths are acceptable to leave uncovered:

- Defensive error handling for OS-level failures (disk full, permission denied)
- Edge cases requiring filesystem mocking or special conditions
- Error wrapping paths that don't affect behavior

## Patterns

### Test Helper Functions

```go
func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()
    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        t.Fatalf("failed to open test db: %v", err)
    }
    t.Cleanup(func() { db.Close() })
    return db
}
```

### Error Assertion

```go
if tt.expectErr && err == nil {
    t.Error("expected error but got nil")
}
if !tt.expectErr && err != nil {
    t.Errorf("unexpected error: %v", err)
}
```

### Running Tests

```bash
go test ./tests/...           # Run all tests
go test ./tests/... -v        # Verbose output
go test ./tests/... -cover    # With coverage
```

## Anti-Patterns

### Testing Implementation Details

```go
// Bad: Testing private fields/methods
func TestHandler_internalState(t *testing.T) {
    h := &Handler{}
    h.cache = make(map[string]string)  // Accessing private field
}

// Good: Test through public API
func TestHandler_Process(t *testing.T) {
    h := NewHandler()
    result, err := h.Process(input)
    // Assert on result
}
```

### Non-Deterministic Tests

```go
// Bad: Flaky time-based test
func TestTimeout(t *testing.T) {
    time.Sleep(100 * time.Millisecond)
    // May fail on slow CI
}

// Good: Use channels or context
func TestTimeout(t *testing.T) {
    ctx, cancel := context.WithTimeout(context.Background(), time.Second)
    defer cancel()
    // Test with context
}
```
