# Mock Patterns with testify/mock

Patterns for creating and using testify/mock in Kratos tests.

<overview>
Testify/mock provides a powerful framework for mocking interfaces in Go. Kratos tests use mocks for repository interfaces (in biz layer) and use case interfaces (in service layer).
</overview>

<basic_mock>
## Basic Mock Structure

```go
import (
    "github.com/stretchr/testify/mock"
)

type MockInterface struct {
    mock.Mock
}

func (m *MockInterface) Method(params) (returns) {
    args := m.Called(params...)
    // Handle return values
}
```

**Key components:**
- Embed `mock.Mock`
- Implement all interface methods
- Use `m.Called(params...)` to register calls
- Extract return values from `args`
</basic_mock>

<return_patterns>
## Return Value Patterns

### Single Return Value (Non-Error)

```go
func (m *MockRepo) FindByID(ctx context.Context, id uint64) (*Symbol, error) {
    args := m.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*Symbol), args.Error(1)
}
```

**Pattern:**
1. Check if first return is nil
2. If nil, return nil + error
3. If not nil, type assert and return + error

### Single Error Return

```go
func (m *MockRepo) Delete(ctx context.Context, id uint64) error {
    args := m.Called(ctx, id)
    return args.Error(0)
}
```

**Pattern:**
- Use `args.Error(N)` for error at position N
- No nil check needed for error-only returns

### Multiple Non-Error Returns

```go
func (m *MockRepo) ListSymbols(ctx context.Context, options *ListSymbolsOptions) ([]*Symbol, *PaginationMeta, error) {
    args := m.Called(ctx, options)
    if args.Get(0) == nil {
        return nil, nil, args.Error(2)
    }
    if args.Get(1) == nil {
        return args.Get(0).([]*Symbol), nil, args.Error(2)
    }
    return args.Get(0).([]*Symbol), args.Get(1).(*PaginationMeta), args.Error(2)
}
```

**Pattern:**
1. Check first return (slice)
2. If nil, return nil for all non-errors
3. Check second return (pagination meta)
4. If nil, return first + nil + error
5. Otherwise return all with type assertions

### No Return Value (Void)

Rarely used, but if interface method returns nothing:

```go
func (m *MockRepo) SomeMethod(ctx context.Context) {
    m.Called(ctx)
}
```
</return_patterns>

<type_assertions>
## Type Assertions

Use `args.Get(N)` with type assertion for non-error returns:

```go
// Pointer types
return args.Get(0).(*Symbol)

// Slice types
return args.Get(0).([]*Symbol)

// Interface types
return args.Get(0).(SomeInterface)

// Concrete types (rare)
return args.Get(0).(int)
```

**Always check nil first** before type assertion to avoid panic:

```go
if args.Get(0) == nil {
    return nil, args.Error(1)
}
return args.Get(0).(*Symbol), args.Error(1)
```
</type_assertions>

<setting_expectations>
## Setting Mock Expectations

### Basic Expectation

```go
mockRepo.On("FindByID", ctx, uint64(1)).Return(symbol, nil)
```

**Pattern:** `On(methodName, ...args).Return(...returns)`

### With mock.Anything

```go
mockRepo.On("Create", ctx, mock.Anything).Return(symbol, nil)
```

Use when exact value doesn't matter.

### With mock.AnythingOfType

```go
mockRepo.On("Create", ctx, mock.AnythingOfType("*biz.Symbol")).Return(symbol, nil)
```

Use when type matters but specific value doesn't.

### Multiple Expectations

```go
// First call returns success
mockRepo.On("FindByID", ctx, uint64(1)).Return(symbol, nil).Once()

// Second call returns error
mockRepo.On("FindByID", ctx, uint64(1)).Return(nil, ErrNotFound).Once()
```

Use `.Once()`, `.Twice()`, or `.Times(n)` for call count expectations.

### Return Different Values

```go
mockRepo.On("FindByID", ctx, uint64(1)).Return(symbol, nil)
mockRepo.On("FindByID", ctx, uint64(999)).Return(nil, ErrNotFound)
```

Different args = different expectations.
</setting_expectations>

<repository_mock>
## Complete Repository Mock Example

```go
type MockSymbolRepo struct {
    mock.Mock
}

func (m *MockSymbolRepo) Create(ctx context.Context, symbol *Symbol) (*Symbol, error) {
    args := m.Called(ctx, symbol)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*Symbol), args.Error(1)
}

func (m *MockSymbolRepo) Update(ctx context.Context, symbol *Symbol) (*Symbol, error) {
    args := m.Called(ctx, symbol)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*Symbol), args.Error(1)
}

func (m *MockSymbolRepo) FindByID(ctx context.Context, id uint64) (*Symbol, error) {
    args := m.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*Symbol), args.Error(1)
}

func (m *MockSymbolRepo) ListSymbols(ctx context.Context, options *ListSymbolsOptions) ([]*Symbol, *PaginationMeta, error) {
    args := m.Called(ctx, options)
    if args.Get(0) == nil {
        return nil, nil, args.Error(2)
    }
    if args.Get(1) == nil {
        return args.Get(0).([]*Symbol), nil, args.Error(2)
    }
    return args.Get(0).([]*Symbol), args.Get(1).(*PaginationMeta), args.Error(2)
}

func (m *MockSymbolRepo) Delete(ctx context.Context, id uint64) error {
    args := m.Called(ctx, id)
    return args.Error(0)
}
```

