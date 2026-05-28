# Python Style Rules

Detailed reference from Google Python Style Guide Sections 3.1-3.18. For quick lookup, see the main [SKILL.md](SKILL.md).

## 3.1 Semicolons

Never use semicolons to terminate lines or place multiple statements on one line.

```python
# Good
x = 1
y = 2

# Bad
x = 1; y = 2
x = 1;
```

## 3.2 Line Length

Maximum 80 characters. Exceptions: long imports, URLs in comments, long string constants that can't be split.

### Line Continuation

Use implicit continuation inside parentheses, brackets, and braces. Avoid backslash continuation.

```python
# Good
result = some_function(
    argument_one,
    argument_two,
    argument_three,
)

long_string = (
    "This is a very long string that needs to be "
    "split across multiple lines for readability."
)

# Bad
result = some_function(argument_one, \
    argument_two, argument_three)
```

### Breaking Long Lines

Break at the highest syntactic level. Prefer breaking after operators.

```python
# Good
income = (
    gross_wages
    + taxable_interest
    + (dividends - qualified_dividends)
    - ira_deduction
    - student_loan_interest
)

# Bad
income = (gross_wages +
    taxable_interest +
    (dividends - qualified_dividends) -
    ira_deduction -
    student_loan_interest)
```

## 3.3 Parentheses

Use sparingly. Required for tuples, optional elsewhere.

```python
# Good
return x, y
single_element_tuple = (x,)
if condition:
    ...

# Bad
return (x, y)  # Unnecessary parens
if (condition):  # Unnecessary parens
    ...
```

## 3.4 Indentation

4 spaces per level, never tabs. Configure your editor to insert spaces when you press Tab.

### Continuation Alignment

```python
# Good - aligned with opening delimiter
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Good - hanging indent (4 spaces)
def long_function_name(
    var_one: int,
    var_two: str,
    var_three: list[int],
    var_four: dict[str, Any],
) -> None:
    print(var_one)

# Good - hanging indent in function call
result = some_function_that_takes_arguments(
    "argument one",
    "argument two",
    "argument three",
)

# Bad - no hanging indent
def long_function_name(
var_one: int, var_two: str) -> None:  # Not indented
    print(var_one)

# Bad - misaligned
foo = long_function_name(var_one, var_two,
    var_three, var_four)  # Should align with opening paren
```

### Closing Brackets

```python
# Good - on same line as last element
my_list = [
    1, 2, 3,
    4, 5, 6,
]

# Good - on own line, aligned with first character of line starting construct
my_list = [
    1, 2, 3,
    4, 5, 6,
]
```

## 3.4.1 Trailing Commas

Use trailing commas when the closing bracket is on a separate line. This signals auto-formatters to use one-item-per-line style.

```python
# Good - signals formatter to expand
config = {
    "name": "app",
    "version": "1.0",
    "debug": True,
}

# Good - single line, no trailing comma
config = {"name": "app", "version": "1.0"}

# Bad - multi-line without trailing comma (causes messy diffs on additions)
config = {
    "name": "app",
    "version": "1.0",
    "debug": True
}
```

## 3.5 Blank Lines

- Two blank lines between top-level definitions (functions, classes)
- One blank line between method definitions
- One blank line after class docstring before first method
- No blank line after `def` line

```python
# Good
class MyClass:
    """Class docstring."""

    def __init__(self) -> None:
        self.value = 0

    def method_one(self) -> None:
        ...

    def method_two(self) -> None:
        ...


def top_level_function() -> None:
    ...


def another_function() -> None:
    ...

# Bad
class MyClass:
    """Class docstring."""
    def __init__(self) -> None:  # Missing blank after docstring
        self.value = 0
    def method_one(self) -> None:  # Missing blank between methods
        ...
```

## 3.6 Whitespace

### Inside Brackets

No whitespace immediately inside parentheses, brackets, or braces.

```python
# Good
spam(ham[1], {eggs: 2})
result = items[0]

# Bad
spam( ham[ 1 ], { eggs: 2 } )
result = items[ 0 ]
```

### Before Commas and Colons

No whitespace before comma, semicolon, or colon.

```python
# Good
if x == 4:
    print(x, y)
    x, y = y, x

# Bad
if x == 4 :
    print(x , y)
    x , y = y , x
```

### Around Operators

Spaces around binary operators. No spaces around `=` in keyword arguments (except with type annotations).

```python
# Good
x = 1
y = x + 1
z = x * 2 - 1

def function(default: int = 0) -> None:
    ...

function(value=42)

# Bad
x=1
y = x+1
z = x * 2-1

def function(default: int=0) -> None:  # Need space with annotation
    ...

function(value = 42)  # No space without annotation
```

### Slices

No spaces in slices.

