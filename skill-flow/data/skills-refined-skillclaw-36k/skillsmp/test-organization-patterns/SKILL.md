---
name: test-organization-patterns
description: 'Organize tests into maintainable structures with helper modules, clear patterns, and quality standards. Use when asked to "organize tests", "structure test suite", "create test helpers", or when building comprehensive test coverage. Applicable to Terraform, JavaScript, Python, Go, and other testing frameworks.'
---

# Test Organization Patterns

Structure tests for maintainability, clarity, and comprehensive coverage. This skill covers test organization applicable across testing frameworks and programming languages.

## When to Use This Skill

- User asks to "organize tests", "structure test suite", "set up testing"
- Creating comprehensive test coverage
- Building test infrastructure (helpers, fixtures, utilities)
- Organizing large test suites
- Establishing testing patterns for teams
- Improving test maintainability

## Test Directory Structures

### Terraform

**Standard Layout:**
```
module-root/
├── main.tf
├── variables.tf
├── outputs.tf
└── tests/
    ├── basic.tftest.hcl          # Simple test
    ├── integration.tftest.hcl    # Integration tests
    ├── unit.tftest.hcl           # Unit tests (mocked)
    ├── setup/                    # Setup helper module
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    ├── final/                    # Validation helper module
    │   └── main.tf
    └── mocks/                    # Shared mock data
        └── aws.tfmock.hcl
```

### JavaScript (Jest)

**Standard Layout:**
```
src/
├── services/
│   ├── userService.js
│   └── __tests__/
│       ├── userService.test.js
│       └── userService.integration.test.js
├── utils/
│   ├── validation.js
│   └── __tests__/
│       └── validation.test.js
└── __tests__/
    ├── setup.js              # Test setup
    ├── fixtures/             # Test data
    │   ├── users.js
    │   └── products.js
    └── helpers/              # Test utilities
        ├── database.js
        └── api.js
```

**Alternative (tests/ directory):**
```
src/
└── services/
    └── userService.js
tests/
├── unit/
│   └── services/
│       └── userService.test.js
├── integration/
│   └── services/
│       └── userService.integration.test.js
├── fixtures/
│   └── users.js
└── helpers/
    └── database.js
```

### Python (pytest)

**Standard Layout:**
```
src/
└── myapp/
    ├── services/
    │   └── user_service.py
    └── utils/
        └── validation.py
tests/
├── unit/
│   ├── test_user_service.py
│   └── test_validation.py
├── integration/
│   └── test_user_service_integration.py
├── fixtures/
│   ├── __init__.py
│   └── users.py
├── helpers/
│   ├── __init__.py
│   └── database.py
└── conftest.py              # Shared fixtures
```

### Go

**Standard Layout:**
```
pkg/
└── services/
    ├── user.go
    └── user_test.go         # Tests next to code
internal/
└── database/
    ├── db.go
    └── db_test.go
test/
├── integration/             # Integration tests
│   └── user_integration_test.go
├── fixtures/                # Test data
│   └── users.go
└── helpers/                 # Test utilities
    └── database.go
```

## Helper Modules/Utilities

### Terraform Helper Modules

**Setup Module (tests/setup/):**
```hcl
# tests/setup/main.tf
terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "3.5.1"
    }
  }
}

resource "random_pet" "prefix" {
  length = 4
}

output "prefix" {
  value = random_pet.prefix.id
}
```

**Using Setup Module:**
```hcl
# tests/integration.tftest.hcl
run "setup" {
  module {
    source = "./tests/setup"
  }
}

run "create_resources" {
  variables {
    name = "${run.setup.prefix}-resource"
  }
}
```

**Validation Module (tests/final/):**
```hcl
# tests/final/main.tf
terraform {
  required_providers {
    http = {
      source  = "hashicorp/http"
      version = "3.4.0"
    }
  }
}

variable "endpoint" {
  type = string
}

data "http" "health" {
  url = var.endpoint
}

output "status_code" {
  value = data.http.health.status_code
}
```

### JavaScript Test Helpers

**Database Helper:**
```javascript
// tests/helpers/database.js
export class TestDatabase {
  constructor() {
    this.data = new Map();
  }

  async insert(table, record) {
    const key = `${table}:${record.id}`;
    this.data.set(key, record);
    return record;
  }

  async findById(table, id) {
    return this.data.get(`${table}:${id}`);
  }

  clear() {
    this.data.clear();
  }
}
```

