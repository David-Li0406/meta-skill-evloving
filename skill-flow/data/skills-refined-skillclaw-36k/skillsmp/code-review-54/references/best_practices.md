# Code Quality Best Practices

Level 3 resource for code-review skill - load for quality reviews.

## Code Organization

### File Structure

- One primary type per file
- Related types can be in same file
- Test files alongside source files
- Clear package boundaries

### Function Design

- Single responsibility principle
- Maximum 50 lines per function (guideline)
- Maximum 5 parameters (prefer structs for more)
- Early returns for error cases

### Naming Conventions

#### Go

```go
// Exported: PascalCase
func ProcessRequest(req *Request) error

// Unexported: camelCase
func validateInput(input string) bool

// Interfaces: -er suffix
type Reader interface { Read(p []byte) (n int, err error) }

// Acronyms: consistent case
func ParseHTTPRequest()  // not ParseHttpRequest
type URLParser struct{}  // not UrlParser
```

#### TypeScript

```typescript
// Classes: PascalCase
class UserService {}

// Functions/variables: camelCase
function processData() {}
const userData = {};

// Constants: SCREAMING_SNAKE_CASE
const MAX_RETRY_COUNT = 3;

// Interfaces: PascalCase, no I prefix
interface UserProfile {}  // not IUserProfile
```

## Error Handling

### Go Error Patterns

```go
// ✅ Good: Wrap with context
if err != nil {
    return fmt.Errorf("failed to process user %s: %w", userID, err)
}

// ❌ Bad: Naked return
if err != nil {
    return err
}

// ✅ Good: Check specific errors
if errors.Is(err, sql.ErrNoRows) {
    return nil, ErrNotFound
}

// ✅ Good: Custom error types for API boundaries
type ValidationError struct {
    Field   string
    Message string
}
```

### TypeScript Error Patterns

```typescript
// ✅ Good: Typed errors
class ValidationError extends Error {
  constructor(public field: string, message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

// ✅ Good: Result types
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };
```

## Documentation

### When to Document

- All exported functions/types
- Complex algorithms
- Non-obvious business logic
- API endpoints

### How to Document

```go
// ProcessUser handles user processing with the following steps:
// 1. Validates input parameters
// 2. Checks user permissions
// 3. Updates user record
//
// Returns ErrNotFound if user doesn't exist.
// Returns ErrPermissionDenied if user lacks permissions.
func ProcessUser(ctx context.Context, userID string) error {
```

## Testing

### Test Coverage Guidelines

- Aim for 80% coverage minimum
- 100% coverage for critical paths
- Cover error cases, not just happy paths

### Test Organization

```go
func TestFunction(t *testing.T) {
    tests := []struct {
        name    string
        input   InputType
        want    OutputType
        wantErr bool
    }{
        {"valid input", validInput, expectedOutput, false},
        {"empty input", "", nil, true},
        {"edge case", edgeCase, edgeOutput, false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Function(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
            }
            if !reflect.DeepEqual(got, tt.want) {
                t.Errorf("got = %v, want %v", got, tt.want)
            }
        })
    }
}
```

## Code Smells to Avoid

| Smell | Description | Fix |
| ------- | ------------- | ----- |
| Long function | >50 lines | Extract smaller functions |
| Deep nesting | >3 levels | Early returns, extract functions |
| Magic numbers | Unexplained literals | Use named constants |
| Duplicate code | Copy-paste patterns | Extract shared function |
| God object | Class does everything | Split responsibilities |
| Feature envy | Method uses other class more | Move method |

## Dependency Injection

```go
// ✅ Good: Accept interfaces
type Service struct {
    store Store  // interface
}

func NewService(store Store) *Service {
    return &Service{store: store}
}

// ❌ Bad: Create dependencies internally
func NewService() *Service {
    return &Service{store: NewPostgresStore()}  // tightly coupled
}
```

## Concurrency (Go)

```go
// ✅ Good: Context for cancellation
func Process(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case result := <-resultChan:
        return handleResult(result)
    }
}

// ✅ Good: WaitGroup for goroutine coordination
var wg sync.WaitGroup
for _, item := range items {
    wg.Add(1)
    go func(item Item) {
        defer wg.Done()
        process(item)
    }(item)
}
wg.Wait()
```
