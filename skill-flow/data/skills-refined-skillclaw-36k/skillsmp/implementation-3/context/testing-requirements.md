# Testing Requirements

## Testing Philosophy

**Tests are proof your code works.**

Without tests:
- You hope code works
- Refactoring is scary
- Regressions are common
- "It worked yesterday" is your debugging tool

With tests:
- You know code works
- Refactoring is safe
- Regressions are caught immediately
- Tests document intended behavior

## Coverage Requirements

### Minimum Coverage Targets

| Code Type | Coverage Target | Rationale |
|-----------|----------------|-----------|
| Service Layer | 90% | Core business logic, must be proven |
| API Endpoints | 85% | Integration points, critical paths |
| Repositories | 85% | Data access, error cases important |
| Utilities | 95% | Reused everywhere, must be bulletproof |
| Components (Frontend) | 80% | UI logic, user interactions |
| Overall Project | 80% | Acceptable baseline |

**Coverage is necessary, not sufficient.** 100% coverage with bad tests proves nothing.

## Test Types

### Unit Tests

**Purpose:** Prove individual functions/methods work in isolation

**Characteristics:**
- Fast (< 10ms per test)
- Isolated (no database, no network, no filesystem)
- Deterministic (same result every time)

**Coverage:** Happy path + edge cases + error cases

**Example:**

```python
# File: tests/unit/services/test_user_service.py

def test_create_user_success(db_session):
    """Test successful user creation."""
    service = UserService(db_session)
    request = CreateUserRequest(
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )

    user = await service.create_user(request)

    assert user.email == "john@example.com"
    assert user.id is not None

def test_create_user_duplicate_email_raises_error(db_session):
    """Test error on duplicate email."""
    service = UserService(db_session)
    request = CreateUserRequest(
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )

    await service.create_user(request)

    with pytest.raises(DuplicateEntityError):
        await service.create_user(request)

def test_create_user_empty_email_raises_error(db_session):
    """Test validation of required fields."""
    service = UserService(db_session)
    request = CreateUserRequest(
        email="",
        first_name="John",
        last_name="Doe"
    )

    with pytest.raises(ValidationError):
        await service.create_user(request)
```

### Integration Tests

**Purpose:** Prove components work together

**Characteristics:**
- Medium speed (< 1s per test)
- Real dependencies (test database, real services)
- End-to-end workflows

**Coverage:** Critical user workflows

**Example:**

```python
# File: tests/integration/test_user_api.py

def test_user_creation_flow(client: TestClient):
    """Test complete user creation through API."""
    # Create user
    response = client.post("/api/v1/users", json={
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    })

    assert response.status_code == 201
    user_data = response.json()
    user_id = user_data["id"]

    # Retrieve user
    response = client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["email"] == "john@example.com"

    # Update user
    response = client.patch(f"/api/v1/users/{user_id}", json={
        "first_name": "Jane"
    })

    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"

    # Delete user
    response = client.delete(f"/api/v1/users/{user_id}")

    assert response.status_code == 204
```

### Contract Tests

**Purpose:** Verify DTOs match specification

**Characteristics:**
- Very fast (< 5ms per test)
- Structure validation only (not behavior)
- Critical for frontend/backend sync

**Coverage:** All DTOs

**Example:**

```python
# File: tests/contract/test_user_contracts.py

def test_create_user_request_structure():
    """Verify CreateUserRequest matches spec."""
    expected_fields = {'email', 'first_name', 'last_name'}
    actual_fields = set(CreateUserRequest.__fields__.keys())

    assert actual_fields == expected_fields

def test_user_response_structure():
    """Verify UserResponse matches spec."""
    expected_fields = {'id', 'email', 'first_name', 'last_name', 'created_at'}
    actual_fields = set(UserResponse.__fields__.keys())

    assert actual_fields == expected_fields
```

### E2E Tests

**Purpose:** Verify complete user workflows in real browser

**Characteristics:**
- Slow (5-30s per test)
- Real browser + real backend
- High-value scenarios only

**Coverage:** 5-10 critical paths

**Example:**

```typescript
// File: frontend/cypress/e2e/user-management.cy.ts

describe('User Management', () => {
  beforeEach(() => {
    cy.task('db:reset');
    cy.login('admin@example.com', 'password');
  });

  it('creates and displays new user', () => {
    cy.visit('/users');
    cy.get('[data-test="create-user-btn"]').click();

    cy.get('input#email').type('newuser@example.com');
    cy.get('input#first_name').type('New');
    cy.get('input#last_name').type('User');
    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/users');
    cy.contains('newuser@example.com').should('be.visible');
  });
});
```

## Test Quality Standards

### Good Tests

**Characteristics:**
- **Descriptive names** - Test name explains what's being tested
- **Arrange-Act-Assert** - Clear structure
- **One concept** - Tests one thing
- **Fast** - Runs in milliseconds
- **Independent** - Can run in any order
- **Repeatable** - Same result every time

**Example:**

```python
def test_user_creation_sets_active_status_by_default():
    """
    Test that newly created users have 'active' status.

    Business rule: Users start active unless explicitly set otherwise.
    """
    # Arrange
    service = UserService(db)
    request = CreateUserRequest(
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )

    # Act
    user = await service.create_user(request)

    # Assert
    assert user.status == UserStatus.ACTIVE
```

