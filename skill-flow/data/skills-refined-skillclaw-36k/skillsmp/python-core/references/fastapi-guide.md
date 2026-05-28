# FastAPI Comprehensive Guide

Modern Python web framework for building APIs with automatic OpenAPI docs and type safety.

## Why FastAPI?

- **Fast**: Very high performance, on par with NodeJS and Go
- **Fast to code**: Type hints enable autocomplete and validation
- **Fewer bugs**: ~40% reduction in human errors
- **Intuitive**: Great editor support, less debugging
- **Standards-based**: OpenAPI and JSON Schema

## Quick Start

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

Run with: `uvicorn main:app --reload`

## Request Body with Pydantic

```python
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)
    is_active: bool = True

@app.post("/users/")
async def create_user(user: User):
    return user
```

## Path Parameters

```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model_name": model_name, "message": "Deep Learning model"}
```

## Query Parameters

```python
@app.get("/items/")
async def read_items(
    skip: int = 0,
    limit: int = 10,
    q: str | None = None
):
    return {"skip": skip, "limit": limit, "q": q}
```

## Dependency Injection

```python
from fastapi import Depends
from typing import Annotated

async def get_db():
    db = Database()
    try:
        yield db
    finally:
        await db.close()

@app.get("/users/")
async def read_users(db: Annotated[Database, Depends(get_db)]):
    return await db.fetch_users()

# Common dependency pattern
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
```

## Database Integration (SQLAlchemy)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Model
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Endpoint
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

## Async Database (SQLAlchemy 2.0)

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg://user:password@localhost/dbname")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_db():
    async with async_session() as session:
        yield session

@app.get("/users/")
async def read_users(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(UserModel))
    return result.scalars().all()
```

## Authentication

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## File Uploads

```python
from fastapi import File, UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

@app.post("/files/")
async def create_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email logic
    pass

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification sent"}
```

## WebSocket

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message: {data}")
```

## Middleware

```python
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Error Handling

```python
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong."},
    )

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Custom header"},
        )
    return items[item_id]
```

## Testing

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user():
    response = client.post(
        "/users/",
        json={"username": "test", "email": "test@example.com", "age": 25}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "test"
```

## Project Structure

```
my-fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── dependencies.py
│   └── database.py
├── tests/
│   └── test_main.py
├── requirements.txt
└── pyproject.toml
```

## Best Practices

1. **Use type hints**: Enable validation and docs
2. **Pydantic models**: For request/response validation
3. **Dependency injection**: For DB sessions, auth
4. **Async where appropriate**: For I/O operations
5. **Response models**: Specify return types
6. **Error handling**: Use HTTPException
7. **Testing**: Use TestClient
8. **Docs**: Add descriptions to endpoints
9. **Security**: Implement proper authentication
10. **Structure**: Organize with routers

## Performance Tips

- Use async for I/O-bound operations
- Connection pooling for databases
- Caching with Redis
- Background tasks for long operations
- Gzip compression middleware
- Database query optimization
