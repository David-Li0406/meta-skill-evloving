---
title: Graceful Server Shutdown
impact: HIGH
impactDescription: Prevent request loss
tags: framework, shutdown, signal
---

## Graceful Server Shutdown

Services must support graceful shutdown to ensure in-flight requests complete before exit.

**Incorrect (immediate exit):**

```go
func main() {
    r := gin.Default()
    r.GET("/", handler)
    r.Run(":8080") // Exits immediately on signal, requests interrupted
}
```

**Correct (graceful shutdown):**

```go
func main() {
    r := gin.Default()
    r.GET("/", handler)

    srv := &http.Server{
        Addr:    ":8080",
        Handler: r,
    }

    // Start server
    go func() {
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("listen: %s\n", err)
        }
    }()

    // Wait for interrupt signal
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit
    log.Println("Shutting down server...")

    // Graceful shutdown with 5 second timeout
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        log.Fatal("Server forced to shutdown:", err)
    }

    log.Println("Server exiting")
}
```

**Key Points:**
- Catch SIGINT and SIGTERM signals
- Use `http.Server.Shutdown` for graceful shutdown
- Set timeout to avoid infinite waiting
- Ensure database connections and resources are properly released
