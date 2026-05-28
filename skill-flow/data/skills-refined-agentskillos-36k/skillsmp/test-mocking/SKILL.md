---
name: test-mocking
description: 'Use mocking and test doubles to isolate code under test from external dependencies. Use when asked to "mock dependencies", "create test doubles", "isolate tests", "avoid external calls", or when testing code that depends on databases, APIs, cloud providers, or expensive resources. Applicable to Terraform, JavaScript, Python, Go, and other testing frameworks.'
---

# Test Mocking

Mock external dependencies to create fast, isolated, and deterministic tests. This skill covers mocking strategies applicable across testing frameworks and programming languages.

## When to Use This Skill

- User asks to "mock dependencies", "create mocks", "use test doubles"
- Testing code with external dependencies (databases, APIs, cloud services)
- Creating unit tests that run without credentials
- Avoiding slow or expensive resource creation in tests
- Isolating code under test from infrastructure dependencies
- Making tests deterministic and reproducible
- Testing error handling without triggering real errors

## Types of Test Doubles

### 1. Mock

**Definition:** Object that verifies behavior (interactions)

**Use when:** You need to verify a method was called with specific arguments

**Example (JavaScript/Jest):**
```javascript
const emailService = {
  send: jest.fn()
};

sendWelcomeEmail(user, emailService);

expect(emailService.send).toHaveBeenCalledWith({
  to: user.email,
  subject: 'Welcome!'
});
```

**Example (Python/unittest.mock):**
```python
from unittest.mock import Mock

email_service = Mock()
send_welcome_email(user, email_service)

email_service.send.assert_called_once_with(
    to=user.email,
    subject='Welcome!'
)
```

### 2. Stub

**Definition:** Object that provides canned responses

**Use when:** You need to control return values

**Example (JavaScript):**
```javascript
const database = {
  getUser: jest.fn().mockResolvedValue({ id: 1, name: 'John' })
};

const user = await fetchUserProfile(1, database);
expect(user.name).toBe('John');
```

**Example (Python):**
```python
database = Mock()
database.get_user.return_value = {'id': 1, 'name': 'John'}

user = fetch_user_profile(1, database)
assert user['name'] == 'John'
```

### 3. Fake

**Definition:** Working implementation with shortcuts

**Use when:** You need realistic behavior without full complexity

**Example (In-Memory Database):**
```javascript
class FakeUserRepository {
  constructor() {
    this.users = new Map();
  }

  save(user) {
    this.users.set(user.id, user);
    return Promise.resolve(user);
  }

  findById(id) {
    return Promise.resolve(this.users.get(id));
  }
}

// Use in tests
const repo = new FakeUserRepository();
await repo.save({ id: 1, name: 'John' });
const user = await repo.findById(1);
```

**Example (Python):**
```python
class FakeUserRepository:
    def __init__(self):
        self.users = {}

    def save(self, user):
        self.users[user.id] = user
        return user

    def find_by_id(self, user_id):
        return self.users.get(user_id)
```

### 4. Spy

**Definition:** Records information about calls while delegating to real object

**Use when:** You want real behavior + verification

**Example (JavaScript):**
```javascript
const realService = {
  processPayment: (amount) => ({ success: true, amount })
};

const spy = jest.spyOn(realService, 'processPayment');

const result = realService.processPayment(100);

expect(result.success).toBe(true);
expect(spy).toHaveBeenCalledWith(100);
```

## Mocking Strategies

### Strategy 1: Dependency Injection

**Principle:** Pass dependencies as parameters instead of creating them internally

**❌ Hard to test (dependencies hardcoded):**
```javascript
function sendWelcomeEmail(user) {
  const emailService = new EmailService(); // Hard-coded dependency
  emailService.send({
    to: user.email,
    subject: 'Welcome!'
  });
}
```

