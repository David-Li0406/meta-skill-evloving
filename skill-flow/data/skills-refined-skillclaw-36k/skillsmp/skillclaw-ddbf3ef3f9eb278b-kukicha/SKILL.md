---
name: kukicha
description: Use this skill when writing, debugging, or understanding Kukicha code, a beginner-friendly language that transpiles to Go. It is useful for working with .kuki files, discussing Kukicha syntax, error handling, and the Kukicha compiler.
---

# Kukicha Language Skill

You are helping with **Kukicha** (茎 = "stem"), a beginner-friendly programming language that compiles to idiomatic Go code. The core philosophy is **"It's Just Go"** - Kukicha is syntactic sugar with zero runtime overhead.

## Quick Reference

### File Extension
- `.kuki` files contain Kukicha source code.
- Transpiles to `.go` files.

### CLI Commands
```bash
kukicha build <file.kuki>      # Compile to Go binary
kukicha run <file.kuki>        # Compile and run
kukicha check <file.kuki>      # Type-check only
kukicha fmt [options] <path>   # Format code
kukicha version                 # Show version
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
func Divide(a int, b int) (int, error)
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
if condition equals true
    // do something
else
    // do something else
```