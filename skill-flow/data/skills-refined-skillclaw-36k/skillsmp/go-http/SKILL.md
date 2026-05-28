---
name: go-http
description: >
  HTTP handler, module, middleware, and routing patterns. Use when implementing
  endpoints, modules, middleware, routes, or HTTP responses. Includes module
  pattern for mountable sub-applications and path normalization at router level.
  Triggers: http.Handler, http.HandlerFunc, Handler struct, Routes() method,
  routes.Group, routes.Route, module.Module, module.Router, middleware stack,
  RespondJSON, RespondError, CORS, SSE, text/event-stream, MapHTTPStatus,
  long-running processes, lifecycle context, client disconnect, path normalization.
  File patterns: internal/*/handler.go, pkg/module/*.go, pkg/middleware/*.go, pkg/routes/*.go
---

# Go HTTP Patterns

## When This Skill Applies

- Implementing HTTP handlers
- Creating route groups
- Creating mountable modules
- Adding middleware
- Building SSE streaming endpoints
- Handling request/response patterns
- Understanding path normalization

## Principles

### 1. Handler Struct Pattern

Each domain has a Handler struct with a Routes() method:

```go
type Handler struct {
    sys        System
    logger     *slog.Logger
    pagination pagination.Config
}

func NewHandler(sys System, logger *slog.Logger, pagination pagination.Config) *Handler {
    return &Handler{
        sys:        sys,
        logger:     logger,
        pagination: pagination,
    }
}

func (h *Handler) Routes() routes.Group {
    return routes.Group{
        Prefix:      "/providers",  // API module adds /api prefix
        Tags:        []string{"Providers"},
        Description: "Provider configuration management",
        Routes: []routes.Route{
            {Method: "GET", Pattern: "", Handler: h.List, OpenAPI: Spec.List},
            {Method: "POST", Pattern: "", Handler: h.Create, OpenAPI: Spec.Create},
            {Method: "GET", Pattern: "/{id}", Handler: h.Find, OpenAPI: Spec.Find},
            {Method: "PUT", Pattern: "/{id}", Handler: h.Update, OpenAPI: Spec.Update},
            {Method: "DELETE", Pattern: "/{id}", Handler: h.Delete, OpenAPI: Spec.Delete},
        },
    }
}
```

### 2. Route Structures

```go
type Group struct {
    Prefix      string
    Tags        []string
    Description string
    Routes      []Route
    Children    []Group  // Nested route groups
}

type Route struct {
    Method  string
    Pattern string
    Handler http.HandlerFunc
    OpenAPI *openapi.Operation  // Optional OpenAPI metadata
}
```

**Hierarchical Routes** - Child groups inherit parent prefix:
```go
routes.Group{
    Prefix: "/workflows",  // API module adds /api prefix
    Routes: []routes.Route{
        {Method: "GET", Pattern: "", Handler: h.ListWorkflows},
        {Method: "POST", Pattern: "/{name}/execute", Handler: h.Execute},
    },
    Children: []routes.Group{
        {
            Prefix: "/runs",  // Results in /workflows/runs (then /api/workflows/runs with module prefix)
            Routes: []routes.Route{
                {Method: "GET", Pattern: "/{id}", Handler: h.FindRun},
            },
        },
    },
}
```

### 3. Response Helpers

```go
// RespondJSON writes a JSON response with status code
handlers.RespondJSON(w, http.StatusOK, data)

// RespondError logs the error and writes a JSON error response
handlers.RespondError(w, h.logger, http.StatusBadRequest, err)
```

**Handler Pattern**:
```go
func (h *Handler) Create(w http.ResponseWriter, r *http.Request) {
    var cmd CreateCommand
    if err := json.NewDecoder(r.Body).Decode(&cmd); err != nil {
        handlers.RespondError(w, h.logger, http.StatusBadRequest, err)
        return
    }

    result, err := h.sys.Create(r.Context(), cmd)
    if err != nil {
        handlers.RespondError(w, h.logger, MapHTTPStatus(err), err)
        return
    }

    handlers.RespondJSON(w, http.StatusCreated, result)
}
```

### 4. Error Status Mapping

Each domain defines a MapHTTPStatus function:

```go
func MapHTTPStatus(err error) int {
    switch {
    case errors.Is(err, ErrNotFound):
        return http.StatusNotFound
    case errors.Is(err, ErrDuplicate):
        return http.StatusConflict
    case errors.Is(err, ErrInvalidConfig):
        return http.StatusBadRequest
    default:
        return http.StatusInternalServerError
    }
}
```

### 5. Module Pattern

Modules are isolated HTTP sub-applications with their own middleware chains. Each module is mounted at a single-level path prefix.

```go
// pkg/module/module.go
type Module struct {
    prefix     string
    router     http.Handler
    middleware middleware.System
}

func New(prefix string, router http.Handler) *Module
func (m *Module) Use(mw func(http.Handler) http.Handler)
func (m *Module) Handler() http.Handler
func (m *Module) Prefix() string
func (m *Module) Serve(w http.ResponseWriter, req *http.Request)
```

**Creating a Module**:
```go
func NewModule(cfg *config.Config, infra *runtime.Infrastructure) (*module.Module, error) {
    runtime := NewRuntime(cfg, infra)
    domain := NewDomain(runtime)

    mux := http.NewServeMux()
    registerRoutes(mux, spec, domain, cfg)

    m := module.New("/api", mux)
    m.Use(middleware.CORS(&cfg.API.CORS))
    m.Use(middleware.Logger(runtime.Logger))

    return m, nil
}
```

**Module Router** routes requests to mounted modules:
```go
router := module.NewRouter()
router.Mount(apiModule)
router.Mount(appModule)
router.HandleNative("GET /health", healthHandler)
```

### 6. Path Normalization

Path normalization happens at the router level, not via redirect middleware. The router strips trailing slashes before routing:

```go
func (r *Router) ServeHTTP(w http.ResponseWriter, req *http.Request) {
    path := normalizePath(req)  // Strips trailing slash
    prefix := extractPrefix(path)

    if m, ok := r.modules[prefix]; ok {
        m.Serve(w, req)
        return
    }
    r.native.ServeHTTP(w, req)
}

func normalizePath(req *http.Request) string {
    path := req.URL.Path
    if len(path) > 1 && strings.HasSuffix(path, "/") {
        path = strings.TrimSuffix(path, "/")
        req.URL.Path = path  // Mutates request in place
    }
    return path
}
```

**Key Points**:
- No HTTP redirects for trailing slashes
- Path is normalized before module routing
- Modules receive paths without trailing slashes
- Native handlers registered separately from modules

### 7. Logger Middleware

```go
func Logger(logger *slog.Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            next.ServeHTTP(w, r)
            logger.Info("request",
                "method", r.Method,
                "uri", r.URL.RequestURI(),
                "addr", r.RemoteAddr,
                "duration", time.Since(start))
        })
    }
}
```

### 8. SSE Streaming Pattern

Server-Sent Events for streaming responses:

```go
func (h *Handler) writeSSEStream(w http.ResponseWriter, r *http.Request, stream <-chan *response.StreamingChunk) {
    w.Header().Set("Content-Type", "text/event-stream")
    w.Header().Set("Cache-Control", "no-cache")
    w.Header().Set("Connection", "keep-alive")
    w.WriteHeader(http.StatusOK)

    if f, ok := w.(http.Flusher); ok {
        f.Flush()
    }

    for chunk := range stream {
        data, _ := json.Marshal(chunk)
        fmt.Fprintf(w, "data: %s\n\n", data)

        if f, ok := w.(http.Flusher); ok {
            f.Flush()
        }
    }

    fmt.Fprintf(w, "data: [DONE]\n\n")
    if f, ok := w.(http.Flusher); ok {
        f.Flush()
    }
}
```

**Key Points**:
- `text/event-stream` content type
- Each chunk prefixed with `data: ` and followed by `\n\n`
- Flush after each chunk for real-time delivery
- Check context cancellation for client disconnect
- Final `[DONE]` marker signals stream completion

## Patterns

### URL Parameter Extraction

```go
func (h *Handler) Find(w http.ResponseWriter, r *http.Request) {
    idStr := r.PathValue("id")
    id, err := uuid.Parse(idStr)
    if err != nil {
        handlers.RespondError(w, h.logger, http.StatusBadRequest, err)
        return
    }
    // ...
}
```

### Pagination from Query

```go
func (h *Handler) List(w http.ResponseWriter, r *http.Request) {
    page := pagination.PageRequestFromQuery(r.URL.Query(), h.pagination)
    filters := FiltersFromQuery(r.URL.Query())

    result, err := h.sys.List(r.Context(), page, filters)
    // ...
}
```

## Anti-Patterns

### Reaching Up for Dependencies

```go
// Bad: Handler reaches up to app for dependencies
type Handler struct {
    app *Application
}

func (h *Handler) Create(w http.ResponseWriter, r *http.Request) {
    sys := h.app.Providers()  // Reaching up
}

// Good: Dependencies injected via constructor
type Handler struct {
    sys    System
    logger *slog.Logger
}
```

### Inline Error Responses

```go
// Bad: Inconsistent error format
w.WriteHeader(http.StatusBadRequest)
w.Write([]byte("bad request"))

// Good: Use helpers for consistent format
handlers.RespondError(w, h.logger, http.StatusBadRequest, err)
```

### HTTP Context for Long-Running Processes

```go
// Bad: Process tied to HTTP request context
// Client disconnect cancels the entire operation
func (h *Handler) Execute(w http.ResponseWriter, r *http.Request) {
    result, err := h.sys.Execute(r.Context(), params)  // Cancelled if client disconnects
}

// Good: Use lifecycle context for long-running processes
// Process survives client disconnect, respects server shutdown
func (h *Handler) Execute(w http.ResponseWriter, r *http.Request) {
    ctx := h.runtime.Lifecycle().Context()  // Server lifecycle, not HTTP request

    events, run, err := h.sys.Execute(ctx, params)
    if err != nil {
        handlers.RespondError(w, h.logger, MapHTTPStatus(err), err)
        return
    }

    // Stream events, checking for client disconnect
    h.writeSSEStream(w, r, events)
}

func (h *Handler) writeSSEStream(w http.ResponseWriter, r *http.Request, events <-chan Event) {
    // ... set headers, write status ...

    for event := range events {
        select {
        case <-r.Context().Done():
            return  // Client disconnected, stop streaming (process continues)
        default:
        }

        data, _ := json.Marshal(event)
        fmt.Fprintf(w, "data: %s\n\n", data)
        // ... flush ...
    }
}
```

**Behavior Matrix**:

| Scenario | HTTP Context | Lifecycle Context |
|----------|--------------|-------------------|
| Client disconnects | Process cancelled | Process continues |
| Cancel endpoint called | No effect | Process cancelled |
| Server shutdown | Process cancelled | Process cancelled |

Use lifecycle context when:
- Process should complete regardless of client connection
- Results are persisted (database, storage)
- Process has its own cancellation mechanism (cancel endpoint)
