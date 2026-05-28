# Testing Guide for ChecklistApplication

## Testing Philosophy

- **Unit tests** for service layer (business logic)
- **Mock dependencies** using testify/mock
- **Table-driven tests** for multiple scenarios
- **Test behavior, not implementation**
- **Aim for meaningful coverage, not 100%**

## Project Testing Standards

### File Naming
```
checklist_service.go       → checklist_service_test.go
checklist_repository.go    → (integration tests, not in CI)
```

### Test Function Naming
```go
// Pattern: Test{StructName}_{MethodName}_{Scenario}
func TestChecklistService_DeleteChecklistById_Success(t *testing.T)
func TestChecklistService_DeleteChecklistById_AccessDenied(t *testing.T)
func TestChecklistService_DeleteChecklistById_ChecklistNotEmpty(t *testing.T)
```

## Service Layer Testing Pattern

### Complete Example: Testing Delete Method

**Code under test** (`internal/core/service/checklist_service.go`):
```go
func (service *checklistService) DeleteChecklistById(ctx context.Context, id uint) domain.Error {
    if err := service.checklistOwnershipChecker.HasAccessToChecklist(ctx, id); err != nil {
        return error.NewChecklistNotFoundError(id)
    }

    if checklistItems, err := service.checklistItemService.FindAllChecklistItems(ctx, id, nil, domain.AscSort); err != nil {
        return err
    } else if len(checklistItems) > 0 {
        return domain.NewError("Checklist is not empty", 400)
    }
    return service.repository.DeleteChecklistById(ctx, id)
}
```

**Test file** (`internal/core/service/checklist_service_test.go`):

