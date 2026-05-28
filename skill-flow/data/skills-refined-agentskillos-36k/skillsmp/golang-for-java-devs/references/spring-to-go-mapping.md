# Spring Boot to Go Concept Mapping

Quick reference for translating Spring Boot patterns to Go equivalents using Chi router.

## HTTP Handling

### Basic Endpoint

**Spring Boot:**
```java
@RestController
@RequestMapping("/users")
public class UserController {

    @GetMapping("/{id}")
    public User getUser(@PathVariable String id) {
        return userService.findById(id);
    }
}
```

**Go (Chi):**
```go
func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    user, err := h.service.FindByID(r.Context(), id)
    if err != nil {
        http.Error(w, err.Error(), http.StatusNotFound)
        return
    }
    json.NewEncoder(w).Encode(user)
}

// registration
r.Get("/users/{id}", handler.GetUser)
```

Key differences:
- Explicit routing registration
- Manual JSON encoding
- Error handling inline, not via exceptions

### Request/Response Bodies

**Spring Boot:**
```java
@PostMapping
public User createUser(@RequestBody @Valid CreateUserRequest req) {
    return userService.create(req);
}
```

**Go:**
```go
func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid request body", http.StatusBadRequest)
        return
    }

    if err := h.validator.Struct(req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    user, err := h.service.Create(r.Context(), &req)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}
```

Key differences:
- Manual JSON decoding
- Explicit validation call
- Explicit status codes

## Middleware (Filters)

**Spring Boot Filter:**
```java
@Component
public class LoggingFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) {
        log.info("Request: {} {}", request.getMethod(), request.getRequestURI());
        chain.doFilter(request, response);
    }
}
```

**Go (Chi Middleware):**
```go
func LoggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        log.Printf("Request: %s %s", r.Method, r.URL.Path)
        next.ServeHTTP(w, r)
    })
}

// registration
r.Use(LoggingMiddleware)
```

Key differences:
- Middleware is just a function wrapping a handler
- No annotations, explicit registration

## Dependency Injection

**Spring Boot (automatic):**
```java
@Service
public class UserService {
    private final UserRepository userRepo;

    public UserService(UserRepository userRepo) {  // auto-injected
        this.userRepo = userRepo;
    }
}
```

**Go (manual):**
```go
type UserService struct {
    repo UserRepository
}

func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}

// in main.go
func main() {
    db := connectDB()
    repo := NewUserRepository(db)
    service := NewUserService(repo)
    handler := NewUserHandler(service)

    r := chi.NewRouter()
    r.Get("/users/{id}", handler.GetUser)
    http.ListenAndServe(":8080", r)
}
```

Key differences:
- No framework - wire dependencies yourself
- Constructor functions return concrete types
- main() is the composition root

## Error Handling

**Spring Boot:**
```java
// in service
public User findById(String id) {
    return repo.findById(id)
        .orElseThrow(() -> new UserNotFoundException(id));
}

// global handler
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(UserNotFoundException ex) {
        return new ErrorResponse(ex.getMessage());
    }
}
```

**Go:**
```go
// sentinel errors
var ErrNotFound = errors.New("not found")

// in service
func (s *UserService) FindByID(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            return nil, fmt.Errorf("user %s: %w", id, ErrNotFound)
        }
        return nil, fmt.Errorf("finding user: %w", err)
    }
    return user, nil
}

// in handler
func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    user, err := h.service.FindByID(r.Context(), chi.URLParam(r, "id"))
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            http.Error(w, err.Error(), http.StatusNotFound)
            return
        }
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(user)
}
```

Key differences:
- No exceptions - errors are values
- Error handling at each layer
- errors.Is for type checking

## Configuration

**Spring Boot:**
```yaml
# application.yml
server:
  port: ${PORT:8080}

database:
  url: ${DATABASE_URL}
  max-connections: ${DB_MAX_CONN:10}
```

```java
@ConfigurationProperties(prefix = "database")
public record DatabaseConfig(String url, int maxConnections) {}
```

