# Advanced Testing Patterns

## Dependency Override Patterns

### Database Override

```python
@pytest.fixture
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

### Authentication Override

```python
from app.auth import get_current_user

@pytest.fixture
def mock_user():
    return User(id=1, email="test@example.com", is_active=True)

@pytest.fixture
async def authenticated_client(client: AsyncClient, mock_user: User):
    app.dependency_overrides[get_current_user] = lambda: mock_user
    yield client
    app.dependency_overrides.pop(get_current_user, None)

@pytest.fixture
async def admin_client(client: AsyncClient):
    admin = User(id=1, email="admin@example.com", is_admin=True)
    app.dependency_overrides[get_current_user] = lambda: admin
    yield client
    app.dependency_overrides.pop(get_current_user, None)
```

### External Service Override

```python
from app.services import EmailService, get_email_service

class MockEmailService:
    def __init__(self):
        self.sent_emails = []

    async def send(self, to: str, subject: str, body: str):
        self.sent_emails.append({"to": to, "subject": subject, "body": body})

@pytest.fixture
def mock_email_service():
    return MockEmailService()

@pytest.fixture
async def client_with_mock_email(client: AsyncClient, mock_email_service):
    app.dependency_overrides[get_email_service] = lambda: mock_email_service
    yield client, mock_email_service
    app.dependency_overrides.pop(get_email_service, None)

@pytest.mark.asyncio
async def test_registration_sends_welcome_email(client_with_mock_email):
    client, email_service = client_with_mock_email

    response = await client.post("/users/", json={
        "email": "new@example.com",
        "password": "secret123"
    })

    assert response.status_code == 201
    assert len(email_service.sent_emails) == 1
    assert email_service.sent_emails[0]["to"] == "new@example.com"
```

## Parametrize Patterns

### Basic Parametrize

```python
@pytest.mark.asyncio
@pytest.mark.parametrize("name,price,expected_status", [
    ("Valid Item", 10.0, 201),
    ("", 10.0, 422),           # Empty name
    ("Item", -5.0, 422),       # Negative price
    ("A" * 256, 10.0, 422),    # Name too long
])
async def test_create_item_validation(client: AsyncClient, name, price, expected_status):
    response = await client.post("/items/", json={"name": name, "price": price})
    assert response.status_code == expected_status
```

### Parametrize with IDs

```python
@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint,method,expected_status", [
    ("/items/", "GET", 200),
    ("/items/1", "GET", 404),
    ("/items/", "POST", 401),
    ("/users/me", "GET", 401),
], ids=[
    "list_items_ok",
    "get_missing_item",
    "create_requires_auth",
    "me_requires_auth",
])
async def test_endpoint_access(client: AsyncClient, endpoint, method, expected_status):
    response = await getattr(client, method.lower())(endpoint)
    assert response.status_code == expected_status
```

### Parametrize with Fixtures

```python
@pytest.fixture(params=["sqlite", "postgres"])
def database_url(request):
    urls = {
        "sqlite": "sqlite+aiosqlite:///./test.db",
        "postgres": "postgresql+asyncpg://test:test@localhost/test"
    }
    return urls[request.param]
```

## CRUD Test Template

```python
# tests/test_crud_items.py
import pytest
from httpx import AsyncClient
from app.schemas import ItemResponse, ItemCreate

class TestItemsCRUD:
    """Complete CRUD test suite for Items."""

    @pytest.mark.asyncio
    async def test_create_item(self, client: AsyncClient):
        """POST /items/ - Create new item."""
        payload = {"name": "Widget", "price": 29.99, "quantity": 10}

        response = await client.post("/items/", json=payload)

        assert response.status_code == 201
        item = ItemResponse(**response.json())
        assert item.name == "Widget"
        assert item.price == 29.99

    @pytest.mark.asyncio
    async def test_read_item(self, client: AsyncClient, item_factory):
        """GET /items/{id} - Read existing item."""
        created = await item_factory(name="Test Item")

        response = await client.get(f"/items/{created.id}")

        assert response.status_code == 200
        item = ItemResponse(**response.json())
        assert item.id == created.id

    @pytest.mark.asyncio
    async def test_read_item_not_found(self, client: AsyncClient):
        """GET /items/{id} - 404 for non-existent item."""
        response = await client.get("/items/99999")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_item(self, client: AsyncClient, item_factory):
        """PUT /items/{id} - Update existing item."""
        created = await item_factory(name="Original", price=10.0)

        response = await client.put(
            f"/items/{created.id}",
            json={"name": "Updated", "price": 20.0}
        )

        assert response.status_code == 200
        item = ItemResponse(**response.json())
        assert item.name == "Updated"
        assert item.price == 20.0

    @pytest.mark.asyncio
    async def test_partial_update_item(self, client: AsyncClient, item_factory):
        """PATCH /items/{id} - Partial update."""
        created = await item_factory(name="Original", price=10.0)

        response = await client.patch(
            f"/items/{created.id}",
            json={"price": 15.0}
        )

        assert response.status_code == 200
        item = ItemResponse(**response.json())
        assert item.name == "Original"  # Unchanged
        assert item.price == 15.0       # Updated

    @pytest.mark.asyncio
    async def test_delete_item(self, client: AsyncClient, item_factory):
        """DELETE /items/{id} - Delete existing item."""
        created = await item_factory()

        response = await client.delete(f"/items/{created.id}")
        assert response.status_code == 204

        # Verify deleted
        get_response = await client.get(f"/items/{created.id}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_items(self, client: AsyncClient, item_factory):
        """GET /items/ - List all items with pagination."""
        for i in range(5):
            await item_factory(name=f"Item {i}")

        response = await client.get("/items/", params={"page": 1, "size": 3})

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 5
```

## Testing WebSockets

```python
@pytest.mark.asyncio
async def test_websocket_connection():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        async with client.stream("GET", "/ws") as response:
            # For actual WebSocket, use websockets library
            pass

# Using websockets library
import websockets

@pytest.mark.asyncio
async def test_websocket_echo():
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        await ws.send("Hello")
        response = await ws.recv()
        assert response == "Message received: Hello"
```

## Testing Background Tasks

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_endpoint_triggers_background_task(client: AsyncClient):
    with patch("app.tasks.send_notification", new_callable=AsyncMock) as mock_task:
        response = await client.post("/orders/", json={"product_id": 1})

        assert response.status_code == 201
        mock_task.assert_called_once()
```

## Testing File Uploads

```python
@pytest.mark.asyncio
async def test_upload_file(client: AsyncClient):
    file_content = b"test file content"

    response = await client.post(
        "/upload/",
        files={"file": ("test.txt", file_content, "text/plain")}
    )

    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"
    assert response.json()["size"] == len(file_content)

@pytest.mark.asyncio
async def test_upload_multiple_files(client: AsyncClient):
    files = [
        ("files", ("file1.txt", b"content1", "text/plain")),
        ("files", ("file2.txt", b"content2", "text/plain")),
    ]

    response = await client.post("/upload-multiple/", files=files)

    assert response.status_code == 200
    assert len(response.json()["filenames"]) == 2
```
