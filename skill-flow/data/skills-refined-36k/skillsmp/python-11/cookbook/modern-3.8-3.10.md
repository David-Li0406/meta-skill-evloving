# Modern Python: 3.8 to 3.10

Key language features from 3.8, 3.9, and 3.10.

---
## Walrus Operator (3.8+)

**Problem**: You need to assign a value and use it in an expression without splitting into multiple lines.

**Solution**:
```python
# Read until empty line
while (line := input()) != "":
    print(f"Got: {line}")

# Filter and capture
if (match := pattern.search(text)) is not None:
    print(match.group(0))

# List comprehension with reuse
results = [y for x in data if (y := expensive(x)) > threshold]
```

**Tip**: The walrus operator `:=` reduces boilerplate when you need both assignment and the value in conditions or comprehensions.

---

## Positional-Only Parameters (3.8+)

**Problem**: You want to prevent callers from using keyword arguments for certain parameters, ensuring API stability.

**Solution**:
```python
def greet(name, /, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alice")              # OK
greet("Alice", "Hi")        # OK
greet(name="Alice")         # TypeError - name is positional-only
```

**Tip**: Use `/` to mark parameters as positional-only, allowing you to rename internal parameters without breaking compatibility.

---

## Self-Documenting F-Strings (3.8+)

**Problem**: You're debugging or logging and want to print variable names along with their values.

**Solution**:
```python
x = 10
y = 25
print(f"{x=}, {y=}, {x+y=}")
# Output: x=10, y=25, x+y=35

user = {"name": "Alice", "age": 30}
print(f"{user['name']=}")
# Output: user['name']='Alice'
```

**Tip**: The `=` specifier in f-strings shows both the expression and its value, perfect for quick debugging.

---

## Dict Merge Operators (3.9+)

**Problem**: You need to merge dictionaries or update one dict with another's values.

**Solution**:
```python
defaults = {"host": "localhost", "port": 8080}
overrides = {"port": 3000, "debug": True}

# Merge (new dict)
config = defaults | overrides
# {'host': 'localhost', 'port': 3000, 'debug': True}

# Update in place
defaults |= overrides
```

**Tip**: Use `|` for merging (creates new dict) and `|=` for in-place updates, replacing the older `{**d1, **d2}` pattern.

---

## Built-in Generic Types (3.9+)

**Problem**: You want type hints without importing from the `typing` module.

**Solution**:
```python
# No more typing.List, typing.Dict imports
def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Works with all builtins
ids: set[int] = {1, 2, 3}
pairs: tuple[str, int] = ("age", 25)
```

**Tip**: All built-in collection types now support generic syntax directly, making type hints cleaner and more readable.

---

## String Prefix/Suffix Removal (3.9+)

**Problem**: You need to cleanly remove known prefixes or suffixes from strings.

**Solution**:
```python
filename = "test_user_service.py"

filename.removeprefix("test_")     # "user_service.py"
filename.removesuffix(".py")       # "test_user_service"

# Replaces awkward patterns like:
# s[len(prefix):] if s.startswith(prefix) else s
```

**Tip**: These methods only remove the prefix/suffix if present, otherwise return the original string unchanged.

---

## Pattern Matching (3.10+)

**Problem**: You need to match complex data structures and extract values in a clean, readable way.

**Solution**:
```python
def handle(command):
    match command.split():
        case ["quit"]:
            return "Goodbye"
        case ["load", filename]:
            return f"Loading {filename}"
        case ["save", filename, "--force"]:
            return f"Force saving {filename}"
        case _:
            return "Unknown command"

# With guards
match point:
    case (x, y) if x == y:
        print("On diagonal")
    case (x, y):
        print(f"At ({x}, {y})")

# Class patterns
match event:
    case Click(x=0, y=0):
        print("Origin click")
    case Click(x=x, y=y):
        print(f"Click at {x}, {y}")
```

**Tip**: Pattern matching is more powerful than `if/elif` chains, supporting destructuring, guards, and type matching in a single construct.

---

## Union Type Syntax (3.10+)

**Problem**: You want cleaner type hints for values that can be multiple types.

**Solution**:
```python
# Instead of Union[int, str]
def process(value: int | str | None) -> str:
    if value is None:
        return "empty"
    return str(value)

# Works in isinstance too
isinstance(x, int | str)  # Same as isinstance(x, (int, str))
```

**Tip**: The `|` syntax works in both type hints and runtime type checking with `isinstance()`.

---

## Parenthesized Context Managers (3.10+)

**Problem**: You need to use multiple context managers without deeply nested indentation.

**Solution**:
```python
with (
    open("input.txt") as src,
    open("output.txt", "w") as dst,
    some_lock as lock,
):
    dst.write(src.read())
```

**Tip**: Parentheses allow you to format multiple context managers cleanly across multiple lines without backslash continuation.

