---
title: Error Wrapping and Context
impact: HIGH
impactDescription: Error traceability
tags: error, wrap, context
---

## Error Wrapping and Context

Use `fmt.Errorf` and `%w` to wrap errors, preserving the complete call chain.

**Bad Example (losing context):**

```go
func GetUser(id int) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, err // Lost GetUser context
    }
    return user, nil
}
```

**Good Example (wrapping error):**

```go
func GetUser(id int) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, fmt.Errorf("get user %d: %w", id, err)
    }
    return user, nil
}

// Caller can check the root cause
func Handler(c *gin.Context) {
    user, err := GetUser(id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            c.JSON(404, gin.H{"error": "user not found"})
            return
        }
        c.JSON(500, gin.H{"error": "internal error"})
        log.Printf("failed to get user: %v", err)
        // Log output: failed to get user: get user 123: sql: no rows
        return
    }
}
```

**Key Points:**
- Use `%w` verb to wrap errors
- Include operation name and key parameters
- Use `errors.Is()` to check error types
- Use `errors.As()` to extract error types
