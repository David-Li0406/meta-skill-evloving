---
name: smoketest-writing
description: Write isolated integration/smoke tests for FastAPI backends using ephemeral Docker PostgreSQL, TestClient, and dependency injection. Tests run against temporary database (not dev DB), gated by RUN_INTEGRATION_TESTS env var. Covers test-db.sh scripts, conftest.py fixtures, test runner scripts, and proper teardown. Use when adding integration tests to FastAPI projects or converting real-server tests to isolated TestClient tests.
---

# Smoketest / Integration Test Writing Guide

Write isolated integration tests for FastAPI backends that use an ephemeral Docker PostgreSQL database instead of your development database.

## Testing Terminology

| Type | What it tests | How to run | Skill |
|------|---------------|------------|-------|
| **Unit test** | Individual functions/classes in isolation | `pytest` | `python-unit-testing` |
| **CLI test** | Command-line interface via CliRunner | `pytest` | `python-cli-testing` |
| **Smoketest** | Full system with real services (AKA e2e, integration) | `RUN_INTEGRATION_TESTS=true pytest` | This skill |

## Core Principles

1. **True isolation** - Tests use a temporary Docker PostgreSQL container, not dev database
2. **Ephemeral data** - Database is created fresh, destroyed after tests
3. **TestClient not HTTP** - Use FastAPI's TestClient, not requests to real server
4. **Dependency injection** - Override `get_session`/`get_dbagent` to use test database
5. **Environment gating** - Skip tests unless `RUN_INTEGRATION_TESTS=true`
6. **Vanilla Docker** - Use plain `docker run` commands, NOT docker-compose

## Directory Structure

```
project-root/
├── backend/
│   └── tests/
│       ├── conftest.py              # Unit test fixtures (SQLite)
│       ├── test_*.py                # Unit tests
│       └── integration/
│           ├── conftest.py          # Integration fixtures (TestClient + test DB)
│           ├── scripts/
│           │   └── test-db.sh       # Docker PostgreSQL management
│           └── test_smoketest.py    # Integration tests
└── scripts/
    └── test-integration.sh          # One-command test runner
```

## Step 1: Create test-db.sh Script

Use plain `docker run` commands - no docker-compose. This keeps things simple with a single shell script that can start/stop the test database.

Create `backend/tests/integration/scripts/test-db.sh`:

```bash
#!/bin/bash
# Test Database Management Script
# Manages Docker PostgreSQL container for integration tests

CONTAINER_NAME="<app>-postgres-test"
DB_PORT="5433"  # Different from dev port 5432!
DB_USER="testuser"
DB_PASS="testpass"
DB_NAME="<app>_test"

case "$1" in
    start)
        echo "Starting test PostgreSQL database..."

        # Remove existing container if it exists
        docker rm -f "$CONTAINER_NAME" 2>/dev/null

        # Start PostgreSQL container with tmpfs for speed
        docker run -d \
            --name "$CONTAINER_NAME" \
            -e POSTGRES_USER="$DB_USER" \
            -e POSTGRES_PASSWORD="$DB_PASS" \
            -e POSTGRES_DB="$DB_NAME" \
            -p "${DB_PORT}:5432" \
            --tmpfs /var/lib/postgresql/data \
            postgres:17

        echo "Waiting for database to be ready..."

        # Wait for healthy status (up to 30 seconds)
        for i in {1..30}; do
            if docker exec "$CONTAINER_NAME" pg_isready -U "$DB_USER" -d "$DB_NAME" 2>/dev/null; then
                echo "Test database is ready!"
                exit 0
            fi
            sleep 1
        done

        echo "Failed to start test database"
        docker logs "$CONTAINER_NAME"
        exit 1
        ;;
    stop)
        echo "Stopping test PostgreSQL database..."
        docker rm -f "$CONTAINER_NAME" 2>/dev/null
        echo "Test database stopped and removed"
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    status)
        docker ps -f "name=$CONTAINER_NAME"
        ;;
    logs)
        docker logs -f "$CONTAINER_NAME"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
```

