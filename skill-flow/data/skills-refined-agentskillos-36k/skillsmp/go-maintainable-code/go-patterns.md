# Go-Specific Patterns for Maintainable Code

## Naming Conventions

### Variables
```go
// ✅ Good - descriptive, lowercase for unexported
checklistId := uint(123)
userId := "user123"
checklistItems := []domain.ChecklistItem{}

// ❌ Bad
id := 123  // Too vague in larger scope
ChecklistId := 123  // Exported unnecessarily
cId := 123  // Unclear abbreviation
```

### Functions
```go
// ✅ Good - verb-based, descriptive
func DeleteChecklistById(ctx context.Context, id uint) domain.Error
func FindAllChecklists(ctx context.Context) ([]domain.Checklist, domain.Error)
func HasAccessToChecklist(ctx context.Context, id uint) domain.Error

// ❌ Bad
func Checklist(id uint)  // Unclear what it does
func Get(ctx context.Context, id uint)  // Too generic
```

### Interfaces
```go
// ✅ Good - "I" prefix for clarity
type IChecklistService interface {}
type IChecklistRepository interface {}

// Note: Project uses "I" prefix convention
// Standard Go uses no prefix, but this project has chosen "I"
```

### Constants
```go
// ✅ Good - grouped by purpose
const (
    DefaultPageSize = 20
    MaxPageSize     = 100
)

const (
    StatusPending   = "pending"
    StatusCompleted = "completed"
)
```

## Error Handling

### Custom Error Type
```go
// Project uses domain.Error interface
type Error interface {
    error  // Embeds standard error
    ResponseCode() int
}

// Creating errors
domain.NewError("message", 400)
domain.Wrap(err, "context", 500)

// Checking errors
if err != nil {
    return domain.Wrap(err, "failed to save checklist", 500)
}
```

### Error Patterns
```go
// ✅ Pattern 1: Early returns
func Process(ctx context.Context, id uint) domain.Error {
    if err := validate(id); err != nil {
        return err
    }
    if err := process(id); err != nil {
        return err
    }
    return nil
}

// ✅ Pattern 2: If-else chains for different errors
func Delete(ctx context.Context, id uint) domain.Error {
    if err := s.guardrail.HasAccess(ctx, id); err != nil {
        return error.NewChecklistNotFoundError(id)  // 404
    }

    items, err := s.itemService.FindAll(ctx, id, nil, domain.AscSort)
    if err != nil {
        return err  // Propagate as-is
    }

    if len(items) > 0 {
        return domain.NewError("Checklist is not empty", 400)
    }

    return s.repo.Delete(ctx, id)
}
```

## Context Handling

### Always Pass Context First
```go
// ✅ Good - context is always first parameter
func MyFunction(ctx context.Context, id uint, name string) error

// ❌ Bad
func MyFunction(id uint, ctx context.Context) error
```

### Extracting Values from Context
```go
// User ID
userId, err := domain.GetUserIdFromContext(ctx)
if err != nil {
    return err
}

// Client ID (for SSE)
clientId := serverutils.GetClientIdFromContext(ctx)

// Creating domain context from HTTP context
domainCtx := serverutils.CreateContext(ctx)
```

### Don't Store Context in Structs
```go
// ❌ Bad
type service struct {
    ctx  context.Context  // Never store context!
    repo repository.IRepo
}

// ✅ Good - pass context to each method
type service struct {
    repo repository.IRepo
}

func (s *service) DoWork(ctx context.Context) error {
    return s.repo.Query(ctx, ...)
}
```

## Struct Patterns

### Private Implementation, Public Interface
```go
// Public interface in service package
type IChecklistService interface {
    DeleteChecklistById(ctx context.Context, id uint) domain.Error
}

// Private struct
type checklistService struct {
    repository                repository.IChecklistRepository
    checklistOwnershipChecker guardrail.IChecklistOwnershipChecker
    checklistItemService      IChecklistItemsService
}

// Public constructor (for Wire)
func NewChecklistService(
    repo repository.IChecklistRepository,
    checker guardrail.IChecklistOwnershipChecker,
    itemService IChecklistItemsService,
) IChecklistService {
    return &checklistService{
        repository:                repo,
        checklistOwnershipChecker: checker,
        checklistItemService:      itemService,
    }
}
```

