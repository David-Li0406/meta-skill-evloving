---
title: Static Analysis
impact: HIGH
impactDescription: Discover potential bugs
tags: lint, govet, analysis
---

## Static Analysis

Use go vet for static analysis.

**Basic Usage:**

```bash
go vet ./...
```

**Common Checks:**

```go
// 1. Printf format errors
fmt.Printf("%d", "string") // go vet: type mismatch

// 2. Unused results
strings.ToLower(s) // go vet: result not used

// 3. Unreachable code
func example() int {
    return 1
    fmt.Println("unreachable") // go vet: unreachable
}

// 4. Incorrect lock usage
mu.Lock()
// Forgot to Unlock

// 5. Loop variable capture
for _, v := range values {
    go func() {
        fmt.Println(v) // go vet: loop variable capture
    }()
}

// 6. Incorrect struct tags
type User struct {
    Name string `json:name` // go vet: malformed, should be json:"name"
}

// 7. Copying sync types
var mu sync.Mutex
mu2 := mu // go vet: copied lock

// 8. Incorrect atomic operations
var n int64
n = atomic.AddInt64(&n, 1) // go vet: assignment to n
```

**Shadow Checking:**

```bash
go install golang.org/x/tools/go/analysis/passes/shadow/cmd/shadow@latest

# Check variable shadowing
shadow ./...
```

```go
func example() {
    err := doSomething()
    if err != nil {
        err := handleError() // shadow: err is shadowed
        log.Println(err)
    }
    return err // Returns outer err
}
```

**CI Integration:**

```yaml
- name: Static Analysis
  run: |
    go vet ./...
    shadow ./...
```
