"""
Example service layer following Pricing App patterns.
Shows: business logic separation, external API integration, error handling.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.producto import Producto
from app.core.config import settings
import httpx

class PricingService:
    """
    Business logic for pricing calculations.
    Handles markup, shipping costs, MercadoLibre fees, etc.
    """
    
    @staticmethod
    def calcular_precio_venta(
        costo: int,
        markup_percentage: float,
        incluir_envio: bool = False,
        tipo_publicacion: str = "clasica"
    ) -> dict:
        """
        Calculate final selling price based on cost and markup.
        
        Args:
            costo: Product cost in cents
            markup_percentage: Markup percentage (e.g., 15.5 for 15.5%)
            incluir_envio: Whether to include shipping in calculation
            tipo_publicacion: "clasica" or "premium" (affects ML fees)
        
        Returns:
            dict with breakdown: {
                "costo": int,
                "markup": int,
                "comision_ml": int,
                "envio": int,
                "precio_final": int,
                "ganancia_neta": int
            }
        """
        # Base calculation
        markup = int(costo * (markup_percentage / 100))
        precio_base = costo + markup
        
        # MercadoLibre commission
        comision_rate = 0.14 if tipo_publicacion == "premium" else 0.12
        comision_ml = int(precio_base * comision_rate)
        
        # Shipping cost (if applicable)
        envio = 500 if incluir_envio else 0  # Example: fixed $5.00
        
        # Final price
        precio_final = precio_base + comision_ml + envio
        ganancia_neta = precio_final - costo - comision_ml - envio
        
        return {
            "costo": costo,
            "markup": markup,
            "comision_ml": comision_ml,
            "envio": envio,
            "precio_final": precio_final,
            "ganancia_neta": ganancia_neta,
            "margen_porcentaje": round((ganancia_neta / precio_final) * 100, 2)
        }
    
    @staticmethod
    async def sync_producto_to_ml(
        producto_id: int,
        db: Session
    ) -> dict:
        """
        Sync producto to MercadoLibre.
        Creates or updates ML listing.
        
        Args:
            producto_id: ID of producto to sync
            db: Database session
        
        Returns:
            dict with ML item_id and status
        
        Raises:
            ValueError: If producto not found
            httpx.HTTPError: If ML API fails
        """
        # Get producto
        producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if not producto:
            raise ValueError(f"Producto {producto_id} no encontrado")
        
        # Build ML payload
        payload = {
            "title": producto.titulo_ml or producto.descripcion,
            "category_id": "MLA1051",  # Example category
            "price": producto.precio_lista / 100 if producto.precio_lista else None,
            "currency_id": "ARS",
            "available_quantity": 1,
            "buying_mode": "buy_it_now",
            "listing_type_id": "gold_special",
            "condition": "new",
            "description": {"plain_text": producto.descripcion},
        }
        
        # Call ML API
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {settings.ML_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            response = await client.post(
                "https://api.mercadolibre.com/items",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        return {
            "item_id": data.get("id"),
            "permalink": data.get("permalink"),
            "status": data.get("status")
        }

class PermisosService:
    """
    Business logic for permission checks.
    """
    
    PERMISOS_CATEGORIAS = {
        "admin": ["config", "ventas", "productos", "reportes"],
        "ventas": ["ventas", "productos"],
        "logistica": ["productos"],
        "viewer": []
    }
    
    @staticmethod
    def tiene_permiso(user_roles: List[str], permiso_requerido: str) -> bool:
        """
        Check if user has required permission.
        
        Args:
            user_roles: List of role names (e.g., ["admin", "ventas"])
            permiso_requerido: Permission to check (e.g., "config")
        
        Returns:
            True if user has permission, False otherwise
        """
        for role in user_roles:
            permisos = PermisosService.PERMISOS_CATEGORIAS.get(role, [])
            if permiso_requerido in permisos:
                return True
        return False
    
    @staticmethod
    def get_permisos_usuario(user_roles: List[str]) -> List[str]:
        """
        Get all permissions for user based on roles.
        
        Args:
            user_roles: List of role names
        
        Returns:
            List of unique permissions
        """
        permisos = set()
        for role in user_roles:
            permisos.update(PermisosService.PERMISOS_CATEGORIAS.get(role, []))
        return sorted(list(permisos))
