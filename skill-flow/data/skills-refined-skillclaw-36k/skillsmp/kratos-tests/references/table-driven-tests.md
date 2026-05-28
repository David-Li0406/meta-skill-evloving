# Table-Driven Test Patterns

Structure and patterns for table-driven tests in Kratos microservices.

<overview>
All Kratos tests use table-driven patterns for systematic, comprehensive test coverage. Each test function defines a table of test cases with inputs, setup, and expected outcomes.
</overview>

<basic_structure>
## Basic Table-Driven Test Structure

```go
func TestSomething(t *testing.T) {
    tests := []struct {
        name    string         // Test case name
        input   InputType      // Input data
        wantErr bool           // Expect error?
    }{
        {
            name:    "success case",
            input:   validInput(),
            wantErr: false,
        },
        {
            name:    "error case",
            input:   invalidInput(),
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := functionUnderTest(tt.input)

            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}
```
</basic_structure>

<common_fields>
## Common Table Fields

### Required Fields

**name** - Descriptive test case name:
```go
name: "success with valid input"
name: "validation error - missing required field"
name: "not found error"
name: "edge case - empty data"
```

**wantErr** - Whether error is expected:
```go
wantErr: false  // Success case
wantErr: true   // Error case
```

### Optional Fields

**setup** - Prepare dependencies before test:
```go
setup: func(db *gorm.DB) {
    // Insert test data
}

setup: func(repo *MockRepo, ctx context.Context, id uint64) {
    // Configure mock expectations
}
```

**checkError** - Verify specific error:
```go
checkError: func(t *testing.T, err error) {
    assert.ErrorIs(t, err, biz.ErrNotFound)
}
```

**checkResult** - Verify result details:
```go
checkResult: func(t *testing.T, result *Symbol) {
    assert.NotNil(t, result)
    assert.Equal(t, "expected", result.Field)
}
```

**errContains** - Check error message content:
```go
errContains: "ProjectID"  // Error must contain this string
```
</common_fields>

<layer_patterns>
## Layer-Specific Table Patterns

### Data Layer Table

```go
tests := []struct {
    name        string
    input       *biz.Symbol
    setup       func(*gorm.DB)  // Or func(*gorm.DB) uint64 for Update/Delete
    wantErr     bool
    checkError  func(*testing.T, error)
    checkResult func(*testing.T, *biz.Symbol)
}{
    // Test cases
}
```

### Biz Layer Table

```go
tests := []struct {
    name        string
    symbolID    uint64  // Or other input
    mockSetup   func(*MockSymbolRepo, context.Context, uint64)
    wantErr     bool
    errContains string
    checkResult func(*testing.T, *Symbol)
}{
    // Test cases
}
```

### Service Layer Table

```go
tests := []struct {
    name        string
    request     *v1.CreateSymbolRequest
    mockSetup   func(*mockSymbolUseCase, context.Context, *v1.CreateSymbolRequest)
    wantErr     bool
    checkResult func(*testing.T, *v1.CreateSymbolResponse)
}{
    // Test cases
}
```
</layer_patterns>

<test_case_patterns>
## Common Test Case Patterns

### Success Case

```go
{
    name:   "success",
    input:  validInput(),
    setup:  func(deps) { /* minimal or no setup */ },
    wantErr: false,
    checkResult: func(t *testing.T, result *Type) {
        assert.NotNil(t, result)
        assert.NotZero(t, result.Id)
        assert.Equal(t, "expected", result.Field)
    },
}
```

### Validation Error Case

```go
{
    name: "validation error - missing required field",
    input: func() *Type {
        x := validInput()
        x.RequiredField = "" // Make invalid
        return x
    }(),
    setup:       func(deps) {},  // No setup for validation errors
    wantErr:     true,
    errContains: "RequiredField",
}
```

### Not Found Error Case

```go
{
    name:  "not found error",
    input: 999,  // Non-existent ID
    setup: func(repo, ctx, id) {
        repo.On("FindByID", ctx, id).Return(nil, biz.ErrNotFound)
    },
    wantErr: true,
    checkError: func(t *testing.T, err error) {
        assert.ErrorIs(t, err, biz.ErrNotFound)
    },
}
```

### Edge Case - Nil/Empty Data

```go
{
    name: "success without nested data",
    input: func() *Symbol {
        s := validSymbol()
        s.Data = nil
        return s
    }(),
    setup:   func(deps) {},
    wantErr: false,
    checkResult: func(t *testing.T, result *Symbol) {
        assert.NotNil(t, result)
        assert.Nil(t, result.Data)
    },
}
```

