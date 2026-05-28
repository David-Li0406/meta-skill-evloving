# Service Layer Testing Patterns

Testing patterns for `internal/service/*` gRPC/HTTP service implementations and mapper functions.

<overview>
Service layer tests verify proto message handling, request/response mapping, and service handlers. They use testify/mock to mock use case dependencies and never touch business logic or database directly.
</overview>

<test_structure>
## Standard Service Layer Test File Structure

```go
package service

import (
    "context"
    "errors"
    "testing"
    v1 "symbol-service/api/symbols/v1"
    "{service}/internal/biz"
    "{service}/internal/pkg/pagination"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// Mock use case
type mockXUseCase struct {
    mock.Mock
}

// Mock use case methods
func (uc *mockXUseCase) GetX(ctx context.Context, id uint64) (*biz.X, error) { ... }
func (uc *mockXUseCase) CreateX(ctx context.Context, x *biz.X) (*biz.X, error) { ... }
// ... other methods

// Test functions for service handlers
func TestCreateX(t *testing.T) { ... }
func TestGetX(t *testing.T) { ... }
func TestUpdateX(t *testing.T) { ... }
func TestDeleteX(t *testing.T) { ... }
func TestListX(t *testing.T) { ... }
```
</test_structure>

<mock_usecase>
## Mock UseCase Pattern

```go
type mockSymbolUseCase struct {
    mock.Mock
}

func (uc *mockSymbolUseCase) GetSymbol(ctx context.Context, id uint64) (*biz.Symbol, error) {
    args := uc.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*biz.Symbol), args.Error(1)
}

func (uc *mockSymbolUseCase) CreateSymbol(ctx context.Context, symbol *biz.Symbol) (*biz.Symbol, error) {
    args := uc.Called(ctx, symbol)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*biz.Symbol), args.Error(1)
}

func (uc *mockSymbolUseCase) UpdateSymbol(ctx context.Context, symbol *biz.Symbol) (*biz.Symbol, error) {
    args := uc.Called(ctx, symbol)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*biz.Symbol), args.Error(1)
}

func (uc *mockSymbolUseCase) DeleteSymbol(ctx context.Context, id uint64) error {
    args := uc.Called(ctx, id)
    return args.Error(0)
}

func (uc *mockSymbolUseCase) ListSymbols(ctx context.Context, options *biz.ListSymbolsOptions) ([]*biz.Symbol, *pagination.PaginationMeta, error) {
    args := uc.Called(ctx, options)
    if args.Get(0) == nil {
        return nil, nil, args.Error(2)
    }
    if args.Get(1) == nil {
        return args.Get(0).([]*biz.Symbol), nil, args.Error(2)
    }
    return args.Get(0).([]*biz.Symbol), args.Get(1).(*pagination.PaginationMeta), args.Error(2)
}
```

Same pattern as repository mocks, but for use case interfaces.
</mock_usecase>

<test_patterns>
## Create Service Handler Test

```go
func TestCreateSymbol(t *testing.T) {
    tests := []struct {
        name        string
        request     *v1.CreateSymbolRequest
        mockSetup   func(*mockSymbolUseCase, context.Context, *v1.CreateSymbolRequest)
        wantErr     bool
        checkResult func(*testing.T, *v1.CreateSymbolResponse)
    }{
        {
            name: "success",
            request: &v1.CreateSymbolRequest{
                ProjectId:       1,
                Uid:             "550e8400-e29b-41d4-a716-446655440000",
                Label:           "Test Symbol",
                ClassName:       "TestClass",
                ComponentTarget: "component",
                Version:         1,
                Data:            []byte("test data"),
            },
            mockSetup: func(uc *mockSymbolUseCase, ctx context.Context, req *v1.CreateSymbolRequest) {
                input := SymbolFromCreateRequest(req)
                output := &biz.Symbol{
                    Id:              1,
                    Project:         req.ProjectId,
                    Uid:             req.Uid,
                    Label:           req.Label,
                    ClassName:       req.ClassName,
                    ComponentTarget: req.ComponentTarget,
                    Version:         req.Version,
                    Data: &biz.SymbolData{
                        Id:      1,
                        Project: req.ProjectId,
                        Data:    &req.Data,
                    },
                }
                uc.On("CreateSymbol", ctx, input).Return(output, nil)
            },
            wantErr: false,
            checkResult: func(t *testing.T, resp *v1.CreateSymbolResponse) {
                assert.NotNil(t, resp)
                assert.NotNil(t, resp.Symbol)
                assert.Equal(t, uint64(1), resp.Symbol.Id)
                assert.Equal(t, "Test Symbol", resp.Symbol.Label)
            },
        },
        {
            name: "use case error",
            request: &v1.CreateSymbolRequest{
                ProjectId:       1,
                Uid:             "550e8400-e29b-41d4-a716-446655440000",
                Label:           "Test Symbol",
                ClassName:       "TestClass",
                ComponentTarget: "component",
                Version:         1,
                Data:            []byte("test data"),
            },
            mockSetup: func(uc *mockSymbolUseCase, ctx context.Context, req *v1.CreateSymbolRequest) {
                input := SymbolFromCreateRequest(req)
                uc.On("CreateSymbol", ctx, input).Return(nil, errors.New("database error"))
            },
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            uc := &mockSymbolUseCase{}
            service := &SymbolService{uc: uc}
            ctx := context.Background()

            tt.mockSetup(uc, ctx, tt.request)

            result, err := service.CreateSymbol(ctx, tt.request)

            if tt.wantErr {
                assert.Error(t, err)
                assert.Nil(t, result)
            } else {
                assert.NoError(t, err)
                if tt.checkResult != nil {
                    tt.checkResult(t, result)
                }
            }

            uc.AssertExpectations(t)
        })
    }
}
```