**API Helper:**
```javascript
// tests/helpers/api.js
import request from 'supertest';

export class TestApiClient {
  constructor(app) {
    this.app = app;
  }

  async post(path, data) {
    const response = await request(this.app)
      .post(path)
      .send(data)
      .expect(200);
    return response.body;
  }

  async get(path) {
    const response = await request(this.app)
      .get(path)
      .expect(200);
    return response.body;
  }
}
```

### Python Test Fixtures

**conftest.py (shared fixtures):**
```python
# tests/conftest.py
import pytest
from myapp.database import Database

@pytest.fixture
def database():
    """Provide test database instance."""
    db = Database(':memory:')
    db.setup()
    yield db
    db.teardown()

@pytest.fixture
def mock_users():
    """Provide sample user data."""
    return [
        {'id': 1, 'name': 'John', 'email': 'john@example.com'},
        {'id': 2, 'name': 'Jane', 'email': 'jane@example.com'}
    ]

@pytest.fixture
def api_client(database):
    """Provide configured API client."""
    from myapp.app import create_app
    app = create_app(database)
    return app.test_client()
```

**Using Fixtures:**
```python
# tests/unit/test_user_service.py
def test_create_user(database, mock_users):
    service = UserService(database)
    user = service.create_user(mock_users[0])
    assert user['id'] == 1
```

### Go Test Helpers

**Database Helper:**
```go
// test/helpers/database.go
package helpers

type TestDatabase struct {
    data map[string]interface{}
}

func NewTestDatabase() *TestDatabase {
    return &TestDatabase{
        data: make(map[string]interface{}),
    }
}

func (db *TestDatabase) Insert(key string, value interface{}) error {
    db.data[key] = value
    return nil
}

func (db *TestDatabase) Get(key string) (interface{}, error) {
    val, exists := db.data[key]
    if !exists {
        return nil, errors.New("not found")
    }
    return val, nil
}
```

**Using Helper:**
```go
// pkg/services/user_test.go
func TestCreateUser(t *testing.T) {
    db := helpers.NewTestDatabase()
    service := NewUserService(db)

    user, err := service.CreateUser("John")
    assert.NoError(t, err)
    assert.Equal(t, "John", user.Name)
}
```

## Common Test Patterns

### Pattern 1: Setup → Execute → Validate

**Terraform:**
```hcl
# Setup dependencies
run "setup" {
  module {
    source = "./tests/setup"
  }
}

# Execute test
run "create_infrastructure" {
  variables {
    dependency_id = run.setup.output_id
  }
}

# Validate results
run "validate" {
  module {
    source = "./tests/final"
  }

  variables {
    target = run.create_infrastructure.endpoint
  }

  assert {
    condition     = output.status_code == 200
    error_message = "Validation failed"
  }
}
```

**JavaScript:**
```javascript
describe('User Service', () => {
  let database;
  let service;

  // Setup
  beforeEach(() => {
    database = new TestDatabase();
    service = new UserService(database);
  });

  // Execute + Validate
  it('creates user', async () => {
    const user = await service.createUser({ name: 'John' });
    expect(user.name).toBe('John');
  });

  // Cleanup
  afterEach(() => {
    database.clear();
  });
});
```

**Python:**
```python
class TestUserService:
    # Setup
    def setup_method(self):
        self.database = TestDatabase()
        self.service = UserService(self.database)

    # Execute + Validate
    def test_create_user(self):
        user = self.service.create_user({'name': 'John'})
        assert user['name'] == 'John'

    # Cleanup
    def teardown_method(self):
        self.database.clear()
```

### Pattern 2: Parallel Independent Tests

**Terraform:**
```hcl
test {
  parallel = true
}

run "test_scenario_a" {
  state_key = "scenario_a"
  # Independent state
}

run "test_scenario_b" {
  state_key = "scenario_b"
  # Independent state
}

run "test_scenario_c" {
  state_key = "scenario_c"
  # Independent state
}
```

**JavaScript:**
```javascript
// Tests run in parallel by default in Jest
describe('User Service', () => {
  it('scenario A', () => { /* independent test */ });
  it('scenario B', () => { /* independent test */ });
  it('scenario C', () => { /* independent test */ });
});
```

### Pattern 3: Progressive Validation

