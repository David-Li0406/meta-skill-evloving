---
id: mocking-strategies
name: "Mocking Strategies"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Mocking Strategies

## Overview

Mocking strategies involve using test doubles to isolate code under test from its dependencies. This includes stubs, mocks, spies, and fakes, each serving different purposes in testing scenarios.

## When to Use

- Isolating unit tests from external dependencies
- Testing error handling and edge cases
- Verifying interactions between components
- Speeding up tests by avoiding slow operations
- Testing code that depends on time, randomness, or network

## Key Principles

- **Mock at boundaries**: Mock external systems, not internal classes
- **Prefer state over interaction testing**: Test results, not method calls
- **Use the right double**: Stub for state, mock for behavior verification
- **Keep mocks simple**: Complex mocks indicate design problems
- **Avoid over-mocking**: If everything is mocked, what are you testing?

## Best Practices

### Types of Test Doubles

```
┌─────────────────────────────────────────────────────────────┐
│                    TEST DOUBLES                             │
├─────────────────────────────────────────────────────────────┤
│ DUMMY   │ Passed but never used (fill parameter lists)     │
├─────────────────────────────────────────────────────────────┤
│ STUB    │ Returns canned responses (test state)            │
├─────────────────────────────────────────────────────────────┤
│ SPY     │ Records calls for later verification             │
├─────────────────────────────────────────────────────────────┤
│ MOCK    │ Pre-programmed with expectations (verify calls)  │
├─────────────────────────────────────────────────────────────┤
│ FAKE    │ Working implementation (simpler than production) │
└─────────────────────────────────────────────────────────────┘
```

### Python unittest.mock

```python
from unittest.mock import Mock, MagicMock, patch, AsyncMock
import pytest

# STUB - Returns canned responses
def test_with_stub():
    # Create stub that returns specific values
    user_repo = Mock()
    user_repo.find_by_id.return_value = User(id="123", name="John")

    service = UserService(user_repo)
    result = service.get_user("123")

    assert result.name == "John"

# MOCK - Verifies interactions
def test_with_mock():
    notifier = Mock()
    service = OrderService(notifier=notifier)

    service.place_order(order_id="order-123")

    # Verify the interaction happened
    notifier.send_notification.assert_called_once_with(
        "order-123",
        "Your order has been placed"
    )

# SPY - Wraps real object
def test_with_spy():
    real_calculator = Calculator()
    spy = Mock(wraps=real_calculator)

    result = spy.add(2, 3)

    assert result == 5  # Real behavior
    spy.add.assert_called_with(2, 3)  # Verify call

# Multiple return values
def test_sequence_of_returns():
    mock = Mock()
    mock.get_next.side_effect = [1, 2, 3, StopIteration()]

    assert mock.get_next() == 1
    assert mock.get_next() == 2
    assert mock.get_next() == 3
    with pytest.raises(StopIteration):
        mock.get_next()

# Conditional returns
def test_conditional_returns():
    mock = Mock()

    def side_effect_func(arg):
        if arg == "valid":
            return {"status": "ok"}
        raise ValueError("Invalid input")

    mock.process.side_effect = side_effect_func

    assert mock.process("valid") == {"status": "ok"}
    with pytest.raises(ValueError):
        mock.process("invalid")
```

### Patching

```python
from unittest.mock import patch, MagicMock

# Patch as decorator
@patch('mymodule.external_api.fetch_data')
def test_with_patched_api(mock_fetch):
    mock_fetch.return_value = {"data": "test"}

    result = process_data()

    assert result == "processed: test"

# Patch as context manager
def test_with_context_manager():
    with patch('mymodule.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 15, 10, 30)

        result = get_current_timestamp()

        assert result == "2024-01-15 10:30:00"

# Patch multiple things
@patch('mymodule.send_email')
@patch('mymodule.save_to_database')
def test_with_multiple_patches(mock_save, mock_email):
    # Note: decorators are applied bottom-up
    mock_save.return_value = {"id": "123"}

    result = create_user({"email": "test@example.com"})

    mock_save.assert_called_once()
    mock_email.assert_called_once()

# Patch object attribute
def test_patch_object():
    with patch.object(UserService, 'validate', return_value=True):
        service = UserService()
        result = service.create_user({"name": "Test"})
        assert result is not None

# Patch dict
def test_patch_dict():
    with patch.dict('os.environ', {'API_KEY': 'test-key'}):
        config = load_config()
        assert config['api_key'] == 'test-key'
```

