# Advanced Fixture Patterns

## Table of Contents

1. [Fixture Dependencies](#fixture-dependencies)
2. [Dynamic Fixtures](#dynamic-fixtures)
3. [Autouse Fixtures](#autouse-fixtures)
4. [Fixture Finalization](#fixture-finalization)
5. [Request Object](#request-object)
6. [Override Patterns](#override-patterns)

## Fixture Dependencies

Fixtures can request other fixtures, creating dependency chains:

```python
@pytest.fixture
def database():
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture
def user_repo(database):
    return UserRepository(database)

@pytest.fixture
def user_service(user_repo):
    return UserService(user_repo)

def test_user_creation(user_service):
    user = user_service.create("test@example.com")
    assert user.email == "test@example.com"
```

## Dynamic Fixtures

### Using pytest_generate_tests

Generate test parameters dynamically:

```python
# conftest.py
def pytest_generate_tests(metafunc):
    if "db_engine" in metafunc.fixturenames:
        engines = ["sqlite", "postgres"]
        if metafunc.config.getoption("--mysql"):
            engines.append("mysql")
        metafunc.parametrize("db_engine", engines)
```

### Dynamic Scope

Determine fixture scope at runtime:

```python
def determine_scope(fixture_name, config):
    if config.getoption("--expensive-setup"):
        return "session"
    return "function"

@pytest.fixture(scope=determine_scope)
def expensive_resource():
    return create_expensive_resource()
```

## Autouse Fixtures

Automatically apply fixtures without explicit request:

```python
@pytest.fixture(autouse=True)
def reset_database(database):
    """Clean database before each test."""
    database.truncate_all()
    yield
    database.truncate_all()

@pytest.fixture(autouse=True, scope="module")
def setup_logging():
    """Configure logging for test module."""
    logging.basicConfig(level=logging.DEBUG)
```

### Class-Scoped Autouse

```python
class TestUserFeatures:
    @pytest.fixture(autouse=True)
    def setup_user(self, database):
        self.user = database.create_user("test@example.com")
        yield
        database.delete_user(self.user.id)

    def test_user_name(self):
        assert self.user.email == "test@example.com"
```

## Fixture Finalization

### Multiple Finalizers

```python
@pytest.fixture
def resource_with_cleanup(request):
    resources = []

    def create_resource(name):
        r = Resource(name)
        resources.append(r)
        request.addfinalizer(lambda: r.cleanup())
        return r

    yield create_resource
    # All finalizers run in reverse order
```

### Safe Teardown Pattern

```python
@pytest.fixture
def database():
    db = None
    try:
        db = Database()
        db.connect()
        yield db
    finally:
        if db is not None:
            db.disconnect()
```

## Request Object

Access test context from fixtures:

```python
@pytest.fixture
def resource(request):
    # Access test function name
    test_name = request.node.name

    # Access module-level attribute
    config = getattr(request.module, "RESOURCE_CONFIG", {})

    # Access markers
    marker = request.node.get_closest_marker("resource_type")
    resource_type = marker.args[0] if marker else "default"

    return create_resource(test_name, resource_type, config)
```

### Indirect Parametrization

```python
@pytest.fixture
def user(request):
    return User(role=request.param)

@pytest.mark.parametrize("user", ["admin", "member"], indirect=True)
def test_permissions(user):
    if user.role == "admin":
        assert user.can_delete()
```

## Override Patterns

### Conftest Hierarchy

```
tests/
├── conftest.py              # Base fixture
├── unit/
│   ├── conftest.py          # Override for unit tests
│   └── test_service.py
└── integration/
    ├── conftest.py          # Override for integration tests
    └── test_api.py
```

```python
# tests/conftest.py
@pytest.fixture
def database():
    return MockDatabase()

# tests/integration/conftest.py
@pytest.fixture
def database():
    return RealDatabase()  # Overrides parent
```

### Module-Level Override

```python
# test_specific.py
import pytest

@pytest.fixture
def database():
    """Override conftest fixture for this module."""
    return SpecialDatabase()

def test_with_special_db(database):
    assert isinstance(database, SpecialDatabase)
```

### Parametrized Override

```python
# conftest.py
@pytest.fixture(params=["small", "medium", "large"])
def dataset(request):
    return load_dataset(request.param)

# test_specific.py
@pytest.fixture
def dataset():
    """Use only large dataset for this module."""
    return load_dataset("large")
```

## Fixture Caching

Fixtures are cached per scope:

```python
@pytest.fixture(scope="session")
def expensive_data():
    # Computed once per test session
    return compute_expensive_data()

@pytest.fixture(scope="module")
def module_data(expensive_data):
    # New instance per module, reuses expensive_data
    return process_data(expensive_data)
```

## Async Fixtures (pytest-asyncio)

```python
import pytest_asyncio

@pytest_asyncio.fixture
async def async_client():
    client = AsyncClient()
    await client.connect()
    yield client
    await client.disconnect()

@pytest.mark.asyncio
async def test_async_operation(async_client):
    result = await async_client.fetch()
    assert result is not None
```
