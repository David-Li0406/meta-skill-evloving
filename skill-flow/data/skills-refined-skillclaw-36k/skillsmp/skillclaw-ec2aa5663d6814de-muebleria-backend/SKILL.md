---
name: muebleria-backend
description: Use this skill when developing a Flask backend for MuebleriaIris, including API creation, database management, and Python dependency handling.
---

# Skill body

## When to Use

Use this skill when:

- Creating or modifying Flask API endpoints
- Defining SQLAlchemy models
- Implementing business logic (orders, inventory, CRUD)
- Working with PostgreSQL database
- Managing Python dependencies and virtual environments
- Debugging Python errors and following best practices

## Tech Stack

```
Flask + Flask-SQLAlchemy + PostgreSQL 15+
Python 3.9+ | Flask 3.0+ | SQLAlchemy 2.0+
Flask-CORS | Python-dotenv | psycopg2-binary
```

## Critical Patterns

### API Response Structure

```python
# Success (201)
return jsonify({
    "mensaje": "Producto creado exitosamente",
    "producto": producto.to_dict()
}), 201

# Error (400)
return jsonify({"error": "Campo requerido"}), 400
```

### Business Logic (Order Creation)

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

### Virtual Environment Setup

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

### Import Structure

```python
# Standard library imports
from datetime import datetime, timezone
import os

# Third-party imports
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Local imports
from . import db
from .models import Producto, Cliente
```

### Error Handling

```python
try:
    # Database operation
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify({'mensaje': 'Éxito'}), 201
except Exception as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), 500
```

## Code Style

### Naming Conventions

```python
# Variables and functions: snake_case
nombre_producto = "Sofá"
def crear_producto():
    pass

# Classes: PascalCase
class Producto(db.Model):
    pass

# Constants: UPPER_SNAKE_CASE
API_BASE_URL = "http://localhost:5000"
```

### Docstrings

```python
def create_orden(data):
    """
    Crea una nueva orden de venta.
    
    Args:
        data (dict): Datos de la orden con id_cliente e items
        
    Returns:
        tuple: (response_json, status_code)
        
    Raises:
        ValueError: Si el stock es insuficiente
    """
    pass
```