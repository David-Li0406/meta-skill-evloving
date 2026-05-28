# Test Helper Patterns

Common helper functions used across all Kratos test files.

<overview>
Test helpers reduce boilerplate and ensure consistent test setup. Each layer has specific helpers for its dependencies and test data.
</overview>

<setup_functions>
## Setup Functions

### Data Layer: setupTestDB

```go
func setupTestDB(t *testing.T) *gorm.DB {
    db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
    if err != nil {
        t.Fatalf("Failed to open in-memory SQLite database: %v", err)
    }

    // Run migrations for test tables
    if err := db.AutoMigrate(&model.Entity1{}, &model.Entity2{}); err != nil {
        t.Fatalf("Failed to migrate test tables: %v", err)
    }

    return db
}
```

**Usage:** Create isolated, fast in-memory database for each test file

### Biz Layer: setupXUseCase

```go
func setupSymbolUseCase(mockRepo *MockSymbolRepo) SymbolUseCase {
    logger := log.NewStdLogger(os.Stdout)
    v := NewSymbolValidator()
    return NewSymbolUseCase(mockRepo, v, nil, logger)
}
```

**Usage:** Create use case with mock repo and real validator

### Service Layer: Inline Creation

Service layer typically creates service inline:

```go
uc := &mockSymbolUseCase{}
service := &SymbolService{uc: uc}
```

No helper needed for simple struct initialization.
</setup_functions>

<cleanup_functions>
## Cleanup Functions

### Data Layer: cleanupDB

```go
func cleanupDB(db *gorm.DB) {
    db.Exec("DELETE FROM table1")
    db.Exec("DELETE FROM table2")
}
```

**Usage:** `defer cleanupDB(db)` after setupTestDB

**Note:** SQLite in-memory database is automatically destroyed when test ends, but explicit cleanup ensures isolation between subtests.
</cleanup_functions>

<valid_object_functions>
## Valid Object Functions

These return fully populated, valid objects for testing happy paths.

### Data Layer

**validDomainX** - Returns valid business domain object:

```go
func validDomainSymbol() *biz.Symbol {
    data := []byte(`{"key": "value"}`)
    return &biz.Symbol{
        Project:         1,
        Uid:             "550e8400-e29b-41d4-a716-446655440000",
        Label:           "Test Symbol",
        ClassName:       "TestClass",
        ComponentTarget: "TestTarget",
        Version:         1,
        Data: &biz.SymbolData{
            Project: 1,
            Data:    &data,
        },
    }
}
```

**validEntityX** - Returns valid GORM entity:

```go
func validEntitySymbol() *model.Symbol {
    data := []byte(`{"key": "value"}`)
    return &model.Symbol{
        ProjectID:       1,
        UID:             "550e8400-e29b-41d4-a716-446655440000",
        Label:           "Test Symbol",
        ClassName:       "TestClass",
        ComponentTarget: "TestTarget",
        Version:         1,
        SymbolData: &model.SymbolData{
            Data: &data,
        },
    }
}
```

**Key differences:**
- Domain uses `Uid`, entity uses `UID`
- Domain uses `Project`, entity uses `ProjectID`
- Entity omits Project from nested data (foreign key relationship)

### Biz Layer

**validX** - Returns valid domain object:

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

Same structure as data layer validDomainX but local to biz package.

### Service Layer

No valid object helpers typically needed - use request structs directly or create inline.
</valid_object_functions>

<mock_transaction>
## Mock Transaction

For data layer tests that inject transaction interface:

```go
type mockTransaction struct{}

func (m *mockTransaction) InTx(ctx context.Context, fn func(ctx context.Context) error) error {
    return fn(ctx)
}

// Compile-time interface check
var _ common.Transaction = (*mockTransaction)(nil)
```

**Usage:**

```go
tx := &mockTransaction{}
repo := NewSymbolRepo(db, tx, logger)
```

The mock simply executes the function without actual transaction - sufficient for unit tests.
</mock_transaction>

<helper_patterns>
## Helper Function Patterns

### Naming Convention

- `setupX` - Create and initialize dependencies
- `cleanupX` - Clean up test data or resources
- `validX` - Return valid object for testing
- `validDomainX` - Return valid business domain object (data layer)
- `validEntityX` - Return valid database entity (data layer)

### Location

Helpers go at top of test file, before test functions:

```go
package repo

import (...)

// 1. Setup helpers
func setupTestDB(t *testing.T) *gorm.DB { ... }

// 2. Cleanup helpers
func cleanupDB(db *gorm.DB) { ... }

// 3. Valid object helpers
func validDomainSymbol() *biz.Symbol { ... }
func validEntitySymbol() *model.Symbol { ... }

// 4. Mock structs (if needed)
type mockTransaction struct{}

// 5. Test functions
func TestCreate(t *testing.T) { ... }
```

### Creating Invalid Objects

Use anonymous functions in test cases for invalid variants:

```go
{
    name: "missing required field",
    symbol: func() *Symbol {
        s := validSymbol()
        s.Label = "" // Make invalid
        return s
    }(),
    wantErr: true,
}
```

This pattern:
- Starts with valid object
- Modifies specific field
- Keeps rest of object valid
- Clear what's being tested
</helper_patterns>

<common_imports>
## Common Imports for Test Helpers

### Data Layer
```go
import (
    "context"
    "os"
    "testing"
    "{service}/internal/biz"
    "{service}/internal/data/common"
    "{service}/internal/data/model"

    "github.com/go-kratos/kratos/v2/log"
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
)
```

### Biz Layer
```go
import (
    "context"
    "os"
    "testing"

    "github.com/go-kratos/kratos/v2/log"
    "github.com/go-playground/validator/v10"
)
```

### Service Layer
```go
import (
    "context"
    "testing"
    v1 "{service}/api/symbols/v1"
    "{service}/internal/biz"
)
```
</common_imports>

<best_practices>
## Helper Function Best Practices

1. **One helper per setup type** - Don't combine database + mock + validator in one helper
2. **Return initialized, ready-to-use objects** - Don't require additional setup
3. **Use t.Fatalf for setup failures** - Fail fast if setup doesn't work
4. **Make helpers reusable** - Don't hardcode test-specific values
5. **Document non-obvious helpers** - Explain why helper exists if not immediately clear
6. **Keep helpers simple** - Complex helpers are hard to debug
7. **Use defer for cleanup** - `defer cleanupDB(db)` ensures cleanup happens
8. **Create valid objects by default** - Use anonymous functions in tests for invalid variants
9. **Match naming conventions** - Consistent names help navigate test files
10. **Include compile-time checks for mocks** - `var _ Interface = (*Mock)(nil)`
</best_practices>