---
name: Gin Framework
description: High-performance Go web framework with martini-like API.
metadata:
  labels: [golang, gin, web, framework]
  triggers:
    files: ['**/main.go', '**/routes.go']
    keywords: [gin, gin.Default, gin.Engine, c.JSON]
---

# Gin Framework Standards

## Router Setup

```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default() // Includes Logger and Recovery middleware

    // Routes
    r.GET("/ping", pingHandler)
    r.POST("/users", createUser)

    // Route groups
    api := r.Group("/api/v1")
    {
        api.GET("/users", listUsers)
        api.GET("/users/:id", getUser)
        api.PUT("/users/:id", updateUser)
        api.DELETE("/users/:id", deleteUser)
    }

    r.Run(":8080")
}
```

## Handlers

```go
// Path parameters
func getUser(c *gin.Context) {
    id := c.Param("id")
    user, err := findUser(id)
    if err != nil {
        c.JSON(404, gin.H{"error": "User not found"})
        return
    }
    c.JSON(200, user)
}

// Query parameters
func listUsers(c *gin.Context) {
    page := c.DefaultQuery("page", "1")
    limit := c.DefaultQuery("limit", "10")
    users := fetchUsers(page, limit)
    c.JSON(200, users)
}

// JSON body binding
type CreateUserRequest struct {
    Name  string `json:"name" binding:"required"`
    Email string `json:"email" binding:"required,email"`
}

func createUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    user := insertUser(req)
    c.JSON(201, user)
}
```

## Binding & Validation

```go
type LoginRequest struct {
    Username string `json:"username" binding:"required,min=3,max=50"`
    Password string `json:"password" binding:"required,min=8"`
}

// Custom validation
type BookingRequest struct {
    CheckIn  time.Time `json:"check_in" binding:"required"`
    CheckOut time.Time `json:"check_out" binding:"required,gtfield=CheckIn"`
}

// Bind from different sources
c.ShouldBindJSON(&obj)    // JSON body
c.ShouldBindQuery(&obj)   // Query string
c.ShouldBind(&obj)        // Auto-detect
```

## Middleware

```go
// Global middleware
r := gin.New()
r.Use(gin.Logger())
r.Use(gin.Recovery())
r.Use(corsMiddleware())

// Group middleware
authorized := r.Group("/admin")
authorized.Use(authMiddleware())

// Custom middleware
func authMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.AbortWithStatusJSON(401, gin.H{"error": "Unauthorized"})
            return
        }

        user, err := validateToken(token)
        if err != nil {
            c.AbortWithStatusJSON(401, gin.H{"error": "Invalid token"})
            return
        }

        c.Set("user", user)
        c.Next()
    }
}

// Access middleware data
func handler(c *gin.Context) {
    user, _ := c.Get("user")
    // use user
}
```

## Error Handling

```go
// Centralized error handling
type AppError struct {
    Code    int    `json:"code"`
    Message string `json:"message"`
}

func errorMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        if len(c.Errors) > 0 {
            err := c.Errors.Last()
            switch e := err.Err.(type) {
            case *AppError:
                c.JSON(e.Code, e)
            default:
                c.JSON(500, gin.H{"error": "Internal server error"})
            }
        }
    }
}

// In handler
func handler(c *gin.Context) {
    if err := doSomething(); err != nil {
        c.Error(&AppError{Code: 400, Message: err.Error()})
        return
    }
}
```

## Dependency Injection

```go
type Handler struct {
    db     *sql.DB
    cache  *redis.Client
    logger *zap.Logger
}

func NewHandler(db *sql.DB, cache *redis.Client, logger *zap.Logger) *Handler {
    return &Handler{db: db, cache: cache, logger: logger}
}

func (h *Handler) GetUser(c *gin.Context) {
    user, err := h.db.FindUser(c.Param("id"))
    // ...
}

// Setup routes
func SetupRoutes(r *gin.Engine, h *Handler) {
    r.GET("/users/:id", h.GetUser)
}
```

## Best Practices

1. **Gin modes**: Use `gin.SetMode(gin.ReleaseMode)` in production
2. **Graceful shutdown**: Implement with `http.Server` and context
3. **Validation**: Use struct tags for input validation
4. **Logging**: Replace default logger with structured logging (zap/zerolog)
5. **Testing**: Use `httptest` with gin test mode
