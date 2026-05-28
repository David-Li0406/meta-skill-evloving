---
name: python-style
description: Python coding style guide and best practices. Use when writing Python code, reviewing Python files, or checking code style. Triggers on "python style", "python code", "파이썬 스타일", "코드 스타일".
---

# Python Style Guide

This skill provides Python coding style guidelines and best practices.

## Core Principles

- Follow PEP 8 (line length: 100 chars)
- Use type hints for arguments and return values
- Use Google-style docstrings
- Prefer f-strings, list/dict comprehensions, context managers
- Prefer pathlib over os.path
- Use dataclasses or pydantic for data structures

## Type Hints

```python
# Good
def process_data(items: list[str], threshold: float = 0.5) -> dict[str, int]:
    ...

# Bad
def process_data(items, threshold=0.5):
    ...
```

## Docstrings (Google Style)

```python
def fetch_data(source_id: str, limit: int = 100) -> list[dict]:
    """Fetch data from the specified source.

    Args:
        source_id: The unique identifier for the data source.
        limit: Maximum number of records to fetch.

    Returns:
        A list of dictionaries containing the fetched records.

    Raises:
        ValueError: If source_id is empty.
        ConnectionError: If unable to connect to the source.
    """
    ...
```

## Preferred Patterns

### F-strings over format()

```python
# Good
message = f"Processing {count} items for user {user_id}"

# Bad
message = "Processing {} items for user {}".format(count, user_id)
```

### List/Dict Comprehensions

```python
# Good
squares = [x**2 for x in range(10)]
user_map = {user.id: user for user in users}

# Bad
squares = []
for x in range(10):
    squares.append(x**2)
```

### Context Managers

```python
# Good
with open(file_path) as f:
    content = f.read()

# Bad
f = open(file_path)
content = f.read()
f.close()
```

### Pathlib over os.path

```python
from pathlib import Path

# Good
config_path = Path(__file__).parent / "config" / "settings.yaml"

# Bad
import os
config_path = os.path.join(os.path.dirname(__file__), "config", "settings.yaml")
```

## Data Structures

### Use Dataclasses

```python
from dataclasses import dataclass

@dataclass
class User:
    id: str
    name: str
    email: str
    is_active: bool = True
```

### Use Pydantic for Validation

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None
```

## Common Commands

### Linting and Formatting (ruff)

```bash
# Check for issues
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/

# Format code
ruff format src/ tests/
```

### Running Tests (pytest)

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_module.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

## Import Organization

```python
# Standard library
import os
from datetime import datetime
from pathlib import Path

# Third-party
import pandas as pd
from pydantic import BaseModel

# Local
from src.module import function
from src.utils import helper
```

## Error Handling

```python
# Good - specific exceptions with context
try:
    result = fetch_data(source_id)
except ConnectionError as e:
    logger.error(f"Failed to connect to source {source_id}: {e}")
    raise
except ValueError as e:
    logger.warning(f"Invalid data from source {source_id}: {e}")
    return None

# Bad - generic exception
try:
    result = fetch_data(source_id)
except Exception:
    pass
```

## Logging

```python
import logging

logger = logging.getLogger(__name__)

# Good - structured logging with context
logger.info("Processing started", extra={"source_id": source_id, "count": len(items)})
logger.error(f"Failed to process item {item_id}: {error}", exc_info=True)

# Bad - print statements
print(f"Processing {source_id}")
```