**Go:**
```go
type Config struct {
    Port           string `envconfig:"PORT" default:"8080"`
    DatabaseURL    string `envconfig:"DATABASE_URL" required:"true"`
    DBMaxConns     int    `envconfig:"DB_MAX_CONN" default:"10"`
}

func LoadConfig() (*Config, error) {
    var cfg Config
    if err := envconfig.Process("", &cfg); err != nil {
        return nil, err
    }
    return &cfg, nil
}
```

Key differences:
- No YAML files typically - environment variables are standard
- struct tags for configuration mapping

## Structs (Records/Classes)

**Java record:**
```java
public record User(
    String id,
    String email,
    Instant createdAt
) {}
```

**Go struct:**
```go
type User struct {
    ID        string    `json:"id"`
    Email     string    `json:"email"`
    CreatedAt time.Time `json:"created_at"`
}
```

Key differences:
- struct tags for JSON field names
- no automatic getters - fields are accessed directly

## Validation

**Spring Boot:**
```java
public record CreateUserRequest(
    @NotNull @Email String email,
    @NotBlank @Size(min = 2, max = 100) String name
) {}

@PostMapping
public User createUser(@Valid @RequestBody CreateUserRequest req) {
    // validated automatically
}
```

**Go (go-playground/validator):**
```go
type CreateUserRequest struct {
    Email string `json:"email" validate:"required,email"`
    Name  string `json:"name" validate:"required,min=2,max=100"`
}

func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid json", http.StatusBadRequest)
        return
    }

    if err := h.validator.Struct(req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    // ...
}
```

## Testing

**Spring Boot:**
```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockBean
    UserService userService;

    @Test
    void getUser_returnsUser() throws Exception {
        when(userService.findById("123")).thenReturn(new User("123", "test@example.com"));

        mockMvc.perform(get("/users/123"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.email").value("test@example.com"));
    }
}
```

**Go:**
```go
func TestGetUser(t *testing.T) {
    // setup mock
    mockService := &MockUserService{
        FindByIDFn: func(ctx context.Context, id string) (*User, error) {
            return &User{ID: "123", Email: "test@example.com"}, nil
        },
    }

    handler := NewUserHandler(mockService)

    // create request
    req := httptest.NewRequest("GET", "/users/123", nil)
    rctx := chi.NewRouteContext()
    rctx.URLParams.Add("id", "123")
    req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))

    // record response
    w := httptest.NewRecorder()

    // call handler
    handler.GetUser(w, req)

    // assert
    if w.Code != http.StatusOK {
        t.Errorf("expected status 200, got %d", w.Code)
    }

    var user User
    json.NewDecoder(w.Body).Decode(&user)
    if user.Email != "test@example.com" {
        t.Errorf("expected email test@example.com, got %s", user.Email)
    }
}
```

Key differences:
- httptest package from standard library
- manual mock implementation (or use mockgen)
- table-driven tests are idiomatic

## Quick Reference Table

| Spring Boot | Go Equivalent |
|-------------|---------------|
| @RestController | Chi router + handler struct |
| @GetMapping("/path") | r.Get("/path", handler) |
| @PostMapping | r.Post("/path", handler) |
| @PathVariable | chi.URLParam(r, "param") |
| @RequestParam | r.URL.Query().Get("param") |
| @RequestBody | json.NewDecoder(r.Body).Decode(&req) |
| @Valid | validator.Struct(req) |
| @Service | Regular struct + NewXxx constructor |
| @Repository | Regular struct + NewXxx constructor |
| @Autowired | Manual wiring in main() |
| @Component | Not needed - no scanning |
| OncePerRequestFilter | func(next http.Handler) http.Handler |
| @RestControllerAdvice | Error handling in handlers/middleware |
| @Transactional | Manual tx.Begin(), tx.Commit(), tx.Rollback() |
| @Async | go func() { ... }() |
| @Scheduled | time.Ticker or cron library |
| ResponseEntity<T> | w.WriteHeader(status) + json.Encode() |
| Optional<T> | *T (pointer can be nil) or (T, bool) |
| CompletableFuture | Channels and goroutines |
| @ConfigurationProperties | envconfig or viper |
| application.yml | Environment variables |
| Spring Actuator | Custom /health, /metrics endpoints |
| Lombok @Data | Not needed - structs are simple |
| Lombok @Builder | Functional options pattern |