**Terraform:**
```hcl
# Phase 1: Plan validation
run "plan_validation" {
  command = plan

  assert {
    condition     = aws_s3_bucket.bucket.bucket == "expected"
    error_message = "Plan-time validation failed"
  }
}

# Phase 2: Apply validation
run "apply_validation" {
  command = apply

  assert {
    condition     = can(regex("^arn:aws:", aws_s3_bucket.bucket.arn))
    error_message = "Resource not created"
  }
}

# Phase 3: Runtime validation
run "runtime_validation" {
  module {
    source = "./tests/final"
  }

  assert {
    condition     = output.status_code == 200
    error_message = "Runtime validation failed"
  }
}
```

### Pattern 4: Matrix Testing

**Terraform:**
```hcl
# Test multiple configurations
run "test_dev" {
  variables {
    environment = "dev"
    size = "small"
  }
}

run "test_staging" {
  variables {
    environment = "staging"
    size = "medium"
  }
}

run "test_prod" {
  variables {
    environment = "prod"
    size = "large"
  }
}
```

**JavaScript (Parameterized):**
```javascript
describe.each([
  { env: 'dev', size: 'small' },
  { env: 'staging', size: 'medium' },
  { env: 'prod', size: 'large' }
])('Environment: $env', ({ env, size }) => {
  it(`configures ${env} correctly`, () => {
    const config = createConfig(env, size);
    expect(config.environment).toBe(env);
    expect(config.size).toBe(size);
  });
});
```

**Python (Parametrize):**
```python
import pytest

@pytest.mark.parametrize("env,size", [
    ("dev", "small"),
    ("staging", "medium"),
    ("prod", "large")
])
def test_environment_config(env, size):
    config = create_config(env, size)
    assert config['environment'] == env
    assert config['size'] == size
```

## Test Quality Standards

### Naming Conventions

**Descriptive Test Names:**

**✅ Good:**
```javascript
test('creates user with valid email')
test('throws error when email is invalid')
test('updates user profile successfully')
```

**❌ Bad:**
```javascript
test('test1')
test('user test')
test('works')
```

**Pattern: `<action>_<scenario>_<expected_result>`**

**Terraform:**
```hcl
run "validate_bucket_name_format"
run "test_encryption_enabled"
run "verify_tags_applied"
```

**Python:**
```python
def test_create_user_with_valid_email()
def test_create_user_raises_error_when_email_invalid()
def test_update_user_profile_successfully()
```

### Test Independence

**✅ Good - Independent tests:**
```javascript
test('user creation', () => {
  const db = new TestDatabase();
  const service = new UserService(db);
  const user = service.createUser({ name: 'John' });
  expect(user.name).toBe('John');
});

test('user update', () => {
  const db = new TestDatabase();
  const service = new UserService(db);
  service.createUser({ id: 1, name: 'John' });
  service.updateUser(1, { name: 'Jane' });
  const user = service.getUser(1);
  expect(user.name).toBe('Jane');
});
```

**❌ Bad - Tests depend on order:**
```javascript
let globalDb;
let globalService;

test('create user', () => {
  globalDb = new TestDatabase();
  globalService = new UserService(globalDb);
  globalService.createUser({ id: 1, name: 'John' });
});

test('update user', () => {
  // Depends on previous test!
  globalService.updateUser(1, { name: 'Jane' });
});
```

### Test Isolation

**Use beforeEach/afterEach:**

**JavaScript:**
```javascript
describe('User Service', () => {
  let database;
  let service;

  beforeEach(() => {
    database = new TestDatabase();
    service = new UserService(database);
  });

  afterEach(() => {
    database.clear();
  });

  test('creates user', () => {
    // Fresh database for each test
  });
});
```

**Python:**
```python
class TestUserService:
    def setup_method(self):
        self.database = TestDatabase()
        self.service = UserService(self.database)

    def teardown_method(self):
        self.database.clear()

    def test_creates_user(self):
        # Fresh database for each test
        pass
```

### Coverage Standards

**Aim for:**
- **Statements:** 80%+ coverage
- **Branches:** 80%+ coverage
- **Functions:** 90%+ coverage
- **Lines:** 80%+ coverage

**Test Coverage Types:**

1. **Happy Path** - Normal, expected usage
2. **Edge Cases** - Boundary conditions
3. **Error Cases** - Invalid inputs, failures
4. **Integration** - Component interactions

**Example:**
```javascript
// Happy path
test('creates user with valid data', () => {
  const user = service.createUser({ name: 'John', email: 'john@example.com' });
  expect(user).toBeDefined();
});

// Edge case - empty name
test('handles empty name', () => {
  const user = service.createUser({ name: '', email: 'john@example.com' });
  expect(user.name).toBe('');
});

// Error case - invalid email
test('throws error for invalid email', () => {
  expect(() => {
    service.createUser({ name: 'John', email: 'invalid' });
  }).toThrow('Invalid email');
});

// Integration
test('persists user to database', async () => {
  const user = await service.createUser({ name: 'John' });
  const retrieved = await database.findById('users', user.id);
  expect(retrieved).toEqual(user);
});
```

