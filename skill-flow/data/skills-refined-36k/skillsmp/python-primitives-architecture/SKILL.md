---
name: python-primitives-architecture
description: |
  Guide for implementing ContextHarness's three-layer architecture: Primitives → Services → Interfaces.
  Use this skill when creating new features, adding domain models, implementing business logic,
  or building CLI/SDK interfaces. Ensures proper separation of concerns with pure dataclass
  primitives, Result-based error handling, and protocol-based dependency injection.
version: 1.0.0
tags:
  - architecture
  - python
  - dataclasses
  - clean-code
  - separation-of-concerns
---

# Python Primitives-First Architecture

## Overview

ContextHarness follows a **primitives-first architecture** that establishes clear boundaries between domain models, services, and interfaces. This pattern enables:

1. **Testability**: Pure primitives can be tested without mocks; services can be tested with injected dependencies
2. **Reusability**: Primitives work across all interfaces (CLI, SDK, future Web)
3. **Maintainability**: Clear dependency direction prevents coupling
4. **Type Safety**: Full type annotations with Result types for explicit error handling

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                      INTERFACES                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                      │
│  │   CLI   │  │   SDK   │  │   Web   │                      │
│  └────┬────┘  └────┬────┘  └────┬────┘                      │
└───────┼────────────┼───────────┼────────────────────────────┘
        │            │           │
        ▼            ▼           ▼
┌─────────────────────────────────────────────────────────────┐
│                      SERVICES                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ SkillSvc     │  │ OAuthSvc     │  │ ConfigSvc    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
        │            │           │
        ▼            ▼           ▼
┌─────────────────────────────────────────────────────────────┐
│                     PRIMITIVES                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Skill    │  │ OAuth    │  │ Config   │  │ Result   │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Layer 1: Primitives

**Location**: `src/context_harness/primitives/`

Primitives are pure Python dataclasses representing domain concepts. They follow strict rules:

### Primitive Rules

1. **No I/O operations** - No file access, network calls, or subprocess execution
2. **No framework dependencies** - No click, rich, or other interface libraries
3. **Standard library only** - Only typing, dataclasses, enum, datetime
4. **Immutable when practical** - Use `frozen=True` for value objects
5. **Full type annotations** - Every field and method fully typed

### Creating a New Primitive

```python
# src/context_harness/primitives/my_domain.py
"""My domain primitives.

Pure dataclasses with no I/O operations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class MyStatus(Enum):
    """Status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass(frozen=True)
class MyValueObject:
    """Immutable value object.
    
    Attributes:
        id: Unique identifier
        name: Human-readable name
    """
    id: str
    name: str


@dataclass
class MyEntity:
    """Mutable entity with behavior.
    
    Attributes:
        id: Unique identifier
        status: Current status
        items: Associated items
    """
    id: str
    status: MyStatus = MyStatus.ACTIVE
    items: List[MyValueObject] = field(default_factory=list)
    
    def add_item(self, item: MyValueObject) -> None:
        """Add an item (mutation method)."""
        self.items.append(item)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MyEntity":
        """Create from dictionary (for deserialization)."""
        return cls(
            id=data["id"],
            status=MyStatus(data.get("status", "active")),
            items=[MyValueObject(**i) for i in data.get("items", [])],
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (for serialization)."""
        return {
            "id": self.id,
            "status": self.status.value,
            "items": [{"id": i.id, "name": i.name} for i in self.items],
        }
```

### Export from Package

```python
# src/context_harness/primitives/__init__.py
from context_harness.primitives.my_domain import (
    MyEntity,
    MyStatus,
    MyValueObject,
)

__all__ = [
    # ... existing exports ...
    "MyEntity",
    "MyStatus", 
    "MyValueObject",
]
```

## Layer 2: Services

**Location**: `src/context_harness/services/`

Services implement business logic. They operate on primitives and return Result types.

### Service Rules

1. **Accept primitives as input** - Parameters are primitives or Python built-ins
2. **Return Result[Primitive]** - Always return Success or Failure
3. **Inject dependencies via Protocol** - Use Protocol for I/O adapters
4. **No CLI/Web imports** - Never import interface layer code

### Creating a New Service

```python
# src/context_harness/services/my_service.py
"""My domain service.

Business logic for my domain operations.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Protocol

from context_harness.primitives import (
    ErrorCode,
    Failure,
    MyEntity,
    MyStatus,
    Result,
    Success,
)


class MyStorageProtocol(Protocol):
    """Protocol for my domain storage operations."""
    
    def load(self, id: str) -> Optional[MyEntity]: ...
    def save(self, entity: MyEntity) -> None: ...
    def list_all(self) -> List[MyEntity]: ...


class DefaultMyStorage:
    """Default file-based storage implementation."""
    
    def __init__(self, base_path: Path):
        self._base_path = base_path
    
    def load(self, id: str) -> Optional[MyEntity]:
        # Implementation with file I/O
        ...


class MyService:
    """Service for my domain operations.
    
    Example:
        service = MyService()
        result = service.create("my-entity")
        if isinstance(result, Success):
            print(result.value.id)
    """
    
    def __init__(
        self,
        storage: Optional[MyStorageProtocol] = None,
        base_path: Optional[Path] = None,
    ):
        """Initialize service.
        
        Args:
            storage: Storage implementation (for testing)
            base_path: Base path for default storage
        """
        self._storage = storage or DefaultMyStorage(
            base_path or Path.cwd()
        )
    
    def create(self, name: str) -> Result[MyEntity]:
        """Create a new entity.
        
        Args:
            name: Entity name
            
        Returns:
            Result containing MyEntity or Failure
        """
        if not name:
            return Failure(
                error="Name cannot be empty",
                code=ErrorCode.VALIDATION_ERROR,
            )
        
        entity = MyEntity(id=name, status=MyStatus.ACTIVE)
        
        try:
            self._storage.save(entity)
        except Exception as e:
            return Failure(
                error=f"Failed to save entity: {e}",
                code=ErrorCode.UNKNOWN,
            )
        
        return Success(
            value=entity,
            message=f"Created entity '{name}'",
        )
    
    def get(self, id: str) -> Result[MyEntity]:
        """Get an entity by ID.
        
        Args:
            id: Entity identifier
            
        Returns:
            Result containing MyEntity or Failure
        """
        entity = self._storage.load(id)
        
        if entity is None:
            return Failure(
                error=f"Entity '{id}' not found",
                code=ErrorCode.NOT_FOUND,
                details={"id": id},
            )
        
        return Success(value=entity)
```

