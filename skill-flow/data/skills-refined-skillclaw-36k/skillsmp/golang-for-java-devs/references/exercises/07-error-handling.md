# Exercise 07: Error Handling Patterns

**Time:** 15 minutes
**Goal:** Implement consistent error handling across handlers

## The Spring Boot Version

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(ResourceNotFoundException e) {
        return new ErrorResponse("NOT_FOUND", e.getMessage());
    }

    @ExceptionHandler(ValidationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleValidation(ValidationException e) {
        return new ErrorResponse("VALIDATION_ERROR", e.getMessage());
    }
}
```

## The Go Way

No global exception handler. Instead:
1. Define error types
2. Create error response helpers
3. Use middleware for common handling

---

## Step by Step

### 1. Define error types (3 min)

Create `internal/apperror/errors.go`:

```go
package apperror

import (
    "errors"
    "fmt"
    "net/http"
)

// sentinel errors
var (
    ErrNotFound     = errors.New("not found")
    ErrBadRequest   = errors.New("bad request")
    ErrUnauthorized = errors.New("unauthorized")
    ErrForbidden    = errors.New("forbidden")
    ErrInternal     = errors.New("internal error")
)

// AppError carries HTTP status and message
type AppError struct {
    Err     error
    Message string
    Code    string
    Status  int
}

func (e *AppError) Error() string {
    if e.Message != "" {
        return e.Message
    }
    return e.Err.Error()
}

func (e *AppError) Unwrap() error {
    return e.Err
}

// constructors for common errors
func NotFound(message string) *AppError {
    return &AppError{
        Err:     ErrNotFound,
        Message: message,
        Code:    "NOT_FOUND",
        Status:  http.StatusNotFound,
    }
}

func BadRequest(message string) *AppError {
    return &AppError{
        Err:     ErrBadRequest,
        Message: message,
        Code:    "BAD_REQUEST",
        Status:  http.StatusBadRequest,
    }
}

func ValidationError(message string) *AppError {
    return &AppError{
        Err:     ErrBadRequest,
        Message: message,
        Code:    "VALIDATION_ERROR",
        Status:  http.StatusBadRequest,
    }
}

func Unauthorized(message string) *AppError {
    return &AppError{
        Err:     ErrUnauthorized,
        Message: message,
        Code:    "UNAUTHORIZED",
        Status:  http.StatusUnauthorized,
    }
}

func Internal(err error) *AppError {
    return &AppError{
        Err:     fmt.Errorf("%w: %v", ErrInternal, err),
        Message: "internal server error",
        Code:    "INTERNAL_ERROR",
        Status:  http.StatusInternalServerError,
    }
}
```

### 2. Create error response helper (3 min)

Create `internal/handler/response.go`:

```go
package handler

import (
    "encoding/json"
    "errors"
    "log/slog"
    "net/http"

    "my-first-go-app/internal/apperror"
)

type ErrorResponse struct {
    Code    string `json:"code"`
    Message string `json:"message"`
}

func WriteError(w http.ResponseWriter, logger *slog.Logger, err error) {
    var appErr *apperror.AppError
    if errors.As(err, &appErr) {
        writeJSON(w, appErr.Status, ErrorResponse{
            Code:    appErr.Code,
            Message: appErr.Message,
        })

        if appErr.Status >= 500 {
            logger.Error("internal error", "error", err)
        }
        return
    }

    // unknown error - treat as internal
    logger.Error("unexpected error", "error", err)
    writeJSON(w, http.StatusInternalServerError, ErrorResponse{
        Code:    "INTERNAL_ERROR",
        Message: "internal server error",
    })
}

func WriteJSON(w http.ResponseWriter, status int, data interface{}) {
    writeJSON(w, status, data)
}

func writeJSON(w http.ResponseWriter, status int, data interface{}) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(data)
}
```

### 3. Update handler to use error types (5 min)

Update `internal/handler/task.go`:

```go
package handler

import (
    "encoding/json"
    "errors"
    "log/slog"
    "net/http"

    "github.com/go-chi/chi/v5"
    "github.com/go-playground/validator/v10"
    "github.com/google/uuid"

    "my-first-go-app/internal/apperror"
    "my-first-go-app/internal/model"
    "my-first-go-app/internal/repository"
)

type TaskHandler struct {
    repo     *repository.TaskRepository
    validate *validator.Validate
    logger   *slog.Logger
}

func NewTaskHandler(repo *repository.TaskRepository, logger *slog.Logger) *TaskHandler {
    return &TaskHandler{
        repo:     repo,
        validate: validator.New(),
        logger:   logger,
    }
}

func (h *TaskHandler) GetByID(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")

    task, err := h.repo.FindByID(r.Context(), id)
    if err != nil {
        if errors.Is(err, repository.ErrNotFound) {
            WriteError(w, h.logger, apperror.NotFound("task not found"))
            return
        }
        WriteError(w, h.logger, apperror.Internal(err))
        return
    }

    WriteJSON(w, http.StatusOK, task)
}

func (h *TaskHandler) Create(w http.ResponseWriter, r *http.Request) {
    var req CreateTaskRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        WriteError(w, h.logger, apperror.BadRequest("invalid json body"))
        return
    }

    if err := h.validate.Struct(req); err != nil {
        WriteError(w, h.logger, apperror.ValidationError(formatValidationError(err)))
        return
    }

    task := &model.Task{
        ID:          uuid.New().String(),
        Title:       req.Title,
        Description: req.Description,
    }

    if err := h.repo.Save(r.Context(), task); err != nil {
        WriteError(w, h.logger, apperror.Internal(err))
        return
    }

    WriteJSON(w, http.StatusCreated, task)
}

func formatValidationError(err error) string {
    var sb strings.Builder
    for i, e := range err.(validator.ValidationErrors) {
        if i > 0 {
            sb.WriteString("; ")
        }
        sb.WriteString(fmt.Sprintf("%s: failed %s validation", e.Field(), e.Tag()))
    }
    return sb.String()
}
```

### 4. Create error recovery middleware (4 min)

Create `internal/middleware/recovery.go`:

```go
package middleware

import (
    "log/slog"
    "net/http"
    "runtime/debug"
)

func Recovery(logger *slog.Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            defer func() {
                if err := recover(); err != nil {
                    logger.Error("panic recovered",
                        "error", err,
                        "stack", string(debug.Stack()),
                        "path", r.URL.Path,
                    )

                    w.Header().Set("Content-Type", "application/json")
                    w.WriteHeader(http.StatusInternalServerError)
                    w.Write([]byte(`{"code":"INTERNAL_ERROR","message":"internal server error"}`))
                }
            }()

            next.ServeHTTP(w, r)
        })
    }
}
```

## Error Response Format

Consistent JSON error responses:

```json
{
    "code": "NOT_FOUND",
    "message": "task not found"
}
```

```json
{
    "code": "VALIDATION_ERROR",
    "message": "Title: failed required validation; Description: failed max validation"
}
```

## What Just Happened?

| Spring Boot | Go |
|-------------|-----|
| @RestControllerAdvice | Error helper functions |
| @ExceptionHandler | errors.As type checking |
| Custom exceptions | Custom error types |
| Global handling | Per-handler or middleware |

## Checkpoint

- [ ] Custom error types defined
- [ ] Consistent error response format
- [ ] Proper status codes for each error type
- [ ] Internal errors logged, not exposed

**Next:** Exercise 08 - Testing Handlers
