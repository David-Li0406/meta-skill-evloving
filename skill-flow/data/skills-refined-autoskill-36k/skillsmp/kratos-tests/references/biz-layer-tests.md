# Biz Layer Testing Patterns

Testing patterns for `internal/biz/*` business logic and use case implementations.

<overview>
Biz layer tests verify business logic, validation rules, and use case orchestration. They use testify/mock to mock repository dependencies and never touch the database directly.
</overview>

<test_structure>
## Standard Biz Layer Test File Structure

```go
package biz

import (
    "context"
    "errors"
    "fmt"
    "os"
    "testing"
    "{service}/internal/pkg/pagination"

    "github.com/go-kratos/kratos/v2/log"
    "github.com/go-playground/validator/v10"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// Mock repository
type MockXRepo struct {
    mock.Mock
}

// Mock repository methods
func (m *MockXRepo) Create(ctx context.Context, x *X) (*X, error) { ... }
func (m *MockXRepo) Update(ctx context.Context, x *X) (*X, error) { ... }
// ... other methods

// Helper to create use case with mock
func setupXUseCase(mockRepo *MockXRepo) XUseCase { ... }

// Helper to create valid domain object
func validX() *X { ... }

// Test functions
func TestGetX(t *testing.T) { ... }
func TestCreateX(t *testing.T) { ... }
func TestUpdateX(t *testing.T) { ... }
func TestDeleteX(t *testing.T) { ... }
func TestListX(t *testing.T) { ... }
```
</test_structure>

<mock_repository>
## Mock Repository Pattern

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

func (m *MockSymbolRepo) ListSymbols(ctx context.Context, options *ListSymbolsOptions) ([]*Symbol, *pagination.PaginationMeta, error) {
    args := m.Called(ctx, options)
    if args.Get(0) == nil {
        return nil, nil, args.Error(2)
    }
    if args.Get(1) == nil {
        return args.Get(0).([]*Symbol), nil, args.Error(2)
    }
    return args.Get(0).([]*Symbol), args.Get(1).(*pagination.PaginationMeta), args.Error(2)
}

