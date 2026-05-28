# Concurrency Bridge: Java to Go

You know threads, ExecutorService, and CompletableFuture. Go's concurrency will feel lighter. Here's how to map your mental model.

## The Core Difference

**Java philosophy:** Threads are expensive. Manage them carefully with pools.
```java
ExecutorService executor = Executors.newFixedThreadPool(10);
executor.submit(() -> process(item));
```

**Go philosophy:** Goroutines are cheap. Spin them up freely.
```go
for _, item := range items {
    go process(item)  // thousands? no problem
}
```

A goroutine starts with ~2KB stack (grows as needed). A Java thread starts with ~1MB.

## Quick Reference

| Java | Go |
|------|-----|
| `Thread.start()` / `executor.submit()` | `go func()` |
| `ExecutorService` | Goroutines (no pool needed) |
| `BlockingQueue` | Channels |
| `CompletableFuture` | Channels + select |
| `Future.get()` | `<-channel` |
| `synchronized` / `Lock` | `sync.Mutex` |
| `AtomicInteger` | `sync/atomic` package |
| `CountDownLatch` | `sync.WaitGroup` |
| `@Async` | `go func() { ... }()` |
| Virtual threads (Java 21) | Goroutines (same idea) |

## Pattern 1: Fire and Forget

**Java:**
```java
// with @Async
@Service
public class EmailService {
    @Async
    public void sendEmail(User user) {
        // runs in thread pool
    }
}

// or manually
executor.submit(() -> sendEmail(user));
```

**Go:**
```go
go sendEmail(user)  // that's it

// if you need to handle errors
go func() {
    if err := sendEmail(user); err != nil {
        log.Printf("email failed: %v", err)
    }
}()
```

## Pattern 2: Wait for Completion

**Java:**
```java
ExecutorService executor = Executors.newFixedThreadPool(10);
List<Future<Result>> futures = new ArrayList<>();

for (Item item : items) {
    futures.add(executor.submit(() -> process(item)));
}

// wait for all
for (Future<Result> f : futures) {
    Result r = f.get();  // blocks until complete
}
```

**Go (WaitGroup):**
```go
var wg sync.WaitGroup

for _, item := range items {
    wg.Add(1)
    go func(item Item) {
        defer wg.Done()
        process(item)
    }(item)
}

wg.Wait()  // blocks until all done
```

## Pattern 3: Collect Results

**Java:**
```java
List<CompletableFuture<Result>> futures = items.stream()
    .map(item -> CompletableFuture.supplyAsync(() -> process(item)))
    .toList();

List<Result> results = futures.stream()
    .map(CompletableFuture::join)
    .toList();
```

**Go (Channels):**
```go
results := make(chan Result, len(items))

for _, item := range items {
    go func(item Item) {
        results <- process(item)
    }(item)
}

// collect results
var output []Result
for range items {
    output = append(output, <-results)
}
```

**Go (errgroup for errors):**
```go
import "golang.org/x/sync/errgroup"

g, ctx := errgroup.WithContext(context.Background())
results := make([]Result, len(items))

for i, item := range items {
    i, item := i, item  // capture for closure
    g.Go(func() error {
        r, err := process(ctx, item)
        if err != nil {
            return err
        }
        results[i] = r
        return nil
    })
}

if err := g.Wait(); err != nil {
    return nil, err
}
return results, nil
```

## Pattern 4: Worker Pool

**Java:**
```java
BlockingQueue<Job> queue = new LinkedBlockingQueue<>();
ExecutorService executor = Executors.newFixedThreadPool(workers);

// start workers
for (int i = 0; i < workers; i++) {
    executor.submit(() -> {
        while (true) {
            Job job = queue.take();  // blocks until available
            process(job);
        }
    });
}

// submit jobs
for (Job job : jobs) {
    queue.put(job);
}
```

**Go:**
```go
func worker(jobs <-chan Job, results chan<- Result) {
    for job := range jobs {  // exits when jobs is closed
        results <- process(job)
    }
}

func main() {
    jobs := make(chan Job, 100)
    results := make(chan Result, 100)

    // start workers
    for w := 0; w < numWorkers; w++ {
        go worker(jobs, results)
    }

    // submit jobs
    go func() {
        for _, job := range allJobs {
            jobs <- job
        }
        close(jobs)  // signal no more jobs
    }()

    // collect results
    for range allJobs {
        <-results
    }
}
```