## Layer 3: Interfaces

**Location**: `src/context_harness/interfaces/`

Interfaces are thin layers that call services and transform results for presentation.

### Interface Rules

1. **Thin layer** - Minimal logic, mainly orchestration
2. **Transform results** - Convert Result types to appropriate output
3. **Can depend on services and primitives** - Full access to lower layers
4. **Format-specific** - Each interface handles its own presentation

### CLI Interface Pattern

```python
# src/context_harness/interfaces/cli/my_cmd.py
"""CLI commands for my domain."""

from __future__ import annotations

import click
from rich.console import Console

from context_harness.primitives import Failure, Success
from context_harness.services import MyService

console = Console()


@click.group(name="my")
def my_group() -> None:
    """My domain commands."""
    pass


@my_group.command("create")
@click.argument("name")
def create_command(name: str) -> None:
    """Create a new entity."""
    service = MyService()
    result = service.create(name)
    
    if isinstance(result, Success):
        console.print(f"[green]✓ Created: {result.value.id}[/green]")
    else:
        console.print(f"[red]✗ {result.error}[/red]")
        raise SystemExit(1)
```

## Quick Reference

| Layer | Location | Imports From | Returns | I/O Allowed |
|-------|----------|--------------|---------|-------------|
| Primitives | `primitives/` | stdlib only | Self | ❌ No |
| Services | `services/` | primitives | Result[Primitive] | Via Protocol |
| Storage | `storage/` | primitives | Primitives | ✅ Yes |
| Interfaces | `interfaces/` | services, primitives | Format-specific | ✅ Yes |

## Project Structure Template

```
src/my_package/
├── __init__.py                 # Package version
├── primitives/                 # Pure domain models
│   ├── __init__.py            # Export all primitives
│   ├── result.py              # Result, Success, Failure, ErrorCode
│   ├── entity_a.py            # Domain entity A
│   └── entity_b.py            # Domain entity B
│
├── services/                   # Business logic
│   ├── __init__.py            # Export all services
│   ├── service_a.py           # Service for entity A
│   └── service_b.py           # Service for entity B
│
├── storage/                    # Persistence layer
│   ├── __init__.py            # Export storage classes
│   ├── protocol.py            # StorageProtocol
│   ├── file_storage.py        # File-based implementation
│   └── memory_storage.py      # In-memory (for testing)
│
└── interfaces/                 # User interfaces
    ├── __init__.py
    ├── cli/                    # Command-line interface
    │   ├── __init__.py
    │   ├── main.py            # CLI entry point
    │   └── commands/          # Command modules
    │
    └── sdk/                    # Programmatic interface
        ├── __init__.py
        └── client.py          # SDK client
```

## Common Pitfalls

### ❌ Don't: Import interfaces in services

```python
# WRONG - service importing CLI
from context_harness.interfaces.cli.formatters import format_entity

class MyService:
    def create(self, name: str) -> str:
        entity = MyEntity(id=name)
        return format_entity(entity)  # ❌ Couples to CLI
```

### ✅ Do: Return primitives from services

```python
# CORRECT - service returns primitive
class MyService:
    def create(self, name: str) -> Result[MyEntity]:
        entity = MyEntity(id=name)
        return Success(value=entity)  # ✅ Interface formats as needed
```

### ❌ Don't: Put I/O in primitives

```python
# WRONG - primitive doing I/O
@dataclass
class MyEntity:
    id: str
    
    def save(self, path: Path) -> None:  # ❌ I/O in primitive
        path.write_text(json.dumps(self.to_dict()))
```

### ✅ Do: Keep primitives pure

```python
# CORRECT - primitive has no I/O
@dataclass
class MyEntity:
    id: str
    
    def to_dict(self) -> dict:  # ✅ Pure transformation
        return {"id": self.id}

# Storage handles I/O
class Storage:
    def save(self, entity: MyEntity, path: Path) -> None:
        path.write_text(json.dumps(entity.to_dict()))
```

## References

- [ARCHITECTURE.md](../../../ARCHITECTURE.md) - Full architecture documentation
- [primitives/__init__.py](../../../src/context_harness/primitives/__init__.py) - Primitive exports
- [services/__init__.py](../../../src/context_harness/services/__init__.py) - Service exports
- [tests/unit/services/](../../../tests/unit/services/) - Service test examples

---

_Skill: python-primitives-architecture v1.0.0 | Last updated: 2025-12-30_
