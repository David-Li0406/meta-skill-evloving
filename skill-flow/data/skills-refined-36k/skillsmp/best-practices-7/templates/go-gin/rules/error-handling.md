---
title: Error Handling
impact: CRITICAL
impactDescription: Prevents silent failures and improves debugging
tags: errors, debugging, production
---

# Error Handling

Go's explicit error handling is a feature, not a burden. Use it properly.

## Rule 1: Never Ignore Errors

```go
// ❌ INCORRECT - silent failure
json.Unmarshal(data, &result)

// ✅ CORRECT - handle the error
if err := json.Unmarshal(data, &result); err != nil {
    return fmt.Errorf("unmarshal result: %w", err)
}
```

## Rule 2: Wrap Errors with Context

```go
// ❌ INCORRECT - no context, hard to trace
func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, err  // where did this come from?
    }
    return user, nil
}

// ✅ CORRECT - wrapped with context
func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, fmt.Errorf("find user %s: %w", id, err)
    }
    return user, nil
}
```

## Rule 3: Use Sentinel Errors for Known Conditions

```go
var (
    ErrNotFound = errors.New("not found")
    ErrConflict = errors.New("conflict")
)

func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if errors.Is(err, sql.ErrNoRows) {
        return nil, ErrNotFound
    }
    if err != nil {
        return nil, fmt.Errorf("find user: %w", err)
    }
    return user, nil
}

// Caller can check:
if errors.Is(err, ErrNotFound) {
    c.JSON(404, gin.H{"error": "user not found"})
    return
}
```

## Rule 4: Custom Error Types for Rich Context

```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on %s: %s", e.Field, e.Message)
}

// Usage
if len(email) == 0 {
    return &ValidationError{Field: "email", Message: "required"}
}

// Caller can type assert
var validErr *ValidationError
if errors.As(err, &validErr) {
    c.JSON(400, gin.H{
        "error": validErr.Message,
        "field": validErr.Field,
    })
}
```

## Rule 5: Gin Error Middleware

```go
func ErrorMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        if len(c.Errors) > 0 {
            err := c.Errors.Last().Err

            switch {
            case errors.Is(err, ErrNotFound):
                c.JSON(404, gin.H{"error": "resource not found"})
            case errors.Is(err, ErrUnauthorized):
                c.JSON(401, gin.H{"error": "unauthorized"})
            default:
                log.Printf("internal error: %v", err)
                c.JSON(500, gin.H{"error": "internal server error"})
            }
        }
    }
}

// In handlers:
func GetUser(c *gin.Context) {
    user, err := userService.Get(c.Param("id"))
    if err != nil {
        c.Error(err)  // collected by middleware
        return
    }
    c.JSON(200, user)
}
```

## Rule 6: Panic Recovery

```go
// Only panic for truly unrecoverable situations
// Use Gin's built-in recovery middleware
r := gin.Default()  // includes recovery

// Or custom recovery:
r.Use(gin.CustomRecovery(func(c *gin.Context, recovered interface{}) {
    log.Printf("panic recovered: %v\n%s", recovered, debug.Stack())
    c.JSON(500, gin.H{"error": "internal server error"})
}))
```
