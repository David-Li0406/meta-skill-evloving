---
title: Goroutine Lifecycle Management
impact: CRITICAL
impactDescription: Prevent resource leaks
tags: concurrency, goroutine, lifecycle
---

## Goroutine Lifecycle Management

Ensure every goroutine has a clear exit condition.

**Bad Example (goroutine leak):**

```go
func StartWorker() {
    go func() {
        for {
            processTask() // Never exits
        }
    }()
}
```

**Good Example (controlled exit):**

```go
type Worker struct {
    tasks chan Task
    done  chan struct{}
    wg    sync.WaitGroup
}

func NewWorker() *Worker {
    return &Worker{
        tasks: make(chan Task, 100),
        done:  make(chan struct{}),
    }
}

func (w *Worker) Start(ctx context.Context) {
    w.wg.Add(1)
    go func() {
        defer w.wg.Done()
        for {
            select {
            case <-ctx.Done():
                return
            case <-w.done:
                return
            case task := <-w.tasks:
                w.processTask(task)
            }
        }
    }()
}

func (w *Worker) Stop() {
    close(w.done)
    w.wg.Wait()
}

func (w *Worker) Submit(task Task) {
    select {
    case w.tasks <- task:
    default:
        log.Println("task queue full, dropping task")
    }
}
```

**Key Principles:**
- Use `context.Context` to propagate cancellation signals
- Use `sync.WaitGroup` to wait for goroutines to finish
- Provide explicit shutdown mechanisms