### Embedding for Composition
```go
// Embed interfaces when extending
type ExtendedService interface {
    IChecklistService  // Embeds all methods
    NewMethod(ctx context.Context) error
}
```

## Pointer vs Value

### When to Use Pointers
```go
// ✅ Pointers for:
// - Receivers (always use pointer receivers for consistency)
func (s *service) Method() {}

// - Large structs
type BigStruct struct {
    Data [1000000]byte
}
func Process(b *BigStruct) {}

// - Nullable returns (distinguish between zero value and not found)
func FindById(id uint) (*domain.Checklist, domain.Error) {
    // Can return nil to indicate "not found"
}

// ✅ Values for:
// - Small structs
type Point struct {
    X, Y int
}
func Distance(p1, p2 Point) float64 {}

// - Immutable data
type Config struct {
    Port int
    Host string
}
```

## Slices and Maps

### Nil vs Empty Slices
```go
// Both are valid, but nil is more idiomatic for "no data"
var items []domain.ChecklistItem  // nil slice (preferred)
items := []domain.ChecklistItem{} // empty slice

// Check length, not nil (works for both)
if len(items) == 0 {
    // Empty or nil
}

// Return nil for not found
func FindAll() ([]Item, error) {
    // If no items found
    return nil, nil  // ✅ Idiomatic
    // return []Item{}, nil  // ❌ Less idiomatic
}
```

### Initialize Maps
```go
// ✅ Initialize before use
m := make(map[string]int)
m["key"] = 1

// ❌ Will panic
var m map[string]int
m["key"] = 1  // panic: assignment to entry in nil map
```

## Goroutines and Concurrency

### SSE Non-Blocking Publish Pattern
```go
// From notification service
select {
case clientChan <- event:
    // Event sent successfully
default:
    // Channel full, drop event (don't block)
    log.Printf("dropping event for client %s", clientId)
}
```

### Defer for Cleanup
```go
// Always defer resource cleanup
func Process(ctx context.Context) error {
    tx, err := beginTransaction()
    if err != nil {
        return err
    }
    defer tx.Rollback()  // Always called, even on panic

    // ... work ...

    return tx.Commit()
}
```

## Database Patterns

### Named Parameters (pgx)
```go
// ✅ Good - named args prevent mistakes
args := pgx.NamedArgs{
    "checklist_id": checklistId,
    "user_id":      userId,
    "item_name":    itemName,
}
result, err := tx.Exec(ctx, `
    DELETE FROM checklist_item
    WHERE checklist_id = @checklist_id
      AND user_id = @user_id
`, args)

// ❌ Bad - positional args error-prone
result, err := tx.Exec(ctx,
    "DELETE FROM checklist_item WHERE checklist_id = $1 AND user_id = $2",
    userId, checklistId,  // Easy to swap!
)
```

### Check Rows Affected
```go
result, err := tx.Exec(ctx, deleteQuery, args)
if err != nil {
    return domain.Wrap(err, "failed to delete", 500)
}

if result.RowsAffected() == 0 {
    return domain.NewError("item not found", 404)
}
```

## Comments and Documentation

### When to Comment
```go
// ✅ Good - explain WHY, not WHAT
// Use recursive CTE to preserve ordering from doubly-linked list
query := "SELECT * FROM CHECKLIST_ITEMS_ORDERED_VIEW"

// Guard rail returns 404 instead of 403 for security (don't reveal existence)
if err := s.guardrail.HasAccess(ctx, id); err != nil {
    return error.NewChecklistNotFoundError(id)
}

// ❌ Bad - stating the obvious
// Delete the checklist
s.repo.Delete(ctx, id)

// ❌ Bad - commenting what code does (code should be self-documenting)
// Loop through items and set completed to true
for _, item := range items {
    item.Completed = true
}
```

