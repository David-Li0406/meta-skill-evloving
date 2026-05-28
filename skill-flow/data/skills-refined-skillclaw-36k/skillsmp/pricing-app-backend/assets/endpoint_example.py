"""
Example FastAPI endpoint following Pricing App patterns.
Shows: auth, permissions, response models, error handling.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel, ConfigDict
from app.core.deps import get_current_user
from app.models.user import User
from app.utils.permisos import tienePermiso

router = APIRouter(prefix="/api", tags=["productos"])

# Response Model
class ProductoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    descripcion: str
    costo: int
    marca_id: int | None

# Request Model
class ProductoCreate(BaseModel):
    codigo: str
    descripcion: str
    costo: int
    marca_id: int | None = None

@router.get("/productos", response_model=List[ProductoResponse])
async def get_productos(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> List[ProductoResponse]:
    """
    Retrieve all productos with pagination.
    Requires authentication.
    """
    from app.core.database import SessionLocal
    from app.models.producto import Producto
    
    db = SessionLocal()
    try:
        productos = db.query(Producto).offset(skip).limit(limit).all()
        return productos
    finally:
        db.close()

@router.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def create_producto(
    producto: ProductoCreate,
    current_user: User = Depends(get_current_user)
) -> ProductoResponse:
    """
    Create new producto.
    Requires 'config' permission.
    """
    # Check permissions
    if not tienePermiso(current_user, "config"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para esta operación"
        )
    
    from app.core.database import SessionLocal
    from app.models.producto import Producto
    
    db = SessionLocal()
    try:
        # Check if codigo already exists
        existing = db.query(Producto).filter(Producto.codigo == producto.codigo).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Producto con código {producto.codigo} ya existe"
            )
        
        # Create new producto
        db_producto = Producto(**producto.model_dump())
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return db_producto
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear producto: {str(e)}"
        )
    finally:
        db.close()

@router.put("/productos/{producto_id}", response_model=ProductoResponse)
async def update_producto(
    producto_id: int,
    producto: ProductoCreate,
    current_user: User = Depends(get_current_user)
) -> ProductoResponse:
    """
    Update existing producto.
    Requires 'config' permission.
    """
    if not tienePermiso(current_user, "config"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para esta operación"
        )
    
    from app.core.database import SessionLocal
    from app.models.producto import Producto
    
    db = SessionLocal()
    try:
        db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if not db_producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto {producto_id} no encontrado"
            )
        
        for key, value in producto.model_dump().items():
            setattr(db_producto, key, value)
        
        db.commit()
        db.refresh(db_producto)
        return db_producto
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar producto: {str(e)}"
        )
    finally:
        db.close()
