---
title: errgroup Concurrency Control
impact: HIGH
impactDescription: Elegant concurrent error handling
tags: concurrency, errgroup, parallel
---

## errgroup Concurrency Control

Use errgroup to simplify error handling for concurrent tasks.

**Installation:**

```bash
go get golang.org/x/sync/errgroup
```

**Good Example:**

```go
import "golang.org/x/sync/errgroup"

func FetchAllData(ctx context.Context, ids []int) (*AllData, error) {
    g, ctx := errgroup.WithContext(ctx)

    var (
        users    []User
        orders   []Order
        products []Product
        mu       sync.Mutex
    )

    // Fetch users concurrently
    for _, id := range ids {
        id := id // Important: capture loop variable
        g.Go(func() error {
            user, err := fetchUser(ctx, id)
            if err != nil {
                return fmt.Errorf("fetch user %d: %w", id, err)
            }
            mu.Lock()
            users = append(users, user)
            mu.Unlock()
            return nil
        })
    }

    // Fetch orders concurrently
    g.Go(func() error {
        var err error
        orders, err = fetchOrders(ctx)
        return err
    })

    // Fetch products concurrently
    g.Go(func() error {
        var err error
        products, err = fetchProducts(ctx)
        return err
    })

    // Wait for all tasks to complete; if any fails, cancel others
    if err := g.Wait(); err != nil {
        return nil, err
    }

    return &AllData{Users: users, Orders: orders, Products: products}, nil
}
```

**Limiting Concurrency:**

```go
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(10) // Maximum 10 concurrent goroutines

for _, url := range urls {
    url := url
    g.Go(func() error {
        return fetch(ctx, url)
    })
}
```
