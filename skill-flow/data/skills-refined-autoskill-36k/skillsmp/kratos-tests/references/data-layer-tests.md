# Data Layer Testing Patterns

Testing patterns for `internal/data/repo/*` repository implementations.

<overview>
Data layer tests verify GORM repository operations, entity transformations, and error mapping. They use in-memory SQLite for fast, isolated tests without external database dependencies.
</overview>

<test_structure>
## Standard Data Layer Test File Structure

```go
package repo

import (
    "context"
    "testing"
    "{service}/internal/biz"
    "{service}/internal/data/common"
    "{service}/internal/data/model"
    "{service}/internal/pkg/pagination"

    "github.com/go-kratos/kratos/v2/log"
    "github.com/stretchr/testify/assert"
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
)

// Test helpers
func setupTestDB(t *testing.T) *gorm.DB { ... }
func cleanupDB(db *gorm.DB) { ... }
func validDomainX() *biz.X { ... }
func validEntityX() *model.X { ... }

// Mock transaction
type mockTransaction struct{}

// Test functions
func TestCreate(t *testing.T) { ... }
func TestUpdate(t *testing.T) { ... }
func TestFindByID(t *testing.T) { ... }
func TestList(t *testing.T) { ... }
func TestDelete(t *testing.T) { ... }
func TestEntityTransformations(t *testing.T) { ... }
func TestErrorMapping(t *testing.T) { ... }
```
</test_structure>

<setup_helpers>
## setupTestDB Pattern

Creates in-memory SQLite database for testing:

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

## cleanupDB Pattern

```go
func cleanupDB(db *gorm.DB) {
    db.Exec("DELETE FROM table1")
    db.Exec("DELETE FROM table2")
}
```
</setup_helpers>

<valid_objects>
## Valid Object Helpers

**validDomainX** - Returns valid domain model:

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
</valid_objects>

<mock_transaction>
## Mock Transaction Pattern

```go
type mockTransaction struct{}

func (m *mockTransaction) InTx(ctx context.Context, fn func(ctx context.Context) error) error {
    return fn(ctx)
}

// Compile-time interface check
var _ common.Transaction = (*mockTransaction)(nil)
```
</mock_transaction>

<test_patterns>
## Create Operation Test

```go
func TestCreate(t *testing.T) {
    tests := []struct {
        name        string
        input       *biz.X
        setup       func(*gorm.DB)
        wantErr     bool
        checkError  func(*testing.T, error)
        checkResult func(*testing.T, *biz.X)
    }{
        {
            name:   "success with nested data",
            input:  validDomainX(),
            setup:  func(db *gorm.DB) {},
            wantErr: false,
            checkResult: func(t *testing.T, result *biz.X) {
                assert.NotNil(t, result)
                assert.NotZero(t, result.Id)
                assert.NotNil(t, result.Data)
            },
        },
        {
            name: "success without nested data",
            input: func() *biz.X {
                x := validDomainX()
                x.Data = nil
                return x
            }(),
            setup:   func(db *gorm.DB) {},
            wantErr: false,
        },
        {
            name:  "duplicate entry error",
            input: validDomainX(),
            setup: func(db *gorm.DB) {
                entity := validEntityX()
                db.Session(&gorm.Session{FullSaveAssociations: true}).Create(entity)
            },
            wantErr: true,
            checkError: func(t *testing.T, err error) {
                assert.ErrorIs(t, err, biz.ErrDuplicateEntry)
            },
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            db := setupTestDB(t)
            defer cleanupDB(db)

            tt.setup(db)

            logger := log.NewStdLogger(os.Stdout)
            tx := &mockTransaction{}
            repo := NewXRepo(db, tx, logger)

            result, err := repo.Create(context.Background(), tt.input)

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
}
```

## Update Operation Test

Key difference: setup returns ID to update

```go
func TestUpdate(t *testing.T) {
    tests := []struct {
        name        string
        input       *biz.X
        setup       func(*gorm.DB) uint64  // Returns ID
        wantErr     bool
        checkResult func(*testing.T, *biz.X)
    }{
        {
            name:  "success",
            input: validDomainX(),
            setup: func(db *gorm.DB) uint64 {
                entity := validEntityX()
                db.Session(&gorm.Session{FullSaveAssociations: true}).Create(entity)
                return entity.ID
            },
            wantErr: false,
        },
        {
            name: "not found error",
            input: func() *biz.X {
                x := validDomainX()
                x.Id = 999
                return x
            }(),
            setup: func(db *gorm.DB) uint64 {
                return 999
            },
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            db := setupTestDB(t)
            defer cleanupDB(db)

            id := tt.setup(db)
            tt.input.Id = id

            // ... test execution
        })
    }
}
```