### Database/Repository Error

```go
{
    name:  "repository error",
    input: validInput(),
    setup: func(repo, ctx, input) {
        repo.On("Create", ctx, input).Return(nil, fmt.Errorf("%w: connection failed", biz.ErrDatabase))
    },
    wantErr: true,
}
```
</test_case_patterns>

<test_execution>
## Test Execution Pattern

### Standard Execution Loop

```go
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        // 1. Setup dependencies
        db := setupTestDB(t)
        defer cleanupDB(db)

        // 2. Run test-specific setup
        tt.setup(db)

        // 3. Execute function under test
        result, err := functionUnderTest(tt.input)

        // 4. Assert error expectation
        if tt.wantErr {
            assert.Error(t, err)
            assert.Nil(t, result)
            if tt.checkError != nil {
                tt.checkError(t, err)
            }
        } else {
            assert.NoError(t, err)
            if tt.checkResult != nil {
                tt.checkResult(t, result)
            }
        }
    })
}
```

### With Mock Assertions

```go
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        mockRepo := new(MockSymbolRepo)
        uc := setupSymbolUseCase(mockRepo)
        ctx := context.Background()

        tt.mockSetup(mockRepo, ctx, tt.input)

        result, err := uc.CreateSymbol(ctx, tt.input)

        if tt.wantErr {
            assert.Error(t, err)
            assert.Nil(t, result)
        } else {
            assert.NoError(t, err)
        }

        // IMPORTANT: Always assert mock expectations
        mockRepo.AssertExpectations(t)
    })
}
```
</test_execution>

<naming_conventions>
## Test Case Naming Conventions

**Format:** `{outcome} [- {specifics}]`

### Success Cases
- `"success"` - Basic happy path
- `"success with nested data"` - Success with specific condition
- `"success without nested data"` - Success with edge case
- `"success - first page with next page"` - Success with specific scenario

### Error Cases
- `"validation error - missing required field"` - Validation failure
- `"not found error"` - Resource not found
- `"duplicate entry error"` - Constraint violation
- `"repository error"` - Dependency failure
- `"database error"` - Infrastructure failure

### Edge Cases
- `"edge case - nil input"` - Boundary condition
- `"edge case - empty data"` - Boundary condition
- `"edge case - zero id"` - Boundary condition

**Be specific**: Name should describe exactly what's being tested without needing to read the test case.
</naming_conventions>

<assertion_patterns>
## Assertion Patterns

### Error Assertions

```go
// Basic error check
assert.Error(t, err)
assert.NoError(t, err)

// Specific error type
assert.ErrorIs(t, err, biz.ErrNotFound)
assert.ErrorIs(t, err, biz.ErrDuplicateEntry)

// Error message content
assert.Contains(t, err.Error(), "ProjectID")
assert.Contains(t, err.Error(), "validation")
```

### Nil Checks

```go
// Result should exist
assert.NotNil(t, result)
assert.Nil(t, result)

// Nested data may be nil
assert.NotNil(t, result.Data)
assert.Nil(t, result.Data)
```

### Value Assertions

```go
// Equality
assert.Equal(t, expected, actual)
assert.Equal(t, "Test Symbol", result.Label)

// Numeric comparisons
assert.NotZero(t, result.Id)  // ID was assigned
assert.Equal(t, uint64(1), result.Id)

// Collections
assert.Len(t, symbols, 5)
assert.Empty(t, symbols)
assert.NotEmpty(t, symbols)
```

### Boolean Assertions

```go
// Pagination flags
assert.True(t, meta.HasNextPage)
assert.False(t, meta.HasPreviousPage)
```
</assertion_patterns>

<best_practices>
## Table-Driven Test Best Practices

1. **Descriptive names** - Test case name explains what's being tested
2. **One concern per test** - Each test case validates one scenario
3. **Comprehensive coverage** - Success, validation errors, edge cases, repository errors
4. **Setup isolation** - Each test case has its own setup function
5. **Check functions for detail** - Use checkResult/checkError for detailed assertions
6. **Anonymous functions for variations** - Start with validX(), modify specific field
7. **Consistent table structure** - Use same fields in same order across test files
8. **Run subtests** - Always use `t.Run(tt.name, func(t *testing.T) {...})`
9. **Assert mock expectations** - Call `mock.AssertExpectations(t)` for every test
10. **Clean up resources** - Use `defer cleanupDB(db)` for database tests
</best_practices>