### TODO Comments
```go
// ✅ Good - with context or issue number
// TODO(#123): Add pagination support
// TODO: Refactor after migrating to Go 1.22 generics

// ❌ Bad - vague
// TODO: fix this
```

## Testing Patterns

### Table-Driven Tests
```go
func TestChecklistValidation(t *testing.T) {
    tests := []struct {
        name      string
        checklist domain.Checklist
        wantErr   bool
    }{
        {
            name:      "valid checklist",
            checklist: domain.Checklist{Name: "My List"},
            wantErr:   false,
        },
        {
            name:      "empty name",
            checklist: domain.Checklist{Name: ""},
            wantErr:   true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := validate(tt.checklist)
            if (err != nil) != tt.wantErr {
                t.Errorf("validate() error = %v, wantErr %v", err, tt.wantErr)
            }
        })
    }
}
```

### Mock Assertions
```go
// Setup expectations
mockRepo.On("Delete", mock.Anything, uint(123)).Return(nil)

// Execute
svc.Delete(ctx, 123)

// Verify all expectations met
mockRepo.AssertExpectations(t)

// Verify method NOT called
mockRepo.AssertNotCalled(t, "Delete")
```

## Avoid Common Pitfalls

### Range Loop Variables
```go
// ❌ Bad - loop variable capture
var funcs []func()
for _, item := range items {
    funcs = append(funcs, func() {
        fmt.Println(item.Name)  // All print same item!
    })
}

// ✅ Good - create new variable
for _, item := range items {
    item := item  // Shadow variable
    funcs = append(funcs, func() {
        fmt.Println(item.Name)
    })
}

// ✅ Better - pass as parameter
for _, item := range items {
    funcs = append(funcs, func(i domain.Item) func() {
        return func() { fmt.Println(i.Name) }
    }(item))
}
```

### Nil Interface Values
```go
// Tricky: interface can be non-nil with nil value
var err error
var customErr *CustomError = nil
err = customErr  // err != nil (interface contains type info)

// Safe pattern: return nil directly
func DoWork() error {
    var customErr *CustomError
    if something {
        customErr = &CustomError{}
    }

    if customErr != nil {
        return customErr
    }
    return nil  // ✅ Return nil, not customErr
}
```

## Project-Specific Idioms

### Error Response Mapping
```go
// Pattern from controllers
if err := controller.service.DoWork(ctx, id); err == nil {
    return Success200Response{}, nil
} else if err.ResponseCode() == http.StatusNotFound {
    return Error404Response{Message: err.Error()}, nil
} else if err.ResponseCode() == http.StatusBadRequest {
    return Error400Response{Message: err.Error()}, nil
} else {
    return Error500Response{Message: err.Error()}, nil
}
```

### Service Method Signatures
```go
// Pattern: context first, return (result, domain.Error)
func (s *service) FindById(ctx context.Context, id uint) (*domain.Entity, domain.Error)
func (s *service) Delete(ctx context.Context, id uint) domain.Error
func (s *service) Update(ctx context.Context, entity domain.Entity) (domain.Entity, domain.Error)
```

### Repository Query Pattern
```go
func (r *repo) FindAll(ctx context.Context) ([]domain.Entity, domain.Error) {
    rows, err := r.connection.Query(ctx, query, args)
    if err != nil {
        return nil, domain.Wrap(err, "failed to query entities", 500)
    }
    defer rows.Close()

    var entities []domain.Entity
    for rows.Next() {
        var dbo EntityDBO
        if err := rows.Scan(&dbo.Field1, &dbo.Field2); err != nil {
            return nil, domain.Wrap(err, "failed to scan row", 500)
        }
        entities = append(entities, toEntity(dbo))
    }

    return entities, nil
}
```