```go
package service

import (
    "context"
    "testing"

    "com.raunlo.checklist/internal/core/domain"
    "github.com/stretchr/testify/mock"
)

// Step 1: Create mocks for all dependencies
type mockChecklistRepository struct {
    mock.Mock
}

func (m *mockChecklistRepository) DeleteChecklistById(ctx context.Context, id uint) domain.Error {
    args := m.Called(ctx, id)
    if arg := args.Get(0); arg != nil {
        return arg.(domain.Error)
    }
    return nil
}

// ... implement other IChecklistRepository methods ...

type mockChecklistItemsService struct {
    mock.Mock
}

func (m *mockChecklistItemsService) FindAllChecklistItems(ctx context.Context, checklistId uint, completed *bool, sortOrder domain.SortOrder) ([]domain.ChecklistItem, domain.Error) {
    args := m.Called(ctx, checklistId, completed, sortOrder)
    var items []domain.ChecklistItem
    var err domain.Error
    if arg := args.Get(0); arg != nil {
        items = arg.([]domain.ChecklistItem)
    }
    if arg := args.Get(1); arg != nil {
        err = arg.(domain.Error)
    }
    return items, err
}

// ... implement other IChecklistItemsService methods ...

type mockChecklistOwnershipChecker struct {
    mock.Mock
}

func (m *mockChecklistOwnershipChecker) HasAccessToChecklist(ctx context.Context, checklistId uint) domain.Error {
    args := m.Called(ctx, checklistId)
    if arg := args.Get(0); arg != nil {
        return arg.(domain.Error)
    }
    return nil
}

// ... implement other guard rail methods ...

// Step 2: Test success scenario
func TestChecklistService_DeleteChecklistById_Success(t *testing.T) {
    // Arrange
    ctx := context.Background()
    checklistId := uint(123)

    repo := new(mockChecklistRepository)
    ownershipChecker := new(mockChecklistOwnershipChecker)
    itemService := new(mockChecklistItemsService)

    // Set expectations
    ownershipChecker.On("HasAccessToChecklist", ctx, checklistId).Return(nil)
    itemService.On("FindAllChecklistItems", ctx, checklistId, (*bool)(nil), domain.AscSort).Return([]domain.ChecklistItem{}, nil)
    repo.On("DeleteChecklistById", ctx, checklistId).Return(nil)

    svc := &checklistService{
        repository:                repo,
        checklistOwnershipChecker: ownershipChecker,
        checklistItemService:      itemService,
    }

    // Act
    err := svc.DeleteChecklistById(ctx, checklistId)

    // Assert
    if err != nil {
        t.Fatalf("expected no error, got: %v", err)
    }

    ownershipChecker.AssertExpectations(t)
    itemService.AssertExpectations(t)
    repo.AssertExpectations(t)
}

// Step 3: Test error scenarios
func TestChecklistService_DeleteChecklistById_AccessDenied(t *testing.T) {
    ctx := context.Background()
    checklistId := uint(123)
    expectedErr := domain.NewError("access denied", 403)

    repo := new(mockChecklistRepository)
    ownershipChecker := new(mockChecklistOwnershipChecker)
    itemService := new(mockChecklistItemsService)

    ownershipChecker.On("HasAccessToChecklist", ctx, checklistId).Return(expectedErr)

    svc := &checklistService{
        repository:                repo,
        checklistOwnershipChecker: ownershipChecker,
        checklistItemService:      itemService,
    }

    err := svc.DeleteChecklistById(ctx, checklistId)

    if err == nil {
        t.Fatal("expected error, got nil")
    }
    if err.Error() != "Checklist(id=123) not found" {
        t.Fatalf("expected not found error, got: %v", err.Error())
    }

    ownershipChecker.AssertExpectations(t)
    // Verify subsequent methods were NOT called
    itemService.AssertNotCalled(t, "FindAllChecklistItems")
    repo.AssertNotCalled(t, "DeleteChecklistById")
}

func TestChecklistService_DeleteChecklistById_ChecklistNotEmpty(t *testing.T) {
    ctx := context.Background()
    checklistId := uint(123)

    repo := new(mockChecklistRepository)
    ownershipChecker := new(mockChecklistOwnershipChecker)
    itemService := new(mockChecklistItemsService)

    items := []domain.ChecklistItem{
        {Id: 1, Name: "Item 1"},
        {Id: 2, Name: "Item 2"},
    }

    ownershipChecker.On("HasAccessToChecklist", ctx, checklistId).Return(nil)
    itemService.On("FindAllChecklistItems", ctx, checklistId, (*bool)(nil), domain.AscSort).Return(items, nil)

    svc := &checklistService{
        repository:                repo,
        checklistOwnershipChecker: ownershipChecker,
        checklistItemService:      itemService,
    }

    err := svc.DeleteChecklistById(ctx, checklistId)

    if err == nil {
        t.Fatal("expected error, got nil")
    }
    if err.Error() != "Checklist is not empty" {
        t.Fatalf("expected 'Checklist is not empty', got: %v", err.Error())
    }
    if err.ResponseCode() != 400 {
        t.Fatalf("expected status 400, got: %d", err.ResponseCode())
    }

    ownershipChecker.AssertExpectations(t)
    itemService.AssertExpectations(t)
    repo.AssertNotCalled(t, "DeleteChecklistById")
}
```

## Mock Implementation Patterns

### Mock Repository with Multiple Methods

```go
type mockChecklistRepository struct {
    mock.Mock
}

// Pattern 1: Method returning (Entity, Error)
func (m *mockChecklistRepository) FindById(ctx context.Context, id uint) (*domain.Checklist, domain.Error) {
    args := m.Called(ctx, id)
    var entity *domain.Checklist
    var err domain.Error
    if arg := args.Get(0); arg != nil {
        entity = arg.(*domain.Checklist)
    }
    if arg := args.Get(1); arg != nil {
        err = arg.(domain.Error)
    }
    return entity, err
}

// Pattern 2: Method returning ([]Entity, Error)
func (m *mockChecklistRepository) FindAll(ctx context.Context) ([]domain.Checklist, domain.Error) {
    args := m.Called(ctx)
    var entities []domain.Checklist
    var err domain.Error
    if arg := args.Get(0); arg != nil {
        entities = arg.([]domain.Checklist)
    }
    if arg := args.Get(1); arg != nil {
        err = arg.(domain.Error)
    }
    return entities, err
}

// Pattern 3: Method returning only Error
func (m *mockChecklistRepository) Delete(ctx context.Context, id uint) domain.Error {
    args := m.Called(ctx, id)
    if arg := args.Get(0); arg != nil {
        return arg.(domain.Error)
    }
    return nil
}

// Pattern 4: Method with complex return (custom struct + error)
func (m *mockChecklistRepository) Process(ctx context.Context, id uint) (domain.ProcessResult, domain.Error) {
    args := m.Called(ctx, id)
    var result domain.ProcessResult
    var err domain.Error
    if arg := args.Get(0); arg != nil {
        result = arg.(domain.ProcessResult)
    }
    if arg := args.Get(1); arg != nil {
        err = arg.(domain.Error)
    }
    return result, err
}
```

