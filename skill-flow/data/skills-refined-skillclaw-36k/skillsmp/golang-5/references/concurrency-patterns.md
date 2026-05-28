# Go Concurrency Patterns

## Goroutines

### Basic Spawning

```go
// Simple goroutine
go func() {
    doWork()
}()

// With parameters (capture by value)
for _, item := range items {
    item := item  // Create new variable for closure
    go func() {
        process(item)
    }()
}

// Go 1.22+: Loop variables are per-iteration
for _, item := range items {
    go func() {
        process(item)  // Safe in Go 1.22+
    }()
}
```

### Waiting for Completion

```go
// WaitGroup for multiple goroutines
func processAll(items []Item) {
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)
        go func(it Item) {
            defer wg.Done()
            process(it)
        }(item)
    }

    wg.Wait()  // Block until all complete
}
```

## Channels

### Channel Basics

```go
// Unbuffered - synchronous
ch := make(chan int)

// Buffered - async up to capacity
ch := make(chan int, 100)

// Send and receive
ch <- value    // Send
value := <-ch  // Receive

// Close channel (sender only)
close(ch)

// Check if closed
value, ok := <-ch
if !ok {
    // Channel closed
}
```

### Channel Directions

```go
// Send-only channel
func producer(out chan<- int) {
    for i := 0; i < 10; i++ {
        out <- i
    }
    close(out)
}

// Receive-only channel
func consumer(in <-chan int) {
    for value := range in {
        process(value)
    }
}

// Bidirectional converted at call site
func main() {
    ch := make(chan int)
    go producer(ch)  // ch -> chan<- int
    consumer(ch)     // ch -> <-chan int
}
```

## Common Patterns

### Fan-Out / Fan-In

```go
// Fan-out: Distribute work to multiple goroutines
func fanOut(input <-chan int, workers int) []<-chan int {
    outputs := make([]<-chan int, workers)
    for i := 0; i < workers; i++ {
        outputs[i] = worker(input)
    }
    return outputs
}

func worker(input <-chan int) <-chan int {
    output := make(chan int)
    go func() {
        defer close(output)
        for n := range input {
            output <- process(n)
        }
    }()
    return output
}

// Fan-in: Merge multiple channels into one
func fanIn(inputs ...<-chan int) <-chan int {
    output := make(chan int)
    var wg sync.WaitGroup

    for _, in := range inputs {
        wg.Add(1)
        go func(ch <-chan int) {
            defer wg.Done()
            for n := range ch {
                output <- n
            }
        }(in)
    }

    go func() {
        wg.Wait()
        close(output)
    }()

    return output
}
```

### Worker Pool

```go
func workerPool(jobs <-chan Job, results chan<- Result, workers int) {
    var wg sync.WaitGroup

    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                results <- processJob(job)
            }
        }()
    }

    // Close results when all workers done
    go func() {
        wg.Wait()
        close(results)
    }()
}

// Usage
func main() {
    jobs := make(chan Job, 100)
    results := make(chan Result, 100)

    workerPool(jobs, results, 5)

    // Send jobs
    go func() {
        for _, job := range allJobs {
            jobs <- job
        }
        close(jobs)
    }()

    // Collect results
    for result := range results {
        handleResult(result)
    }
}
```

### Pipeline

```go
func pipeline() {
    // Stage 1: Generate numbers
    gen := func(nums ...int) <-chan int {
        out := make(chan int)
        go func() {
            defer close(out)
            for _, n := range nums {
                out <- n
            }
        }()
        return out
    }

    // Stage 2: Square numbers
    square := func(in <-chan int) <-chan int {
        out := make(chan int)
        go func() {
            defer close(out)
            for n := range in {
                out <- n * n
            }
        }()
        return out
    }

    // Connect stages
    nums := gen(1, 2, 3, 4, 5)
    squared := square(nums)

    for n := range squared {
        fmt.Println(n)
    }
}
```

### Select Statement

```go
// Multiple channel operations
select {
case msg := <-msgCh:
    handleMessage(msg)
case err := <-errCh:
    handleError(err)
case <-time.After(5 * time.Second):
    handleTimeout()
case <-ctx.Done():
    return ctx.Err()
}

// Non-blocking with default
select {
case msg := <-ch:
    process(msg)
default:
    // Channel empty, do something else
}
```

