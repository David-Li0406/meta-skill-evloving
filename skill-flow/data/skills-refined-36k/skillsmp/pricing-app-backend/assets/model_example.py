"""
Example SQLAlchemy model following Pricing App patterns.
Shows: proper types, relationships, indexes, timestamps.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Producto(Base):
    """
    Producto from ERP system.
    Represents items available for sale.
    """
    __tablename__ = "productos_erp"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Core fields
    codigo = Column(String(50), nullable=False, unique=True, comment="Unique product code")
    descripcion = Column(String(255), nullable=False, comment="Product description")
    titulo_ml = Column(String(255), nullable=True, comment="MercadoLibre listing title")
    
    # Pricing
    costo = Column(Integer, nullable=False, comment="Cost in cents")
    precio_lista = Column(Integer, nullable=True, comment="List price in cents")
    
    # Relationships
    marca_id = Column(Integer, ForeignKey("marcas.id", ondelete="SET NULL"), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="SET NULL"), nullable=True)
    
    # Metadata
    activo = Column(Integer, default=1, comment="1=active, 0=inactive")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    marca = relationship("Marca", back_populates="productos")
    categoria = relationship("Categoria", back_populates="productos")
    ventas = relationship("VentaDetalle", back_populates="producto")
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_producto_codigo", "codigo"),
        Index("idx_producto_marca", "marca_id"),
        Index("idx_producto_categoria", "categoria_id"),
        Index("idx_producto_activo", "activo"),
        Index("idx_producto_titulo_ml", "titulo_ml"),  # For ML sync
    )
    
    def __repr__(self):
        return f"<Producto(id={self.id}, codigo={self.codigo}, descripcion={self.descripcion})>"

class Marca(Base):
    """Brand/Manufacturer"""
    __tablename__ = "marcas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    porcentaje_markup = Column(Numeric(5, 2), nullable=True, comment="Default markup %")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    productos = relationship("Producto", back_populates="marca")
    
    __table_args__ = (
        Index("idx_marca_nombre", "nombre"),
    )

class VentaDetalle(Base):
    """Sale line items"""
    __tablename__ = "tb_sale_order_detail"
    
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("tb_sale_order_header.id", ondelete="CASCADE"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos_erp.id", ondelete="RESTRICT"), nullable=False)
    
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Integer, nullable=False, comment="Unit price in cents")
    descuento = Column(Integer, nullable=True, default=0, comment="Discount in cents")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="ventas")
    
    __table_args__ = (
        Index("idx_venta_detalle_venta", "venta_id"),
        Index("idx_venta_detalle_producto", "producto_id"),
        Index("idx_venta_detalle_created", "created_at"),
    )
    
    @property
    def subtotal(self) -> int:
        """Calculate subtotal (price * quantity - discount)"""
        return (self.precio_unitario * self.cantidad) - (self.descuento or 0)