### Setting Mock Expectations

```go
// Basic expectation
mockRepo.On("Delete", ctx, uint(123)).Return(nil)

// With specific arguments
mockRepo.On("Update", ctx, domain.Checklist{Id: 123, Name: "Test"}).Return(expectedResult, nil)

// With mock.Anything for flexible matching
mockRepo.On("Save", mock.Anything, mock.Anything).Return(savedEntity, nil)

// Returning errors
expectedErr := domain.NewError("not found", 404)
mockRepo.On("FindById", ctx, uint(999)).Return((*domain.Checklist)(nil), expectedErr)

// Multiple return values
mockRepo.On("Process", ctx, uint(123)).Return(
    domain.ProcessResult{Success: true},
    nil,
)
```

## Table-Driven Tests

For testing multiple scenarios with similar setup:

```go
func TestChecklistService_Validate(t *testing.T) {
    tests := []struct {
        name      string
        checklist domain.Checklist
        wantErr   bool
        errMsg    string
        errCode   int
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
            errMsg:    "name cannot be empty",
            errCode:   400,
        },
        {
            name:      "name too long",
            checklist: domain.Checklist{Name: strings.Repeat("a", 256)},
            wantErr:   true,
            errMsg:    "name too long",
            errCode:   400,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            svc := &checklistService{/* ... */}
            err := svc.Validate(context.Background(), tt.checklist)

            if (err != nil) != tt.wantErr {
                t.Errorf("Validate() error = %v, wantErr %v", err, tt.wantErr)
                return
            }

            if tt.wantErr {
                if err.Error() != tt.errMsg {
                    t.Errorf("Validate() error message = %v, want %v", err.Error(), tt.errMsg)
                }
                if err.ResponseCode() != tt.errCode {
                    t.Errorf("Validate() error code = %v, want %v", err.ResponseCode(), tt.errCode)
                }
            }
        })
    }
}
```

## Testing SSE Notifications

```go
type mockNotificationService struct {
    mock.Mock
}

func (m *mockNotificationService) NotifyItemDeleted(ctx context.Context, checklistId uint, itemId uint) {
    m.Called(ctx, checklistId, itemId)
}

func TestChecklistItemService_Delete_SendsNotification(t *testing.T) {
    repo := new(mockChecklistItemsRepository)
    notifier := new(mockNotificationService)
    ownershipChecker := new(mockChecklistOwnershipChecker)

    checklistId := uint(10)
    itemId := uint(20)

    ownershipChecker.On("HasAccessToChecklist", mock.Anything, checklistId).Return(nil)
    repo.On("DeleteChecklistItemById", mock.Anything, checklistId, itemId).Return(nil)
    notifier.On("NotifyItemDeleted", mock.Anything, checklistId, itemId).Return()

    svc := &checklistItemsService{
        repository:                repo,
        notifier:                  notifier,
        checklistOwnershipChecker: ownershipChecker,
    }

    err := svc.DeleteChecklistItemById(context.Background(), checklistId, itemId)

    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }

    // Verify notification was sent
    notifier.AssertExpectations(t)
    notifier.AssertCalled(t, "NotifyItemDeleted", mock.Anything, checklistId, itemId)
}
```

## Edge Cases to Test

