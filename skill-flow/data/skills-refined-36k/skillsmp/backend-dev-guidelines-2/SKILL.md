---
name: backend-dev-guidelines
description: Comprehensive backend development guide for Python/FastAPI/SQLAlchemy applications. Use when creating routes, services, models, schemas, database operations, or working with FastAPI endpoints, SQLAlchemy/Alembic migrations, Pydantic validation, error handling, dependency injection, or async patterns. Covers layered architecture (routes → services → repositories → models), separation of concerns, error handling, performance, testing strategies, and best practices.
---

# Backend Development Guidelines (FastAPI/Python)

## Purpose

Establish consistency and best practices for Python/FastAPI backend development using modern FastAPI/SQLAlchemy/Pydantic patterns.

## When to Use This Skill

Automatically activates when working on:
- Creating or modifying routes, endpoints, APIs
- Building services, repositories
- Database models and schemas (SQLAlchemy/Pydantic)
- Alembic migrations
- Input validation with Pydantic
- Error handling and exception management
- Dependency injection
- Backend testing and refactoring

---

## Quick Start

### New Backend Feature Checklist

- [ ] **Route**: Clean FastAPI route definition, delegate to service
- [ ] **Service**: Business logic with dependency injection
- [ ] **Repository**: Database access layer (if complex queries)
- [ ] **Model**: SQLAlchemy model (database table)
- [ ] **Schema**: Pydantic schema (validation + serialization)
- [ ] **Migration**: Alembic migration for schema changes
- [ ] **Validation**: Pydantic validators
- [ ] **Error Handling**: Proper HTTPException with status codes
- [ ] **Tests**: Unit + integration tests
- [ ] **Documentation**: FastAPI auto-docs (/docs)

---

## Architecture Overview

### Layered Architecture

```
HTTP Request
    ↓
Routes (FastAPI endpoints - routing only)
    ↓
Services (business logic)
    ↓
Repositories (complex database operations)
    ↓
Models (SQLAlchemy ORM)
    ↓
Database (PostgreSQL via Supabase)
```

**Key Principle:** Each layer has ONE responsibility.

**Current Project Structure:**
```
backend/app/
├── routes/              # API routes (ML_Routes.py, Reddit_Routes.py)
├── services/            # Business logic (TO BE CREATED)
├── repositories/        # Data access (TO BE CREATED as needed)
├── models.py            # SQLAlchemy models (City, Project, Article, ArticleChunk)
├── schemas.py           # Pydantic schemas (validation + serialization)
├── db.py                # Database connection and session management
├── main.py              # FastAPI app setup and CRUD endpoints
└── machine_learning/    # ML-specific logic
```

---

## Core Principles (7 Key Rules)

### 1. Routes Only Route, Services Handle Logic

```python
# ❌ NEVER: Business logic directly in routes
@app.post("/complex-operation")
async def complex_operation(data: dict, db: Session = Depends(get_db)):
    # 50 lines of business logic
    # Database queries
    # Validation
    # Error handling
    return result

# ✅ ALWAYS: Delegate to service
@app.post("/complex-operation")
async def complex_operation(
    data: ComplexOperationRequest,
    db: Session = Depends(get_db)
):
    result = await operation_service.execute(data, db)
    return result
```

**Why:** Testability, reusability, maintainability

### 2. Use Pydantic for ALL Input/Output

```python
# ❌ NEVER: Untyped dict parameters
@app.post("/create-user")
def create_user(user_data: dict):
    name = user_data.get("name")  # No validation!

# ✅ ALWAYS: Pydantic schema
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(ge=0, le=120)

@app.post("/create-user", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Already validated!
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    return db_user
```

### 3. Separate Models (DB) from Schemas (API)

```python
# models.py - SQLAlchemy (database)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # NEVER expose!
    created_at = Column(DateTime, default=datetime.utcnow)

# schemas.py - Pydantic (API)
class UserCreate(BaseModel):
    email: EmailStr
    password: str  # Plain password for input

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    # NO hashed_password - never expose to API!

    model_config = ConfigDict(from_attributes=True)
```

