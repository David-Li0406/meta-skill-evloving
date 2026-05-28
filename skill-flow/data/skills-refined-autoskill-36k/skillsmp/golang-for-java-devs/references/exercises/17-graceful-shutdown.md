# Exercise 17: Graceful Shutdown

**Time:** 15 minutes
**Goal:** Handle shutdown signals and drain connections gracefully

## The Spring Boot Version

```java
// Spring handles this automatically
// Or configure shutdown timeout
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=30s
```

## The Go Way

Manually handle OS signals and shutdown the server:

```go
// listen for shutdown signals
quit := make(chan os.Signal, 1)
signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

// block until signal received
<-quit

// shutdown with timeout
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()
server.Shutdown(ctx)
```

---

## Step by Step

### 1. Basic signal handling (4 min)

Update `cmd/server/main.go`:

```go
package main

import (
    "context"
    "log/slog"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

    // setup router...
    r := setupRouter()

    server := &http.Server{
        Addr:         ":8080",
        Handler:      r,
        ReadTimeout:  5 * time.Second,
        WriteTimeout: 10 * time.Second,
        IdleTimeout:  120 * time.Second,
    }

    // channel for shutdown signals
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

    // start server in goroutine
    go func() {
        logger.Info("starting server", "addr", server.Addr)
        if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            logger.Error("server error", "error", err)
            os.Exit(1)
        }
    }()

    // block until signal
    sig := <-quit
    logger.Info("shutdown signal received", "signal", sig)

    // graceful shutdown with timeout
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := server.Shutdown(ctx); err != nil {
        logger.Error("server shutdown error", "error", err)
        os.Exit(1)
    }

    logger.Info("server stopped gracefully")
}
```

### 2. Add cleanup for other resources (4 min)

```go
func main() {
    // ... setup code ...

    // connect to database
    db, err := database.Connect(cfg)
    if err != nil {
        logger.Error("database connection failed", "error", err)
        os.Exit(1)
    }

    // start server...

    // wait for shutdown signal
    <-quit
    logger.Info("shutting down...")

    // create shutdown context
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    // shutdown in order
    logger.Info("stopping HTTP server...")
    if err := server.Shutdown(ctx); err != nil {
        logger.Error("HTTP shutdown error", "error", err)
    }

    logger.Info("closing database connection...")
    if err := db.Close(); err != nil {
        logger.Error("database close error", "error", err)
    }

    logger.Info("shutdown complete")
}
```

### 3. Create a graceful server wrapper (5 min)

Create `internal/server/server.go`:

```go
package server

import (
    "context"
    "log/slog"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
)

type Server struct {
    httpServer *http.Server
    logger     *slog.Logger
    cleanup    []func(context.Context) error
}

func New(addr string, handler http.Handler, logger *slog.Logger) *Server {
    return &Server{
        httpServer: &http.Server{
            Addr:         addr,
            Handler:      handler,
            ReadTimeout:  5 * time.Second,
            WriteTimeout: 10 * time.Second,
            IdleTimeout:  120 * time.Second,
        },
        logger: logger,
    }
}

// OnShutdown registers cleanup functions
func (s *Server) OnShutdown(fn func(context.Context) error) {
    s.cleanup = append(s.cleanup, fn)
}

// Run starts the server and blocks until shutdown
func (s *Server) Run() error {
    // signal channel
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

    // error channel for server
    errChan := make(chan error, 1)

    // start server
    go func() {
        s.logger.Info("starting server", "addr", s.httpServer.Addr)
        if err := s.httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            errChan <- err
        }
    }()

    // wait for signal or error
    select {
    case err := <-errChan:
        return err
    case sig := <-quit:
        s.logger.Info("shutdown signal received", "signal", sig)
    }

    // graceful shutdown
    return s.shutdown()
}

func (s *Server) shutdown() error {
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    // shutdown HTTP server
    s.logger.Info("stopping HTTP server...")
    if err := s.httpServer.Shutdown(ctx); err != nil {
        s.logger.Error("HTTP shutdown error", "error", err)
    }

    // run cleanup functions
    for _, fn := range s.cleanup {
        if err := fn(ctx); err != nil {
            s.logger.Error("cleanup error", "error", err)
        }
    }

    s.logger.Info("shutdown complete")
    return nil
}
```

### 4. Use the server wrapper (2 min)

```go
func main() {
    // setup...

    db, _ := database.Connect(cfg)

    srv := server.New(":8080", r, logger)

    // register cleanup
    srv.OnShutdown(func(ctx context.Context) error {
        logger.Info("closing database...")
        return db.Close()
    })

    if err := srv.Run(); err != nil {
        logger.Error("server error", "error", err)
        os.Exit(1)
    }
}
```

## Testing Graceful Shutdown

```bash
# start server
go run ./cmd/server &

# send SIGTERM
kill -TERM $!

# or press Ctrl+C for SIGINT
```

## What Happens During Shutdown

1. Signal received (SIGINT/SIGTERM)
2. Stop accepting new connections
3. Wait for in-flight requests to complete (up to timeout)
4. Close database connections
5. Release other resources
6. Exit

## Health Check for Load Balancers

```go
// health endpoint that reflects shutdown state
var isShuttingDown atomic.Bool

r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
    if isShuttingDown.Load() {
        w.WriteHeader(http.StatusServiceUnavailable)
        w.Write([]byte("shutting down"))
        return
    }
    w.Write([]byte("ok"))
})

// set during shutdown
isShuttingDown.Store(true)
// wait a bit for LB to remove from rotation
time.Sleep(5 * time.Second)
// then shutdown
```

## What Just Happened?

| Spring Boot | Go |
|-------------|-----|
| Auto graceful shutdown | Manual signal handling |
| @PreDestroy hooks | OnShutdown callbacks |
| Shutdown timeout config | context.WithTimeout |

## Checkpoint

- [ ] Server handles SIGINT and SIGTERM
- [ ] In-flight requests complete before shutdown
- [ ] Database connections closed properly
- [ ] Shutdown has a timeout

**Next:** Exercise 18 - Integration Testing
