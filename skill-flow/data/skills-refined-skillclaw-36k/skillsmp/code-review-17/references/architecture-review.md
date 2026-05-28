# Architecture Review Checklist

## Layer Compliance

### Domain Layer Review

```
□ No external framework imports (FastAPI, SQLAlchemy, Redis, etc.)
□ Entities have behavior, not just data (no anemic domain model)
□ Value Objects are immutable (frozen=True)
□ Value Objects validate in __post_init__
□ Domain exceptions are specific and meaningful
□ Domain services are stateless
□ No infrastructure concerns (logging, metrics) in domain
```

**Red Flags:**
```python
# BAD: Framework import in domain
from sqlalchemy.orm import Mapped  # Infrastructure leak!
from fastapi import HTTPException  # Presentation leak!

# BAD: Anemic entity
@dataclass
class User:
    id: int
    name: str
    # No methods - just a data container

# BAD: Mutable Value Object
@dataclass  # Missing frozen=True
class Email:
    value: str
```

### Application Layer Review

```
□ Use cases have single responsibility
□ Dependencies injected via constructor
□ Uses Ports (Protocol), not concrete implementations
□ Commands and Queries properly separated (CQRS)
□ Transaction management is explicit
□ No direct infrastructure usage
□ Input/Output are explicit DTOs
```

**Red Flags:**
```python
# BAD: Direct infrastructure usage
from sqlalchemy.ext.asyncio import AsyncSession

class CreateUserInteractor:
    def __init__(self, session: AsyncSession):  # Concrete type!
        self._session = session

# BAD: Multiple responsibilities
class UserInteractor:
    async def create(self, ...): ...
    async def update(self, ...): ...
    async def delete(self, ...): ...
    async def list(self, ...): ...
```

### Infrastructure Layer Review

```
□ Adapters implement Ports correctly
□ No business logic in adapters
□ Proper mapping between domain and infrastructure types
□ Error translation (infra errors → domain errors)
□ Connection/session management is proper
□ External service calls have timeout/retry
```

**Red Flags:**
```python
# BAD: Business logic in repository
class UserRepository:
    async def save(self, user: User) -> None:
        if user.email.endswith("@blocked.com"):  # Business rule!
            raise BlockedEmailError()
        ...

# BAD: Returns ORM model instead of entity
async def get_by_id(self, id: UUID) -> UserModel:  # Should return User
    return await self._session.get(UserModel, id)
```

### Presentation Layer Review

```
□ Controllers are thin (delegate to use cases)
□ Request/Response schemas are Pydantic models
□ Domain entities not exposed in API
□ Error handling translates to HTTP status codes
□ Validation done via Pydantic, not manual checks
□ No business logic in endpoints
```

**Red Flags:**
```python
# BAD: Business logic in controller
@router.post("/orders")
async def create_order(request: OrderRequest):
    if request.total > 10000:  # Business rule!
        raise HTTPException(400, "Requires approval")
    ...

# BAD: Exposing domain entity
@router.get("/users/{id}")
async def get_user(id: UUID) -> User:  # Domain entity exposed!
    return await user_service.get(id)
```

---

## Dependency Direction Check

### Allowed Dependencies Matrix

| Layer | Can Import From |
|-------|-----------------|
| Domain | Standard library only |
| Application | Domain |
| Infrastructure | Domain, Application |
| Presentation | Application |

### Import Analysis

```python
# Run this to check imports
import ast
import sys

def check_imports(file_path: str, layer: str) -> list[str]:
    violations = []
    forbidden = {
        'domain': ['fastapi', 'sqlalchemy', 'redis', 'httpx'],
        'application': ['fastapi', 'sqlalchemy', 'redis'],
        'infrastructure': [],  # Can import anything
        'presentation': ['sqlalchemy'],  # Should use DTOs
    }

    with open(file_path) as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if any(alias.name.startswith(f) for f in forbidden.get(layer, [])):
                    violations.append(f"Forbidden import: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.module and any(node.module.startswith(f) for f in forbidden.get(layer, [])):
                violations.append(f"Forbidden import: {node.module}")

    return violations
```

---

## Port/Adapter Pattern Check

### Port Definition Checklist

```
□ Defined as Protocol (not ABC)
□ Located in correct layer (domain/ports or application/ports)
□ Methods use domain types (not ORM models)
□ Single responsibility
□ Named appropriately ({Entity}Repository, {Action}er)
```

### Adapter Implementation Checklist

```
□ All Port methods implemented
□ Method signatures match Protocol exactly
□ Located in infrastructure/adapters
□ Named with technology prefix (Postgres{X}, Redis{X})
□ Has mapping methods (_to_entity, _to_model)
```

---

## CQRS Compliance Check

### Command Review

```
□ Named {Verb}{Noun}Interactor
□ Has frozen dataclass Command DTO
□ Modifies state (create/update/delete)
□ Uses write repository
□ Manages transaction (commit/rollback)
□ Returns ID or void (not full entity)
□ May publish events
```

### Query Review

```
□ Named {Verb}{Noun}QueryService
□ Has frozen dataclass Query DTO
□ Read-only (no state changes)
□ Uses QueryGateway (not write repository)
□ No transaction management
□ Returns DTO (not entity)
□ Can be cached
```

---

## Common Architecture Violations

| Violation | Detection | Severity |
|-----------|-----------|----------|
| Domain imports framework | `import fastapi` in domain/ | Critical |
| Business logic in controller | if/else with business rules in router | Major |
| Anemic domain model | Entity with only fields, no methods | Major |
| Repository returns ORM model | Return type is SQLAlchemy model | Major |
| Direct DB access in use case | `session.execute()` in application/ | Major |
| Missing Port interface | Concrete class used directly | Minor |
| Mixed Command/Query | Single class does both read and write | Minor |
