# Concurrency Cookbook

Recipes for goroutines, channels, synchronization, and concurrent patterns in Go.

---

## Basic Goroutines with WaitGroup

**Problem**: How to run multiple tasks concurrently and wait for all to complete?

**Solution**:
```go
import "sync"

func processAll(items []Item) {
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)
        go func(it Item) {
            defer wg.Done()
            process(it)
        }(item)
    }

    wg.Wait()
}
```

**Tip**: Always call `wg.Add(1)` before starting the goroutine, not inside it - prevents race conditions.

---

## Goroutines with Results

**Problem**: How to collect results from multiple concurrent goroutines?

**Solution**:
```go
func processAllWithResults(items []Item) []Result {
    results := make([]Result, len(items))
    var wg sync.WaitGroup

    for i, item := range items {
        wg.Add(1)
        go func(idx int, it Item) {
            defer wg.Done()
            results[idx] = process(it)
        }(i, item)
    }

    wg.Wait()
    return results
}
```

**Tip**: Writing to different slice indices is safe without mutex. The pre-allocated slice avoids races.

---

## Producer-Consumer Pattern

**Problem**: How to decouple data production from consumption using channels?

**Solution**:
```go
func producer(ch chan<- int) {
    for i := 0; i < 10; i++ {
        ch <- i
    }
    close(ch)
}

func consumer(ch <-chan int) {
    for v := range ch {
        fmt.Println(v)
    }
}

func main() {
    ch := make(chan int, 10) // Buffered channel
    go producer(ch)
    consumer(ch)
}
```

**Tip**: Always close channels from the sender side. Use directional channel types (`chan<-`, `<-chan`) for clarity.

---

## Fan-Out/Fan-In

**Problem**: How to distribute work across multiple workers and merge their results?

**Solution**:
```go
func fanOut(input <-chan int, workers int) []<-chan int {
    outputs := make([]<-chan int, workers)
    for i := 0; i < workers; i++ {
        outputs[i] = worker(input)
    }
    return outputs
}

func fanIn(channels ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)

    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for v := range c {
                out <- v
            }
        }(ch)
    }

    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}
```

**Tip**: Fan-out distributes load; fan-in merges results. Combine for parallel pipelines.

---

## Select with Timeout

**Problem**: How to avoid blocking forever when waiting for channel operations?

**Solution**:
```go
func doWithTimeout(ch <-chan Result, timeout time.Duration) (Result, error) {
    select {
    case result := <-ch:
        return result, nil
    case <-time.After(timeout):
        return Result{}, errors.New("timeout")
    }
}
```

**Tip**: `time.After` creates a new timer each call. For loops, use `time.NewTimer` and call `Reset()`.

---

## Context Cancellation

**Problem**: How to gracefully stop long-running goroutines?

**Solution**:
```go
func longRunningTask(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
            if done := doPartialWork(); done {
                return nil
            }
        }
    }
}

// Usage
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

go func() {
    time.Sleep(5 * time.Second)
    cancel()
}()

err := longRunningTask(ctx)
```

**Tip**: Always `defer cancel()` to prevent context leaks. Check `ctx.Done()` in loops.

---

## Context Timeout

**Problem**: How to automatically cancel operations that take too long?

**Solution**:
```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

result, err := fetchData(ctx, url)
if errors.Is(err, context.DeadlineExceeded) {
    log.Println("request timed out")
}
```

**Tip**: Pass context as the first parameter. Most stdlib and third-party APIs accept context.

---

## Context Values

**Problem**: How to pass request-scoped data through function calls without changing signatures?

**Solution**:
```go
type ctxKey string

const userIDKey ctxKey = "userID"

func WithUserID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, userIDKey, id)
}

func UserIDFrom(ctx context.Context) (string, bool) {
    id, ok := ctx.Value(userIDKey).(string)
    return id, ok
}
```

**Tip**: Use custom types for keys to avoid collisions. Only use for request-scoped data, not dependencies.

---

## errgroup for Concurrent Operations

**Problem**: How to run concurrent operations and return on first error?

**Solution**:
```go
import "golang.org/x/sync/errgroup"

func fetchAll(urls []string) ([]Response, error) {
    g, ctx := errgroup.WithContext(context.Background())
    responses := make([]Response, len(urls))

    for i, url := range urls {
        i, url := i, url
        g.Go(func() error {
            resp, err := fetch(ctx, url)
            if err != nil {
                return err
            }
            responses[i] = resp
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, err
    }
    return responses, nil
}
```

**Tip**: The context from `errgroup.WithContext` is cancelled when any goroutine returns an error.

---

## errgroup with Concurrency Limit