```python
# Good
items[1:4]
items[::2]
items[1:4:2]

# Bad
items[1 : 4]
items[ ::2]
```

## 3.7 Shebang Line

Use `#!/usr/bin/env python3` for executable scripts. Omit for non-executable modules.

```python
#!/usr/bin/env python3
"""Module docstring."""

import sys
...
```

## 3.8 Comments and Docstrings

Use triple double-quotes `"""` for all docstrings.

### Module Docstrings

```python
"""One-line summary of module purpose.

Longer description if needed. Describe the module's contents
and typical usage.

Example:
    from mymodule import something
    result = something.do_work()
"""
```

### Function Docstrings

```python
def fetch_data(
    url: str,
    timeout: float = 30.0,
    *,
    retry: bool = True,
) -> dict[str, Any]:
    """Fetch JSON data from a URL.

    Makes an HTTP GET request to the specified URL and returns
    the parsed JSON response.

    Args:
        url: The URL to fetch from.
        timeout: Request timeout in seconds.
        retry: Whether to retry failed requests.

    Returns:
        The parsed JSON response as a dictionary.

    Raises:
        ValueError: If the URL is malformed.
        TimeoutError: If the request times out after all retries.
    """
```

### Class Docstrings

```python
class DataProcessor:
    """Process and transform data records.

    This class handles the loading, validation, and transformation
    of data records from various sources.

    Attributes:
        source: The data source identifier.
        records: List of processed records.
    """

    def __init__(self, source: str) -> None:
        """Initialize the processor.

        Args:
            source: The data source identifier.
        """
        self.source = source
        self.records: list[Record] = []
```

### Inline Comments

Use sparingly. Separate by at least two spaces from code.

```python
# Good
x = x + 1  # Compensate for border offset

# Bad
x = x + 1 # Too close
x = x + 1  # increment x (obvious, don't comment)
```

## 3.10 Strings

### Formatting

Use f-strings for most formatting. Use `%` or `.format()` when f-strings aren't appropriate.

```python
# Good
name = "World"
greeting = f"Hello, {name}!"

count = 42
message = f"Found {count} items"

# Acceptable for complex formatting
template = "Name: {name}, Age: {age}"
result = template.format(name=user.name, age=user.age)
```

### Quote Consistency

Pick either single `'` or double `"` quotes and be consistent within a file. Use `"""` for docstrings.

### Multi-line Strings

```python
# Good
long_text = (
    "This is a very long piece of text that needs to span "
    "multiple lines for readability purposes."
)

# Good for preserving formatting
query = """\
SELECT name, email
FROM users
WHERE active = true
ORDER BY name
"""

# Bad - implicit concatenation can be confusing
message = "Hello " "World"  # Avoid
```

### No Loop Concatenation

```python
# Good
items = ["a", "b", "c"]
result = "".join(items)

# Good
parts: list[str] = []
for item in items:
    parts.append(transform(item))
result = "".join(parts)

# Bad - O(n^2) complexity
result = ""
for item in items:
    result += transform(item)
```

## 3.10.1 Logging

Pass placeholders to logging functions. Don't use f-strings.

```python
# Good
import logging

logger = logging.getLogger(__name__)

logger.info("Processing user %s", user_id)
logger.debug("Request params: %r", params)
logger.error("Failed to connect to %s:%d", host, port)

# Bad
logger.info(f"Processing user {user_id}")  # Defeats lazy evaluation
logger.error("Failed to connect to " + host)  # String concatenation
```

### Why This Matters

1. Lazy evaluation: Format string isn't rendered if log level is disabled
2. Log aggregation: Tools can group by pattern "Processing user %s"
3. Structured logging: Some systems parse format strings

## 3.10.2 Error Messages

Error messages should clearly identify the problem and include relevant values.

```python
# Good
raise ValueError(f"Expected positive integer, got {value=}")
raise FileNotFoundError(f"Config file not found: {path}")
raise TypeError(f"Expected str, got {type(value).__name__}")

# Bad
raise ValueError("Invalid value")  # No context
raise ValueError(f"Invalid")  # Even worse
```

## 3.11 Files and Resources

Always use `with` statements for files and resources.

```python
# Good
with open("data.txt") as f:
    content = f.read()

with open("output.txt", "w") as f:
    f.write(result)

# Good - multiple resources
with open("input.txt") as infile, open("output.txt", "w") as outfile:
    for line in infile:
        outfile.write(transform(line))

# Good - contextlib for non-context-manager resources
from contextlib import closing
from urllib.request import urlopen

with closing(urlopen("https://example.com")) as page:
    content = page.read()

# Bad
f = open("data.txt")
content = f.read()
f.close()  # May not execute on exception
```

## 3.12 TODO Comments

Format: `# TODO: link - explanation`