### Bad Tests

**Anti-patterns:**

```python
# ❌ Bad - vague name
def test_user():
    ...

# ❌ Bad - tests multiple things
def test_user_creation_and_update_and_delete():
    ...

# ❌ Bad - no assertion
def test_create_user():
    service.create_user(request)
    # No assertion!

# ❌ Bad - fragile (depends on order)
def test_get_user():
    user = service.get_user_by_id("123")  # Assumes user exists
    assert user.email == "test@example.com"

# ❌ Bad - tests mock behavior, not real code
def test_create_user():
    mock_repo = MagicMock()
    mock_repo.save.return_value = User(...)
    service = UserService(mock_repo)

    service.create_user(request)

    mock_repo.save.assert_called_once()  # Testing mock!
```

## Test Organization

### Directory Structure

```
Backend (Python):
tests/
├── unit/              # Fast, isolated tests
│   ├── services/
│   ├── repositories/
│   └── utils/
├── integration/       # Tests with database
│   ├── test_user_api.py
│   └── test_auth_flow.py
├── contract/          # DTO structure validation
│   └── test_user_contracts.py
└── conftest.py        # Shared fixtures

Frontend (TypeScript):
frontend/
├── src/
│   └── components/
│       └── users/
│           └── __tests__/
│               └── CreateUserForm.test.ts
└── cypress/
    └── e2e/
        └── user-management.cy.ts
```

### Test Naming

**Pattern:** `test_<what>_<when>_<expected>`

```python
# Good names
test_create_user_with_valid_data_returns_user()
test_create_user_with_duplicate_email_raises_error()
test_get_user_when_not_found_raises_error()

# Bad names
test_create_user()
test_user_1()
test_bug_fix()
```

## Test Fixtures

### Backend Fixtures

```python
# File: tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

@pytest.fixture(scope="function")
def db_session():
    """Create test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def client(db_session):
    """Create test API client."""
    from fastapi.testclient import TestClient
    from app.main import app
    from app.api.dependencies import get_db

    app.dependency_overrides[get_db] = lambda: db_session

    yield TestClient(app)

    app.dependency_overrides.clear()
```

### Frontend Fixtures

```typescript
// File: frontend/src/test/setup.ts
import { beforeEach } from 'vitest';
import { config } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';

beforeEach(() => {
  // Reset Pinia state
  setActivePinia(createPinia());
});

// Global test utilities
export function createMockUser(): UserResponse {
  return {
    id: '550e8400-e29b-41d4-a716-446655440000',
    email: 'test@example.com',
    first_name: 'Test',
    last_name: 'User',
    created_at: '2024-01-15T10:30:00Z',
  };
}
```

## Running Tests

### Development Workflow

```bash
# Run tests on file save (watch mode)
uv run pytest --watch
npm run test -- --watch

# Run specific test
uv run pytest tests/unit/services/test_user_service.py::test_create_user_success
npm run test -- CreateUserForm.test.ts

# Run with coverage
uv run pytest --cov=app --cov-report=html
npm run test:coverage
```

### CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
- name: Unit Tests
  run: uv run pytest tests/unit/ -v

- name: Integration Tests
  run: uv run pytest tests/integration/ -v

- name: E2E Tests
  run: npm run test:e2e:headless

- name: Coverage Check
  run: |
    uv run pytest --cov=app --cov-fail-under=80
    npm run test:coverage -- --coverage.threshold.lines=80
```

## Test-Driven Development

**Prefer TDD when possible:**

See: `~/.claude/skills/test-driven-development/SKILL.md`

```
1. Write test first (RED)
2. Watch it fail
3. Write minimal code (GREEN)
4. Watch it pass
5. Refactor
6. Repeat
```

**Benefits:**
- Tests prove what's required (not what's implemented)
- Watching test fail proves test works
- Implementation is focused (only what's needed)

## Performance Targets

| Test Type | Target Speed | Max Acceptable |
|-----------|--------------|----------------|
| Unit test | < 10ms | 100ms |
| Integration test | < 1s | 5s |
| E2E test | < 10s | 30s |
| Full test suite | < 2min | 10min |

**If tests are slow:**
- Use in-memory database (SQLite)
- Parallelize tests
- Optimize fixtures
- Reduce E2E test count

## Testing Checklist

Before marking work complete:

- [ ] Unit tests cover happy path
- [ ] Unit tests cover error cases
- [ ] Unit tests cover edge cases
- [ ] Integration tests verify workflows
- [ ] Contract tests validate DTOs
- [ ] E2E tests cover critical paths
- [ ] All tests passing
- [ ] Coverage >= 80%
- [ ] Tests run fast (< 10s for unit)
- [ ] No skipped/disabled tests
- [ ] No flaky tests

## Common Testing Mistakes

| Mistake | Fix |
|---------|-----|
| Testing implementation details | Test behavior, not internals |
| Mocking everything | Use real code, mock only boundaries |
| Tests depend on order | Make tests independent |
| No assertions | Every test must assert something |
| Vague test names | Name describes what's tested |
| One giant test | Split into focused tests |
| Skipping error cases | Test errors as thoroughly as success |

---

**Remember:** Tests are an investment. Write them comprehensively, run them frequently, trust them completely. Good tests enable fearless refactoring and prevent regressions.
