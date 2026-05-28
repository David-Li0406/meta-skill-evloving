---
name: fastapi-backend-specialist
description: Expert FastAPI backend development for building high-performance REST APIs with Python. Use when building APIs, creating endpoints, implementing CRUD operations, integrating databases (SQL/NoSQL), adding validation, handling async operations, implementing middleware, dependency injection, background tasks, WebSockets, error handling, testing, or any FastAPI backend development task.
---

# FastAPI Backend Specialist

Build modern, high-performance REST APIs with FastAPI.

## Quick Start Workflow

1. **Understand requirements** - API endpoints, data models, database needs
2. **Setup FastAPI** - Install FastAPI and Uvicorn
3. **Define models** - Create Pydantic models for validation
4. **Implement endpoints** - Create path operations (GET, POST, PUT, DELETE)
5. **Add database** - Integrate SQLAlchemy or MongoDB
6. **Add validation** - Use Pydantic for request/response validation
7. **Test API** - Use FastAPI automatic docs at `/docs`

## Installation

```bash
# Basic installation
pip install fastapi uvicorn

# With SQLAlchemy (SQL databases)
pip install fastapi[all] sqlalchemy psycopg2-binary

# With MongoDB
pip install fastapi motor pymongo

# Development dependencies
pip install pytest httpx black flake8
```

## Basic Patterns

### Pattern 1: Simple CRUD API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

items_db = {}

@app.post("/items")
async def create_item(item: Item):
    item_id = len(items_db) + 1
    items_db[item_id] = item
    return {"id": item_id, **item.dict()}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted"}
```

### Pattern 2: With SQLAlchemy Database

```python
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class ItemModel(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items")
async def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = ItemModel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(ItemModel).offset(skip).limit(limit).all()
    return items
```

### Pattern 3: With Async MongoDB

```python
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.mydatabase

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
async def create_item(item: Item):
    result = await db.items.insert_one(item.dict())
    return {"id": str(result.inserted_id), **item.dict()}

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item["id"] = str(item.pop("_id"))
    return item
```

### Pattern 4: With Dependency Injection

```python
from fastapi import Depends, HTTPException, Header

async def get_token_header(x_token: str = Header(...)):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    return x_token

async def get_current_user(token: str = Depends(get_token_header)):
    # Validate token and get user
    return {"username": "user", "token": token}

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

@app.get("/items")
async def read_items(current_user: dict = Depends(get_current_user)):
    return {"items": [], "user": current_user}
```

## Project Structure

```
app/
├── main.py              # FastAPI app initialization
├── models/              # Pydantic models
│   ├── __init__.py
│   ├── item.py
│   └── user.py
├── schemas/             # Database models (SQLAlchemy/Motor)
│   ├── __init__.py
│   └── models.py
├── routers/             # API routes
│   ├── __init__.py
│   ├── items.py
│   └── users.py
├── dependencies.py      # Shared dependencies
├── database.py          # Database connection
└── config.py            # Configuration
```

## Common Use Cases

### Building a CRUD API
1. Define Pydantic models for validation
2. Create database models (SQLAlchemy/Motor)
3. Implement CRUD endpoints (POST, GET, PUT/PATCH, DELETE)
4. Add query parameters for filtering/pagination
5. Use dependency injection for database sessions

See [api-patterns.md](references/api-patterns.md) for complete CRUD examples.

### Database Integration

**SQL (PostgreSQL/MySQL):**
- Use SQLAlchemy ORM
- Define models inheriting from Base
- Use dependency injection for sessions
- Implement CRUD operations with ORM

**NoSQL (MongoDB):**
- Use Motor (async) or PyMongo
- Define Pydantic models
- Use async/await for operations
- Handle ObjectId conversion

### Validation with Pydantic

```python
from pydantic import BaseModel, EmailStr, Field, validator

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, le=120)
    password: str = Field(..., min_length=8)

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v
```

### Async Operations

```python
import asyncio

@app.get("/slow")
async def slow_operation():
    await asyncio.sleep(5)  # Simulate slow operation
    return {"message": "Done"}

# Background tasks
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message)

@app.post("/send-notification")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Email sent to {email}")
    return {"message": "Notification sent"}
```

### Error Handling

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong."}
    )
```

### Middleware

```python
from fastapi.middleware.cors import CORSMiddleware
import time

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Running the API

```bash
# Development
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Testing

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_item():
    response = client.post("/items", json={"name": "Test", "price": 10.0})
    assert response.status_code == 200
    assert response.json()["name"] == "Test"

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
```

## Documentation

FastAPI automatically generates:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Environment Variables

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My API"
    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()
```

## Reference Files

- **[api-patterns.md](references/api-patterns.md)** - Complete API patterns, CRUD operations, routing, validation, error handling

## Best Practices

1. **Use async/await** - FastAPI is built for async operations
2. **Dependency injection** - Use Depends() for shared logic
3. **Response models** - Always define response_model for type safety
4. **Status codes** - Use appropriate HTTP status codes
5. **Error handling** - Create custom exception handlers
6. **Validation** - Use Pydantic for request/response validation
7. **API versioning** - Use prefixes like /api/v1
8. **Database sessions** - Always use dependency injection for DB sessions
9. **Background tasks** - Use BackgroundTasks for non-blocking operations
10. **Testing** - Write tests with TestClient

## Common Patterns

### Pagination

```python
@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return items[skip : skip + limit]
```

### Filtering

```python
@app.get("/items")
async def list_items(
    name: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None
):
    filtered = items
    if name:
        filtered = [i for i in filtered if name.lower() in i.name.lower()]
    if min_price:
        filtered = [i for i in filtered if i.price >= min_price]
    if max_price:
        filtered = [i for i in filtered if i.price <= max_price]
    return filtered
```

### Sorting

```python
@app.get("/items")
async def list_items(sort_by: str = "name", order: str = "asc"):
    sorted_items = sorted(items, key=lambda x: getattr(x, sort_by), reverse=(order == "desc"))
    return sorted_items
```

## Security

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate user
    return {"access_token": token, "token_type": "bearer"}
```

## Example Workflow

User request: "Build a REST API for managing todos"

1. **Define models**
   ```python
   class TodoCreate(BaseModel):
       title: str
       description: str | None = None

   class Todo(TodoCreate):
       id: int
       completed: bool = False
   ```

2. **Setup database** (SQLAlchemy)
   ```python
   class TodoModel(Base):
       __tablename__ = "todos"
       id = Column(Integer, primary_key=True)
       title = Column(String)
       description = Column(String, nullable=True)
       completed = Column(Boolean, default=False)
   ```

3. **Implement CRUD endpoints**
   - POST /todos - Create todo
   - GET /todos - List todos
   - GET /todos/{id} - Get single todo
   - PUT /todos/{id} - Update todo
   - DELETE /todos/{id} - Delete todo

4. **Add features**
   - Pagination (skip, limit)
   - Filtering (completed status)
   - Sorting (by date, title)

5. **Test** - Use FastAPI docs at `/docs`

Result: Fully functional REST API for todo management.
