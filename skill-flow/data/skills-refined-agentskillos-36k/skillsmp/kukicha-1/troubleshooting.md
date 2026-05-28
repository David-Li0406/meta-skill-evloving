# Kukicha Troubleshooting Guide

## Common Errors and Solutions

### "missing type annotation for parameter"

**Cause:** Function parameters must have explicit types.

```kukicha
# Wrong
func Add(a, b)
    return a + b

# Correct
func Add(a int, b int) int
    return a + b
```

### "missing return type"

**Cause:** Functions that return values must declare return types.

```kukicha
# Wrong
func GetName()
    return "Alice"

# Correct
func GetName() string
    return "Alice"
```

### "expected INDENT"

**Cause:** Missing or incorrect indentation after function/control flow declarations.

```kukicha
# Wrong (no indentation)
func Test()
return 42

# Correct (4-space indent)
func Test() int
    return 42
```

### "unexpected token in type context"

**Cause:** Using Go syntax instead of Kukicha type syntax.

```kukicha
# Wrong (Go syntax)
func Process(items []string)

# Correct (Kukicha syntax)
func Process(items list of string)
```

### "undefined: nil"

**Cause:** Kukicha uses `empty` instead of `nil`.

```kukicha
# Wrong
if user == nil
    return nil

# Correct
if user equals empty
    return empty
```

### "invalid operator &&"

**Cause:** Kukicha uses English boolean operators.

```kukicha
# Wrong
if a && b || !c

# Correct
if a and b or not c
```

### "expected 'of' after 'list'"

**Cause:** Collection types require the full syntax.

```kukicha
# Wrong
items list string

# Correct
items list of string
```

### "onerr requires error-returning expression"

**Cause:** Using `onerr` on a function that doesn't return an error.

```kukicha
# Wrong (len doesn't return error)
length := len(items) onerr 0

# Correct
length := len(items)
```

### "cannot use reference without 'of'"

**Cause:** Address-of syntax requires `reference of`.

```kukicha
# Wrong
ptr := &user

# Correct
ptr := reference of user
```

## Indentation Issues

### Mixed Tabs and Spaces

Kukicha requires 4-space indentation. Tabs cause errors.

```bash
# Fix with formatter
kukicha fmt -w myfile.kuki
```

### Inconsistent Block Levels

Each nested block must increase indentation by exactly 4 spaces.

```kukicha
# Wrong (8-space jump)
func Test()
        return 42

# Correct
func Test() int
    return 42

# Nested blocks
func Process()
    if condition
        for item in items
            process(item)
```

## Type Inference Limits

### Where Inference Works
```kukicha
func Example()
    x := 42              # Inferred as int
    name := "Alice"      # Inferred as string
    items := list of string{"a", "b"}  # Explicit type in literal
```

### Where Inference Doesn't Work
```kukicha
# Function parameters - must be explicit
func Process(x int)     # Required

# Function returns - must be explicit
func GetValue() int     # Required
    return 42

# Empty collections need type
items := list of string{}   # Type required
```

## Error Handling Edge Cases

### Multiple Return Values with onerr
```kukicha
# When function returns (T, error)
value := getData() onerr return empty, error

# When function returns (T1, T2, error)
# Use tuple unpacking first
a, b, err := getMultiple()
if err != empty
    return empty, empty, err
```

### onerr with return
```kukicha
# Must match function's return signature
func LoadConfig() Config, error
    data := readFile() onerr return empty Config, error  # Explicit empty type
    # ...
```

## String Interpolation Gotchas

### Escaping Braces
```kukicha
# To include literal braces, double them
msg := "Use {{name}} for variables"  # Outputs: Use {name} for variables
```

### Complex Expressions
```kukicha
# Expressions in interpolation must be valid
msg := "Sum: {a + b}"           # OK
msg := "Cond: {if x then y}"    # Wrong - no if expressions

# Use intermediate variable for complex logic
result := if condition then "yes" else "no"  # Wrong - no ternary
result := "yes"
if not condition
    result = "no"
msg := "Result: {result}"
```

## Import Path Issues

### stdlib Imports
```kukicha
# Correct stdlib path
import "stdlib/slice"
import "stdlib/iter"

# Not this
import "slice"           # Wrong
import "./stdlib/slice"  # Wrong
```

### Go Standard Library
```kukicha
# Use exactly as in Go
import "fmt"
import "encoding/json"
import "net/http"
```

## Method Receiver Mistakes

### Forgetting Receiver Name
```kukicha
# Wrong (missing receiver name)
func Display on Todo string

# Correct
func Display on todo Todo string
    return todo.title
```

### Value vs Reference Receiver
```kukicha
# Value receiver (cannot modify)
func GetTitle on todo Todo string
    return todo.title

# Reference receiver (can modify)
func SetTitle on todo reference Todo title string
    todo.title = title
```

## Debugging Tips

### Check Generated Go Code
```bash
# View transpiled output
kukicha build myfile.kuki
cat myfile.go  # or check build output
```

### Verbose Type Checking
```bash
kukicha check myfile.kuki
```

### Common Build Errors

| Error | Likely Cause |
|-------|--------------|
| "unexpected NEWLINE" | Missing expression or extra blank line |
| "expected identifier" | Using reserved word as variable name |
| "type mismatch" | Wrong type in assignment/return |
| "undeclared name" | Variable used before declaration |
| "not enough arguments" | Missing function arguments |

## Function Type Errors

### "undefined function type"

**Cause:** Using function type syntax incorrectly or with wrong parameter/return types.

```kukicha
# Wrong - mixed Go and Kukicha syntax
callback func(int) -> int

# Correct
callback func(int) int
```

### "function expects N arguments, got M"

**Cause:** Passing function literal with wrong number of parameters.

```kukicha
func Filter(items list of int, predicate func(int) bool) list of int
    # ...

# Wrong - takes 2 parameters instead of 1
result := Filter(numbers, func(a int, b int) bool
    return a > b
)

# Correct - takes 1 parameter
result := Filter(numbers, func(n int) bool
    return n > 5
)
```

### "function literal must return type"

**Cause:** Function type requires return type but function literal doesn't specify it.

```kukicha
# Wrong - no return type specified
callback := func(n int)
    return n * 2

# Correct
callback := func(n int) int
    return n * 2
```

### "cannot use func with wrong signature"

**Cause:** Function signature doesn't match the parameter type.

```kukicha
func Process(handler func(string) int)
    # ...

# Wrong - returns string, not int
Process(func(s string) string
    return s
)

# Correct - returns int
Process(func(s string) int
    return len(s)
)
```

## Performance Considerations

### Negative Indexing
```kukicha
# Literal negative index - zero overhead
last := items[-1]  # Compiles to items[len(items)-1]

# Dynamic negative index - requires runtime check
idx := getIndex()  # Might be negative
item := items.at(idx)  # Use .at() method for safety
```

### String Interpolation in Loops
```kukicha
# Avoid in hot loops - each creates new string
for i from 0 to 1000000
    msg := "Item {i}"  # fmt.Sprintf overhead

# Better for hot paths
var builder strings.Builder
for i from 0 to 1000000
    builder.WriteString("Item ")
    builder.WriteString(strconv.Itoa(i))
```