**✅ Easy to test (dependency injected):**
```javascript
function sendWelcomeEmail(user, emailService) {
  emailService.send({
    to: user.email,
    subject: 'Welcome!'
  });
}

// In test
const mockEmailService = { send: jest.fn() };
sendWelcomeEmail(user, mockEmailService);
```

### Strategy 2: Interface-Based Mocking

**Principle:** Depend on interfaces/protocols, not concrete implementations

**Example (TypeScript):**
```typescript
interface EmailService {
  send(message: EmailMessage): Promise<void>;
}

class RealEmailService implements EmailService {
  async send(message: EmailMessage) {
    // Real SMTP implementation
  }
}

class MockEmailService implements EmailService {
  async send(message: EmailMessage) {
    // Mock implementation for testing
  }
}
```

### Strategy 3: Environment-Based Mocking

**Principle:** Use environment detection to swap implementations

**Example (Terraform - Mock Provider):**
```hcl
mock_provider "aws" {}

run "test_without_credentials" {
  # Provider mocked - no AWS calls
}
```

**Example (JavaScript - Environment Check):**
```javascript
const emailService = process.env.NODE_ENV === 'test'
  ? new MockEmailService()
  : new RealEmailService();
```

### Strategy 4: Module/Import Mocking

**Principle:** Replace entire modules during test execution

**Example (Jest):**
```javascript
// In test file
jest.mock('./emailService', () => ({
  sendEmail: jest.fn()
}));

const { sendEmail } = require('./emailService');

// sendEmail is now a mock function
```

**Example (Python unittest.mock):**
```python
from unittest.mock import patch

@patch('myapp.email_service.send_email')
def test_send_welcome_email(mock_send):
    send_welcome_email(user)
    mock_send.assert_called_once()
```

## When to Mock vs When to Use Real Implementation

### ✅ Mock When:

1. **Dependency is slow**
   - Database queries
   - Network requests
   - File system operations
   - Cloud provider API calls

2. **Dependency is non-deterministic**
   - Random number generators
   - Current time/date
   - External API responses

3. **Dependency is expensive**
   - Cloud resource creation (EC2, S3, etc.)
   - Payment processing
   - SMS/email sending

4. **Dependency is unavailable**
   - No test credentials
   - Service not in test environment
   - Rate-limited APIs

5. **Testing error conditions**
   - Network timeouts
   - Service failures
   - Invalid responses

### ❌ Don't Mock When:

1. **Testing integration points**
   - Verifying actual service behavior
   - End-to-end tests
   - Contract testing

2. **Dependency is simple and fast**
   - Pure functions
   - Simple calculations
   - In-memory operations

3. **Mock would be as complex as real implementation**
   - Over-mocking leads to brittle tests
   - Test the real behavior instead

4. **You're testing the thing you'd mock**
   - Don't mock the system under test
   - Only mock dependencies

## Framework-Specific Examples

### Terraform Mock Provider

**Basic Mock:**
```hcl
mock_provider "aws" {}

run "unit_test" {
  command = plan

  assert {
    condition     = aws_s3_bucket.bucket.bucket == "expected-name"
    error_message = "Naming logic incorrect"
  }
}
```

**Mock with Defaults:**
```hcl
mock_provider "aws" {
  mock_resource "aws_s3_bucket" {
    defaults = {
      arn = "arn:aws:s3:::test-bucket"
    }
  }
}
```

**Override Specific Resources:**
```hcl
override_resource {
  target = aws_rds_instance.database
  values = {
    endpoint = "mock-db.us-east-1.rds.amazonaws.com:5432"
  }
}

run "test_without_rds" {
  # RDS not created, uses override values
}
```

### JavaScript/Jest Mocking

**Mock Function:**
```javascript
const mockFn = jest.fn();
mockFn.mockReturnValue(42);

expect(mockFn()).toBe(42);
expect(mockFn).toHaveBeenCalled();
```

**Mock Module:**
```javascript
jest.mock('./api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: 1, name: 'John' })
}));
```