**Key points:**
- Use port `5433` to avoid conflict with dev database on `5432`
- Use `--tmpfs` for PostgreSQL data directory (fast, ephemeral)
- Wait for `pg_isready` before proceeding
- Replace `<app>` with your application name

Make executable:
```bash
chmod +x backend/tests/integration/scripts/test-db.sh
```

## Step 2: Create conftest.py

Create `backend/tests/integration/conftest.py`:

```python
"""
Integration test fixtures for <App> API.

Uses FastAPI TestClient to make HTTP requests to API endpoints.
Prerequisites:
1. Start test database: ./backend/tests/integration/scripts/test-db.sh start
2. Run tests: RUN_INTEGRATION_TESTS=true pytest backend/tests/integration/
"""
import sys
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Skip all integration tests unless explicitly enabled
pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "true",
    reason="Integration tests disabled. Set RUN_INTEGRATION_TESTS=true to run."
)

# Test database configuration - must match test-db.sh
TEST_DB_URL = "postgresql://testuser:testpass@localhost:5433/<app>_test"


@pytest.fixture(scope="session")
def test_engine():
    """Create engine connected to test PostgreSQL"""
    from sqlmodel import create_engine, SQLModel

    engine = create_engine(TEST_DB_URL)
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def client(test_engine):
    """Create TestClient with test database"""
    from backend.main import app
    from backend.database import get_session  # or get_dbagent
    from sqlmodel import Session

    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
```

### Variant: Using DBAgent Pattern

If your app uses a database agent pattern instead of direct sessions:

```python
@pytest.fixture(scope="session")
def test_dbagent():
    """Create DBAgent connected to test PostgreSQL"""
    from backend.database.database import DBAgent

    dbagent = DBAgent(postgres_str=TEST_DB_URL)
    yield dbagent
    if hasattr(dbagent, 'engine'):
        dbagent.engine.dispose()


@pytest.fixture(scope="session")
def client(test_dbagent):
    """Create TestClient with test database"""
    from backend.main import app
    from backend.database.database import get_dbagent

    def override_get_dbagent():
        return test_dbagent

    app.dependency_overrides[get_dbagent] = override_get_dbagent

    with TestClient(app) as c:
        c.app.state.dbagent = test_dbagent
        yield c

    app.dependency_overrides.clear()
```

## Step 3: Write Test Files

Create `backend/tests/integration/test_smoketest.py`:

```python
"""
<App> API Smoketests

Integration tests using TestClient to make HTTP requests to API endpoints.
Tests API contracts, authentication requirements, and endpoint availability.

Prerequisites:
1. Start test database: ./backend/tests/integration/scripts/test-db.sh start
2. Run tests: RUN_INTEGRATION_TESTS=true pytest backend/tests/integration/
"""
import os
import pytest

# Skip all tests in this module unless RUN_INTEGRATION_TESTS=true
pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "true",
    reason="Integration tests disabled. Set RUN_INTEGRATION_TESTS=true to run."
)


class TestServerAvailability:
    """Verify the API is responding"""

    def test_health_check(self, client):
        """Health endpoint should return healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_root_endpoint(self, client):
        """Root endpoint should respond"""
        response = client.get("/")
        assert response.status_code == 200


class TestAuthenticationRequired:
    """Test that protected endpoints require authentication"""

    def test_protected_endpoint_requires_auth(self, client):
        """GET /api/v1/protected/ without auth should return 401"""
        response = client.get("/api/v1/protected/")
        assert response.status_code == 401
```

### Test Patterns

**Testing unauthenticated access:**
```python
def test_requires_auth(self, client):
    response = client.get("/api/v1/users/")
    assert response.status_code == 401
```

