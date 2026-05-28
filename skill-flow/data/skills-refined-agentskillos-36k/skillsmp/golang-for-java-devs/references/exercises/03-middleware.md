# Exercise 03: Middleware

**Time:** 15 minutes
**Goal:** Create Chi middleware for cross-cutting concerns

## The Spring Boot Version

```java
@Component
public class LoggingFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {
        long start = System.currentTimeMillis();

        chain.doFilter(request, response);

        long duration = System.currentTimeMillis() - start;
        log.info("{} {} - {}ms", request.getMethod(), request.getRequestURI(), duration);
    }
}
```

## The Go Way

Chi middleware is a function that wraps a handler:

```go
func LoggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        next.ServeHTTP(w, r)

        duration := time.Since(start)
        log.Printf("%s %s - %v", r.Method, r.URL.Path, duration)
    })
}
```

## Your Task

Create three middleware:
1. **Request ID** - adds unique ID to each request
2. **Logging** - logs request method, path, duration
3. **Auth** - checks for API key header

---

## Step by Step

### 1. Create Request ID Middleware (4 min)

Create `internal/middleware/requestid.go`:

```go
package middleware

import (
    "context"
    "net/http"

    "github.com/google/uuid"
)

type contextKey string

const RequestIDKey contextKey = "requestID"

func RequestID(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        requestID := r.Header.Get("X-Request-ID")
        if requestID == "" {
            requestID = uuid.New().String()
        }

        // add to context
        ctx := context.WithValue(r.Context(), RequestIDKey, requestID)

        // add to response header
        w.Header().Set("X-Request-ID", requestID)

        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// helper to get request ID from context
func GetRequestID(ctx context.Context) string {
    if id, ok := ctx.Value(RequestIDKey).(string); ok {
        return id
    }
    return ""
}
```

### 2. Create Logging Middleware (4 min)

Create `internal/middleware/logging.go`:

```go
package middleware

import (
    "log/slog"
    "net/http"
    "time"
)

// responseWriter wraps http.ResponseWriter to capture status code
type responseWriter struct {
    http.ResponseWriter
    status int
}

func (rw *responseWriter) WriteHeader(code int) {
    rw.status = code
    rw.ResponseWriter.WriteHeader(code)
}

func Logging(logger *slog.Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()

            // wrap response writer to capture status
            wrapped := &responseWriter{ResponseWriter: w, status: http.StatusOK}

            next.ServeHTTP(wrapped, r)

            logger.Info("request",
                "method", r.Method,
                "path", r.URL.Path,
                "status", wrapped.status,
                "duration", time.Since(start),
                "request_id", GetRequestID(r.Context()),
            )
        })
    }
}
```

### 3. Create Auth Middleware (4 min)

Create `internal/middleware/auth.go`:

```go
package middleware

import (
    "net/http"
)

func APIKeyAuth(validKey string) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            key := r.Header.Get("X-API-Key")

            if key == "" {
                http.Error(w, "missing API key", http.StatusUnauthorized)
                return
            }

            if key != validKey {
                http.Error(w, "invalid API key", http.StatusUnauthorized)
                return
            }

            next.ServeHTTP(w, r)
        })
    }
}
```

### 4. Apply Middleware (3 min)

In `cmd/server/main.go`:

```go
package main

import (
    "log"
    "log/slog"
    "net/http"
    "os"

    "github.com/go-chi/chi/v5"

    "my-first-go-app/internal/handler"
    "my-first-go-app/internal/middleware"
)

func main() {
    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

    r := chi.NewRouter()

    // global middleware (applies to all routes)
    r.Use(middleware.RequestID)
    r.Use(middleware.Logging(logger))

    // public routes
    r.Get("/api/hello", handler.Hello)

    // protected routes
    r.Group(func(r chi.Router) {
        r.Use(middleware.APIKeyAuth("secret-key"))

        userHandler := handler.NewUserHandler()
        r.Post("/api/users", userHandler.Create)
    })

    log.Println("starting server on :8080")
    log.Fatal(http.ListenAndServe(":8080", r))
}
```

### 5. Test it

```bash
# public route - no auth needed
curl http://localhost:8080/api/hello

# protected route - missing key
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"John","age":25}'
# returns 401

# protected route - with key
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -H "X-API-Key: secret-key" \
  -d '{"email":"test@example.com","name":"John","age":25}'
# returns 201
```

## Middleware Pattern

```go
func MyMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // BEFORE: runs before handler
        // - check auth
        // - add request ID
        // - start timer

        next.ServeHTTP(w, r)

        // AFTER: runs after handler
        // - log duration
        // - record metrics
    })
}
```

## Middleware with Dependencies

```go
// middleware that needs config or services
func RateLimiter(limiter *rate.Limiter) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            if !limiter.Allow() {
                http.Error(w, "rate limit exceeded", http.StatusTooManyRequests)
                return
            }
            next.ServeHTTP(w, r)
        })
    }
}
```

## Built-in Chi Middleware

Chi includes useful middleware:

```go
import "github.com/go-chi/chi/v5/middleware"

r.Use(middleware.Logger)      // basic request logging
r.Use(middleware.Recoverer)   // recover from panics
r.Use(middleware.RealIP)      // extract real IP from headers
r.Use(middleware.Timeout(60 * time.Second))  // request timeout
r.Use(middleware.Compress(5)) // gzip compression
```

## What Just Happened?

| Spring Boot | Go (Chi) |
|-------------|----------|
| `@Component` Filter | `func(http.Handler) http.Handler` |
| `@Order` annotation | Order of `r.Use()` calls |
| FilterChain.doFilter | `next.ServeHTTP(w, r)` |
| HttpServletRequest attributes | `context.WithValue` |
| SecurityFilterChain | Route groups with middleware |

## Checkpoint

- [ ] Request ID middleware adds ID to context and response
- [ ] Logging middleware logs request details
- [ ] Auth middleware protects routes
- [ ] I understand middleware chaining

**Next:** Exercise 04 - Dependency Injection
