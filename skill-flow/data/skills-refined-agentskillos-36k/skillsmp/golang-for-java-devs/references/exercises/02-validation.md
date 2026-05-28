# Exercise 02: Request Validation

**Time:** 15 minutes
**Goal:** Validate incoming requests using go-playground/validator

## The Spring Boot Version

```java
public record CreateUserRequest(
    @NotNull @Email String email,
    @NotBlank @Size(min = 2, max = 100) String name,
    @Min(0) @Max(150) Integer age
) {}

@PostMapping("/users")
public User createUser(@Valid @RequestBody CreateUserRequest request) {
    // if we reach here, request is already validated
    return userService.create(request);
}
```

Spring automatically returns 400 with validation errors.

## The Go Way

Go doesn't have annotation-based validation. We use struct tags with a validation library.

```go
type CreateUserRequest struct {
    Email string `json:"email" validate:"required,email"`
    Name  string `json:"name" validate:"required,min=2,max=100"`
    Age   int    `json:"age" validate:"gte=0,lte=150"`
}
```

## Your Task

1. Create a POST endpoint `/api/users`
2. Accept JSON body with email, name, and age
3. Validate the request
4. Return 400 with error details if invalid
5. Return 201 with the user if valid

---

## Step by Step

### 1. Add the validator dependency (1 min)

```bash
go get github.com/go-playground/validator/v10
```

### 2. Create the request struct (3 min)

Create `internal/handler/user.go`:

```go
package handler

import (
    "encoding/json"
    "net/http"

    "github.com/go-playground/validator/v10"
)

type CreateUserRequest struct {
    Email string `json:"email" validate:"required,email"`
    Name  string `json:"name" validate:"required,min=2,max=100"`
    Age   int    `json:"age" validate:"gte=0,lte=150"`
}

type User struct {
    ID    string `json:"id"`
    Email string `json:"email"`
    Name  string `json:"name"`
    Age   int    `json:"age"`
}
```

### 3. Create the handler struct with validator (4 min)

```go
type UserHandler struct {
    validate *validator.Validate
}

func NewUserHandler() *UserHandler {
    return &UserHandler{
        validate: validator.New(),
    }
}
```

### 4. Implement the create handler (5 min)

```go
func (h *UserHandler) Create(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest

    // decode json body
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid json", http.StatusBadRequest)
        return
    }

    // validate
    if err := h.validate.Struct(req); err != nil {
        validationErrors := err.(validator.ValidationErrors)
        errors := make(map[string]string)
        for _, e := range validationErrors {
            errors[e.Field()] = e.Tag()
        }

        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusBadRequest)
        json.NewEncoder(w).Encode(map[string]interface{}{
            "errors": errors,
        })
        return
    }

    // create user (for now, just echo back with ID)
    user := User{
        ID:    "123",  // would be generated
        Email: req.Email,
        Name:  req.Name,
        Age:   req.Age,
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}
```

### 5. Register the route (2 min)

In `cmd/server/main.go`:

```go
userHandler := handler.NewUserHandler()
r.Post("/api/users", userHandler.Create)
```

### 6. Test it

```bash
# valid request
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"John","age":25}'

# invalid request
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"email":"not-an-email","name":"J","age":200}'
```

## Common Validation Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `required` | Field must be present | `validate:"required"` |
| `email` | Must be valid email | `validate:"email"` |
| `min` | Minimum length/value | `validate:"min=2"` |
| `max` | Maximum length/value | `validate:"max=100"` |
| `gte` | Greater than or equal | `validate:"gte=0"` |
| `lte` | Less than or equal | `validate:"lte=150"` |
| `oneof` | Must be one of values | `validate:"oneof=active inactive"` |
| `url` | Must be valid URL | `validate:"url"` |
| `uuid` | Must be valid UUID | `validate:"uuid"` |

## Custom Validation

```go
func (h *UserHandler) init() {
    h.validate.RegisterValidation("notadmin", func(fl validator.FieldLevel) bool {
        return fl.Field().String() != "admin"
    })
}

type CreateUserRequest struct {
    Username string `json:"username" validate:"required,notadmin"`
}
```

## Better Error Messages

```go
func formatValidationErrors(err error) map[string]string {
    errors := make(map[string]string)

    for _, e := range err.(validator.ValidationErrors) {
        field := strings.ToLower(e.Field())
        switch e.Tag() {
        case "required":
            errors[field] = fmt.Sprintf("%s is required", field)
        case "email":
            errors[field] = "must be a valid email address"
        case "min":
            errors[field] = fmt.Sprintf("must be at least %s characters", e.Param())
        case "max":
            errors[field] = fmt.Sprintf("must be at most %s characters", e.Param())
        default:
            errors[field] = fmt.Sprintf("failed %s validation", e.Tag())
        }
    }

    return errors
}
```

## What Just Happened?

| Spring Boot | Go |
|-------------|-----|
| `@Valid` annotation | `validator.Struct(req)` |
| Jakarta annotations | Struct tags |
| Auto 400 response | Manual response writing |
| Global exception handler | Handler-level error handling |

Go's approach is more explicit but gives you full control over error formatting.

## Checkpoint

- [ ] POST endpoint accepts JSON body
- [ ] Invalid requests return 400 with errors
- [ ] Valid requests return 201 with user
- [ ] I understand validation struct tags

**Next:** Exercise 03 - Middleware
