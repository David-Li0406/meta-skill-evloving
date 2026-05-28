---
name: golang
description: Go patterns for backend development, testing, and clean architecture. Use when writing Go code.
---

# Go

## Project Structure

```
├── cmd/app/            # Entrypoint
├── internal/           # Private application code
│   ├── entity/         # Domain models
│   ├── usecase/        # Business logic
│   ├── repo/           # Repository interfaces + implementations
│   └── controller/     # HTTP/gRPC handlers
└── pkg/                # Reusable libraries
```

## Interface Pattern

```go
// Define interface where it's used (consumer side)
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, user *User) error
}

// Implement in outer layer
type postgresUserRepo struct {
    db *sql.DB
}

func (r *postgresUserRepo) FindByID(ctx context.Context, id string) (*User, error) {
    // implementation
}

// Constructor with interface return
func NewUserRepository(db *sql.DB) UserRepository {
    return &postgresUserRepo{db: db}
}
```

## Error Handling

```go
// Wrap errors with context
if err != nil {
    return fmt.Errorf("UserRepo.FindByID: %w", err)
}

// Custom error types
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s with ID %s not found", e.Resource, e.ID)
}

// Check error type
if errors.Is(err, sql.ErrNoRows) {
    return &NotFoundError{Resource: "user", ID: id}
}
```

## Testing

```go
// Table-driven tests
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name  string
        email string
        want  bool
    }{
        {"valid", "test@example.com", true},
        {"invalid", "invalid", false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := ValidateEmail(tt.email)
            if got != tt.want {
                t.Errorf("got %v, want %v", got, tt.want)
            }
        })
    }
}

// Mock with interface
type mockUserRepo struct {
    users map[string]*User
}

func (m *mockUserRepo) FindByID(ctx context.Context, id string) (*User, error) {
    if u, ok := m.users[id]; ok {
        return u, nil
    }
    return nil, &NotFoundError{Resource: "user", ID: id}
}
```

## Context & Logging

```go
// Always pass context first
func (uc *UseCase) CreateUser(ctx context.Context, req CreateUserRequest) (*User, error)

// Context-aware logging
type ctxKey struct{}

func WithLogger(ctx context.Context, l *slog.Logger) context.Context {
    return context.WithValue(ctx, ctxKey{}, l)
}

func FromContext(ctx context.Context) *slog.Logger {
    if l, ok := ctx.Value(ctxKey{}).(*slog.Logger); ok {
        return l
    }
    return slog.Default()
}

// Usage
logger := FromContext(ctx).With("user_id", userID)
logger.Info("creating user")
```

## HTTP Handler Pattern

```go
type Handler struct {
    usecase UserUseCase
    logger  *slog.Logger
}

func (h *Handler) CreateUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid request", http.StatusBadRequest)
        return
    }

    user, err := h.usecase.CreateUser(r.Context(), req)
    if err != nil {
        var notFound *NotFoundError
        if errors.As(err, &notFound) {
            http.Error(w, err.Error(), http.StatusNotFound)
            return
        }
        h.logger.Error("create user failed", "error", err)
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}
```

## Concurrency

```go
// errgroup for concurrent operations
g, ctx := errgroup.WithContext(ctx)

g.Go(func() error {
    return fetchUserData(ctx)
})

g.Go(func() error {
    return fetchUserOrders(ctx)
})

if err := g.Wait(); err != nil {
    return err
}

// Semaphore for rate limiting
sem := make(chan struct{}, 10)
for _, item := range items {
    sem <- struct{}{}
    go func(item Item) {
        defer func() { <-sem }()
        process(item)
    }(item)
}
```

## Best Practices

- Accept interfaces, return structs
- Keep interfaces small (1-3 methods)
- Use `context.Context` as first parameter
- Wrap errors with `fmt.Errorf("...: %w", err)`
- Use `slog` for structured logging (Go 1.21+)
- Table-driven tests with `t.Run`
- Generate mocks with `mockgen` or `moq`
- Use `golangci-lint` for linting
- Prefer `errors.Is/As` over type assertions
