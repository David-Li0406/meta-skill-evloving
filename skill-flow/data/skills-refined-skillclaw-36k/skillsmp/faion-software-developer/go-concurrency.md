---
id: go-concurrency
name: "Go Concurrency Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Go Concurrency Patterns

## Overview

Go's concurrency model is built on goroutines and channels, enabling efficient parallel processing. This methodology covers common patterns for safe concurrent programming, including worker pools, pipelines, and synchronization primitives.

## When to Use

- Parallel processing of data
- HTTP servers handling concurrent requests
- Background task processing
- I/O-bound operations
- CPU-bound parallel computation

## Key Principles

1. **Don't communicate by sharing memory; share memory by communicating**
2. **Use channels for coordination** - Goroutines communicate via channels
3. **Keep critical sections small** - Minimize mutex-protected code
4. **Avoid goroutine leaks** - Always provide exit conditions
5. **Use context for cancellation** - Propagate cancellation signals

## Best Practices

### Basic Goroutine Patterns

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

// Simple goroutine with WaitGroup
func basicConcurrency() {
    var wg sync.WaitGroup

    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func(n int) {
            defer wg.Done()
            fmt.Printf("Worker %d starting\n", n)
            time.Sleep(time.Second)
            fmt.Printf("Worker %d done\n", n)
        }(i)
    }

    wg.Wait()
    fmt.Println("All workers completed")
}

// Goroutine with result channel
func fetchWithResult() {
    results := make(chan string, 3)

    go func() { results <- fetch("url1") }()
    go func() { results <- fetch("url2") }()
    go func() { results <- fetch("url3") }()

    for i := 0; i < 3; i++ {
        fmt.Println(<-results)
    }
}
```

### Worker Pool Pattern

```go
package worker

import (
    "context"
    "sync"
)

type Job struct {
    ID   int
    Data string
}

type Result struct {
    JobID int
    Value string
    Err   error
}

// Worker pool processes jobs concurrently
func WorkerPool(ctx context.Context, numWorkers int, jobs <-chan Job) <-chan Result {
    results := make(chan Result, numWorkers)

    var wg sync.WaitGroup

    // Start workers
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func(workerID int) {
            defer wg.Done()
            for {
                select {
                case job, ok := <-jobs:
                    if !ok {
                        return // Channel closed
                    }
                    result := processJob(job)
                    select {
                    case results <- result:
                    case <-ctx.Done():
                        return
                    }
                case <-ctx.Done():
                    return
                }
            }
        }(i)
    }

    // Close results when all workers done
    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}

func processJob(job Job) Result {
    // Process the job
    return Result{
        JobID: job.ID,
        Value: "processed: " + job.Data,
    }
}

// Usage
func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    jobs := make(chan Job, 100)

    // Start worker pool
    results := WorkerPool(ctx, 5, jobs)

    // Send jobs
    go func() {
        for i := 0; i < 100; i++ {
            jobs <- Job{ID: i, Data: fmt.Sprintf("data-%d", i)}
        }
        close(jobs)
    }()

    // Collect results
    for result := range results {
        if result.Err != nil {
            log.Printf("job %d failed: %v", result.JobID, result.Err)
        } else {
            log.Printf("job %d: %s", result.JobID, result.Value)
        }
    }
}
```

### Pipeline Pattern

```go
package pipeline

import "context"

// Stage 1: Generate numbers
func generate(ctx context.Context, nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

// Stage 2: Square numbers
func square(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case out <- n * n:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

// Stage 3: Filter even numbers
func filterEven(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            if n%2 == 0 {
                select {
                case out <- n:
                case <-ctx.Done():
                    return
                }
            }
        }
    }()
    return out
}

// Fan-out: Distribute work to multiple goroutines
func fanOut(ctx context.Context, in <-chan int, n int) []<-chan int {
    outs := make([]<-chan int, n)
    for i := 0; i < n; i++ {
        outs[i] = square(ctx, in)
    }
    return outs
}

