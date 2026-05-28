# FastAPI API Patterns

REST API patterns, routing, and request/response handling in FastAPI.

## Table of Contents
- Basic Routing
- CRUD Operations
- Path and Query Parameters
- Request Body Validation
- Response Models
- Status Codes
- Error Handling

## Basic Routing

### Simple GET Endpoint

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items")
async def get_items():
    return {"items": ["item1", "item2", "item3"]}
```

### Path Parameters

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/{username}")
async def get_user(username: str):
    return {"username": username}

# Multiple path parameters
@app.get("/users/{user_id}/posts/{post_id}")
async def get_user_post(user_id: int, post_id: int):
    return {"user_id": user_id, "post_id": post_id}
```

### Query Parameters

```python
@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# Optional query parameters
@app.get("/search")
async def search(q: str | None = None, page: int = 1):
    return {"query": q, "page": page}

# Multiple query parameters with validation
from fastapi import Query

@app.get("/items")
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    sort_by: str = Query("created_at")
):
    return {"skip": skip, "limit": limit, "sort_by": sort_by}
```

## CRUD Operations

### Complete CRUD Pattern

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic models
class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float | None = None

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

# In-memory storage (replace with database)
items_db: dict[int, Item] = {}
current_id = 1

# CREATE
@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    global current_id
    new_item = Item(id=current_id, **item.dict())
    items_db[current_id] = new_item
    current_id += 1
    return new_item

# READ (List)
@app.get("/items", response_model=List[Item])
async def list_items(skip: int = 0, limit: int = 10):
    items = list(items_db.values())
    return items[skip : skip + limit]

# READ (Single)
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

# UPDATE
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = items_db[item_id]
    update_data = item.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(stored_item, field, value)

    return stored_item

# PATCH (Partial update)
@app.patch("/items/{item_id}", response_model=Item)
async def partial_update_item(item_id: int, item: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = items_db[item_id]
    update_data = item.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(stored_item, field, value)

    return stored_item

# DELETE
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    return None
```

## Request Body Validation

### Basic Request Body

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    full_name: str | None = None

@app.post("/users")
async def create_user(user: User):
    return user
```

### Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str

class UserWithAddress(BaseModel):
    username: str
    email: str
    address: Address

@app.post("/users")
async def create_user(user: UserWithAddress):
    return user
```

### Multiple Body Parameters

```python
from fastapi import Body

@app.post("/items")
async def create_item(
    item: Item,
    user: User,
    importance: int = Body(...)
):
    return {"item": item, "user": user, "importance": importance}
```

## Response Models

### Response Model with Validation

```python
class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: str
    full_name: str | None = None

@app.post("/users", response_model=UserOut)
async def create_user(user: UserIn):
    # Password is not returned in response
    return user
```

### Response with Different Status Codes

```python
from fastapi.responses import JSONResponse

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items_db:
        return JSONResponse(
            status_code=404,
            content={"detail": "Item not found"}
        )
    return items_db[item_id]
```

### Multiple Response Models

```python
from typing import Union

class BaseUser(BaseModel):
    username: str
    email: str

class AdminUser(BaseUser):
    admin: bool = True
    permissions: List[str]

@app.get("/users/{user_id}", response_model=Union[BaseUser, AdminUser])
async def get_user(user_id: int):
    # Return different models based on condition
    if user_id == 1:
        return AdminUser(
            username="admin",
            email="admin@example.com",
            permissions=["read", "write", "delete"]
        )
    return BaseUser(username="user", email="user@example.com")
```

## Status Codes

```python
from fastapi import status

@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    # Delete logic
    return None

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return items_db[item_id]
```

## Error Handling

### Basic Error Handling

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "ItemNotFound"}
        )
    return items_db[item_id]
```

### Custom Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

@app.exception_handler(ItemNotFoundException)
async def item_not_found_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Item {exc.item_id} not found",
            "item_id": exc.item_id
        }
    )

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items_db:
        raise ItemNotFoundException(item_id=item_id)
    return items_db[item_id]
```

### Validation Error Handling

```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "message": "Validation error"
        }
    )
```

## Router Organization

### APIRouter for Modular Structure

```python
from fastapi import APIRouter

# items.py
router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def list_items():
    return {"items": []}

@router.get("/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

@router.post("/")
async def create_item(item: Item):
    return item

# main.py
from fastapi import FastAPI
from .routers import items

app = FastAPI()
app.include_router(items.router)
```

### Multiple Routers

```python
# main.py
from fastapi import FastAPI
from .routers import items, users, auth

app = FastAPI(title="My API", version="1.0.0")

app.include_router(auth.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
```

## Request and Response Examples

### Adding Examples to Schemas

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2
            }
        }

@app.post("/items")
async def create_item(item: Item):
    return item
```

## File Uploads

```python
from fastapi import File, UploadFile

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }

@app.post("/uploadfiles")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    return {
        "filenames": [file.filename for file in files]
    }
```

## Form Data

```python
from fastapi import Form

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
```

## Headers and Cookies

```python
from fastapi import Header, Cookie

@app.get("/items")
async def read_items(
    user_agent: str | None = Header(None),
    session_id: str | None = Cookie(None)
):
    return {
        "User-Agent": user_agent,
        "session_id": session_id
    }
```

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
