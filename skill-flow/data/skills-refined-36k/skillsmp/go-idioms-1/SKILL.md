---
name: go-idioms
description: >
  Go idioms, patterns, and best practices. Load when working with .go files
  or Go projects. Triggers: go.mod, interface design, error handling,
  context usage, naming conventions, composition patterns, logging,
  or asking about Go patterns.
license: MIT
compatibility: opencode
---

# Go Idioms

Idiomatic Go patterns and best practices for writing clean, maintainable Go code.

## When This Skill MUST Be Used

**ALWAYS invoke this skill when the user's request involves ANY of these:**

- Creating or editing `.go` files
- Working with `go.mod` or Go project setup
- Questions about interface design or composition
- Error handling patterns and wrapping
- Context usage and propagation
- Naming conventions (packages, interfaces, getters)
- Logging with `log/slog`
- Decorator pattern implementation
- Performance optimization in Go

**If you're about to write Go code, STOP and use this skill first.**

## Critical Safety Rules

**NEVER:**
- Store `context.Context` in structs
- Ignore errors (`_, _ := ...`)
- Use panic for expected errors
- Create interfaces with 10+ methods
- Use `Get` prefix for getters (`user.GetName()`)

**ALWAYS:**
- Pass `context.Context` as first parameter
- Handle errors immediately after the call
- Define interfaces where they're used, not implemented
- Use small, focused interfaces (1-3 methods)
- Wrap errors with context using `%w`

## Quick Reference

| Task | Command |
|------|---------|
| Build | `go build ./...` |
| Test | `go test ./...` |
| Lint | `golangci-lint run` |
| Format | `gofmt -w .` |
| Tidy deps | `go mod tidy` |
| Vet | `go vet ./...` |

---

# Interface Design

## Small, Focused Interfaces

```go
// GOOD: Small interface (1-3 methods)
type UserGetter interface {
    GetUser(ctx context.Context, id UserID) (*User, error)
}

// GOOD: Compose interfaces
type ReadWriter interface {
    Reader
    Writer
}

// BAD: Interface pollution (too many methods)
type UserService interface {
    GetUser(...)
    CreateUser(...)
    UpdateUser(...)
    DeleteUser(...)
    ListUsers(...)
    // ... 10 more methods
}
```

## Accept Interfaces, Return Structs

```go
// GOOD: Accept interface at usage site
func NewHandler(users UserGetter) *Handler {
    return &Handler{users: users}
}

// GOOD: Return concrete type
func NewUserRepository(db *sql.DB) *UserRepository {
    return &UserRepository{db: db}
}
```

## Define Interfaces Where Used

```go
// In handler package (consumer)
type UserGetter interface {
    GetUser(ctx context.Context, id UserID) (*User, error)
}

// Handler depends on interface, not concrete type
type Handler struct {
    users UserGetter
}
```

---

# Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Packages | Short, lowercase, singular | `user`, `order`, `http` |
| Interfaces | Method + "er" suffix | `Reader`, `Handler`, `Validator` |
| Getters | No `Get` prefix | `user.Name()` not `user.GetName()` |
| Constructors | `New` prefix | `NewOrder()`, `NewFromConfig()` |
| Booleans | Question form | `IsValid`, `HasPermission`, `CanExecute` |

## Avoid Stuttering

```go
// BAD: Stuttering
user.UserID
order.OrderStatus

// GOOD: No stutter
user.ID
order.Status
```

---

# Error Handling

## Sentinel Errors

Define in `errors.go` per package:

```go
var (
    ErrInvalidOrderID = errors.New("invalid order ID")
    ErrOrderNotFound  = errors.New("order not found")
)
```

## Wrap with Context

Always wrap errors with `%w`:

```go
result, err := doSomething()
if err != nil {
    return fmt.Errorf("failed to do something: %w", err)
}
```

Add context at each layer:
- Repository: `"query order by id: %w"`
- Application: `"complete order %d: %w"`
- Handler: `"handle complete request: %w"`

## Check Errors Properly

```go
// Use errors.Is() for sentinel errors
if errors.Is(err, ErrOrderNotFound) {
    return nil, status.NotFound
}

// Use errors.As() for type assertions
var validationErr *ValidationError
if errors.As(err, &validationErr) {
    return nil, validationErr.Fields
}
```

## Layer Patterns

| Layer | Pattern |
|-------|---------|
| Domain | Return sentinel errors, no logging |
| Application | Wrap errors, log before returning |
| Infrastructure | Translate external errors to domain errors |

**Infrastructure Translation:**
```go
// MySQL repository
if errors.Is(err, sql.ErrNoRows) {
    return nil, domain.ErrOrderNotFound
}

// External API client
if resp.StatusCode == 404 {
    return nil, domain.ErrResourceNotFound
}
```

---

# Context

## Always First Parameter

```go
func (s *Service) Process(ctx context.Context, req Request) (Result, error)
```

## Never Store in Structs

```go
// BAD: Context in struct
type Service struct {
    ctx context.Context  // NEVER do this
}

// GOOD: Pass through methods
func (s *Service) Do(ctx context.Context) error {
    return s.repo.Save(ctx, s.data)
}
```

## Use for Cancellation, Timeouts, Request-Scoped Values

```go
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()

resp, err := client.Do(req.WithContext(ctx))
```

