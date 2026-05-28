# Import Resolution Errors

## import: Check for import issues

**Error Code**: `[import]`

**Configuration**: Enabled by default

**Type Safety Principle**: All imported modules must be resolvable.

### What This Error Prevents

MyPy generates an error if it can't resolve an import statement. This is a parent error code of `import-not-found` and `import-untyped`.

### When This Is an Error

```python
# Error: Cannot find implementation or library stub for module named "unknown_module" [import]
import unknown_module
```

### Configuration Options

Configure with `ignore_missing_imports`:

```ini
[mypy]
ignore_missing_imports = True
```

---

## import-not-found: Check import target can be found

**Error Code**: `[import-not-found]`

**Configuration**: Enabled by default

**Type Safety Principle**: Imported module sources must be accessible.

### When This Is an Error

```python
# Error: Cannot find implementation or library stub for module named "m0dule_with_typo" [import-not-found]
import m0dule_with_typo

# Or with typo in from import
from unknown_package import something
```

### Examples of Corrected Code

```python
# Correct import
import os
from typing import List

# Or ensure package is installed
import numpy  # requires: pip install numpy
```

### Configuration Options

```ini
[mypy]
ignore_missing_imports = True
```

---

## import-untyped: Check import has type annotations

**Error Code**: `[import-untyped]`

**Configuration**: Enabled by default

**Type Safety Principle**: Imported modules should provide type information.

### When This Is an Error

```python
# Error: Library stubs not installed for "bs4" [import-untyped]
import bs4

# Error: Skipping analyzing "no_py_typed": module missing library stubs or py.typed marker [import-untyped]
import no_py_typed
```

### Examples of Corrected Code

```python
# Install type stubs
# pip install types-beautifulsoup4
import bs4  # Now OK if stubs installed

# Or use typed library
import requests  # Has type information
```

### Configuration Options

```ini
[mypy]
ignore_missing_imports = True

# Or allow untyped
disallow_untyped_calls = False
```
