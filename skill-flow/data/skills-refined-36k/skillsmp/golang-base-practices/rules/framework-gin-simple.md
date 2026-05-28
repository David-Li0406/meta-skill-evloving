---
title: Use Gin for Simple Projects
impact: CRITICAL
impactDescription: Quick setup, suitable for small to medium projects
tags: framework, gin, http, api
---

## Use Gin for Simple Projects

For small to medium projects, simple REST APIs, or rapid prototyping, prefer the Gin framework.

**Incorrect (over-engineering a small project):**

```go
// Using a full microservice framework for a simple CRUD API
import (
    "github.com/go-kratos/kratos/v2"
    "github.com/go-kratos/kratos/v2/transport/grpc"
    "github.com/go-kratos/kratos/v2/transport/http"
)

func main() {
    // Lots of configuration code...
    app := kratos.New(
        kratos.Name("simple-api"),
        kratos.Server(grpcServer, httpServer),
    )
}
```

**Correct (use Gin for simple projects):**

```go
package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()

    r.GET("/users/:id", getUser)
    r.POST("/users", createUser)
    r.PUT("/users/:id", updateUser)
    r.DELETE("/users/:id", deleteUser)

    r.Run(":8080")
}

func getUser(c *gin.Context) {
    id := c.Param("id")
    c.JSON(http.StatusOK, gin.H{"id": id})
}
```

**Selection Criteria:**
- Monolith or simple microservice → Gin
- Team with limited Go experience → Gin (gentle learning curve)
- Rapid prototype validation → Gin
- No gRPC requirement → Gin
