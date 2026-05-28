---
title: Always Check Error Returns
impact: CRITICAL
impactDescription: Avoid hidden bugs
tags: error, check, handling
---

## Always Check Error Returns

Go requires explicit error handling. Never ignore error return values.

**Bad Example (ignoring errors):**

```go
func ProcessData() {
    data, _ := fetchData()        // Ignoring error!
    json.Unmarshal(data, &result) // Ignoring error!
    saveResult(result)            // This will break if data is empty
}
```

**Good Example (explicit handling):**

```go
func ProcessData() error {
    data, err := fetchData()
    if err != nil {
        return fmt.Errorf("fetch data: %w", err)
    }

    var result Result
    if err := json.Unmarshal(data, &result); err != nil {
        return fmt.Errorf("unmarshal data: %w", err)
    }

    if err := saveResult(result); err != nil {
        return fmt.Errorf("save result: %w", err)
    }

    return nil
}
```

**Special Cases (explicit ignore):**

```go
// When error is truly not needed, use blank identifier with comment
_ = conn.Close() // ignore close error, already logging

// Or log but don't return
if err := conn.Close(); err != nil {
    log.Printf("warning: failed to close connection: %v", err)
}
```

**Lint Check:**

```bash
# Use errcheck to detect unhandled errors
go install github.com/kisielk/errcheck@latest
errcheck ./...
```
