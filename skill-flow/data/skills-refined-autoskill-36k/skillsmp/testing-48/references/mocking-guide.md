# When and How to Mock

Mocking enables unit testing but can hide bugs if overused.

## When to Mock

### ✅ DO Mock

- **External services** - APIs, databases, file systems
- **Time-dependent code** - Clocks, timers, schedulers
- **Non-deterministic code** - Random numbers, UUIDs
- **Expensive operations** - Network calls, heavy computation
- **Error conditions** - Hard to trigger naturally

### ❌ DON'T Mock

- **The code under test** - You're testing nothing
- **Simple data transformations** - Just test the real code
- **Internal implementation details** - Tests become brittle
- **Everything** - Tests become meaningless

## Mock Types

| Type | Purpose | Example |
|------|---------|---------|
| **Stub** | Returns canned data | `userService.getUser = () => fakeUser` |
| **Spy** | Records calls, runs real code | `jest.spyOn(service, 'save')` |
| **Mock** | Verifies interactions | `expect(mock).toHaveBeenCalledWith(...)` |
| **Fake** | Working implementation | In-memory database |

## Patterns by Language

### JavaScript (Jest)

```javascript
// Stub external dependency
jest.mock('./database');
const db = require('./database');
db.getUser.mockResolvedValue({ id: 1, name: 'Test' });

// Spy on method
const spy = jest.spyOn(console, 'log');
doSomething();
expect(spy).toHaveBeenCalledWith('expected message');

// Mock module partially
jest.mock('./utils', () => ({
  ...jest.requireActual('./utils'),
  sendEmail: jest.fn(),
}));
```

### Python (pytest + unittest.mock)

```python
from unittest.mock import Mock, patch, MagicMock

# Patch external dependency
@patch('mymodule.requests.get')
def test_fetch(mock_get):
    mock_get.return_value.json.return_value = {'data': 'test'}
    result = fetch_data()
    assert result == {'data': 'test'}

# Mock with spec (catches typos)
mock_user = Mock(spec=User)
mock_user.name = 'Test'

# Context manager
with patch('mymodule.send_email') as mock_send:
    mock_send.return_value = True
    result = process_order()
    mock_send.assert_called_once()
```

### Go (testify/mock or interfaces)

```go
// Interface-based mocking
type UserRepository interface {
    GetUser(ctx context.Context, id string) (*User, error)
}

type MockUserRepo struct {
    mock.Mock
}

func (m *MockUserRepo) GetUser(ctx context.Context, id string) (*User, error) {
    args := m.Called(ctx, id)
    return args.Get(0).(*User), args.Error(1)
}

func TestGetUser(t *testing.T) {
    mockRepo := new(MockUserRepo)
    mockRepo.On("GetUser", mock.Anything, "123").Return(&User{Name: "Test"}, nil)

    service := NewUserService(mockRepo)
    user, err := service.GetUser(context.Background(), "123")

    assert.NoError(t, err)
    assert.Equal(t, "Test", user.Name)
    mockRepo.AssertExpectations(t)
}
```

## Anti-Patterns

```javascript
// ❌ Mocking implementation details
jest.spyOn(service, 'privateHelper');  // Brittle

// ❌ Asserting on mocks instead of behavior
expect(mockDb.save).toHaveBeenCalled();  // Doesn't verify correctness

// ❌ Mocking everything
const result = service.process(mockA, mockB, mockC);  // What are you testing?

// ✅ Test behavior, not implementation
const result = service.createUser({ name: 'Test' });
expect(result.id).toBeDefined();
expect(await db.getUser(result.id)).toEqual(result);
```

## Dependency Injection for Testability

```typescript
// ❌ Hard to test - creates its own dependencies
class UserService {
  private db = new Database();
  async getUser(id: string) {
    return this.db.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}

// ✅ Easy to test - dependencies injected
class UserService {
  constructor(private db: Database) {}
  async getUser(id: string) {
    return this.db.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}

// Test
const mockDb = { query: jest.fn().mockResolvedValue([{ id: '1' }]) };
const service = new UserService(mockDb);
```
