# Authentication & Authorization Patterns

Conditional Keycloak or application-based RBAC.

## AI Prompt: Authentication Strategy Selection

**IMPORTANT**: When creating a new FastAPI project, AI must ask:

> "Do you want **Keycloak-based authentication** with role/user management from Keycloak, or **application-based RBAC** with roles stored in the database?"

## Option 1: Keycloak Authentication

### Install

```bash
pip install python-keycloak python-jose[cryptography]
```

### Configuration

```python
# core/config.py
class Settings(BaseSettings):
    KEYCLOAK_URL: str = "https://keycloak.example.com"
    KEYCLOAK_REALM: str = "my-realm"
    KEYCLOAK_CLIENT_ID: str = "fastapi-app"
    KEYCLOAK_CLIENT_SECRET: str = ""
```

### Setup (core/auth_keycloak.py)

```python
from keycloak import KeycloakOpenID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from core.config import settings

security = HTTPBearer()

keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    try:
        # Verify token with Keycloak
        user_info = keycloak_openid.decode_token(
            token,
            key=keycloak_openid.public_key(),
            options={"verify_signature": True, "verify_aud": False}
        )
        return user_info
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

def require_role(required_role: str):
    """Dependency to check Keycloak role."""
    async def check_role(user = Depends(get_current_user)):
        user_roles = user.get("realm_access", {}).get("roles", [])
        if required_role not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required"
            )
        return user
    return check_role
```

### Usage

```python
from core.auth_keycloak import get_current_user, require_role

@router.get("/profile")
async def get_profile(user = Depends(get_current_user)):
    return {"email": user["email"], "name": user["name"]}

@router.post("/admin/action")
async def admin_action(user = Depends(require_role("admin"))):
    # Only users with "admin" role can access
    return {"message": "Admin action performed"}
```

## Option 2: Application-Based RBAC

### Models

```python
# models/user.py
from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.db import Base

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('role_id', ForeignKey('roles.id'))
)

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    
    roles: Mapped[list["Role"]] = relationship(
        secondary=user_roles,
        back_populates="users"
    )

class Role(Base):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    
    users: Mapped[list["User"]] = relationship(
        secondary=user_roles,
        back_populates="roles"
    )
```

### Auth Setup (core/auth_app.py)

```python
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.config import settings
from core.db import get_db
from models.user import User

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def require_role(required_role: str):
    """Check if user has required role."""
    async def check_role(user: User = Depends(get_current_user)):
        user_role_names = [role.name for role in user.roles]
        if required_role not in user_role_names:
            raise HTTPException(
                status_code=403,
                detail=f"Role '{required_role}' required"
            )
        return user
    return check_role
```

### Usage

```python
from core.auth_app import get_current_user, require_role

@router.get("/profile")
async def get_profile(user: User = Depends(get_current_user)):
    return {"email": user.email, "roles": [r.name for r in user.roles]}

@router.post("/admin/action")
async def admin_action(user: User = Depends(require_role("admin"))):
    return {"message": "Admin action"}
```

## Central Role Management

**No per-endpoint duplication**:

✅ **Good**:
```python
# Central dependency
admin_required = Depends(require_role("admin"))

@router.post("/action1")
async def action1(user = admin_required): ...

@router.post("/action2")
async def action2(user = admin_required): ...
```

❌ **Bad**:
```python
@router.post("/action1")
async def action1(user = Depends(require_role("admin"))): ...

@router.post("/action2")
async def action2(user = Depends(require_role("admin"))): ...
```

## Router-Level Authorization

```python
# Protect entire router
router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(require_role("admin"))]
)

@router.get("/users")  # Auto-requires admin role
async def list_users(): ...
```

## Next Steps

- [Routing Patterns](routing-patterns.md) - Apply auth to routes
- [Clean Code Standards](clean-code-standards.md) - Organize auth code
- [Database Patterns](database-patterns.md) - User/role models
