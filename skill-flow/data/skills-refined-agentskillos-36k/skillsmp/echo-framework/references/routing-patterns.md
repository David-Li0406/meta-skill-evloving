# Echo Routing Patterns

## Basic Routing

```go
import (
    "net/http"
    "github.com/labstack/echo/v4"
)

func main() {
    e := echo.New()

    // Basic routes
    e.GET("/users", listUsers)
    e.POST("/users", createUser)
    e.GET("/users/:id", getUser)
    e.PUT("/users/:id", updateUser)
    e.DELETE("/users/:id", deleteUser)

    e.Logger.Fatal(e.Start(":8080"))
}

// Handler with path parameter
func getUser(c echo.Context) error {
    id := c.Param("id")
    return c.JSON(http.StatusOK, map[string]string{"id": id})
}

// Query parameters
func listUsers(c echo.Context) error {
    page := c.QueryParam("page")
    limit := c.QueryParam("limit")
    return c.JSON(http.StatusOK, map[string]string{
        "page":  page,
        "limit": limit,
    })
}
```

## Route Groups

```go
func main() {
    e := echo.New()

    // API versioning
    v1 := e.Group("/api/v1")
    {
        v1.GET("/users", listUsersV1)
        v1.POST("/users", createUserV1)
    }

    v2 := e.Group("/api/v2")
    {
        v2.GET("/users", listUsersV2)
    }

    // Group with middleware
    admin := e.Group("/admin", middleware.BasicAuth(validateAdmin))
    {
        admin.GET("/stats", getStats)
        admin.POST("/config", updateConfig)
    }
}
```

## Request Binding

```go
type CreateUserRequest struct {
    Name  string `json:"name" validate:"required"`
    Email string `json:"email" validate:"required,email"`
    Age   int    `json:"age" validate:"gte=0,lte=130"`
}

func createUser(c echo.Context) error {
    req := new(CreateUserRequest)
    if err := c.Bind(req); err != nil {
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }

    // Validate
    if err := c.Validate(req); err != nil {
        return err
    }

    // Process...
    return c.JSON(http.StatusCreated, req)
}

// Setup validator
func main() {
    e := echo.New()
    e.Validator = &CustomValidator{validator: validator.New()}
}

type CustomValidator struct {
    validator *validator.Validate
}

func (cv *CustomValidator) Validate(i interface{}) error {
    if err := cv.validator.Struct(i); err != nil {
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }
    return nil
}
```

## Error Handling

```go
// Custom HTTP error handler
e.HTTPErrorHandler = func(err error, c echo.Context) {
    code := http.StatusInternalServerError
    message := "Internal Server Error"

    if he, ok := err.(*echo.HTTPError); ok {
        code = he.Code
        message = he.Message.(string)
    }

    c.JSON(code, map[string]string{
        "error": message,
    })
}

// In handlers
func getUser(c echo.Context) error {
    id := c.Param("id")
    user, err := userService.FindByID(id)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            return echo.NewHTTPError(http.StatusNotFound, "user not found")
        }
        return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
    }
    return c.JSON(http.StatusOK, user)
}
```
