# Exercise 12: Goroutines

**Time:** 15 minutes
**Goal:** Run concurrent operations with goroutines and sync.WaitGroup

## The Spring Boot Version

```java
@Async
public void sendNotification(User user) {
    // runs in thread pool
}

// or with CompletableFuture
List<CompletableFuture<Void>> futures = users.stream()
    .map(user -> CompletableFuture.runAsync(() -> sendNotification(user)))
    .toList();

CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
```

## The Go Way

Goroutines are lightweight threads. Just add `go`:

```go
go sendNotification(user)  // runs concurrently

// wait for multiple
var wg sync.WaitGroup
for _, user := range users {
    wg.Add(1)
    go func(u User) {
        defer wg.Done()
        sendNotification(u)
    }(user)
}
wg.Wait()
```

---

## Step by Step

### 1. Simple goroutine (3 min)

Create `internal/notification/sender.go`:

```go
package notification

import (
    "context"
    "fmt"
    "time"
)

type Sender struct{}

func NewSender() *Sender {
    return &Sender{}
}

func (s *Sender) Send(ctx context.Context, userID, message string) error {
    // simulate slow operation
    time.Sleep(100 * time.Millisecond)
    fmt.Printf("sent notification to %s: %s\n", userID, message)
    return nil
}
```

### 2. Fire-and-forget pattern (3 min)

```go
// fire and forget - no waiting
func (s *Sender) SendAsync(ctx context.Context, userID, message string) {
    go func() {
        if err := s.Send(ctx, userID, message); err != nil {
            // log error but don't propagate
            fmt.Printf("failed to send notification: %v\n", err)
        }
    }()
}
```

### 3. Wait for all with WaitGroup (5 min)

```go
package notification

import (
    "context"
    "sync"
)

func (s *Sender) SendBulk(ctx context.Context, userIDs []string, message string) error {
    var wg sync.WaitGroup

    for _, userID := range userIDs {
        wg.Add(1)
        go func(uid string) {
            defer wg.Done()
            if err := s.Send(ctx, uid, message); err != nil {
                fmt.Printf("failed for %s: %v\n", uid, err)
            }
        }(userID)  // pass userID to avoid closure capture bug
    }

    wg.Wait()  // block until all complete
    return nil
}
```

### 4. Collect errors (4 min)

```go
func (s *Sender) SendBulkWithErrors(ctx context.Context, userIDs []string, message string) []error {
    var (
        wg     sync.WaitGroup
        mu     sync.Mutex
        errors []error
    )

    for _, userID := range userIDs {
        wg.Add(1)
        go func(uid string) {
            defer wg.Done()
            if err := s.Send(ctx, uid, message); err != nil {
                mu.Lock()
                errors = append(errors, fmt.Errorf("user %s: %w", uid, err))
                mu.Unlock()
            }
        }(userID)
    }

    wg.Wait()
    return errors
}
```

### 5. Test it

```go
func main() {
    sender := notification.NewSender()
    ctx := context.Background()

    users := []string{"user1", "user2", "user3", "user4", "user5"}

    // sequential: ~500ms
    start := time.Now()
    for _, u := range users {
        sender.Send(ctx, u, "hello")
    }
    fmt.Printf("sequential: %v\n", time.Since(start))

    // concurrent: ~100ms
    start = time.Now()
    sender.SendBulk(ctx, users, "hello")
    fmt.Printf("concurrent: %v\n", time.Since(start))
}
```

## Common Gotchas

### Loop Variable Capture (Go < 1.22)

```go
// BUG: all goroutines see same userID
for _, userID := range userIDs {
    go func() {
        send(userID)  // userID changes during loop!
    }()
}

// FIX 1: pass as parameter
for _, userID := range userIDs {
    go func(uid string) {
        send(uid)
    }(userID)
}

// FIX 2: shadow variable
for _, userID := range userIDs {
    userID := userID  // shadow
    go func() {
        send(userID)
    }()
}
```

### Forgetting WaitGroup

```go
// BUG: main exits before goroutines complete
func main() {
    for i := 0; i < 5; i++ {
        go doWork(i)
    }
    // program exits immediately!
}

// FIX: wait for completion
func main() {
    var wg sync.WaitGroup
    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func(i int) {
            defer wg.Done()
            doWork(i)
        }(i)
    }
    wg.Wait()
}
```

## Goroutine vs Thread Comparison

| Aspect | Java Thread | Go Goroutine |
|--------|-------------|--------------|
| Stack size | ~1MB | ~2KB (grows) |
| Creation cost | High | Very low |
| Context switch | OS level | Go runtime |
| Typical count | Tens/hundreds | Thousands/millions |

## What Just Happened?

| Java | Go |
|------|-----|
| `new Thread().start()` | `go func()` |
| `ExecutorService` | Just use goroutines |
| `CountDownLatch` | `sync.WaitGroup` |
| `@Async` | `go func()` |

## Checkpoint

- [ ] Can start a goroutine with `go`
- [ ] Can wait for multiple with WaitGroup
- [ ] Understand loop variable capture
- [ ] Can collect errors from concurrent operations

**Next:** Exercise 13 - Channels
