#!/usr/bin/env python3
"""Scaffold a Python project with uv, hatchling, pytest, and onion architecture."""

import argparse
import os
import re
from pathlib import Path


def to_package_name(project_name: str) -> str:
    """Convert project name to valid Python package name."""
    return re.sub(r"[^a-z0-9]", "_", project_name.lower()).strip("_")


def create_pyproject_toml(project_name: str, package_name: str) -> str:
    return f'''[project]
name = "{project_name}"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "injector>=0.23.0",
    "pydantic>=2.12.0",
]

[dependency-groups]
dev = [
    "pyright>=1.1.407",
    "pytest>=9.0.2",
    "pytest-cov>=6.0",
    "ruff>=0.14.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{package_name}"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-v"

[tool.pyright]
include = ["src"]
venv = ".venv"
typeCheckingMode = "standard"

[tool.ruff]
src = ["src"]
line-length = 88
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
'''


def create_readme(project_name: str) -> str:
    return f'''# {project_name}

## Setup

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync
```

## Development

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Type check
uv run pyright

# Format code
uv run ruff format src tests

# Lint code
uv run ruff check src tests --fix
```

## Architecture

This project follows onion architecture with four layers:

- **domain/** - Core business logic, entities, and repository interfaces
- **application/** - Use cases and application services
- **infrastructure/** - External adapters (database, APIs, config)
- **presentation/** - Entry points (CLI, REST API)

Dependencies flow inward: presentation → infrastructure → application → domain
'''


def create_conftest(package_name: str) -> str:
    return f'''"""Shared pytest fixtures."""

import pytest


@pytest.fixture
def sample_fixture():
    """Example fixture - replace with real fixtures."""
    return {{"key": "value"}}
'''


def create_init(docstring: str = "") -> str:
    if docstring:
        return f'"""{docstring}"""\n'
    return ""


def create_entity_example() -> str:
    return '''"""Example domain entity using Pydantic."""

from pydantic import BaseModel, Field
from uuid import uuid4


class Entity(BaseModel):
    """Base class for domain entities with identity."""

    id: str = Field(default_factory=lambda: str(uuid4()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
'''


def create_value_object_example() -> str:
    return '''"""Example domain value objects using Pydantic."""

from pydantic import BaseModel, Field


class ValueObject(BaseModel):
    """Base class for value objects - immutable and compared by value."""

    model_config = {"frozen": True}


class Money(ValueObject):
    """Monetary value with currency."""

    amount: int = Field(gt=0, description="Amount in smallest unit (e.g., cents)")
    currency: str = Field(min_length=3, max_length=3, description="ISO 4217 currency code")

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} vs {other.currency}")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def subtract(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} vs {other.currency}")
        return Money(amount=self.amount - other.amount, currency=self.currency)


class Email(ValueObject):
    """Email address value object."""

    value: str = Field(pattern=r"^[\\w.-]+@[\\w.-]+\\.\\w+$")
'''


def create_repository_interface() -> str:
    return '''"""Repository interface (port) for domain entities."""

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Abstract repository defining persistence operations."""

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[T]:
        """Find entity by ID."""
        ...

    @abstractmethod
    def save(self, entity: T) -> T:
        """Persist entity."""
        ...

    @abstractmethod
    def delete(self, id: str) -> None:
        """Remove entity by ID."""
        ...
'''


def create_domain_exceptions() -> str:
    return '''"""Domain-specific exceptions."""


class DomainException(Exception):
    """Base exception for domain errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EntityNotFoundError(DomainException):
    """Raised when an entity is not found."""

    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with id '{entity_id}' not found")


class ValidationError(DomainException):
    """Raised when domain validation fails."""

    def __init__(self, message: str, field: str | None = None):
        self.field = field
        super().__init__(message)


class DuplicateEntityError(DomainException):
    """Raised when attempting to create a duplicate entity."""

    def __init__(self, entity_type: str, field: str, value: str):
        self.entity_type = entity_type
        self.field = field
        self.value = value
        super().__init__(f"{entity_type} with {field} '{value}' already exists")


class BusinessRuleViolationError(DomainException):
    """Raised when a business rule is violated."""

    pass
'''


def create_use_case_example() -> str:
    return '''"""Example use case implementation."""

from dataclasses import dataclass
from typing import Protocol


class Repository(Protocol):
    """Repository protocol for dependency injection."""

    def find_by_id(self, id: str): ...
    def save(self, entity): ...


@dataclass
class UseCaseResult:
    """Result wrapper for use case operations."""

    success: bool
    data: object = None
    error: str = None


class UseCase:
    """Base class for application use cases."""

    def execute(self, *args, **kwargs) -> UseCaseResult:
        """Execute the use case logic."""
        raise NotImplementedError
'''


