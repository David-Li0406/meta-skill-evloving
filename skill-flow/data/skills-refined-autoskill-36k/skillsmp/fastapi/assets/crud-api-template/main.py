"""
Complete CRUD API Template with FastAPI

This template demonstrates a full CRUD (Create, Read, Update, Delete) API
with proper validation, error handling, and REST principles.
"""

from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from schemas import Item, ItemCreate, ItemUpdate

app = FastAPI(
    title="CRUD API",
    description="A complete CRUD API template built with FastAPI",
    version="1.0.0"
)

# In-memory storage (replace with database in production)
items_db: dict[int, dict] = {}
item_id_counter = 1


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "CRUD API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "items": "/items"
        }
    }


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(item: ItemCreate):
    """
    Create a new item.

    - **name**: Item name (required, 1-100 characters)
    - **description**: Item description (optional, max 500 characters)
    - **price**: Item price (required, must be positive)
    - **tax**: Tax amount (optional, must be non-negative)
    - **in_stock**: Stock status (optional, defaults to True)
    """
    global item_id_counter

    new_item = {
        "id": item_id_counter,
        **item.model_dump(),
        "created_at": datetime.now(),
        "updated_at": None
    }

    items_db[item_id_counter] = new_item
    item_id_counter += 1

    return new_item


@app.get("/items/", response_model=List[Item], tags=["Items"])
async def list_items(
    skip: int = 0,
    limit: int = 100,
    in_stock: bool = None
):
    """
    Retrieve a list of items.

    - **skip**: Number of items to skip (pagination)
    - **limit**: Maximum number of items to return
    - **in_stock**: Filter by stock status (optional)
    """
    items = list(items_db.values())

    # Filter by stock status if specified
    if in_stock is not None:
        items = [item for item in items if item["in_stock"] == in_stock]

    # Apply pagination
    return items[skip: skip + limit]


@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def get_item(item_id: int):
    """
    Retrieve a specific item by ID.

    - **item_id**: The ID of the item to retrieve
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    return items_db[item_id]


@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
async def update_item(item_id: int, item: ItemUpdate):
    """
    Update an existing item.

    - **item_id**: The ID of the item to update
    - All fields are optional; only provided fields will be updated
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    stored_item = items_db[item_id]
    update_data = item.model_dump(exclude_unset=True)

    # Update only the fields that were provided
    for field, value in update_data.items():
        stored_item[field] = value

    stored_item["updated_at"] = datetime.now()

    return stored_item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
async def delete_item(item_id: int):
    """
    Delete an item.

    - **item_id**: The ID of the item to delete
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    del items_db[item_id]
    return None


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "items_count": len(items_db)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
