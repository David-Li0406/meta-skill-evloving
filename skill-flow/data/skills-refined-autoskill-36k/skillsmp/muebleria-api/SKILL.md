---
name: muebleria-api
description: >
  MuebleriaIris API patterns: Flask + SQLAlchemy + PostgreSQL ERP backend.
  Trigger: When working in backend/ on routes, models, or database operations.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Creating/modifying API endpoints"
    - "Working with database models"
    - "Implementing business logic"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Creating or modifying Flask API endpoints
- Defining SQLAlchemy models
- Implementing business logic (orders, inventory, CRUD)
- Working with PostgreSQL database
- Handling CORS and API security

---

## Tech Stack

```
Flask + Flask-SQLAlchemy + PostgreSQL 15+
Flask-CORS | Python-dotenv | psycopg2-binary
```

---

## Critical Patterns

### Pattern 1: ERP Modules (4 Core)

1. **Catálogo**: Productos, Categorías, Imágenes
2. **Logística**: Inventario, Proveedores, Stock
3. **Comercial**: Clientes, Órdenes, Detalles, Pagos (MercadoPago)
4. **Administración**: Usuarios, Roles

### Pattern 2: API Response Structure

```python
# Success (201)
return jsonify({
    "mensaje": "Producto creado exitosamente",
    "producto": producto.to_dict()
}), 201

# Error (400)
return jsonify({"error": "Campo requerido"}), 400
```

### Pattern 3: Business Logic (Order Creation)

```python
try:
    # 1. Create order header
    orden = Orden(id_cliente=data['id_cliente'], monto_total=0)
    db.session.add(orden)
    db.session.flush()  # Generate ID
    
    # 2. Process items + check stock
    for item in data['items']:
        producto = Producto.query.get(item['id_producto'])
        inventario = Inventario.query.filter_by(id_producto=producto.id_producto).first()
        
        if inventario.cantidad_stock < item['cantidad']:
            raise ValueError('Stock insuficiente')
        
        # Create detail + deduct stock
        detalle = DetalleOrden(...)
        db.session.add(detalle)
        inventario.cantidad_stock -= item['cantidad']
    
    # 3. Update total + commit
    orden.monto_total = total_calculado
    db.session.commit()
    
except Exception as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), 500
```

---

## Model Patterns

```python
from . import db
from datetime import datetime, timezone

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id_producto = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'))
    
    # Relationships
    imagenes = db.relationship('ImagenProducto', cascade='all, delete-orphan')
    inventario = db.relationship('Inventario', uselist=False)
    
    def to_dict(self):
        return {'id': self.id_producto, 'precio': float(self.precio)}
```

---

## API Endpoints

**Catálogo:**
- `GET/POST /api/categorias`
- `GET/POST /api/productos`
- `GET/PUT/DELETE /api/productos/:id`

**Logística:**
- `GET/POST /api/proveedores`
- `GET/POST /api/inventario`

**Comercial:**
- `GET/POST /api/clientes`
- `GET/POST /api/ordenes`
- `PATCH /api/ordenes/:id/estado`

---

## Commands

```bash
pip install -r backend/requirements.txt
python backend/run.py    # Start API server
```

---

## Resources

- **Models**: `backend/app/models.py` (428 lines)
- **Routes**: `backend/app/routes.py` (852 lines)
- **Config**: `backend/config.py`
