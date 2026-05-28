# Layer Structure Reference

## Domain Layer

The innermost layer - **zero external dependencies**.

### Entities

```python
# domain/entities/user.py
from dataclasses import dataclass
from typing import Self

@dataclass
class User:
    id: UserId
    email: Email
    password_hash: PasswordHash
    role: UserRole
    is_active: bool = True

    @classmethod
    def create(cls, email: Email, password_hash: PasswordHash) -> Self:
        return cls(
            id=UserId.generate(),
            email=email,
            password_hash=password_hash,
            role=UserRole.USER,
        )

    def activate(self) -> None:
        if self.is_active:
            raise UserAlreadyActiveError()
        self.is_active = True

    def deactivate(self) -> None:
        if not self.is_active:
            raise UserAlreadyInactiveError()
        self.is_active = False
```

### Value Objects

```python
# domain/value_objects/email.py
from dataclasses import dataclass
import re

@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', self.value):
            raise InvalidEmailError(f"Invalid email: {self.value}")
```

### Domain Ports

```python
# domain/ports/password_hasher.py
from typing import Protocol

class PasswordHasher(Protocol):
    async def hash(self, password: str) -> PasswordHash: ...
    async def verify(self, password: str, hash: PasswordHash) -> bool: ...
```

### Domain Services

```python
# domain/services/user_service.py
class UserService:
    def __init__(
        self,
        id_generator: UserIdGenerator,
        hasher: PasswordHasher,
    ):
        self._id_gen = id_generator
        self._hasher = hasher

    async def create_user(
        self,
        email: Email,
        raw_password: str,
        role: UserRole,
    ) -> User:
        password_hash = await self._hasher.hash(raw_password)
        return User(
            id=self._id_gen.generate(),
            email=email,
            password_hash=password_hash,
            role=role,
        )
```

---

## Application Layer

Orchestrates use cases, depends only on Domain.

### Commands (Write Use Cases)

```python
# application/commands/activate_user.py
@dataclass(frozen=True)
class ActivateUserCommand:
    user_id: UUID

class ActivateUserInteractor:
    def __init__(
        self,
        user_repo: UserRepository,
        tx: TransactionManager,
    ):
        self._repo = user_repo
        self._tx = tx

    async def execute(self, cmd: ActivateUserCommand) -> None:
        user = await self._repo.get_by_id(UserId(cmd.user_id))
        if not user:
            raise UserNotFoundError(cmd.user_id)

        user.activate()  # Domain logic
        await self._repo.save(user)
        await self._tx.commit()
```

### Queries (Read Use Cases)

```python
# application/queries/list_users.py
@dataclass(frozen=True)
class ListUsersQuery:
    limit: int = 20
    offset: int = 0

class ListUsersQueryService:
    def __init__(self, reader: UserQueryGateway):
        self._reader = reader

    async def execute(self, query: ListUsersQuery) -> list[UserDTO]:
        return await self._reader.list_all(
            limit=query.limit,
            offset=query.offset,
        )
```

### Application Ports

```python
# application/ports/user_repository.py
class UserRepository(Protocol):
    """Write operations"""
    async def get_by_id(self, id: UserId) -> User | None: ...
    async def save(self, user: User) -> None: ...

# application/ports/user_query_gateway.py
class UserQueryGateway(Protocol):
    """Read operations - returns DTOs, not entities"""
    async def get_by_id(self, id: UUID) -> UserDTO | None: ...
    async def list_all(self, limit: int, offset: int) -> list[UserDTO]: ...

# application/ports/transaction_manager.py
class TransactionManager(Protocol):
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
```

---

## Infrastructure Layer

Implements Ports, connects to external systems.

### Adapters

```python
# infrastructure/adapters/postgres_user_repository.py
class PostgresUserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: UserId) -> User | None:
        stmt = select(UserModel).where(UserModel.id == id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def save(self, user: User) -> None:
        model = self._to_model(user)
        self._session.add(model)
        await self._session.flush()

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=UserId(model.id),
            email=Email(model.email),
            password_hash=PasswordHash(model.password_hash),
            role=UserRole(model.role),
            is_active=model.is_active,
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id.value,
            email=entity.email.value,
            password_hash=entity.password_hash.value,
            role=entity.role.value,
            is_active=entity.is_active,
        )
```

### External Integrations

```python
# infrastructure/integrations/grpc_character_client.py
class GrpcCharacterClient:
    def __init__(self, channel: grpc.aio.Channel):
        self._stub = CharacterServiceStub(channel)

    async def get_character(self, character_id: str) -> CharacterDTO:
        request = GetCharacterRequest(id=character_id)
        response = await self._stub.GetCharacter(request)
        return CharacterDTO(
            id=response.id,
            name=response.name,
            personality=response.personality,
        )
```

---

## Presentation Layer

HTTP handling, request/response transformation.

### Controllers

```python
# presentation/http/controllers/users.py
router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=201)
async def create_user(
    request: CreateUserRequest,
    interactor: CreateUserInteractor = Depends(get_create_user_interactor),
) -> CreateUserResponse:
    user_id = await interactor.execute(
        CreateUserCommand(
            email=request.email,
            password=request.password,
        )
    )
    return CreateUserResponse(id=user_id.value)

@router.get("/")
async def list_users(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: ListUsersQueryService = Depends(get_list_users_service),
) -> list[UserResponse]:
    users = await service.execute(ListUsersQuery(limit=limit, offset=offset))
    return [UserResponse.from_dto(u) for u in users]
```

### Request/Response Schemas

```python
# presentation/http/schemas/user.py
class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class CreateUserResponse(BaseModel):
    id: UUID

class UserResponse(BaseModel):
    id: UUID
    email: str
    role: str
    is_active: bool

    @classmethod
    def from_dto(cls, dto: UserDTO) -> Self:
        return cls(
            id=dto.id,
            email=dto.email,
            role=dto.role.value,
            is_active=dto.is_active,
        )
```

---

## Dependency Flow Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                     COMPILE-TIME DEPENDENCIES                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Presentation ───────▶ Application ───────▶ Domain              │
│       │                     │                  ▲                 │
│       │                     │                  │                 │
│       │                     ▼                  │                 │
│       │              Application Ports ────────┤                 │
│       │                     ▲                  │                 │
│       │                     │ implements       │                 │
│       │                     │                  │                 │
│       └──────────▶ Infrastructure ─────────────┘                │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                      RUNTIME DEPENDENCIES                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Controller ──▶ UseCase ──▶ Port ◀── Adapter ──▶ Database       │
│                             (interface)  (concrete)              │
│                                                                  │
│  DI Container wires Adapter to Port at runtime                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```
