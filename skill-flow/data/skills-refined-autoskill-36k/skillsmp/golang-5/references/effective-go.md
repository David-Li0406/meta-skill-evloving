# Effective Go Patterns

Idiomatic Go patterns that embrace the language's philosophy.

## Naming Conventions

```go
// Package names: short, lowercase, no underscores
package httputil  // not http_util

// Exported names: MixedCaps
func ReadFile() {}  // exported
func readFile() {}  // unexported

// Interfaces: -er suffix for single method
type Reader interface { Read(p []byte) (n int, err error) }
type Stringer interface { String() string }

// Getters: no "Get" prefix
func (u *User) Name() string { return u.name }  // not GetName()
```

## Interface Design

```go
// Accept interfaces, return structs
type UserGetter interface {
    GetUser(ctx context.Context, id string) (*User, error)
}

func NewHandler(users UserGetter) *Handler {
    return &Handler{users: users}
}

// Keep interfaces small (1-3 methods)
// io.Reader, io.Writer are ideal examples

// Define interfaces where they're used, not where implemented
// package handlers (consumer)
type UserStore interface {
    GetUser(ctx context.Context, id string) (*User, error)
}
```

## Error Handling

```go
// Always handle errors immediately
result, err := doSomething()
if err != nil {
    return fmt.Errorf("doSomething: %w", err)
}

// Use sentinel errors for expected conditions
var ErrNotFound = errors.New("not found")

// Check error types
if errors.Is(err, ErrNotFound) {
    // handle not found
}

// Extract error details
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    fmt.Println("Failed path:", pathErr.Path)
}

// Don't panic for recoverable errors
// Reserve panic for programmer errors only
```

## Concurrency

```go
// Use context for cancellation
func process(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case result := <-work():
        return handle(result)
    }
}

// WaitGroup for goroutine coordination
var wg sync.WaitGroup
for _, item := range items {
    wg.Add(1)
    go func(item Item) {
        defer wg.Done()
        process(item)
    }(item)
}
wg.Wait()

// errgroup for error propagation
g, ctx := errgroup.WithContext(ctx)
for _, item := range items {
    item := item  // capture
    g.Go(func() error {
        return process(ctx, item)
    })
}
if err := g.Wait(); err != nil {
    return err
}
```

## Struct Initialization

```go
// Use field names for clarity
user := User{
    Name:  "Alice",
    Email: "alice@example.com",
    Age:   30,
}

// Functional options for complex construction
type Option func(*Server)

func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{addr: addr, timeout: defaultTimeout}
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

## Common Anti-Patterns

```go
// ❌ Ignoring errors
result, _ := something()

// ❌ Naked returns in long functions
func process() (result string, err error) {
    // 50 lines later...
    return  // What's being returned?
}

// ❌ Global state
var db *sql.DB  // use dependency injection

// ❌ init() for complex setup
func init() { /* complex initialization */ }
// Better: explicit initialization in main()

// ❌ Interface pollution
type UserRepository interface {
    GetUser() error
    CreateUser() error
    UpdateUser() error
    DeleteUser() error
    ListUsers() error
    // ... 20 more methods
}
// Better: small, focused interfaces
```

## Testing

```go
// Table-driven tests
func TestAdd(t *testing.T) {
    tests := []struct {
        name string
        a, b int
        want int
    }{
        {"positive", 1, 2, 3},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := Add(tt.a, tt.b)
            if got != tt.want {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.want)
            }
        })
    }
}

// Use testify for assertions (optional)
assert.Equal(t, expected, actual)
require.NoError(t, err)
```
