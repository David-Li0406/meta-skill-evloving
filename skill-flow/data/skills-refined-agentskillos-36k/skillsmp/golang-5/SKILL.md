---
name: golang
description: "Go development process and idiomatic code review. Use when writing Go code, reviewing Go PRs, implementing concurrency with goroutines/channels, debugging Go race conditions, or fixing Go error handling. Also use for Go project setup, module management, interface design, context usage, and when errors are being ignored, goroutines lack coordination, or code feels 'clever' instead of clear. Essential for Go API design and fighting borrow-checker-like constraints."
---

# Go Skill

## Overview

Go's simplicity is intentional. This skill guides writing idiomatic Go that embraces the language's philosophy: clear is better than clever.

**Core principle:** Don't fight the language. Go's constraints (explicit error handling, no generics abuse, simple concurrency) lead to better code.

## The Go Development Process

### Phase 1: Design Idiomatically

**Before writing implementation:**

1. **Think in Interfaces**
   - What behavior does this need?
   - Keep interfaces small (1-3 methods)
   - Accept interfaces, return structs

2. **Plan Error Handling**
   - What can fail?
   - How should errors propagate?
   - What context should errors include?

3. **Consider Concurrency**
   - Is concurrency needed?
   - Who owns the goroutine lifecycle?
   - How will it be cancelled?

### Phase 2: Implement Simply

**Write Go, not Java-in-Go:**

1. **Handle Errors Immediately**
   ```go
   // ✅ Handle and wrap errors
   result, err := doSomething()
   if err != nil {
       return fmt.Errorf("doSomething failed: %w", err)
   }

   // ❌ Never ignore errors
   result, _ := doSomething()
   ```

2. **Use Context for Cancellation**
   ```go
   func doWork(ctx context.Context) error {
       select {
       case <-ctx.Done():
           return ctx.Err()
       case result := <-processAsync():
           return handleResult(result)
       }
   }
   ```

3. **Keep Functions Short**
   - If it needs comments to explain, break it up
   - Early returns reduce nesting
   - One level of abstraction per function

### Phase 3: Review for Idioms

**Before approving:**

1. **Check Error Handling**
   - All errors checked?
   - Errors wrapped with context?
   - No panic for normal errors?

2. **Check Concurrency**
   - Goroutines have clear ownership?
   - Channels closed by sender?
   - Context used for cancellation?

3. **Check Interfaces**
   - Interfaces are small?
   - Interfaces defined where used, not implemented?

## Red Flags - STOP and Fix

### Error Handling Red Flags

```go
// Ignored error
result, _ := something()

// Panic for recoverable errors
if err != nil {
    panic(err)
}

// Error without context
return err  // Which operation failed?

// Checking error string content
if err.Error() == "not found" {
```

### Concurrency Red Flags

```go
// Goroutine without lifecycle management
go doSomething()  // Who waits? Who cancels?

// Shared state without synchronization
counter++  // In a goroutine

// Channel without close
for v := range ch {  // Will block forever if not closed

// Sleep instead of proper synchronization
time.Sleep(time.Second)  // Race condition waiting to happen
```

### Design Red Flags

```
- Interface with > 5 methods (too big)
- Package with > 10 files (break it up)
- Function > 50 lines (simplify)
- Nested if > 3 levels (use early returns)
- init() functions (explicit initialization preferred)
- Global variables (dependency injection instead)
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "The error can't happen" | It will. Handle it. |
| "I'll add error handling later" | Later never comes. Handle now. |
| "Channels are complicated" | Use sync primitives if simpler. |
| "I need a big interface" | Break it into smaller ones. |
| "Go is too verbose" | Explicit is better. Embrace it. |
| "I need generics for this" | Do you? Concrete types often clearer. |

## Go Quality Checklist

Before approving Go code:

- [ ] **Errors handled**: All errors checked and wrapped
- [ ] **No panics**: Only for unrecoverable errors
- [ ] **Context used**: Cancellation and timeouts proper
- [ ] **Goroutines managed**: Clear ownership and lifecycle
- [ ] **Interfaces small**: 1-3 methods each
- [ ] **Tests table-driven**: Comprehensive test cases
- [ ] **Linter clean**: golangci-lint passes

## Quick Go Patterns

### Error Wrapping

```go
// ✅ Wrap with context
if err != nil {
    return fmt.Errorf("failed to fetch user %s: %w", userID, err)
}

// Check wrapped errors
if errors.Is(err, ErrNotFound) {
    // Handle not found
}

var pathErr *os.PathError
if errors.As(err, &pathErr) {
    // Handle path error specifically
}
```

### Small Interfaces

```go
// ✅ Interface where it's used
type UserGetter interface {
    GetUser(ctx context.Context, id string) (*User, error)
}

func NewHandler(users UserGetter) *Handler {
    return &Handler{users: users}
}

// ❌ Big interface at implementation
type UserService interface {
    GetUser(...)
    CreateUser(...)
    UpdateUser(...)
    DeleteUser(...)
    ListUsers(...)
    // ... 10 more methods
}
```

### Goroutine Lifecycle

```go
// ✅ Clear ownership with WaitGroup
func processItems(ctx context.Context, items []Item) error {
    var wg sync.WaitGroup
    errCh := make(chan error, len(items))

    for _, item := range items {
        wg.Add(1)
        go func(item Item) {
            defer wg.Done()
            if err := process(ctx, item); err != nil {
                errCh <- err
            }
        }(item)
    }

    wg.Wait()
    close(errCh)

    // Collect errors
    for err := range errCh {
        return err  // Return first error
    }
    return nil
}
```

## Quick Commands

```bash
# Format
go fmt ./...

# Vet
go vet ./...

# Full lint
golangci-lint run

# Test with race detector
go test -race -cover ./...

# Security scan
govulncheck ./...
```

## References

Detailed patterns and examples in `references/`:
- `effective-go.md` - Idiomatic Go patterns
- `concurrency-patterns.md` - Goroutines, channels, sync
- `error-handling.md` - Error wrapping and handling
