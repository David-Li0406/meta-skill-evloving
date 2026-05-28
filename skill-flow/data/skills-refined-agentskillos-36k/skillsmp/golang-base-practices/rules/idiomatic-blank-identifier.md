---
title: Blank Identifier Usage
impact: MEDIUM
impactDescription: Explicitly ignore values
tags: idiomatic, blank-identifier, underscore
---

## Blank Identifier Usage

Use the blank identifier `_` correctly.

**Ignore Unneeded Return Values:**

```go
// Only need the error
_, err := io.Copy(dst, src)

// Only need the first return value
value, _ := cache.Load(key)  // Caution: may hide errors

// Ignore key or value in range
for _, v := range slice {}
for i := range slice {}  // Can omit value when only index is needed
```

**Import for Side Effects Only:**

```go
import (
    "database/sql"
    _ "github.com/go-sql-driver/mysql" // Register MySQL driver
)

import _ "net/http/pprof" // Register pprof handlers
```

**Compile-Time Type Check:**

```go
// Verify type implements interface
var _ io.Reader = (*MyReader)(nil)
var _ fmt.Stringer = MyType{}

// Verify struct satisfies interface
type Handler struct{}
var _ http.Handler = (*Handler)(nil)
```

**Temporary Handling of Unused Variables:**

```go
// Temporarily handle unused variable during development
func example() {
    x := computeX()
    _ = x // TODO: use later

    // Better approach: delete or use directly
}
```

**Notes on Error Handling:**

```go
// Wrong: Ignoring errors is dangerous
data, _ := json.Marshal(obj)  // What if it fails?

// If you must ignore, add comment explaining why
_ = conn.Close() // ignore close error, already logged

// Better approach: Log but don't return
if err := conn.Close(); err != nil {
    log.Printf("warning: close failed: %v", err)
}
```

**Unused Parameters in Method Implementations:**

```go
// Parameter required by interface but not needed by method
func (h *Handler) ServeHTTP(w http.ResponseWriter, _ *http.Request) {
    w.Write([]byte("Hello"))
}
```
