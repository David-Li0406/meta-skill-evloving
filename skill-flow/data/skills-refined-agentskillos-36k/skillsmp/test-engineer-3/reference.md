# Test Engineer Reference

Comprehensive testing patterns for Faiston NEXO.

## Testing Philosophy

### Testing Pyramid

```
        /\
       /E2E\        ← Few: Critical user journeys
      /──────\
     /Integr.\      ← Some: Component + API
    /──────────\
   / Unit Tests \   ← Many: Functions, hooks
```

### Test Priorities

| Priority | Test Type | Examples |
|----------|-----------|----------|
| 1 | Unit | Utility functions, hooks, pure logic |
| 2 | Integration | Components with API calls |
| 3 | Component | User interactions, rendering |
| 4 | E2E | Login → Dashboard → AI features |

---

## Frontend Testing Patterns

### Component Test Structure

```typescript
// Pattern: Arrange-Act-Assert

describe("ComponentName", () => {
  // Default props fixture
  const defaultProps = {
    title: "Test",
    onClick: vi.fn(),
  };

  // Reset mocks between tests
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should render with correct content", () => {
    // Arrange
    render(<Component {...defaultProps} />);

    // Assert
    expect(screen.getByText("Test")).toBeInTheDocument();
  });

  it("should call onClick when clicked", async () => {
    // Arrange
    const user = userEvent.setup();
    render(<Component {...defaultProps} />);

    // Act
    await user.click(screen.getByRole("button"));

    // Assert
    expect(defaultProps.onClick).toHaveBeenCalledTimes(1);
  });
});
```

### Hook Test Structure

```typescript
import { renderHook, act } from "@testing-library/react";

describe("useCustomHook", () => {
  it("should return initial state", () => {
    const { result } = renderHook(() => useCustomHook());

    expect(result.current.value).toBe(0);
  });

  it("should update state when action called", () => {
    const { result } = renderHook(() => useCustomHook());

    act(() => {
      result.current.increment();
    });

    expect(result.current.value).toBe(1);
  });
});
```

### MSW Handler Patterns

```typescript
// handlers.ts - Default handlers
export const handlers = [
  // GET endpoint
  http.get("/api/posts", () => {
    return HttpResponse.json({
      posts: [{ id: "1", title: "Test Post" }],
    });
  }),

  // POST endpoint with validation
  http.post("/api/posts", async ({ request }) => {
    const body = await request.json();
    if (!body.title) {
      return HttpResponse.json(
        { error: "Title required" },
        { status: 400 }
      );
    }
    return HttpResponse.json({ id: "new", ...body }, { status: 201 });
  }),

  // Error simulation
  http.get("/api/error", () => {
    return HttpResponse.error();
  }),
];

// Override in specific test
server.use(
  http.get("/api/posts", () => {
    return HttpResponse.json({ posts: [] });
  })
);
```

### Query Client Test Setup

```typescript
// test-utils.tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

export function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,           // Don't retry in tests
        gcTime: Infinity,       // Don't garbage collect
        staleTime: Infinity,    // Don't refetch
      },
      mutations: {
        retry: false,
      },
    },
    logger: {
      log: console.log,
      warn: console.warn,
      error: () => {},          // Suppress error logs
    },
  });
}

export function renderWithProviders(
  ui: React.ReactElement,
  { queryClient = createTestQueryClient() } = {}
) {
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>
        <AuthProvider>
          {ui}
        </AuthProvider>
      </MemoryRouter>
    </QueryClientProvider>
  );
}
```

---

## Backend Testing Patterns

### pytest Fixtures

```python
# conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock

@pytest.fixture
def anyio_backend():
    """Use asyncio backend for async tests."""
    return "asyncio"

@pytest.fixture
async def client(app):
    """Async HTTP client for FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_dynamodb():
    """Mock DynamoDB table operations."""
    with patch("boto3.resource") as mock:
        table = MagicMock()
        mock.return_value.Table.return_value = table
        yield table

@pytest.fixture
def auth_headers():
    """Mock authentication headers."""
    return {"Authorization": "Bearer test-token"}
```

### Async Test Patterns

```python
import pytest

@pytest.mark.asyncio
async def test_async_endpoint(client):
    """Test async endpoint."""
    response = await client.get("/api/data")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_async_with_timeout(client):
    """Test with timeout."""
    import asyncio
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(
            client.get("/api/slow"),
            timeout=1.0
        )
```

### Mocking AWS Services

```python
# Mock S3
@pytest.fixture
def mock_s3():
    with patch("boto3.client") as mock:
        s3 = MagicMock()
        mock.return_value = s3
        s3.generate_presigned_url.return_value = "https://example.com/file"
        yield s3

# Mock Cognito
@pytest.fixture
def mock_cognito():
    with patch("boto3.client") as mock:
        cognito = MagicMock()
        mock.return_value = cognito
        cognito.get_user.return_value = {
            "Username": "test@example.com",
            "UserAttributes": [{"Name": "email", "Value": "test@example.com"}]
        }
        yield cognito
```

### Pydantic Model Testing

```python
import pytest
from pydantic import ValidationError
from server.models import PostCreate

def test_valid_model():
    """Test valid model creation."""
    post = PostCreate(title="Test", content="Content")
    assert post.title == "Test"

def test_invalid_model():
    """Test validation error on invalid data."""
    with pytest.raises(ValidationError) as exc_info:
        PostCreate(title="")  # Empty title

    errors = exc_info.value.errors()
    assert any(e["loc"] == ("title",) for e in errors)
```

