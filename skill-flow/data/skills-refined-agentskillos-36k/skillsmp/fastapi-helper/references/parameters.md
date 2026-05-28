# FastAPI Parameters Reference

## Path Parameters

```python
from fastapi import Path

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(
        ...,                    # Required (... = Ellipsis)
        title="Item ID",
        description="The ID of the item",
        ge=1,                   # Greater than or equal
        le=1000,                # Less than or equal
        example=42
    )
):
    return {"item_id": item_id}
```

## Query Parameters

```python
from fastapi import Query

@app.get("/items/")
async def read_items(
    q: str | None = Query(
        default=None,
        min_length=3,
        max_length=50,
        pattern="^fixedquery$",  # Regex pattern
        title="Query string",
        description="Query for items",
        alias="item-query",      # Use different name in URL
        deprecated=False,
        include_in_schema=True
    ),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, le=100)
):
    return {"q": q, "skip": skip, "limit": limit}

# Multiple values
@app.get("/items/")
async def read_items(q: list[str] = Query(default=[])):
    return {"q": q}  # ?q=foo&q=bar -> {"q": ["foo", "bar"]}
```

## Request Body

```python
from fastapi import Body
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item

# Multiple bodies
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(default=1, ge=1, le=5)
):
    return {"item_id": item_id, "item": item, "user": user}

# Embed single body
@app.post("/items/")
async def create_item(item: Item = Body(embed=True)):
    # Expects: {"item": {"name": "...", "price": ...}}
    return item
```

## Headers

```python
from fastapi import Header

@app.get("/items/")
async def read_items(
    user_agent: str | None = Header(default=None),
    x_token: str = Header(..., alias="X-Token"),
    x_tokens: list[str] = Header(default=[])
):
    return {"User-Agent": user_agent, "X-Token": x_token}
```

## Cookies

```python
from fastapi import Cookie

@app.get("/items/")
async def read_items(
    session_id: str | None = Cookie(default=None),
    tracking_id: str = Cookie(...)
):
    return {"session_id": session_id}
```

## Form Data

```python
from fastapi import Form

@app.post("/login/")
async def login(
    username: str = Form(...),
    password: str = Form(...)
):
    return {"username": username}
```

## File Uploads

```python
from fastapi import File, UploadFile

# Simple file (bytes)
@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

# UploadFile (recommended for large files)
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }

# Multiple files
@app.post("/files/")
async def create_files(files: list[UploadFile]):
    return {"filenames": [f.filename for f in files]}

# File with form data
@app.post("/files/")
async def create_file(
    file: UploadFile,
    description: str = Form(...)
):
    return {"filename": file.filename, "description": description}
```

### UploadFile Attributes & Methods

```python
file.filename       # Original filename
file.content_type   # MIME type (e.g., "image/png")
file.file           # SpooledTemporaryFile object
file.headers        # Headers

await file.read()   # Read contents
await file.write(data)
await file.seek(0)  # Go to start
await file.close()
```
