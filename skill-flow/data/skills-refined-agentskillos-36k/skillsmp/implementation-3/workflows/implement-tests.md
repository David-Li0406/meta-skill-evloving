# Test Implementation Workflow

## Purpose

This workflow guides systematic creation of tests for backend and frontend code. It complements the `test-driven-development` skill and references `testing-anti-patterns`.

Use this workflow when:
- Writing unit tests for services/components
- Creating integration tests for APIs
- Implementing contract tests for DTOs
- Building E2E tests for user workflows

## Test Philosophy

**Tests are proof, not afterthought.**

Good tests:
- Prove code works as specified
- Enable confident refactoring
- Document intended behavior
- Catch regressions immediately

Bad tests:
- Test mock behavior instead of real code
- Are flaky (pass/fail randomly)
- Are slow (run for minutes)
- Duplicate implementation logic

## Test-Driven Development Integration

**Prefer TDD when possible:**

```
1. Write test first (RED)
2. Watch it fail
3. Write minimal code (GREEN)
4. Watch it pass
5. Refactor
6. Repeat
```

See: `~/.claude/skills/test-driven-development/SKILL.md`

**If not using TDD:** Still write comprehensive tests immediately after implementation, before moving to next feature.

## Phase 0: Start Task Tracking

Before beginning test implementation, start task tracking:

```bash
# Start the task to update status and track progress
shark task start <task-id>

# Example:
shark task start T-E04-F06-001
```

This:
- Updates task status to "in-progress" in the database
- Tracks when implementation began
- Provides visibility to the team
- Enables accurate progress reporting

## Test Types

### Unit Tests
- Test single function/method in isolation
- Fast (milliseconds)
- No database, no network, no filesystem
- Mock only unavoidable dependencies

### Integration Tests
- Test multiple components working together
- Medium speed (seconds)
- Real database (test instance), real services
- Minimal mocking

### Contract Tests
- Test DTO structure matches specification
- Very fast (milliseconds)
- No logic, just structure validation
- Critical for frontend/backend synchronization

### E2E Tests
- Test complete user workflows
- Slow (seconds to minutes)
- Real browser, real backend
- Minimal, high-value scenarios only

## Phase 1: Unit Test Implementation

### Step 1.1: Identify What to Test

For a service/component, test:

1. **Happy path** - Feature works as expected
2. **Edge cases** - Boundary conditions (empty, max, min)
3. **Error cases** - Invalid input, failures
4. **Business rules** - Domain constraints

**Don't test:**
- Framework internals (Vue reactivity, React hooks)
- Third-party libraries
- Generated code
- Trivial getters/setters

### Step 1.2: Write Unit Tests (Backend Example)

```python
# File: tests/unit/services/test_user_service.py
import pytest
from uuid import uuid4
from app.services.user_service import UserService
from app.schemas.user_schema import CreateUserRequest
from app.services.exceptions import DuplicateEntityError, EntityNotFoundError

class TestUserService:
    """Unit tests for UserService."""

    @pytest.fixture
    def service(self, db_session):
        """Create UserService instance for tests."""
        return UserService(db_session)

    def test_create_user_success(self, service):
        """Test successful user creation."""
        # Arrange
        request = CreateUserRequest(
            email="john@example.com",
            first_name="John",
            last_name="Doe"
        )

        # Act
        user = await service.create_user(request)

        # Assert
        assert user.email == "john@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.id is not None
        assert user.created_at is not None

    def test_create_user_duplicate_email(self, service):
        """Test error when creating user with duplicate email."""
        # Arrange
        request = CreateUserRequest(
            email="john@example.com",
            first_name="John",
            last_name="Doe"
        )
        await service.create_user(request)

        # Act & Assert
        with pytest.raises(DuplicateEntityError) as exc_info:
            await service.create_user(request)

        assert "john@example.com" in str(exc_info.value)

    def test_get_user_by_id_success(self, service):
        """Test retrieving user by ID."""
        # Arrange
        created = await service.create_user(CreateUserRequest(
            email="john@example.com",
            first_name="John",
            last_name="Doe"
        ))

        # Act
        user = await service.get_user_by_id(str(created.id))

        # Assert
        assert user.id == created.id
        assert user.email == created.email

    def test_get_user_by_id_not_found(self, service):
        """Test error when user not found."""
        # Arrange
        non_existent_id = str(uuid4())

        # Act & Assert
        with pytest.raises(EntityNotFoundError) as exc_info:
            await service.get_user_by_id(non_existent_id)

        assert non_existent_id in str(exc_info.value)

    def test_update_user_success(self, service):
        """Test successful user update."""
        # Arrange
        user = await service.create_user(CreateUserRequest(
            email="john@example.com",
            first_name="John",
            last_name="Doe"
        ))

        update_request = UpdateUserRequest(
            first_name="Jane"
        )

        # Act
        updated = await service.update_user(str(user.id), update_request)

        # Assert
        assert updated.first_name == "Jane"
        assert updated.last_name == "Doe"  # Unchanged
        assert updated.updated_at > user.updated_at
```

