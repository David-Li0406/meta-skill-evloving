---
name: go-web-framework
description: Use this skill when you need to set up a high-performance web application in Go using a minimalist framework.
---

# Skill body

## Application Setup

```go
package main

import (
    "github.com/labstack/echo/v4" // or "github.com/gin-gonic/gin" for Gin
    "github.com/labstack/echo/v4/middleware" // for Echo
    // "github.com/gin-gonic/gin" // for Gin
)

func main() {
    e := echo.New() // or r := gin.Default() for Gin

    // Middleware
    e.Use(middleware.Logger()) // for Echo
    e.Use(middleware.Recover()) // for Echo
    // r.Use(gin.Logger()) // for Gin
    // r.Use(gin.Recovery()) // for Gin

    // Routes
    e.GET("/", homeHandler) // or r.GET("/ping", pingHandler) for Gin
    e.POST("/users", createUser)

    // Route groups
    api := e.Group("/api/v1")
    api.GET("/users", listUsers)
    api.GET("/users/:id", getUser)

    e.Logger.Fatal(e.Start(":8080")) // or r.Run(":8080") for Gin
}
```

## Handlers

```go
// Path parameters
func getUser(c echo.Context) error { // or func getUser(c *gin.Context) for Gin
    id := c.Param("id")
    user, err := findUser(id)
    if err != nil {
        return echo.NewHTTPError(404, "User not found") // or c.JSON(404, gin.H{"error": "User not found"}) for Gin
    }
    return c.JSON(200, user) // or c.JSON(200, user) for Gin
}

// Query parameters
func listUsers(c echo.Context) error { // or func listUsers(c *gin.Context) for Gin
    page := c.QueryParam("page")
    limit := c.QueryParam("limit")
    users := fetchUsers(page, limit)
    return c.JSON(200, users) // or c.JSON(200, users) for Gin
}

// JSON body binding
type CreateUserRequest struct {
    Name  string `json:"name" validate:"required"` // or binding:"required" for Gin
    Email string `json:"email" validate:"required,email"` // or binding:"required,email" for Gin
}

func createUser(c echo.Context) error { // or func createUser(c *gin.Context) for Gin
    var req CreateUserRequest
    if err := c.Bind(&req); err != nil { // or c.ShouldBindJSON(&req) for Gin
        return echo.NewHTTPError(400, err.Error()) // or c.JSON(400, gin.H{"error": err.Error()}) for Gin
    }
    user := insertUser(req)
    return c.JSON(201, user) // or c.JSON(201, user) for Gin
}
```

## Middleware

```go
// Built-in middleware
e.Use(middleware.CORS()) // for Echo
// r.Use(corsMiddleware()) // for Gin

// Custom middleware example
func authMiddleware() gin.HandlerFunc { // for Gin
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        // Implement token validation logic
    }
}
```