**Testing authenticated access (create JWT fixtures):**
```python
@pytest.fixture(scope="session")
def admin_headers() -> dict:
    """Authorization headers for admin user"""
    from backend.auth.tokens import create_access_token
    token = create_access_token(data={"sub": "1", "roles": ["admin"]})
    return {"Authorization": f"Bearer {token}"}

def test_admin_can_list_users(self, client, admin_headers):
    response = client.get("/api/v1/users/", headers=admin_headers)
    assert response.status_code == 200
```

**Testing CRUD operations:**
```python
def test_create_and_retrieve_item(self, client, admin_headers):
    # Create
    response = client.post(
        "/api/v1/items/",
        json={"name": "Test Item"},
        headers=admin_headers
    )
    assert response.status_code == 201
    item_id = response.json()["id"]

    # Retrieve
    response = client.get(f"/api/v1/items/{item_id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"
```

## Step 4: Create Test Runner Script

Create `scripts/test-integration.sh`:

```bash
#!/bin/bash
# Run integration tests with ephemeral test database

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

echo "=== Integration Tests ==="

# Start test database
echo "Starting test database..."
$PROJECT_ROOT/backend/tests/integration/scripts/test-db.sh start

# Run integration tests
echo "Running integration tests..."
cd $PROJECT_ROOT/backend
source ../.venv/bin/activate
RUN_INTEGRATION_TESTS=true pytest tests/integration/ -v
TEST_EXIT_CODE=$?

# Stop test database
echo "Stopping test database..."
$PROJECT_ROOT/backend/tests/integration/scripts/test-db.sh stop

echo "=== Integration tests complete ==="
exit $TEST_EXIT_CODE
```

Make executable:
```bash
chmod +x scripts/test-integration.sh
```

## Running Tests

### Full test run (recommended):
```bash
./scripts/test-integration.sh
```

### Manual approach:
```bash
# Terminal 1: Start test database
./backend/tests/integration/scripts/test-db.sh start

# Terminal 2: Run tests
cd backend
source ../.venv/bin/activate
RUN_INTEGRATION_TESTS=true pytest tests/integration/ -v

# After tests: Stop database
./backend/tests/integration/scripts/test-db.sh stop
```

### Run without test database (tests will skip):
```bash
pytest backend/tests/integration/  # All tests skip
```

## Best Practices

### 1. Keep Test Database Separate
- Use port `5433` (not `5432`)
- Use different container name (`<app>-postgres-test`)
- Use `--tmpfs` for speed

### 2. Session-Scoped Fixtures
- Use `scope="session"` for database engine and client
- Avoids recreating database for each test
- Tests share the same database state (plan accordingly)

### 3. Environment Gating
- Always gate with `RUN_INTEGRATION_TESTS`
- Prevents accidental runs during regular `pytest`
- Makes CI configuration explicit

### 4. Test Independence
- Don't rely on test execution order
- Clean up data you create, or accept session-shared state
- For strict isolation, use `scope="function"` fixtures (slower)

### 5. No External Dependencies
- Tests should not require running backend server
- Tests should not require network access beyond Docker
- Tests should not modify development database

## Migrating from Real Server Tests

If you have tests using `requests` to hit a real server:

**Before:**
```python
import requests

def test_health(api_base_url, api_client):
    response = api_client.get(f"{api_base_url}/health")
    assert response.status_code == 200
```

**After:**
```python
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
```

**Changes:**
- Remove `requests.Session` fixtures
- Remove `api_base_url` parameter
- Use `client` fixture (TestClient)
- Use relative URLs (no base URL needed)

## Checklist for New Integration Tests

- [ ] `test-db.sh` created and executable
- [ ] `conftest.py` with environment gating and TestClient fixture
- [ ] Test database URL matches `test-db.sh` credentials
- [ ] Dependency override for `get_session` or `get_dbagent`
- [ ] `test-integration.sh` created and executable
- [ ] Tests use relative URLs with `client.get("/path")`
- [ ] Tests have `pytestmark` skip condition