Implements all methods of SymbolRepo interface.
</repository_mock>

<usecase_mock>
## Complete UseCase Mock Example

```go
type mockSymbolUseCase struct {
    mock.Mock
}

func (uc *mockSymbolUseCase) GetSymbol(ctx context.Context, id uint64) (*Symbol, error) {
    args := uc.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*Symbol), args.Error(1)
}

func (uc *mockSymbolUseCase) CreateSymbol(ctx context.Context, symbol *Symbol) (*Symbol, error) {
    args := uc.Called(ctx, symbol)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*Symbol), args.Error(1)
}

func (uc *mockSymbolUseCase) UpdateSymbol(ctx context.Context, symbol *Symbol) (*Symbol, error) {
    args := uc.Called(ctx, symbol)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*Symbol), args.Error(1)
}

func (uc *mockSymbolUseCase) DeleteSymbol(ctx context.Context, id uint64) error {
    args := uc.Called(ctx, id)
    return args.Error(0)
}

func (uc *mockSymbolUseCase) ListSymbols(ctx context.Context, options *ListSymbolsOptions) ([]*Symbol, *PaginationMeta, error) {
    args := uc.Called(ctx, options)
    if args.Get(0) == nil {
        return nil, nil, args.Error(2)
    }
    if args.Get(1) == nil {
        return args.Get(0).([]*Symbol), nil, args.Error(2)
    }
    return args.Get(0).([]*Symbol), args.Get(1).(*PaginationMeta), args.Error(2)
}
```

Same pattern as repository mocks.
</usecase_mock>

<compile_check>
## Compile-Time Interface Check

Always add after mock definition:

```go
type MockSymbolRepo struct {
    mock.Mock
}

// ... mock methods ...

// Compile-time interface check
var _ SymbolRepo = (*MockSymbolRepo)(nil)
```

This ensures:
- Mock implements all interface methods
- Method signatures match exactly
- Catches errors at compile time, not runtime

**Location:** After all mock methods, before test functions
</compile_check>

<assertion>
## Mock Assertion

Always assert expectations at end of each test:

```go
func TestSomething(t *testing.T) {
    mockRepo := new(MockSymbolRepo)

    // Setup expectations
    mockRepo.On("FindByID", ctx, uint64(1)).Return(symbol, nil)

    // Execute test
    result, err := usecase.GetSymbol(ctx, 1)

    // Assertions
    assert.NoError(t, err)
    assert.NotNil(t, result)

    // CRITICAL: Assert mock was called as expected
    mockRepo.AssertExpectations(t)
}
```

**What it checks:**
- All expected methods were called
- Called with correct arguments
- Called correct number of times

**Failure means:**
- Method not called when expected
- Called with wrong arguments
- Called too many or too few times
</assertion>

<common_patterns>
## Common Mock Setup Patterns

### Success Setup

```go
mockSetup: func(repo *MockSymbolRepo, ctx context.Context, id uint64) {
    symbol := validSymbol()
    symbol.Id = id
    repo.On("FindByID", ctx, id).Return(symbol, nil)
}
```

### Error Setup

```go
mockSetup: func(repo *MockSymbolRepo, ctx context.Context, id uint64) {
    repo.On("FindByID", ctx, id).Return(nil, ErrNotFound)
}
```

### With mock.AnythingOfType

```go
mockSetup: func(repo *MockSymbolRepo, ctx context.Context, symbol *Symbol) {
    expected := &Symbol{Id: 1, Label: symbol.Label}
    repo.On("Create", ctx, mock.AnythingOfType("*biz.Symbol")).Return(expected, nil)
}
```

Use when you care about type but not exact instance.
</common_patterns>

<best_practices>
## Mock Best Practices

1. **New mock per test** - `new(MockRepo)` prevents test pollution
2. **Embed mock.Mock** - Don't create custom mock base
3. **Check nil before type assert** - Prevents panics
4. **Use args.Error(N)** - For error returns
5. **Use args.Get(N).(*Type)** - For typed returns
6. **Always AssertExpectations** - Verify mocks were called correctly
7. **Compile-time checks** - `var _ Interface = (*Mock)(nil)`
8. **Specific expectations when possible** - Exact values better than mock.Anything
9. **One expectation per test case** - Keep setup functions focused
10. **Match return pattern to signature** - Multiple returns need multiple nil checks
</best_practices>