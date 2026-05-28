# Exercise 16: Observability

**Time:** 15 minutes
**Goal:** Add structured logging and Prometheus metrics

## The Spring Boot Version

```java
// logging with SLF4J
@Slf4j
@Service
public class UserService {
    public User findById(String id) {
        log.info("Finding user {}", id);
        // ...
    }
}

// metrics with Micrometer
@Autowired
MeterRegistry registry;

Counter requestCounter = registry.counter("api.requests", "endpoint", "/users");
requestCounter.increment();
```

## The Go Way

Use `log/slog` for structured logging and `prometheus/client_golang` for metrics:

```go
logger.Info("finding user", "id", id, "source", "api")

requestsTotal.WithLabelValues("/users", "GET").Inc()
```

---

## Step by Step

### 1. Setup structured logging (4 min)

Create `internal/logger/logger.go`:

```go
package logger

import (
    "log/slog"
    "os"
)

type Config struct {
    Level  string // debug, info, warn, error
    Format string // json, text
}

func New(cfg Config) *slog.Logger {
    var level slog.Level
    switch cfg.Level {
    case "debug":
        level = slog.LevelDebug
    case "warn":
        level = slog.LevelWarn
    case "error":
        level = slog.LevelError
    default:
        level = slog.LevelInfo
    }

    opts := &slog.HandlerOptions{Level: level}

    var handler slog.Handler
    if cfg.Format == "json" {
        handler = slog.NewJSONHandler(os.Stdout, opts)
    } else {
        handler = slog.NewTextHandler(os.Stdout, opts)
    }

    return slog.New(handler)
}

// WithRequestID adds request ID to logger
func WithRequestID(logger *slog.Logger, requestID string) *slog.Logger {
    return logger.With("request_id", requestID)
}
```

### 2. Add logging to handlers (3 min)

```go
func (h *TaskHandler) GetByID(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    id := chi.URLParam(r, "id")

    h.logger.Info("getting task",
        "task_id", id,
        "method", r.Method,
        "path", r.URL.Path,
    )

    task, err := h.service.GetByID(ctx, id)
    if err != nil {
        h.logger.Error("failed to get task",
            "task_id", id,
            "error", err,
        )
        // handle error...
        return
    }

    h.logger.Debug("task retrieved",
        "task_id", id,
        "task_title", task.Title,
    )

    WriteJSON(w, http.StatusOK, task)
}
```

### 3. Setup Prometheus metrics (4 min)

Add dependency:
```bash
go get github.com/prometheus/client_golang/prometheus
go get github.com/prometheus/client_golang/prometheus/promhttp
```

Create `internal/metrics/metrics.go`:

```go
package metrics

import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    RequestsTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "path", "status"},
    )

    RequestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "path"},
    )

    TasksCreated = promauto.NewCounter(
        prometheus.CounterOpts{
            Name: "tasks_created_total",
            Help: "Total number of tasks created",
        },
    )

    ActiveTasks = promauto.NewGauge(
        prometheus.GaugeOpts{
            Name: "tasks_active",
            Help: "Number of active (incomplete) tasks",
        },
    )
)
```

### 4. Create metrics middleware (4 min)

Create `internal/middleware/metrics.go`:

```go
package middleware

import (
    "net/http"
    "strconv"
    "time"

    "github.com/go-chi/chi/v5"

    "my-first-go-app/internal/metrics"
)

type statusRecorder struct {
    http.ResponseWriter
    status int
}

func (r *statusRecorder) WriteHeader(status int) {
    r.status = status
    r.ResponseWriter.WriteHeader(status)
}

func Metrics(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        recorder := &statusRecorder{ResponseWriter: w, status: http.StatusOK}

        next.ServeHTTP(recorder, r)

        // get route pattern for consistent labels
        routePattern := chi.RouteContext(r.Context()).RoutePattern()
        if routePattern == "" {
            routePattern = r.URL.Path
        }

        duration := time.Since(start).Seconds()

        metrics.RequestsTotal.WithLabelValues(
            r.Method,
            routePattern,
            strconv.Itoa(recorder.status),
        ).Inc()

        metrics.RequestDuration.WithLabelValues(
            r.Method,
            routePattern,
        ).Observe(duration)
    })
}
```

### 5. Expose metrics endpoint

In `cmd/server/main.go`:

```go
import "github.com/prometheus/client_golang/prometheus/promhttp"

// add metrics endpoint
r.Handle("/metrics", promhttp.Handler())

// use metrics middleware
r.Use(middleware.Metrics)
```

### Test it

```bash
# make some requests
curl http://localhost:8080/api/tasks
curl http://localhost:8080/api/tasks/123

# view metrics
curl http://localhost:8080/metrics | grep http_requests
```

## Log Levels

| Level | Use For |
|-------|---------|
| Debug | Development details, verbose tracing |
| Info | Normal operations, significant events |
| Warn | Recoverable problems, deprecations |
| Error | Failures requiring attention |

## Metric Types

| Type | Use For | Example |
|------|---------|---------|
| Counter | Totals (always increases) | requests_total |
| Gauge | Current value (can go up/down) | active_connections |
| Histogram | Distributions (latency, size) | request_duration |

## What Just Happened?

| Spring Boot | Go |
|-------------|-----|
| @Slf4j + Logback | log/slog |
| MDC for context | slog.With() |
| Micrometer | prometheus/client_golang |
| Spring Actuator /metrics | promhttp.Handler() |

## Checkpoint

- [ ] Structured logging with slog
- [ ] Request logging with context
- [ ] Prometheus metrics exposed
- [ ] Metrics middleware tracks requests

**Next:** Exercise 17 - Graceful Shutdown
