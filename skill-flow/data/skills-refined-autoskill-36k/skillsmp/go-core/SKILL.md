---
name: Go Core
description: Go language fundamentals, concurrency, error handling, and project patterns.
metadata:
  labels: [golang, core, language]
  triggers:
    files: ['go.mod', '**/*.go']
    keywords: [func, package, import, goroutine, chan]
---

# Go Core Standards

## Goroutines & Channels

```go
// Spawn goroutine
go func() {
    result := process(data)
    resultChan <- result
}()

// Unbuffered channel (synchronous)
ch := make(chan int)

// Buffered channel
ch := make(chan int, 100)

// Send and receive
ch <- value      // Send
value := <-ch    // Receive

// Select for multiplexing
select {
case msg := <-msgChan:
    handle(msg)
case <-time.After(5 * time.Second):
    return errors.New("timeout")
case <-ctx.Done():
    return ctx.Err()
}
```

**Patterns**:
- Worker pools with buffered channels
- Fan-out/fan-in for parallel processing
- Done channel for cancellation

## Error Handling

```go
// Return errors, don't panic
func fetchUser(id int) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, fmt.Errorf("fetch user %d: %w", id, err)
    }
    return user, nil
}

// Error wrapping (Go 1.13+)
if errors.Is(err, sql.ErrNoRows) {
    return nil, ErrNotFound
}

// Type assertion for custom errors
var apiErr *APIError
if errors.As(err, &apiErr) {
    log.Printf("API error: %d", apiErr.Code)
}

// Sentinel errors
var ErrNotFound = errors.New("not found")
```

**Rules**:
- Always check errors immediately
- Wrap with context: `fmt.Errorf("operation: %w", err)`
- Use `errors.Is` and `errors.As` for comparison
- **Never**: `panic` for recoverable errors

## Interfaces

```go
// Small interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Composition
type ReadWriter interface {
    Reader
    Writer
}

// Accept interfaces, return structs
func ProcessData(r Reader) (*Result, error) {
    data, err := io.ReadAll(r)
    // ...
    return &Result{}, nil
}
```

**Best Practices**:
- Define interfaces where used, not where implemented
- Keep interfaces small (1-3 methods)
- Use `interface{}` sparingly; prefer generics (Go 1.18+)

## Context

```go
// Pass context as first parameter
func fetchData(ctx context.Context, id int) (*Data, error) {
    // Respect cancellation
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    default:
    }

    // Use context with HTTP requests
    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    return client.Do(req)
}

// Add timeout
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()

// Add values (use sparingly)
ctx = context.WithValue(ctx, requestIDKey, reqID)
```

**Rules**:
- Never store context in structs
- Always call cancel function (use defer)
- Use for cancellation, deadlines, request-scoped values only

## Project Structure

```
project/
├── cmd/
│   └── myapp/
│       └── main.go       # Entry point
├── internal/             # Private packages
│   ├── handler/
│   ├── service/
│   └── repository/
├── pkg/                  # Public packages
├── api/                  # API definitions (proto, OpenAPI)
├── configs/
├── go.mod
└── go.sum
```

**Conventions**:
- `internal/` prevents external imports
- `cmd/` for multiple entry points
- Flat structure for small projects

## Testing

```go
// Table-driven tests
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 1, 2, 3},
        {"negative", -1, -1, -2},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

// Parallel tests
func TestParallel(t *testing.T) {
    t.Parallel()
    // ...
}

// Benchmarks
func BenchmarkProcess(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Process(data)
    }
}
```

## Performance

1. **Preallocate slices**: `make([]T, 0, expectedLen)`
2. **Avoid allocations**: Reuse buffers, use `sync.Pool`
3. **Profile first**: `go tool pprof` before optimizing
4. **Escape analysis**: `go build -gcflags='-m'` to check heap escapes
5. **String building**: Use `strings.Builder` not `+` concatenation
