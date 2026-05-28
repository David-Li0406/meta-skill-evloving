---
title: Race Detection
impact: CRITICAL
impactDescription: Discover concurrency bugs
tags: concurrency, race, detection
---

## Race Detection

Use the race detector to discover concurrency issues.

**Enable Race Detection:**

```bash
# Enable during testing
go test -race ./...

# Enable during runtime
go run -race main.go

# Enable during build
go build -race -o myapp
```

**Common Race Conditions:**

```go
// Bad Example 1: Unprotected shared variable
var counter int

func increment() {
    counter++ // DATA RACE
}

go increment()
go increment()
```

```go
// Bad Example 2: Loop variable capture
for _, item := range items {
    go func() {
        process(item) // DATA RACE: item is shared by all goroutines
    }()
}

// Good Example
for _, item := range items {
    item := item // Create local copy
    go func() {
        process(item)
    }()
}
```

```go
// Bad Example 3: Concurrent map writes
m := make(map[string]int)

go func() { m["a"] = 1 }() // DATA RACE
go func() { m["b"] = 2 }()

// Good Example: Use sync.Map or mutex
```

**CI Integration:**

```yaml
# .github/workflows/test.yml
- name: Test with race detector
  run: go test -race -v ./...
```

**Notes:**
- Race detector has performance overhead (2-20x)
- Do not enable in production
- CI must include race detection
