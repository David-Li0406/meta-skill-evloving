# Test Framework Guides

Framework-specific testing guidance and configuration.

## JavaScript/TypeScript

### Jest Configuration
```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src', '<rootDir>/tests'],
  testMatch: ['**/*.test.ts', '**/*.spec.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/index.ts'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  }
};
```

### Jest Common Patterns
```typescript
// Async testing
test('fetches data', async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});

// Error testing
test('throws on invalid input', () => {
  expect(() => validateInput(null)).toThrow('Input required');
});

// Async error testing
test('rejects with error', async () => {
  await expect(asyncOperation()).rejects.toThrow('Failed');
});

// Mock modules
jest.mock('./database', () => ({
  query: jest.fn().mockResolvedValue([{ id: 1 }])
}));

// Mock timers
jest.useFakeTimers();
test('debounces calls', () => {
  const callback = jest.fn();
  const debounced = debounce(callback, 1000);

  debounced();
  debounced();
  debounced();

  expect(callback).not.toHaveBeenCalled();

  jest.advanceTimersByTime(1000);

  expect(callback).toHaveBeenCalledTimes(1);
});
```

### Vitest Configuration
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['**/*.{test,spec}.{js,ts}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: ['node_modules/', 'tests/']
    },
    setupFiles: ['./tests/setup.ts']
  }
});
```

### React Testing Library
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('submits form with user input', async () => {
  const onSubmit = jest.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  // Query by role (preferred)
  await userEvent.type(screen.getByRole('textbox', { name: /email/i }), 'test@example.com');
  await userEvent.type(screen.getByLabelText(/password/i), 'password123');
  await userEvent.click(screen.getByRole('button', { name: /submit/i }));

  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
  });
});

// Testing async state changes
test('shows loading then data', async () => {
  render(<UserList />);

  expect(screen.getByText(/loading/i)).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });

  expect(screen.getByRole('list')).toBeInTheDocument();
});
```

## Python

### pytest Configuration
```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
filterwarnings =
    ignore::DeprecationWarning
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --cov=src --cov-report=term-missing"
testpaths = ["tests"]

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError"
]
```

### pytest Patterns
```python
import pytest
from unittest.mock import Mock, patch, AsyncMock

# Fixtures
@pytest.fixture
def user():
    return User(id=1, name="Test User")

@pytest.fixture
def db_session():
    session = create_test_session()
    yield session
    session.rollback()
    session.close()

# Parameterized tests
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
])
def test_uppercase(input, expected):
    assert uppercase(input) == expected

# Exception testing
def test_raises_on_invalid():
    with pytest.raises(ValueError, match="must be positive"):
        calculate(-1)

# Async testing
@pytest.mark.asyncio
async def test_async_fetch():
    result = await fetch_data()
    assert result is not None

# Mocking
def test_with_mock(mocker):
    mock_api = mocker.patch('module.api_call')
    mock_api.return_value = {"status": "ok"}

    result = process_data()

    mock_api.assert_called_once()
    assert result["status"] == "ok"

# Context manager mock
def test_file_processing():
    with patch('builtins.open', mock_open(read_data='test content')):
        result = read_file('test.txt')
        assert result == 'test content'
```

### pytest-django
```python
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_create_user(client):
    response = client.post(reverse('user-create'), {
        'username': 'testuser',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
    assert User.objects.filter(username='testuser').exists()

@pytest.fixture
def authenticated_client(client, django_user_model):
    user = django_user_model.objects.create_user(
        username='testuser',
        password='testpass'
    )
    client.force_login(user)
    return client
```

## Go

### Go Test Basics
```go
package user

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestCreateUser(t *testing.T) {
    // Arrange
    input := CreateUserInput{Name: "Test", Email: "test@example.com"}

    // Act
    user, err := CreateUser(input)

    // Assert
    require.NoError(t, err)
    assert.Equal(t, "Test", user.Name)
    assert.NotEmpty(t, user.ID)
}

// Table-driven tests
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid email", "test@example.com", false},
        {"missing @", "testexample.com", true},
        {"empty", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}

// Subtests with setup/teardown
func TestUserService(t *testing.T) {
    db := setupTestDB(t)
    defer db.Close()

    svc := NewUserService(db)

    t.Run("Create", func(t *testing.T) {
        user, err := svc.Create("test@example.com")
        require.NoError(t, err)
        assert.NotEmpty(t, user.ID)
    })

    t.Run("Get", func(t *testing.T) {
        // ...
    })
}
```

