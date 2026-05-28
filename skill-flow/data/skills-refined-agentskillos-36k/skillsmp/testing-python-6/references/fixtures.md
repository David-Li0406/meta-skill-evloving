# Pytest Fixtures Reference

## Fixture Basics

```python
import pytest

@pytest.fixture
def simple_fixture():
    """Returns a value."""
    return {"key": "value"}

def test_uses_fixture(simple_fixture):
    assert simple_fixture["key"] == "value"
```

## Fixture Scopes

| Scope | Lifetime | Use Case |
|-------|----------|----------|
| `function` | Each test (default) | Most fixtures |
| `class` | Per test class | Shared class state |
| `module` | Per test file | Expensive setup |
| `package` | Per package | Rare |
| `session` | Entire test run | Very expensive (DB init) |

```python
@pytest.fixture(scope="module")
def database():
    """Created once per module."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture(scope="session")
def app():
    """Created once for entire test session."""
    return create_app()
```

## Setup/Teardown with yield

```python
@pytest.fixture
def temp_file():
    # Setup
    path = Path("/tmp/test.txt")
    path.write_text("test content")

    yield path  # Test runs here

    # Teardown
    path.unlink()


@pytest.fixture
def db_transaction(db):
    """Rollback after each test."""
    transaction = db.begin()
    yield db
    transaction.rollback()
```

## Fixture Dependencies

```python
@pytest.fixture
def user():
    return User(name="Test")

@pytest.fixture
def authenticated_client(client, user):
    """Depends on client and user fixtures."""
    client.login(user)
    return client

def test_protected_route(authenticated_client):
    response = authenticated_client.get("/protected")
    assert response.status_code == 200
```

## Parametrized Fixtures

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def database(request):
    """Test runs 3 times with different DBs."""
    db_type = request.param
    db = create_database(db_type)
    yield db
    db.cleanup()

def test_query(database):
    # This test runs 3 times
    result = database.query("SELECT 1")
    assert result is not None
```

## Factory Fixtures

```python
@pytest.fixture
def make_user():
    """Factory for creating users with defaults."""
    created = []

    def _make_user(name="Test", email=None, **kwargs):
        email = email or f"{name.lower()}@test.com"
        user = User(name=name, email=email, **kwargs)
        created.append(user)
        return user

    yield _make_user

    # Cleanup
    for user in created:
        user.delete()


def test_multiple_users(make_user):
    user1 = make_user("Alice")
    user2 = make_user("Bob", role="admin")

    assert user1.name == "Alice"
    assert user2.role == "admin"
```

## Async Fixtures

```python
@pytest.fixture
async def async_client():
    async with AsyncClient() as client:
        yield client


@pytest.fixture
async def db_pool():
    pool = await create_pool()
    yield pool
    await pool.close()


async def test_async(async_client, db_pool):
    response = await async_client.get("/")
    assert response.status_code == 200
```

## conftest.py Hierarchy

```
tests/
├── conftest.py              # Available to all tests
├── unit/
│   ├── conftest.py          # Only for unit tests
│   └── test_service.py
└── integration/
    ├── conftest.py          # Only for integration tests
    └── test_api.py
```

## Built-in Fixtures

| Fixture | Description |
|---------|-------------|
| `tmp_path` | Temporary directory (Path) |
| `tmp_path_factory` | Factory for temp dirs |
| `capsys` | Capture stdout/stderr |
| `caplog` | Capture log messages |
| `monkeypatch` | Modify objects/env vars |
| `request` | Fixture request object |

```python
def test_output(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"


def test_logging(caplog):
    import logging
    logging.warning("test warning")
    assert "test warning" in caplog.text


def test_env_var(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    assert os.environ["API_KEY"] == "test-key"


def test_temp_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("content")
    assert file.read_text() == "content"
```

## Autouse Fixtures

```python
@pytest.fixture(autouse=True)
def reset_database(db):
    """Runs automatically before every test."""
    yield
    db.truncate_all()


@pytest.fixture(autouse=True, scope="session")
def setup_logging():
    """Configure logging once for all tests."""
    logging.basicConfig(level=logging.DEBUG)
```

## Request Object

```python
@pytest.fixture
def dynamic_fixture(request):
    """Access test info and params."""
    # Test name
    test_name = request.node.name

    # Markers
    if request.node.get_closest_marker("slow"):
        timeout = 60
    else:
        timeout = 10

    # Parametrize value
    if hasattr(request, "param"):
        value = request.param
    else:
        value = "default"

    return {"test": test_name, "timeout": timeout, "value": value}
```
