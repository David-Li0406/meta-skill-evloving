# FastAPI Routing Reference

## Application & Router

### FastAPI Application

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc
    openapi_url="/openapi.json"
)
```

### APIRouter (Modular Routes)

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def read_items():
    return [{"item_id": "Foo"}]

# Include in main app
app.include_router(router)
```

## Route Decorators

### HTTP Methods

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items/", status_code=201)
async def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    return None

@app.patch("/items/{item_id}")
async def partial_update(item_id: int, item: ItemUpdate):
    return {"item_id": item_id}

@app.options("/items/")
async def options_items():
    return {"methods": ["GET", "POST"]}

@app.head("/items/{item_id}")
async def head_item(item_id: int):
    return None
```

### Route Parameters

```python
@app.get(
    "/items/{item_id}",
    response_model=Item,
    status_code=200,
    tags=["items"],
    summary="Get an item",
    description="Get item by ID",
    response_description="The item",
    deprecated=False,
    operation_id="get_item",
    responses={
        200: {"description": "Successful"},
        404: {"description": "Not found"}
    }
)
async def read_item(item_id: int):
    return {"item_id": item_id}
```
