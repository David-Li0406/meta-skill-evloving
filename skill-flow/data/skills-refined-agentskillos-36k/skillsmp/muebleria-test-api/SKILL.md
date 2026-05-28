---
name: muebleria-test-api
description: >
  Backend API testing patterns with pytest for Flask endpoints.
  Trigger: When writing tests for Flask routes, models, or database operations.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Writing API tests"
    - "Testing Flask endpoints"
    - "Database testing"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Writing tests for Flask API endpoints
- Testing database models and relationships
- Testing business logic
- Mocking database operations
- Integration testing

---

## Testing Strategy

```
Unit Tests         → Individual functions, models
Integration Tests  → API endpoints + database
Fixtures           → Reusable test data
Mocking            → Isolate external dependencies
```

---

## Critical Patterns

### Pattern 1: Test Setup

```python
# backend/tests/conftest.py
import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_producto(app):
    from app.models import Producto, Categoria
    
    categoria = Categoria(nombre='Sofás')
    db.session.add(categoria)
    db.session.flush()
    
    producto = Producto(
        sku='SOF001',
        nombre='Sofá 3 Cuerpos',
        precio=1500,
        material='Tela',
        id_categoria=categoria.id_categoria
    )
    db.session.add(producto)
    db.session.commit()
    
    return producto
```

### Pattern 2: Endpoint Testing

```python
# backend/tests/test_productos.py
def test_get_productos(client):
    """Test GET /api/productos returns product list"""
    response = client.get('/api/productos')
    
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_producto(client):
    """Test POST /api/productos creates new product"""
    data = {
        'sku': 'SOF001',
        'nombre': 'Sofá 3 Cuerpos',
        'precio': 1500,
        'material': 'Tela',
        'id_categoria': 1
    }
    
    response = client.post('/api/productos', json=data)
    
    assert response.status_code == 201
    assert response.json['mensaje'] == 'Producto creado exitosamente'
    assert response.json['producto']['sku'] == 'SOF001'

def test_create_producto_missing_field(client):
    """Test POST /api/productos validates required fields"""
    data = {'nombre': 'Sofá'}  # Missing required fields
    
    response = client.post('/api/productos', json=data)
    
    assert response.status_code == 400
    assert 'error' in response.json
```

### Pattern 3: Model Testing

```python
# backend/tests/test_models.py
from app.models import Producto, Categoria

def test_producto_to_dict(app, sample_producto):
    """Test Producto.to_dict() serialization"""
    result = sample_producto.to_dict()
    
    assert result['sku'] == 'SOF001'
    assert result['precio'] == 1500.0
    assert 'nombre' in result

def test_producto_relationship(app):
    """Test Producto-Categoria relationship"""
    categoria = Categoria(nombre='Mesas')
    producto = Producto(
        sku='MES001',
        nombre='Mesa Comedor',
        precio=800,
        material='Madera',
        id_categoria=categoria.id_categoria
    )
    
    db.session.add_all([categoria, producto])
    db.session.commit()
    
    assert producto.categoria.nombre == 'Mesas'
```

### Pattern 4: Business Logic Testing

```python
# backend/tests/test_ordenes.py
def test_create_orden_deducts_stock(client, app):
    """Test creating order deducts inventory"""
    from app.models import Inventario, Producto
    
    # Setup: Create product with stock
    producto = Producto(...)
    inventario = Inventario(id_producto=producto.id_producto, cantidad_stock=10)
    db.session.add_all([producto, inventario])
    db.session.commit()
    
    # Create order
    order_data = {
        'id_cliente': 1,
        'items': [{'id_producto': producto.id_producto, 'cantidad': 3}]
    }
    
    response = client.post('/api/ordenes', json=order_data)
    
    # Assert: Stock was deducted
    assert response.status_code == 201
    
    inventario_updated = Inventario.query.filter_by(
        id_producto=producto.id_producto
    ).first()
    assert inventario_updated.cantidad_stock == 7

def test_create_orden_insufficient_stock(client, app):
    """Test order fails with insufficient stock"""
    # Setup: Product with low stock
    inventario = Inventario(id_producto=1, cantidad_stock=1)
    db.session.add(inventario)
    db.session.commit()
    
    # Try to order more than available
    order_data = {
        'id_cliente': 1,
        'items': [{'id_producto': 1, 'cantidad': 5}]
    }
    
    response = client.post('/api/ordenes', json=order_data)
    
    assert response.status_code == 400
    assert 'stock' in response.json['error'].lower()
```

---

## Commands

```bash
# Install pytest
pip install pytest pytest-flask pytest-cov

# Run all tests
pytest backend/tests/

# Run specific test file
pytest backend/tests/test_productos.py

# Run with coverage
pytest --cov=backend/app backend/tests/

# Run verbose
pytest -v

# Run only failed tests
pytest --lf
```

---

## Best Practices

```python
# ✅ DO: Use descriptive test names
def test_create_producto_validates_required_fields():
    pass

# ✅ DO: Arrange-Act-Assert pattern
def test_example():
    # Arrange
    data = {...}
    
    # Act
    response = client.post('/api/endpoint', json=data)
    
    # Assert
    assert response.status_code == 201

# ✅ DO: Use fixtures for reusable data
@pytest.fixture
def sample_cliente():
    return Cliente(nombre='Juan', email='juan@test.com')

# ❌ DON'T: Test multiple things in one test
def test_everything():  # Bad
    test_create()
    test_update()
    test_delete()
```

---

## QA Checklist

- [ ] Tests cover CRUD operations
- [ ] Error cases tested (400, 404, 500)
- [ ] Business logic validated
- [ ] Database rollback after each test
- [ ] Fixtures clean up properly
- [ ] No hardcoded IDs (use fixtures)
- [ ] Test edge cases (empty lists, null values)

---

## Resources

- **pytest**: https://docs.pytest.org
- **Flask Testing**: https://flask.palletsprojects.com/testing
