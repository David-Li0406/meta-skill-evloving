---
name: Echo Framework
description: High-performance, minimalist Go web framework.
metadata:
  labels: [golang, echo, web, framework]
  triggers:
    files: ['**/main.go']
    keywords: [echo, echo.New, echo.Context, e.Start]
---

# Echo Framework Standards

## Application Setup

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

## Handlers

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

## Validation

```go
import "github.com/go-playground/validator/v10"

type CustomValidator struct {
    validator *validator.Validate
}

func (cv *CustomValidator) Validate(i interface{}) error {
    if err := cv.validator.Struct(i); err != nil {
        return echo.NewHTTPError(400, err.Error())
    }
    return nil
}

func main() {
    e := echo.New()
    e.Validator = &CustomValidator{validator: validator.New()}
}
```

## Middleware

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

// Apply middleware to group
api := e.Group("/api", authMiddleware)
```

## Error Handling

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

// In handlers
func handler(c echo.Context) error {
    if notFound {
        return echo.NewHTTPError(404, "Resource not found")
    }
    return c.JSON(200, data)
}
```

## Response Types

```go
// JSON
c.JSON(200, user)

// String
c.String(200, "Hello, World!")

// HTML
c.HTML(200, "<h1>Hello</h1>")

// File
c.File("path/to/file.pdf")

// Stream
c.Stream(200, "text/csv", reader)

// Redirect
c.Redirect(301, "/new-location")

// No Content
c.NoContent(204)
```

## Context Values

```go
// Set value
c.Set("user", user)

// Get value
user := c.Get("user").(*User)

// Request context
ctx := c.Request().Context()
```

## Best Practices

1. **Validation**: Always validate input with custom validator
2. **Error handling**: Use `echo.NewHTTPError` for HTTP errors
3. **Context**: Don't store echo.Context outside request lifecycle
4. **Middleware order**: Logger first, then Recover, then custom
5. **Graceful shutdown**: Use `e.Shutdown(ctx)` for graceful shutdown