## Context for Cancellation

### Creating Contexts

```go
// Root context
ctx := context.Background()

// With cancellation
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

// With timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

// With deadline
deadline := time.Now().Add(10 * time.Second)
ctx, cancel := context.WithDeadline(context.Background(), deadline)
defer cancel()

// With value (use sparingly)
ctx = context.WithValue(ctx, "requestID", "abc123")
```

### Using Context

```go
func doWork(ctx context.Context) error {
    // Check cancellation
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
    }

    // Or in a loop
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case item := <-workCh:
            process(item)
        }
    }
}

// Pass context as first parameter
func fetchData(ctx context.Context, url string) ([]byte, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }
    // Request will be cancelled if context is cancelled
    resp, err := http.DefaultClient.Do(req)
    // ...
}
```

## Synchronization Primitives

### Mutex

```go
type SafeCounter struct {
    mu    sync.Mutex
    count int
}

func (c *SafeCounter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *SafeCounter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}
```

### RWMutex

```go
type Cache struct {
    mu   sync.RWMutex
    data map[string]string
}

// Multiple readers allowed
func (c *Cache) Get(key string) (string, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    val, ok := c.data[key]
    return val, ok
}

// Exclusive writer
func (c *Cache) Set(key, value string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.data[key] = value
}
```

### Once

```go
var (
    instance *Singleton
    once     sync.Once
)

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{}
        instance.initialize()
    })
    return instance
}
```

### Atomic Operations

```go
import "sync/atomic"

type Counter struct {
    value atomic.Int64
}

func (c *Counter) Increment() {
    c.value.Add(1)
}

func (c *Counter) Value() int64 {
    return c.value.Load()
}

// Atomic pointer
var config atomic.Pointer[Config]

func UpdateConfig(c *Config) {
    config.Store(c)
}

func GetConfig() *Config {
    return config.Load()
}
```

## Error Handling in Goroutines

### errgroup Package

```go
import "golang.org/x/sync/errgroup"

func fetchAll(ctx context.Context, urls []string) ([][]byte, error) {
    g, ctx := errgroup.WithContext(ctx)
    results := make([][]byte, len(urls))

    for i, url := range urls {
        i, url := i, url  // Capture for closure
        g.Go(func() error {
            data, err := fetch(ctx, url)
            if err != nil {
                return err
            }
            results[i] = data
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, err
    }
    return results, nil
}
```

### Manual Error Collection

```go
func processAll(items []Item) error {
    errCh := make(chan error, len(items))

    for _, item := range items {
        go func(it Item) {
            errCh <- process(it)
        }(item)
    }

    var errs []error
    for range items {
        if err := <-errCh; err != nil {
            errs = append(errs, err)
        }
    }

    if len(errs) > 0 {
        return fmt.Errorf("processing failed: %v", errs)
    }
    return nil
}
```

## Common Mistakes

### Goroutine Leak

```go
// ❌ Leaking goroutine - channel never read
func leak() {
    ch := make(chan int)
    go func() {
        ch <- 42  // Blocks forever
    }()
    // Function returns, goroutine stuck
}

// ✅ Use buffered channel or ensure reader
func noLeak() {
    ch := make(chan int, 1)  // Buffered
    go func() {
        ch <- 42  // Won't block
    }()
}

// ✅ Or use context for cancellation
func noLeakWithContext(ctx context.Context) {
    ch := make(chan int)
    go func() {
        select {
        case ch <- 42:
        case <-ctx.Done():
            return
        }
    }()
}
```

### Race Condition

```go
// ❌ Race condition
var counter int
for i := 0; i < 1000; i++ {
    go func() {
        counter++  // Data race!
    }()
}

// ✅ Use mutex or atomic
var counter atomic.Int64
for i := 0; i < 1000; i++ {
    go func() {
        counter.Add(1)
    }()
}
```

## Testing Concurrent Code

```go
// Use -race flag
// go test -race ./...

func TestConcurrent(t *testing.T) {
    counter := NewSafeCounter()

    var wg sync.WaitGroup
    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter.Increment()
        }()
    }

    wg.Wait()

    if counter.Value() != 100 {
        t.Errorf("expected 100, got %d", counter.Value())
    }
}
```
