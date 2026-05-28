# Fiber Routing Patterns

## Basic Setup

```go
import "github.com/gofiber/fiber/v2"

func main() {
    app := fiber.New(fiber.Config{
        Prefork:       false,
        CaseSensitive: true,
        StrictRouting: true,
        ServerHeader:  "MyApp",
        AppName:       "My App v1.0.0",
    })

    // Basic routes
    app.Get("/", func(c *fiber.Ctx) error {
        return c.SendString("Hello, World!")
    })

    app.Post("/users", createUser)
    app.Get("/users/:id", getUser)
    app.Put("/users/:id", updateUser)
    app.Delete("/users/:id", deleteUser)

    app.Listen(":3000")
}
```

## Handlers

```go
// Path parameters
func getUser(c *fiber.Ctx) error {
    id := c.Params("id")
    return c.JSON(fiber.Map{"id": id})
}

// Query parameters
func listUsers(c *fiber.Ctx) error {
    page := c.QueryInt("page", 1)
    limit := c.QueryInt("limit", 10)
    search := c.Query("search", "")
    
    return c.JSON(fiber.Map{
        "page":   page,
        "limit":  limit,
        "search": search,
    })
}

// Request body
type CreateUserRequest struct {
    Name  string `json:"name" validate:"required"`
    Email string `json:"email" validate:"required,email"`
}

func createUser(c *fiber.Ctx) error {
    req := new(CreateUserRequest)
    if err := c.BodyParser(req); err != nil {
        return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
            "error": err.Error(),
        })
    }
    
    return c.Status(fiber.StatusCreated).JSON(req)
}

// Headers
func handler(c *fiber.Ctx) error {
    auth := c.Get("Authorization")
    c.Set("X-Custom-Header", "value")
    return c.SendString("OK")
}
```

## Route Groups

```go
func main() {
    app := fiber.New()

    // API group
    api := app.Group("/api")
    
    // Version groups
    v1 := api.Group("/v1")
    v1.Get("/users", listUsersV1)
    
    v2 := api.Group("/v2")
    v2.Get("/users", listUsersV2)

    // Group with middleware
    admin := api.Group("/admin", authMiddleware)
    admin.Get("/stats", getStats)
    admin.Post("/config", updateConfig)

    app.Listen(":3000")
}
```

## Middleware

```go
import (
    "github.com/gofiber/fiber/v2"
    "github.com/gofiber/fiber/v2/middleware/logger"
    "github.com/gofiber/fiber/v2/middleware/recover"
    "github.com/gofiber/fiber/v2/middleware/cors"
    "github.com/gofiber/fiber/v2/middleware/limiter"
)

func main() {
    app := fiber.New()

    // Built-in middleware
    app.Use(recover.New())
    app.Use(logger.New())
    app.Use(cors.New(cors.Config{
        AllowOrigins: "https://example.com",
        AllowMethods: "GET,POST,PUT,DELETE",
    }))
    
    // Rate limiter
    app.Use(limiter.New(limiter.Config{
        Max:        100,
        Expiration: 1 * time.Minute,
    }))

    // Custom middleware
    app.Use(func(c *fiber.Ctx) error {
        start := time.Now()
        
        err := c.Next()
        
        duration := time.Since(start)
        c.Set("X-Response-Time", duration.String())
        
        return err
    })
}
```

## Error Handling

```go
func main() {
    app := fiber.New(fiber.Config{
        ErrorHandler: func(c *fiber.Ctx, err error) error {
            code := fiber.StatusInternalServerError
            
            if e, ok := err.(*fiber.Error); ok {
                code = e.Code
            }
            
            return c.Status(code).JSON(fiber.Map{
                "error": err.Error(),
            })
        },
    })

    app.Get("/user/:id", func(c *fiber.Ctx) error {
        id := c.Params("id")
        user, err := findUser(id)
        if err != nil {
            return fiber.NewError(fiber.StatusNotFound, "User not found")
        }
        return c.JSON(user)
    })
}
```

## Static Files and Templates

```go
// Static files
app.Static("/", "./public")
app.Static("/static", "./assets")

// Templates
app := fiber.New(fiber.Config{
    Views: html.New("./views", ".html"),
})

app.Get("/", func(c *fiber.Ctx) error {
    return c.Render("index", fiber.Map{
        "Title": "Hello, World!",
    })
})
```
