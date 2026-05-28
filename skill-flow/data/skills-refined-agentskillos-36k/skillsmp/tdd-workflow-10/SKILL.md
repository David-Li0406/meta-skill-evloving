---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests.
---

# Test-Driven Development Workflow

This skill ensures all code development follows TDD principles with comprehensive test coverage.

## When to Activate

- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints
- Creating new components

## Core Principles

### 1. Tests BEFORE Code
ALWAYS write tests first, then implement code to make tests pass.

### 2. Coverage Requirements
- Minimum 80% coverage (unit + integration + E2E)
- All edge cases covered
- Error scenarios tested
- Boundary conditions verified

### 3. Test Types

#### Unit Tests
- Individual functions and utilities
- Component logic
- Pure functions
- Helpers and utilities

#### Integration Tests
- API endpoints
- Database operations
- Service interactions
- External API calls

#### E2E Tests (Playwright)
- Critical user flows
- Complete workflows
- Browser automation
- UI interactions

## TDD Workflow Steps

### Step 1: Write User Journeys
```
As a [role], I want to [action], so that [benefit]

Example:
As a user, I want to search for markets semantically,
so that I can find relevant markets even without exact keywords.
```

### Step 2: Generate Test Cases
For each user journey, create comprehensive test cases:

```python
import pytest

class TestSemanticSearch:
    @pytest.mark.asyncio
    async def test_returns_relevant_markets_for_query(self):
        # Test implementation
        pass

    @pytest.mark.asyncio
    async def test_handles_empty_query_gracefully(self):
        # Test edge case
        pass

    @pytest.mark.asyncio
    async def test_falls_back_to_substring_search_when_redis_unavailable(self):
        # Test fallback behavior
        pass

    @pytest.mark.asyncio
    async def test_sorts_results_by_similarity_score(self):
        # Test sorting logic
        pass
```

### Step 3: Run Tests (They Should Fail)
```bash
pytest tests/
# Tests should fail - we haven't implemented yet
```

### Step 4: Implement Code
Write minimal code to make tests pass:

```python
# Implementation guided by tests
async def search_markets(query: str) -> list[dict]:
    # Implementation here
    pass
```

### Step 5: Run Tests Again
```bash
pytest tests/
# Tests should now pass
```

### Step 6: Refactor
Improve code quality while keeping tests green:
- Remove duplication
- Improve naming
- Optimize performance
- Enhance readability

### Step 7: Verify Coverage
```bash
pytest tests/ --cov=. --cov-report=html
# Verify 80%+ coverage achieved
```

## Testing Patterns

### Unit Test Pattern (pytest)
```python
import pytest
from unittest.mock import Mock, patch
from app.services.button_service import ButtonService

class TestButtonService:
    def test_renders_with_correct_text(self):
        button = ButtonService(text='Click me')
        assert button.text == 'Click me'

    def test_calls_on_click_when_clicked(self):
        handle_click = Mock()
        button = ButtonService(on_click=handle_click, text='Click')

        button.click()

        handle_click.assert_called_once()

    def test_is_disabled_when_disabled_prop_is_true(self):
        button = ButtonService(disabled=True, text='Click')
        assert button.disabled is True
```

### API Integration Test Pattern
```python
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

app = FastAPI()

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac

class TestGetMarkets:
    @pytest.mark.asyncio
    async def test_returns_markets_successfully(self, client: AsyncClient):
        response = await client.get('/api/markets')
        data = response.json()

        assert response.status_code == 200
        assert data['success'] is True
        assert isinstance(data['data'], list)

    @pytest.mark.asyncio
    async def test_validates_query_parameters(self, client: AsyncClient):
        response = await client.get('/api/markets?limit=invalid')
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_handles_database_errors_gracefully(self, client: AsyncClient):
        # Mock database failure
        with patch('app.database.get_markets', side_effect=Exception('DB Error')):
            response = await client.get('/api/markets')
            # Test error handling
            assert response.status_code == 500
```

### E2E Test Pattern (Playwright)
```python
from playwright.async_api import Page, expect
import pytest

@pytest.mark.asyncio
async def test_user_can_search_and_filter_markets(page: Page):
    # Navigate to markets page
    await page.goto('/')
    await page.click('a[href="/markets"]')

    # Verify page loaded
    await expect(page.locator('h1')).to_contain_text('Markets')

    # Search for markets
    await page.fill('input[placeholder="Search markets"]', 'election')

    # Wait for debounce and results
    await page.wait_for_timeout(600)

    # Verify search results displayed
    results = page.locator('[data-testid="market-card"]')
    await expect(results).to_have_count(5, timeout=5000)

    # Verify results contain search term
    first_result = results.first
    await expect(first_result).to_contain_text('election', ignore_case=True)

    # Filter by status
    await page.click('button:has-text("Active")')

    # Verify filtered results
    await expect(results).to_have_count(3)

@pytest.mark.asyncio
async def test_user_can_create_new_market(page: Page):
    # Login first
    await page.goto('/creator-dashboard')

    # Fill market creation form
    await page.fill('input[name="name"]', 'Test Market')
    await page.fill('textarea[name="description"]', 'Test description')
    await page.fill('input[name="endDate"]', '2025-12-31')

    # Submit form
    await page.click('button[type="submit"]')

    # Verify success message
    await expect(page.locator('text=Market created successfully')).to_be_visible()

    # Verify redirect to market page
    await expect(page).to_have_url(r'/markets/test-market/')
```