### Step 1.3: Write Unit Tests (Frontend Example)

```typescript
// File: frontend/src/components/users/__tests__/CreateUserForm.test.ts
import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import CreateUserForm from '../CreateUserForm.vue';
import type { CreateUserRequest } from '@/types/api/users';

describe('CreateUserForm', () => {
  it('renders all form fields', () => {
    const wrapper = mount(CreateUserForm);

    expect(wrapper.find('input#email').exists()).toBe(true);
    expect(wrapper.find('input#first_name').exists()).toBe(true);
    expect(wrapper.find('input#last_name').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true);
  });

  it('validates required fields on submit', async () => {
    const wrapper = mount(CreateUserForm);

    // Act - submit empty form
    await wrapper.find('form').trigger('submit');

    // Assert - shows validation errors
    expect(wrapper.text()).toContain('Email is required');
    expect(wrapper.text()).toContain('First name is required');
    expect(wrapper.text()).toContain('Last name is required');

    // Assert - does not emit submit event
    expect(wrapper.emitted('submit')).toBeFalsy();
  });

  it('emits submit with correct data when valid', async () => {
    const wrapper = mount(CreateUserForm);

    // Arrange - fill form
    await wrapper.find('input#email').setValue('john@example.com');
    await wrapper.find('input#first_name').setValue('John');
    await wrapper.find('input#last_name').setValue('Doe');

    // Act - submit
    await wrapper.find('form').trigger('submit');

    // Assert - emits correct data
    expect(wrapper.emitted('submit')).toBeTruthy();
    const emittedData = wrapper.emitted('submit')![0][0] as CreateUserRequest;
    expect(emittedData).toEqual({
      email: 'john@example.com',
      first_name: 'John',  // Verify snake_case preserved
      last_name: 'Doe',
    });
  });

  it('displays initial data when provided', () => {
    const initialData: Partial<CreateUserRequest> = {
      email: 'existing@example.com',
      first_name: 'Existing',
    };

    const wrapper = mount(CreateUserForm, {
      props: { initialData },
    });

    expect(wrapper.find('input#email').element.value).toBe('existing@example.com');
    expect(wrapper.find('input#first_name').element.value).toBe('Existing');
  });

  it('clears errors when user starts typing', async () => {
    const wrapper = mount(CreateUserForm);

    // Trigger validation errors
    await wrapper.find('form').trigger('submit');
    expect(wrapper.text()).toContain('Email is required');

    // Start typing
    await wrapper.find('input#email').setValue('john@example.com');

    // Error should clear
    expect(wrapper.text()).not.toContain('Email is required');
  });
});
```

## Phase 2: Integration Test Implementation

### Step 2.1: Backend Integration Tests

Test API endpoints with real database:

```python
# File: tests/integration/test_user_api.py
import pytest
from fastapi.testclient import TestClient

class TestUserAPI:
    """Integration tests for User API endpoints."""

    def test_create_user_endpoint(self, client: TestClient):
        """Test POST /api/v1/users creates user."""
        # Act
        response = client.post(
            "/api/v1/users",
            json={
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe"
            }
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "john@example.com"
        assert data["first_name"] == "John"
        assert "id" in data
        assert "created_at" in data

    def test_create_user_duplicate_email_returns_409(self, client: TestClient):
        """Test duplicate email returns 409 Conflict."""
        # Arrange - create first user
        client.post(
            "/api/v1/users",
            json={
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe"
            }
        )

        # Act - attempt duplicate
        response = client.post(
            "/api/v1/users",
            json={
                "email": "john@example.com",
                "first_name": "Jane",
                "last_name": "Smith"
            }
        )

        # Assert
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_get_user_by_id_endpoint(self, client: TestClient):
        """Test GET /api/v1/users/{id} retrieves user."""
        # Arrange - create user
        create_response = client.post(
            "/api/v1/users",
            json={
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe"
            }
        )
        user_id = create_response.json()["id"]

        # Act
        response = client.get(f"/api/v1/users/{user_id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == "john@example.com"

    def test_get_nonexistent_user_returns_404(self, client: TestClient):
        """Test GET with invalid ID returns 404."""
        # Act
        response = client.get("/api/v1/users/nonexistent-id")

        # Assert
        assert response.status_code == 404
```

