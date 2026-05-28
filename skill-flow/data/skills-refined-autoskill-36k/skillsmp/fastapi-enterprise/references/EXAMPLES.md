# FastAPI Enterprise Examples

Complete examples for common tasks.

## Example 1: Create New API Module (User Management)

### 1. Create Model

```bash
python scripts/create_model.py --name User --table users --module auth
```

Edit `models/auth/user.py`:
```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
```

### 2. Create Migration

```bash
alembic revision --autogenerate -m "Add users table"
alembic upgrade head
```

### 3. Create Schemas

```bash
python scripts/create_schema.py --name User --module auth
```

Edit `schemas/auth/user.py`:
```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    
    model_config = {"from_attributes": True}
```

### 4. Create Service

```bash
python scripts/create_service.py --name User --module auth
```

Edit `services/auth/user.py`:
```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.auth.user import User
from schemas.auth.user import UserCreate

class UserService:
    async def create(self, db: AsyncSession, data: UserCreate) -> User:
        user = User(**data.model_dump())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    async def get_all(self, db: AsyncSession) -> list[User]:
        result = await db.execute(select(User))
        return result.scalars().all()

user_service = UserService()
```

### 5. Create Endpoint

```bash
python scripts/create_endpoint.py --module user --service profile --method post --path create --with-schema --with-service
```

Edit `api/routes/v1/user/profile.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from schemas.auth.user import UserCreate, UserResponse
from services.auth.user import user_service

router = APIRouter()

@router.post("/create", response_model=UserResponse, status_code=201)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user = await user_service.create(db, data)
    return user

@router.get("/list", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    users = await user_service.get_all(db)
    return users
```

Result: `POST /api/v1/user/profile/create` and `GET /api/v1/user/profile/list`

## Example 2: Add Keycloak Authentication

### 1. Install Dependencies

```bash
pip install python-keycloak python-jose[cryptography]
```

### 2. Add Configuration

```bash
# .env
KEYCLOAK_URL=https://keycloak.example.com
KEYCLOAK_REALM=my-realm
KEYCLOAK_CLIENT_ID=fastapi-app
KEYCLOAK_CLIENT_SECRET=secret
```

### 3. Create Auth Module

Create `core/auth.py`:
```python
from keycloak import KeycloakOpenID
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from core.config import settings

security = HTTPBearer()

keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
)

async def get_current_user(credentials = Depends(security)):
    token = credentials.credentials
    try:
        user_info = keycloak_openid.decode_token(
            token,
            key=keycloak_openid.public_key(),
            options={"verify_signature": True, "verify_aud": False}
        )
        return user_info
    except:
        raise HTTPException(401, "Invalid authentication")

def require_role(role: str):
    async def check_role(user = Depends(get_current_user)):
        if role not in user.get("realm_access", {}).get("roles", []):
            raise HTTPException(403, f"Role '{role}' required")
        return user
    return check_role
```

### 4. Protect Endpoints

```python
from core.auth import get_current_user, require_role

@router.post("/create")
async def create_user(
    data: UserCreate,
    current_user = Depends(get_current_user),  # ← Requires auth
    db: AsyncSession = Depends(get_db),
):
    ...

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user = Depends(require_role("admin")),  # ← Requires admin role
    db: AsyncSession = Depends(get_db),
):
    ...
```

## Example 3: External API Integration

### 1. Add Config

```yaml
# config/development.yml
payment_api:
  base_url: "https://api-sandbox.payment.com"
  api_key: "dev_key_123"
  timeout: 30
```

### 2. Create Pydantic Config Model

```python
# core/config.py
class PaymentAPIConfig(BaseModel):
    base_url: str
    api_key: str
    timeout: int = 30
```

### 3. Create Client

```python
# services/payment/client.py
from core.httpx import HTTPClient
from core.config import load_yaml_config, PaymentAPIConfig

# Load config
config_dict = load_yaml_config("payment_api")
config = PaymentAPIConfig(**config_dict)

# Create client
payment_client = HTTPClient(
    base_url=config.base_url,
    timeout=config.timeout,
    headers={"Authorization": f"Bearer {config.api_key}"}
)
```

### 4. Use in Service

```python
# services/payment/transaction.py
from services.payment.client import payment_client

class TransactionService:
    async def create_payment(self, amount: float, currency: str):
        response = await payment_client.post(
            "/transactions",
            json={"amount": amount, "currency": currency}
        )
        return response.json()

transaction_service = TransactionService()
```

### 5. Use in Endpoint

```python
@router.post("/payment/create")
async def create_payment(
    amount: float,
    currency: str,
    db: AsyncSession = Depends(get_db),
):
    result = await transaction_service.create_payment(amount, currency)
    return result
```

## Example 4: Add Custom Prometheus Metric

### 1. Define Metric

```python
# core/metrics.py
from prometheus_client import Counter

orders_created_total = Counter(
    "orders_created_total",
    "Total orders created",
    ["product_category"]
)
```

### 2. Use in Service

```python
# services/order/order.py
from core.metrics import orders_created_total

class OrderService:
    async def create_order(self, db: AsyncSession, data: OrderCreate):
        order = Order(**data.model_dump())
        db.add(order)
        await db.commit()
        
        # Track metric
        orders_created_total.labels(
            product_category=order.product_category
        ).inc()
        
        return order
```

### 3. View Metrics

Visit `http://localhost:8000/metrics`

## Example 5: Database Transaction

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def transfer_points(
    db: AsyncSession,
    from_user_id: int,
    to_user_id: int,
    points: int,
):
    """Transfer points between users with transaction."""
    try:
        # Get users
        from_user = await user_service.get_by_id(db, from_user_id)
        to_user = await user_service.get_by_id(db, to_user_id)
        
        # Validate
        if from_user.points < points:
            raise ValueError("Insufficient points")
        
        # Transfer
        from_user.points -= points
        to_user.points += points
        
        # Commit transaction
        await db.commit()
        
        logger.info(
            "Points transferred",
            from_user=from_user_id,
            to_user=to_user_id,
            points=points,
        )
        
    except Exception as e:
        # Rollback on error
        await db.rollback()
        logger.error("Transfer failed", error=str(e))
        raise
```

## Example 6: Pagination Helper

```python
# helpers/pagination.py
from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int

async def paginate(
    db: AsyncSession,
    query,
    page: int = 1,
    page_size: int = 10,
):
    """Paginate SQLAlchemy query."""
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.execute(count_query)
    total = total.scalar()
    
    # Get page
    offset = (page - 1) * page_size
    items_query = query.offset(offset).limit(page_size)
    result = await db.execute(items_query)
    items = result.scalars().all()
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )
```

Usage:
```python
@router.get("/users", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db),
):
    query = select(User).where(User.is_active == True)
    return await paginate(db, query, page, page_size)
```

## Next Steps

- Explore [SKILL.md](../SKILL.md) for comprehensive patterns
- Check [scripts/](../scripts/) for automation tools
- Review [references/](../references/) for detailed guides
