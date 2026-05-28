# Test Case Organization Rules

This document defines comprehensive rules for organizing test cases from scattered business code into proper test directory structures.

## Directory Structure Standards

### Standard Test Directory Layout

```
project-root/
├── src/               # Business code
│   ├── module_a/
│   ├── module_b/
│   └── utils/
└── tests/             # All test code
    ├── unit/          # Unit tests
    │   ├── module_a/
    │   ├── module_b/
    │   └── utils/
    ├── integration/   # Integration tests
    │   └── api/
    └── e2e/           # End-to-end tests
        └── scenarios/
```

### Alternative Patterns

#### Co-located Tests (JavaScript/TypeScript)

```
src/
├── components/
│   ├── Button.tsx
│   ├── Button.test.tsx      # Co-located
│   ├── Form.tsx
│   └── Form.test.tsx
└── utils/
    ├── helpers.ts
    └── helpers.test.ts
```

#### Java Maven Structure

```
src/
├── main/
│   └── java/
│       └── com/example/
│           └── MyClass.java
└── test/
    └── java/
        └── com/example/
            └── MyClassTest.java
```

#### Python Package Structure

```
mypackage/
├── __init__.py
├── module_a.py
├── module_b.py
└── tests/
    ├── __init__.py
    ├── test_module_a.py
    └── test_module_b.py
```

## Naming Conventions

### Test File Naming

| Language/Framework | Convention | Example |
|-------------------|------------|---------|
| Python (pytest) | `test_*.py` or `*_test.py` | `test_auth.py` |
| Python (unittest) | `test_*.py` | `test_user_service.py` |
| JavaScript (Jest) | `*.test.js` or `*.spec.js` | `Button.test.js` |
| Java (JUnit) | `*Test.java` | `UserServiceTest.java` |
| Go | `*_test.go` | `auth_test.go` |
| Ruby (RSpec) | `*_spec.rb` | `user_spec.rb` |
| C# (NUnit) | `*Tests.cs` | `UserServiceTests.cs` |

### Test Function Naming

**Python:**
```python
def test_user_login_success():          # Descriptive, action-based
    pass

def test_user_login_invalid_password():
    pass

def test_calculate_total_with_discount():
    pass
```

**JavaScript:**
```javascript
test('user login succeeds with valid credentials', () => {});
it('should calculate total with discount', () => {});
describe('UserService', () => {
    test('creates new user', () => {});
});
```

**Java:**
```java
@Test
public void testUserLoginSuccess() {}

@Test
public void testCalculateTotalWithDiscount() {}
```

## Test Classification Rules

### Unit Tests

**Characteristics:**
- Test single function, method, or class
- No external dependencies (database, network, file system)
- Fast execution (<100ms per test)
- Use mocks/stubs for dependencies

**Examples:**
```python
# Unit test - isolated function
def test_calculate_discount():
    result = calculate_discount(100, 0.1)
    assert result == 90

# Unit test - pure logic
def test_validate_email_format():
    assert validate_email("user@example.com") == True
    assert validate_email("invalid") == False
```

**Location:** `tests/unit/`

### Integration Tests

**Characteristics:**
- Test interaction between components
- May use real dependencies (database, API)
- Slower execution (100ms - 5s per test)
- Test data flow across boundaries

**Examples:**
```python
# Integration test - database interaction
def test_user_repository_save():
    user = User(name="Alice")
    repo = UserRepository(db_connection)
    repo.save(user)

    retrieved = repo.find_by_name("Alice")
    assert retrieved.name == "Alice"

# Integration test - API endpoint
def test_create_user_endpoint():
    response = client.post('/users', json={'name': 'Bob'})
    assert response.status_code == 201
```

**Location:** `tests/integration/`

### End-to-End (E2E) Tests

**Characteristics:**
- Test complete user workflows
- Use full application stack
- Slowest execution (>5s per test)
- Test from user perspective

**Examples:**
```python
# E2E test - complete workflow
def test_user_registration_and_login_flow():
    # Register
    register_page.fill_form(email="test@example.com", password="pass123")
    register_page.submit()

    # Login
    login_page.login(email="test@example.com", password="pass123")

    # Verify dashboard
    assert dashboard_page.is_displayed()
```

**Location:** `tests/e2e/`

## Categorization Criteria

### By Business Domain

Group tests by feature area or module:

```
tests/unit/
├── auth/              # Authentication tests
│   ├── test_login.py
│   └── test_permissions.py
├── payments/          # Payment processing tests
│   ├── test_checkout.py
│   └── test_refunds.py
└── users/             # User management tests
    ├── test_profile.py
    └── test_registration.py
```

### By Component Type

```
tests/unit/
├── models/            # Data model tests
├── services/          # Business logic tests
├── controllers/       # Request handling tests
└── utils/             # Utility function tests
```

