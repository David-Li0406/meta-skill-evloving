---
title: Channel Usage Patterns
impact: HIGH
impactDescription: Use channels correctly
tags: concurrency, channel, patterns
---

## Channel Usage Patterns

Use channels correctly for inter-goroutine communication.

**Common Patterns:**

```go
// 1. Signal channel (no data transfer)
done := make(chan struct{})
close(done) // Broadcast signal

// 2. Send with timeout
select {
case ch <- data:
case <-time.After(5 * time.Second):
    return errors.New("send timeout")
}

// 3. Receive with timeout
select {
case data := <-ch:
    process(data)
case <-time.After(5 * time.Second):
    return errors.New("receive timeout")
}

// 4. Non-blocking operation
select {
case ch <- data:
default:
    // Channel is full, handle overflow
}

// 5. Fan-out
func fanOut(input <-chan int, workers int) []<-chan int {
    outputs := make([]<-chan int, workers)
    for i := 0; i < workers; i++ {
        outputs[i] = worker(input)
    }
    return outputs
}

// 6. Fan-in
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

**Rules:**
- The sender is responsible for closing the channel
- Closing an already closed channel will panic
- Sending to a closed channel will panic
- Receiving from a closed channel returns the zero value