---

## Agent Testing Patterns

### Mock Google ADK Components

```python
from unittest.mock import MagicMock, AsyncMock, patch

@pytest.fixture
def mock_agent():
    """Mock Agent class."""
    with patch("google.adk.agents.Agent") as mock:
        agent = MagicMock()
        mock.return_value = agent
        yield agent

@pytest.fixture
def mock_session_service():
    """Mock InMemorySessionService."""
    with patch("google.adk.sessions.InMemorySessionService") as mock:
        service = MagicMock()
        service.create_session = AsyncMock()
        mock.return_value = service
        yield service

@pytest.fixture
def mock_runner():
    """Mock Runner with async iteration."""
    with patch("google.adk.runners.Runner") as mock:
        runner = MagicMock()
        mock.return_value = runner

        async def mock_run_async(*args, **kwargs):
            event = MagicMock()
            event.is_final_response.return_value = True
            event.content = MagicMock()
            event.content.parts = [MagicMock(text='{"result": "success"}')]
            yield event

        runner.run_async = mock_run_async
        yield runner
```

### Testing Agent Output Parsing

```python
from server.agentcore.agents.utils import parse_json_safe, extract_json

def test_extract_json_from_markdown():
    """Test JSON extraction from markdown code block."""
    response = '''
    Here is the result:
    ```json
    {"flashcards": []}
    ```
    '''
    result = extract_json(response)
    assert result == '{"flashcards": []}'

def test_parse_json_safe_with_invalid():
    """Test safe parsing with invalid JSON."""
    result = parse_json_safe("not json")
    assert "error" in result
    assert "raw_response" in result
```

### Integration Test with Mocked LLM

```python
@pytest.fixture
def deterministic_llm_response():
    """Fixture for deterministic LLM responses."""
    return {
        "flashcards": [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
        ]
    }

@pytest.mark.asyncio
async def test_flashcards_generation(mock_runner, deterministic_llm_response):
    """Test flashcard generation with mocked LLM."""
    import json

    # Configure mock to return deterministic response
    async def mock_run_async(*args, **kwargs):
        event = MagicMock()
        event.is_final_response.return_value = True
        event.content.parts = [MagicMock(text=json.dumps(deterministic_llm_response))]
        yield event

    mock_runner.run_async = mock_run_async

    from server.agentcore.agents.flashcards_agent import FlashcardsAgent
    agent = FlashcardsAgent()
    result = await agent.generate("Test content", "medium", 5)

    assert len(result["flashcards"]) == 2
```

---

## Test Commands Reference

### Frontend

| Command | Description |
|---------|-------------|
| `pnpm test` | Run all tests |
| `pnpm test --watch` | Watch mode |
| `pnpm test --coverage` | With coverage |
| `pnpm test ComponentName` | Single file |
| `pnpm test --grep "pattern"` | Filter by name |

### Backend

| Command | Description |
|---------|-------------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -x` | Stop on first failure |
| `pytest --cov=.` | With coverage |
| `pytest -k "test_name"` | Filter by name |
| `pytest -m asyncio` | Only async tests |

### Coverage Thresholds

```python
# pytest.ini or pyproject.toml
[tool.coverage.run]
source = ["server"]
branch = true

[tool.coverage.report]
fail_under = 70
show_missing = true
```

---

## Common Test Scenarios

### 1. Loading States

```typescript
it("shows loading spinner while fetching", async () => {
  render(<DataComponent />);

  expect(screen.getByRole("status")).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.queryByRole("status")).not.toBeInTheDocument();
  });
});
```

### 2. Error States

```typescript
it("shows error message on API failure", async () => {
  server.use(
    http.get("/api/data", () => HttpResponse.error())
  );

  render(<DataComponent />);

  await waitFor(() => {
    expect(screen.getByText(/error/i)).toBeInTheDocument();
  });
});
```

### 3. Empty States

```typescript
it("shows empty state when no data", async () => {
  server.use(
    http.get("/api/posts", () => HttpResponse.json({ posts: [] }))
  );

  render(<PostList />);

  await waitFor(() => {
    expect(screen.getByText(/no posts/i)).toBeInTheDocument();
  });
});
```

### 4. Form Validation

```typescript
it("shows validation errors on invalid submit", async () => {
  const user = userEvent.setup();
  render(<LoginForm />);

  await user.click(screen.getByRole("button", { name: /login/i }));

  expect(screen.getByText(/email required/i)).toBeInTheDocument();
});
```

### 5. Async Operations

```python
@pytest.mark.asyncio
async def test_async_operation_completes():
    """Test async operation with proper await."""
    result = await long_running_operation()
    assert result.status == "complete"
```

---

## Troubleshooting

### Frontend

| Issue | Solution |
|-------|----------|
| `act()` warnings | Use `userEvent` instead of `fireEvent` |
| Query not found | Use `findBy*` for async elements |
| MSW not working | Check `await server.listen()` in setup |
| Stale closure | Add dependency to `useCallback`/`useEffect` |

### Backend

| Issue | Solution |
|-------|----------|
| `ScopeMismatch` | Match fixture scopes (function/session) |
| Async test not running | Add `@pytest.mark.asyncio` |
| Mock not applied | Check patch path matches import |
| Import error | Use `conftest.py` for shared fixtures |
