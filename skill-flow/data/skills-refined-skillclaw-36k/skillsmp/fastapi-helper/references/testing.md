# FastAPI Testing Reference

## TestClient Setup

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

## Async Testing

```python
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
```

## Testing with Dependencies Override

```python
from fastapi.testclient import TestClient
from main import app, get_db

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={"name": "Test", "price": 10.0})
    assert response.status_code == 201

# Clean up after tests
def teardown_module():
    app.dependency_overrides = {}
```

## Testing Different Request Types

```python
# GET with query params
def test_read_items():
    response = client.get("/items/?skip=0&limit=10")
    assert response.status_code == 200

# POST with JSON body
def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Foo", "price": 42.0}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Foo"

# PUT with path params
def test_update_item():
    response = client.put(
        "/items/1",
        json={"name": "Updated", "price": 50.0}
    )
    assert response.status_code == 200

# DELETE
def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 204

# With headers
def test_with_auth():
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200

# With cookies
def test_with_cookies():
    response = client.get(
        "/items/",
        cookies={"session": "abc123"}
    )
    assert response.status_code == 200

# File upload
def test_upload_file():
    response = client.post(
        "/uploadfile/",
        files={"file": ("test.txt", b"file content", "text/plain")}
    )
    assert response.status_code == 200

# Form data
def test_login():
    response = client.post(
        "/login/",
        data={"username": "test", "password": "secret"}
    )
    assert response.status_code == 200
```

## Testing WebSockets

```python
def test_websocket():
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello")
        data = websocket.receive_text()
        assert data == "Message received: Hello"
```

## Pytest Fixtures

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}

def test_create_item(client):
    response = client.post("/items/", json={"name": "Test", "price": 10.0})
    assert response.status_code == 201
```
