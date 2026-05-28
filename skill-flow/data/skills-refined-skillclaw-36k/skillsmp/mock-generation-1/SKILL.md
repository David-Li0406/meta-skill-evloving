---
name: mock-generation
description: >
  Generate mocks for Go interfaces using mockgen. Automate mock creation for
  unit tests across domain, application, and infra layers. Triggers: adding new
  interfaces, refactoring interfaces, updating mocks, go:generate directives,
  gomock, mockgen commands, or mock usage in tests.
license: MIT
compatibility: opencode
---

# Mock Generation Skill

Automatically generate mocks for Go interfaces using `mockgen` from the `go.uber.org/mock` package.

## When This Skill MUST Be Used

**ALWAYS invoke this skill when the user's request involves ANY of these:**

- Adding a new interface that needs to be mocked for testing
- Refactoring an existing interface (signature changes)
- Running `go generate` for mock-related directives
- Writing tests that require mocks
- Troubleshooting mock generation issues
- Setting up `go:generate` directives for mockgen
- Questions about gomock matchers or expectations

**If you're about to write a new interface or modify an existing one, consider if mocks need updating.**

## Critical Safety Rules

**NEVER:**
- Manually edit generated mock files (`*_mock.go`) - always regenerate
- Use relative import paths in `go:generate` directives
- Forget to run `go generate` after adding new interfaces
- Mix source-mode and reflect-mode inconsistently in the same package

**ALWAYS:**
- Use full module import paths in `go:generate` directives
- Place mocks in a `mocks/` subdirectory of the package containing the interface
- Run `go generate ./...` from the module root to regenerate all mocks
- Verify mockgen is installed: `go install go.uber.org/mock/mockgen@latest`

## Quick Reference

| Task | Command |
|------|---------|
| Install mockgen | `go install go.uber.org/mock/mockgen@latest` |
| Generate all mocks | `make generate` or `go generate ./...` |
| Generate for package | `go generate ./internal/domain/order/...` |
| Check mockgen version | `mockgen --version` |

## Patterns

### Pattern 1: Source File Generation (Multiple Interfaces)

Generate mocks from a source file containing multiple interfaces:

```go
//go:generate mockgen -source=ports.go -destination=mocks/ports_mocks.go -package=mocks

// File: internal/domain/chat/ports.go
type StateStore interface {
    Set(ctx context.Context, key string, value any, ttl time.Duration) error
    Get(ctx context.Context, key string) (any, error)
    Delete(ctx context.Context, key string) error
}
```

**Use this for:** Multiple interfaces in one file, often in `ports.go`

### Pattern 2: Named Interface Generation (Single Interface)

Generate mocks for specific interfaces by name:

```go
//go:generate mockgen -destination=mocks/repository_mock.go -package=mocks mymodule/internal/domain/order Repository

// File: internal/domain/order/repository.go
type Repository interface {
    Save(ctx context.Context, order *Order) error
    Update(ctx context.Context, order *Order) error
    GetByID(ctx context.Context, id ID) (*Order, error)
}
```

**Use this for:** Single interface per file, cleaner one-mock-per-file organization

### Pattern 3: Application Layer Mocks

Generate mocks for application layer dependencies:

```go
//go:generate mockgen -destination=mocks/user_repository_mock.go -package=mocks mymodule/internal/application/user UserRepository

// File: internal/application/user/application.go
type UserRepository interface {
    GetByID(ctx context.Context, id user.ID) (*user.User, error)
    List(ctx context.Context) ([]*user.User, error)
}
```

## Full Example: Adding a New Interface

### 1. Define Interface in Domain

```go
// File: internal/domain/order/notifier.go
package order

import "context"

//go:generate mockgen -destination=mocks/notifier_mock.go -package=mocks mymodule/internal/domain/order Notifier

type Notifier interface {
    SendOrderCreated(ctx context.Context, orderID ID, userID user.ID) error
    SendOrderCompleted(ctx context.Context, orderID ID) error
}
```

### 2. Generate Mock

```bash
go generate ./internal/domain/order/...
```

### 3. Use Mock in Test

