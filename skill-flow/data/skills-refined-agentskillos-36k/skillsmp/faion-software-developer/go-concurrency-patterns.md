---
id: go-concurrency-patterns
name: "Concurrency Patterns"
domain: GO
skill: faion-software-developer
category: "backend"
---

## Concurrency Patterns

### Problem
Handle concurrent operations safely and efficiently.

### Framework: Worker Pool

```go
package worker

import (
    "context"
    "sync"
)

type Job func(ctx context.Context) error

type Pool struct {
    workers int
    jobs    chan Job
    wg      sync.WaitGroup
}

func NewPool(workers int, buffer int) *Pool {
    return &Pool{
        workers: workers,
        jobs:    make(chan Job, buffer),
    }
}

func (p *Pool) Start(ctx context.Context) {
    for i := 0; i < p.workers; i++ {
        p.wg.Add(1)
        go p.worker(ctx)
    }
}

func (p *Pool) worker(ctx context.Context) {
    defer p.wg.Done()
    for {
        select {
        case <-ctx.Done():
            return
        case job, ok := <-p.jobs:
            if !ok {
                return
            }
            _ = job(ctx) // Handle error as needed
        }
    }
}

func (p *Pool) Submit(job Job) {
    p.jobs <- job
}

func (p *Pool) Stop() {
    close(p.jobs)
    p.wg.Wait()
}
```

### Framework: Fan-Out/Fan-In

```go
func ProcessItems(ctx context.Context, items []Item) []Result {
    numWorkers := runtime.NumCPU()
    jobs := make(chan Item, len(items))
    results := make(chan Result, len(items))

    // Fan-out: start workers
    var wg sync.WaitGroup
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for item := range jobs {
                results <- processItem(ctx, item)
            }
        }()
    }

    // Send jobs
    for _, item := range items {
        jobs <- item
    }
    close(jobs)

    // Wait and close results
    go func() {
        wg.Wait()
        close(results)
    }()

    // Fan-in: collect results
    var output []Result
    for r := range results {
        output = append(output, r)
    }
    return output
}
```

### Agent

faion-backend-agent
