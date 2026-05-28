---
id: go-error-handling
name: "Error Handling"
domain: GO
skill: faion-software-developer
category: "backend"
---

## Error Handling

### Problem
Consistent error handling with proper context.

### Framework: Custom Errors

```go
package apperror

import (
    "fmt"
    "net/http"
)

type AppError struct {
    Code       string `json:"code"`
    Message    string `json:"message"`
    HTTPStatus int    `json:"-"`
    Err        error  `json:"-"`
}

func (e *AppError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("%s: %v", e.Message, e.Err)
    }
    return e.Message
}

func (e *AppError) Unwrap() error {
    return e.Err
}

// Common errors
var (
    ErrNotFound = &AppError{
        Code:       "NOT_FOUND",
        Message:    "Resource not found",
        HTTPStatus: http.StatusNotFound,
    }
    ErrUnauthorized = &AppError{
        Code:       "UNAUTHORIZED",
        Message:    "Authentication required",
        HTTPStatus: http.StatusUnauthorized,
    }
    ErrValidation = &AppError{
        Code:       "VALIDATION_ERROR",
        Message:    "Invalid input",
        HTTPStatus: http.StatusBadRequest,
    }
)

func NewNotFound(resource string) *AppError {
    return &AppError{
        Code:       "NOT_FOUND",
        Message:    fmt.Sprintf("%s not found", resource),
        HTTPStatus: http.StatusNotFound,
    }
}

func Wrap(err error, message string) *AppError {
    return &AppError{
        Code:       "INTERNAL_ERROR",
        Message:    message,
        HTTPStatus: http.StatusInternalServerError,
        Err:        err,
    }
}
```

### Middleware Error Handler

```go
func ErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        if len(c.Errors) > 0 {
            err := c.Errors.Last().Err
            if appErr, ok := err.(*apperror.AppError); ok {
                c.JSON(appErr.HTTPStatus, gin.H{
                    "error": gin.H{
                        "code":    appErr.Code,
                        "message": appErr.Message,
                    },
                })
                return
            }
            c.JSON(http.StatusInternalServerError, gin.H{
                "error": gin.H{
                    "code":    "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                },
            })
        }
    }
}
```

### Agent

faion-backend-agent