### Nil vs Empty Slices
```go
func TestService_FindAll_EmptyResult(t *testing.T) {
    // Test both nil and empty slice returns
    tests := []struct {
        name   string
        result []domain.Item
    }{
        {"nil slice", nil},
        {"empty slice", []domain.Item{}},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            mockRepo := new(mockRepository)
            mockRepo.On("FindAll", mock.Anything).Return(tt.result, nil)

            svc := &service{repo: mockRepo}
            items, err := svc.FindAll(context.Background())

            if err != nil {
                t.Fatalf("unexpected error: %v", err)
            }
            if len(items) != 0 {
                t.Errorf("expected empty result, got %d items", len(items))
            }
        })
    }
}
```

### Pointer Returns (Nullable)
```go
func TestService_FindById_NotFound(t *testing.T) {
    mockRepo := new(mockRepository)
    // Return nil entity with nil error (not found case)
    mockRepo.On("FindById", mock.Anything, uint(999)).Return((*domain.Entity)(nil), nil)

    svc := &service{repo: mockRepo}
    result, err := svc.FindById(context.Background(), 999)

    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if result != nil {
        t.Errorf("expected nil result, got %v", result)
    }
}
```

### Context Values
```go
func TestService_RequiresUserId(t *testing.T) {
    // Test with missing user ID in context
    ctx := context.Background()

    svc := &service{/* ... */}
    err := svc.DoWork(ctx)

    if err == nil {
        t.Fatal("expected error when user ID missing from context")
    }
    if err.Error() != "User ID not found in context" {
        t.Errorf("unexpected error: %v", err)
    }
}
```

## Common Testing Mistakes

### ❌ Not Resetting Mocks Between Tests
```go
// Bad - mock state carries over
var mockRepo = new(mockRepository)

func TestA(t *testing.T) {
    mockRepo.On("Save", mock.Anything).Return(nil)
    // ...
}

func TestB(t *testing.T) {
    // TestA's expectations still active!
}

// ✅ Good - create new mocks per test
func TestA(t *testing.T) {
    mockRepo := new(mockRepository)
    mockRepo.On("Save", mock.Anything).Return(nil)
}
```

### ❌ Not Checking All Error Cases
```go
// Bad - only tests success
func TestDelete_Success(t *testing.T) { /* ... */ }

// ✅ Good - tests all paths
func TestDelete_Success(t *testing.T) { /* ... */ }
func TestDelete_NotFound(t *testing.T) { /* ... */ }
func TestDelete_AccessDenied(t *testing.T) { /* ... */ }
func TestDelete_HasItems(t *testing.T) { /* ... */ }
```

### ❌ Testing Implementation, Not Behavior
```go
// Bad - tests internal method calls
func TestDelete(t *testing.T) {
    // Verifying internal implementation details
    mockRepo.AssertCalled(t, "BeginTransaction")
    mockRepo.AssertCalled(t, "QuerySomething")
    mockRepo.AssertCalled(t, "Commit")
}

// ✅ Good - tests observable behavior
func TestDelete(t *testing.T) {
    err := svc.Delete(ctx, id)
    if err != nil {
        t.Fatalf("Delete failed: %v", err)
    }
    // Verify the delete actually happened (behavior)
    mockRepo.AssertExpectations(t)
}
```

## Running Tests

```bash
# Run all tests
go test ./...

# Run specific package
go test ./internal/core/service

# Run specific test
go test ./internal/core/service -run TestChecklistService_DeleteChecklistById

# Run with verbose output
go test ./internal/core/service -v

# Run with coverage
go test ./internal/core/service -cover

# Generate coverage report
go test ./internal/core/service -coverprofile=coverage.out
go tool cover -html=coverage.out
```

## Test Organization

```
internal/core/service/
├── checklist_service.go
├── checklist_service_test.go          # Tests for checklist_service
├── checklist_items_service.go
├── checklist_items_service_test.go    # Tests for checklist_items_service
└── test_helpers.go                     # Shared test utilities (optional)
```

## When NOT to Test

- Generated code (`*_gen.go`, `wire_gen.go`)
- Simple getters/setters
- Trivial constructors with no logic
- Repository implementations (integration tests, not unit tests)
- Controllers (mostly glue code, hard to unit test effectively)

Focus testing on **business logic** in the service layer.