### By Test Scope

```
tests/
├── unit/              # Single component
│   └── services/
├── integration/       # Multiple components
│   └── api/
├── e2e/              # Full system
│   └── workflows/
└── performance/       # Load/stress tests
    └── benchmarks/
```

## Framework-Specific Rules

### pytest (Python)

**File structure:**
```
tests/
├── conftest.py                # Shared fixtures
├── unit/
│   ├── conftest.py            # Unit-specific fixtures
│   └── test_module.py
└── integration/
    └── test_api.py
```

**Fixture organization:**
- Global fixtures: `tests/conftest.py`
- Scope-specific fixtures: `tests/{scope}/conftest.py`
- Test-specific fixtures: Inside test file

**Markers:**
```python
# tests/pytest.ini
[pytest]
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow-running tests

# Usage
@pytest.mark.unit
def test_fast_function():
    pass

@pytest.mark.integration
@pytest.mark.slow
def test_database_operation():
    pass
```

### Jest (JavaScript/TypeScript)

**File structure:**
```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   └── Button.test.tsx      # Co-located
│   └── __tests__/               # Or centralized
│       └── Button.test.tsx
└── utils/
    ├── helpers.ts
    └── __tests__/
        └── helpers.test.ts
```

**Test organization:**
```javascript
describe('UserService', () => {
    describe('createUser', () => {
        it('should create user with valid data', () => {});
        it('should throw error with invalid email', () => {});
    });

    describe('deleteUser', () => {
        it('should delete existing user', () => {});
    });
});
```

**Setup files:**
```javascript
// jest.config.js
module.exports = {
    testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
    setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
};
```

### JUnit (Java)

**File structure:**
```
src/
├── main/java/com/example/
│   └── UserService.java
└── test/java/com/example/
    └── UserServiceTest.java
```

**Naming convention:**
- Class: `<ClassName>Test` (e.g., `UserServiceTest`)
- Method: `test<Method>_<Condition>_<ExpectedResult>`

**Organization:**
```java
public class UserServiceTest {
    @BeforeEach
    void setUp() {
        // Setup before each test
    }

    @Test
    void testCreateUser_ValidData_Success() {
        // Test implementation
    }

    @Test
    void testCreateUser_InvalidEmail_ThrowsException() {
        // Test implementation
    }

    @AfterEach
    void tearDown() {
        // Cleanup after each test
    }
}
```

### Go Standard Testing

**File structure:**
```
mypackage/
├── user.go
└── user_test.go          # Same directory
```

**Naming convention:**
```go
// user_test.go
package mypackage

import "testing"

func TestCreateUser(t *testing.T) {
    // Test implementation
}

func TestCreateUser_InvalidEmail(t *testing.T) {
    // Test implementation
}
```

**Table-driven tests:**
```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        want    bool
    }{
        {"valid email", "user@example.com", true},
        {"invalid format", "invalid", false},
        {"missing @", "userexample.com", false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := ValidateEmail(tt.email)
            if got != tt.want {
                t.Errorf("got %v, want %v", got, tt.want)
            }
        })
    }
}
```

## Test Data Management

### Test Fixtures

**Location:**
```
tests/
├── fixtures/
│   ├── users.json           # Sample user data
│   ├── products.csv         # Product catalog
│   └── api_responses/       # Mock API responses
│       └── github_user.json
└── unit/
    └── test_module.py
```

**Loading fixtures:**
```python
# Python
import json
from pathlib import Path

def load_fixture(filename):
    fixture_path = Path(__file__).parent.parent / 'fixtures' / filename
    with open(fixture_path) as f:
        return json.load(f)

def test_process_user_data():
    user_data = load_fixture('users.json')
    result = process_users(user_data)
    assert len(result) == 5
```

### Factory Pattern

```python
# tests/factories.py
class UserFactory:
    @staticmethod
    def create(**kwargs):
        defaults = {
            'name': 'Test User',
            'email': 'test@example.com',
            'age': 30
        }
        defaults.update(kwargs)
        return User(**defaults)

# Usage in tests
def test_user_validation():
    user = UserFactory.create(age=17)
    assert not user.is_adult()
```

## Shared Test Utilities

### Helper Functions

**Location:** `tests/helpers.py` or `tests/utils/`

```python
# tests/helpers.py
def assert_response_success(response):
    """Helper to check successful API response"""
    assert response.status_code == 200
    assert 'error' not in response.json()

def create_temp_file(content):
    """Create temporary test file"""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(content)
        return f.name
```

### Mock Utilities

```python
# tests/mocks.py
class MockDatabase:
    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

# Usage
def test_with_mock_db():
    db = MockDatabase()
    service = UserService(db)
    service.create_user('Alice')
    assert db.get('users')['Alice'] is not None
```

## Anti-Patterns to Avoid

