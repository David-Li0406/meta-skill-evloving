---
title: Context Cancellation Propagation
impact: CRITICAL
impactDescription: Request lifecycle management
tags: concurrency, context, cancel
---

## Context Cancellation Propagation

Use context to propagate cancellation signals and deadlines.

**Good Example:**

```go
func HandleRequest(w http.ResponseWriter, r *http.Request) {
    // Request context automatically propagates cancellation
    ctx := r.Context()

    // Add timeout
    ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()

    result, err := processWithContext(ctx)
    if err != nil {
        if errors.Is(err, context.DeadlineExceeded) {
            http.Error(w, "request timeout", http.StatusGatewayTimeout)
            return
        }
        if errors.Is(err, context.Canceled) {
            // Client cancelled the request
            return
        }
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    json.NewEncoder(w).Encode(result)
}

func processWithContext(ctx context.Context) (*Result, error) {
    // Check context
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    default:
    }

    // Pass context to downstream
    data, err := fetchData(ctx)
    if err != nil {
        return nil, err
    }

    return &Result{Data: data}, nil
}

func fetchData(ctx context.Context) ([]byte, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    return io.ReadAll(resp.Body)
}
```

**Context Chain:**

```go
// Base context
ctx := context.Background()

// Add timeout
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()

// Add value
ctx = context.WithValue(ctx, userIDKey, userID)

// Pass to all downstream calls
result := doSomething(ctx)
```
