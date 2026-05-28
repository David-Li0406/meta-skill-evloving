---
id: go-error-handling-patterns
name: "Go Error Handling"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Go Error Handling

## Overview

Go's explicit error handling is a core language feature that promotes robust code. This methodology covers error creation, wrapping, checking, and best practices for building reliable Go applications.

## When to Use

- All Go projects
- API error responses
- Database operations
- External service calls
- Any operation that can fail

## Key Principles

1. **Errors are values** - Handle them like any other value
2. **Wrap errors** - Add context as errors propagate up
3. **Check errors immediately** - Don't defer error checking
4. **Sentinel errors** - Use for expected conditions
5. **Custom error types** - For rich error information

## Best Practices

### Basic Error Handling

```go
package main

import (
    "errors"
    "fmt"
    "log"
)

// Always check errors immediately after the call
func readFile(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("reading file %s: %w", path, err)
    }
    return data, nil
}

// Handle errors at appropriate level
func main() {
    data, err := readFile("config.json")
    if err != nil {
        log.Fatalf("failed to read config: %v", err)
    }
    // use data
}
```

### Error Wrapping with Context

```go
package service

import (
    "errors"
    "fmt"
)

// Wrap errors to add context
func (s *UserService) GetUser(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("getting user %s: %w", id, err)
    }

    if user == nil {
        return nil, fmt.Errorf("user %s: %w", id, ErrNotFound)
    }

    return user, nil
}

// Unwrap errors to check cause
func (h *Handler) handleError(err error) int {
    if errors.Is(err, ErrNotFound) {
        return http.StatusNotFound
    }
    if errors.Is(err, ErrUnauthorized) {
        return http.StatusUnauthorized
    }
    if errors.Is(err, ErrValidation) {
        return http.StatusBadRequest
    }
    return http.StatusInternalServerError
}
```

### Sentinel Errors

```go
package apperror

import "errors"

// Sentinel errors for expected conditions
var (
    ErrNotFound      = errors.New("resource not found")
    ErrUnauthorized  = errors.New("unauthorized")
    ErrForbidden     = errors.New("forbidden")
    ErrValidation    = errors.New("validation failed")
    ErrConflict      = errors.New("resource conflict")
    ErrInternal      = errors.New("internal error")
)

// Usage
func (r *UserRepository) FindByID(ctx context.Context, id string) (*User, error) {
    var user User
    err := r.db.GetContext(ctx, &user, "SELECT * FROM users WHERE id = $1", id)
    if err == sql.ErrNoRows {
        return nil, ErrNotFound
    }
    if err != nil {
        return nil, fmt.Errorf("querying user: %w", err)
    }
    return &user, nil
}

// Checking sentinel errors
func (s *Service) GetUser(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if errors.Is(err, ErrNotFound) {
        // Handle not found case
        return nil, fmt.Errorf("user %s: %w", id, err)
    }
    if err != nil {
        return nil, err
    }
    return user, nil
}
```

### Custom Error Types

```go
package apperror

import (
    "fmt"
    "net/http"
)

// Custom error type with additional context
type AppError struct {
    Code    string            `json:"code"`
    Message string            `json:"message"`
    Status  int               `json:"-"`
    Details map[string]string `json:"details,omitempty"`
    Err     error             `json:"-"`
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

// Constructor functions
func NotFound(resource, id string) *AppError {
    return &AppError{
        Code:    "NOT_FOUND",
        Message: fmt.Sprintf("%s with id %s not found", resource, id),
        Status:  http.StatusNotFound,
    }
}

func ValidationError(details map[string]string) *AppError {
    return &AppError{
        Code:    "VALIDATION_ERROR",
        Message: "validation failed",
        Status:  http.StatusBadRequest,
        Details: details,
    }
}

func Unauthorized(message string) *AppError {
    return &AppError{
        Code:    "UNAUTHORIZED",
        Message: message,
        Status:  http.StatusUnauthorized,
    }
}

func Internal(err error) *AppError {
    return &AppError{
        Code:    "INTERNAL_ERROR",
        Message: "internal server error",
        Status:  http.StatusInternalServerError,
        Err:     err,
    }
}

// Check if error is AppError
func AsAppError(err error) (*AppError, bool) {
    var appErr *AppError
    if errors.As(err, &appErr) {
        return appErr, true
    }
    return nil, false
}
```

### Error Handling in HTTP Handlers

```go
package handler

import (
    "encoding/json"
    "errors"
    "log/slog"
    "net/http"

    "github.com/username/project/internal/apperror"
)

type Handler struct {
    userService UserService
    logger      *slog.Logger
}

func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")

    user, err := h.userService.GetUser(r.Context(), id)
    if err != nil {
        h.handleError(w, r, err)
        return
    }

    h.respondJSON(w, http.StatusOK, user)
}

func (h *Handler) handleError(w http.ResponseWriter, r *http.Request, err error) {
    // Check for custom AppError
    if appErr, ok := apperror.AsAppError(err); ok {
        h.respondJSON(w, appErr.Status, appErr)
        return
    }

    // Check for sentinel errors
    switch {
    case errors.Is(err, apperror.ErrNotFound):
        h.respondJSON(w, http.StatusNotFound, map[string]string{
            "error": "resource not found",
        })
    case errors.Is(err, apperror.ErrUnauthorized):
        h.respondJSON(w, http.StatusUnauthorized, map[string]string{
            "error": "unauthorized",
        })
    case errors.Is(err, apperror.ErrValidation):
        h.respondJSON(w, http.StatusBadRequest, map[string]string{
            "error": "validation failed",
        })
    default:
        // Log unexpected errors
        h.logger.Error("unexpected error",
            "error", err,
            "path", r.URL.Path,
            "method", r.Method,
        )
        h.respondJSON(w, http.StatusInternalServerError, map[string]string{
            "error": "internal server error",
        })
    }
}

func (h *Handler) respondJSON(w http.ResponseWriter, status int, data any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(data)
}
```