### Go Mocking with mockgen
```go
//go:generate mockgen -source=repository.go -destination=mocks/repository_mock.go

type UserRepository interface {
    FindByID(id string) (*User, error)
    Save(user *User) error
}

// In test file
func TestUserService_GetUser(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRepo := mocks.NewMockUserRepository(ctrl)
    mockRepo.EXPECT().
        FindByID("user-1").
        Return(&User{ID: "user-1", Name: "Test"}, nil)

    svc := NewUserService(mockRepo)
    user, err := svc.GetUser("user-1")

    assert.NoError(t, err)
    assert.Equal(t, "Test", user.Name)
}
```

### Go Coverage
```bash
# Run with coverage
go test -cover ./...

# Generate coverage profile
go test -coverprofile=coverage.out ./...

# View HTML report
go tool cover -html=coverage.out

# Check coverage percentage
go tool cover -func=coverage.out | grep total
```

## Playwright (E2E)

### Configuration
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html'], ['list']],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'] } },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Playwright Patterns
```typescript
import { test, expect } from '@playwright/test';

test.describe('User Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
  });

  test('displays user name', async ({ page }) => {
    await expect(page.locator('.user-name')).toContainText('Test User');
  });

  test('navigates to settings', async ({ page }) => {
    await page.click('text=Settings');
    await expect(page).toHaveURL('/settings');
  });
});

// API testing with Playwright
test('API returns user data', async ({ request }) => {
  const response = await request.get('/api/users/1');
  expect(response.ok()).toBeTruthy();

  const user = await response.json();
  expect(user).toHaveProperty('id', 1);
});

// Visual comparison
test('homepage matches snapshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png');
});
```

## Cypress

### Configuration
```javascript
// cypress.config.js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    specPattern: 'cypress/e2e/**/*.cy.{js,ts}',
    supportFile: 'cypress/support/e2e.js',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,
    retries: {
      runMode: 2,
      openMode: 0
    }
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite'
    }
  }
});
```

### Cypress Patterns
```javascript
describe('Login Flow', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('logs in successfully', () => {
    cy.get('[data-cy=email]').type('test@example.com');
    cy.get('[data-cy=password]').type('password123');
    cy.get('[data-cy=submit]').click();

    cy.url().should('include', '/dashboard');
    cy.get('[data-cy=welcome]').should('contain', 'Welcome');
  });

  it('shows error for invalid credentials', () => {
    cy.get('[data-cy=email]').type('wrong@example.com');
    cy.get('[data-cy=password]').type('wrongpassword');
    cy.get('[data-cy=submit]').click();

    cy.get('[data-cy=error]').should('be.visible');
  });
});

// Custom commands
// cypress/support/commands.js
Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('[data-cy=email]').type(email);
    cy.get('[data-cy=password]').type(password);
    cy.get('[data-cy=submit]').click();
    cy.url().should('include', '/dashboard');
  });
});

// Usage
it('accesses protected page', () => {
  cy.login('test@example.com', 'password123');
  cy.visit('/protected');
  cy.get('h1').should('contain', 'Protected Content');
});

// API stubbing
it('handles API error gracefully', () => {
  cy.intercept('GET', '/api/users', {
    statusCode: 500,
    body: { error: 'Server error' }
  });

  cy.visit('/users');
  cy.get('[data-cy=error-message]').should('contain', 'Failed to load');
});
```

## CI Integration

### GitHub Actions
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
```

### Pre-commit Hook for Tests
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run affected tests only
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACMR | grep -E '\.(js|ts)$')

if [ -n "$CHANGED_FILES" ]; then
  npm test -- --findRelatedTests $CHANGED_FILES --passWithNoTests
fi
```
