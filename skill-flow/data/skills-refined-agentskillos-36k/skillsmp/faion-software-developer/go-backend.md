# Go Backend Development

**Go backend patterns for production-grade applications with Gin and Echo frameworks.**

---

## Go Project Structure

### Problem
Organize Go projects for maintainability and team collaboration.

### Framework: Standard Layout

```
project/
├── cmd/
│   └── api/
│       └── main.go           # Entry point
├── internal/
│   ├── handler/              # HTTP handlers
│   ├── service/              # Business logic
│   ├── repository/           # Data access
│   ├── model/                # Domain models
│   ├── middleware/           # HTTP middleware
│   └── config/               # Configuration
├── pkg/                      # Public packages
├── migrations/               # Database migrations
├── go.mod
└── go.sum
```

### Key Principles

- `internal/` prevents external imports
- `cmd/` for multiple binaries
- Flat structure within packages
- Interfaces defined at consumer side

### Example: Handler

```go
// internal/handler/user.go
package handler

import (
    "net/http"
    "github.com/gin-gonic/gin"
    "project/internal/service"
)

type UserHandler struct {
    userService service.UserService
}

func NewUserHandler(us service.UserService) *UserHandler {
    return &UserHandler{userService: us}
}

func (h *UserHandler) GetUser(c *gin.Context) {
    id := c.Param("id")
    user, err := h.userService.GetByID(c.Request.Context(), id)
    if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
        return
    }
    c.JSON(http.StatusOK, user)
}
```

---

## HTTP Handlers (Gin/Echo)

### Problem
Build performant HTTP APIs with proper request handling.

### Framework: Gin Router

```go
package main

import (
    "github.com/gin-gonic/gin"
    "project/internal/handler"
    "project/internal/middleware"
)

func SetupRouter(h *handler.UserHandler) *gin.Engine {
    r := gin.Default()

    // Global middleware
    r.Use(middleware.RequestID())
    r.Use(middleware.Logger())
    r.Use(middleware.Recovery())

    // API v1
    v1 := r.Group("/api/v1")
    {
        users := v1.Group("/users")
        users.Use(middleware.Auth())
        {
            users.GET("", h.ListUsers)
            users.GET("/:id", h.GetUser)
            users.POST("", h.CreateUser)
            users.PUT("/:id", h.UpdateUser)
            users.DELETE("/:id", h.DeleteUser)
        }
    }

    return r
}
```

### Framework: Echo Router

```go
package main

import (
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
)

func SetupRouter() *echo.Echo {
    e := echo.New()

    e.Use(middleware.Logger())
    e.Use(middleware.Recover())
    e.Use(middleware.RequestID())

    api := e.Group("/api/v1")
    api.Use(middleware.JWT([]byte("secret")))

    api.GET("/users", listUsers)
    api.GET("/users/:id", getUser)
    api.POST("/users", createUser)

    return e
}
```

### Request Binding

```go
type CreateUserRequest struct {
    Name  string `json:"name" binding:"required,min=2,max=100"`
    Email string `json:"email" binding:"required,email"`
    Age   int    `json:"age" binding:"gte=0,lte=130"`
}

func (h *UserHandler) CreateUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    // Process valid request
}
```

---

## Go Concurrency Patterns

### Problem
Handle concurrent operations safely and efficiently.

### Framework: Worker Pool

```go
package worker

import (
    "context"
    "sync"
)

type Job func(ctx context.Context) error

type Pool struct {
    workers int
    jobs    chan Job
    wg      sync.WaitGroup
}

func NewPool(workers int, buffer int) *Pool {
    return &Pool{
        workers: workers,
        jobs:    make(chan Job, buffer),
    }
}

func (p *Pool) Start(ctx context.Context) {
    for i := 0; i < p.workers; i++ {
        p.wg.Add(1)
        go p.worker(ctx)
    }
}

func (p *Pool) worker(ctx context.Context) {
    defer p.wg.Done()
    for {
        select {
        case <-ctx.Done():
            return
        case job, ok := <-p.jobs:
            if !ok {
                return
            }
            _ = job(ctx) // Handle error as needed
        }
    }
}

func (p *Pool) Submit(job Job) {
    p.jobs <- job
}

func (p *Pool) Stop() {
    close(p.jobs)
    p.wg.Wait()
}
```

### Framework: Fan-Out/Fan-In

```go
func ProcessItems(ctx context.Context, items []Item) []Result {
    numWorkers := runtime.NumCPU()
    jobs := make(chan Item, len(items))
    results := make(chan Result, len(items))

    // Fan-out: start workers
    var wg sync.WaitGroup
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for item := range jobs {
                results <- processItem(ctx, item)
            }
        }()
    }

    // Send jobs
    for _, item := range items {
        jobs <- item
    }
    close(jobs)

    // Wait and close results
    go func() {
        wg.Wait()
        close(results)
    }()

    // Fan-in: collect results
    var output []Result
    for r := range results {
        output = append(output, r)
    }
    return output
}
```

---

## Go Error Handling

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

---

## Sources

- [Go Gin](https://gin-gonic.com/docs/)
- [Go Echo](https://echo.labstack.com/docs)
