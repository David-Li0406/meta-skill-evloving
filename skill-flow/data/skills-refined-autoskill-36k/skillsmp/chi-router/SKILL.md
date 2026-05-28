---
name: Chi Router
description: Lightweight, composable Go HTTP router built on net/http.
metadata:
  labels: [golang, chi, router, http]
  triggers:
    files: ['**/main.go', '**/routes.go']
    keywords: [chi, chi.NewRouter, chi.Router, r.Route]
---

# Chi Router Standards

## Router Setup

```go
package main

import (
    "net/http"
    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"
)

func main() {
    r := chi.NewRouter()

    // Middleware
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    r.Use(middleware.RequestID)
    r.Use(middleware.RealIP)

    // Routes
    r.Get("/", homeHandler)
    r.Get("/users/{id}", getUser)
    r.Post("/users", createUser)

    // Sub-routers
    r.Route("/api/v1", func(r chi.Router) {
        r.Get("/items", listItems)
        r.Post("/items", createItem)
    })

    http.ListenAndServe(":8080", r)
}
```

## Handlers

```go
// Path parameters
func getUser(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    user, err := findUser(id)
    if err != nil {
        http.Error(w, "Not found", http.StatusNotFound)
        return
    }
    json.NewEncoder(w).Encode(user)
}

// Query parameters
func listUsers(w http.ResponseWriter, r *http.Request) {
    page := r.URL.Query().Get("page")
    limit := r.URL.Query().Get("limit")
    users := fetchUsers(page, limit)
    json.NewEncoder(w).Encode(users)
}

// JSON body
func createUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    user := insertUser(req)
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}
```

## Middleware

```go
// Built-in middleware
r.Use(middleware.Logger)          // Logs requests
r.Use(middleware.Recoverer)       // Panic recovery
r.Use(middleware.RequestID)       // Request ID header
r.Use(middleware.RealIP)          // Real IP from headers
r.Use(middleware.Compress(5))     // Gzip compression
r.Use(middleware.Timeout(60 * time.Second))

// Custom middleware
func authMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if token == "" {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }

        user, err := validateToken(token)
        if err != nil {
            http.Error(w, "Invalid token", http.StatusUnauthorized)
            return
        }

        ctx := context.WithValue(r.Context(), "user", user)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// Apply to group
r.Route("/api", func(r chi.Router) {
    r.Use(authMiddleware)
    r.Get("/protected", protectedHandler)
})
```

## Route Groups & Nesting

```go
r.Route("/api/v1", func(r chi.Router) {
    // All routes here prefixed with /api/v1

    r.Route("/users", func(r chi.Router) {
        r.Get("/", listUsers)
        r.Post("/", createUser)

        r.Route("/{id}", func(r chi.Router) {
            r.Get("/", getUser)
            r.Put("/", updateUser)
            r.Delete("/", deleteUser)
        })
    })

    r.Route("/items", func(r chi.Router) {
        r.Get("/", listItems)
    })
})
```

## Mount Sub-Routers

```go
func main() {
    r := chi.NewRouter()
    r.Mount("/api/v1", apiRouter())
    r.Mount("/admin", adminRouter())
    http.ListenAndServe(":8080", r)
}

func apiRouter() chi.Router {
    r := chi.NewRouter()
    r.Get("/users", listUsers)
    r.Post("/users", createUser)
    return r
}

func adminRouter() chi.Router {
    r := chi.NewRouter()
    r.Use(adminAuthMiddleware)
    r.Get("/stats", getStats)
    return r
}
```

## Context Values

```go
// Set in middleware
ctx := context.WithValue(r.Context(), "user", user)
next.ServeHTTP(w, r.WithContext(ctx))

// Get in handler
user := r.Context().Value("user").(*User)

// Type-safe context keys
type contextKey string
const userKey contextKey = "user"

ctx := context.WithValue(r.Context(), userKey, user)
user := r.Context().Value(userKey).(*User)
```

## Response Helpers

```go
import "github.com/go-chi/render"

type UserResponse struct {
    ID    int    `json:"id"`
    Name  string `json:"name"`
}

func (u *UserResponse) Render(w http.ResponseWriter, r *http.Request) error {
    return nil
}

func getUser(w http.ResponseWriter, r *http.Request) {
    user := &UserResponse{ID: 1, Name: "John"}
    render.Render(w, r, user)
}

// Error response
func ErrNotFound(w http.ResponseWriter, r *http.Request, err error) {
    render.Status(r, http.StatusNotFound)
    render.JSON(w, r, map[string]string{"error": err.Error()})
}
```

## Best Practices

1. **Standard library**: Chi uses net/http, fully compatible with standard handlers
2. **Composition**: Use `r.Route()` for grouping, `r.Mount()` for sub-routers
3. **Middleware order**: Apply in order of execution (outer to inner)
4. **Context**: Use typed keys for context values
5. **Testing**: Use `httptest` - Chi handlers are standard `http.Handler`
