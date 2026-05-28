---
id: go-standard-layout
name: "Project Structure"
domain: GO
skill: faion-software-developer
category: "backend"
---

## Project Structure

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

### Agent

faion-backend-agent