def create_dto_example() -> str:
    return '''"""Data Transfer Objects for application layer."""

from pydantic import BaseModel


class BaseDTO(BaseModel):
    """Base class for DTOs - immutable data containers."""

    model_config = {"frozen": True}


class RequestDTO(BaseDTO):
    """Example request DTO."""

    pass


class ResponseDTO(BaseDTO):
    """Example response DTO."""

    success: bool
    message: str | None = None
'''


def create_persistence_model_example(package_name: str) -> str:
    return f'''"""Persistence models with domain mappers."""

from pydantic import BaseModel
from datetime import datetime

from {package_name}.domain.entities.base import Entity


class EntityModel(BaseModel):
    """Base persistence model with domain mapping methods."""

    id: str

    @classmethod
    def from_domain(cls, entity: Entity) -> "EntityModel":
        """Create persistence model from domain entity."""
        return cls(id=entity.id)

    def to_domain(self) -> Entity:
        """Convert to domain entity."""
        return Entity(id=self.id)


# Example: User persistence model
# class UserModel(BaseModel):
#     id: str
#     email: str
#     name: str
#     created_at: datetime
#
#     @classmethod
#     def from_domain(cls, entity: "User") -> "UserModel":
#         return cls(
#             id=entity.id,
#             email=entity.email,
#             name=entity.name,
#             created_at=entity.created_at,
#         )
#
#     def to_domain(self) -> "User":
#         return User(
#             id=self.id,
#             email=self.email,
#             name=self.name,
#             created_at=self.created_at,
#         )
'''


def create_config_example() -> str:
    return '''"""Application configuration."""

import os
from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration loaded from environment."""

    debug: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
'''


def create_di_module_example(package_name: str) -> str:
    return f'''"""Dependency injection module using injector."""

from injector import Injector, Module, provider, singleton

from {package_name}.infrastructure.config.settings import Config


class AppModule(Module):
    """Main application module for dependency bindings."""

    def __init__(self, config: Config):
        self._config = config

    @singleton
    @provider
    def provide_config(self) -> Config:
        return self._config

    # Add more providers here as your application grows
    # Example:
    # @singleton
    # @provider
    # def provide_user_repository(self) -> UserRepository:
    #     return InMemoryUserRepository()


def create_injector(config: Config | None = None) -> Injector:
    """Create and configure the dependency injector."""
    if config is None:
        config = Config.from_env()
    return Injector([AppModule(config)])
'''


def create_api_schemas_example(package_name: str) -> str:
    return f'''"""API schemas (request/response models) with domain mappers."""

from pydantic import BaseModel, Field
from datetime import datetime

from {package_name}.domain.entities.base import Entity


class BaseResponse(BaseModel):
    """Base class for API response models."""

    pass


class EntityResponse(BaseResponse):
    """Example API response with domain mapper."""

    id: str

    @classmethod
    def from_domain(cls, entity: Entity) -> "EntityResponse":
        """Create API response from domain entity."""
        return cls(id=entity.id)


class ErrorResponse(BaseModel):
    """API error response."""

    detail: str
    code: str | None = None


# Example: User API schemas
# class UserCreateRequest(BaseModel):
#     email: str = Field(examples=["user@example.com"])
#     name: str = Field(min_length=1, max_length=100)
#
#
# class UserResponse(BaseResponse):
#     id: str
#     email: str
#     name: str
#     created_at: datetime
#
#     @classmethod
#     def from_domain(cls, entity: "User") -> "UserResponse":
#         return cls(
#             id=entity.id,
#             email=entity.email,
#             name=entity.name,
#             created_at=entity.created_at,
#         )
'''


def create_test_example(package_name: str) -> str:
    return f'''"""Example unit test for domain layer."""

import pytest


class TestExample:
    """Example test class."""

    def test_placeholder(self):
        """Placeholder test - replace with real tests."""
        assert True

    def test_with_fixture(self, sample_fixture):
        """Example test using fixture from conftest."""
        assert sample_fixture["key"] == "value"
'''