**Key patterns:**
- Use mapper functions: `SymbolFromCreateRequest(req)`
- Mock expects mapped input: `uc.On("CreateSymbol", ctx, input)`
- Return biz domain object from mock
- Check proto response fields
</test_patterns>

<get_test_pattern>
## Get Service Handler Test

```go
func TestGetSymbol(t *testing.T) {
    tests := []struct {
        name        string
        request     *v1.GetSymbolRequest
        mockSetup   func(*mockSymbolUseCase, context.Context, *v1.GetSymbolRequest)
        wantErr     bool
        checkResult func(*testing.T, *v1.GetSymbolResponse)
    }{
        {
            name: "success",
            request: &v1.GetSymbolRequest{
                Id: 1,
            },
            mockSetup: func(uc *mockSymbolUseCase, ctx context.Context, req *v1.GetSymbolRequest) {
                data := []byte("test data")
                symbol := &biz.Symbol{
                    Id:              1,
                    Project:         1,
                    Uid:             "550e8400-e29b-41d4-a716-446655440000",
                    Label:           "Test Symbol",
                    ClassName:       "TestClass",
                    ComponentTarget: "component",
                    Version:         1,
                    Data: &biz.SymbolData{
                        Id:      1,
                        Project: 1,
                        Data:    &data,
                    },
                }
                uc.On("GetSymbol", ctx, req.Id).Return(symbol, nil)
            },
            wantErr: false,
            checkResult: func(t *testing.T, resp *v1.GetSymbolResponse) {
                assert.NotNil(t, resp)
                assert.NotNil(t, resp.Symbol)
                assert.Equal(t, uint64(1), resp.Symbol.Id)
                assert.Equal(t, "Test Symbol", resp.Symbol.Label)
                assert.NotEmpty(t, resp.Symbol.Data)
            },
        },
        {
            name: "not found error",
            request: &v1.GetSymbolRequest{
                Id: 999,
            },
            mockSetup: func(uc *mockSymbolUseCase, ctx context.Context, req *v1.GetSymbolRequest) {
                uc.On("GetSymbol", ctx, req.Id).Return(nil, errors.New("symbol not found"))
            },
            wantErr: true,
        },
        {
            name: "success with nil data",
            request: &v1.GetSymbolRequest{
                Id: 1,
            },
            mockSetup: func(uc *mockSymbolUseCase, ctx context.Context, req *v1.GetSymbolRequest) {
                symbol := &biz.Symbol{
                    Id:              1,
                    Project:         1,
                    Uid:             "550e8400-e29b-41d4-a716-446655440000",
                    Label:           "Test Symbol",
                    ClassName:       "TestClass",
                    ComponentTarget: "component",
                    Version:         1,
                    Data:            nil,
                }
                uc.On("GetSymbol", ctx, req.Id).Return(symbol, nil)
            },
            wantErr: false,
            checkResult: func(t *testing.T, resp *v1.GetSymbolResponse) {
                assert.NotNil(t, resp)
                assert.NotNil(t, resp.Symbol)
                assert.Nil(t, resp.Symbol.Data)
            },
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            uc := &mockSymbolUseCase{}
            service := &SymbolService{uc: uc}
            ctx := context.Background()

            tt.mockSetup(uc, ctx, tt.request)

            result, err := service.GetSymbol(ctx, tt.request)

            if tt.wantErr {
                assert.Error(t, err)
                assert.Nil(t, result)
            } else {
                assert.NoError(t, err)
                if tt.checkResult != nil {
                    tt.checkResult(t, result)
                }
            }

            uc.AssertExpectations(t)
        })
    }
}
```

**Test with and without nested data** - Verify nil Data field handled correctly
</get_test_pattern>

<list_test_pattern>
## List Service Handler Test

