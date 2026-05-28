# Exercise 01: Your First Go Endpoint

**Time:** 15 minutes
**Goal:** Get a Go app running with one endpoint using Chi router

## Prerequisites (First Time Only)

### Verify Your Environment

```bash
go version    # expect: go1.21 or higher
```

If Go is missing:
- macOS: `brew install go`
- Or download from https://go.dev/dl/

### Project Setup

**Option A: Use the template** (recommended for first time)

```bash
cp -r ~/.claude/skills/golang-for-java-devs/template/go-starter ./my-first-go-app
cd my-first-go-app
go mod tidy
go run ./cmd/server
```

**Option B: Start from scratch**

```bash
mkdir my-first-go-app && cd my-first-go-app
go mod init my-first-go-app
go get github.com/go-chi/chi/v5
```

---

## The Spring Boot Version

```java
@RestController
@RequestMapping("/api")
public class HelloController {

    @GetMapping("/hello")
    public HelloResponse hello() {
        return new HelloResponse("Hello from Spring Boot");
    }
}

public record HelloResponse(String message) {}
```

## Your Task

Create a Go equivalent that:
1. Runs on port 8080
2. Has a GET endpoint at `/api/hello`
3. Returns JSON: `{"message": "Hello from Go"}`

## Try First (Optional)

Before looking at the solution, try writing:
- A struct for the response
- A handler function
- Router setup with Chi

---

## Step by Step

### 1. Create the Response Struct (2 min)

Create `internal/handler/hello.go`:

```go
package handler

type HelloResponse struct {
    Message string `json:"message"`
}
```

Note the struct tag - it controls JSON field name (lowercase).

### 2. Create the Handler (5 min)

Add to `internal/handler/hello.go`:

```go
package handler

import (
    "encoding/json"
    "net/http"
)

type HelloResponse struct {
    Message string `json:"message"`
}

func Hello(w http.ResponseWriter, r *http.Request) {
    response := HelloResponse{
        Message: "Hello from Go",
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}
```

### 3. Set Up the Router (5 min)

Create or edit `cmd/server/main.go`:

```go
package main

import (
    "log"
    "net/http"

    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"

    "my-first-go-app/internal/handler"
)

func main() {
    r := chi.NewRouter()

    // middleware
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)

    // routes
    r.Get("/api/hello", handler.Hello)

    log.Println("starting server on :8080")
    log.Fatal(http.ListenAndServe(":8080", r))
}
```

### 4. Run It (3 min)

```bash
go run ./cmd/server
```

Test:
```bash
curl http://localhost:8080/api/hello
```

Expected output:
```json
{"message":"Hello from Go"}
```

## What Just Happened?

| Spring Boot | Go (Chi) |
|-------------|----------|
| `@RestController` | Handler function |
| `@GetMapping("/path")` | `r.Get("/path", handler)` |
| Return object -> auto JSON | `json.NewEncoder(w).Encode(obj)` |
| Embedded Tomcat | `http.ListenAndServe` |
| Auto component scanning | Explicit route registration |

Go did very little behind the scenes:
- Chi router matched the path
- Your handler wrote the response
- stdlib's net/http served it

## Common Mistakes

**Wrong package structure:**
```
my-app/
    main.go           // bad: everything in one file
```

**Better:**
```
my-app/
    cmd/server/main.go     // entry point
    internal/handler/      // handlers
    internal/service/      // business logic
```

**Forgetting Content-Type:**
```go
// bad: no content type
json.NewEncoder(w).Encode(response)

// good: set content type
w.Header().Set("Content-Type", "application/json")
json.NewEncoder(w).Encode(response)
```

## Stretch Goal

Add a second endpoint `/api/hello/{name}` that returns `"Hello, {name}"`:

```go
func HelloName(w http.ResponseWriter, r *http.Request) {
    name := chi.URLParam(r, "name")

    response := HelloResponse{
        Message: fmt.Sprintf("Hello, %s", name),
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

// in main.go
r.Get("/api/hello/{name}", handler.HelloName)
```

## Checkpoint

- [ ] App runs without errors
- [ ] `/api/hello` returns JSON
- [ ] I understand how Chi routing works
- [ ] I can create a struct with JSON tags

**Next:** Exercise 02 - Adding Validation
