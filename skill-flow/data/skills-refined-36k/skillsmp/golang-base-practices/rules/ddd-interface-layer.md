---
title: Interface Layer Design
impact: HIGH
impactDescription: External interaction entry point
tags: ddd, interface, http, grpc
---

## Interface Layer Design

The interface layer handles external requests and converts them to application layer commands/queries.

**HTTP Handler:**

```go
// internal/interfaces/http/handler/user.go
package handler

import (
    "net/http"
    "strconv"
    "myapp/internal/application/user"
    "github.com/gin-gonic/gin"
)

type UserHandler struct {
    userHandler *user.Handler
}

func NewUserHandler(uh *user.Handler) *UserHandler {
    return &UserHandler{userHandler: uh}
}

// Request/Response DTOs (separate from domain entities)
type CreateUserRequest struct {
    Email string `json:"email" binding:"required,email"`
    Name  string `json:"name" binding:"required,min=2,max=100"`
}

type UserResponse struct {
    ID     uint64 `json:"id"`
    Email  string `json:"email"`
    Name   string `json:"name"`
    Status string `json:"status"`
}

func (h *UserHandler) Create(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    u, err := h.userHandler.CreateUser(c.Request.Context(), user.CreateUserCommand{
        Email: req.Email,
        Name:  req.Name,
    })
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusCreated, h.toResponse(u))
}

func (h *UserHandler) Get(c *gin.Context) {
    id, err := strconv.ParseUint(c.Param("id"), 10, 64)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "invalid id"})
        return
    }

    u, err := h.userHandler.GetUser(c.Request.Context(), user.GetUserQuery{ID: id})
    if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
        return
    }

    c.JSON(http.StatusOK, h.toResponse(u))
}

func (h *UserHandler) toResponse(u *domain.User) UserResponse {
    return UserResponse{
        ID:     u.ID,
        Email:  u.Email,
        Name:   u.Name,
        Status: string(u.Status),
    }
}
```

**Router Registration:**

```go
// internal/interfaces/http/router.go
func SetupRouter(userHandler *handler.UserHandler) *gin.Engine {
    r := gin.Default()

    api := r.Group("/api/v1")
    {
        users := api.Group("/users")
        users.POST("", userHandler.Create)
        users.GET("/:id", userHandler.Get)
    }

    return r
}
```