**Spy on Method:**
```javascript
const spy = jest.spyOn(object, 'method');
spy.mockImplementation(() => 'mocked value');

expect(object.method()).toBe('mocked value');
expect(spy).toHaveBeenCalled();
```

### Python Mock (unittest.mock)

**Mock Object:**
```python
from unittest.mock import Mock

mock_db = Mock()
mock_db.get_user.return_value = {'id': 1, 'name': 'John'}

user = service.fetch_user(1, mock_db)
mock_db.get_user.assert_called_once_with(1)
```

**Patch Decorator:**
```python
from unittest.mock import patch

@patch('myapp.database.connection')
def test_fetch_user(mock_connection):
    mock_connection.query.return_value = [{'id': 1}]
    result = fetch_user(1)
    assert result['id'] == 1
```

**Context Manager:**
```python
from unittest.mock import patch

def test_send_email():
    with patch('myapp.email.send') as mock_send:
        send_welcome_email(user)
        mock_send.assert_called_once()
```

### Go Mocking (Interfaces)

**Define Interface:**
```go
type UserRepository interface {
    GetUser(id int) (*User, error)
    SaveUser(user *User) error
}
```

**Mock Implementation:**
```go
type MockUserRepository struct {
    GetUserFunc func(id int) (*User, error)
    SaveUserFunc func(user *User) error
}

func (m *MockUserRepository) GetUser(id int) (*User, error) {
    return m.GetUserFunc(id)
}

func (m *MockUserRepository) SaveUser(user *User) error {
    return m.SaveUserFunc(user)
}
```

**Use in Test:**
```go
func TestFetchUserProfile(t *testing.T) {
    mockRepo := &MockUserRepository{
        GetUserFunc: func(id int) (*User, error) {
            return &User{ID: 1, Name: "John"}, nil
        },
    }

    user, err := FetchUserProfile(1, mockRepo)
    assert.NoError(t, err)
    assert.Equal(t, "John", user.Name)
}
```

## Mock Data Management

### Shared Mock Data Files

**Terraform:**
```hcl
# tests/mocks/aws.tfmock.hcl
mock_resource "aws_s3_bucket" {
  defaults = {
    arn = "arn:aws:s3:::test-bucket"
  }
}

mock_data "aws_ami" {
  defaults = {
    id = "ami-12345678"
  }
}
```

```hcl
# tests/unit.tftest.hcl
mock_provider "aws" {
  source = "./tests/mocks"
}
```

**JavaScript:**
```javascript
// tests/fixtures/users.js
export const mockUsers = [
  { id: 1, name: 'John', email: 'john@example.com' },
  { id: 2, name: 'Jane', email: 'jane@example.com' }
];

// In test
import { mockUsers } from './fixtures/users';
database.getUsers.mockResolvedValue(mockUsers);
```

**Python:**
```python
# tests/fixtures/users.py
MOCK_USERS = [
    {'id': 1, 'name': 'John', 'email': 'john@example.com'},
    {'id': 2, 'name': 'Jane', 'email': 'jane@example.com'}
]

# In test
from tests.fixtures.users import MOCK_USERS
mock_db.get_users.return_value = MOCK_USERS
```

## Best Practices

### 1. Mock at the Boundaries

**✅ Good - Mock external services:**
```javascript
// Mock HTTP client
const mockHttp = {
  get: jest.fn().mockResolvedValue({ data: { user: 'John' } })
};

// Test your service
const result = await userService.fetchUser(1, mockHttp);
```

**❌ Bad - Mock internal logic:**
```javascript
// Don't mock the thing you're testing
jest.mock('./userService');
const userService = require('./userService');
userService.fetchUser.mockResolvedValue({ user: 'John' });
```

### 2. Verify Behavior, Not Implementation