## Test Organization Checklist

Before finalizing test suite:

### Structure
- [ ] Tests organized in logical directories
- [ ] Unit and integration tests separated
- [ ] Helper modules/utilities in dedicated directories
- [ ] Shared fixtures/data easily accessible

### Naming
- [ ] Test files follow naming convention (`*.test.js`, `test_*.py`, `*_test.go`, `*.tftest.hcl`)
- [ ] Test names are descriptive and clear
- [ ] Helper/fixture files clearly named

### Independence
- [ ] Tests can run in any order
- [ ] Tests don't depend on shared state
- [ ] Each test has proper setup/teardown
- [ ] Parallel execution possible (if desired)

### Coverage
- [ ] Happy path tested
- [ ] Edge cases covered
- [ ] Error conditions tested
- [ ] Integration points validated

### Quality
- [ ] Clear, helpful error messages
- [ ] Assertions test behavior, not implementation
- [ ] No hardcoded test data
- [ ] Tests run quickly

## Framework-Specific Patterns

### Jest Best Practices

**Group Related Tests:**
```javascript
describe('UserService', () => {
  describe('createUser', () => {
    it('creates user with valid data', () => {});
    it('throws error for invalid email', () => {});
  });

  describe('updateUser', () => {
    it('updates existing user', () => {});
    it('throws error for non-existent user', () => {});
  });
});
```

**Setup/Teardown:**
```javascript
beforeAll(() => {
  // Runs once before all tests
});

afterAll(() => {
  // Runs once after all tests
});

beforeEach(() => {
  // Runs before each test
});

afterEach(() => {
  // Runs after each test
});
```

### Pytest Best Practices

**Fixtures:**
```python
@pytest.fixture(scope="module")
def database():
    """Module-scoped fixture - shared across module"""
    db = Database()
    yield db
    db.close()

@pytest.fixture(scope="function")
def user():
    """Function-scoped fixture - new for each test"""
    return {'id': 1, 'name': 'John'}
```

**Markers:**
```python
@pytest.mark.slow
def test_slow_operation():
    pass

@pytest.mark.integration
def test_database_integration():
    pass

# Run with: pytest -m "not slow"
```

### Go Test Best Practices

**Subtests:**
```go
func TestUserService(t *testing.T) {
    t.Run("CreateUser", func(t *testing.T) {
        t.Run("with valid data", func(t *testing.T) {
            // Test implementation
        })

        t.Run("with invalid email", func(t *testing.T) {
            // Test implementation
        })
    })
}
```

**Table-Driven Tests:**
```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid email", "john@example.com", false},
        {"invalid email", "invalid", true},
        {"empty email", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateEmail() error = %v, wantErr %v", err, tt.wantErr)
            }
        })
    }
}
```

## Best Practices Summary

### Do's

✅ **Organize tests in logical directories**
✅ **Use descriptive test names**
✅ **Keep tests independent and isolated**
✅ **Create reusable helper modules/fixtures**
✅ **Separate unit and integration tests**
✅ **Use setup/teardown appropriately**
✅ **Test happy path, edge cases, and errors**
✅ **Aim for good coverage (80%+)**
✅ **Keep tests focused (one concern per test)**
✅ **Make tests run quickly**

### Don'ts

❌ **Don't create test dependencies (order matters)**
❌ **Don't use global state between tests**
❌ **Don't skip cleanup/teardown**
❌ **Don't test implementation details**
❌ **Don't create overly complex test helpers**
❌ **Don't duplicate test logic**
❌ **Don't ignore slow tests**
❌ **Don't mix unit and integration tests**

## References

- **Jest Documentation**: <https://jestjs.io/docs/getting-started>
- **Pytest Documentation**: <https://docs.pytest.org/>
- **Go Testing**: <https://golang.org/pkg/testing/>
- **Terraform Tests**: <https://developer.hashicorp.com/terraform/language/tests>
- **Test Mocking**: Use the **test-mocking** skill for mocking patterns
- **Test Assertions**: Use the **test-assertions** skill for assertion best practices
- **Terraform Tests**: Use the **terraform-tests** skill for Terraform test block syntax