```go
func TestListSymbols(t *testing.T) {
    tests := []struct {
        name        string
        request     *v1.ListSymbolsRequest
        mockSetup   func(*mockSymbolUseCase, context.Context, *v1.ListSymbolsRequest)
        wantErr     bool
        checkResult func(*testing.T, *v1.ListSymbolsResponse)
    }{
        {
            name: "success with empty results",
            request: &v1.ListSymbolsRequest{
                ProjectId: 1,
                Limit:     10,
            },
            mockSetup: func(uc *mockSymbolUseCase, ctx context.Context, req *v1.ListSymbolsRequest) {
                options, _ := NewListSymbolsOptions(req)
                meta := &pagination.PaginationMeta{
                    TotalCount:      0,
                    Offset:          0,
                    Limit:           10,
                    HasNextPage:     false,
                    HasPreviousPage: false,
                }
                uc.On("ListSymbols", ctx, options).Return([]*biz.Symbol{}, meta, nil)
            },
            wantErr: false,
            checkResult: func(t *testing.T, resp *v1.ListSymbolsResponse) {
                assert.NotNil(t, resp)
                assert.Empty(t, resp.Symbols)
                assert.NotNil(t, resp.Pagination)
                assert.Equal(t, uint64(0), resp.Pagination.TotalCount)
            },
        },
        {
            name: "success with pagination - second page",
            request: &v1.ListSymbolsRequest{
                ProjectId: 1,
                Offset:    10,
                Limit:     10,
            },
            mockSetup: func(uc *mockSymbolUseCase, ctx context.Context, req *v1.ListSymbolsRequest) {
                options, _ := NewListSymbolsOptions(req)
                meta := &pagination.PaginationMeta{
                    TotalCount:      25,
                    Offset:          10,
                    Limit:           10,
                    HasNextPage:     true,
                    HasPreviousPage: true,
                }
                uc.On("ListSymbols", ctx, options).Return([]*biz.Symbol{}, meta, nil)
            },
            wantErr: false,
            checkResult: func(t *testing.T, resp *v1.ListSymbolsResponse) {
                assert.NotNil(t, resp)
                assert.NotNil(t, resp.Pagination)
                assert.True(t, resp.Pagination.HasNextPage)
                assert.True(t, resp.Pagination.HasPreviousPage)
            },
        },
    }
}
```

**Test pagination scenarios:**
- Empty results
- First page
- Middle page
- Last page
</list_test_pattern>

<mapper_tests>
## Mapper Function Tests

Test proto ↔ domain conversions separately:

```go
func Test_toBizSymbol(t *testing.T) {
    data := []byte(`{"key": "value"}`)

    tests := []struct {
        name     string
        input    *v1.Symbol
        expected *biz.Symbol
    }{
        {
            name: "complete symbol conversion",
            input: &v1.Symbol{
                Id:              123,
                ProjectId:       456,
                Uid:             "550e8400-e29b-41d4-a716-446655440000",
                Label:           "Test Symbol",
                ClassName:       "TestClass",
                ComponentTarget: "web",
                Version:         1,
                Data:            data,
            },
            expected: &biz.Symbol{
                Id:              123,
                Project:         456,
                Uid:             "550e8400-e29b-41d4-a716-446655440000",
                Label:           "Test Symbol",
                ClassName:       "TestClass",
                ComponentTarget: "web",
                Version:         1,
                Data: &biz.SymbolData{
                    Project: 456,
                    Data:    &data,
                },
            },
        },
        {
            name: "symbol with empty data",
            input: &v1.Symbol{
                Id:              1,
                ProjectId:       2,
                Uid:             "550e8400-e29b-41d4-a716-446655440001",
                Label:           "Empty Data Symbol",
                ClassName:       "EmptyClass",
                ComponentTarget: "mobile",
                Version:         1,
                Data:            []byte{},
            },
            expected: &biz.Symbol{
                Id:              1,
                Project:         2,
                Uid:             "550e8400-e29b-41d4-a716-446655440001",
                Label:           "Empty Data Symbol",
                ClassName:       "EmptyClass",
                ComponentTarget: "mobile",
                Version:         1,
                Data: &biz.SymbolData{
                    Project: 2,
                    Data:    &[]byte{},
                },
            },
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := toBizSymbol(tt.input)

            assert.Equal(t, tt.expected.Id, result.Id)
            assert.Equal(t, tt.expected.Project, result.Project)
            assert.Equal(t, tt.expected.Uid, result.Uid)
            // ... assert all fields
        })
    }
}

func Test_toV1Symbol(t *testing.T) {
    // Mirror pattern for biz → proto conversion
}
```

**Mapper test structure:**
- Test complete objects
- Test with empty/nil nested data
- Test field name conversions (ProjectId ↔ Project)
- Assert all fields individually
</mapper_tests>

<best_practices>
## Service Layer Testing Best Practices

1. **Mock use cases only** - Never mock repositories or touch database
2. **Use mapper functions** - Don't inline conversion logic in mocks
3. **Test proto validation** - Proto validate tags tested automatically
4. **Test nil nested data** - Verify Data fields can be nil
5. **Test pagination metadata** - Verify all pagination fields in list responses
6. **Assert response structure** - Check all response fields populated correctly
7. **Keep service tests thin** - Business logic tested in biz layer
8. **Test mapper functions separately** - Unit test conversions
9. **Match request/response** - Use correct v1.{Operation}Request/Response types
10. **Initialize service correctly** - `&SymbolService{uc: uc}` pattern
</best_practices>