### Step 2.2: Frontend Integration Tests (E2E)

```typescript
// File: frontend/cypress/e2e/user-creation.cy.ts
describe('User Creation Flow', () => {
  beforeEach(() => {
    // Reset database state
    cy.task('db:reset');
    cy.visit('/users/create');
  });

  it('creates user successfully', () => {
    // Arrange & Act
    cy.get('input#email').type('john@example.com');
    cy.get('input#first_name').type('John');
    cy.get('input#last_name').type('Doe');
    cy.get('button[type="submit"]').click();

    // Assert - redirected to user list
    cy.url().should('include', '/users');

    // Assert - success message shown
    cy.contains('User created successfully');

    // Assert - user appears in list
    cy.contains('john@example.com');
  });

  it('shows validation errors for empty fields', () => {
    // Act - submit empty form
    cy.get('button[type="submit"]').click();

    // Assert - shows errors
    cy.contains('Email is required');
    cy.contains('First name is required');
    cy.contains('Last name is required');

    // Assert - stays on same page
    cy.url().should('include', '/users/create');
  });

  it('handles duplicate email error', () => {
    // Arrange - create first user
    cy.task('db:createUser', {
      email: 'john@example.com',
      first_name: 'Existing',
      last_name: 'User',
    });

    // Act - attempt duplicate
    cy.get('input#email').type('john@example.com');
    cy.get('input#first_name').type('John');
    cy.get('input#last_name').type('Doe');
    cy.get('button[type="submit"]').click();

    // Assert - shows error
    cy.contains('already exists');
  });
});
```

## Phase 3: Contract Test Implementation

### Step 3.1: Backend Contract Tests

```python
# File: tests/contract/test_user_contracts.py
import pytest
from app.schemas.user_schema import CreateUserRequest, UserResponse

class TestUserContracts:
    """Contract tests verify DTO structure matches specification."""

    def test_create_user_request_has_required_fields(self):
        """Verify CreateUserRequest has all required fields from spec."""
        # Spec: /docs/plan/.../04-api-specification.md#CreateUserRequest
        expected_fields = {'email', 'first_name', 'last_name'}
        actual_fields = set(CreateUserRequest.__fields__.keys())

        assert actual_fields == expected_fields, \
            f"DTO fields diverged. Expected: {expected_fields}, Got: {actual_fields}"

    def test_user_response_has_required_fields(self):
        """Verify UserResponse has all required fields from spec."""
        expected_fields = {'id', 'email', 'first_name', 'last_name', 'created_at'}
        actual_fields = set(UserResponse.__fields__.keys())

        assert actual_fields == expected_fields

    def test_create_user_request_field_types(self):
        """Verify field types match specification."""
        from pydantic import EmailStr

        assert CreateUserRequest.__fields__['email'].type_ == EmailStr
        assert CreateUserRequest.__fields__['first_name'].type_ == str
        assert CreateUserRequest.__fields__['last_name'].type_ == str

    def test_user_response_serialization_format(self):
        """Verify response serialization matches frontend expectations."""
        from uuid import uuid4
        from datetime import datetime

        user = UserResponse(
            id=uuid4(),
            email="test@example.com",
            first_name="Test",
            last_name="User",
            created_at=datetime.utcnow()
        )

        # Serialize to dict (what frontend receives)
        serialized = user.dict()

        # Verify id is UUID string
        assert isinstance(serialized['id'], str)

        # Verify created_at is ISO 8601 string (after JSON encoding)
        json_data = user.json()
        assert '"created_at"' in json_data
        assert 'T' in json_data  # ISO 8601 format includes 'T'
```

### Step 3.2: Frontend Contract Tests