func (m *MockSymbolRepo) Delete(ctx context.Context, id uint64) error {
    args := m.Called(ctx, id)
    return args.Error(0)
}
```

**Key patterns:**
- Use `m.Called(params...)` to register call
- Check `args.Get(0) == nil` before type assertion
- Type assert non-error returns: `args.Get(0).(*Type)`
- Return errors with `args.Error(N)`
- For methods with multiple return values, handle each separately
</mock_repository>

<setup_helper>
## Setup Use Case Helper

```go
func setupSymbolUseCase(mockRepo *MockSymbolRepo) SymbolUseCase {
    logger := log.NewStdLogger(os.Stdout)
    v := NewSymbolValidator()
    return NewSymbolUseCase(mockRepo, v, nil, logger)
}
```

Creates use case with:
- Mock repository
- Real validator
- Optional transaction (usually nil)
- Logger
</setup_helper>

<valid_objects>
## Valid Domain Object Helper

```go
func validSymbol() *Symbol {
    bytes := []byte(`{"key": "value"}`)
    return &Symbol{
        Project:         1,
        Uid:             "550e8400-e29b-41d4-a716-446655440000",
        Label:           "Test Symbol",
        ClassName:       "TestClass",
        ComponentTarget: "TestTarget",
        Version:         1,
        Data:            &SymbolData{Project: 1, Data: &bytes},
    }
}
```
</valid_objects>

<test_patterns>
## Get/FindByID Test Pattern

```go
func TestGetSymbol(t *testing.T) {
    tests := []struct {
        name        string
        symbolID    uint64
        mockSetup   func(*MockSymbolRepo, context.Context, uint64)
        wantErr     bool
        checkResult func(*testing.T, *Symbol)
    }{
        {
            name:     "success",
            symbolID: 1,
            mockSetup: func(repo *MockSymbolRepo, ctx context.Context, id uint64) {
                symbol := validSymbol()
                symbol.Id = id
                repo.On("FindByID", ctx, id).Return(symbol, nil)
            },
            wantErr: false,
            checkResult: func(t *testing.T, result *Symbol) {
                assert.NotNil(t, result)
                assert.Equal(t, uint64(1), result.Id)
            },
        },
        {
            name:     "not found",
            symbolID: 999,
            mockSetup: func(repo *MockSymbolRepo, ctx context.Context, id uint64) {
                repo.On("FindByID", ctx, id).Return(nil, ErrNotFound)
            },
            wantErr: true,
        },
        {
            name:     "repository error",
            symbolID: 1,
            mockSetup: func(repo *MockSymbolRepo, ctx context.Context, id uint64) {
                repo.On("FindByID", ctx, id).Return(nil, fmt.Errorf("%w: connection failed", ErrDatabase))
            },
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            mockRepo := new(MockSymbolRepo)
            uc := setupSymbolUseCase(mockRepo)
            ctx := context.Background()

            tt.mockSetup(mockRepo, ctx, tt.symbolID)

            result, err := uc.GetSymbol(ctx, tt.symbolID)

            if tt.wantErr {
                assert.Error(t, err)
                assert.Nil(t, result)
            } else {
                assert.NoError(t, err)
                if tt.checkResult != nil {
                    tt.checkResult(t, result)
                }
            }

            mockRepo.AssertExpectations(t)
        })
    }
}
```

**Key elements:**
- `mockSetup` function configures mock expectations
- Create new mock for each test: `new(MockSymbolRepo)`
- Call `mockRepo.AssertExpectations(t)` at end
- Test success, not found, and other errors
</test_patterns>

<create_test_pattern>
## Create Test Pattern

Focus on validation:

```go
func TestCreateSymbol(t *testing.T) {
    tests := []struct {
        name        string
        symbol      *Symbol
        mockSetup   func(*MockSymbolRepo, context.Context, *Symbol)
        wantErr     bool
        errContains string
        checkResult func(*testing.T, *Symbol)
    }{
        {
            name:   "success",
            symbol: validSymbol(),
            mockSetup: func(repo *MockSymbolRepo, ctx context.Context, symbol *Symbol) {
                expected := &Symbol{
                    Id:              1,
                    Project:         symbol.Project,
                    Uid:             symbol.Uid,
                    Label:           symbol.Label,
                    // ... other fields
                }
                repo.On("Create", ctx, mock.AnythingOfType("*biz.Symbol")).Return(expected, nil)
            },
            wantErr: false,
        },
        {
            name: "missing required field - project",
            symbol: &Symbol{
                Uid:             "550e8400-e29b-41d4-a716-446655440000",
                Label:           "Test",
                ClassName:       "Class",
                ComponentTarget: "Target",
                Version:         1,
            },
            mockSetup:   func(repo *MockSymbolRepo, ctx context.Context, symbol *Symbol) {},
            wantErr:     true,
            errContains: "Project",
        },
        {
            name: "invalid uuid format",
            symbol: &Symbol{
                Project:         1,
                Uid:             "invalid-uuid",
                Label:           "Test",
                ClassName:       "Class",
                ComponentTarget: "Target",
                Version:         1,
            },
            mockSetup:   func(repo *MockSymbolRepo, ctx context.Context, symbol *Symbol) {},
            wantErr:     true,
            errContains: "Uid",
        },
        {
            name:   "repository error",
            symbol: validSymbol(),
            mockSetup: func(repo *MockSymbolRepo, ctx context.Context, symbol *Symbol) {
                repo.On("Create", ctx, mock.AnythingOfType("*biz.Symbol")).Return(nil, fmt.Errorf("%w: connection failed", ErrDatabase))
            },
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            mockRepo := new(MockSymbolRepo)
            uc := setupSymbolUseCase(mockRepo)
            ctx := context.Background()

            tt.mockSetup(mockRepo, ctx, tt.symbol)

            result, err := uc.CreateSymbol(ctx, tt.symbol)

            if tt.wantErr {
                assert.Error(t, err)
                assert.Nil(t, result)
                if tt.errContains != "" {
                    assert.Contains(t, err.Error(), tt.errContains)
                }
            } else {
                assert.NoError(t, err)
                if tt.checkResult != nil {
                    tt.checkResult(t, result)
                }
            }

            mockRepo.AssertExpectations(t)
        })
    }
}
```

**Validation test cases:**
- Test each required field individually
- Test format validation (UUID, email, etc.)
- Test length constraints
- Test business rule violations
- Use `errContains` to verify correct validation message
</create_test_pattern>

<update_test_pattern>
## Update Test Pattern

```go
func TestUpdateSymbol(t *testing.T) {
    tests := []struct {
        name        string
        symbol      *Symbol
        mockSetup   func(*MockSymbolRepo, context.Context, *Symbol)
        wantErr     bool
        checkResult func(*testing.T, *Symbol)
    }{
        {
            name: "success",
            symbol: func() *Symbol {
                s := validSymbol()
                s.Id = 1
                return s
            }(),
            mockSetup: func(repo *MockSymbolRepo, ctx context.Context, symbol *Symbol) {
                repo.On("Update", ctx, mock.AnythingOfType("*biz.Symbol")).Return(symbol, nil)
            },
            wantErr: false,
        },
        {
            name: "validation error",
            symbol: func() *Symbol {
                s := validSymbol()
                s.Id = 1
                s.Label = "" // Invalid
                return s
            }(),
            mockSetup: func(repo *MockSymbolRepo, ctx context.Context, symbol *Symbol) {},
            wantErr:   true,
        },
        {
            name: "not found error",
            symbol: func() *Symbol {
                s := validSymbol()
                s.Id = 999
                return s
            }(),
            mockSetup: func(repo *MockSymbolRepo, ctx context.Context, symbol *Symbol) {
                repo.On("Update", ctx, mock.AnythingOfType("*biz.Symbol")).Return(nil, ErrNotFound)
            },
            wantErr: true,
        },
    }
}
```
</update_test_pattern>

<delete_test_pattern>
## Delete Test Pattern

```go
func TestDeleteSymbol(t *testing.T) {
    tests := []struct {
        name        string
        symbolID    uint64
        mockSetup   func(*MockSymbolRepo, context.Context, uint64)
        wantErr     bool
        errContains string
    }{
        {
            name:     "success",
            symbolID: 1,
            mockSetup: func(repo *MockSymbolRepo, ctx context.Context, id uint64) {
                repo.On("Delete", ctx, id).Return(nil)
            },
            wantErr: false,
        },
        {
            name:        "zero id",
            symbolID:    0,
            mockSetup:   func(repo *MockSymbolRepo, ctx context.Context, id uint64) {},
            wantErr:     true,
            errContains: "invalid",
        },
        {
            name:     "not found error",
            symbolID: 999,
            mockSetup: func(repo *MockSymbolRepo, ctx context.Context, id uint64) {
                repo.On("Delete", ctx, id).Return(ErrNotFound)
            },
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            mockRepo := new(MockSymbolRepo)
            uc := setupSymbolUseCase(mockRepo)
            ctx := context.Background()

            tt.mockSetup(mockRepo, ctx, tt.symbolID)

            err := uc.DeleteSymbol(ctx, tt.symbolID)

            if tt.wantErr {
                assert.Error(t, err)
                if tt.errContains != "" {
                    assert.Contains(t, err.Error(), tt.errContains)
                }
            } else {
                assert.NoError(t, err)
            }

            mockRepo.AssertExpectations(t)
        })
    }
}
```
</delete_test_pattern>

<list_test_pattern>
## List Test Pattern

```go
func TestListSymbols(t *testing.T) {
    tests := []struct {
        name        string
        options     *ListSymbolsOptions
        mockSetup   func(*MockSymbolRepo, context.Context, *ListSymbolsOptions)
        wantErr     bool
        errContains string
        checkResult func(*testing.T, []*Symbol, *pagination.PaginationMeta)
    }{
        {
            name: "success - first page",
            options: &ListSymbolsOptions{
                ProjectID: 1,
                Pagination: pagination.PaginationParams{
                    Offset: 0,
                    Limit:  10,
                },
            },
            mockSetup: func(repo *MockSymbolRepo, ctx context.Context, options *ListSymbolsOptions) {
                symbols := []*Symbol{validSymbol()}
                meta := &pagination.PaginationMeta{
                    TotalCount:      1,
                    Offset:          0,
                    Limit:           10,
                    HasNextPage:     false,
                    HasPreviousPage: false,
                }
                repo.On("ListSymbols", ctx, options).Return(symbols, meta, nil)
            },
            wantErr: false,
            checkResult: func(t *testing.T, symbols []*Symbol, meta *pagination.PaginationMeta) {
                assert.Len(t, symbols, 1)
                assert.Equal(t, uint64(1), meta.TotalCount)
                assert.False(t, meta.HasNextPage)
            },
        },
        {
            name: "missing project id",
            options: &ListSymbolsOptions{
                ProjectID: 0,
                Pagination: pagination.PaginationParams{
                    Offset: 0,
                    Limit:  10,
                },
            },
            mockSetup:   func(repo *MockSymbolRepo, ctx context.Context, options *ListSymbolsOptions) {},
            wantErr:     true,
            errContains: "ProjectID",
        },
    }
}
```
</list_test_pattern>

<best_practices>
## Biz Layer Testing Best Practices

1. **Always use mocks** - Never access database directly in biz tests
2. **Create new mock per test** - `new(MockXRepo)` prevents test pollution
3. **Assert expectations** - Always call `mockRepo.AssertExpectations(t)`
4. **Test validation thoroughly** - Each required field, format, constraint
5. **Use `mock.AnythingOfType()`** - When exact value doesn't matter: `mock.AnythingOfType("*biz.Symbol")`
6. **Test error propagation** - Verify repository errors bubble up correctly
7. **Use errContains** - Check error messages contain expected field name
8. **Test business rules** - Not just validation, but business logic constraints
9. **Test with and without nested data** - Verify optional nested objects work
10. **Setup validation once** - Use real validator (NewSymbolValidator()) not mock
</best_practices>