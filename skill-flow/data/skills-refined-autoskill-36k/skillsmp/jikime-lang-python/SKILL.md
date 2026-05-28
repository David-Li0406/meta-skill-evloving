---
name: jikime-lang-python
description: Python 3.13+ development specialist covering FastAPI, Django, async patterns, and data science. Use when developing Python APIs, web applications, data pipelines, or writing tests.
version: 1.0.0
tags: ["language", "python", "fastapi", "django", "pytest", "async", "data-science"]
triggers:
  keywords: ["python", "fastapi", "django", "pytest", "pydantic", "sqlalchemy", "파이썬"]
  phases: ["run"]
  agents: ["backend", "test-guide"]
  languages: ["python"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2000
user-invocable: false
---

# Python Development Guide

Python 3.13+ 개발을 위한 간결한 가이드.

## Quick Reference

| 용도 | 도구 | 특징 |
|------|------|------|
| Web Framework | **FastAPI** | 빠름, 타입 힌트, OpenAPI |
| Web Framework | **Django** | 풀스택, 관리자, ORM |
| Validation | **Pydantic** | 데이터 검증 |
| Testing | **pytest** | 유연한 테스팅 |

## Project Setup

```bash
# uv (권장)
uv init project && cd project
uv add fastapi uvicorn pydantic sqlalchemy

# poetry
poetry new project && cd project
poetry add fastapi uvicorn pydantic

# pip
python -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn pydantic
```

## FastAPI Patterns

### Basic API

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}

@app.post("/users", response_model=UserResponse)
async def create_user(data: UserCreate):
    user = await UserService.create(data)
    return user

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await UserService.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Dependency Injection

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    return await UserRepository(db).list_all()
```

### Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    user = await verify_token(token.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user
```

## Pydantic v2 Patterns

```python
from pydantic import BaseModel, Field, field_validator

class User(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=50)
    email: str
    age: int | None = None

    model_config = {"from_attributes": True, "str_strip_whitespace": True}

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email")
        return v.lower()

# Usage
user = User.model_validate(orm_object)
user_dict = user.model_dump()
user_json = user.model_dump_json()
```

## SQLAlchemy 2.0 Async

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)

# Repository
class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def create(self, data: UserCreate) -> User:
        user = User(**data.model_dump())
        self.session.add(user)
        await self.session.commit()
        return user
```

## pytest Patterns

```python
import pytest
from httpx import AsyncClient

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/users", json={
        "name": "John",
        "email": "john@example.com"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "John"

# Parametrize
@pytest.mark.parametrize("email,expected", [
    ("valid@email.com", True),
    ("invalid", False),
    ("", False),
])
def test_validate_email(email, expected):
    result = validate_email(email)
    assert result == expected
```

## Project Structure

```
project/
├── src/
│   └── project/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   └── routes/
│       ├── core/
│       │   └── config.py
│       ├── models/
│       ├── schemas/
│       └── services/
├── tests/
├── pyproject.toml
└── README.md
```

## Best Practices

- **Type Hints**: 모든 함수에 타입 힌트 사용
- **Async**: I/O 작업에 async/await 사용
- **Pydantic**: 입출력 검증에 Pydantic 모델 사용
- **Dependency Injection**: FastAPI Depends로 의존성 주입
- **환경변수**: pydantic-settings로 설정 관리

---

Last Updated: 2026-01-21
Version: 2.0.0
