---
title: Custom Error Types
impact: MEDIUM
impactDescription: Carry additional information
tags: error, custom, type
---

## Custom Error Types

Define custom error types when you need to carry additional information.

**Good Example:**

```go
// pkg/errors/errors.go
package errors

import "fmt"

// ValidationError contains field-level validation errors
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error: %s - %s", e.Field, e.Message)
}

// NotFoundError contains resource type and ID
type NotFoundError struct {
    Resource string
    ID       interface{}
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s with id %v not found", e.Resource, e.ID)
}

// BusinessError is a business error with error code
type BusinessError struct {
    Code    int
    Message string
    Details map[string]interface{}
}

func (e *BusinessError) Error() string {
    return fmt.Sprintf("[%d] %s", e.Code, e.Message)
}

func NewBusinessError(code int, message string) *BusinessError {
    return &BusinessError{Code: code, Message: message}
}
```

**Using errors.As to extract:**

```go
func Handler(c *gin.Context) {
    err := service.CreateUser(ctx, req)
    if err != nil {
        var validErr *errors.ValidationError
        if errors.As(err, &validErr) {
            c.JSON(http.StatusBadRequest, gin.H{
                "error": validErr.Message,
                "field": validErr.Field,
            })
            return
        }

        var bizErr *errors.BusinessError
        if errors.As(err, &bizErr) {
            c.JSON(http.StatusUnprocessableEntity, gin.H{
                "code":    bizErr.Code,
                "message": bizErr.Message,
            })
            return
        }

        c.JSON(http.StatusInternalServerError, gin.H{"error": "internal error"})
    }
}
```
