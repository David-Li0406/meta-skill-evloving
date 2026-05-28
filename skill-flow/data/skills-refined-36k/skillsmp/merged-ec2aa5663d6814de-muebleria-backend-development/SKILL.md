---
name: muebleria-backend-development
description: Use this skill when developing the MuebleriaIris backend with Flask and SQLAlchemy, managing dependencies, or implementing business logic.
---

# When to Use

Use this skill when:

- Creating or modifying Flask API endpoints
- Defining SQLAlchemy models
- Implementing business logic (orders, inventory, CRUD)
- Working with PostgreSQL database
- Managing Python dependencies with pip
- Setting up virtual environments
- Debugging Python errors
- Following Python best practices

---

## Tech Stack

```
Flask + Flask-SQLAlchemy + PostgreSQL 15+
Python 3.9+ | Flask 3.0+ | SQLAlchemy 2.0+
Virtual environments (venv) | pip
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

### Pattern 4: Virtual Environment Setup

```bash
# Create venv
python3 -m venv backend/venv

# Activate (Linux/Mac)
source backend/venv/bin/activate

# Activate (Windows)
backend\venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Freeze dependencies
pip freeze > backend/requirements.txt
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
# Start API server
python backend/run.py

# Install specific package
pip install flask-cors

# Uninstall package
pip uninstall flask-cors

# List installed packages
pip list
```

---

## QA Checklist

- [ ] Use type hints for function parameters
- [ ] Handle exceptions with try/except
- [ ] Use environment variables for sensitive data
- [ ] Follow PEP 8 style guide
- [ ] Add docstrings to functions
- [ ] Use virtual environment (never global pip)
- [ ] Keep requirements.txt updated

---

## Resources

- **PEP 8**: Python style guide
- **Flask Docs**: https://flask.palletsprojects.com
- **SQLAlchemy**: https://www.sqlalchemy.org