---

# Logging

## Use log/slog

Always use standard library `log/slog` for structured logging.

```go
logger.InfoContext(ctx, "Order completed", "order_id", orderID)
```

## Log Levels

| Level | When to Use |
|-------|-------------|
| `Debug` | Development-only, verbose details |
| `Info` | Normal operations, state changes |
| `Warn` | Recoverable issues, degraded state |
| `Error` | Failures requiring attention |

## Field Naming

- Use `snake_case`: `order_id`, `user_id`, `external_id`
- Suffix with `_id` for identifiers
- Suffix with `_ms` for milliseconds

## Anti-Patterns

- Don't log sensitive data (passwords, tokens)
- Don't log in domain layer (pure business logic)
- Don't use printf-style formatting
- Don't log expected errors at Error level

---

# Decorator Pattern

## Core Principle

**Constructors accept interfaces, return concrete types.**

```go
type Service interface {
    Do(ctx context.Context, input Data) (Result, error)
}

// Decorator wraps interface, returns concrete
func NewLoggedService(svc Service, logger Logger) *LoggedService {
    return &LoggedService{service: svc, logger: logger}
}
```

## Composition Chain

Build functionality by stacking decorators:

```go
// Core implementation
core := NewCoreService(repo)

// Add cross-cutting concerns
logged := NewLoggedService(core, logger)
metered := NewMeteredService(logged, metrics)
cached := NewCachedService(metered, cache)

// Use the fully decorated service
handler := NewHandler(cached)
```

**Order matters**: Outermost decorator executes first.

## Common Decorator Use Cases

| Decorator | Purpose |
|-----------|---------|
| Logging | Log method calls, arguments, results |
| Metrics | Record latency, count calls, track errors |
| Caching | Cache results, invalidate on writes |
| Circuit Breaker | Fail fast when downstream is unhealthy |
| Retry | Retry transient failures with backoff |
| Rate Limiting | Throttle requests |
| Authorization | Check permissions before execution |
| Validation | Validate inputs before processing |
| Tracing | Add spans for distributed tracing |

## Implementation Pattern

```go
type LoggedService struct {
    next   Service  // The wrapped service
    logger Logger
}

func NewLoggedService(next Service, logger Logger) *LoggedService {
    return &LoggedService{next: next, logger: logger}
}

func (s *LoggedService) Do(ctx context.Context, input Data) (Result, error) {
    s.logger.Info("service.Do called", "input", input)
    
    result, err := s.next.Do(ctx, input)
    
    if err != nil {
        s.logger.Error("service.Do failed", "error", err)
    }
    return result, err
}
```

---

# Zero Values

Design types so zero value is useful:

```go
var buf bytes.Buffer  // Ready to use, no initialization needed
buf.WriteString("hello")
```

Use zero to indicate "use default":

```go
type Config struct {
    Timeout time.Duration  // Zero means use default
}

func (c *Config) GetTimeout() time.Duration {
    if c.Timeout == 0 {
        return 30 * time.Second  // Default
    }
    return c.Timeout
}
```

---

# Performance Patterns

```go
// Preallocate slices when size is known
results := make([]Result, 0, len(items))

// Use strings.Builder for concatenation
var b strings.Builder
b.WriteString("hello")
b.WriteString(" world")
```

---

# Composition Over Inheritance

Use embedding to share behavior:

```go
type LoggedService struct {
    Service  // Embedded interface
    logger   Logger
}
```

Prefer composition for flexibility:

```go
type Handler struct {
    users  UserRepository
    orders OrderRepository
    logger Logger
}
```

---

# Concurrency

**"Don't communicate by sharing memory; share memory by communicating."**

- Use channels for coordination
- Use sync primitives only when channels don't fit

```go
// GOOD: Channel for coordination
results := make(chan Result)
go func() {
    results <- doWork()
}()

// Use sync.Mutex when channels don't fit
type Counter struct {
    mu    sync.Mutex
    value int
}
```

---

# Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Stuttering | `user.UserID` | `user.ID` |
| Interface pollution | 10+ methods | Split into small interfaces |
| Premature abstraction | Interface before 2+ implementations | Wait for need |
| Chain calls | `a.B().C().D()` | Law of Demeter - delegate |
| Context in structs | Stored context | Pass through methods |
| Ignoring errors | `_, _ := ...` | Handle every error |
| Get prefix | `user.GetName()` | `user.Name()` |

---

# Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "interface has no methods" | Empty interface{} | Use `any` in Go 1.18+ |
| "too many methods" | Fat interface | Split by use case |
| Import cycle | Wrong dependency direction | Introduce interface |
| Nil pointer | Zero value of pointer | Check nil or use value type |
| Data race | Shared mutable state | Use channels or sync primitives |

---

# Example Requests

| User Request | Action |
|--------------|--------|
| "Create a new Go interface" | Define small (1-3 methods) at consumer site |
| "Handle errors properly" | Wrap with `%w`, use `errors.Is/As` |
| "Add logging to service" | Create logging decorator with `log/slog` |
| "Fix stuttering names" | Remove type prefix from field names |
| "Pass context correctly" | First param, never store in struct |
| "Make this more idiomatic" | Apply naming conventions, small interfaces |
| "Add metrics to handler" | Use decorator pattern with metrics middleware |