### Multiple Error Aggregation

```go
package validation

import (
    "errors"
    "strings"
)

// MultiError collects multiple errors
type MultiError struct {
    Errors []error
}

func (m *MultiError) Add(err error) {
    if err != nil {
        m.Errors = append(m.Errors, err)
    }
}

func (m *MultiError) HasErrors() bool {
    return len(m.Errors) > 0
}

func (m *MultiError) Error() string {
    if len(m.Errors) == 0 {
        return ""
    }

    msgs := make([]string, len(m.Errors))
    for i, err := range m.Errors {
        msgs[i] = err.Error()
    }
    return strings.Join(msgs, "; ")
}

func (m *MultiError) Unwrap() []error {
    return m.Errors
}

// Usage
func ValidateUser(input CreateUserInput) error {
    var errs MultiError

    if input.Email == "" {
        errs.Add(errors.New("email is required"))
    }
    if input.Name == "" {
        errs.Add(errors.New("name is required"))
    }
    if len(input.Password) < 8 {
        errs.Add(errors.New("password must be at least 8 characters"))
    }

    if errs.HasErrors() {
        return &errs
    }
    return nil
}
```

### Retry with Exponential Backoff

```go
package retry

import (
    "context"
    "errors"
    "math"
    "time"
)

type RetryConfig struct {
    MaxAttempts int
    InitialWait time.Duration
    MaxWait     time.Duration
    Multiplier  float64
}

func DefaultConfig() RetryConfig {
    return RetryConfig{
        MaxAttempts: 3,
        InitialWait: 100 * time.Millisecond,
        MaxWait:     10 * time.Second,
        Multiplier:  2.0,
    }
}

// Retryable marks an error as retryable
type Retryable interface {
    Retryable() bool
}

func IsRetryable(err error) bool {
    var r Retryable
    if errors.As(err, &r) {
        return r.Retryable()
    }
    return false
}

func Do(ctx context.Context, cfg RetryConfig, fn func() error) error {
    var lastErr error

    for attempt := 0; attempt < cfg.MaxAttempts; attempt++ {
        err := fn()
        if err == nil {
            return nil
        }

        lastErr = err

        // Don't retry if not retryable
        if !IsRetryable(err) {
            return err
        }

        // Calculate backoff
        wait := time.Duration(float64(cfg.InitialWait) * math.Pow(cfg.Multiplier, float64(attempt)))
        if wait > cfg.MaxWait {
            wait = cfg.MaxWait
        }

        // Wait or context cancelled
        select {
        case <-ctx.Done():
            return ctx.Err()
        case <-time.After(wait):
        }
    }

    return fmt.Errorf("max retries exceeded: %w", lastErr)
}
```

### Panic Recovery

```go
package middleware

import (
    "log/slog"
    "net/http"
    "runtime/debug"
)

// Recovery middleware catches panics
func Recovery(logger *slog.Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            defer func() {
                if rec := recover(); rec != nil {
                    logger.Error("panic recovered",
                        "panic", rec,
                        "stack", string(debug.Stack()),
                        "path", r.URL.Path,
                    )

                    http.Error(w, "Internal Server Error", http.StatusInternalServerError)
                }
            }()

            next.ServeHTTP(w, r)
        })
    }
}

// Only panic for programming errors, not runtime errors
func mustParse(s string) int {
    n, err := strconv.Atoi(s)
    if err != nil {
        panic(fmt.Sprintf("invalid number: %s", s))
    }
    return n
}
```

## Anti-patterns

### Avoid: Ignoring Errors

```go
// BAD - ignored error
data, _ := json.Marshal(user)
w.Write(data)

// GOOD - handle error
data, err := json.Marshal(user)
if err != nil {
    log.Printf("failed to marshal user: %v", err)
    http.Error(w, "Internal Error", 500)
    return
}
w.Write(data)
```

### Avoid: Logging and Returning

```go
// BAD - logs error then returns it (causes duplicate logs)
func GetUser(id string) (*User, error) {
    user, err := repo.Find(id)
    if err != nil {
        log.Printf("error getting user: %v", err)
        return nil, err
    }
    return user, nil
}

// GOOD - wrap and return, let caller decide to log
func GetUser(id string) (*User, error) {
    user, err := repo.Find(id)
    if err != nil {
        return nil, fmt.Errorf("getting user %s: %w", id, err)
    }
    return user, nil
}
```

### Avoid: Using Panic for Control Flow

```go
// BAD - panic for expected conditions
func GetUser(id string) *User {
    user, err := repo.Find(id)
    if err != nil {
        panic(err)
    }
    return user
}

// GOOD - return error
func GetUser(id string) (*User, error) {
    user, err := repo.Find(id)
    if err != nil {
        return nil, err
    }
    return user, nil
}
```

## References

- [Error Handling in Go](https://go.dev/blog/error-handling-and-go)
- [Working with Errors in Go 1.13](https://go.dev/blog/go1.13-errors)
- [Don't Just Check Errors, Handle Them Gracefully](https://dave.cheney.net/2016/04/27/dont-just-check-errors-handle-them-gracefully)
- [Uber Go Style Guide - Errors](https://github.com/uber-go/guide/blob/master/style.md#errors)
