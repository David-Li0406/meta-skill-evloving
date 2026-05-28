# Zap Logger Configuration

## Basic Setup

```go
import "go.uber.org/zap"

func main() {
    // Development (human-readable, debug level)
    logger, _ := zap.NewDevelopment()
    defer logger.Sync()

    // Production (JSON, info level)
    logger, _ := zap.NewProduction()
    defer logger.Sync()

    // Example logger (for tests)
    logger := zap.NewExample()
}
```

## Standard Logger

```go
logger, _ := zap.NewProduction()

// Typed fields - fast, type-safe
logger.Info("user logged in",
    zap.String("user_id", "12345"),
    zap.Int("attempt", 1),
    zap.Duration("latency", time.Second),
    zap.Time("timestamp", time.Now()),
    zap.Any("metadata", map[string]string{"key": "value"}),
)

logger.Error("failed to process",
    zap.Error(err),
    zap.String("request_id", reqID),
)

// Log levels
logger.Debug("debug message")
logger.Info("info message")
logger.Warn("warning message")
logger.Error("error message")
logger.Fatal("fatal - calls os.Exit(1)")
logger.Panic("panic - calls panic()")
```

## Sugared Logger

```go
logger, _ := zap.NewProduction()
sugar := logger.Sugar()
defer sugar.Sync()

// Printf-style (slower but convenient)
sugar.Infof("user %s logged in", userID)
sugar.Errorw("failed to process",
    "error", err,
    "request_id", reqID,
)

// Key-value pairs
sugar.Infow("user action",
    "user_id", userID,
    "action", "login",
    "ip", clientIP,
)
```

## Custom Configuration

```go
config := zap.Config{
    Level:       zap.NewAtomicLevelAt(zap.InfoLevel),
    Development: false,
    Encoding:    "json", // or "console"
    EncoderConfig: zapcore.EncoderConfig{
        TimeKey:        "timestamp",
        LevelKey:       "level",
        NameKey:        "logger",
        CallerKey:      "caller",
        MessageKey:     "message",
        StacktraceKey:  "stacktrace",
        LineEnding:     zapcore.DefaultLineEnding,
        EncodeLevel:    zapcore.LowercaseLevelEncoder,
        EncodeTime:     zapcore.ISO8601TimeEncoder,
        EncodeDuration: zapcore.MillisDurationEncoder,
        EncodeCaller:   zapcore.ShortCallerEncoder,
    },
    OutputPaths:      []string{"stdout", "/var/log/app.log"},
    ErrorOutputPaths: []string{"stderr"},
}

logger, _ := config.Build()
```

## Child Loggers

```go
logger, _ := zap.NewProduction()

// Add fields to all subsequent logs
requestLogger := logger.With(
    zap.String("request_id", uuid.New().String()),
    zap.String("user_id", userID),
)

requestLogger.Info("processing request")
requestLogger.Info("request completed") // includes request_id and user_id
```

## Sampling (High-Volume)

```go
config := zap.NewProductionConfig()
config.Sampling = &zap.SamplingConfig{
    Initial:    100,  // log first 100 per second
    Thereafter: 100,  // then log every 100th
}

logger, _ := config.Build()
```

## Integration with Gin/Echo

```go
// Gin middleware
func GinLogger(logger *zap.Logger) gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        path := c.Request.URL.Path

        c.Next()

        logger.Info("request",
            zap.String("path", path),
            zap.String("method", c.Request.Method),
            zap.Int("status", c.Writer.Status()),
            zap.Duration("latency", time.Since(start)),
        )
    }
}

// Echo middleware
func EchoLogger(logger *zap.Logger) echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            start := time.Now()
            
            err := next(c)
            
            logger.Info("request",
                zap.String("path", c.Path()),
                zap.String("method", c.Request().Method),
                zap.Int("status", c.Response().Status),
                zap.Duration("latency", time.Since(start)),
            )
            
            return err
        }
    }
}
```