## List Operation Test

Includes pagination metadata verification:

```go
func TestListX(t *testing.T) {
    tests := []struct {
        name        string
        options     *biz.ListXOptions
        setup       func(*gorm.DB)
        wantErr     bool
        checkResult func(*testing.T, []*biz.X, *pagination.PaginationMeta)
    }{
        {
            name: "success - first page with next page",
            options: &biz.ListXOptions{
                ProjectID: 1,
                Pagination: pagination.PaginationParams{
                    Offset: 0,
                    Limit:  5,
                },
            },
            setup: func(db *gorm.DB) {
                for i := 0; i < 10; i++ {
                    entity := validEntityX()
                    entity.UID = fmt.Sprintf("uid-%d", i)
                    db.Session(&gorm.Session{FullSaveAssociations: true}).Create(entity)
                }
            },
            wantErr: false,
            checkResult: func(t *testing.T, items []*biz.X, meta *pagination.PaginationMeta) {
                assert.Len(t, items, 5)
                assert.Equal(t, uint64(10), meta.TotalCount)
                assert.True(t, meta.HasNextPage)
                assert.False(t, meta.HasPreviousPage)
            },
        },
    }
}
```
</test_patterns>

<transformation_tests>
## Entity Transformation Tests

Test domain ↔ entity conversions:

```go
func TestToDomainX(t *testing.T) {
    tests := []struct {
        name   string
        input  *model.X
        assert func(*testing.T, *biz.X)
    }{
        {
            name:  "nil input returns nil",
            input: nil,
            assert: func(t *testing.T, result *biz.X) {
                assert.Nil(t, result)
            },
        },
        {
            name: "complete entity converts correctly",
            input: validEntityX(),
            assert: func(t *testing.T, result *biz.X) {
                assert.NotNil(t, result)
                assert.Equal(t, uint64(1), result.Id)
                // ... field assertions
            },
        },
    }
}

func TestToEntityX(t *testing.T) {
    // Mirror pattern for domain → entity
}
```
</transformation_tests>

<error_mapping_tests>
## Error Mapping Tests

```go
func TestMapGormError(t *testing.T) {
    logger := log.NewStdLogger(os.Stdout)
    tx := &mockTransaction{}
    db := setupTestDB(t)
    defer cleanupDB(db)

    repo := NewXRepo(db, tx, logger).(*xRepo)

    tests := []struct {
        name       string
        inputError error
        wantError  error
    }{
        {
            name:       "nil input returns nil",
            inputError: nil,
            wantError:  nil,
        },
        {
            name:       "gorm.ErrRecordNotFound returns biz.ErrNotFound",
            inputError: gorm.ErrRecordNotFound,
            wantError:  biz.ErrNotFound,
        },
        {
            name:       "duplicate key error",
            inputError: errors.New("Error 1062: Duplicate entry"),
            wantError:  biz.ErrDuplicateEntry,
        },
        {
            name:       "other errors return biz.ErrDatabase",
            inputError: errors.New("connection timeout"),
            wantError:  biz.ErrDatabase,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := repo.mapGormError(tt.inputError)
            if tt.wantError == nil {
                assert.Nil(t, result)
            } else {
                assert.ErrorIs(t, result, tt.wantError)
            }
        })
    }
}
```
</error_mapping_tests>

<best_practices>
## Data Layer Testing Best Practices

1. **Use SQLite in-memory** - Fast, isolated, no cleanup needed
2. **Test with FullSaveAssociations** - When creating entities with relationships
3. **Test both with and without nested data** - Verify optional relationships work
4. **Verify pagination metadata** - Check TotalCount, HasNextPage, HasPreviousPage
5. **Test transformation functions separately** - toDomain and toEntity as unit tests
6. **Test error mapping thoroughly** - Cover all GORM error types
7. **Always cleanup** - Use defer cleanupDB(db) even with in-memory DB
8. **Verify IDs assigned** - Check generated IDs after Create operations
</best_practices>