## Test File Organization

```
project/
├── app/
│   ├── services/
│   │   ├── button_service.py
│   │   └── test_button_service.py      # Unit tests
│   └── api/
│       └── markets/
│           ├── route.py
│           └── test_route.py            # Integration tests
└── tests/
    ├── e2e/
    │   ├── test_markets.py              # E2E tests
    │   ├── test_trading.py
    │   └── test_auth.py
    └── conftest.py                      # Shared fixtures
```

## Mocking External Services

### Database Mock
```python
from unittest.mock import Mock, patch
import pytest

@pytest.fixture
def mock_supabase():
    mock_client = Mock()
    mock_client.from.return_value.select.return_value.eq.return_value = {
        'data': [{'id': 1, 'name': 'Test Market'}],
        'error': None
    }
    return mock_client

def test_with_mock_supabase(mock_supabase):
    with patch('app.database.supabase', mock_supabase):
        # Test implementation
        pass
```

### Redis Mock
```python
from unittest.mock import Mock, patch

@pytest.fixture
def mock_redis():
    mock_redis_client = Mock()
    mock_redis_client.search_markets_by_vector.return_value = [
        {'slug': 'test-market', 'similarity_score': 0.95}
    ]
    mock_redis_client.check_redis_health.return_value = {'connected': True}
    return mock_redis_client

def test_with_mock_redis(mock_redis):
    with patch('app.services.redis_client', mock_redis):
        # Test implementation
        pass
```

### OpenAI Mock
```python
from unittest.mock import Mock, patch

@pytest.fixture
def mock_openai():
    mock_client = Mock()
    mock_client.generate_embedding.return_value = [0.1] * 1536  # Mock 1536-dim embedding
    return mock_client

def test_with_mock_openai(mock_openai):
    with patch('app.services.openai_client', mock_openai):
        # Test implementation
        pass
```

## Test Coverage Verification

### Run Coverage Report
```bash
pytest tests/ --cov=. --cov-report=html
```

### Coverage Thresholds
```ini
# pytest.ini or setup.cfg
[tool:pytest]
addopts = --cov=. --cov-report=html --cov-report=term-missing
[coverage:run]
source = app
[coverage:report]
fail_under = 80
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## Common Testing Mistakes to Avoid

### ❌ WRONG: Testing Implementation Details
```python
# Don't test internal state
assert component._count == 5
```

### ✅ CORRECT: Test User-Visible Behavior
```python
# Test what users see/experience
result = service.get_count_display()
assert 'Count: 5' in result
```

### ❌ WRONG: Brittle Selectors
```python
# Breaks easily
await page.click('.css-class-xyz')
```

### ✅ CORRECT: Semantic Selectors
```python
# Resilient to changes
await page.click('button:has-text("Submit")')
await page.click('[data-testid="submit-button"]')
```

### ❌ WRONG: No Test Isolation
```python
# Tests depend on each other
def test_creates_user():
    # Creates user in database
    pass

def test_updates_same_user():
    # Depends on previous test's user
    pass
```

### ✅ CORRECT: Independent Tests
```python
# Each test sets up its own data
@pytest.fixture
def test_user():
    return create_test_user()

def test_creates_user(test_user):
    # Test logic with isolated user
    pass

def test_updates_user(test_user):
    # Update logic with isolated user
    pass
```

## Continuous Testing

### Watch Mode During Development
```bash
pytest-watch
# Tests run automatically on file changes
```

### Pre-Commit Hook
```bash
# Runs before every commit
pytest tests/ && ruff check .
```

### CI/CD Integration
```yaml
# GitHub Actions
- name: Run Tests
  run: pytest tests/ --cov=. --cov-report=xml
- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

## Best Practices

1. **Write Tests First** - Always TDD
2. **One Assert Per Test** - Focus on single behavior
3. **Descriptive Test Names** - Explain what's tested
4. **Arrange-Act-Assert** - Clear test structure
5. **Mock External Dependencies** - Isolate unit tests
6. **Test Edge Cases** - Null, undefined, empty, large
7. **Test Error Paths** - Not just happy paths
8. **Keep Tests Fast** - Unit tests < 50ms each
9. **Clean Up After Tests** - No side effects
10. **Review Coverage Reports** - Identify gaps

## Success Metrics

- 80%+ code coverage achieved
- All tests passing (green)
- No skipped or disabled tests
- Fast test execution (< 30s for unit tests)
- E2E tests cover critical user flows
- Tests catch bugs before production

---

**Remember**: Tests are not optional. They are the safety net that enables confident refactoring, rapid development, and production reliability.
