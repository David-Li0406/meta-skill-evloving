# PEP 8 Style Guide Summary

Source: https://peps.python.org/pep-0008/

## Core Principles

- **Readability counts**: Code is read more often than written
- **Consistency matters**: Be consistent within a project, module, or function
- **Know when to break rules**: Sometimes the style guide doesn't apply

## Code Layout

**Indentation:**
- Use 4 spaces per indentation level
- Use spaces, not tabs (tabs only for existing tab-indented code)
- Continuation lines should align or use hanging indent

**Line Length:**
- Limit lines to 79 characters (100 is acceptable for modern projects)
- Limit docstrings/comments to 72 characters
- Use implicit line continuation inside parentheses, brackets, braces

**Examples:**
```python
# Good: implicit continuation
result = some_function(
    arg1, arg2, arg3,
    arg4, arg5
)

# Good: hanging indent
my_list = [
    1, 2, 3,
    4, 5, 6,
]

# Bad: no indentation distinction
result = some_function(arg1, arg2, arg3,
arg4, arg5)
```

**Blank Lines:**
- Two blank lines around top-level functions and classes
- One blank line around method definitions inside a class
- Use blank lines sparingly inside functions for logical sections

**Example:**
```python
class MyClass:
    """A class."""

    def __init__(self):
        """Initialize."""
        pass

    def method(self):
        """A method."""
        pass


def top_level_function():
    """A function."""
    pass
```

## Imports

**Import Organization:**
1. Standard library imports
2. Related third-party imports
3. Local application/library imports

Separate each group with a blank line.

**Import Style:**
```python
# Good: one import per line
import os
import sys

# Good: multiple names from same module
from subprocess import Popen, PIPE

# Bad: multiple modules on one line
import sys, os
```

**Import Ordering:**
```python
# Standard library
import os
import sys
from pathlib import Path

# Third-party
import numpy as np
import requests
from loguru import logger

# Local application
from myapp.core import process
from myapp.utils import helper
```

**Import Guidelines:**
- Prefer absolute imports over relative imports
- Avoid wildcard imports (`from module import *`)
- Put imports at the top of the file

## Whitespace

**Avoid extraneous whitespace:**
```python
# Good
spam(ham[1], {eggs: 2})
foo = (0,)
if x == 4:
    print(x, y)

# Bad
spam( ham[ 1 ], { eggs: 2 } )
foo = (0, )
if x == 4 :
    print(x , y)
```

**Around operators:**
```python
# Good: single space around operators
x = 1
y = x + 2
z = x * 2 - 1

# Good: no space for high-priority operators
i = i + 1
submitted += 1
x = x*2 - 1

# Bad: inconsistent spacing
x=1
y = x+2
z=x*2-1
```

## Naming Conventions

**Naming Styles:**
- Functions, variables, methods: `lowercase_with_underscores`
- Classes: `CapWords` (also called PascalCase)
- Constants: `UPPER_CASE_WITH_UNDERSCORES`
- Private/internal: prefix with single underscore `_internal`
- Module names: `short_lowercase` (avoid underscores if possible)

**Examples:**
```python
# Good naming
class UserAccount:
    MAX_CONNECTIONS = 100

    def __init__(self):
        self._internal_id = None
        self.user_name = None

    def get_user_name(self):
        return self.user_name

# Module-level constant
DEFAULT_TIMEOUT = 30
```

**Special Cases:**
- Use `self` for instance method first argument
- Use `cls` for class method first argument
- Avoid single letter names except for counters or iterators
- Use trailing underscore to avoid keyword conflicts: `class_`, `type_`

## Comments and Docstrings

**Comments:**
- Write complete sentences
- Update comments when code changes
- Comments should explain "why", not "what"
- Block comments start with `#` and a single space

```python
# Good: explains why
# We need to retry because the API occasionally returns 503
retry_count = 3

# Bad: states the obvious
# Set retry count to 3
retry_count = 3
```

**Docstrings:**
- Use triple double quotes `"""`
- Write docstrings for all public modules, functions, classes, methods
- One-line docstrings can be on one line
- Multi-line docstrings have summary line, blank line, then details

```python
def simple_function():
    """Do something simple."""
    pass


def complex_function(arg1, arg2):
    """Do something complex.

    This function performs a complex operation that requires
    multiple parameters and detailed explanation.

    Args:
        arg1: First argument description
        arg2: Second argument description

    Returns:
        Description of return value
    """
    pass
```

## Programming Recommendations

**Comparisons:**
```python
# Good: use "is" for None
if x is None:
    pass

# Good: use "not in"
if item not in collection:
    pass

# Bad
if x == None:
    pass
```

**Boolean checks:**
```python
# Good: rely on truthiness
if sequence:
    pass

# Bad: explicit comparison to empty
if len(sequence) > 0:
    pass
```

**Function definitions:**
```python
# Good: use def, not lambda assignment
def f(x):
    return 2 * x

# Bad: lambda assignment
f = lambda x: 2 * x
```

**Exception handling:**
```python
# Good: specific exceptions
try:
    process()
except ValueError:
    handle_error()

# Bad: bare except
try:
    process()
except:
    handle_error()
```

**Return consistency:**
```python
# Good: consistent returns
def foo(x):
    if x >= 0:
        return math.sqrt(x)
    return None

# Bad: inconsistent returns
def foo(x):
    if x >= 0:
        return math.sqrt(x)
```

**String methods:**
```python
# Good: use string methods
if filename.endswith('.py'):
    pass

# Bad: string slicing
if filename[-3:] == '.py':
    pass
```

**Type checks:**
```python
# Good: isinstance
if isinstance(obj, int):
    pass

# Bad: type comparison
if type(obj) is type(1):
    pass
```

## Modern Python Additions (3.12+)

While PEP 8 doesn't cover Python 3.12+ features specifically, follow these guidelines:

**Type hints:**
```python
def greet(name: str, count: int = 1) -> None:
    """Greet someone."""
    pass
```

**Union types:**
```python
from typing import Any
# Modern syntax (Python 3.10+)
def process(data: str | int | None = None) -> dict[str, Any]:
    pass
```

**Match statements:**
```python
match status_code:
    case 200:
        process_success()
    case 404:
        handle_not_found()
    case _:
        handle_other()
```
