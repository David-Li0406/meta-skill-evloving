"""
Common Dependencies
Reusable dependencies for FastAPI endpoints.
"""

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import get_db
from config import settings
from typing import Optional


# Pagination dependency
class PaginationParams:
    """Dependency for pagination parameters"""
    
    def __init__(
        self,
        skip: int = 0,
        limit: int = settings.DEFAULT_PAGE_SIZE
    ):
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip must be non-negative"
            )
        
        if limit < 1 or limit > settings.MAX_PAGE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Limit must be between 1 and {settings.MAX_PAGE_SIZE}"
            )
        
        self.skip = skip
        self.limit = limit


# Authentication dependency (example)
async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Dependency to get the current authenticated user.
    Replace with your actual authentication logic.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # TODO: Implement actual token validation
    # Example: Validate JWT token and get user from database
    
    # For now, return a mock user
    return {"id": 1, "email": "user@example.com"}


# Optional authentication dependency
async def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Dependency that returns the current user if authenticated,
    otherwise returns None.
    """
    if not authorization:
        return None
    
    try:
        return await get_current_user(authorization, db)
    except HTTPException:
        return None


# Admin role dependency (example)
async def require_admin(
    current_user: dict = Depends(get_current_user)
):
    """
    Dependency that requires the user to have admin role.
    Raises 403 if user is not an admin.
    """
    # TODO: Implement actual role checking
    # Example: Check if user has 'admin' role in database
    
    is_admin = current_user.get("is_admin", False)
    
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user
