---
title: API Error Response Standards
impact: HIGH
impactDescription: Consistent error format
tags: error, api, response
---

## API Error Response Standards

Define a unified API error response format.

**Error Response Structure:**

```go
// pkg/response/error.go
package response

type ErrorResponse struct {
    Code    string                 `json:"code"`
    Message string                 `json:"message"`
    Details map[string]interface{} `json:"details,omitempty"`
}

// Common error codes
const (
    ErrCodeValidation   = "VALIDATION_ERROR"
    ErrCodeNotFound     = "NOT_FOUND"
    ErrCodeUnauthorized = "UNAUTHORIZED"
    ErrCodeForbidden    = "FORBIDDEN"
    ErrCodeInternal     = "INTERNAL_ERROR"
    ErrCodeConflict     = "CONFLICT"
)
```

**Middleware for Unified Handling:**

```go
// internal/interfaces/http/middleware/error.go
package middleware

func ErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        if len(c.Errors) > 0 {
            err := c.Errors.Last().Err
            handleError(c, err)
        }
    }
}

func handleError(c *gin.Context, err error) {
    var validErr *errors.ValidationError
    if errors.As(err, &validErr) {
        c.JSON(http.StatusBadRequest, response.ErrorResponse{
            Code:    response.ErrCodeValidation,
            Message: validErr.Message,
            Details: map[string]interface{}{"field": validErr.Field},
        })
        return
    }

    if errors.Is(err, user.ErrUserNotFound) {
        c.JSON(http.StatusNotFound, response.ErrorResponse{
            Code:    response.ErrCodeNotFound,
            Message: "User not found",
        })
        return
    }

    // Unknown error: log it, return generic error
    log.Printf("internal error: %v", err)
    c.JSON(http.StatusInternalServerError, response.ErrorResponse{
        Code:    response.ErrCodeInternal,
        Message: "An internal error occurred",
    })
}
```

**Example Response:**

```json
{
    "code": "VALIDATION_ERROR",
    "message": "Email format is invalid",
    "details": {
        "field": "email"
    }
}
```