### Async Mocking

```python
from unittest.mock import AsyncMock, patch
import pytest

@pytest.mark.asyncio
async def test_async_mock():
    # AsyncMock for async functions
    mock_client = AsyncMock()
    mock_client.fetch_user.return_value = {"id": "123", "name": "John"}

    service = AsyncUserService(mock_client)
    result = await service.get_user("123")

    assert result["name"] == "John"
    mock_client.fetch_user.assert_awaited_once_with("123")

@pytest.mark.asyncio
async def test_async_side_effect():
    mock = AsyncMock()

    async def async_side_effect(user_id):
        if user_id == "valid":
            return {"id": user_id}
        raise UserNotFoundError()

    mock.find.side_effect = async_side_effect

    result = await mock.find("valid")
    assert result["id"] == "valid"

    with pytest.raises(UserNotFoundError):
        await mock.find("invalid")

# Patching async methods
@pytest.mark.asyncio
@patch('mymodule.aiohttp.ClientSession.get', new_callable=AsyncMock)
async def test_http_client(mock_get):
    mock_response = AsyncMock()
    mock_response.json.return_value = {"data": "test"}
    mock_get.return_value.__aenter__.return_value = mock_response

    result = await fetch_api_data()

    assert result == {"data": "test"}
```

### Fake Implementations

```python
from typing import Optional, Dict
from abc import ABC, abstractmethod

# Interface
class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

# Fake implementation for testing
class FakeUserRepository(UserRepository):
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.email_index: Dict[str, str] = {}

    def save(self, user: User) -> User:
        if not user.id:
            user.id = str(uuid4())
        self.users[user.id] = user
        self.email_index[user.email] = user.id
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        user_id = self.email_index.get(email)
        return self.users.get(user_id) if user_id else None

    def clear(self):
        self.users.clear()
        self.email_index.clear()

# Using fake in tests
@pytest.fixture
def fake_repo():
    return FakeUserRepository()

def test_user_registration(fake_repo):
    service = UserService(fake_repo)

    result = service.register(email="new@example.com", name="New User")

    assert result.id is not None
    assert fake_repo.find_by_email("new@example.com") is not None

def test_duplicate_email_rejected(fake_repo):
    fake_repo.save(User(email="exists@example.com", name="Existing"))
    service = UserService(fake_repo)

    with pytest.raises(DuplicateEmailError):
        service.register(email="exists@example.com", name="Duplicate")
```

### TypeScript/Jest Mocking

```typescript
import { jest, describe, it, expect, beforeEach } from '@jest/globals';

// Auto-mock entire module
jest.mock('../services/emailService');
import { EmailService } from '../services/emailService';

// Manual mock
const mockUserRepository = {
  save: jest.fn(),
  findById: jest.fn(),
  findByEmail: jest.fn(),
};

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    jest.clearAllMocks();
    service = new UserService(mockUserRepository as any);
  });

  it('should create user and return with id', async () => {
    // Arrange
    const userData = { email: 'test@example.com', name: 'Test' };
    mockUserRepository.save.mockResolvedValue({ id: '123', ...userData });

    // Act
    const result = await service.createUser(userData);

    // Assert
    expect(result.id).toBe('123');
    expect(mockUserRepository.save).toHaveBeenCalledWith(
      expect.objectContaining({ email: 'test@example.com' })
    );
  });

  it('should throw on duplicate email', async () => {
    mockUserRepository.findByEmail.mockResolvedValue({ id: 'existing' });

    await expect(
      service.createUser({ email: 'exists@example.com', name: 'Test' })
    ).rejects.toThrow('Email already registered');
  });
});

// Spy on real implementation
describe('Calculator', () => {
  it('should spy on method calls', () => {
    const calculator = new Calculator();
    const addSpy = jest.spyOn(calculator, 'add');

    const result = calculator.add(2, 3);

    expect(result).toBe(5);
    expect(addSpy).toHaveBeenCalledWith(2, 3);
  });

  it('should mock method while preserving others', () => {
    const calculator = new Calculator();
    jest.spyOn(calculator, 'add').mockReturnValue(100);

    expect(calculator.add(2, 3)).toBe(100);  // Mocked
    expect(calculator.multiply(2, 3)).toBe(6);  // Real
  });
});

// Mock timers
describe('Scheduler', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('should execute callback after delay', () => {
    const callback = jest.fn();
    const scheduler = new Scheduler();

    scheduler.scheduleAfter(callback, 5000);

    expect(callback).not.toHaveBeenCalled();

    jest.advanceTimersByTime(5000);

    expect(callback).toHaveBeenCalledTimes(1);
  });
});
```

