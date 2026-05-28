# Mocking Patterns with Pytest

## Setup

```bash
uv add --dev pytest-mock
```

## Basic Mocking with pytest-mock

```python
def test_with_mocker(mocker):
    """pytest-mock provides the mocker fixture."""
    mock_function = mocker.patch("mypackage.api.fetch_data")
    mock_function.return_value = {"data": "test"}
    
    result = process_data()
    
    assert result["data"] == "test"
    mock_function.assert_called_once()
```

## Mock Return Values

```python
def test_return_value(mocker):
    """Simple return value."""
    mock = mocker.patch("mypackage.api.get_user")
    mock.return_value = {"id": 1, "name": "Test"}
    
    user = get_user(1)
    assert user["name"] == "Test"


def test_side_effect(mocker):
    """Different return values on successive calls."""
    mock = mocker.patch("mypackage.api.fetch")
    mock.side_effect = [
        {"page": 1},
        {"page": 2},
        {"page": 3},
    ]
    
    assert fetch()["page"] == 1
    assert fetch()["page"] == 2
    assert fetch()["page"] == 3


def test_exception(mocker):
    """Raise exception."""
    mock = mocker.patch("mypackage.api.fetch")
    mock.side_effect = ConnectionError("Network error")
    
    with pytest.raises(ConnectionError):
        fetch()
```

## Patch Decorators

```python
from unittest.mock import patch

@patch("mypackage.api.requests.get")
def test_with_patch_decorator(mock_get):
    """Using @patch decorator."""
    mock_get.return_value.json.return_value = {"id": 1}
    mock_get.return_value.status_code = 200
    
    user = fetch_user(1)
    
    assert user["id"] == 1
    mock_get.assert_called_once_with("https://api.example.com/users/1")


@patch("mypackage.api.database.save")
@patch("mypackage.api.database.fetch")
def test_multiple_patches(mock_fetch, mock_save):
    """Multiple patches (bottom-up order)."""
    mock_fetch.return_value = {"id": 1}
    
    result = update_user(1, {"name": "New Name"})
    
    mock_fetch.assert_called_once_with(1)
    mock_save.assert_called_once()
```

## Mocking Classes

```python
def test_mock_class(mocker):
    """Mock entire class."""
    MockDatabase = mocker.patch("mypackage.database.Database")
    mock_instance = MockDatabase.return_value
    mock_instance.query.return_value = [{"id": 1}]
    
    db = Database()
    results = db.query("SELECT * FROM users")
    
    assert len(results) == 1
    mock_instance.query.assert_called_once()


def test_mock_method(mocker):
    """Mock single method."""
    db = Database()
    mocker.patch.object(db, "query", return_value=[{"id": 1}])
    
    results = db.query("SELECT * FROM users")
    
    assert len(results) == 1
```

## Spying (Partial Mocking)

```python
def test_spy_on_function(mocker):
    """Spy lets original function run while tracking calls."""
    spy = mocker.spy(mypackage.api, "fetch_data")
    
    result = fetch_and_process()
    
    spy.assert_called_once()
    assert result is not None  # Real function executed
```

## Mock Attributes

```python
def test_mock_attributes(mocker):
    """Mock object attributes."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1}
    mock_response.headers = {"Content-Type": "application/json"}
    
    # Use the mock
    assert mock_response.status_code == 200
    assert mock_response.json()["id"] == 1
```

## Assertions

```python
def test_call_assertions(mocker):
    """Various assertion patterns."""
    mock = mocker.patch("mypackage.api.fetch")
    
    fetch(1)
    fetch(2)
    
    # Called
    mock.assert_called()
    
    # Call count
    assert mock.call_count == 2
    
    # Last call
    mock.assert_called_with(2)
    
    # Any call
    mock.assert_any_call(1)
    
    # All calls
    assert mock.call_args_list == [
        mocker.call(1),
        mocker.call(2),
    ]


def test_not_called(mocker):
    """Assert function was never called."""
    mock = mocker.patch("mypackage.api.fetch")
    
    # Do something that shouldn't call fetch
    process_cached_data()
    
    mock.assert_not_called()
```

