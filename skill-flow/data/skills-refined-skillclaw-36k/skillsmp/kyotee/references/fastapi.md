# Kyotee: Python + FastAPI Patterns

Use these patterns when building modern async Python APIs with FastAPI and Pydantic.

## Project Structure

```
app/
  __init__.py
  main.py               # FastAPI app entry point
  config.py             # Configuration
  dependencies.py       # Dependency injection
  routers/
    __init__.py
    users.py            # User routes
    auth.py             # Auth routes
  models/
    __init__.py
    user.py             # SQLAlchemy models
  schemas/
    __init__.py
    user.py             # Pydantic schemas
  services/
    __init__.py
    user.py             # Business logic
  repositories/
    __init__.py
    user.py             # Data access
  middleware/
    __init__.py
    logging.py
tests/
  __init__.py
  test_users.py
requirements.txt
pyproject.toml
```

## Naming Conventions

- **Files**: snake_case (`user_service.py`)
- **Classes**: PascalCase (`UserService`, `UserSchema`)
- **Functions**: snake_case (`get_user`, `create_user`)
- **Variables**: snake_case (`user_id`, `created_at`)
- **Constants**: UPPER_SNAKE_CASE (`DATABASE_URL`)

## Main Entry Point

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, auth
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="API Description",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

## Configuration

```python
# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "My API"
    DATABASE_URL: str = "sqlite:///./app.db"
    SECRET_KEY: str = "your-secret-key"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
```

## Pydantic Schemas

```python
# app/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserList(BaseModel):
    users: list[UserResponse]
    total: int
```

## SQLAlchemy Models

```python
# app/models/user.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

## Router

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserList
from app.services.user import UserService

router = APIRouter()


@router.get("", response_model=UserList)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    service = UserService(db)
    users = await service.get_all(skip=skip, limit=limit)
    total = await service.count()
    return UserList(users=users, total=total)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    service = UserService(db)
    existing = await service.get_by_email(user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return await service.create(user_data)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    service = UserService(db)
    user = await service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
):
    service = UserService(db)
    user = await service.update(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    service = UserService(db)
    deleted = await service.delete(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
```

## Service Layer

```python
# app/services/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user import UserRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.repo.find_all(skip=skip, limit=limit)

    async def get(self, user_id: int) -> User | None:
        return await self.repo.find_by_id(user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self.repo.find_by_email(email)

    async def create(self, data: UserCreate) -> User:
        hashed_password = pwd_context.hash(data.password)
        return await self.repo.create(
            email=data.email,
            name=data.name,
            hashed_password=hashed_password,
        )

    async def update(self, user_id: int, data: UserUpdate) -> User | None:
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(user_id, update_data)

    async def delete(self, user_id: int) -> bool:
        return await self.repo.delete(user_id)

    async def count(self) -> int:
        return await self.repo.count()
```

## Repository Layer

```python
# app/repositories/user.py
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def find_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def find_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    async def find_by_email(self, email: str) -> User | None:
        result = self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    async def update(self, user_id: int, data: dict) -> User | None:
        user = await self.find_by_id(user_id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.find_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    async def count(self) -> int:
        result = self.db.execute(select(func.count(User.id)))
        return result.scalar()
```

## Dependencies

```python
# app/dependencies.py
from typing import Generator
from sqlalchemy.orm import Session
from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Database Setup

```python
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite only
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
```

## requirements.txt

```
fastapi>=0.100.0
uvicorn[standard]>=0.22.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-multipart>=0.0.6
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0
```

## Tips

- **Async by default** - Use `async def` for route handlers
- **Pydantic for validation** - Automatic request/response validation
- **Dependency injection** - Use `Depends()` for shared logic
- **Type hints** - FastAPI uses them for docs and validation
- **OpenAPI** - Auto-generated at `/docs` (Swagger) and `/redoc`
- **Background tasks** - Use `BackgroundTasks` for async operations