**Why:** Security, flexibility, separation of concerns

### 4. Use Dependency Injection

```python
# ❌ NEVER: Global db connection
db = SessionLocal()  # Dangerous!

@app.get("/users")
def get_users():
    users = db.query(User).all()  # What if db closed?
    return users

# ✅ ALWAYS: Dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

**Current Project Pattern:** Already using this correctly in `main.py`! Keep it up.

### 5. Proper Error Handling with HTTPException

```python
# ❌ NEVER: Generic exceptions or silent failures
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user  # Returns None if not found - confusing!

# ✅ ALWAYS: Explicit HTTP exceptions
from fastapi import HTTPException, status

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return user
```

**Available Status Codes:**
- `201`: Created
- `204`: No Content (delete successful)
- `400`: Bad Request (validation error)
- `404`: Not Found
- `409`: Conflict (duplicate)
- `422`: Unprocessable Entity (Pydantic validation)
- `500`: Internal Server Error

### 6. Transaction Management

```python
# ❌ RISKY: Manual commit without error handling
def create_order(order_data: OrderCreate, db: Session):
    order = Order(**order_data.model_dump())
    db.add(order)
    db.commit()  # What if this fails?

    item = OrderItem(order_id=order.id, ...)
    db.add(item)
    db.commit()  # Item created even if next step fails!

# ✅ SAFE: Transaction with rollback
def create_order(order_data: OrderCreate, db: Session):
    try:
        # Create order
        order = Order(**order_data.model_dump())
        db.add(order)
        db.flush()  # Get order.id without committing

        # Create items
        for item_data in order_data.items:
            item = OrderItem(order_id=order.id, **item_data.model_dump())
            db.add(item)

        # Commit everything together
        db.commit()
        db.refresh(order)
        return order

    except Exception as e:
        db.rollback()  # Rollback everything
        raise HTTPException(status_code=500, detail=str(e))
```

**Current Project Pattern:** Your `ingest_json_payload` uses this pattern correctly with try/except and commit at the end!

### 7. Use Type Hints Everywhere

```python
# ❌ NEVER: No types
def process_data(data):
    result = transform(data)
    return result

# ✅ ALWAYS: Full typing
from typing import List, Optional, Dict, Any

def process_data(
    data: List[Dict[str, Any]],
    db: Session
) -> Optional[ProcessedResult]:
    result: ProcessedResult = transform(data)
    return result
```

---

## Directory Structure (Recommended Evolution)

### Current Structure
```
backend/app/
├── main.py              # Has routes, CRUD, ingest logic
├── models.py
├── schemas.py
├── db.py
└── routes/
    ├── ML_Routes.py
    └── Reddit_Routes.py
```

### Recommended Structure (As Project Grows)
```
backend/app/
├── main.py              # FastAPI app setup only
├── db.py
├── models.py            # Or split into models/
├── schemas.py           # Or split into schemas/
├── routes/
│   ├── __init__.py
│   ├── cities.py
│   ├── projects.py
│   ├── articles.py
│   ├── ml.py
│   └── reddit.py
├── services/            # Business logic
│   ├── __init__.py
│   ├── city_service.py
│   ├── project_service.py
│   ├── article_service.py
│   ├── ingest_service.py
│   └── ml_service.py
├── repositories/        # Complex queries
│   ├── __init__.py
│   └── article_repository.py  # Only if needed
├── utils/
│   └── helpers.py
└── tests/
    ├── test_routes.py
    ├── test_services.py
    └── conftest.py