def scaffold_project(project_name: str, output_path: Path) -> None:
    """Create the complete project structure."""
    package_name = to_package_name(project_name)
    project_dir = output_path / project_name

    # Define directory structure
    dirs = [
        f"src/{package_name}/domain/entities",
        f"src/{package_name}/domain/value_objects",
        f"src/{package_name}/domain/services",
        f"src/{package_name}/domain/repositories",
        f"src/{package_name}/application/use_cases",
        f"src/{package_name}/application/dto",
        f"src/{package_name}/infrastructure/persistence",
        f"src/{package_name}/infrastructure/external",
        f"src/{package_name}/infrastructure/config",
        f"src/{package_name}/presentation/cli",
        f"src/{package_name}/presentation/api",
        "tests/unit/domain",
        "tests/unit/application",
        "tests/integration/infrastructure",
        "tests/integration/presentation",
    ]

    # Create directories
    for d in dirs:
        (project_dir / d).mkdir(parents=True, exist_ok=True)

    # Create root files
    (project_dir / "pyproject.toml").write_text(
        create_pyproject_toml(project_name, package_name)
    )
    (project_dir / "README.md").write_text(create_readme(project_name))
    (project_dir / ".python-version").write_text("3.13\n")

    # Create __init__.py files with docstrings
    init_files = {
        f"src/{package_name}/__init__.py": f"{project_name} package.",
        f"src/{package_name}/domain/__init__.py": "Domain layer - core business logic.",
        f"src/{package_name}/domain/entities/__init__.py": "Domain entities.",
        f"src/{package_name}/domain/value_objects/__init__.py": "Domain value objects.",
        f"src/{package_name}/domain/services/__init__.py": "Domain services.",
        f"src/{package_name}/domain/repositories/__init__.py": "Repository interfaces (ports).",
        f"src/{package_name}/application/__init__.py": "Application layer - use cases.",
        f"src/{package_name}/application/use_cases/__init__.py": "Application use cases.",
        f"src/{package_name}/application/dto/__init__.py": "Data transfer objects.",
        f"src/{package_name}/infrastructure/__init__.py": "Infrastructure layer - adapters.",
        f"src/{package_name}/infrastructure/persistence/__init__.py": "Persistence adapters.",
        f"src/{package_name}/infrastructure/external/__init__.py": "External API adapters.",
        f"src/{package_name}/infrastructure/config/__init__.py": "Configuration.",
        f"src/{package_name}/presentation/__init__.py": "Presentation layer - entry points.",
        f"src/{package_name}/presentation/cli/__init__.py": "CLI commands.",
        f"src/{package_name}/presentation/api/__init__.py": "API endpoints.",
        "tests/__init__.py": "",
        "tests/unit/__init__.py": "",
        "tests/unit/domain/__init__.py": "",
        "tests/unit/application/__init__.py": "",
        "tests/integration/__init__.py": "",
        "tests/integration/infrastructure/__init__.py": "",
        "tests/integration/presentation/__init__.py": "",
    }

    for path, docstring in init_files.items():
        (project_dir / path).write_text(create_init(docstring))

    # Create example files
    (project_dir / f"src/{package_name}/domain/entities/base.py").write_text(
        create_entity_example()
    )
    (project_dir / f"src/{package_name}/domain/value_objects/base.py").write_text(
        create_value_object_example()
    )
    (project_dir / f"src/{package_name}/domain/repositories/base.py").write_text(
        create_repository_interface()
    )
    (project_dir / f"src/{package_name}/domain/exceptions.py").write_text(
        create_domain_exceptions()
    )
    (project_dir / f"src/{package_name}/application/use_cases/base.py").write_text(
        create_use_case_example()
    )
    (project_dir / f"src/{package_name}/application/dto/base.py").write_text(
        create_dto_example()
    )
    (project_dir / f"src/{package_name}/infrastructure/config/settings.py").write_text(
        create_config_example()
    )
    (project_dir / f"src/{package_name}/infrastructure/config/container.py").write_text(
        create_di_module_example(package_name)
    )
    (project_dir / f"src/{package_name}/infrastructure/persistence/models.py").write_text(
        create_persistence_model_example(package_name)
    )
    (project_dir / f"src/{package_name}/presentation/api/schemas.py").write_text(
        create_api_schemas_example(package_name)
    )
    (project_dir / "tests/conftest.py").write_text(create_conftest(package_name))
    (project_dir / "tests/unit/domain/test_example.py").write_text(
        create_test_example(package_name)
    )

    print(f"✅ Created project: {project_dir}")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  uv sync")
    print(f"  uv run pytest")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a Python project with onion architecture"
    )
    parser.add_argument("name", help="Project name")
    parser.add_argument(
        "--path",
        default=".",
        help="Output directory (default: current directory)",
    )
    args = parser.parse_args()

    output_path = Path(args.path).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    scaffold_project(args.name, output_path)


if __name__ == "__main__":
    main()
