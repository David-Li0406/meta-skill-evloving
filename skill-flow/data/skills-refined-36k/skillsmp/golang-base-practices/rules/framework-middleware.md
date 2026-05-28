---
title: Middleware Design Patterns
impact: HIGH
impactDescription: Reusable cross-cutting concerns
tags: framework, middleware, pattern
---

## Middleware Design Patterns

Use middleware pattern to handle cross-cutting concerns like logging, authentication, and rate limiting.

**Incorrect (repeated code):**

```go
func GetUser(c *gin.Context) {
    // Logging repeated in every handler
    log.Printf("request: %s %s", c.Request.Method, c.Request.URL)
    start := time.Now()

    // Token validation repeated in every handler
    token := c.GetHeader("Authorization")
    if token == "" {
        c.JSON(401, gin.H{"error": "unauthorized"})
        return
    }

    // Business logic...

    log.Printf("duration: %v", time.Since(start))
}
```

**Correct (middleware abstraction):**

```go
// Logger middleware
func Logger() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        path := c.Request.URL.Path

        c.Next()

        log.Printf("%s %s %d %v",
            c.Request.Method,
            path,
            c.Writer.Status(),
            time.Since(start),
        )
    }
}

// Auth middleware
func Auth() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.AbortWithStatusJSON(401, gin.H{"error": "unauthorized"})
            return
        }

        claims, err := validateToken(token)
        if err != nil {
            c.AbortWithStatusJSON(401, gin.H{"error": "invalid token"})
            return
        }

        c.Set("user_id", claims.UserID)
        c.Next()
    }
}

func main() {
    r := gin.New()
    r.Use(Logger(), Recovery())

    api := r.Group("/api", Auth())
    {
        api.GET("/users/:id", GetUser)
    }
}
```
