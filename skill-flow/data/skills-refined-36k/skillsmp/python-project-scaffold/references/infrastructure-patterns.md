# Infrastructure Layer Patterns

The infrastructure layer implements adapters for external systems. Depends on domain and application.

## Persistence Models

Define persistence models with mapper methods to/from domain entities:

```python
from pydantic import BaseModel
from datetime import datetime

from your_app.domain.entities.user import User


class UserModel(BaseModel):
    """Persistence model for User entity."""

    id: str
    email: str
    name: str
    created_at: datetime

    @classmethod
    def from_domain(cls, entity: User) -> "UserModel":
        """Create persistence model from domain entity."""
        return cls(
            id=entity.id,
            email=entity.email,
            name=entity.name,
            created_at=entity.created_at,
        )

    def to_domain(self) -> User:
        """Convert to domain entity."""
        return User(
            id=self.id,
            email=self.email,
            name=self.name,
            created_at=self.created_at,
        )
```

## Repository Implementations

Implement domain repository interfaces using persistence models:

```python
from your_app.domain.entities.user import User
from your_app.domain.repositories.user import UserRepository
from your_app.infrastructure.persistence.models import UserModel


class InMemoryUserRepository(UserRepository):
    """In-memory implementation for testing."""

    def __init__(self):
        self._store: dict[str, UserModel] = {}

    def find_by_id(self, id: str) -> User | None:
        model = self._store.get(id)
        return model.to_domain() if model else None

    def find_by_email(self, email: str) -> User | None:
        for model in self._store.values():
            if model.email == email:
                return model.to_domain()
        return None

    def find_all(self) -> list[User]:
        return [model.to_domain() for model in self._store.values()]

    def save(self, entity: User) -> User:
        model = UserModel.from_domain(entity)
        self._store[model.id] = model
        return entity

    def delete(self, id: str) -> None:
        self._store.pop(id, None)
```

## SQLAlchemy Repository Example

```python
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Session, DeclarativeBase

from your_app.domain.entities.user import User
from your_app.domain.repositories.user import UserRepository


class Base(DeclarativeBase):
    pass


class UserTable(Base):
    """SQLAlchemy table model with domain mappers."""

    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    @classmethod
    def from_domain(cls, entity: User) -> "UserTable":
        return cls(
            id=entity.id,
            email=entity.email,
            name=entity.name,
            created_at=entity.created_at,
        )

    def to_domain(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            name=self.name,
            created_at=self.created_at,
        )


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self._session = session

    def find_by_id(self, id: str) -> User | None:
        model = self._session.query(UserTable).filter_by(id=id).first()
        return model.to_domain() if model else None

    def find_by_email(self, email: str) -> User | None:
        model = self._session.query(UserTable).filter_by(email=email).first()
        return model.to_domain() if model else None

    def find_all(self) -> list[User]:
        models = self._session.query(UserTable).all()
        return [model.to_domain() for model in models]

    def save(self, entity: User) -> User:
        model = UserTable.from_domain(entity)
        self._session.merge(model)
        self._session.commit()
        return entity

    def delete(self, id: str) -> None:
        self._session.query(UserTable).filter_by(id=id).delete()
        self._session.commit()
```

## External API Clients

Wrap external services:

```python
from pydantic import BaseModel, Field
import httpx


class EmailService(BaseModel):
    api_key: str
    base_url: str = "https://api.email.com"

    def send(self, to: str, subject: str, body: str) -> bool:
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/send",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"to": to, "subject": subject, "body": body},
            )
            return response.status_code == 200
```

## Configuration

Load from environment with validation:

```python
import os
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    host: str
    port: int = 5432
    name: str
    user: str
    password: str

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        return cls(
            host=os.environ["DB_HOST"],
            port=int(os.getenv("DB_PORT", "5432")),
            name=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
        )


class AppConfig(BaseModel):
    debug: bool = False
    database: DatabaseConfig | None = None
    api_key: str | None = None

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            database=None,  # Load as needed
            api_key=os.getenv("API_KEY"),
        )
```

## Dependency Injection with Injector

Use the `injector` library (Guice-inspired) for DI:

```python
from injector import Injector, Module, provider, singleton

from your_app.domain.repositories.user import UserRepository
from your_app.infrastructure.persistence.user import InMemoryUserRepository
from your_app.infrastructure.config.settings import AppConfig
from your_app.application.use_cases.create_user import CreateUserUseCase


class AppModule(Module):
    """Main application module for dependency bindings."""

    def __init__(self, config: AppConfig):
        self._config = config

    @singleton
    @provider
    def provide_config(self) -> AppConfig:
        return self._config

    @singleton
    @provider
    def provide_user_repository(self) -> UserRepository:
        return InMemoryUserRepository()

    @provider
    def provide_create_user_use_case(
        self, repository: UserRepository
    ) -> CreateUserUseCase:
        return CreateUserUseCase(repository)


def create_injector(config: AppConfig) -> Injector:
    return Injector([AppModule(config)])
```

## Using @inject Decorator

Mark dependencies for automatic injection:

```python
from injector import inject


class UserService:
    @inject
    def __init__(self, repository: UserRepository, config: AppConfig):
        self._repository = repository
        self._config = config

    def get_user(self, user_id: str) -> User | None:
        return self._repository.find_by_id(user_id)
```

## Testing with Injector

Override bindings for tests:

```python
import pytest
from injector import Injector, Module, singleton
from unittest.mock import Mock


class TestModule(Module):
    def configure(self, binder):
        mock_repo = Mock(spec=UserRepository)
        mock_repo.find_by_id.return_value = User(id="1", email="test@test.com", name="Test")
        binder.bind(UserRepository, to=mock_repo, scope=singleton)


@pytest.fixture
def test_injector():
    return Injector([TestModule()])


def test_user_service(test_injector):
    service = test_injector.get(UserService)
    user = service.get_user("1")
    assert user.email == "test@test.com"
```

## Rules

1. **Mapper methods on persistence models** - `from_domain()` and `to_domain()` keep mapping in infrastructure
2. **Domain entities stay clean** - No persistence concerns in domain layer
3. **Repository uses mappers** - Convert at repository boundaries
4. **Use injector modules** - Organize bindings by concern
5. **No business logic** - Only technical concerns in infrastructure
