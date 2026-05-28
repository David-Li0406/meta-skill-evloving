---
name: python-storage-abstraction
description: |
  Python Protocol-based storage abstraction pattern enabling dependency injection and testable file operations.
  Use this skill when implementing storage backends, adding file operations to services, or writing tests
  that need to avoid filesystem side effects. The pattern uses Python's typing.Protocol for structural
  subtyping, allowing any class with matching methods to satisfy the interface without explicit inheritance.
version: 1.0.0
tags:
  - python
  - testing
  - architecture
  - dependency-injection
  - protocols
---

# Python Storage Protocol Pattern

## Overview

The Storage Protocol Pattern provides a clean abstraction layer for file system operations in Python. It uses Python's `typing.Protocol` to define a structural interface that implementations can satisfy without explicit inheritance (duck typing with type safety).

This pattern enables:
- **Testability**: Use `MemoryStorage` in tests to avoid real filesystem operations
- **Flexibility**: Swap storage backends (file, memory, cloud) without changing business logic
- **Clean Architecture**: Services depend on abstractions, not concrete implementations

## When to Use This Skill

Activate this skill when:
- Implementing a new storage backend (cloud storage, database-backed, etc.)
- Adding file I/O operations to any service
- Writing unit tests for code that reads/writes files
- Refactoring existing code to be more testable
- Understanding dependency injection patterns in Python

## Protocol Definition

The `StorageProtocol` defines the contract all storage implementations must follow:

```python
from typing import Iterator, List, Optional, Protocol, Union
from pathlib import Path

PathLike = Union[str, Path]

class StorageProtocol(Protocol):
    """Protocol for storage operations.
    
    This protocol defines the contract for all storage backends.
    Implementations can be filesystem-based, in-memory, cloud-based, etc.
    """
    
    def read(self, path: PathLike) -> Optional[str]:
        """Read content from a path. Returns None if not found."""
        ...
    
    def read_bytes(self, path: PathLike) -> Optional[bytes]:
        """Read binary content from a path."""
        ...
    
    def write(self, path: PathLike, content: str, mode: int = 0o644) -> None:
        """Write content to a path. Creates parent directories."""
        ...
    
    def delete(self, path: PathLike) -> bool:
        """Delete a file. Returns True if deleted, False if not found."""
        ...
    
    def exists(self, path: PathLike) -> bool:
        """Check if a path exists."""
        ...
    
    def is_file(self, path: PathLike) -> bool:
        """Check if path is a file."""
        ...
    
    def is_dir(self, path: PathLike) -> bool:
        """Check if path is a directory."""
        ...
    
    def mkdir(self, path: PathLike, mode: int = 0o755, parents: bool = True) -> None:
        """Create a directory."""
        ...
    
    def glob(self, pattern: str, path: PathLike = ".") -> Iterator[str]:
        """Find files matching a glob pattern."""
        ...
    
    @property
    def root(self) -> Path:
        """Get the root/base path for this storage."""
        ...
```

### Key Design Decisions

1. **Return `None` instead of raising exceptions** for missing files
2. **Return `bool` for deletion operations** to indicate success/failure
3. **Auto-create parent directories** in write operations
4. **All paths relative to `root`** for isolation
5. **Use `PathLike` type alias** for flexibility (str or Path)

## Implementations

### FileStorage (Production)

Uses the real filesystem via `pathlib`:

```python
from context_harness.storage import FileStorage

# Storage rooted at home directory
storage = FileStorage(Path.home())
storage.write(".context-harness/config.json", '{"key": "value"}')

# Storage rooted at current directory (default)
storage = FileStorage()
storage.write("data/file.txt", "content")
```

### MemoryStorage (Testing)

In-memory implementation using dictionaries:

```python
from context_harness.storage import MemoryStorage

storage = MemoryStorage()
storage.write("config.json", '{"key": "value"}')
assert storage.read("config.json") == '{"key": "value"}'
assert storage.exists("config.json")

# Clean up between tests
storage.clear()

# Get snapshot of all contents
snapshot = storage.snapshot()  # {"config.json": "{...}"}
```

**Key Features:**
- No filesystem side effects
- Fast execution (no I/O)
- `clear()` method for test isolation
- `snapshot()` for debugging/assertions

## Using the Pattern in Services

### Service with Storage Dependency

```python
from context_harness.storage import StorageProtocol, FileStorage

class MyService:
    """Service that depends on storage abstraction."""
    
    def __init__(self, storage: StorageProtocol):
        self._storage = storage
    
    def save_data(self, name: str, data: dict) -> None:
        import json
        content = json.dumps(data, indent=2)
        self._storage.write(f"data/{name}.json", content)
    
    def load_data(self, name: str) -> Optional[dict]:
        import json
        content = self._storage.read(f"data/{name}.json")
        if content is None:
            return None
        return json.loads(content)

# Production usage
service = MyService(FileStorage())

# Test usage
from context_harness.storage import MemoryStorage
test_service = MyService(MemoryStorage())
```

## Testing with MemoryStorage

### Basic Test Pattern

```python
import pytest
from context_harness.storage import MemoryStorage

class TestMyService:
    def test_save_and_load(self) -> None:
        storage = MemoryStorage()
        service = MyService(storage)
        
        service.save_data("user", {"name": "Alice"})
        
        result = service.load_data("user")
        assert result == {"name": "Alice"}
    
    def test_load_missing_returns_none(self) -> None:
        storage = MemoryStorage()
        service = MyService(storage)
        
        result = service.load_data("nonexistent")
        assert result is None
```

### Using Snapshot for Assertions

```python
def test_multiple_writes() -> None:
    storage = MemoryStorage()
    storage.write("a.txt", "content a")
    storage.write("b.txt", "content b")
    
    snapshot = storage.snapshot()
    
    assert snapshot == {
        "a.txt": "content a",
        "b.txt": "content b",
    }
```

## Best Practices

### DO:

1. **Accept `StorageProtocol` in constructors** for dependency injection
2. **Default to `FileStorage`** in production code
3. **Use `MemoryStorage` in all unit tests** for speed and isolation
4. **Call `storage.clear()`** in test setup/teardown if reusing storage
5. **Use `Optional[str]` returns** for reads (None means not found)

### DON'T:

1. **Don't hardcode `FileStorage`** in service implementations
2. **Don't catch exceptions in storage methods** - let implementations handle them
3. **Don't assume filesystem layout** - use `root` property for base path
4. **Don't use `tmp_path` fixture unnecessarily** when `MemoryStorage` suffices

## Common Patterns

### Pattern: Factory Method for Testing

```python
class MyService:
    @classmethod
    def create_for_testing(cls) -> "MyService":
        return cls(storage=MemoryStorage())
```

### Pattern: Pytest Fixture

```python
import pytest
from context_harness.storage import MemoryStorage

@pytest.fixture
def storage() -> MemoryStorage:
    return MemoryStorage()

@pytest.fixture
def service(storage: MemoryStorage) -> MyService:
    return MyService(storage=storage)
```

## References

### Python Documentation
- [typing.Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol)
- [pathlib](https://docs.python.org/3/library/pathlib.html)

### Project Files
- `src/context_harness/storage/protocol.py` - Protocol definition
- `src/context_harness/storage/file_storage.py` - FileStorage implementation
- `src/context_harness/storage/memory_storage.py` - MemoryStorage implementation
- `tests/unit/storage/test_memory_storage.py` - Comprehensive tests

---

_Skill: python-storage-abstraction v1.0.0 | Last updated: 2025-12-30_
