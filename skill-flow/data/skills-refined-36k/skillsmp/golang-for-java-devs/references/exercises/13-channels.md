# Exercise 13: Channels

**Time:** 15 minutes
**Goal:** Communicate between goroutines using channels

## The Spring Boot Version

```java
BlockingQueue<Task> queue = new LinkedBlockingQueue<>();

// producer
queue.put(task);

// consumer
Task task = queue.take();  // blocks until available
```

## The Go Way

Channels are typed conduits for communication:

```go
ch := make(chan Task)

// sender
ch <- task

// receiver
task := <-ch
```

---

## Step by Step

### 1. Basic channel usage (3 min)

Create `internal/worker/basic.go`:

```go
package worker

import "fmt"

func BasicChannel() {
    // create unbuffered channel
    ch := make(chan string)

    // sender goroutine
    go func() {
        ch <- "hello"  // blocks until receiver ready
    }()

    // receive
    msg := <-ch  // blocks until sender ready
    fmt.Println(msg)
}
```

### 2. Buffered channels (3 min)

```go
func BufferedChannel() {
    // buffer size of 3
    ch := make(chan int, 3)

    // can send without blocking (up to buffer size)
    ch <- 1
    ch <- 2
    ch <- 3
    // ch <- 4  // would block!

    fmt.Println(<-ch)  // 1
    fmt.Println(<-ch)  // 2
    fmt.Println(<-ch)  // 3
}
```

### 3. Channel with results (4 min)

```go
package worker

import (
    "context"
    "fmt"
    "time"
)

type Result struct {
    ID    string
    Value int
    Err   error
}

func ProcessWithResults(ctx context.Context, ids []string) []Result {
    results := make(chan Result, len(ids))

    // spawn workers
    for _, id := range ids {
        go func(id string) {
            // simulate work
            time.Sleep(50 * time.Millisecond)
            results <- Result{ID: id, Value: len(id)}
        }(id)
    }

    // collect results
    var output []Result
    for range ids {
        output = append(output, <-results)
    }

    return output
}
```

### 4. Select for multiple channels (5 min)

```go
func SelectExample(ctx context.Context) {
    ch1 := make(chan string)
    ch2 := make(chan string)

    go func() {
        time.Sleep(100 * time.Millisecond)
        ch1 <- "from ch1"
    }()

    go func() {
        time.Sleep(200 * time.Millisecond)
        ch2 <- "from ch2"
    }()

    // receive from whichever is ready first
    for i := 0; i < 2; i++ {
        select {
        case msg := <-ch1:
            fmt.Println("ch1:", msg)
        case msg := <-ch2:
            fmt.Println("ch2:", msg)
        case <-ctx.Done():
            fmt.Println("cancelled")
            return
        case <-time.After(time.Second):
            fmt.Println("timeout")
            return
        }
    }
}
```

### 5. Closing channels (2 min)

```go
func CloseExample() {
    ch := make(chan int)

    // producer
    go func() {
        for i := 0; i < 5; i++ {
            ch <- i
        }
        close(ch)  // signal no more values
    }()

    // consumer - range exits when channel closed
    for val := range ch {
        fmt.Println(val)
    }

    // check if closed
    val, ok := <-ch
    if !ok {
        fmt.Println("channel closed, got zero value:", val)
    }
}
```

## Channel Direction

Function signatures can restrict channel direction:

```go
// send-only
func producer(out chan<- int) {
    out <- 42
    // <-out  // compile error
}

// receive-only
func consumer(in <-chan int) {
    val := <-in
    // in <- 1  // compile error
}
```

## Common Patterns

### Generator

```go
func generate(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

// usage
for n := range generate(1, 2, 3, 4, 5) {
    fmt.Println(n)
}
```

### Pipeline

```go
func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

// usage
nums := generate(1, 2, 3, 4)
squares := square(nums)
for s := range squares {
    fmt.Println(s)  // 1, 4, 9, 16
}
```

## Channel vs WaitGroup

| Use Case | Tool |
|----------|------|
| Wait for completion only | WaitGroup |
| Send data between goroutines | Channel |
| Coordinate multiple workers | Channel |
| Simple fan-out | WaitGroup |
| Fan-out with results | Channel |

## What Just Happened?

| Java | Go |
|------|-----|
| `BlockingQueue.put()` | `ch <- value` |
| `BlockingQueue.take()` | `<-ch` |
| `poll(timeout)` | `select` with `time.After` |
| Queue capacity | Buffer size |

## Checkpoint

- [ ] Can create and use channels
- [ ] Understand buffered vs unbuffered
- [ ] Can use select for multiple channels
- [ ] Know when to close channels

**Next:** Exercise 14 - Worker Pools
