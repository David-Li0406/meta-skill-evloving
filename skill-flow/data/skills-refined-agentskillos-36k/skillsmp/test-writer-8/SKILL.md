---
name: test-writer
description: Write comprehensive tests for NutriProfile. Use this skill when creating unit tests, integration tests, or ensuring test coverage. Covers Vitest for frontend and pytest for backend with proper mocking and assertions.
allowed-tools: Read,Write,Edit,Grep,Glob,Bash
---

# NutriProfile Test Writer Skill

You are a testing expert for the NutriProfile application. This skill helps you write comprehensive tests with proper mocking, assertions, and coverage requirements.

## Testing Stack

### Frontend (React/TypeScript)
- **Test Runner**: Vitest
- **Testing Library**: React Testing Library
- **User Events**: @testing-library/user-event
- **Mocking**: Vitest vi.mock()
- **Coverage**: V8 provider

### Backend (Python/FastAPI)
- **Test Runner**: pytest
- **Async Testing**: pytest-asyncio
- **HTTP Testing**: httpx AsyncClient
- **Coverage**: pytest-cov
- **Fixtures**: conftest.py

## Frontend Testing

### Configuration Files
- `frontend/vitest.config.ts` - Vitest configuration
- `frontend/src/test/setup.ts` - Global test setup and mocks

### Coverage Thresholds
```typescript
// vitest.config.ts
coverage: {
  thresholds: {
    statements: 80,
    branches: 75,
    functions: 80,
    lines: 80
  }
}
```

### Required Mocks (setup.ts)

```typescript
// Mock i18next
vi.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (key: string, params?: Record<string, unknown>) => {
      if (params) {
        let result = key
        Object.entries(params).forEach(([param, value]) => {
          result = result.replace(`{{${param}}}`, String(value))
        })
        return result
      }
      return key
    },
  }),
}))

// Mock sonner toast
vi.mock('sonner', () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
    info: vi.fn(),
  },
}))

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))

// Mock ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))
```

### Test File Structure

```
frontend/src/
├── data/
│   └── __tests__/
│       └── nutritionReference.test.ts
├── components/
│   └── vision/
│       └── __tests__/
│           ├── EditFoodItemModal.test.tsx
│           └── EditFoodItemIntegration.test.tsx
└── test/
    └── setup.ts
```

### Writing Unit Tests

```typescript
// Example: nutritionReference.test.ts
import { describe, it, expect } from 'vitest'
import { calculateNutrition, searchFoods, normalizeFood } from '../nutritionReference'

describe('calculateNutrition', () => {
  it('calcule correctement pour un aliment connu', () => {
    const result = calculateNutrition('riz', 100, 'g')

    expect(result.calories).toBe(130)
    expect(result.protein).toBe(2.7)
    expect(result.carbs).toBe(28)
    expect(result.fat).toBe(0.3)
  })

  it('applique le multiplicateur de portion', () => {
    const result = calculateNutrition('pâtes', 200, 'g')

    expect(result.calories).toBe(262)  // 131 * 2
  })

  it('retourne des valeurs par défaut pour aliment inconnu', () => {
    const result = calculateNutrition('aliment_inexistant', 100, 'g')

    expect(result.calories).toBe(100)
    expect(result.protein).toBe(5)
  })
})

describe('searchFoods', () => {
  it('trouve les aliments correspondants', () => {
    const results = searchFoods('pa', 5)

    expect(results).toContain('pâtes')
    expect(results).toContain('pain')
    expect(results.length).toBeLessThanOrEqual(5)
  })

  it('est insensible à la casse', () => {
    expect(searchFoods('riz')).toEqual(searchFoods('RIZ'))
  })
})
```

### Writing Component Tests

```typescript
// Example: EditFoodItemModal.test.tsx
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { EditFoodItemModal } from '../EditFoodItemModal'

describe('EditFoodItemModal', () => {
  const defaultProps = {
    item: { name: 'riz', quantity: '200', unit: 'g' },
    onClose: vi.fn(),
    onSave: vi.fn(),
    isLoading: false,
  }

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('affiche les valeurs initiales', () => {
    render(<EditFoodItemModal {...defaultProps} />)

    expect(screen.getByDisplayValue('riz')).toBeInTheDocument()
    expect(screen.getByDisplayValue('200')).toBeInTheDocument()
  })

  it('appelle onSave avec les données modifiées', async () => {
    const user = userEvent.setup()

    render(<EditFoodItemModal {...defaultProps} />)

    const nameInput = screen.getByDisplayValue('riz')
    await user.clear(nameInput)
    await user.type(nameInput, 'pâtes')

    const saveButton = screen.getByText('result.edit.save')
    await user.click(saveButton)

    await waitFor(() => {
      expect(defaultProps.onSave).toHaveBeenCalledWith(
        expect.objectContaining({ name: 'pâtes' })
      )
    })
  })

  it('désactive le bouton save si nom vide', async () => {
    const user = userEvent.setup()

    render(<EditFoodItemModal {...defaultProps} />)

    const nameInput = screen.getByDisplayValue('riz')
    await user.clear(nameInput)

    const saveButton = screen.getByText('result.edit.save')
    expect(saveButton).toBeDisabled()
  })

  it('appelle onClose quand on clique cancel', async () => {
    const user = userEvent.setup()

    render(<EditFoodItemModal {...defaultProps} />)

    const cancelButton = screen.getByText('result.edit.cancel')
    await user.click(cancelButton)

    expect(defaultProps.onClose).toHaveBeenCalled()
  })
})
```

