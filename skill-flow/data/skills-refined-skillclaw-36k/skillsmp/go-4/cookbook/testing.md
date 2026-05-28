# Testing Cookbook

Recipes for writing effective tests in Go using standard library and testify.

---

## Table-Driven Tests

**Problem**: How to test multiple inputs efficiently without duplicating test code?

**Solution**:
```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positives", 2, 3, 5},
        {"negatives", -1, -1, -2},
        {"zero", 0, 5, 5},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := Add(tt.a, tt.b)
            if got != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.expected)
            }
        })
    }
}
```

**Tip**: Use descriptive test case names - they appear in test output on failure.

---

## Table-Driven Tests with Errors

**Problem**: How to test functions that return errors alongside regular values?

**Solution**:
```go
func TestParse(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    int
        wantErr bool
    }{
        {"valid", "42", 42, false},
        {"invalid", "abc", 0, true},
        {"empty", "", 0, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Parse(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("Parse() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("Parse() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

**Tip**: Return early after error check to avoid nil pointer issues in subsequent assertions.

---

## Testify Assertions

**Problem**: How to write cleaner assertions with better failure messages?

**Solution**:
```go
import "github.com/stretchr/testify/assert"

func TestExample(t *testing.T) {
    // Basic assertions (continues on failure)
    assert.Equal(t, expected, actual)
    assert.NotEqual(t, a, b)
    assert.Nil(t, err)
    assert.NotNil(t, result)
    assert.True(t, condition)
    assert.Empty(t, slice)
    assert.Len(t, slice, 3)
    assert.Contains(t, "hello world", "world")
    assert.ElementsMatch(t, []int{1, 2, 3}, []int{3, 2, 1})

    // Error assertions
    assert.NoError(t, err)
    assert.Error(t, err)
    assert.ErrorIs(t, err, ErrNotFound)
    assert.ErrorContains(t, err, "not found")
}
```

**Tip**: Use `require` instead of `assert` for setup steps that must succeed - it stops the test immediately on failure.

---

## Testify Require for Setup

**Problem**: How to fail fast when setup steps fail, avoiding cascading errors?

**Solution**:
```go
import "github.com/stretchr/testify/require"

func TestWithSetup(t *testing.T) {
    // Use require for setup - stops test on failure
    conn, err := Connect()
    require.NoError(t, err)
    require.NotNil(t, conn)

    // Use assert for actual test assertions
    result := conn.Query()
    assert.Equal(t, expected, result)
}
```

**Tip**: Pattern: `require` for preconditions, `assert` for assertions you want to see all failures for.

---

## Mocking with Testify

**Problem**: How to test code that depends on external services or databases?

**Solution**:
```go
import "github.com/stretchr/testify/mock"

// Define mock
type MockDB struct {
    mock.Mock
}

func (m *MockDB) Get(id string) (*User, error) {
    args := m.Called(id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

// Use in test
func TestService(t *testing.T) {
    mockDB := new(MockDB)

    // Set expectations
    mockDB.On("Get", "123").Return(&User{Name: "John"}, nil)
    mockDB.On("Get", "999").Return(nil, ErrNotFound)

    svc := NewService(mockDB)
    user, err := svc.GetUser("123")

    assert.NoError(t, err)
    assert.Equal(t, "John", user.Name)
    mockDB.AssertExpectations(t)
}
```

**Tip**: Call `AssertExpectations(t)` at the end to verify all expected calls were made.

---

## Test Suites

**Problem**: How to share setup/teardown logic across related tests?

**Solution**:
```go
import (
    "testing"
    "github.com/stretchr/testify/suite"
)

type ExampleSuite struct {
    suite.Suite
    db *sql.DB
}

func (s *ExampleSuite) SetupTest() {
    s.db = setupTestDB()
}

func (s *ExampleSuite) TearDownTest() {
    s.db.Close()
}

func (s *ExampleSuite) TestInsert() {
    err := Insert(s.db, "data")
    s.NoError(err)
}

func (s *ExampleSuite) TestQuery() {
    result := Query(s.db)
    s.NotEmpty(result)
}

func TestExampleSuite(t *testing.T) {
    suite.Run(t, new(ExampleSuite))
}
```

**Tip**: Use `SetupSuite`/`TearDownSuite` for one-time setup, `SetupTest`/`TearDownTest` for per-test setup.

---

## Parallel Tests

**Problem**: How to speed up test execution by running independent tests concurrently?

**Solution**:
```go
func TestParallel(t *testing.T) {
    tests := []struct {
        name  string
        input int
    }{
        {"case1", 1},
        {"case2", 2},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            result := Process(tt.input)
            assert.NotZero(t, result)
        })
    }
}
```

**Tip**: In Go 1.22+, loop variable capture is automatic. For earlier versions, add `tt := tt` before the subtest.

---

## Benchmarks

**Problem**: How to measure and compare performance of functions?

**Solution**:
```go
func BenchmarkProcess(b *testing.B) {
    data := setupData()
    b.ResetTimer() // Exclude setup time

    for i := 0; i < b.N; i++ {
        Process(data)
    }
}

