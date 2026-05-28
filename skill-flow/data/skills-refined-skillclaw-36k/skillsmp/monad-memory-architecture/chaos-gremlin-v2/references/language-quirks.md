# Language-Specific Quirks

**Exploitable Language Features by Language**

---

## Purpose

Catalog language-specific behaviors that chaos-gremlin can exploit for unconventional solutions. These are features (or bugs) specific to each language that enable creative chaos.

---

## JavaScript

### Type Coercion Olympics

```javascript
// WAT Collection
"" == false           // true
[] == false           // true
[] == ![]             // true
null >= 0             // true
null == 0             // false
null <= 0             // true

// Useful chaos
!!value               // Convert to boolean
+value                // Convert to number
""+value              // Convert to string
~~value               // Truncate to integer (double bitwise NOT)
```

### Automatic Semicolon Insertion

```javascript
// ASI can break things
return
  { value: 42 }       // Returns undefined!

// Correct
return {
  value: 42
}
```

### Hoisting

```javascript
console.log(chaos)    // undefined (not error!)
var chaos = "exists"

// Function hoisting
doThing()             // Works!
function doThing() { }

// Temporal dead zone (let/const)
console.log(x)        // ReferenceError
let x = 5
```

---

## Python

### Mutable Default Arguments

```python
# Classic trap
def append_to(element, list=[]):
    list.append(element)
    return list

append_to(1)  # [1]
append_to(2)  # [1, 2] - WAT

# Exploitable for memoization
def counter(increment, count=[0]):
    count[0] += increment
    return count[0]
```

### Walrus Operator (Assignment Expression)

```python
# := allows assignment in expressions
if (n := len(data)) > 10:
    print(f"Large dataset: {n}")

# Cursed but useful
while (line := file.readline()):
    process(line)
```

### Everything Is An Object

```python
# Functions are objects
def func():
    pass

func.counter = 0  # Add attributes to functions
func.counter += 1
```

---

## Go

### Multiple Return Values

```go
// Functions can return multiple values
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Chaos: swap without temp
func swap(a, b int) (int, int) {
    return b, a
}
```

### Defer Stack

```go
// Defer executes in LIFO order
func chaos() {
    defer fmt.Println("1")
    defer fmt.Println("2")
    defer fmt.Println("3")
}
// Prints: 3, 2, 1
```

---

## Related Files
- `SKILL.md` - Main documentation
- `cursed-but-correct.md` - Patterns using these quirks
- `edge-case-library.md` - Edge cases