### Mocking HTTP Requests

```python
import pytest
import responses
import httpx
from pytest_httpx import HTTPXMock

# Using responses library (requests)
@responses.activate
def test_api_client_with_responses():
    responses.add(
        responses.GET,
        "https://api.example.com/users/123",
        json={"id": "123", "name": "John"},
        status=200
    )

    client = APIClient("https://api.example.com")
    result = client.get_user("123")

    assert result["name"] == "John"
    assert len(responses.calls) == 1

# Using pytest-httpx (httpx/async)
@pytest.mark.asyncio
async def test_async_api_client(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://api.example.com/users/123",
        json={"id": "123", "name": "John"}
    )

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/users/123")

    assert response.json()["name"] == "John"

# Mock error responses
@responses.activate
def test_api_error_handling():
    responses.add(
        responses.GET,
        "https://api.example.com/users/invalid",
        json={"error": "User not found"},
        status=404
    )

    client = APIClient("https://api.example.com")

    with pytest.raises(UserNotFoundError):
        client.get_user("invalid")
```

### Mocking Time and Randomness

```python
from unittest.mock import patch
from datetime import datetime
import random

# Mock datetime
def test_time_based_logic():
    with patch('mymodule.datetime') as mock_dt:
        # Fixed time for testing
        mock_dt.now.return_value = datetime(2024, 1, 15, 10, 30, 0)
        mock_dt.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

        result = generate_timestamp()

        assert result == "2024-01-15T10:30:00"

# Using freezegun
from freezegun import freeze_time

@freeze_time("2024-01-15 10:30:00")
def test_with_frozen_time():
    assert datetime.now() == datetime(2024, 1, 15, 10, 30, 0)

    # Time stays frozen throughout the test
    result = calculate_age(birth_date=datetime(1990, 1, 15))
    assert result == 34

# Mock random
def test_random_selection():
    with patch('random.choice') as mock_choice:
        mock_choice.return_value = "selected_item"

        result = pick_random_winner(["a", "b", "c"])

        assert result == "selected_item"

# Seed random for deterministic tests
def test_with_seeded_random():
    random.seed(42)

    results = [random.randint(1, 100) for _ in range(5)]

    # Same seed = same sequence
    assert results == [82, 15, 4, 95, 36]
```

### MagicMock for Dunder Methods

```python
from unittest.mock import MagicMock

def test_magic_mock_features():
    mock = MagicMock()

    # Supports iteration
    mock.__iter__.return_value = iter([1, 2, 3])
    assert list(mock) == [1, 2, 3]

    # Supports context manager
    mock.__enter__.return_value = "entered"
    with mock as m:
        assert m == "entered"

    # Supports len
    mock.__len__.return_value = 5
    assert len(mock) == 5

    # Supports indexing
    mock.__getitem__.return_value = "item"
    assert mock[0] == "item"

# Mock file operations
def test_file_processing():
    mock_file = MagicMock()
    mock_file.read.return_value = "file content"
    mock_file.__enter__.return_value = mock_file

    with patch('builtins.open', return_value=mock_file):
        result = read_config_file("config.json")

    assert result == "file content"
```

## Anti-patterns

- **Over-mocking**: Mocking everything including the code under test
- **Mocking internal details**: Tests break on refactoring
- **Complex mock setups**: Indicates design problems
- **Verify every call**: Testing implementation, not behavior
- **Mock data structures**: Use real data structures
- **Not resetting mocks**: State leaking between tests

## References

- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-mock](https://pytest-mock.readthedocs.io/)
- [Jest Mock Functions](https://jestjs.io/docs/mock-functions)
- [Mocks Aren't Stubs - Martin Fowler](https://martinfowler.com/articles/mocksArentStubs.html)
