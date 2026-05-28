---
id: go-http-handlers
name: "HTTP Handlers (Gin/Echo)"
domain: GO
skill: faion-software-developer
category: "backend"
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

### Agent

faion-backend-agent
