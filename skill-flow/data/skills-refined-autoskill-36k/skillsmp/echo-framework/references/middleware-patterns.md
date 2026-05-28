# Echo Middleware Patterns

## Built-in Middleware

```go
import (
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
)

func main() {
    e := echo.New()

    // Logger
    e.Use(middleware.Logger())

    // Recover from panics
    e.Use(middleware.Recover())

    // CORS
    e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
        AllowOrigins: []string{"https://example.com"},
        AllowMethods: []string{http.MethodGet, http.MethodPost},
    }))

    // Request ID
    e.Use(middleware.RequestID())

    // Rate limiter
    e.Use(middleware.RateLimiter(middleware.NewRateLimiterMemoryStore(20)))

    // Gzip compression
    e.Use(middleware.Gzip())
}
```

## Custom Middleware

```go
// Timing middleware
func TimingMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
    return func(c echo.Context) error {
        start := time.Now()
        
        err := next(c)
        
        duration := time.Since(start)
        c.Response().Header().Set("X-Response-Time", duration.String())
        
        return err
    }
}

// Auth middleware
func AuthMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
    return func(c echo.Context) error {
        token := c.Request().Header.Get("Authorization")
        if token == "" {
            return echo.NewHTTPError(http.StatusUnauthorized, "missing token")
        }

        // Validate token
        claims, err := validateToken(token)
        if err != nil {
            return echo.NewHTTPError(http.StatusUnauthorized, "invalid token")
        }

        // Store in context
        c.Set("user", claims.UserID)
        
        return next(c)
    }
}

// Usage
e.GET("/protected", handler, AuthMiddleware)
```

## Middleware with Config

```go
type AuthConfig struct {
    Skipper    middleware.Skipper
    TokenLookup string
    AuthScheme  string
}

func AuthWithConfig(config AuthConfig) echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            if config.Skipper != nil && config.Skipper(c) {
                return next(c)
            }
            
            // Auth logic using config...
            
            return next(c)
        }
    }
}

// Skip auth for certain paths
e.Use(AuthWithConfig(AuthConfig{
    Skipper: func(c echo.Context) bool {
        return c.Path() == "/health" || c.Path() == "/login"
    },
}))
```

## JWT Authentication

```go
import "github.com/labstack/echo-jwt/v4"

func main() {
    e := echo.New()

    // JWT middleware
    config := echojwt.Config{
        SigningKey: []byte("secret"),
        NewClaimsFunc: func(c echo.Context) jwt.Claims {
            return new(JwtCustomClaims)
        },
    }

    r := e.Group("/api")
    r.Use(echojwt.WithConfig(config))

    r.GET("/users", func(c echo.Context) error {
        token := c.Get("user").(*jwt.Token)
        claims := token.Claims.(*JwtCustomClaims)
        return c.JSON(http.StatusOK, claims)
    })
}

type JwtCustomClaims struct {
    UserID string `json:"user_id"`
    Role   string `json:"role"`
    jwt.RegisteredClaims
}
```
