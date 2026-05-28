---
name: muebleria-python
description: >
  Python development patterns for MuebleriaIris backend.
  Trigger: When writing Python code in backend/, working with Flask, or managing dependencies.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Writing Python backend code"
    - "Managing Python dependencies"
    - "Setting up virtual environments"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Writing Python code for Flask backend
- Managing dependencies with pip/requirements.txt
- Setting up virtual environments
- Debugging Python errors
- Following Python best practices

---

## Tech Stack

```
Python 3.9+ | Flask 3.0+ | SQLAlchemy 2.0+
Virtual environments (venv) | pip
```

---

## Critical Patterns

### Pattern 1: Virtual Environment Setup

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

### Pattern 2: Import Structure

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

### Pattern 3: Error Handling

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

---

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

---

## Common Tasks

### Environment Variables

```python
# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost/muebleria_erp'
```

### Flask Factory Pattern

```python
# backend/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    CORS(app)
    
    from .routes import main
    app.register_blueprint(main)
    
    return app
```

---

## Debugging

```python
# Print debugging (development only)
print(f"DEBUG: {variable}")

# Flask debug mode (backend/run.py)
if __name__ == "__main__":
    app.run(debug=True)

# Python debugger
import pdb; pdb.set_trace()
```

---

## Commands

```bash
# Run Flask app
python backend/run.py

# Python REPL
python

# Check Python version
python --version

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
