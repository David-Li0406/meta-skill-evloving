---
title: Channel Size Selection
impact: HIGH
impactDescription: Correct buffering strategy
tags: concurrency, channel, buffer
---

## Channel Size Selection

Channel size should be 0 or 1; larger buffers require careful justification.

**Unbuffered Channel (size=0):**

```go
// Synchronous communication, sender blocks until receiver receives
done := make(chan struct{})

go func() {
    // Work...
    close(done)  // Signal completion
}()

<-done  // Wait for completion
```

**Buffer Size 1 Channel:**

```go
// Allow at most one pending item
// Commonly used for signal notification to prevent goroutine leaks
notify := make(chan struct{}, 1)

// Non-blocking send
select {
case notify <- struct{}{}:
default:
    // Already has pending notification, skip
}
```

**Why Avoid Large Buffers:**

```go
// Bad: Large buffer hides problems
ch := make(chan Task, 1000)

// Problems:
// 1. Producer doesn't know if consumer is keeping up
// 2. Uncontrolled memory usage
// 3. Data may be lost on shutdown
// 4. Latency issues are hidden
```

**Valid Reasons for Large Buffers:**

```go
// 1. Explicit batch processing scenarios
batchSize := 100
batch := make(chan Item, batchSize)

// 2. Burst traffic smoothing (with clear bounds)
// Must have backpressure mechanism
const maxBurst = 1000
queue := make(chan Request, maxBurst)

// 3. Semaphore pattern
semaphore := make(chan struct{}, 10)  // Limit to 10 concurrent

for _, task := range tasks {
    semaphore <- struct{}{}  // Acquire semaphore
    go func(t Task) {
        defer func() { <-semaphore }()  // Release
        process(t)
    }(task)
}
```

**Selection Guide:**

| Scenario | Recommended Size |
|----------|------------------|
| Synchronous communication | 0 |
| Signal notification (prevent leaks) | 1 |
| Semaphore/rate limiting | N (explicit concurrency count) |
| Batch processing | Batch size |
| Other cases | Requires written justification |

**Alternatives to Large Buffers:**

```go
// Use worker pool instead of large buffer
func workerPool(tasks <-chan Task, workers int) {
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for task := range tasks {
                process(task)
            }
        }()
    }
    wg.Wait()
}
```
