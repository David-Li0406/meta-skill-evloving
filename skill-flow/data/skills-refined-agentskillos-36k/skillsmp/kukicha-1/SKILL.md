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
    |> slice.Filter(func(u User) bool
        return u.active
    )
    |> slice.Map(func(u User) string
        return u.name
    )

# Placeholder strategy: use _ to specify where piped value goes
# Useful when piped value isn't the first argument
todo |> json.MarshalWrite(writer, _)     # Becomes: json.MarshalWrite(writer, todo)
data |> encode(options, _, format)       # Becomes: encode(options, data, format)
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
    
 for                          # Infinite loop
     if something
         break
     continue
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
msg := receive from ch
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

# Complex Logic (Improved Parser)
if err != empty or failed
    handleError()
```

### Output (print Builtin)
```kukicha
# print automatically imports fmt and transpiles to fmt.Println()
print("Hello World")
print("Value:", count, "items")       # Variadic - accepts multiple arguments
print(user.Name, user.Age)            # Works with any types
```

### Function Types (Callbacks & Higher-Order Functions)
```kukicha
# Simple callback: takes int, returns bool
func Filter(items list of int, predicate func(int) bool) list of int
    result := list of int{}
    for item in items
        if predicate(item)
            result = append(result, item)
    return result

# No return type
func ForEach(items list of string, action func(string))
    for item in items
        action(item)

# Pass function literal as callback
evens := Filter(list of int{1, 2, 3, 4}, func(n int) bool
    return n % 2 equals 0
)
```

## Transpilation Patterns

| Kukicha | Go |
|---------|-----|
| `list of int` | `[]int` |
| `map of string to int` | `map[string]int` |
| `func(int) bool` | `func(int) bool` |
| `func(string)` | `func(string)` |
| `reference User` | `*User` |
| `reference of x` | `&x` |
| `dereference ptr` | `*ptr` |
| `empty` | `nil` |
| `and`, `or`, `not` | &&, \|\|, ! |
| `equals` | `==` |
| `print(...)` | `fmt.Println(...)` |
| `"Hello {name}"` | `fmt.Sprintf("Hello %s", name)` |
| `items[-1]` | `items[len(items)-1]` |
| `json:"name"` (struct tag) | `` `json:"name"` `` (backtick-quoted) |
| Indentation blocks | `{ }` braces |
| `a \|> f(b)` | `f(a, b)` |
| `a \|> f(b, _)` | `f(b, a)` (placeholder) |
| `x := f() onerr "default"` | `x, err := f(); if err != nil { x = "default" }` |
| `x := f() onerr discard` | `x, _ := f()` |
| `break` | `break` |
| `continue` | `continue` |
| `for` (bare) | `for { ... }` |

## Standard Library

Located in `stdlib/`:

| Package | Purpose |
|---------|---------|
| `iter` | Functional iterators with Go 1.25+ generics (Filter, Map, Take, Skip) |
| `slice` | Slice operations with Go 1.25+ generics (First, Last, Reverse, Unique, **GroupBy**) |
| `string` | String utilities (ToUpper, Split, Contains) |
| `json` | Pipe-friendly jsonv2 wrapper (Marshal, Unmarshal, MarshalWrite, UnmarshalRead, Encoder/Decoder) |
| `fetch` | HTTP client with builder pattern (Get, Post, CheckStatus, Text, Bytes) |
| `files` | File operations (Read, Write, List) |
| `parse` | Data format parsing (CSV, YAML) - delegates JSON to stdlib/json |
| `concurrent` | Concurrency helpers (Parallel, ParallelWithLimit, Go) |
| `http` | HTTP server helpers (WithCSRF, Serve) |
| `shell` | Command execution with builder pattern (New, Dir, SetTimeout, Env, Execute) |
| `cli` | CLI argument parsing with builder pattern (New, Arg, AddFlag, Action, RunApp) |

Example with stdlib:
```kukicha
import "stdlib/fetch"
import "stdlib/slice"
import "stdlib/json"

# Fetch data with pipes (each step can fail, handled at end)
repos := list of Repo{}
resp := fetch.Get("https://api.github.com/users/golang/repos") onerr panic "fetch failed"
resp = resp |> fetch.CheckStatus() onerr panic "bad status"
data := resp |> fetch.Bytes() onerr panic "read failed"
json.Unmarshal(data, reference of repos) onerr panic "parse failed"