```typescript
// File: frontend/src/types/api/__tests__/users.contract.test.ts
import { describe, it, expect } from 'vitest';
import type { CreateUserRequest, UserResponse } from '../users';

describe('User API Contracts', () => {
  it('CreateUserRequest matches backend DTO structure', () => {
    // This test verifies TypeScript interface at compile time
    const request: CreateUserRequest = {
      email: 'test@example.com',
      first_name: 'Test',  // snake_case matches backend
      last_name: 'User',
    };

    // Runtime verification
    expect(Object.keys(request).sort()).toEqual(['email', 'first_name', 'last_name'].sort());
  });

  it('UserResponse matches backend DTO structure', () => {
    const response: UserResponse = {
      id: '550e8400-e29b-41d4-a716-446655440000',
      email: 'test@example.com',
      first_name: 'Test',
      last_name: 'User',
      created_at: '2024-01-15T10:30:00Z',
    };

    expect(Object.keys(response).sort()).toEqual(
      ['id', 'email', 'first_name', 'last_name', 'created_at'].sort()
    );

    // Verify ISO 8601 datetime format
    expect(response.created_at).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
  });
});
```

## Phase 4: Test Organization

### Directory Structure

```
Backend (Python):
tests/
├── unit/                    # Fast, isolated tests
│   ├── services/
│   │   └── test_user_service.py
│   └── utils/
│       └── test_helpers.py
├── integration/             # Tests with database/network
│   ├── test_user_api.py
│   └── test_auth_flow.py
├── contract/                # DTO structure validation
│   └── test_user_contracts.py
└── conftest.py              # Shared fixtures

Frontend (TypeScript):
frontend/
├── src/
│   ├── components/
│   │   └── users/
│   │       └── __tests__/
│   │           └── CreateUserForm.test.ts
│   └── types/
│       └── api/
│           └── __tests__/
│               └── users.contract.test.ts
└── cypress/
    └── e2e/
        └── user-creation.cy.ts
```

### Test Fixtures

**Backend (pytest):**
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

    # Override database dependency
    app.dependency_overrides[get_db] = lambda: db_session

    yield TestClient(app)

    app.dependency_overrides.clear()
```

**Frontend (Vitest):**
```typescript
// File: frontend/src/test/setup.ts
import { config } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';

// Global test setup
beforeEach(() => {
  // Reset Pinia state
  setActivePinia(createPinia());
});

// Mock console methods to avoid noise
global.console = {
  ...console,
  error: vi.fn(),
  warn: vi.fn(),
};
```

## Phase 5: Validation Gates

Run tests at appropriate gates:

### Gate 1: Unit Tests (Fast)
```bash
# Backend
uv run pytest tests/unit/ -v

# Frontend
npm run test:unit
```

### Gate 2: Contract Tests
```bash
# Backend
uv run pytest tests/contract/ -v

# Frontend
npm run test -- users.contract.test.ts
```

### Gate 3: Integration Tests
```bash
# Backend
uv run pytest tests/integration/ -v
```

### Gate 4: E2E Tests
```bash
# Frontend
npm run test:e2e:headless
```

### Gate 5: Coverage
```bash
# Backend
uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=80

# Frontend
npm run test:coverage -- --coverage.threshold.lines=80
```

## Testing Anti-Patterns

See: `~/.claude/skills/testing-anti-patterns/SKILL.md`

**DO NOT:**
- Test mock behavior
- Add test-only methods to production code
- Mock everything
- Write flaky tests
- Test implementation details
- Skip tests for "simple" code

## Completion Checklist

- [ ] Unit tests cover happy path
- [ ] Unit tests cover error cases
- [ ] Unit tests cover edge cases
- [ ] Integration tests verify end-to-end workflows
- [ ] Contract tests verify DTO structure
- [ ] E2E tests cover critical user paths
- [ ] All tests passing
- [ ] Coverage >= 80% for new code
- [ ] No flaky tests
- [ ] Tests run fast (< 10 seconds for unit)
- [ ] **Task completed:** `shark task complete <task-id>`

**Final Step:** Mark the task as complete:
```bash
shark task complete T-E04-F06-001
```

This updates the task status to "completed" and records completion time in the database.

## Reference

- TDD methodology: `../../test-driven-development/SKILL.md`
- Testing anti-patterns: `../../testing-anti-patterns/SKILL.md`
- Testing requirements: `../context/testing-requirements.md`

---

**Remember:** Tests are proof your code works. Write them comprehensively, run them frequently, trust them completely.