```

**When to create a service:**
- Logic is >20 lines
- Logic is reused in multiple endpoints
- Logic involves multiple models/tables
- Business rules need testing independently

**When to create a repository:**
- Complex queries with joins
- Query reuse across services
- Query optimization needed
- Raw SQL required

---

## Detailed Guides

### [Architecture & Patterns](resources/architecture-patterns.md)
- Layered architecture deep dive
- When to extract services
- When to create repositories
- Dependency injection patterns

### [Models & Schemas](resources/models-and-schemas.md)
- SQLAlchemy model patterns
- Pydantic schema patterns
- Relationships (ForeignKey, Many-to-Many)
- Model validators and computed fields

### [Database Patterns](resources/database-patterns.md)
- Session management
- Transaction patterns
- Query optimization
- Alembic migrations

### [Routing & Endpoints](resources/routing-and-endpoints.md)
- FastAPI route patterns
- Path parameters, query parameters, body
- Response models
- Status codes

### [Error Handling](resources/error-handling.md)
- HTTPException patterns
- Custom exception handlers
- Validation errors
- Logging and monitoring

### [Testing Guide](resources/testing-guide.md)
- pytest setup
- Testing with database
- Fixtures and factories
- Integration tests

### [Performance & Optimization](resources/performance.md)
- Async vs sync
- Database query optimization
- Caching patterns
- Connection pooling

---

## Package Management

**This project uses `uv` for Python package management.**

```bash
# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>

# Install dependencies
uv sync

# Run Python with uv
uv run python script.py

# Run uvicorn with uv
uv run uvicorn app.main:app --reload
```

**❌ NEVER use `pip install`** - Always use `uv add` instead.

---

## Migration Strategy (From Current to Recommended)

**Phase 1: Extract Services (Do this when routes get >30 lines)**
1. Create `services/` directory
2. Move business logic from `main.py` routes to services
3. Keep routes thin

**Phase 2: Split Routes (Do this when main.py gets >500 lines)**
1. Create separate route files by resource
2. Use `APIRouter` for each resource
3. Include routers in `main.py`

**Phase 3: Add Repositories (Only if needed)**
1. If you have complex joins/queries
2. Create `repositories/` directory
3. Move query logic from services to repositories

**Don't over-engineer early!** Start simple, refactor when needed.

---

## Common Patterns

### Pattern: Get or Create

```python
# Common pattern for ensuring entities exist
def get_or_create_city(city_name: str, db: Session) -> models.City:
    city = db.query(models.City).filter(
        models.City.city_name == city_name
    ).first()

    if not city:
        city = models.City(city_name=city_name)
        db.add(city)
        db.flush()  # Get city.id without full commit

    return city
```

### Pattern: Bulk Operations

```python
# Efficient bulk insert
def bulk_create_articles(
    articles: List[ArticleCreate],
    db: Session
) -> List[models.Article]:
    db_articles = [
        models.Article(**article.model_dump())
        for article in articles
    ]
    db.bulk_save_objects(db_articles)
    db.commit()
    return db_articles
```

### Pattern: Pagination

```python
from fastapi import Query

@app.get("/articles")
def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    total = db.query(models.Article).count()
    articles = db.query(models.Article).offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "results": articles
    }
```

### Pattern: Search with Filters

```python
@app.get("/search")
def search_articles(
    query: Optional[str] = None,
    city: Optional[str] = None,
    project: Optional[str] = None,
    db: Session = Depends(get_db)
):
    articles_query = db.query(models.Article)

    if query:
        articles_query = articles_query.filter(
            or_(
                models.Article.title.ilike(f"%{query}%"),
                models.Article.full_text.ilike(f"%{query}%")
            )
        )

    if city:
        articles_query = articles_query.join(models.Article.projects).join(
            models.Project.city
        ).filter(models.City.city_name.ilike(f"%{city}%"))

    return articles_query.all()
```

---

## Quick Reference

### FastAPI Decorators
```python
@app.get("/path")           # GET request
@app.post("/path")          # POST request
@app.put("/path/{id}")      # PUT request (full update)
@app.patch("/path/{id}")    # PATCH request (partial update)
@app.delete("/path/{id}")   # DELETE request
```

### Common Imports
```python
from fastapi import FastAPI, HTTPException, Depends, status, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field, validator
```

### Pydantic Config
```python
class UserResponse(BaseModel):
    id: int
    name: str

    # For SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)
```

---

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

---

**Remember:** Start simple, refactor when complexity demands it. Your current structure in `main.py` is fine for early development. Extract to services/repositories as routes grow beyond 30-50 lines.
