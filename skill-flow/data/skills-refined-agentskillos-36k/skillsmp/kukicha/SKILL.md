---
name: kukicha
description: Help write, debug, and understand Kukicha code - a beginner-friendly language that transpiles to Go. Use when working with .kuki files, discussing Kukicha syntax, error handling with onerr, pipe operators, or the Kukicha compiler/transpiler.
---

# Kukicha Language Skill

You are helping with **Kukicha** (茎 = "stem"), a beginner-friendly programming language that compiles to idiomatic Go code. The core philosophy is **"It's Just Go"** - Kukicha is syntactic sugar with zero runtime overhead.

## Quick Reference

### File Extension
- `.kuki` files contain Kukicha source code
- Transpiles to `.go` files

### CLI Commands
```bash
kukicha build <file.kuki>      # Compile to Go binary
kukicha run <file.kuki>        # Compile and run
kukicha check <file.kuki>      # Type-check only
kukicha fmt [options] <path>   # Format code
kukicha version                # Show version
```

## Syntax Essentials

### Variables (Walrus Operator)
```kukicha
count := 42          # Create new binding (short declaration)
count = 100          # Reassign existing variable
```

### Functions (Explicit Types Required)
```kukicha
func Greet(name string) string
    return "Hello {name}"

# Multiple returns
func Divide(a int, b int) int, error
    if b equals 0
        return 0, error "division by zero"
    return a / b, empty

# No return value
func PrintMessage(msg string)
    fmt.Println(msg)
```

### Methods (Receiver Syntax)
```kukicha
# Syntax: func Name on receiverName ReceiverType ReturnType
func Display on todo Todo string
    return "{todo.id}: {todo.title}"

# Pointer receiver
func SetTitle on todo reference Todo
    todo.title = "New Title"
```

### String Interpolation
```kukicha
name := "World"
greeting := "Hello {name}!"        # Transpiles to fmt.Sprintf
complex := "Result: {a + b}"       # Expressions allowed
```

### Error Handling (onerr Operator)
```kukicha
# Panic on error
content := file.read("config.json") onerr panic "missing file"

# Provide default value
port := env.get("PORT") onerr "8080"

# Return error to caller
data := fetchData() onerr return empty, error

# Discard error (use sparingly)
result := riskyOp() onerr discard
```

### Pipe Operator
```kukicha
result := data
    |> parse()
    |> transform()
    |> process()

# With arguments (piped value becomes first argument)
users := fetchUsers()
    |> slice.Filter(u -> u.active)
    |> slice.Map(u -> u.name)
```

### Control Flow
```kukicha
# If statements (use 'equals' for comparison)
if count equals 0
    return "empty"
else if count < 10
    return "small"
else
    return "large"

# For loops
for item in items
    process(item)

for index, item in items
    fmt.Println("{index}: {item}")

for i from 0 to 10           # 0 to 9 (exclusive)
    fmt.Println(i)

for i from 0 through 10      # 0 to 10 (inclusive)
    fmt.Println(i)

for count > 0                # While-style loop
    count--
```

### Types
```kukicha
type Todo
    id int64
    title string
    completed bool
    tags list of string
    metadata map of string to string

# With struct tags (for JSON, database mapping, etc.)
type User
    ID int64 json:"id"
    Name string json:"name"
    Email string json:"email"
    Active bool json:"active"

# Struct tags support any Go format: json, xml, db, validate, etc.
# Multiple tags: json:"name" db:"user_name"

# Interface
interface Storage
    Save(item Todo) error
    Load(id int64) Todo, error
```

### Collections
```kukicha
# Lists (slices)
items := list of string{"a", "b", "c"}
last := items[-1]                    # Negative indexing supported

# Maps
config := map of string to int{"port": 8080}

# Check membership
if user in admins
    grantAccess()
```

### Pointers & References
```kukicha
# Pointer type
userPtr reference User

# Address-of
ptr := reference of user

# Dereference
val := dereference ptr

# Common pattern with json
json.Unmarshal(data, reference of result) onerr panic "parse failed"
```

### Concurrency
```kukicha
# Goroutines
go fetchData(url)

# Channels
ch := make channel of string
send ch, "message"
msg := receive ch
close(ch)
```

### Null/Nil
```kukicha
# Use 'empty' instead of nil
if user equals empty
    return error "user not found"

# Typed empty for returns
return empty list of string
```

### Boolean Operators
```kukicha
# Use English keywords
if a and b
if a or b
if not done

# Equality
if x equals y      # Same as ==
if x != y          # Not equals still uses !=
```

## Transpilation Patterns