```go
// File: internal/domain/order/order_test.go
package order_test

import (
    "go.uber.org/mock/gomock"
    "mymodule/internal/domain/order/mocks"
)

func TestOrder_Creation(t *testing.T) {
    ctrl := gomock.NewController(t)

    mockNotifier := mocks.NewMockNotifier(ctrl)
    mockNotifier.EXPECT().
        SendOrderCreated(gomock.Any(), gomock.Any(), gomock.Any()).
        Return(nil).
        Times(1)

    // Test code here
    mockNotifier.SendOrderCreated(ctx, orderID, userID)
}
```

## Mock Usage Guidelines

### Fixture Pattern (Recommended)

```go
type fixture struct {
    mockRepo *mocks.MockRepository
    sut      *Service
}

func newFixture(t *testing.T) *fixture {
    t.Helper()
    ctrl := gomock.NewController(t)
    mockRepo := mocks.NewMockRepository(ctrl)
    
    return &fixture{
        mockRepo: mockRepo,
        sut:      NewService(mockRepo),
    }
}

func TestService_Operation(t *testing.T) {
    f := newFixture(t)
    f.mockRepo.EXPECT().GetByID(gomock.Any(), gomock.Eq(123)).
        Return(&Order{}, nil).
        Times(1)
    
    // Test
}
```

### Mock Expectations

```go
// Flexible matching
mockRepo.EXPECT().GetByID(gomock.Any(), gomock.Any()).Return(&Order{}, nil)

// Strict matching
mockRepo.EXPECT().GetByID(gomock.Any(), gomock.Eq(123)).Return(&Order{}, nil)

// Error case
mockRepo.EXPECT().GetByID(gomock.Any(), gomock.Any()).Return(nil, ErrNotFound)

// Multiple calls
mockRepo.EXPECT().Save(gomock.Any(), gomock.Any()).Return(nil).Times(2)

// Call ordering
gomock.InOrder(
    mockRepo.EXPECT().GetByID(gomock.Any(), gomock.Any()).Return(&Order{}, nil),
    mockRepo.EXPECT().Save(gomock.Any(), gomock.Any()).Return(nil),
)
```

## Directory Structure

Mocks follow this standard structure:

```
internal/
├── domain/
│   ├── order/
│   │   ├── repository.go          # Domain interface + go:generate
│   │   ├── mocks/
│   │   │   ├── repository_mock.go # Generated mock
│   │   │   └── publisher_mock.go  # Generated mock
│   │   └── order_test.go          # Uses mocks
│   └── chat/
│       ├── ports.go               # Multiple interfaces + go:generate
│       ├── mocks/
│       │   └── ports_mocks.go     # All mocks in one file
│       └── ports_test.go
└── application/
    └── user/
        ├── application.go         # References domain interfaces
        ├── mocks/
        │   └── user_repository_mock.go
        └── application_test.go
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Mocks not generated | mockgen not installed | `go install go.uber.org/mock/mockgen@latest` |
| Import errors in generated files | Relative import path in directive | Use full module path: `mymodule/internal/domain/order` |
| Interface not found | Wrong interface name or case | Check exact name: `Repository` not `repository` |
| Mock file in wrong location | Wrong destination path | Ensure destination is relative to directive file location |
| "package mocks not found" | mocks/ directory doesn't exist | Run `go generate` to create it, or `mkdir mocks` first |
| Stale mock (missing methods) | Interface changed without regenerating | Run `go generate ./...` |

## Example Requests

| User Request | Action |
|--------------|--------|
| "Add a new Repository interface" | Define interface with `go:generate` directive, run `go generate` |
| "The mock is missing the new method" | Run `go generate ./...` to regenerate |
| "How do I mock this interface?" | Add `go:generate` directive, generate, show test usage |
| "Set up mocks for testing" | Install mockgen, add directives, generate mocks |
| "My go generate isn't creating mocks" | Check mockgen installed, verify directive syntax |

## Key Points

- **Always use full import paths** in `go:generate` directives
- **One interface per mock file** recommended for clarity
- **Mocks go in `mocks/` subdirectory** of the package containing the interface
- **Run `make generate`** or `go generate ./...` from module root to regenerate all
- **Never manually edit generated mock files** - always regenerate
- **Use `gomock.Any()`** when argument values don't matter in test
- **Use `gomock.Eq(value)`** when testing specific values
