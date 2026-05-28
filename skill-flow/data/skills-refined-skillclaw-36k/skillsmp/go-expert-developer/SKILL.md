---
name: go-expert-developer
description: Go best practices for writing clean, idiomatic, and maintainable Go code. This skill should be used when writing or reviewing Go code.
---

# Go Expert Developer

## Foreword

- You MUST follow these standards when writing Go code.
- Existing code SHOULD be refactored to comply when modified.
- Do NOT be mislead by existing code; ALWAYS remind yourself of these standards.

## Principles

- **KISS**: Code should be as simple as possible; avoid premature abstractions and optimizations
- **DRY**: Extract shared patterns
- **YAGNI**: Don't build until needed
- **Clear > Clever**: Readability is EXTREMELY important. Do not sacrifice clarity for cleverness.
- **Idiomatic Go**: stdlib first; don't import other languages' idioms
- Follow Uber's Go Style Guide, Google's Go Style Guide, and Effective Go

## Naming

### Constructors

```go
// ✓ package.New() when package name provides context
package server
func New() *Server { ... }  // server.New()

// ✗ Redundant type name
func NewServer() *Server { ... }
```

### Methods

```go
// ✓ No Get prefix
func (u *User) Name() string { ... }
func (c *Client) FetchUser(id string) (*User, error) { ... }

// ✗ Get prefix
func (u *User) GetName() string { ... }
```

### Variables

Rule: distance from declaration → name length.

```go
// ✓ Short names for small scopes
for i := range len(items) { ... }
func parse(r io.Reader) error { ... }

// ✓ Descriptive for wider scopes
func (s *Server) sendNotifications(userID string) error {
    user, err := s.db.GetUser(userID)
    // ...
}
```

### Receivers

```go
// ✓ 1-2 letter abbreviation
func (c *Client) Connect() error { ... }
func (ns *Namespace) Name() string { ... }
```

## Errors

### Wrapping Format

```go
// ✓ Imperative, lowercase, no "failed/error"
fmt.Errorf("connect to database: %w", err)
fmt.Errorf("parse config: %w", err)

// ✗ Bad patterns
fmt.Errorf("failed to connect: %w", err)
fmt.Errorf("Error parsing config: %w", err)
```

### Naming

```go
// ✓ Err prefix
var ErrNotFound = errors.New("not found")
var errInternal = errors.New("internal error")
```

## Structure

### Initialization

```go
// ✓ Empty slice
var users []User

// ✓ Named fields
user := User{Name: "John", Email: "john@example.com"}
```

### Struct Field Grouping

```go
// ✓ Grouped logically, embedded types first
type Server struct {
    httpSrv *http.Server

    host string
    port int

    log     *slog.Logger
    metrics *Metrics

    mu    sync.Mutex
    conns map[string]*Conn
}
```

### Reduce Nesting & Early Returns

```go
// ✓ Flat with early returns
func (s *Server) Handle(w http.ResponseWriter, r *http.Request) {
    id := r.URL.Query().Get("id")
    if id == "" {
        http.Error(w, "missing id", http.StatusBadRequest)
        return
    }

    user, err := s.db.GetUser(r.Context(), id)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    // happy path continues...
}
```

### Handle Once

```go
// ✓ Return OR log, never both
func loadConfig() (Config, error) {
    data, err := os.ReadFile("config.json")
    if err != nil {
        return Config{}, fmt.Errorf("load config: %w", err)
    }
    // ...
}
```

### Nil Handing

1. Functions must never return (nil, nil) or when returning a single non-error value, never return nil.
   It is the responsibility of functions to ensure `(nil, nil)` or only `nil` is ever returned.
2. When a function parameter is a pointer, it is the caller's responsibility to ensure it is non-nil unless otherwise documented.

```go
// ✓ User is not nil-checked
func (s *Service) NotifyUser(user *User, msg string) error {
    if user.Email != "" {
        return s.mailer.Send(user.Email, msg)
    }
    return nil
}
```

### Pass by Value

Default to value semantics. Use pointers only for:

- Types with pointer semantics (`sync.Mutex`, `sql.DB`)
- Types conventionally returned as pointers (`*bytes.Buffer`)
- Non-data structs such as servers, clients, handlers with a long lifecycle needing mutation

```go
// ✓ Value for config, time
func (s *Server) Start(cfg Config) error { ... }
func formatTimestamp(t time.Time) string { ... }

// ✓ Pointer for mutation, semantics
func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request)
```

## Goroutines

- Goroutines must not leak. Use contexts or wait groups to manage lifecycle.
- Goroutines must not be unbounded in number.

```go
func deleteUsers(ctx context.Context, userIDs []int) ([]User, error) {
	eg, ctx := errgroup.WithContext(ctx)
	eg.SetLimit(5) // ✓ Bound concurrency
	users := make([]User, len(userIDs))

	for i, id := range userIDs {
		eg.Go(func() error {
			user, err := fetchUser(ctx, id)
			if err != nil {
				return fmt.Errorf("fetch user %d: %w", id, err)
			}
			users[i] = user
			return nil
		})
	}

    // ✓ Wait for all goroutines to finish
	if err := eg.Wait(); err != nil {
		return nil, err
	}

	return users, nil
}
```

## Interfaces

**Placement**: Define interfaces in the consuming package, not the implementing package.
**Embedding**: Prefer composition over type embedding to avoid surprises.

```go
// ✓ Pass interface by value
func parseYAML(r io.Reader) (Config, error) { ... }

// ✗ Pointer to interface
func parseYAML(r *io.Reader) (Config, error) { ... }
```

### Testability

Don't add interfaces just for testing. Code should be testable as-is. Accept interfaces and return structs.

## Documentation

```go
// Package server provides HTTP server functionality.
package server

// Config contains server configuration.
type Config struct {
    Port int
}

// New creates a server instance.
func New(cfg Config) *Server { ... }
```

## Miscellaneous

- API surface should be minimal; unexported by default.
- Use logging sparingly; log only when it adds important context.
- Prefer the standard library over third-party packages unless absolutely necessary.
- Avoid init functions; prefer explicit initialization.
- Use `iota` (starting from `1`) for related constants. `stringer` can be used for generating string representations.
- Use `defer` for resource cleanup and unlocking mutexes.

## Additional References

- Refer to [TESTING.md](./TESTING.md) when writing tests.
- Refer to [PKG_DESIGN.md](./PKG_DESIGN.md) when designing and creating packages.