| Kukicha | Go |
|---------|-----|
| `list of int` | `[]int` |
| `map of string to int` | `map[string]int` |
| `reference User` | `*User` |
| `reference of x` | `&x` |
| `dereference ptr` | `*ptr` |
| `empty` | `nil` |
| `and`, `or`, `not` | &&, \|\|, ! |
| `equals` | `==` |
| `"Hello {name}"` | `fmt.Sprintf("Hello %s", name)` |
| `items[-1]` | `items[len(items)-1]` |
| `json:"name"` (struct tag) | `` `json:"name"` `` (backtick-quoted) |
| Indentation blocks | `{ }` braces |

## Standard Library

Located in `stdlib/`:

| Package | Purpose |
|---------|---------|
| `iter` | Functional iterators (Filter, Map, Take, Skip) |
| `slice` | Slice operations (First, Last, Reverse, Unique) |
| `string` | String utilities (ToUpper, Split, Contains) |
| `fetch` | HTTP client for pipe-based requests (uses jsonv2) |
| `files` | File operations (Read, Write, List) |
| `parse` | Data format parsing (JSON, CSV, YAML) - uses jsonv2 for 2-10x faster JSON |
| `concurrent` | Concurrency helpers (Parallel, ParallelWithLimit, Go) |
| `http` | HTTP server helpers (WithCSRF, Serve) |

Example with stdlib:
```kukicha
import "stdlib/fetch"
import "stdlib/slice"
import "stdlib/parse"

repos := "https://api.github.com/users/golang/repos"
    |> fetch.Get()
    |> fetch.CheckStatus()
    |> fetch.Text()
    |> parse.Json() as list of Repo
    |> slice.Filter(r -> r.Stars > 100)
```

### Parse Package (jsonv2 powered)
```kukicha
# Standard JSON parsing
data := jsonStr |> parse.Json() as Config

# Streaming JSON from readers (memory efficient)
config := file |> parse.JsonFromReader() as Config

# NDJSON (newline-delimited JSON) parsing
logs := logData |> parse.JsonLines() as list of LogEntry

# Pretty-print JSON
output := config |> parse.JsonPretty()
```

### Concurrent Package
```kukicha
import "stdlib/concurrent"

# Run multiple tasks in parallel
concurrent.Parallel(task1, task2, task3)

# Limit concurrent execution (at most 4 tasks at once)
concurrent.ParallelWithLimit(4, tasks...)

# Run with WaitGroup tracking
wg := concurrent.Go(myFunc)
wg.Wait()
```

### HTTP Package
```kukicha
import "stdlib/http"

# Add Cross-Origin protection to handler
handler := http.WithCSRF(myHandler)

# Start server
http.Serve(":8080", handler)
```

## Project Structure

- `petiole` = package (Go equivalent)
- `stem.toml` = project root config
- Package name auto-calculated from file path if not declared

```kukicha
petiole mypackage    # Optional - usually inferred from directory

import "fmt"
import "encoding/json"
import "stdlib/slice"
```

## Common Patterns

### Struct Literals
```kukicha
todo := Todo
    id: 1
    title: "Learn Kukicha"
    completed: false
```

### Lambda/Arrow Functions
```kukicha
filtered := slice.Filter(items, x -> x > 10)
mapped := slice.Map(items, x -> x * 2)
```

### Defer
```kukicha
func ProcessFile(path string)
    file := os.Open(path) onerr panic "cannot open"
    defer file.Close()
    # ... process file
```

## Go 1.25+ Features

Kukicha leverages modern Go features:

- **encoding/json/v2**: 2-10x faster JSON parsing in `stdlib/parse` and `stdlib/fetch`
- **WaitGroup.Go()**: Automatic Add(1) and Done() tracking (used in `stdlib/concurrent`)
- **testing/synctest**: Deterministic concurrency testing in compiler tests
- **Green Tea GC**: Improved garbage collection (no code changes needed)

## Architecture (for compiler work)

The compiler has 4 phases:

1. **Lexer** (`internal/lexer/`) - Tokenization with INDENT/DEDENT
2. **Parser** (`internal/parser/`) - AST building
3. **Semantic** (`internal/semantic/`) - Type checking, validation
4. **CodeGen** (`internal/codegen/`) - Go code generation

Key design decisions:
- **Signature-first inference**: Function params/returns need explicit types; local vars are inferred
- **Indentation-based**: 4-space blocks (no braces in canonical form)
- **Context-sensitive keywords**: `list`, `map`, `channel` are keywords only in type contexts

## Testing

```bash
go test ./...                        # Run all tests
go test ./internal/lexer/... -v      # Verbose lexer tests
go test ./... -cover                 # With coverage
```

## When Writing Kukicha Code

1. Always use explicit types for function parameters and returns
2. Use `onerr` for error handling instead of manual `if err != nil`
3. Prefer pipe operators for data transformation chains
4. Use English keywords (`and`, `or`, `not`, `equals`, `empty`)
5. Use 4-space indentation (tabs not allowed)
6. Use `reference of` and `dereference` instead of `&` and `*`
