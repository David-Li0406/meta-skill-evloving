"""
Complete CRUD API Example
A full-featured CRUD API for managing users with SQLAlchemy and FastAPI.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from contextlib import asynccontextmanager

from database import engine, get_db, Base
from models import User, UserCreate, UserUpdate
from schemas import User as UserModel


# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="CRUD API Example",
    description="Complete CRUD operations for user management",
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


@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint"""
    return {
        "message": "CRUD API Example",
        "docs": "/docs",
        "endpoints": {
            "create": "POST /users",
            "read_all": "GET /users",
            "read_one": "GET /users/{user_id}",
            "update": "PUT /users/{user_id}",
            "delete": "DELETE /users/{user_id}"
        }
    }


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user
    
    - **email**: User's email address (must be unique)
    - **name**: User's full name
    - **age**: User's age (optional)
    """
    # Check if email already exists
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = UserModel(
        email=user.email,
        name=user.name,
        age=user.age
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@app.get("/users", response_model=List[User], tags=["Users"])
async def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Retrieve all users with pagination
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    """
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit cannot exceed 100"
        )
    
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific user by ID
    
    - **user_id**: The ID of the user to retrieve
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@app.put("/users/{user_id}", response_model=User, tags=["Users"])
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a user's information
    
    - **user_id**: The ID of the user to update
    - **email**: New email (optional)
    - **name**: New name (optional)
    - **age**: New age (optional)
    """
    # Get existing user
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Check if new email already exists (if email is being updated)
    if user_update.email and user_update.email != db_user.email:
        existing_user = db.query(UserModel).filter(
            UserModel.email == user_update.email
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update fields (only if provided)
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user
    
    - **user_id**: The ID of the user to delete
    """
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    db.delete(db_user)
    db.commit()
    
    return None


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
