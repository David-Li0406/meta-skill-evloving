---
title: Zero Value Utilization
impact: MEDIUM
impactDescription: Simplified initialization
tags: idiomatic, zero-value, default
---

## Zero Value Utilization

Use Go's zero value feature to simplify code.

**Zero Values Ready to Use:**

```go
// sync.Mutex zero value is usable
var mu sync.Mutex
mu.Lock()
mu.Unlock()

// bytes.Buffer zero value is usable
var buf bytes.Buffer
buf.WriteString("hello")

// sync.WaitGroup zero value is usable
var wg sync.WaitGroup
wg.Add(1)

// sync.Once zero value is usable
var once sync.Once
once.Do(func() {})
```

**Design APIs with Meaningful Zero Values:**

```go
// Good design: Zero value is meaningful
type Config struct {
    Timeout time.Duration // Zero value 0 can mean "use default"
    Retries int           // Zero value 0 can mean "no retries"
}

func NewClient(cfg Config) *Client {
    if cfg.Timeout == 0 {
        cfg.Timeout = 30 * time.Second
    }
    return &Client{cfg: cfg}
}

// Callers can omit fields
client := NewClient(Config{}) // Use all defaults
```

**Boolean Zero Value:**

```go
// Zero value false should be a reasonable default
type Options struct {
    DisableCache bool  // false = caching enabled (default)
    SkipValidate bool  // false = validation enabled (default)
}

// Avoid double negatives
// Wrong: DisableDisableCache bool
// Correct: EnableCache bool (if default is no caching)
```

**Pointer Zero Value:**

```go
// nil pointer means "not set"
type User struct {
    Name     string
    Nickname *string // nil = nickname not set
}

// Check if set
if user.Nickname != nil {
    fmt.Println(*user.Nickname)
}
```
