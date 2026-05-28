---
name: test
description: Generate unit tests, integration tests, and test data. Use when writing tests, improving test coverage, or creating test scenarios.
allowed-tools: Read, Write, Bash, Grep
---

# Test Generation Skill

Generate comprehensive tests for your code.

## 1. Unit Test Generation

**Python (pytest):**
```python
import pytest
from mymodule import function_to_test

class TestFunctionName:
    def test_normal_case(self):
        result = function_to_test("input")
        assert result == "expected"

    def test_edge_case_empty(self):
        result = function_to_test("")
        assert result == ""

    def test_edge_case_none(self):
        with pytest.raises(TypeError):
            function_to_test(None)

    def test_large_input(self):
        large_input = "x" * 10000
        result = function_to_test(large_input)
        assert len(result) > 0

    @pytest.mark.parametrize("input,expected", [
        ("test", "TEST"),
        ("hello", "HELLO"),
        ("123", "123"),
    ])
    def test_multiple_cases(self, input, expected):
        assert function_to_test(input) == expected
```

**JavaScript (Jest):**
```javascript
describe('functionToTest', () => {
    test('handles normal input', () => {
        const result = functionToTest('input');
        expect(result).toBe('expected');
    });

    test('handles empty string', () => {
        const result = functionToTest('');
        expect(result).toBe('');
    });

    test('throws on null', () => {
        expect(() => functionToTest(null)).toThrow(TypeError);
    });

    test.each([
        ['test', 'TEST'],
        ['hello', 'HELLO'],
        ['123', '123'],
    ])('transforms %s to %s', (input, expected) => {
        expect(functionToTest(input)).toBe(expected);
    });
});
```

## 2. Integration Tests

**API Integration Tests:**
```python
import pytest
import requests

class TestAPI:
    BASE_URL = "http://localhost:8000/api"

    def test_create_user(self):
        response = requests.post(
            f"{self.BASE_URL}/users",
            json={"name": "Test User", "email": "test@example.com"}
        )
        assert response.status_code == 201
        assert response.json()["name"] == "Test User"

    def test_get_user(self):
        response = requests.get(f"{self.BASE_URL}/users/1")
        assert response.status_code == 200
        assert "name" in response.json()

    def test_update_user(self):
        response = requests.put(
            f"{self.BASE_URL}/users/1",
            json={"name": "Updated Name"}
        )
        assert response.status_code == 200

    def test_delete_user(self):
        response = requests.delete(f"{self.BASE_URL}/users/1")
        assert response.status_code == 204
```

**Database Integration Tests:**
```python
import pytest
from sqlalchemy import create_engine
from myapp.models import User, db

@pytest.fixture
def test_db():
    engine = create_engine('sqlite:///:memory:')
    db.create_all()
    yield db
    db.drop_all()

def test_user_creation(test_db):
    user = User(name="Test", email="test@example.com")
    test_db.session.add(user)
    test_db.session.commit()

    assert user.id is not None
    assert User.query.count() == 1
```

## 3. Mock Data Generation

**Python Mocks:**
```python
from unittest.mock import Mock, patch, MagicMock

def test_with_mock():
    # Mock object
    mock_api = Mock()
    mock_api.get_data.return_value = {"status": "success"}

    result = function_that_uses_api(mock_api)
    mock_api.get_data.assert_called_once()

def test_with_patch():
    with patch('mymodule.external_api_call') as mock_call:
        mock_call.return_value = {"data": "mocked"}
        result = function_that_calls_api()
        assert result == "mocked"
```

**JavaScript Mocks:**
```javascript
const mockFn = jest.fn();
mockFn.mockReturnValue('mocked value');

jest.mock('./api', () => ({
    getData: jest.fn(() => Promise.resolve({ status: 'success' }))
}));

test('calls API correctly', async () => {
    const result = await functionThatUsesAPI();
    expect(api.getData).toHaveBeenCalledTimes(1);
    expect(result).toEqual({ status: 'success' });
});
```

## 4. Test Coverage

**Check Coverage:**
```bash
# Python
pytest --cov=myapp --cov-report=html tests/
coverage run -m pytest
coverage report
coverage html

# JavaScript
jest --coverage
npm test -- --coverage

# View coverage
open htmlcov/index.html  # Python
open coverage/index.html  # JavaScript
```

## 5. E2E Tests

**Playwright/Selenium:**
```python
from playwright.sync_api import sync_playwright

def test_login_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto('http://localhost:3000/login')
        page.fill('[name="email"]', 'test@example.com')
        page.fill('[name="password"]', 'password123')
        page.click('button[type="submit"]')

        page.wait_for_url('**/dashboard')
        assert page.title() == 'Dashboard'

        browser.close()
```

## 6. Test Data Factories

**Python Factory:**
```python
import factory
from myapp.models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker('name')
    email = factory.Faker('email')
    age = factory.Faker('random_int', min=18, max=100)

# Usage
user = UserFactory()
users = UserFactory.create_batch(10)
```

## 7. Test Utilities

**Setup and Teardown:**
```python
import pytest

@pytest.fixture(scope="function")
def setup_database():
    # Setup
    db.create_all()
    yield db
    # Teardown
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope="module")
def app_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
```

## 8. Test Categories

Generate tests for:

- **Happy Path**: Normal expected inputs
- **Edge Cases**: Empty, null, zero, max values
- **Error Cases**: Invalid inputs, exceptions
- **Boundary Conditions**: Min/max values
- **Security**: SQL injection, XSS attempts
- **Performance**: Large datasets, timeouts
- **Concurrency**: Race conditions, locks

## When to Use This Skill

Use `/test` when:
- Writing tests for new code
- Improving test coverage
- Creating test data
- Setting up test fixtures
- Generating test cases for edge cases
- Creating integration or E2E tests