## Context Managers

```python
def test_mock_context_manager(mocker):
    """Mock context manager."""
    mock_file = mocker.mock_open(read_data="file content")
    mocker.patch("builtins.open", mock_file)
    
    with open("test.txt") as f:
        content = f.read()
    
    assert content == "file content"
    mock_file.assert_called_once_with("test.txt")
```

## Async Mocking

```python
from unittest.mock import AsyncMock

async def test_async_mock(mocker):
    """Mock async function."""
    mock_fetch = mocker.patch("mypackage.api.fetch_async", new=AsyncMock())
    mock_fetch.return_value = {"data": "test"}
    
    result = await fetch_and_process()
    
    assert result["data"] == "test"
    mock_fetch.assert_awaited_once()


async def test_async_side_effect(mocker):
    """Async side effects."""
    mock_fetch = mocker.patch("mypackage.api.fetch_async", new=AsyncMock())
    mock_fetch.side_effect = [
        {"page": 1},
        {"page": 2},
    ]
    
    page1 = await fetch_async()
    page2 = await fetch_async()
    
    assert page1["page"] == 1
    assert page2["page"] == 2
```

## HTTP Mocking with respx

```bash
uv add --dev respx
```

```python
import httpx
import respx

@respx.mock
async def test_http_mock():
    """Mock HTTP requests with respx."""
    respx.get("https://api.example.com/users/1").respond(
        json={"id": 1, "name": "John"},
        status_code=200,
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/users/1")
    
    assert response.status_code == 200
    assert response.json()["name"] == "John"


@pytest.fixture
def mock_api():
    """Reusable HTTP mock fixture."""
    with respx.mock:
        respx.get("https://api.example.com/data").respond(json={"ok": True})
        yield respx


async def test_with_mock_fixture(mock_api):
    """Use mock fixture."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
    
    assert response.json()["ok"] is True
```

## Environment Variables

```python
def test_with_env_var(mocker):
    """Mock environment variable."""
    mocker.patch.dict("os.environ", {"API_KEY": "test-key"})
    
    api_key = os.getenv("API_KEY")
    assert api_key == "test-key"


def test_with_monkeypatch(monkeypatch):
    """Using built-in monkeypatch fixture."""
    monkeypatch.setenv("API_KEY", "test-key")
    monkeypatch.setattr("mypackage.config.DEBUG", True)
    
    assert os.getenv("API_KEY") == "test-key"
    assert mypackage.config.DEBUG is True
```

## Best Practices

### DO:
- Mock external dependencies (APIs, databases, file I/O)
- Use `mocker` fixture from pytest-mock
- Assert calls with specific arguments
- Mock at the boundary (where your code calls external code)
- Use `respx` for HTTP mocking with httpx

### DON'T:
- Mock internal implementation details
- Over-mock (some integration is good)
- Mock standard library unless necessary
- Forget to verify mock was called when expected
- Use mocks as a substitute for poor architecture

## Common Patterns

### Mock Database

```python
@pytest.fixture
def mock_db(mocker):
    """Mock database connection."""
    mock = mocker.Mock()
    mock.query.return_value = []
    mock.insert.return_value = {"id": 1}
    return mock

def test_with_mock_db(mock_db):
    service = UserService(mock_db)
    user = service.create({"name": "Test"})
    
    assert user["id"] == 1
    mock_db.insert.assert_called_once()
```

### Mock File Operations

```python
def test_read_file(mocker):
    """Mock file reading."""
    mock_open = mocker.mock_open(read_data="test content")
    mocker.patch("builtins.open", mock_open)
    
    content = read_config("config.txt")
    
    assert content == "test content"
```

### Mock Time

```python
def test_timestamp(mocker):
    """Mock time.time()."""
    mocker.patch("time.time", return_value=1234567890.0)
    
    timestamp = get_current_timestamp()
    
    assert timestamp == 1234567890.0
```