**Problem**: How to limit the number of concurrent goroutines to avoid overwhelming resources?

**Solution**:
```go
func processWithLimit(items []Item, limit int) error {
    g := new(errgroup.Group)
    g.SetLimit(limit)

    for _, item := range items {
        item := item
        g.Go(func() error {
            return process(item)
        })
    }

    return g.Wait()
}
```

**Tip**: Use `TryGo` instead of `Go` for non-blocking - returns false if limit reached.

---

## sourcegraph/conc Pool

**Problem**: How to manage goroutine pools with a cleaner API than errgroup?

**Solution**:
```go
import "github.com/sourcegraph/conc/pool"

// Basic pool
func processWithPool(items []Item) {
    p := pool.New().WithMaxGoroutines(10)
    for _, item := range items {
        item := item
        p.Go(func() { process(item) })
    }
    p.Wait()
}

// Pool with results
func processWithResults(items []Item) []Result {
    p := pool.NewWithResults[Result]().WithMaxGoroutines(10)
    for _, item := range items {
        item := item
        p.Go(func() Result { return process(item) })
    }
    return p.Wait()
}

// Pool with errors
func processWithErrors(items []Item) error {
    p := pool.New().WithErrors().WithMaxGoroutines(10)
    for _, item := range items {
        item := item
        p.Go(func() error { return process(item) })
    }
    return p.Wait()
}
```

**Tip**: `conc` panics are caught and re-raised cleanly. Results are collected automatically.

---

## conc Stream for Ordered Results

**Problem**: How to process items concurrently but handle results in original order?

**Solution**:
```go
import "github.com/sourcegraph/conc/stream"

func processOrdered(items []Item) {
    s := stream.New().WithMaxGoroutines(10)

    for _, item := range items {
        item := item
        s.Go(func() stream.Callback {
            result := process(item) // Runs concurrently
            return func() {
                handleResult(result) // Runs sequentially, in order
            }
        })
    }

    s.Wait()
}
```

**Tip**: The inner closure runs concurrently; the returned callback runs sequentially in submission order.

---

## Mutex for Shared State

**Problem**: How to safely access shared data from multiple goroutines?

**Solution**:
```go
type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Inc() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}

func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.value
}
```

**Tip**: Keep the critical section small. Consider `atomic` package for simple counters.

---

## RWMutex for Read-Heavy Workloads

**Problem**: How to allow concurrent reads while ensuring exclusive writes?

**Solution**:
```go
type Cache struct {
    mu   sync.RWMutex
    data map[string]string
}

func (c *Cache) Get(key string) (string, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    v, ok := c.data[key]
    return v, ok
}

func (c *Cache) Set(key, value string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.data[key] = value
}
```

**Tip**: Use `RWMutex` when reads vastly outnumber writes. Multiple readers can hold `RLock` simultaneously.

---

## sync.Once for One-Time Initialization

**Problem**: How to ensure initialization code runs exactly once, even with concurrent calls?

**Solution**:
```go
type Client struct {
    initOnce sync.Once
    conn     *Connection
}

func (c *Client) getConn() *Connection {
    c.initOnce.Do(func() {
        c.conn = connect()
    })
    return c.conn
}
```

**Tip**: `sync.Once` is goroutine-safe. Other goroutines block until `Do` completes.

---

## sync.Map for Concurrent Map Access

**Problem**: How to use a map safely from multiple goroutines without manual locking?

**Solution**:
```go
var cache sync.Map

// Store
cache.Store("key", value)

// Load
if v, ok := cache.Load("key"); ok {
    // Use v.(YourType)
}

// LoadOrStore - atomic get-or-set
actual, loaded := cache.LoadOrStore("key", newValue)

// Delete
cache.Delete("key")

// Range - iterate safely
cache.Range(func(key, value any) bool {
    fmt.Println(key, value)
    return true // Continue iteration
})
```

**Tip**: Best for caches with many reads, few writes, and disjoint key sets. Otherwise use `RWMutex` + regular map.

---

## Rate Limiting

**Problem**: How to limit the rate of operations (e.g., API calls)?

**Solution**:
```go
import "golang.org/x/time/rate"

// Allow 10 requests per second, burst of 20
limiter := rate.NewLimiter(10, 20)

func handleRequest(ctx context.Context) error {
    if err := limiter.Wait(ctx); err != nil {
        return err // Context cancelled
    }
    return processRequest()
}

// Non-blocking check
if limiter.Allow() {
    processRequest()
} else {
    return errors.New("rate limited")
}
```

**Tip**: `Wait` blocks until allowed; `Allow` returns immediately. Use `Reserve` for custom scheduling.