// With memory allocation reporting
func BenchmarkAlloc(b *testing.B) {
    b.ReportAllocs()
    for i := 0; i < b.N; i++ {
        _ = make([]byte, 1024)
    }
}

// Sub-benchmarks for different sizes
func BenchmarkSizes(b *testing.B) {
    for _, size := range []int{10, 100, 1000} {
        b.Run(fmt.Sprintf("size-%d", size), func(b *testing.B) {
            data := make([]int, size)
            for i := 0; i < b.N; i++ {
                Process(data)
            }
        })
    }
}
```

**Tip**: Run with `go test -bench=. -benchmem` to see memory allocations per operation.

---

## Fuzz Testing

**Problem**: How to find edge cases and bugs by testing with random inputs?

**Solution**:
```go
func FuzzParse(f *testing.F) {
    // Seed corpus with known inputs
    f.Add("hello")
    f.Add("123")
    f.Add("")

    f.Fuzz(func(t *testing.T, input string) {
        result, err := Parse(input)
        if err != nil {
            return // Expected for some inputs
        }
        // Check invariants
        if result < 0 {
            t.Errorf("negative result for input %q", input)
        }
    })
}
```

**Tip**: Run with `go test -fuzz=FuzzParse -fuzztime=30s`. Failing inputs are saved to `testdata/fuzz/`.

---

## Test Helpers

**Problem**: How to create reusable test utilities with proper error reporting?

**Solution**:
```go
func assertJSON(t *testing.T, expected, actual any) {
    t.Helper() // Reports caller's line on failure

    exp, _ := json.Marshal(expected)
    act, _ := json.Marshal(actual)
    if !bytes.Equal(exp, act) {
        t.Errorf("JSON mismatch:\nexpected: %s\nactual: %s", exp, act)
    }
}

// Cleanup helper
func TestWithTempFile(t *testing.T) {
    f, err := os.CreateTemp("", "test")
    require.NoError(t, err)
    t.Cleanup(func() { os.Remove(f.Name()) })

    // Test using file...
}
```

**Tip**: Always call `t.Helper()` first in helper functions - it ensures error messages point to the test, not the helper.

---

## HTTP Handler Testing

**Problem**: How to test HTTP handlers without starting a real server?

**Solution**:
```go
import (
    "net/http"
    "net/http/httptest"
)

func TestHandler(t *testing.T) {
    req := httptest.NewRequest("GET", "/users/123", nil)
    rec := httptest.NewRecorder()

    handler := NewUserHandler()
    handler.ServeHTTP(rec, req)

    assert.Equal(t, http.StatusOK, rec.Code)
    assert.Contains(t, rec.Body.String(), "user")
}
```

**Tip**: Use `httptest.NewServer` when you need to test actual HTTP client code against a mock server.

---

## HTTP Client Testing

**Problem**: How to test code that makes HTTP requests to external services?

**Solution**:
```go
func TestClient(t *testing.T) {
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        assert.Equal(t, "/api/users", r.URL.Path)
        w.WriteHeader(http.StatusOK)
        w.Write([]byte(`{"status": "ok"}`))
    }))
    defer server.Close()

    client := NewClient(server.URL)
    result, err := client.Get()

    assert.NoError(t, err)
    assert.Equal(t, "ok", result.Status)
}
```

**Tip**: The test server URL is `server.URL` - pass it to your client instead of the real API URL.
