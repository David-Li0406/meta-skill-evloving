# Presentation Layer Patterns

The presentation layer provides entry points (CLI, REST API, etc.). Depends on all other layers.

## API Models (Schemas)

Define API-specific models with mapper methods to/from domain entities or DTOs:

```python
from pydantic import BaseModel, Field
from datetime import datetime

from your_app.domain.entities.user import User
from your_app.application.dto.user import UserDTO


class UserCreateRequest(BaseModel):
    """API request model for creating a user."""

    email: str = Field(examples=["user@example.com"])
    name: str = Field(min_length=1, max_length=100, examples=["John Doe"])


class UserResponse(BaseModel):
    """API response model for user data."""

    id: str
    email: str
    name: str
    created_at: datetime

    @classmethod
    def from_domain(cls, entity: User) -> "UserResponse":
        """Create API response from domain entity."""
        return cls(
            id=entity.id,
            email=entity.email,
            name=entity.name,
            created_at=entity.created_at,
        )

    @classmethod
    def from_dto(cls, dto: UserDTO) -> "UserResponse":
        """Create API response from DTO."""
        return cls(
            id=dto.id,
            email=dto.email,
            name=dto.name,
            created_at=dto.created_at,
        )


class UserListResponse(BaseModel):
    """API response model for paginated user list."""

    items: list[UserResponse]
    total: int
    page: int
    page_size: int


class ErrorResponse(BaseModel):
    """API error response."""

    detail: str
    code: str | None = None
```

## REST API with FastAPI

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from injector import Injector

from your_app.infrastructure.config import AppConfig, AppModule
from your_app.application.use_cases.create_user import CreateUserUseCase, CreateUserRequest
from your_app.presentation.api.schemas import UserCreateRequest, UserResponse, ErrorResponse


# Global injector instance
injector: Injector | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global injector
    config = AppConfig.from_env()
    injector = Injector([AppModule(config)])
    yield


app = FastAPI(title="User Service", lifespan=lifespan)


def get_injector() -> Injector:
    assert injector is not None
    return injector


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(
    request: UserCreateRequest,
    inj: Injector = Depends(get_injector),
):
    use_case = inj.get(CreateUserUseCase)
    result = use_case.execute(
        CreateUserRequest(email=request.email, name=request.name)
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)

    # Fetch created user and map to response
    user = inj.get(GetUserUseCase).execute(result.user_id)
    return UserResponse.from_domain(user)


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    inj: Injector = Depends(get_injector),
):
    use_case = inj.get(GetUserUseCase)
    user = use_case.execute(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse.from_domain(user)
```

## CLI with Click

```python
import click
from injector import Injector

from your_app.infrastructure.config import AppConfig, AppModule
from your_app.application.use_cases.create_user import CreateUserUseCase, CreateUserRequest


def create_injector() -> Injector:
    config = AppConfig.from_env()
    return Injector([AppModule(config)])


@click.group()
@click.pass_context
def cli(ctx):
    """Application CLI."""
    ctx.obj = create_injector()


@cli.command()
@click.argument("email")
@click.argument("name")
@click.pass_context
def create_user(ctx, email: str, name: str):
    """Create a new user."""
    use_case = ctx.obj.get(CreateUserUseCase)
    result = use_case.execute(CreateUserRequest(email=email, name=name))

    if result.success:
        click.echo(f"Created user: {result.user_id}")
    else:
        click.echo(f"Error: {result.error}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    cli()
```

## Entry Point (main.py)

```python
"""Application entry point."""

import sys


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        import uvicorn
        from your_app.presentation.api.main import app

        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        from your_app.presentation.cli.main import cli

        cli()


if __name__ == "__main__":
    main()
```

## Error Handling

Convert domain exceptions to HTTP responses. Domain exceptions are defined in the domain layer; the presentation layer maps them to appropriate status codes:

```python
from fastapi import Request
from fastapi.responses import JSONResponse

from your_app.domain.exceptions import (
    DomainException,
    EntityNotFoundError,
    ValidationError,
    DuplicateEntityError,
    BusinessRuleViolationError,
)


@app.exception_handler(EntityNotFoundError)
async def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message, "code": "NOT_FOUND"},
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message, "code": "VALIDATION_ERROR", "field": exc.field},
    )


@app.exception_handler(DuplicateEntityError)
async def duplicate_entity_handler(request: Request, exc: DuplicateEntityError):
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message, "code": "DUPLICATE_ENTITY"},
    )


@app.exception_handler(BusinessRuleViolationError)
async def business_rule_handler(request: Request, exc: BusinessRuleViolationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.message, "code": "BUSINESS_RULE_VIOLATION"},
    )


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    """Catch-all for any unhandled domain exceptions."""
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message, "code": "DOMAIN_ERROR"},
    )
```

## Testing Presentation Layer

```python
import pytest
from fastapi.testclient import TestClient
from injector import Injector, Module, singleton
from unittest.mock import Mock

from your_app.presentation.api.main import app, get_injector
from your_app.application.use_cases.create_user import CreateUserUseCase, CreateUserResponse


class TestModule(Module):
    def __init__(self):
        self.mock_use_case = Mock(spec=CreateUserUseCase)

    def configure(self, binder):
        binder.bind(CreateUserUseCase, to=self.mock_use_case, scope=singleton)


@pytest.fixture
def test_module():
    return TestModule()


@pytest.fixture
def test_injector(test_module):
    return Injector([test_module])


@pytest.fixture
def client(test_injector):
    app.dependency_overrides[get_injector] = lambda: test_injector
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_user_success(client, test_module):
    test_module.mock_use_case.execute.return_value = CreateUserResponse(
        success=True, user_id="123"
    )

    response = client.post("/users", json={"email": "test@example.com", "name": "Test"})

    assert response.status_code == 201
    assert response.json()["id"] == "123"
```

## Rules

1. **API models with mappers** - `from_domain()` and `from_dto()` on response models
2. **Domain entities stay clean** - No serialization concerns in domain layer
3. **Validate at API boundary** - Use Pydantic Field constraints on request models
4. **Keep controllers thin** - Delegate to use cases, map results to responses
5. **Use injector.get()** - Resolve dependencies from the injector instance
