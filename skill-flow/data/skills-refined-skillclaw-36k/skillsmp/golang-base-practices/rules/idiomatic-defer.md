---
title: defer Usage Guidelines
impact: MEDIUM
impactDescription: Resource cleanup
tags: idiomatic, defer, cleanup
---

## defer Usage Guidelines

Use defer to ensure proper resource cleanup.

**Resource Cleanup:**

```go
func ReadFile(path string) ([]byte, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer f.Close() // Ensure file is closed

    return io.ReadAll(f)
}
```

**Lock Release:**

```go
func (c *Cache) Get(key string) interface{} {
    c.mu.Lock()
    defer c.mu.Unlock() // Ensure unlock
    return c.data[key]
}
```

**defer Execution Order (LIFO):**

```go
func example() {
    defer fmt.Println("first")
    defer fmt.Println("second")
    defer fmt.Println("third")
}
// Output: third, second, first
```

**Recover Panic in defer:**

```go
func SafeCall(fn func()) (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("panic: %v", r)
        }
    }()
    fn()
    return nil
}
```

**Important Notes:**

```go
// defer arguments are evaluated at defer time
func example() {
    i := 0
    defer fmt.Println(i) // Outputs 0
    i++
}

// Use closure to capture latest value
func example() {
    i := 0
    defer func() { fmt.Println(i) }() // Outputs 1
    i++
}
```

**defer in Loops:**

```go
// Wrong: defer accumulation
func processFiles(paths []string) error {
    for _, path := range paths {
        f, _ := os.Open(path)
        defer f.Close() // All defers execute at function end
    }
}

// Correct: Extract to function
func processFiles(paths []string) error {
    for _, path := range paths {
        if err := processFile(path); err != nil {
            return err
        }
    }
    return nil
}

func processFile(path string) error {
    f, err := os.Open(path)
    if err != nil {
        return err
    }
    defer f.Close()
    // ...
}
```
