# Exercise 15: Context and Cancellation

**Time:** 15 minutes
**Goal:** Use context for timeouts, deadlines, and cancellation

## The Spring Boot Version

```java
// timeout via annotation
@Timeout(value = 5, unit = TimeUnit.SECONDS)
public Result process() { ... }

// or CompletableFuture
CompletableFuture.supplyAsync(() -> doWork())
    .orTimeout(5, TimeUnit.SECONDS)
    .join();
```

## The Go Way

Context carries deadlines, cancellation signals, and request-scoped values:

```go
// with timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

result, err := service.Process(ctx)
if errors.Is(err, context.DeadlineExceeded) {
    // timeout
}
```

---

## Step by Step

### 1. Basic context usage (3 min)

Create `internal/slowservice/service.go`:

```go
package slowservice

import (
    "context"
    "time"
)

type Service struct{}

func (s *Service) SlowOperation(ctx context.Context) (string, error) {
    // simulate slow work with context checking
    select {
    case <-time.After(2 * time.Second):
        return "completed", nil
    case <-ctx.Done():
        return "", ctx.Err()
    }
}
```

### 2. Timeout example (4 min)

```go
func ExampleTimeout() {
    svc := &Service{}

    // create context with 1 second timeout
    ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
    defer cancel()  // always call cancel to release resources

    result, err := svc.SlowOperation(ctx)
    if err != nil {
        if errors.Is(err, context.DeadlineExceeded) {
            fmt.Println("operation timed out")
            return
        }
        fmt.Println("error:", err)
        return
    }

    fmt.Println("result:", result)
}
```

### 3. Manual cancellation (4 min)

```go
func ExampleCancellation() {
    svc := &Service{}

    ctx, cancel := context.WithCancel(context.Background())

    // cancel after 500ms
    go func() {
        time.Sleep(500 * time.Millisecond)
        cancel()  // signal cancellation
    }()

    result, err := svc.SlowOperation(ctx)
    if err != nil {
        if errors.Is(err, context.Canceled) {
            fmt.Println("operation was cancelled")
            return
        }
    }

    fmt.Println("result:", result)
}
```

### 4. Propagate context through layers (4 min)

```go
// handler receives context from request
func (h *Handler) GetData(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()  // request context (cancelled if client disconnects)

    // add timeout for this specific operation
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    // pass to service
    data, err := h.service.FetchData(ctx)
    if err != nil {
        // handle error
    }
}

// service passes to repository
func (s *Service) FetchData(ctx context.Context) (*Data, error) {
    return s.repo.FindData(ctx)
}

// repository passes to database
func (r *Repository) FindData(ctx context.Context) (*Data, error) {
    return r.db.QueryContext(ctx, "SELECT ...")
}
```

### 5. Context values (request-scoped data)

```go
type contextKey string

const RequestIDKey contextKey = "request_id"

// set value
ctx = context.WithValue(ctx, RequestIDKey, "abc-123")

// get value
if id, ok := ctx.Value(RequestIDKey).(string); ok {
    fmt.Println("request ID:", id)
}
```

## Best Practices

### Always pass context as first parameter

```go
// good
func Process(ctx context.Context, input string) error

// bad
func Process(input string, ctx context.Context) error
```

### Always call cancel()

```go
ctx, cancel := context.WithTimeout(context.Background(), time.Second)
defer cancel()  // prevents resource leak
```

### Check context in loops

```go
for _, item := range items {
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
    }
    process(item)
}
```

### Don't store context in structs

```go
// bad
type Service struct {
    ctx context.Context  // don't do this
}

// good - pass context to methods
func (s *Service) DoWork(ctx context.Context) error
```

## Context Hierarchy

```go
// contexts form a tree
root := context.Background()

// child contexts inherit from parent
ctx1, cancel1 := context.WithTimeout(root, 5*time.Second)
ctx2, cancel2 := context.WithTimeout(ctx1, 2*time.Second)  // nested, shorter timeout

// cancelling parent cancels all children
cancel1()  // ctx1 and ctx2 both cancelled
```

## HTTP Request Context

```go
func (h *Handler) Handle(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()  // cancelled when:
                        // - client disconnects
                        // - request completes
                        // - server shuts down

    // respect client disconnect
    result, err := h.service.LongOperation(ctx)
    if errors.Is(err, context.Canceled) {
        // client went away, don't bother responding
        return
    }
}
```

## What Just Happened?

| Java | Go |
|------|-----|
| Thread.interrupt() | context.Cancel() |
| InterruptedException | context.Canceled |
| @Timeout annotation | context.WithTimeout |
| ThreadLocal | context.WithValue |

## Checkpoint

- [ ] Can create timeout context
- [ ] Can manually cancel operations
- [ ] Pass context through all layers
- [ ] Check ctx.Done() in long operations

**Next:** Exercise 16 - Observability
