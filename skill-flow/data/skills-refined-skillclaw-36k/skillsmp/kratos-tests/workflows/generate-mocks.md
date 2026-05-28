# Workflow: Generate Mock Implementations

<required_reading>
**Read**: references/mock-patterns.md
</required_reading>

<process>
## Step 1: Identify Interface

Ask user or infer from context:
- Which interface to mock?
- Where is it defined? (internal/biz/interfaces.go usually)

## Step 2: Read Interface Definition

Read the file containing the interface to get:
- Interface name
- Method signatures
- Parameter types
- Return types

Example:
```go
type SymbolRepo interface {
    Create(ctx context.Context, symbol *Symbol) (*Symbol, error)
    Update(ctx context.Context, symbol *Symbol) (*Symbol, error)
    FindByID(ctx context.Context, id uint64) (*Symbol, error)
    // ...
}
```

## Step 3: Determine Mock Location

Mocks go in test files that use them:
- Repository interfaces → mocked in biz layer tests
- UseCase interfaces → mocked in service layer tests

Ask: "Where will this mock be used?"

## Step 4: Generate Mock Struct

Create testify/mock implementation:

```go
type Mock{InterfaceName} struct {
    mock.Mock
}

func (m *Mock{InterfaceName}) MethodName(params) (returns) {
    args := m.Called(params)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*Type), args.Error(1)
}
```

**For each method:**
1. Implement with `m.Called(params)`
2. Handle nil return values
3. Type assert non-error returns
4. Return error from args.Error(N)

## Step 5: Add Compile-Time Check

Add interface verification:

```go
var _ InterfaceName = (*MockInterfaceName)(nil)
```

This ensures mock implements interface correctly.

## Step 6: Write Mock

Write the mock implementation to the appropriate test file or show it to the user.

## Step 7: Verify

If written to file, run:

```bash
cd {service-directory}
go build ./...
```

Verify no compilation errors.
</process>

<success_criteria>
- [ ] Interface identified and read
- [ ] Mock struct generated with all methods
- [ ] Each method uses testify/mock.Called pattern
- [ ] Nil return values handled correctly
- [ ] Compile-time interface check added
- [ ] Mock compiles without errors
</success_criteria>