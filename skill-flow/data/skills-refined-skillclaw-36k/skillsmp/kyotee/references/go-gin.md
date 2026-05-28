# Kyotee: Go + Gin Patterns

Use these patterns when building REST APIs with Go and the Gin framework.

## Project Structure

```
cmd/
  server/
    main.go           # Entry point
internal/
  handlers/           # HTTP handlers
    user.go
    health.go
  services/           # Business logic
    user.go
  repositories/       # Data access
    user.go
  models/             # Data structures
    user.go
  middleware/         # Custom middleware
    auth.go
    logging.go
  config/             # Configuration
    config.go
pkg/                  # Shared utilities
  response/
    response.go
go.mod
go.sum
Makefile
```

## Naming Conventions

- **Files**: snake_case (`user_handler.go`)
- **Packages**: lowercase, short (`handlers`, `models`)
- **Structs/Interfaces**: PascalCase (`UserService`, `UserRepository`)
- **Functions**: PascalCase for exported, camelCase for private
- **Variables**: camelCase

## Main Entry Point

```go
// cmd/server/main.go
package main

import (
    "log"
    "myapp/internal/config"
    "myapp/internal/handlers"
    "myapp/internal/middleware"
    "github.com/gin-gonic/gin"
)

func main() {
    cfg := config.Load()

    r := gin.Default()

    // Middleware
    r.Use(middleware.Logger())
    r.Use(middleware.CORS())

    // Routes
    api := r.Group("/api/v1")
    {
        api.GET("/health", handlers.Health)

        users := api.Group("/users")
        {
            users.GET("", handlers.ListUsers)
            users.POST("", handlers.CreateUser)
            users.GET("/:id", handlers.GetUser)
            users.PUT("/:id", handlers.UpdateUser)
            users.DELETE("/:id", handlers.DeleteUser)
        }
    }

    log.Printf("Server starting on %s", cfg.Port)
    r.Run(":" + cfg.Port)
}
```

## Handler Pattern

```go
// internal/handlers/user.go
package handlers

import (
    "net/http"
    "myapp/internal/models"
    "myapp/internal/services"
    "myapp/pkg/response"
    "github.com/gin-gonic/gin"
)

type UserHandler struct {
    service *services.UserService
}

func NewUserHandler(s *services.UserService) *UserHandler {
    return &UserHandler{service: s}
}

func (h *UserHandler) List(c *gin.Context) {
    users, err := h.service.List(c.Request.Context())
    if err != nil {
        response.Error(c, http.StatusInternalServerError, err.Error())
        return
    }
    response.Success(c, users)
}

func (h *UserHandler) Create(c *gin.Context) {
    var input models.CreateUserInput
    if err := c.ShouldBindJSON(&input); err != nil {
        response.Error(c, http.StatusBadRequest, err.Error())
        return
    }

    user, err := h.service.Create(c.Request.Context(), input)
    if err != nil {
        response.Error(c, http.StatusInternalServerError, err.Error())
        return
    }
    response.Success(c, user)
}

func (h *UserHandler) Get(c *gin.Context) {
    id := c.Param("id")
    user, err := h.service.Get(c.Request.Context(), id)
    if err != nil {
        response.Error(c, http.StatusNotFound, "user not found")
        return
    }
    response.Success(c, user)
}
```

## Service Pattern

```go
// internal/services/user.go
package services

import (
    "context"
    "myapp/internal/models"
    "myapp/internal/repositories"
)

type UserService struct {
    repo *repositories.UserRepository
}

func NewUserService(r *repositories.UserRepository) *UserService {
    return &UserService{repo: r}
}

func (s *UserService) List(ctx context.Context) ([]models.User, error) {
    return s.repo.FindAll(ctx)
}

func (s *UserService) Create(ctx context.Context, input models.CreateUserInput) (*models.User, error) {
    user := &models.User{
        Name:  input.Name,
        Email: input.Email,
    }
    return s.repo.Create(ctx, user)
}

func (s *UserService) Get(ctx context.Context, id string) (*models.User, error) {
    return s.repo.FindByID(ctx, id)
}
```

## Repository Pattern

```go
// internal/repositories/user.go
package repositories

import (
    "context"
    "database/sql"
    "myapp/internal/models"
)

type UserRepository struct {
    db *sql.DB
}

func NewUserRepository(db *sql.DB) *UserRepository {
    return &UserRepository{db: db}
}

func (r *UserRepository) FindAll(ctx context.Context) ([]models.User, error) {
    rows, err := r.db.QueryContext(ctx, "SELECT id, name, email FROM users")
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var users []models.User
    for rows.Next() {
        var u models.User
        if err := rows.Scan(&u.ID, &u.Name, &u.Email); err != nil {
            return nil, err
        }
        users = append(users, u)
    }
    return users, nil
}

func (r *UserRepository) Create(ctx context.Context, user *models.User) (*models.User, error) {
    result, err := r.db.ExecContext(ctx,
        "INSERT INTO users (name, email) VALUES (?, ?)",
        user.Name, user.Email)
    if err != nil {
        return nil, err
    }
    id, _ := result.LastInsertId()
    user.ID = int(id)
    return user, nil
}
```

## Models

```go
// internal/models/user.go
package models

type User struct {
    ID    int    `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

type CreateUserInput struct {
    Name  string `json:"name" binding:"required"`
    Email string `json:"email" binding:"required,email"`
}

type UpdateUserInput struct {
    Name  string `json:"name"`
    Email string `json:"email" binding:"omitempty,email"`
}
```

## Response Helper

```go
// pkg/response/response.go
package response

import (
    "github.com/gin-gonic/gin"
)

type Response struct {
    Success bool        `json:"success"`
    Data    interface{} `json:"data,omitempty"`
    Error   string      `json:"error,omitempty"`
}

func Success(c *gin.Context, data interface{}) {
    c.JSON(200, Response{Success: true, Data: data})
}

func Error(c *gin.Context, code int, message string) {
    c.JSON(code, Response{Success: false, Error: message})
}
```

## Middleware

```go
// internal/middleware/logging.go
package middleware

import (
    "log"
    "time"
    "github.com/gin-gonic/gin"
)

func Logger() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        path := c.Request.URL.Path

        c.Next()

        log.Printf("%s %s %d %v",
            c.Request.Method,
            path,
            c.Writer.Status(),
            time.Since(start))
    }
}
```

## Config

```go
// internal/config/config.go
package config

import "os"

type Config struct {
    Port        string
    DatabaseURL string
}

func Load() *Config {
    return &Config{
        Port:        getEnv("PORT", "8080"),
        DatabaseURL: getEnv("DATABASE_URL", ""),
    }
}

func getEnv(key, fallback string) string {
    if v := os.Getenv(key); v != "" {
        return v
    }
    return fallback
}
```

## Makefile

```makefile
.PHONY: run build test

run:
	go run cmd/server/main.go

build:
	go build -o bin/server cmd/server/main.go

test:
	go test -v ./...

tidy:
	go mod tidy
```

## Tips

- **Dependency injection** - Pass dependencies through constructors
- **Context propagation** - Always pass context through the call chain
- **Error handling** - Return errors, don't panic
- **Validation** - Use Gin's binding tags for input validation
- **Middleware** - Use for cross-cutting concerns (logging, auth, CORS)
