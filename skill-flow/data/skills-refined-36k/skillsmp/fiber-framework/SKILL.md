---
name: Fiber Framework
description: Express-inspired Go web framework built on fasthttp.
metadata:
  labels: [golang, fiber, web, framework, fasthttp]
  triggers:
    files: ['**/main.go']
    keywords: [fiber, fiber.New, fiber.Ctx, app.Listen]
---

# Fiber Framework Standards

## Application Setup

```go
package main

import (
    "github.com/gofiber/fiber/v2"
    "github.com/gofiber/fiber/v2/middleware/logger"
    "github.com/gofiber/fiber/v2/middleware/recover"
)

func main() {
    app := fiber.New(fiber.Config{
        ErrorHandler: customErrorHandler,
        ReadTimeout:  10 * time.Second,
        WriteTimeout: 10 * time.Second,
    })

    // Middleware
    app.Use(logger.New())
    app.Use(recover.New())

    // Routes
    app.Get("/", homeHandler)
    app.Get("/users/:id", getUser)
    app.Post("/users", createUser)

    // Route groups
    api := app.Group("/api/v1")
    api.Get("/items", listItems)

    app.Listen(":3000")
}
```

## Handlers

```go
// Path parameters
func getUser(c *fiber.Ctx) error {
    id := c.Params("id")
    user, err := findUser(id)
    if err != nil {
        return c.Status(404).JSON(fiber.Map{"error": "Not found"})
    }
    return c.JSON(user)
}

// Query parameters
func listUsers(c *fiber.Ctx) error {
    page := c.QueryInt("page", 1)
    limit := c.QueryInt("limit", 10)
    users := fetchUsers(page, limit)
    return c.JSON(users)
}

// JSON body
type CreateUserRequest struct {
    Name  string `json:"name"`
    Email string `json:"email"`
}

func createUser(c *fiber.Ctx) error {
    var req CreateUserRequest
    if err := c.BodyParser(&req); err != nil {
        return c.Status(400).JSON(fiber.Map{"error": "Invalid request"})
    }
    user := insertUser(req)
    return c.Status(201).JSON(user)
}
```

## Middleware

```go
// Built-in middleware
app.Use(logger.New())
app.Use(recover.New())
app.Use(cors.New())
app.Use(compress.New())
app.Use(limiter.New(limiter.Config{
    Max:        100,
    Expiration: 1 * time.Minute,
}))

// Custom middleware
func authMiddleware(c *fiber.Ctx) error {
    token := c.Get("Authorization")
    if token == "" {
        return c.Status(401).JSON(fiber.Map{"error": "Unauthorized"})
    }

    user, err := validateToken(token)
    if err != nil {
        return c.Status(401).JSON(fiber.Map{"error": "Invalid token"})
    }

    c.Locals("user", user)
    return c.Next()
}

// Apply middleware
api := app.Group("/api", authMiddleware)
```

## Error Handling

```go
// Custom error handler
func customErrorHandler(c *fiber.Ctx, err error) error {
    code := fiber.StatusInternalServerError
    message := "Internal Server Error"

    if e, ok := err.(*fiber.Error); ok {
        code = e.Code
        message = e.Message
    }

    return c.Status(code).JSON(fiber.Map{
        "error": message,
    })
}

// In handlers, return fiber.Error
func handler(c *fiber.Ctx) error {
    if notFound {
        return fiber.NewError(404, "Resource not found")
    }
    return c.JSON(data)
}
```

## Validation

```go
import "github.com/go-playground/validator/v10"

var validate = validator.New()

type CreateItemRequest struct {
    Name  string `json:"name" validate:"required,min=1,max=100"`
    Price int    `json:"price" validate:"required,min=0"`
}

func createItem(c *fiber.Ctx) error {
    var req CreateItemRequest
    if err := c.BodyParser(&req); err != nil {
        return c.Status(400).JSON(fiber.Map{"error": "Invalid JSON"})
    }

    if err := validate.Struct(&req); err != nil {
        return c.Status(400).JSON(fiber.Map{"error": err.Error()})
    }

    item := insertItem(req)
    return c.Status(201).JSON(item)
}
```

## WebSocket Support

```go
import "github.com/gofiber/websocket/v2"

app.Get("/ws", websocket.New(func(c *websocket.Conn) {
    for {
        mt, msg, err := c.ReadMessage()
        if err != nil {
            break
        }
        if err := c.WriteMessage(mt, msg); err != nil {
            break
        }
    }
}))
```

## Best Practices

1. **fasthttp awareness**: Fiber uses fasthttp, not net/http - some incompatibilities
2. **Context reuse**: Don't store `*fiber.Ctx` - it's reused across requests
3. **Prefork**: Use `app.Listen(":3000", fiber.Config{Prefork: true})` for multi-core
4. **Graceful shutdown**: Use `app.ShutdownWithTimeout(30 * time.Second)`
5. **Memory**: fasthttp is optimized for low memory, high concurrency