# Filter with pipes
activeRepos := repos |> slice.Filter(func(r Repo) bool
    return r.Stars > 100
)
```

### Parse Package (jsonv2 powered)
```kukicha
# Standard JSON parsing - use json.Unmarshal with parse.Json()
config := Config{}
jsonStr |> parse.Json() |> json.Unmarshal(_, reference config) onerr panic "parse failed"

# NDJSON (newline-delimited JSON) parsing
lines := logData |> parse.JsonLines()  # Returns list of JSON strings
logs := lines |> slice.Map(parse.Json)  # Convert each line to bytes
           |> slice.Map(json.Unmarshal(_, reference of LogEntry{}))

# Pretty-print JSON - delegates to json.MarshalPretty
output := config |> parse.JsonPretty()
```

### Concurrent Package
```kukicha
import "stdlib/concurrent"

# Run multiple tasks in parallel
concurrent.Parallel(task1, task2, task3)

# Limit concurrent execution (at most 4 tasks at once)
concurrent.ParallelWithLimit(4, tasks...)

# Run a function in a goroutine
concurrent.Go(myFunc)
```

### HTTP Package
```kukicha
import "stdlib/http"

# Add Cross-Origin protection to handler
handler := http.WithCSRF(myHandler)

# Start server
http.Serve(":8080", handler)
```

### Shell Package
```kukicha
import "stdlib/shell"

# Simple command
cmd := shell.New("ls", "-la")
result := shell.Execute(cmd)
if shell.Success(result)
    print(string(shell.GetOutput(result)))

# Command with options using builder pattern
cmd := shell.New("git", "status")
    |> shell.Dir("./repo")
    |> shell.SetTimeout(30)
result := shell.Execute(cmd)

if shell.Success(result)
    print(string(shell.GetOutput(result)))
else
    print("Error: {string(shell.GetError(result))}")

# Check if command exists
if shell.Which("docker")
    print("Docker is installed")

# Run with environment variables
cmd := shell.New("npm", "install")
    |> shell.Dir("./frontend")
    |> shell.Env("NODE_ENV", "production")
result := shell.Execute(cmd)
if shell.Success(result)
    print("npm install succeeded")
```

### CLI Package
```kukicha
import "stdlib/cli"

func main()
    app := cli.New("mytool")
        |> cli.Arg("command", "Command to run (fetch|process)")
        |> cli.Arg("input", "Input file or URL")
        |> cli.AddFlag("verbose", "Enable verbose output", "false")
        |> cli.AddFlag("format", "Output format", "json")
        |> cli.Action(handleCommand)

    cli.RunApp(app) onerr panic "command failed"

func handleCommand(args cli.Args)
    command := cli.GetString(args, "command")
    input := cli.GetString(args, "input")
    verbose := cli.GetBool(args, "verbose")
    format := cli.GetString(args, "format")

    if command == "fetch"
        print("Fetching {input} with format {format}")
    else if command == "process"
        print("Processing {input}")
```

### Slice Package with Generics
```kukicha
import "stdlib/slice"

type LogEntry
    level string
    message string

# Group log entries by level (automatically generates [T any, K comparable])
entries := logs |> slice.GroupBy(func(e LogEntry) string
    return e.level
)
# Result: map[string][]LogEntry with keys "ERROR", "WARN", "INFO", etc.

# GroupBy is Go 1.25+ generic - you write simple Kukicha code, transpiler handles the generics
```

## Transparent Go 1.25+ Generics

**Important:** You don't write generic syntax in Kukicha! The transpiler automatically generates proper Go generics for stdlib functions.

When you use `slice.GroupBy`, `iter.Map`, etc., the transpiler:
- Infers type parameters from your code (`T` for element type, `K` for key type)
- Applies proper constraints where needed (`K comparable` for map keys)
- Generates correct Go 1.25+ generic syntax
- All type safety benefits without the syntax burden

This is part of Kukicha's philosophy: **"It's Just Go"** - zero runtime overhead, full type safety, no learning curve for generics.

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

### Defer
```kukicha
func ProcessFile(path string)
    file := os.Open(path) onerr panic "cannot open"
    defer file.Close()
    # ... process file
```

## Go 1.25+ Features

Kukicha leverages modern Go features:

- **encoding/json/v2**: 2-10x faster JSON parsing in `stdlib/json` and `stdlib/fetch`
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