```python
# Good
# TODO: github.com/org/repo/issues/123 - Add retry logic for network errors
# TODO: b/12345 - Refactor when API v2 is available

# Bad
# TODO: add caching
# TODO(username): fix this later
```

## 3.13 Import Formatting

### Order

1. `from __future__ import` statements
2. Standard library imports
3. Third-party imports
4. Local/application imports

Blank line between each group. Sort lexicographically within each group.

```python
# Good
from __future__ import annotations

import os
import sys
from collections.abc import Callable, Sequence
from typing import Any

import numpy as np
import requests
from sqlalchemy import Column, Integer, String

from myapp.models import User
from myapp.utils import helpers
```

### One Import Per Line

```python
# Good
import os
import sys

# Acceptable for typing
from typing import Any, Callable, TypeVar

# Bad
import os, sys
```

## 3.14 Statements

One statement per line. Short conditional bodies can be on the same line if there's no `else`.

```python
# Good
if foo:
    bar()

# Acceptable (short, no else)
if foo: bar()

# Bad
if foo: bar()
else: baz()  # Has else clause

if foo:
    bar(); baz()  # Multiple statements
```

## 3.15 Getters and Setters

Use only when access involves computation or validation. For simple attribute access, make the attribute public.

```python
# Good - validation needed
class User:
    def __init__(self, email: str) -> None:
        self._email = ""
        self.email = email  # Uses setter

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value:
            raise ValueError(f"Invalid email: {value}")
        self._email = value

# Good - simple attribute, no getter/setter needed
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x  # Public attribute
        self.y = y

# Bad - unnecessary accessor
class Point:
    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    def get_x(self) -> float:  # Unnecessary
        return self._x
```

## 3.16 Naming

### Conventions Table

| Type | Public | Internal |
|------|--------|----------|
| Package | `lower_with_under` | — |
| Module | `lower_with_under` | `_lower_with_under` |
| Class | `CapWords` | `_CapWords` |
| Exception | `CapWords` | — |
| Function | `lower_with_under()` | `_lower_with_under()` |
| Constant | `CAPS_WITH_UNDER` | `_CAPS_WITH_UNDER` |
| Variable | `lower_with_under` | `_lower_with_under` |
| Method | `lower_with_under()` | `_lower_with_under()` |
| Parameter | `lower_with_under` | — |

### Names to Avoid

- Single characters except `i`, `j`, `k` (loops), `e` (exceptions), `f` (files)
- Dashes in package/module names
- `__double_leading_and_trailing_underscore__` names (reserved)
- Type-inclusive names like `users_list` or `name_string`

```python
# Good
users = []
name = "Alice"
for i, item in enumerate(items):
    ...

# Bad
l = []  # Looks like 1
O = 0  # Looks like 0
users_list = []  # Type in name
```

### Test Method Names

```python
# Good
def test_parse_valid_input(self) -> None:
    ...

def test_parse_empty_string_raises_value_error(self) -> None:
    ...

# Pattern: test_<method>_<scenario>_<expected>
```

## 3.16.3 File Naming

- Use `.py` extension
- Use `lower_with_under.py`
- No dashes (can't be imported)

```bash
# Good
my_module.py
data_processor.py

# Bad
my-module.py  # Can't import
MyModule.py   # Inconsistent with convention
```

## 3.17 Main

Guard main execution. Put logic in a `main()` function.

```python
# Good
def main() -> None:
    """Run the application."""
    config = load_config()
    app = Application(config)
    app.run()


if __name__ == "__main__":
    main()
```

This enables:
- Importing the module without side effects
- Testing the `main()` function
- Running with `python -m module`

## 3.18 Function Length

Prefer small, focused functions. No hard limit, but reconsider functions exceeding ~40 lines.

### Signs a Function Is Too Long

- Multiple levels of nesting
- Many local variables
- Multiple conceptual "sections"
- Hard to name accurately

### Splitting Strategies

```python
# Before - too long
def process_order(order: Order) -> None:
    # 1. Validate
    if not order.items:
        raise ValueError("Empty order")
    for item in order.items:
        if item.quantity <= 0:
            raise ValueError(f"Invalid quantity for {item.name}")
    # ... 20 more lines of validation

    # 2. Calculate totals
    subtotal = sum(item.price * item.quantity for item in order.items)
    tax = subtotal * 0.08
    # ... 15 more lines of calculation

    # 3. Apply discounts
    # ... 20 more lines

    # 4. Save
    # ... 10 more lines

# After - split into focused functions
def process_order(order: Order) -> None:
    _validate_order(order)
    totals = _calculate_totals(order)
    totals = _apply_discounts(order, totals)
    _save_order(order, totals)

def _validate_order(order: Order) -> None:
    ...

def _calculate_totals(order: Order) -> OrderTotals:
    ...
```
