# Go Code Style Guidelines

## General Principles

- Use the Go standard library whenever possible. Only use third-party libraries when necessary.
- Limit line length to 120 characters.
- Write code that is easy to test:
  - Use interfaces to decouple components and improve testability.
  - Use dependency injection to pass dependencies into functions and methods.
  - Wrap even basic operations (such as OS functions and file operations) in interfaces to make them easier to mock and test.

## Struct Definitions

After each struct definition, verify interface implementation by adding:

```go
var _ InterfaceName = (*StructName)(nil)
```

## Constructors

Provide a constructor function for each struct, named `NewStructName`.

- Place this function immediately after the struct definition and the interface assertion line (if present).

```go
type MyService struct {
    logger Logger
    fs     FileSystem
}

var _ Service = (*MyService)(nil)

func NewMyService(logger Logger, fs FileSystem) *MyService {
    return &MyService{
        logger: logger,
        fs:     fs,
    }
}
```

## Code Formatting

- Vertically align function arguments when there are multiple arguments.
- Insert blank lines between logical sections of code.
- Do not separate error unwrapping from related code with a blank line; treat it as part of the same section.

```go
// Good: error handling is part of the same section
result, err := doSomething()
if err != nil {
    return fmt.Errorf("failed to do something: %w", err)
}

// Next logical section starts after blank line
processResult(result)
```

## Documentation

End all type and function comments with a period, following Go conventions.

```go
// MyService handles business logic for the application.
type MyService struct {
    // ...
}

// Process executes the main workflow and returns the result.
func (s *MyService) Process(ctx context.Context) error {
    // ...
}
```

## Performance

Pre-allocate collections (such as slices and maps) to their expected size when possible to reduce memory allocations and improve performance.

```go
// Good: pre-allocated slice
items := make([]Item, 0, len(input))
for _, v := range input {
    items = append(items, transform(v))
}

// Good: pre-allocated map
lookup := make(map[string]int, len(keys))
for i, k := range keys {
    lookup[k] = i
}
```

## Mocks

Never edit mock files directly. Instead, regenerate them by running the `mockery` command in the Go module root directory:

```bash
mockery
```

Run without any arguments to regenerate all mocks.

## Dependency Injection

Always prefer to use dependency injection to pass dependencies into constructors.

```go
// Good: dependencies injected
func NewHandler(
    logger Logger,
    service Service,
    validator Validator,
) *Handler {
    return &Handler{
        logger:    logger,
        service:   service,
        validator: validator,
    }
}

// Bad: dependencies created internally
func NewHandler() *Handler {
    return &Handler{
        logger:    NewDefaultLogger(),  // Don't do this
        service:   NewService(),        // Don't do this
    }
}
```
