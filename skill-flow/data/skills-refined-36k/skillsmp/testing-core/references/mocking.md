# Mocking Patterns

## Python (unittest.mock)

### Basic Mock

```python
from unittest.mock import Mock, MagicMock

# Simple mock
mock = Mock()
mock.some_method.return_value = "result"
assert mock.some_method() == "result"

# Magic mock (supports magic methods)
mock = MagicMock()
mock.__len__.return_value = 5
assert len(mock) == 5
```

### Patch Decorator

```python
from unittest.mock import patch

# Patch module function
@patch("myapp.services.email.send_email")
def test_signup(mock_send):
    mock_send.return_value = True
    result = signup("test@example.com")
    mock_send.assert_called_once()

# Patch with return value
@patch("myapp.services.payment.charge", return_value={"id": "ch_123"})
def test_checkout(mock_charge):
    result = checkout(cart)
    assert result.payment_id == "ch_123"
```

### Patch Context Manager

```python
def test_with_context():
    with patch("myapp.external.api.fetch") as mock_fetch:
        mock_fetch.return_value = {"data": "test"}
        result = process_data()
        assert result == "test"
```

### Async Mock

```python
from unittest.mock import AsyncMock, patch

@patch("myapp.services.db.get_user", new_callable=AsyncMock)
async def test_async_function(mock_get):
    mock_get.return_value = User(id=1, name="Test")
    user = await get_user_profile(1)
    assert user.name == "Test"
```

### Mock Side Effects

```python
# Raise exception
mock.method.side_effect = ValueError("error")

# Return different values on each call
mock.method.side_effect = [1, 2, 3]
assert mock.method() == 1
assert mock.method() == 2

# Custom function
mock.method.side_effect = lambda x: x * 2
assert mock.method(5) == 10
```

### Assertions

```python
mock.method.assert_called()
mock.method.assert_called_once()
mock.method.assert_called_with("arg1", key="value")
mock.method.assert_called_once_with("arg1")
mock.method.assert_not_called()

# Call count
assert mock.method.call_count == 3

# All calls
mock.method.assert_has_calls([
    call("first"),
    call("second"),
])
```

## TypeScript (Vitest)

### Basic Mock

```typescript
import { vi, expect } from 'vitest';

// Mock function
const mockFn = vi.fn();
mockFn.mockReturnValue('result');
expect(mockFn()).toBe('result');

// Mock with implementation
const mockImpl = vi.fn((x: number) => x * 2);
expect(mockImpl(5)).toBe(10);
```

### Mock Module

```typescript
// Mock entire module
vi.mock('./email', () => ({
  sendEmail: vi.fn().mockResolvedValue(true),
}));

// Import after mocking
import { sendEmail } from './email';

test('sends email', async () => {
  await signup('test@example.com');
  expect(sendEmail).toHaveBeenCalledWith('test@example.com', expect.any(String));
});
```

### Spy

```typescript
import { vi } from 'vitest';

const user = {
  getName: () => 'John',
};

const spy = vi.spyOn(user, 'getName');
user.getName();

expect(spy).toHaveBeenCalled();
spy.mockRestore();
```

### Mock Return Values

```typescript
const mock = vi.fn();

// Static return
mock.mockReturnValue('static');

// Different returns per call
mock.mockReturnValueOnce('first').mockReturnValueOnce('second');

// Async
mock.mockResolvedValue('async result');
mock.mockRejectedValue(new Error('fail'));
```

### Reset Mocks

```typescript
import { beforeEach, vi } from 'vitest';

beforeEach(() => {
  vi.clearAllMocks();    // Clear call history
  vi.resetAllMocks();    // Clear history + implementations
  vi.restoreAllMocks();  // Restore original implementations
});
```

## Rust (mockall)

```rust
use mockall::automock;

#[automock]
trait Database {
    fn get_user(&self, id: i32) -> Option<User>;
}

#[test]
fn test_with_mock() {
    let mut mock = MockDatabase::new();
    mock.expect_get_user()
        .with(eq(1))
        .times(1)
        .returning(|_| Some(User { id: 1, name: "Test".into() }));

    let result = get_user_profile(&mock, 1);
    assert_eq!(result.name, "Test");
}
```

## When NOT to Mock

```
❌ Don't mock:
- The code under test
- Pure functions
- Simple data objects
- Standard library
- Things easily instantiated

✅ Do mock:
- External HTTP APIs
- Database (for unit tests)
- File system
- Time/randomness
- Email/SMS services
- Payment processors
```