### Writing Integration Tests

```typescript
// Example: EditFoodItemIntegration.test.tsx
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { FoodLogCard } from '../FoodLogCard'
import { visionApi } from '@/services/visionApi'

vi.mock('@/services/visionApi', () => ({
  visionApi: {
    updateItem: vi.fn(),
    deleteItem: vi.fn(),
  },
}))

describe('EditFoodItemIntegration', () => {
  let queryClient: QueryClient

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    })
    vi.clearAllMocks()
  })

  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )

  it('met à jour un aliment via l\'API', async () => {
    const user = userEvent.setup()

    vi.mocked(visionApi.updateItem).mockResolvedValue({
      id: 1,
      name: 'pâtes',
      quantity: '150',
      unit: 'g',
      calories: 195,
    })

    render(
      <FoodLogCard
        log={{
          id: 1,
          meal_type: 'lunch',
          items: [{ id: 1, name: 'riz', quantity: '200', unit: 'g', calories: 260 }],
        }}
      />,
      { wrapper }
    )

    // Open edit modal
    const editButton = screen.getByRole('button', { name: /edit/i })
    await user.click(editButton)

    // Modify food
    const nameInput = screen.getByDisplayValue('riz')
    await user.clear(nameInput)
    await user.type(nameInput, 'pâtes')

    // Save
    const saveButton = screen.getByText('result.edit.save')
    await user.click(saveButton)

    await waitFor(() => {
      expect(visionApi.updateItem).toHaveBeenCalledWith(
        1,
        expect.objectContaining({ name: 'pâtes' })
      )
    })
  })
})
```

## Backend Testing

### Configuration
```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### Test Structure
```
backend/tests/
├── conftest.py         # Shared fixtures
├── test_auth.py
├── test_users.py
├── test_vision.py
├── test_recipes.py
├── test_coaching.py
└── test_subscriptions.py
```

### Fixtures (conftest.py)

```python
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.main import app
from app.database import get_db

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def db_session():
    # Create test database session
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with AsyncSession(engine) as session:
        yield session

@pytest.fixture
async def auth_headers(async_client):
    # Create test user and return auth headers
    response = await async_client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

### Backend Test Examples

```python
# test_vision.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_analyze_food_photo(async_client: AsyncClient, auth_headers: dict):
    response = await async_client.post(
        "/api/v1/vision/analyze",
        headers=auth_headers,
        json={
            "image_base64": "...",
            "meal_type": "lunch"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "detected_items" in data
    assert "total_calories" in data
    assert data["confidence_score"] >= 0

@pytest.mark.asyncio
async def test_get_food_logs(async_client: AsyncClient, auth_headers: dict):
    response = await async_client.get(
        "/api/v1/vision/logs",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_food_log(async_client: AsyncClient, auth_headers: dict):
    # First create a log
    create_response = await async_client.post(
        "/api/v1/vision/analyze",
        headers=auth_headers,
        json={"image_base64": "...", "meal_type": "lunch"}
    )
    log_id = create_response.json()["id"]

    # Update it
    update_response = await async_client.patch(
        f"/api/v1/vision/logs/{log_id}",
        headers=auth_headers,
        json={"user_corrections": [{"name": "riz", "quantity": 150}]}
    )

    assert update_response.status_code == 200
```

## Running Tests

### Frontend
```bash
cd frontend
npm test              # Run all tests
npm run test:watch    # Watch mode
npm run test:ui       # Vitest UI
npm run test:coverage # With coverage report
```

### Backend
```bash
cd backend
pytest                    # Run all tests
pytest -v                 # Verbose
pytest --cov              # With coverage
pytest tests/test_vision.py  # Specific file
pytest -k "test_analyze"  # By name pattern
```

## Best Practices

1. **Test naming**: Use French for describe/it blocks (consistency with i18n)
2. **Mock external services**: Always mock APIs, databases in unit tests
3. **Test edge cases**: Empty inputs, errors, boundary values
4. **Isolate tests**: Each test should be independent
5. **Use factories**: Create helper functions for test data
6. **Check coverage**: Aim for 80%+ on new code
7. **Test user flows**: Integration tests for critical paths

## Common Patterns

### Testing with React Query
```typescript
const wrapper = ({ children }) => (
  <QueryClientProvider client={new QueryClient()}>
    {children}
  </QueryClientProvider>
)

render(<MyComponent />, { wrapper })
```

### Testing async operations
```typescript
await waitFor(() => {
  expect(screen.getByText('Success')).toBeInTheDocument()
})
```

### Testing form validation
```typescript
await user.clear(input)
expect(submitButton).toBeDisabled()
```
