"""
Todo API Example
A complete todo list API with categories, search, filtering, and status management.
"""

from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from contextlib import asynccontextmanager

from database import engine, get_db, Base
from models import (
    Todo, TodoCreate, TodoUpdate,
    Category, CategoryCreate,
    TodoWithCategory, PaginatedTodosResponse
)
from schemas import Todo as TodoModel, Category as CategoryModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup"""
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Todo API",
    description="Complete todo list management API with categories and filtering",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== Todo Endpoints ==========

@app.post("/todos", response_model=TodoWithCategory, status_code=status.HTTP_201_CREATED, tags=["Todos"])
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo item"""
    
    # Verify category exists if provided
    if todo.category_id:
        category = db.query(CategoryModel).filter(
            CategoryModel.id == todo.category_id
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {todo.category_id} not found"
            )
    
    db_todo = TodoModel(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    
    return db_todo


@app.get("/todos", response_model=PaginatedTodosResponse, tags=["Todos"])
async def get_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    completed: Optional[bool] = None,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all todos with filtering and pagination
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    - **completed**: Filter by completion status (optional)
    - **category_id**: Filter by category (optional)
    - **search**: Search in title and description (optional)
    """
    query = db.query(TodoModel)
    
    # Apply filters
    if completed is not None:
        query = query.filter(TodoModel.completed == completed)
    
    if category_id is not None:
        query = query.filter(TodoModel.category_id == category_id)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (TodoModel.title.ilike(search_pattern)) |
            (TodoModel.description.ilike(search_pattern))
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination and get results
    todos = query.offset(skip).limit(limit).all()
    
    return {
        "todos": todos,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@app.get("/todos/{todo_id}", response_model=TodoWithCategory, tags=["Todos"])
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo by ID"""
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo


@app.put("/todos/{todo_id}", response_model=TodoWithCategory, tags=["Todos"])
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db)
):
    """Update a todo item"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    # Verify category exists if being updated
    if todo_update.category_id is not None:
        category = db.query(CategoryModel).filter(
            CategoryModel.id == todo_update.category_id
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {todo_update.category_id} not found"
            )
    
    # Update fields
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)
    
    db.commit()
    db.refresh(db_todo)
    
    return db_todo


@app.patch("/todos/{todo_id}/toggle", response_model=TodoWithCategory, tags=["Todos"])
async def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    """Toggle todo completion status"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    db_todo.completed = not db_todo.completed
    db.commit()
    db.refresh(db_todo)
    
    return db_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todos"])
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo item"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    db.delete(db_todo)
    db.commit()


# ========== Category Endpoints ==========

@app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED, tags=["Categories"])
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category"""
    
    # Check if category name already exists
    existing = db.query(CategoryModel).filter(
        CategoryModel.name == category.name
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )
    
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@app.get("/categories", response_model=List[Category], tags=["Categories"])
async def get_categories(db: Session = Depends(get_db)):
    """Get all categories"""
    categories = db.query(CategoryModel).all()
    return categories


@app.get("/categories/{category_id}", response_model=Category, tags=["Categories"])
async def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID"""
    category = db.query(CategoryModel).filter(
        CategoryModel.id == category_id
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    return category


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Categories"])
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category"""
    db_category = db.query(CategoryModel).filter(
        CategoryModel.id == category_id
    ).first()
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    
    db.delete(db_category)
    db.commit()


# ========== Statistics Endpoint ==========

@app.get("/stats", tags=["Statistics"])
async def get_statistics(db: Session = Depends(get_db)):
    """Get todo statistics"""
    total = db.query(TodoModel).count()
    completed = db.query(TodoModel).filter(TodoModel.completed == True).count()
    active = total - completed
    
    categories = db.query(CategoryModel).count()
    
    return {
        "total_todos": total,
        "completed": completed,
        "active": active,
        "completion_rate": round((completed / total * 100) if total > 0 else 0, 2),
        "total_categories": categories
    }


@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint"""
    return {
        "message": "Todo API",
        "docs": "/docs",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
