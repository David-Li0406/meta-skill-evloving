# Chi Routing Patterns

## Basic Setup

```go
import (
    "net/http"
    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"
)

func main() {
    r := chi.NewRouter()

    // Built-in middleware
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    r.Use(middleware.RequestID)

    // Routes
    r.Get("/", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("Hello World!"))
    })

    r.Get("/users/{id}", getUser)
    r.Post("/users", createUser)

    http.ListenAndServe(":3000", r)
}
```

## Handlers

```go
import (
    "encoding/json"
    "net/http"
    "github.com/go-chi/chi/v5"
)

func getUser(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    
    user := User{ID: id, Name: "John"}
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}

func createUser(w http.ResponseWriter, r *http.Request) {
    var user User
    if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}
```

## Route Groups

```go
func main() {
    r := chi.NewRouter()

    // API routes
    r.Route("/api", func(r chi.Router) {
        r.Use(apiMiddleware)
        
        r.Route("/v1", func(r chi.Router) {
            r.Get("/users", listUsersV1)
            r.Post("/users", createUserV1)
            
            r.Route("/users/{id}", func(r chi.Router) {
                r.Get("/", getUser)
                r.Put("/", updateUser)
                r.Delete("/", deleteUser)
            })
        })
    })

    // Admin routes with auth
    r.Group(func(r chi.Router) {
        r.Use(authMiddleware)
        r.Get("/admin/stats", getStats)
    })
}
```

## Subrouters

```go
// users.go
func UsersRouter() chi.Router {
    r := chi.NewRouter()
    
    r.Get("/", listUsers)
    r.Post("/", createUser)
    r.Get("/{id}", getUser)
    r.Put("/{id}", updateUser)
    r.Delete("/{id}", deleteUser)
    
    return r
}

// orders.go
func OrdersRouter() chi.Router {
    r := chi.NewRouter()
    r.Get("/", listOrders)
    r.Post("/", createOrder)
    return r
}

// main.go
func main() {
    r := chi.NewRouter()
    
    r.Mount("/users", UsersRouter())
    r.Mount("/orders", OrdersRouter())
    
    http.ListenAndServe(":3000", r)
}
```

## Middleware

```go
// Custom middleware
func AuthMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if token == "" {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }
        
        // Validate token, add user to context
        ctx := context.WithValue(r.Context(), "user", userID)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// Request-scoped middleware
func UserCtx(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        id := chi.URLParam(r, "id")
        user, err := findUser(id)
        if err != nil {
            http.Error(w, "Not Found", http.StatusNotFound)
            return
        }
        ctx := context.WithValue(r.Context(), "user", user)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// Usage
r.Route("/users/{id}", func(r chi.Router) {
    r.Use(UserCtx)
    r.Get("/", getUser)    // User available in context
    r.Put("/", updateUser)
})
```

## Built-in Middleware

```go
import "github.com/go-chi/chi/v5/middleware"

r.Use(middleware.RequestID)       // X-Request-ID header
r.Use(middleware.RealIP)          // X-Real-IP, X-Forwarded-For
r.Use(middleware.Logger)          // Request logging
r.Use(middleware.Recoverer)       // Panic recovery
r.Use(middleware.Timeout(60 * time.Second))
r.Use(middleware.Throttle(100))   // Rate limiting
r.Use(middleware.Compress(5))     // Gzip compression
r.Use(middleware.AllowContentType("application/json"))
```

## Pattern Matching

```go
// Basic pattern
r.Get("/users/{id}", handler)

// Regex constraint
r.Get("/articles/{date:\\d{4}-\\d{2}-\\d{2}}", handler)

// Catch-all
r.Get("/files/*", handler) // r.URL.Path contains full path

// Not found handler
r.NotFound(func(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusNotFound)
    w.Write([]byte("Not found"))
})

// Method not allowed
r.MethodNotAllowed(func(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusMethodNotAllowed)
    w.Write([]byte("Method not allowed"))
})
```
