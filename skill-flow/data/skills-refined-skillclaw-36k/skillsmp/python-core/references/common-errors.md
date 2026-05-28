# Common Python Errors

## ModuleNotFoundError
```bash
# Solution: Install the package
pip install package-name

# Or activate virtual environment
source venv/bin/activate
```

## IndentationError
```python
# Bad
def foo():
print("hello")  # Wrong indentation

# Good
def foo():
    print("hello")
```

## TypeError: ... is not subscriptable
```python
# Bad (Python <3.9)
def process(items: list[str]):  # Error in <3.9
    pass

# Good
from typing import List
def process(items: List[str]):
    pass

# Or use Python 3.9+
```

## AttributeError: 'NoneType' object has no attribute
```python
# Bad
result = get_data()
print(result.value)  # Error if result is None

# Good
result = get_data()
if result is not None:
    print(result.value)
```

## ImportError: cannot import name
```python
# Usually circular import
# Solution: Restructure code or use TYPE_CHECKING

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from other_module import SomeClass
```

## Quick Fixes

| Error | Fix |
|-------|-----|
| ModuleNotFoundError | Install package or check venv |
| IndentationError | Use 4 spaces, check consistency |
| NameError | Check variable spelling |
| KeyError | Use `.get()` method |
| TypeError | Check type hints |
| AttributeError | Check for None |