## Pattern 5: Timeout

**Java:**
```java
CompletableFuture<Result> future = CompletableFuture.supplyAsync(() -> doWork());

try {
    Result result = future.get(5, TimeUnit.SECONDS);
} catch (TimeoutException e) {
    future.cancel(true);
    // handle timeout
}
```

**Go (Context):**
```go
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

resultCh := make(chan Result, 1)
go func() {
    resultCh <- doWork(ctx)
}()

select {
case result := <-resultCh:
    // success
case <-ctx.Done():
    // timeout
}
```

**Go (simpler with select):**
```go
select {
case result := <-resultCh:
    // success
case <-time.After(5 * time.Second):
    // timeout
}
```

## Pattern 6: First One Wins

**Java:**
```java
CompletableFuture<Result> first = CompletableFuture.anyOf(
    CompletableFuture.supplyAsync(() -> callServiceA()),
    CompletableFuture.supplyAsync(() -> callServiceB())
).thenApply(obj -> (Result) obj);
```

**Go:**
```go
resultCh := make(chan Result, 2)  // buffer for both

go func() { resultCh <- callServiceA() }()
go func() { resultCh <- callServiceB() }()

first := <-resultCh  // get whichever finishes first
```

## Pattern 7: Fan-Out, Fan-In

**Java:**
```java
// fan-out
List<CompletableFuture<List<Result>>> futures = sources.stream()
    .map(source -> CompletableFuture.supplyAsync(() -> fetch(source)))
    .toList();

// fan-in
List<Result> allResults = futures.stream()
    .map(CompletableFuture::join)
    .flatMap(List::stream)
    .toList();
```

**Go:**
```go
// fan-out: multiple goroutines reading from one channel
func fanOut(input <-chan Job, workers int) []<-chan Result {
    outputs := make([]<-chan Result, workers)
    for i := 0; i < workers; i++ {
        outputs[i] = worker(input)
    }
    return outputs
}

// fan-in: merge multiple channels into one
func fanIn(channels ...<-chan Result) <-chan Result {
    var wg sync.WaitGroup
    merged := make(chan Result)

    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan Result) {
            defer wg.Done()
            for v := range c {
                merged <- v
            }
        }(ch)
    }

    go func() {
        wg.Wait()
        close(merged)
    }()

    return merged
}
```

## Pattern 8: Mutex for Shared State

**Java:**
```java
public class Counter {
    private final Lock lock = new ReentrantLock();
    private int count;

    public void increment() {
        lock.lock();
        try {
            count++;
        } finally {
            lock.unlock();
        }
    }
}
```

**Go:**
```go
type Counter struct {
    mu    sync.Mutex
    count int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

// or use atomic for simple operations
type AtomicCounter struct {
    count atomic.Int64
}

func (c *AtomicCounter) Increment() {
    c.count.Add(1)
}
```

## Channel Directionality

Go channels can be directional - this is a compile-time safety feature:

```go
// send-only channel
func producer(out chan<- int) {
    out <- 1
    // <-out  // compile error: cannot receive
}

// receive-only channel
func consumer(in <-chan int) {
    val := <-in
    // in <- 1  // compile error: cannot send
}

// bidirectional
func both(ch chan int) {
    ch <- 1
    <-ch
}
```

## Buffered vs Unbuffered Channels

```go
// unbuffered: send blocks until receive
ch := make(chan int)

// buffered: send blocks only when buffer full
ch := make(chan int, 10)
```

**Rule of thumb:**
- Unbuffered for synchronization (handoff)
- Buffered for decoupling/batching

## Context for Cancellation

Context is Go's replacement for `InterruptedException` and thread interruption:

```go
func work(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()  // Canceled or DeadlineExceeded
        default:
            // do work
        }
    }
}

// caller controls cancellation
ctx, cancel := context.WithCancel(context.Background())
go work(ctx)
// ...
cancel()  // signals work to stop
```

## Mental Model Shift

**In Java:** Think about thread pools, synchronization, and careful resource management.

**In Go:** Think about goroutines as cheap, channels as communication pipes, and context for lifecycle management.

Go's mantra: "Don't communicate by sharing memory; share memory by communicating."

If you find yourself reaching for mutexes everywhere, consider if channels would be cleaner.