// Fan-in: Merge multiple channels into one
func fanIn(ctx context.Context, channels ...<-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup

    output := func(c <-chan int) {
        defer wg.Done()
        for n := range c {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }

    wg.Add(len(channels))
    for _, c := range channels {
        go output(c)
    }

    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}

// Usage
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // Build pipeline
    nums := generate(ctx, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    squared := square(ctx, nums)
    even := filterEven(ctx, squared)

    for n := range even {
        fmt.Println(n)
    }
}
```

### Rate Limiting

```go
package ratelimit

import (
    "context"
    "time"
)

// Token bucket rate limiter
type RateLimiter struct {
    tokens   chan struct{}
    ticker   *time.Ticker
    quit     chan struct{}
}

func NewRateLimiter(rate int, burst int) *RateLimiter {
    rl := &RateLimiter{
        tokens: make(chan struct{}, burst),
        ticker: time.NewTicker(time.Second / time.Duration(rate)),
        quit:   make(chan struct{}),
    }

    // Fill initial tokens
    for i := 0; i < burst; i++ {
        rl.tokens <- struct{}{}
    }

    // Refill tokens
    go func() {
        for {
            select {
            case <-rl.ticker.C:
                select {
                case rl.tokens <- struct{}{}:
                default: // Bucket full
                }
            case <-rl.quit:
                return
            }
        }
    }()

    return rl
}

func (rl *RateLimiter) Wait(ctx context.Context) error {
    select {
    case <-rl.tokens:
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
}

func (rl *RateLimiter) Close() {
    rl.ticker.Stop()
    close(rl.quit)
}

// Usage with HTTP client
func fetchWithRateLimit(ctx context.Context, urls []string) {
    limiter := NewRateLimiter(10, 5) // 10 req/sec, burst of 5
    defer limiter.Close()

    var wg sync.WaitGroup
    for _, url := range urls {
        wg.Add(1)
        go func(u string) {
            defer wg.Done()

            if err := limiter.Wait(ctx); err != nil {
                return
            }

            resp, err := http.Get(u)
            if err != nil {
                log.Printf("fetch error: %v", err)
                return
            }
            defer resp.Body.Close()

            // Process response
        }(url)
    }
    wg.Wait()
}
```

### Semaphore Pattern

```go
package semaphore

import "context"

// Semaphore limits concurrent operations
type Semaphore chan struct{}

func New(n int) Semaphore {
    return make(chan struct{}, n)
}

func (s Semaphore) Acquire(ctx context.Context) error {
    select {
    case s <- struct{}{}:
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
}

func (s Semaphore) Release() {
    <-s
}

// Usage: Limit concurrent database connections
func processUsers(ctx context.Context, users []User) error {
    sem := New(10) // Max 10 concurrent operations
    var wg sync.WaitGroup
    errCh := make(chan error, len(users))

    for _, user := range users {
        wg.Add(1)
        go func(u User) {
            defer wg.Done()

            if err := sem.Acquire(ctx); err != nil {
                errCh <- err
                return
            }
            defer sem.Release()

            if err := processUser(ctx, u); err != nil {
                errCh <- err
            }
        }(user)
    }

    wg.Wait()
    close(errCh)

    // Collect first error
    for err := range errCh {
        return err
    }
    return nil
}
```

### Select with Timeout

```go
package main

import (
    "context"
    "fmt"
    "time"
)

// Timeout pattern
func fetchWithTimeout(url string, timeout time.Duration) (string, error) {
    ctx, cancel := context.WithTimeout(context.Background(), timeout)
    defer cancel()

    resultCh := make(chan string, 1)
    errCh := make(chan error, 1)

    go func() {
        result, err := doFetch(ctx, url)
        if err != nil {
            errCh <- err
            return
        }
        resultCh <- result
    }()

    select {
    case result := <-resultCh:
        return result, nil
    case err := <-errCh:
        return "", err
    case <-ctx.Done():
        return "", fmt.Errorf("timeout after %v", timeout)
    }
}

// First response wins
func fetchFirst(ctx context.Context, urls []string) (string, error) {
    ctx, cancel := context.WithCancel(ctx)
    defer cancel() // Cancel remaining requests

    resultCh := make(chan string, len(urls))

    for _, url := range urls {
        go func(u string) {
            result, err := doFetch(ctx, u)
            if err == nil {
                resultCh <- result
            }
        }(url)
    }

    select {
    case result := <-resultCh:
        return result, nil
    case <-ctx.Done():
        return "", ctx.Err()
    }
}
```

### Mutex and RWMutex

```go
package cache

import (
    "sync"
    "time"
)

// Thread-safe cache with RWMutex
type Cache struct {
    mu    sync.RWMutex
    items map[string]*cacheItem
}

type cacheItem struct {
    value     interface{}
    expiresAt time.Time
}

func NewCache() *Cache {
    return &Cache{
        items: make(map[string]*cacheItem),
    }
}

func (c *Cache) Get(key string) (interface{}, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()

    item, exists := c.items[key]
    if !exists {
        return nil, false
    }

    if time.Now().After(item.expiresAt) {
        return nil, false
    }

    return item.value, true
}

func (c *Cache) Set(key string, value interface{}, ttl time.Duration) {
    c.mu.Lock()
    defer c.mu.Unlock()

    c.items[key] = &cacheItem{
        value:     value,
        expiresAt: time.Now().Add(ttl),
    }
}

func (c *Cache) Delete(key string) {
    c.mu.Lock()
    defer c.mu.Unlock()

    delete(c.items, key)
}

// Cleanup expired items periodically
func (c *Cache) StartCleanup(interval time.Duration) {
    ticker := time.NewTicker(interval)
    go func() {
        for range ticker.C {
            c.mu.Lock()
            now := time.Now()
            for key, item := range c.items {
                if now.After(item.expiresAt) {
                    delete(c.items, key)
                }
            }
            c.mu.Unlock()
        }
    }()
}
```

### Once Pattern

```go
package singleton

import "sync"

type Database struct {
    conn string
}

var (
    instance *Database
    once     sync.Once
)

// GetDatabase returns singleton database instance
func GetDatabase() *Database {
    once.Do(func() {
        instance = &Database{
            conn: "connection_string",
        }
    })
    return instance
}

// Lazy initialization per key
type LazyMap struct {
    mu    sync.Mutex
    items map[string]*sync.Once
    data  map[string]interface{}
}

func (m *LazyMap) Get(key string, init func() interface{}) interface{} {
    m.mu.Lock()
    if m.items == nil {
        m.items = make(map[string]*sync.Once)
        m.data = make(map[string]interface{})
    }

    o, exists := m.items[key]
    if !exists {
        o = &sync.Once{}
        m.items[key] = o
    }
    m.mu.Unlock()

    o.Do(func() {
        m.mu.Lock()
        m.data[key] = init()
        m.mu.Unlock()
    })

    m.mu.Lock()
    defer m.mu.Unlock()
    return m.data[key]
}
```

## Anti-patterns

### Avoid: Goroutine Leaks

```go
// BAD - goroutine never exits if no consumer
func leakyGenerator() <-chan int {
    ch := make(chan int)
    go func() {
        for i := 0; ; i++ {
            ch <- i // Blocks forever if no consumer
        }
    }()
    return ch
}

// GOOD - goroutine exits when context cancelled
func safeGenerator(ctx context.Context) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)
        for i := 0; ; i++ {
            select {
            case ch <- i:
            case <-ctx.Done():
                return
            }
        }
    }()
    return ch
}
```

### Avoid: Data Races

```go
// BAD - concurrent map access
var cache = make(map[string]int)

func increment(key string) {
    cache[key]++ // RACE!
}

// GOOD - use mutex or sync.Map
var (
    cache = make(map[string]int)
    mu    sync.Mutex
)

func increment(key string) {
    mu.Lock()
    cache[key]++
    mu.Unlock()
}
```

## References

- [Go Concurrency Patterns](https://go.dev/blog/pipelines)
- [Go Concurrency Patterns: Context](https://go.dev/blog/context)
- [Share Memory By Communicating](https://go.dev/blog/codelab-share)
- [Advanced Go Concurrency Patterns](https://go.dev/blog/io2013-talk-concurrency)
