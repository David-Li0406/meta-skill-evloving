---
name: Zap Logging
description: Blazing fast structured logging from Uber.
metadata:
  labels: [golang, zap, logging, observability]
  triggers:
    files: ['**/logger.go', '**/main.go']
    keywords: [zap, Logger, SugaredLogger, zapcore]
---

# Zap Logging Standards

## Setup

```go
import "go.uber.org/zap"

// Development (human readable)
func NewDevelopmentLogger() *zap.Logger {
    logger, _ := zap.NewDevelopment()
    return logger
}

// Production (JSON, optimized)
func NewProductionLogger() *zap.Logger {
    logger, _ := zap.NewProduction()
    return logger
}

// With options
func NewLogger() *zap.Logger {
    cfg := zap.NewProductionConfig()
    cfg.Level = zap.NewAtomicLevelAt(zap.InfoLevel)
    cfg.OutputPaths = []string{"stdout", "/var/log/app.log"}
    cfg.EncoderConfig.TimeKey = "timestamp"
    cfg.EncoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder

    logger, _ := cfg.Build()
    return logger
}
```

## Logger vs SugaredLogger

```go
// Logger - faster, type-safe
logger := zap.NewProduction()
logger.Info("User logged in",
    zap.String("user_id", "123"),
    zap.Int("attempt", 1),
    zap.Duration("latency", time.Millisecond*50),
)

// SugaredLogger - convenient, slower
sugar := logger.Sugar()
sugar.Infow("User logged in",
    "user_id", "123",
    "attempt", 1,
    "latency", time.Millisecond*50,
)
sugar.Infof("User %s logged in", userID)
```

## Structured Fields

```go
logger.Info("Request completed",
    zap.String("method", "GET"),
    zap.String("path", "/users"),
    zap.Int("status", 200),
    zap.Duration("latency", latency),
    zap.String("client_ip", clientIP),
    zap.Any("headers", headers),     // Any type
    zap.Error(err),                   // Error field
    zap.Stack("stacktrace"),          // Stack trace
)

// Namespaced fields
logger.Info("Request",
    zap.Namespace("http"),
    zap.String("method", "GET"),
    zap.Int("status", 200),
)
// Output: {"http": {"method": "GET", "status": 200}}
```

## Log Levels

```go
logger.Debug("Debug message")   // -1
logger.Info("Info message")     // 0
logger.Warn("Warning message")  // 1
logger.Error("Error message")   // 2
logger.DPanic("DPanic message") // 3 (panics in development)
logger.Panic("Panic message")   // 4 (always panics)
logger.Fatal("Fatal message")   // 5 (calls os.Exit(1))

// Check level before expensive operations
if logger.Core().Enabled(zap.DebugLevel) {
    logger.Debug("Expensive", zap.Any("data", computeExpensiveData()))
}
```

## Child Loggers

```go
// Add fields to all subsequent logs
requestLogger := logger.With(
    zap.String("request_id", requestID),
    zap.String("user_id", userID),
)

requestLogger.Info("Processing request")
requestLogger.Info("Request completed")
// Both logs include request_id and user_id

// Named logger
dbLogger := logger.Named("database")
dbLogger.Info("Query executed")
// Output: {"logger": "database", "msg": "Query executed"}
```

## Gin Integration

```go
import (
    "github.com/gin-gonic/gin"
    "go.uber.org/zap"
)

func GinLogger(logger *zap.Logger) gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        path := c.Request.URL.Path

        c.Next()

        logger.Info("Request",
            zap.String("method", c.Request.Method),
            zap.String("path", path),
            zap.Int("status", c.Writer.Status()),
            zap.Duration("latency", time.Since(start)),
            zap.String("client_ip", c.ClientIP()),
        )
    }
}

r := gin.New()
r.Use(GinLogger(logger))
```

## Custom Encoder

```go
cfg := zap.NewProductionConfig()
cfg.EncoderConfig = zapcore.EncoderConfig{
    TimeKey:        "ts",
    LevelKey:       "level",
    NameKey:        "logger",
    CallerKey:      "caller",
    MessageKey:     "msg",
    StacktraceKey:  "stacktrace",
    LineEnding:     zapcore.DefaultLineEnding,
    EncodeLevel:    zapcore.LowercaseLevelEncoder,
    EncodeTime:     zapcore.ISO8601TimeEncoder,
    EncodeDuration: zapcore.MillisDurationEncoder,
    EncodeCaller:   zapcore.ShortCallerEncoder,
}
```

## Sampling

```go
// Sample logs to reduce volume in production
cfg := zap.NewProductionConfig()
cfg.Sampling = &zap.SamplingConfig{
    Initial:    100,  // First 100 per second logged
    Thereafter: 100,  // Then every 100th message
}
```

## Global Logger

```go
// Replace global logger
logger := zap.NewProduction()
zap.ReplaceGlobals(logger)

// Use global
zap.L().Info("Using global logger")
zap.S().Infow("Using global sugar")

// Always sync before exit
defer logger.Sync()
```

## Best Practices

1. **Production**: Use `zap.NewProduction()` for JSON output
2. **Sync**: Always call `logger.Sync()` before exit
3. **Fields**: Prefer `zap.String()` etc. over SugaredLogger
4. **Child loggers**: Add request context with `With()`
5. **Sampling**: Enable in high-throughput production
