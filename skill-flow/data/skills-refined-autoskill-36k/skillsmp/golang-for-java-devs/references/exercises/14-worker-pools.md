# Exercise 14: Worker Pools

**Time:** 15 minutes
**Goal:** Implement fan-out/fan-in patterns with worker pools

## The Spring Boot Version

```java
ExecutorService executor = Executors.newFixedThreadPool(10);

List<Future<Result>> futures = jobs.stream()
    .map(job -> executor.submit(() -> process(job)))
    .toList();

List<Result> results = futures.stream()
    .map(f -> f.get())
    .toList();

executor.shutdown();
```

## The Go Way

Workers read from a job channel and write to a result channel:

```go
func worker(jobs <-chan Job, results chan<- Result) {
    for job := range jobs {
        results <- process(job)
    }
}
```

---

## Step by Step

### 1. Define job and result types (2 min)

Create `internal/worker/pool.go`:

```go
package worker

import (
    "context"
    "fmt"
    "time"
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
```

### 2. Create a worker function (3 min)

```go
func worker(ctx context.Context, id int, jobs <-chan Job, results chan<- Result) {
    for {
        select {
        case job, ok := <-jobs:
            if !ok {
                return  // channel closed
            }
            // simulate processing
            time.Sleep(50 * time.Millisecond)
            results <- Result{
                JobID: job.ID,
                Value: fmt.Sprintf("worker %d processed: %s", id, job.Data),
            }
        case <-ctx.Done():
            return
        }
    }
}
```

### 3. Create the worker pool (5 min)

```go
type Pool struct {
    numWorkers int
    jobs       chan Job
    results    chan Result
}

func NewPool(numWorkers, jobBuffer int) *Pool {
    return &Pool{
        numWorkers: numWorkers,
        jobs:       make(chan Job, jobBuffer),
        results:    make(chan Result, jobBuffer),
    }
}

func (p *Pool) Start(ctx context.Context) {
    for i := 0; i < p.numWorkers; i++ {
        go worker(ctx, i, p.jobs, p.results)
    }
}

func (p *Pool) Submit(job Job) {
    p.jobs <- job
}

func (p *Pool) Results() <-chan Result {
    return p.results
}

func (p *Pool) Close() {
    close(p.jobs)
}
```

### 4. Process batch of jobs (5 min)

```go
func (p *Pool) ProcessBatch(ctx context.Context, jobs []Job) []Result {
    // start workers
    p.Start(ctx)

    // submit jobs in goroutine
    go func() {
        for _, job := range jobs {
            select {
            case p.jobs <- job:
            case <-ctx.Done():
                return
            }
        }
        close(p.jobs)
    }()

    // collect results
    results := make([]Result, 0, len(jobs))
    for i := 0; i < len(jobs); i++ {
        select {
        case result := <-p.results:
            results = append(results, result)
        case <-ctx.Done():
            return results
        }
    }

    return results
}
```

### Test it

```go
func main() {
    ctx := context.Background()

    // create jobs
    jobs := make([]Job, 20)
    for i := range jobs {
        jobs[i] = Job{ID: i, Data: fmt.Sprintf("job-%d", i)}
    }

    // process with pool
    pool := NewPool(5, 10)  // 5 workers, buffer of 10

    start := time.Now()
    results := pool.ProcessBatch(ctx, jobs)
    fmt.Printf("processed %d jobs in %v\n", len(results), time.Since(start))

    for _, r := range results {
        fmt.Println(r.Value)
    }
}
```

## Using errgroup (Simpler Alternative)

```go
import "golang.org/x/sync/errgroup"

func ProcessWithErrgroup(ctx context.Context, jobs []Job) ([]Result, error) {
    g, ctx := errgroup.WithContext(ctx)
    results := make([]Result, len(jobs))

    // limit concurrency
    g.SetLimit(5)

    for i, job := range jobs {
        i, job := i, job  // capture
        g.Go(func() error {
            time.Sleep(50 * time.Millisecond)
            results[i] = Result{
                JobID: job.ID,
                Value: "processed: " + job.Data,
            }
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, err
    }

    return results, nil
}
```

## Semaphore for Rate Limiting

```go
import "golang.org/x/sync/semaphore"

func ProcessWithSemaphore(ctx context.Context, jobs []Job) []Result {
    sem := semaphore.NewWeighted(5)  // max 5 concurrent
    var mu sync.Mutex
    var results []Result

    var wg sync.WaitGroup
    for _, job := range jobs {
        wg.Add(1)
        go func(j Job) {
            defer wg.Done()

            // acquire semaphore
            if err := sem.Acquire(ctx, 1); err != nil {
                return
            }
            defer sem.Release(1)

            // process
            result := process(j)

            mu.Lock()
            results = append(results, result)
            mu.Unlock()
        }(job)
    }

    wg.Wait()
    return results
}
```

## When to Use What

| Pattern | Use Case |
|---------|----------|
| WaitGroup | Simple fan-out, no results |
| Channel pool | Stream processing, backpressure |
| errgroup | Error handling, limited concurrency |
| Semaphore | Rate limiting existing code |

## What Just Happened?

| Java | Go |
|------|-----|
| ExecutorService | Worker pool with channels |
| Future.get() | Receive from results channel |
| executor.shutdown() | close(jobs) |
| awaitTermination() | WaitGroup or drain results |

## Checkpoint

- [ ] Workers read from jobs channel
- [ ] Results sent to results channel
- [ ] Pool processes batch of jobs
- [ ] Context used for cancellation

**Next:** Exercise 15 - Context and Cancellation
