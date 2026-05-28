---
name: go-web-frameworks
description: Use this skill when building high-performance web applications in Go using either the Echo or Gin frameworks.
---

# Go Web Frameworks Standards

## Application Setup

### Echo Framework

```go
package main

import (
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
)

func main() {
    e := echo.New()

    // Middleware
    e.Use(middleware.Logger())
    e.Use(middleware.Recover())
    e.Use(middleware.CORS())

    // Routes
    e.GET("/", homeHandler)
    e.GET("/users/:id", getUser)
    e.POST("/users", createUser)

    // Groups
    api := e.Group("/api/v1")
    api.GET("/items", listItems)

    e.Logger.Fatal(e.Start(":8080"))
}
```

### Gin Framework

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

### Echo Handlers

```go
// Path parameters
func getUser(c echo.Context) error {
    id := c.Param("id")
    user, err := findUser(id)
    if err != nil {
        return echo.NewHTTPError(404, "User not found")
    }
    return c.JSON(200, user)
}

// Query parameters
func listUsers(c echo.Context) error {
    page := c.QueryParam("page")
    limit := c.QueryParam("limit")
    users := fetchUsers(page, limit)
    return c.JSON(200, users)
}

// JSON body binding
type CreateUserRequest struct {
    Name  string `json:"name" validate:"required"`
    Email string `json:"email" validate:"required,email"`
}

func createUser(c echo.Context) error {
    var req CreateUserRequest
    if err := c.Bind(&req); err != nil {
        return echo.NewHTTPError(400, err.Error())
    }
    if err := c.Validate(&req); err != nil {
        return err
    }
    user := insertUser(req)
    return c.JSON(201, user)
}
```

### Gin Handlers

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

## Middleware

### Echo Middleware

```go
// Built-in middleware
e.Use(middleware.Logger())
e.Use(middleware.Recover())
e.Use(middleware.CORS())
e.Use(middleware.Gzip())
e.Use(middleware.RateLimiter(middleware.NewRateLimiterMemoryStore(20)))

// JWT middleware
e.Use(middleware.JWTWithConfig(middleware.JWTConfig{
    SigningKey: []byte("secret"),
    Claims:     &JwtCustomClaims{},
}))

// Custom middleware
func authMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
    return func(c echo.Context) error {
        token := c.Request().Header.Get("Authorization")
        if token == "" {
            return echo.NewHTTPError(401, "Unauthorized")
        }

        user, err := validateToken(token)
        if err != nil {
            return echo.NewHTTPError(401, "Invalid token")
        }

        c.Set("user", user)
        return next(c)
    }
}
```

### Gin Middleware

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
```

## Error Handling

### Echo Error Handling

```go
// Custom HTTP error handler
e.HTTPErrorHandler = func(err error, c echo.Context) {
    code := 500
    message := "Internal Server Error"

    if he, ok := err.(*echo.HTTPError); ok {
        code = he.Code
        message = he.Message.(string)
    }

    c.JSON(code, map[string]string{
        "error": message,
    })
}
```

### Gin Error Handling

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
```

## Best Practices

1. **Validation**: Always validate input with custom validators in both frameworks.
2. **Error handling**: Use `echo.NewHTTPError` for HTTP errors in Echo and centralized error handling in Gin.
3. **Middleware order**: Logger first, then Recovery, then custom middleware.
4. **Graceful shutdown**: Implement graceful shutdown using `e.Shutdown(ctx)` for Echo and `http.Server` for Gin.
5. **Logging**: Use structured logging for better insights.