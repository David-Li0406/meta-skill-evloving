# Modern Python: 3.13 to 3.14

Free-threaded mode, new stdlib features, and newer syntax.

---
## Free-Threaded Python (3.13+)

**Problem**: You need true parallel execution for CPU-bound tasks without multiprocessing overhead.

**Solution**:
```python
# Build/install with: --disable-gil
# True parallelism for CPU-bound threads

import threading

# These now run in parallel on multiple cores
threads = [
    threading.Thread(target=cpu_intensive, args=(data,))
    for data in chunks
]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

**Tip**: Free-threaded mode must be enabled at build time. It's experimental in 3.13 but enables true CPU parallelism with threads.

---

## Copy and Replace (3.13+)

**Problem**: You want to create a copy of an object with some fields changed, especially for dataclasses.

**Solution**:
```python
from copy import replace
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

alice = User("Alice", 30)
bob = replace(alice, name="Bob")
# User(name='Bob', age=30)
```

**Tip**: `replace()` works with any object that has `__replace__()`, including dataclasses, namedtuples, and custom classes.

---

## Deprecated Decorator (3.13+)

**Problem**: You need to mark functions as deprecated with proper warnings.

**Solution**:
```python
from warnings import deprecated

@deprecated("Use new_function() instead")
def old_function():
    ...

old_function()  # Emits DeprecationWarning
```

**Tip**: The decorator provides a standard way to deprecate APIs, making migration paths clear to users.

---

## Template Strings (3.14+)

**Problem**: You want safe, inspectable string templates that aren't immediately evaluated like f-strings.

**Solution**:
```python
name = "Alice"
age = 30

# Template object (not evaluated string)
template = t"Hello {name}, age {age}"

# Safer than f-strings for user templates
# Can inspect/transform before rendering
print(template.strings)       # ("Hello ", ", age ", "")
print(template.interpolations) # (Interpolation(name, ...), ...)
```

**Tip**: t-strings return template objects you can inspect and control, preventing injection attacks in user-provided templates.

---

## Deferred Annotation Evaluation (3.14+)

**Problem**: You need forward references in type hints without quote strings.

**Solution**:
```python
# Forward references work without quotes!
class Node:
    def __init__(self, value: int):
        self.value = value
        self.next: Node | None = None  # No "Node" quotes needed

    def append(self, node: Node) -> Node:
        self.next = node
        return node
```

**Tip**: Annotations are evaluated lazily, so you can reference classes before they're fully defined without string quotes.

---

## Time-Sortable UUIDs (3.14+)

**Problem**: You need UUIDs that maintain chronological order for database efficiency.

**Solution**:
```python
from uuid import uuid7

id1 = uuid7()
id2 = uuid7()

assert id1 < id2  # Chronologically sortable!
# Great for database primary keys
```

**Tip**: UUID v7 includes a timestamp, making them naturally sortable and more database-friendly than UUID v4.

---

## Pathlib Copy and Move (3.14+)

**Problem**: You want to copy or move files using pathlib instead of shutil.

**Solution**:
```python
from pathlib import Path

src = Path("file.txt")
src.copy(Path("backup/file.txt"))
src.move(Path("archive/file.txt"))

# Directory copy
Path("src/").copy(Path("backup/"), recursive=True)
```

**Tip**: These methods integrate file operations directly into Path objects, eliminating the need for separate shutil imports.

---

## Simplified Exception Syntax (3.14+)

**Problem**: You want to catch multiple exception types without tuple syntax.

**Solution**:
```python
# Multiple exception types without parentheses
try:
    risky_operation()
except ValueError, TypeError, KeyError:  # No tuple needed!
    handle_error()
```

**Tip**: The comma-separated syntax matches the consistency of other Python syntax and reduces visual clutter.

