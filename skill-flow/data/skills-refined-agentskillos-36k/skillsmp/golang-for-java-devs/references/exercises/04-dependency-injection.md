# Exercise 04: Dependency Injection

**Time:** 15 minutes
**Goal:** Wire dependencies manually using constructor pattern

## The Spring Boot Version

```java
@Service
public class UserService {
    private final UserRepository repo;

    // Spring auto-injects
    public UserService(UserRepository repo) {
        this.repo = repo;
    }
}

@RestController
public class UserController {
    private final UserService service;

    public UserController(UserService service) {
        this.service = service;
    }
}
```

Spring scans for `@Service`, `@Repository`, etc. and wires everything automatically.

## The Go Way

No framework magic. Wire dependencies manually in `main()`:

```go
func main() {
    // create dependencies bottom-up
    repo := NewUserRepository(db)
    service := NewUserService(repo)
    handler := NewUserHandler(service)

    // route to handler
    r.Post("/users", handler.Create)
}
```

## Your Task

Create a proper layered architecture:
1. Repository layer (data access)
2. Service layer (business logic)
3. Handler layer (HTTP handling)

Wire them together in main().

---

## Step by Step

### 1. Create the Repository (4 min)

Create `internal/repository/user.go`:

```go
package repository

import (
    "context"
    "errors"
    "sync"
)

var ErrNotFound = errors.New("not found")

type User struct {
    ID    string
    Email string
    Name  string
    Age   int
}

type UserRepository struct {
    mu    sync.RWMutex
    users map[string]*User
}

func NewUserRepository() *UserRepository {
    return &UserRepository{
        users: make(map[string]*User),
    }
}

func (r *UserRepository) FindByID(ctx context.Context, id string) (*User, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    user, ok := r.users[id]
    if !ok {
        return nil, ErrNotFound
    }
    return user, nil
}

func (r *UserRepository) Save(ctx context.Context, user *User) error {
    r.mu.Lock()
    defer r.mu.Unlock()

    r.users[user.ID] = user
    return nil
}

func (r *UserRepository) FindAll(ctx context.Context) ([]*User, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    users := make([]*User, 0, len(r.users))
    for _, u := range r.users {
        users = append(users, u)
    }
    return users, nil
}
```

### 2. Create the Service (4 min)

Create `internal/service/user.go`:

```go
package service

import (
    "context"
    "errors"

    "github.com/google/uuid"

    "my-first-go-app/internal/repository"
)

var ErrUserNotFound = errors.New("user not found")

type UserService struct {
    repo *repository.UserRepository
}

func NewUserService(repo *repository.UserRepository) *UserService {
    return &UserService{repo: repo}
}

type CreateUserInput struct {
    Email string
    Name  string
    Age   int
}

func (s *UserService) Create(ctx context.Context, input CreateUserInput) (*repository.User, error) {
    user := &repository.User{
        ID:    uuid.New().String(),
        Email: input.Email,
        Name:  input.Name,
        Age:   input.Age,
    }

    if err := s.repo.Save(ctx, user); err != nil {
        return nil, err
    }

    return user, nil
}

func (s *UserService) GetByID(ctx context.Context, id string) (*repository.User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        if errors.Is(err, repository.ErrNotFound) {
            return nil, ErrUserNotFound
        }
        return nil, err
    }
    return user, nil
}

func (s *UserService) List(ctx context.Context) ([]*repository.User, error) {
    return s.repo.FindAll(ctx)
}
```

### 3. Update the Handler (4 min)

Update `internal/handler/user.go`:

```go
package handler

import (
    "encoding/json"
    "errors"
    "net/http"

    "github.com/go-chi/chi/v5"
    "github.com/go-playground/validator/v10"

    "my-first-go-app/internal/service"
)

type UserHandler struct {
    service  *service.UserService
    validate *validator.Validate
}

func NewUserHandler(svc *service.UserService) *UserHandler {
    return &UserHandler{
        service:  svc,
        validate: validator.New(),
    }
}

type CreateUserRequest struct {
    Email string `json:"email" validate:"required,email"`
    Name  string `json:"name" validate:"required,min=2,max=100"`
    Age   int    `json:"age" validate:"gte=0,lte=150"`
}

func (h *UserHandler) Create(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid json", http.StatusBadRequest)
        return
    }

    if err := h.validate.Struct(req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    user, err := h.service.Create(r.Context(), service.CreateUserInput{
        Email: req.Email,
        Name:  req.Name,
        Age:   req.Age,
    })
    if err != nil {
        http.Error(w, "failed to create user", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}

func (h *UserHandler) GetByID(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")

    user, err := h.service.GetByID(r.Context(), id)
    if err != nil {
        if errors.Is(err, service.ErrUserNotFound) {
            http.Error(w, "user not found", http.StatusNotFound)
            return
        }
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}

func (h *UserHandler) List(w http.ResponseWriter, r *http.Request) {
    users, err := h.service.List(r.Context())
    if err != nil {
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(users)
}
```

### 4. Wire Everything in main() (3 min)

Update `cmd/server/main.go`:

```go
package main

import (
    "log"
    "net/http"

    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"

    "my-first-go-app/internal/handler"
    "my-first-go-app/internal/repository"
    "my-first-go-app/internal/service"
)

func main() {
    // create dependencies (bottom-up)
    userRepo := repository.NewUserRepository()
    userService := service.NewUserService(userRepo)
    userHandler := handler.NewUserHandler(userService)

    // setup router
    r := chi.NewRouter()
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)

    // routes
    r.Route("/api/users", func(r chi.Router) {
        r.Post("/", userHandler.Create)
        r.Get("/", userHandler.List)
        r.Get("/{id}", userHandler.GetByID)
    })

    log.Println("starting server on :8080")
    log.Fatal(http.ListenAndServe(":8080", r))
}
```

### 5. Test it

```bash
# create user
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"John","age":25}'

# list users
curl http://localhost:8080/api/users

# get user by ID (use ID from create response)
curl http://localhost:8080/api/users/<id>
```

## Why Manual Wiring?

| Spring DI | Go Manual Wiring |
|-----------|------------------|
| Automatic component scanning | Explicit in main() |
| `@Autowired` magic | Constructor arguments |
| Runtime errors for missing beans | Compile-time errors |
| Hidden dependency graph | Visible dependency graph |

Benefits of manual wiring:
- You can see exactly what depends on what
- No reflection or runtime magic
- Compile-time safety
- Easy to understand for new team members

## When to Use DI Frameworks

For large applications, consider:
- [Wire](https://github.com/google/wire) - compile-time DI
- [Fx](https://github.com/uber-go/fx) - runtime DI

But start with manual wiring - it's often sufficient.

## Checkpoint

- [ ] Repository handles data access
- [ ] Service contains business logic
- [ ] Handler handles HTTP
- [ ] Dependencies are wired in main()

**Next:** Exercise 05 - Configuration