### ❌ Tests in Business Code

```python
# BAD: Test code mixed with business logic
def calculate_total(items):
    total = sum(item.price for item in items)

    # Inline test - DO NOT DO THIS
    assert total > 0, "Total should be positive"

    return total
```

**Fix:** Move to proper test file:
```python
# Good: tests/unit/test_calculations.py
def test_calculate_total_positive():
    items = [Item(price=10), Item(price=20)]
    total = calculate_total(items)
    assert total > 0
```

### ❌ Scattered Test Files

```
# BAD: No organization
project/
├── module_a.py
├── test_something.py        # Scattered
├── module_b.py
├── quick_test.py            # Ad-hoc
└── module_c_tests.py        # Inconsistent naming
```

**Fix:** Organize properly:
```
project/
├── src/
│   ├── module_a.py
│   ├── module_b.py
│   └── module_c.py
└── tests/
    ├── test_module_a.py
    ├── test_module_b.py
    └── test_module_c.py
```

### ❌ Tests Without Assertions

```python
# BAD: No verification
def test_create_user():
    user = create_user('Alice')
    # Missing assertion!
```

**Fix:** Always assert expected behavior:
```python
# Good
def test_create_user():
    user = create_user('Alice')
    assert user.name == 'Alice'
    assert user.is_active == True
```

### ❌ Overly Generic Test Names

```python
# BAD: Unclear purpose
def test_user():
    pass

def test_function():
    pass
```

**Fix:** Descriptive names:
```python
# Good
def test_user_login_with_valid_credentials():
    pass

def test_calculate_discount_applies_percentage_correctly():
    pass
```

## Best Practices

### 1. One Test, One Assertion (Guideline)

Prefer focused tests:
```python
# Preferred
def test_user_creation_sets_name():
    user = User(name='Alice')
    assert user.name == 'Alice'

def test_user_creation_sets_active_status():
    user = User(name='Alice')
    assert user.is_active == True
```

### 2. Arrange-Act-Assert Pattern

```python
def test_shopping_cart_total():
    # Arrange
    cart = ShoppingCart()
    cart.add_item(Item(price=10))
    cart.add_item(Item(price=20))

    # Act
    total = cart.calculate_total()

    # Assert
    assert total == 30
```

### 3. Test Independence

Each test should be runnable in isolation:
```python
# BAD: Tests depend on each other
class TestUserSequence:
    user = None

    def test_1_create_user(self):
        self.user = create_user('Alice')

    def test_2_update_user(self):
        self.user.name = 'Bob'  # Depends on test_1

# GOOD: Independent tests
class TestUser:
    def test_create_user(self):
        user = create_user('Alice')
        assert user.name == 'Alice'

    def test_update_user(self):
        user = create_user('Alice')
        user.name = 'Bob'
        assert user.name == 'Bob'
```

### 4. Meaningful Test Data

Use realistic, representative data:
```python
# Weak
def test_user_age_validation():
    assert validate_age(999) == False

# Better
def test_user_age_validation_rejects_unrealistic_age():
    assert validate_age(150) == False  # Clearly unrealistic
    assert validate_age(-5) == False   # Negative age
    assert validate_age(0) == False    # Zero age
```

### 5. Test Coverage Balance

Aim for:
- **Unit tests:** 70-80% of test suite (fast, focused)
- **Integration tests:** 15-25% (verify interactions)
- **E2E tests:** 5-10% (critical user paths)

## Migration Strategy

### Step-by-Step Migration

1. **Identify scattered tests** - Run organizer script to scan
2. **Create test directory structure** - Establish standard layout
3. **Move tests in batches** - Migrate by module or feature
4. **Update imports and dependencies** - Fix broken references
5. **Execute test suite** - Verify all tests still pass
6. **Remove from business code** - Clean up original locations
7. **Update CI/CD** - Ensure test discovery works
8. **Document structure** - Update project README

### Gradual Migration

For large codebases, migrate incrementally:
- **Week 1:** Set up test directory, move high-priority module
- **Week 2:** Move next module, address failures
- **Week 3:** Continue module-by-module
- **Week 4:** Final cleanup, documentation

### Validation Checklist

After organization:
- [ ] All tests discoverable by test runner
- [ ] Test suite passes completely
- [ ] No test code remains in business files
- [ ] Test coverage maintained or improved
- [ ] CI/CD pipeline updated
- [ ] Documentation reflects new structure
- [ ] Team trained on new organization

## Summary

Effective test organization:
- **Follows standard conventions** for the language/framework
- **Groups tests logically** by type and domain
- **Uses consistent naming** for discoverability
- **Separates concerns** between unit/integration/e2e
- **Maintains independence** between tests
- **Provides clear structure** for new contributors

Use this guide as reference when organizing scattered test cases into maintainable, discoverable test suites.