**✅ Good - Test outcomes:**
```javascript
await sendWelcomeEmail(user, emailService);

expect(emailService.send).toHaveBeenCalledWith(
  expect.objectContaining({
    to: user.email,
    subject: expect.stringContaining('Welcome')
  })
);
```

**❌ Bad - Test implementation details:**
```javascript
// Too brittle - breaks when implementation changes
expect(emailService.send).toHaveBeenCalledTimes(1);
expect(emailService.send.mock.calls[0][0].to).toBe(user.email);
```

### 3. Keep Mocks Simple

**✅ Good - Simple, focused mock:**
```javascript
const mockDatabase = {
  getUser: jest.fn().mockResolvedValue({ id: 1, name: 'John' })
};
```

**❌ Bad - Complex mock duplicating real implementation:**
```javascript
const mockDatabase = {
  getUser: jest.fn(async (id) => {
    // Don't reimplement the real database logic
    const users = await loadFromFile();
    return users.find(u => u.id === id);
  })
};
```

### 4. Reset Mocks Between Tests

**JavaScript:**
```javascript
beforeEach(() => {
  jest.clearAllMocks();
});
```

**Python:**
```python
def setup_method(self):
    self.mock_db = Mock()
```

### 5. Use Realistic Test Data

**✅ Good - Realistic data:**
```javascript
const mockUser = {
  id: 'usr_1234567890',
  email: 'john.doe@example.com',
  created_at: '2024-01-15T10:30:00Z'
};
```

**❌ Bad - Unrealistic data:**
```javascript
const mockUser = {
  id: 1,
  email: 'test',
  created_at: 'now'
};
```

## Anti-Patterns

### ❌ Over-Mocking

**Problem:** Mocking everything, including simple logic

```javascript
// Don't do this
jest.mock('./utils/add');
const add = require('./utils/add');
add.mockReturnValue(5);

expect(add(2, 3)).toBe(5);
// You're testing the mock, not the code!
```

**Solution:** Only mock external dependencies

### ❌ Leaky Mocks

**Problem:** Mock state persists between tests

```javascript
describe('User tests', () => {
  const mockDb = { getUser: jest.fn() };

  test('test 1', () => {
    mockDb.getUser.mockResolvedValue({ id: 1 });
  });

  test('test 2', () => {
    // Mock still has state from test 1!
  });
});
```

**Solution:** Reset mocks in beforeEach

### ❌ Mocking the System Under Test

**Problem:** Mocking the code you're trying to test

```javascript
// Don't do this
jest.mock('./orderService');
const orderService = require('./orderService');
orderService.createOrder.mockResolvedValue({ id: 1 });

// You're not testing anything!
const result = await orderService.createOrder();
```

**Solution:** Only mock dependencies, test real implementation

## Mocking Decision Tree

**Ask yourself:**

1. **Is it an external dependency?**
   - ✅ Yes → Consider mocking
   - ❌ No → Don't mock

2. **Is it slow or expensive?**
   - ✅ Yes → Mock for unit tests
   - ❌ No → Use real implementation

3. **Is it the code under test?**
   - ✅ Yes → Never mock
   - ❌ No → Can mock

4. **Does mocking simplify the test?**
   - ✅ Yes → Mock
   - ❌ No → Keep it real

5. **Am I testing integration?**
   - ✅ Yes → Don't mock
   - ❌ No → Can mock

## References

- **Test Doubles**: <https://martinfowler.com/bliki/TestDouble.html>
- **Mocking Best Practices**: <https://kentcdodds.com/blog/mocking-is-a-code-smell>
- **Terraform Mocking**: <https://developer.hashicorp.com/terraform/language/tests/mocking>
- **Jest Mocking**: <https://jestjs.io/docs/mock-functions>
- **Python unittest.mock**: <https://docs.python.org/3/library/unittest.mock.html>
- **Test Assertions**: Use the **test-assertions** skill for validation patterns
- **Test Organization**: Use the **test-organization-patterns** skill for test structure
