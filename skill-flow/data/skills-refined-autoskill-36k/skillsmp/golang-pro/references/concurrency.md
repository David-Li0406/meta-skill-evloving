# Go Concurrency Patterns

## Worker Pool with Bounded Concurrency

```go
func WorkerPool(ctx context.Context, jobs <-chan Job, workers int) <-chan Result {
    results := make(chan Result)
    var wg sync.WaitGroup

    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                select {
                case <-ctx.Done():
                    return
                default:
                    results <- process(job)
                }
            }
        }()
    }

    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}
```

## Channel Patterns

### Generator Pattern

```go
func Generate(ctx context.Context) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)
        for i := 0; ; i++ {
            select {
            case <-ctx.Done():
                return
            case ch <- i:
            }
        }
    }()
    return ch
}
```

### Fan-Out/Fan-In

Distribute work across goroutines, merge results back.

### Pipeline Pattern

Chain processing stages, each transforms data downstream.

## Synchronization

- `sync.Mutex` - Guards shared state
- `sync.RWMutex` - Optimizes read-heavy workloads
- `sync.Once` - Ensures initialization executes once
- `sync.WaitGroup` - Coordinates goroutine completion

## Select Patterns

- Timeout handling with `time.After`
- Graceful shutdown via done channels
- Context-aware cancellation

## Rate Limiting

Use `golang.org/x/time/rate` for token bucket approach.
