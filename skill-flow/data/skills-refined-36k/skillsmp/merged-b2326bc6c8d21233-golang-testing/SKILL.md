---
name: golang-testing
description: Use this skill when writing comprehensive test suites for Go applications, including unit tests, mocking, benchmarking, and CI/CD integration.
---

# Go Testing

## Overview

Go provides a robust built-in testing framework (`testing` package) that emphasizes simplicity and developer productivity. Combined with community tools like Testify and Gomock, Go testing enables comprehensive test coverage with minimal boilerplate.

**Key Features:**
- 📋 **Table-Driven Tests**: Idiomatic pattern for testing multiple inputs
- ✅ **Testify**: Readable assertions and test suites
- 🎭 **Gomock**: Type-safe interface mocking
- ⚡ **Benchmarking**: Built-in performance testing
- 🔍 **Race Detector**: Concurrent code safety verification
- 📊 **Coverage**: Native coverage reporting and enforcement
- 🚀 **CI Integration**: Test caching and parallel execution

## When to Use This Skill

Activate this skill when:
- Writing test suites for Go libraries or applications
- Setting up testing infrastructure for new projects
- Mocking external dependencies (databases, APIs, services)
- Benchmarking performance-critical code paths
- Ensuring thread-safe concurrent implementations
- Integrating tests into CI/CD pipelines
- Migrating from other testing frameworks

## Core Testing Principles

### The Go Testing Philosophy

1. **Simplicity Over Magic**: Use standard library when possible
2. **Table-Driven Tests**: Test multiple scenarios with a single function
3. **Subtests**: Organize related tests with `t.Run()`
4. **Interface-Based Mocking**: Mock dependencies through interfaces
5. **Test Files Colocate**: Place `*_test.go` files alongside code
6. **Package Naming**: Use `package_test` for external tests, `package` for internal

## Test Organization

**File Naming Convention:**
- Unit tests: `file_test.go`
- Integration tests: `file_integration_test.go`
- Benchmark tests: Prefix with `Benchmark` in the same test file

**Package Structure:**
```
mypackage/
├── user.go
├── user_test.go              // Internal tests (same package)
├── user_external_test.go     // External tests (package mypackage_test)
├── integration_test.go       // Integration tests
└── testdata/                 // Test fixtures (ignored by go build)
    └── golden.json
```

## Table-Driven Test Pattern

### Basic Structure

The idiomatic Go testing pattern for testing multiple inputs:

```go
func TestUserValidation(t *testing.T) {
    tests := []struct {
        name    string
        input   User
        wantErr bool
        errMsg  string
    }{
        {
            name:    "valid user",
            input:   User{Name: "Alice", Age: 30, Email: "alice@example.com"},
            wantErr: false,
        },
        {
            name:    "empty name",
            input:   User{Name: "", Age: 30, Email: "alice@example.com"},
            wantErr: true,
            errMsg:  "name is required",
        },
        {
            name:    "invalid email",
            input:   User{Name: "Bob", Age: 25, Email: "invalid"},
            wantErr: true,
            errMsg:  "invalid email format",
        },
        {
            name:    "negative age",
            input:   User{Name: "Charlie", Age: -5, Email: "charlie@example.com"},
            wantErr: true,
            errMsg:  "age must be positive",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateUser(tt.input)

            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateUser() error = %v, wantErr %v", err, tt.wantErr)
                return
            }

            if tt.wantErr && err.Error() != tt.errMsg {
                t.Errorf("ValidateUser() error message = %v, want %v", err.Error(), tt.errMsg)
            }
        })
    }
}
```

### Parallel Test Execution

Enable parallel test execution for independent tests:

```go
func TestConcurrentOperations(t *testing.T) {
    tests := []struct {
        name string
        fn   func() int
        want int
    }{
        {"operation 1", func() int { return compute1() }, 42},
        {"operation 2", func() int { return compute2() }, 84},
        {"operation 3", func() int { return compute3() }, 126},
    }

    for _, tt := range tests {
        tt := tt // Capture range variable
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // Run tests concurrently

            got := tt.fn()
            if got != tt.want {
                t.Errorf("got %v, want %v", got, tt.want)
            }
        })
    }
}
```

## Testify Framework

### Installation

```bash
go get github.com/stretchr/testify
```

### Assertions

Replace verbose error checking with readable assertions:

```go
import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestCalculator(t *testing.T) {
    calc := NewCalculator()

    // assert: Test continues on failure
    assert.Equal(t, 5, calc.Add(2, 3))
    assert.NotNil(t, calc)
    assert.True(t, calc.IsReady())

    // require: Test stops on failure (for critical assertions)
    result, err := calc.Divide(10, 2)
    require.NoError(t, err) // Stop if error occurs
    assert.Equal(t, 5, result)
}
```

### Test Suites

Organize related tests with setup/teardown:

```go
import (
    "testing"
    "github.com/stretchr/testify/suite"
)

type UserServiceTestSuite struct {
    suite.Suite
    db      *sql.DB
    service *UserService
}

// SetupSuite runs once before all tests
func (s *UserServiceTestSuite) SetupSuite() {
    s.db = setupTestDatabase()
    s.service = NewUserService(s.db)
}

// TearDownSuite runs once after all tests
func (s *UserServiceTestSuite) TearDownSuite() {
    s.db.Close()
}

// SetupTest runs before each test
func (s *UserServiceTestSuite) SetupTest() {
    cleanDatabase(s.db)
}

// TearDownTest runs after each test
func (s *UserServiceTestSuite) TearDownTest() {
    // Cleanup if needed
}

// Test methods must start with "Test"
func (s *UserServiceTestSuite) TestCreateUser() {
    user := &User{Name: "Alice", Email: "alice@example.com"}

    err := s.service.Create(user)
    s.NoError(err)
    s.NotEqual(0, user.ID) // ID assigned
}

// Run the suite
func TestUserServiceTestSuite(t *testing.T) {
    suite.Run(t, new(UserServiceTestSuite))
}
```

## Gomock Interface Mocking

### Installation

```bash
go install github.com/golang/mock/mockgen@latest
```

### Generate Mocks

```go
// user_repository.go
package repository

//go:generate mockgen -source=user_repository.go -destination=mocks/mock_user_repository.go -package=mocks

type UserRepository interface {
    GetByID(id int) (*User, error)
    Create(user *User) error
    Update(user *User) error
    Delete(id int) error
}
```

Generate mocks:
```bash
go generate ./...
# Or manually:
mockgen -source=user_repository.go -destination=mocks/mock_user_repository.go -package=mocks
```

### Using Mocks in Tests

```go
import (
    "testing"
    "github.com/golang/mock/gomock"
    "github.com/stretchr/testify/assert"
    "myapp/repository/mocks"
)

func TestUserService_GetUser(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    // Create mock
    mockRepo := mocks.NewMockUserRepository(ctrl)

    // Set expectations
    expectedUser := &User{ID: 1, Name: "Alice"}
    mockRepo.EXPECT().
        GetByID(1).
        Return(expectedUser, nil).
        Times(1)

    // Test
    service := NewUserService(mockRepo)
    user, err := service.GetUser(1)

    // Assertions
    assert.NoError(t, err)
    assert.Equal(t, expectedUser, user)
}
```

## Benchmark Testing

### Basic Benchmarks

```go
func BenchmarkAdd(b *testing.B) {
    calc := NewCalculator()

    for i := 0; i < b.N; i++ {
        calc.Add(2, 3)
    }
}
```

### Running Benchmarks

```bash
# Run all benchmarks
go test -bench=.

# Run specific benchmark
go test -bench=BenchmarkAdd

# With memory allocation stats
go test -bench=. -benchmem
```

## Advanced Testing Patterns

### httptest for HTTP Handlers

```go
import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestUserHandler(t *testing.T) {
    handler := http.HandlerFunc(UserHandler)

    req := httptest.NewRequest("GET", "/users/1", nil)
    rec := httptest.NewRecorder()

    handler.ServeHTTP(rec, req)

    assert.Equal(t, http.StatusOK, rec.Code)
    assert.Contains(t, rec.Body.String(), "Alice")
}
```

### Race Detector

Detect data races in concurrent code:

```bash
go test -race ./...
```

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.23'

      - name: Run tests
        run: go test -v -race -coverprofile=coverage.out ./...

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.out
```

## Best Practices

1. **Colocate Tests**: Place `*_test.go` files alongside source code
2. **Use Subtests**: Organize related tests with `t.Run()`
3. **Parallel When Safe**: Enable `t.Parallel()` for independent tests
4. **Mock Interfaces**: Design for testability with interface dependencies
5. **Test Errors**: Verify both success and failure paths
6. **Benchmark Critical Paths**: Profile performance-sensitive code
7. **Run Race Detector**: Always use `-race` for concurrent code
8. **Enforce Coverage**: Set minimum thresholds in CI (typically 80%)

## Resources

**Official Documentation:**
- Go Testing Package: https://pkg.go.dev/testing
- Table-Driven Tests: https://github.com/golang/go/wiki/TableDrivenTests

**Testing Frameworks:**
- Testify: https://github.com/stretchr/testify
- Gomock: https://github.com/golang/mock
- httptest: https://pkg.go.dev/net/http/httptest

## Quick Reference

### Run Tests
```bash
go test ./...                    # All tests
go test -v ./...                 # Verbose output
go test -short ./...             # Skip slow tests
go test -run TestUserCreate      # Specific test
go test -race ./...              # With race detector
go test -cover ./...             # With coverage
```

### Generate Mocks
```bash
go generate ./...                           # All //go:generate directives
mockgen -source=interface.go -destination=mock.go
```

### Coverage Analysis
```bash
go tool cover -func=coverage.out           # Coverage per function
go tool cover -html=coverage.out           # HTML report
```