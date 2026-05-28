---
name: test-engineer
description: Full-stack testing specialist for Faiston NEXO. Use when writing tests, fixing test failures, or validating behaviors across Frontend (Vitest, RTL, MSW), Backend (pytest, FastAPI), and Agents (Google ADK mocking).
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Test Engineer Skill

Full-stack testing specialist for the Faiston NEXO project covering ALL layers.

For detailed patterns and templates, see [reference.md](reference.md).

## Testing Stack

### Frontend

- **Unit/Integration**: Vitest
- **Component Testing**: React Testing Library
- **API Mocking**: MSW (Mock Service Worker)
- **Assertions**: Vitest matchers + jest-dom
- **Accessibility**: jest-axe
- **Coverage**: Vitest coverage

### Backend

- **Framework**: pytest + pytest-asyncio
- **API Testing**: httpx (async client for FastAPI)
- **Mocking**: unittest.mock, pytest-mock
- **Fixtures**: conftest.py patterns
- **Coverage**: pytest-cov

### Agents

- **ADK Mocking**: Mock Runner and Agent responses
- **AgentCore Testing**: Mock HTTP invocations
- **LLM Mocking**: Deterministic response fixtures

## Testing Philosophy

### Testing Pyramid

```
      /\
     /E2E\       ← Few: Full user flows (login → dashboard)
    /──────\
   /Integr.\     ← Some: Component + API interactions
  /──────────\
 / Unit Tests \  ← Many: Individual functions, hooks
```

**Priority:**
1. **Unit Tests**: Utility functions, hooks, pure logic
2. **Integration Tests**: Components with API calls
3. **Component Tests**: User interactions, rendering
4. **E2E Tests**: Critical user journeys

## File Structure

```
client/
├── components/
│   ├── PostCard.tsx
│   └── PostCard.test.tsx      # Co-located test
├── hooks/
│   ├── useAuth.ts
│   └── useAuth.test.ts
├── lib/
│   ├── utils.ts
│   └── utils.test.ts
└── __tests__/                  # Integration tests
    └── Community.test.tsx
```

## Test Patterns

### 1. Component Tests

```typescript
// components/PostCard.test.tsx
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { PostCard } from "./PostCard"

describe("PostCard", () => {
  const defaultProps = {
    title: "Test Post",
    content: "Test content",
    author: "Test Author",
    likes: 5,
    onLike: vi.fn(),
  }

  it("renders post content", () => {
    render(<PostCard {...defaultProps} />)

    expect(screen.getByText("Test Post")).toBeInTheDocument()
    expect(screen.getByText("Test content")).toBeInTheDocument()
    expect(screen.getByText("Test Author")).toBeInTheDocument()
  })

  it("calls onLike when like button clicked", async () => {
    const user = userEvent.setup()
    render(<PostCard {...defaultProps} />)

    await user.click(screen.getByRole("button", { name: /like/i }))

    expect(defaultProps.onLike).toHaveBeenCalledTimes(1)
  })
})
```

### 2. Hook Tests

```typescript
// hooks/useAuth.test.ts
import { renderHook, act } from "@testing-library/react"
import { useAuth } from "./useAuth"
import { AuthProvider } from "@/contexts/AuthContext"

describe("useAuth", () => {
  const wrapper = ({ children }) => (
    <AuthProvider>{children}</AuthProvider>
  )

  it("starts with no user", () => {
    const { result } = renderHook(() => useAuth(), { wrapper })

    expect(result.current.user).toBeNull()
    expect(result.current.isAuthenticated).toBe(false)
  })

  it("logs in user", async () => {
    const { result } = renderHook(() => useAuth(), { wrapper })

    await act(async () => {
      await result.current.login("test@example.com", "password")
    })

    expect(result.current.user).toBeDefined()
    expect(result.current.isAuthenticated).toBe(true)
  })
})
```

### 3. Integration Tests with MSW

```typescript
// __tests__/Community.test.tsx
import { render, screen, waitFor } from "@testing-library/react"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { http, HttpResponse } from "msw"
import { setupServer } from "msw/node"
import { MemoryRouter } from "react-router-dom"
import Community from "@/pages/Community"

const server = setupServer(
  http.get("/api/posts", () => {
    return HttpResponse.json({
      posts: [
        {
          post_id: "1",
          title: "Test Post",
          content: "Test content",
          category: "duvidas",
          likes_count: 5,
          comments_count: 2,
        },
      ],
    })
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe("Community Page", () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  })

  const renderCommunity = () => {
    return render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <Community />
        </MemoryRouter>
      </QueryClientProvider>
    )
  }

  it("displays posts after loading", async () => {
    renderCommunity()

    await waitFor(() => {
      expect(screen.getByText("Test Post")).toBeInTheDocument()
    })
  })

  it("displays error state on API failure", async () => {
    server.use(
      http.get("/api/posts", () => {
        return HttpResponse.error()
      })
    )

    renderCommunity()

    await waitFor(() => {
      expect(screen.getByText(/erro/i)).toBeInTheDocument()
    })
  })
})
```

### 4. Utility Function Tests

```typescript
// lib/utils.test.ts
import { cn, formatDate, truncate } from "./utils"

describe("cn (classnames)", () => {
  it("merges class names", () => {
    expect(cn("foo", "bar")).toBe("foo bar")
  })

  it("handles conditional classes", () => {
    expect(cn("base", false && "hidden", true && "visible"))
      .toBe("base visible")
  })

  it("dedupes Tailwind classes", () => {
    expect(cn("px-4", "px-6")).toBe("px-6")
  })
})

describe("truncate", () => {
  it("truncates long strings", () => {
    expect(truncate("Hello World", 5)).toBe("Hello...")
  })

  it("returns short strings unchanged", () => {
    expect(truncate("Hi", 10)).toBe("Hi")
  })
})
```

## Accessibility Testing

```typescript
import { axe, toHaveNoViolations } from "jest-axe"

expect.extend(toHaveNoViolations)

describe("PostCard Accessibility", () => {
  it("has no accessibility violations", async () => {
    const { container } = render(<PostCard {...props} />)

    const results = await axe(container)

    expect(results).toHaveNoViolations()
  })
})
```

## Backend Testing (pytest)

### FastAPI Endpoint Tests

```python
# server/tests/test_main.py
import pytest
from httpx import AsyncClient, ASGITransport
from server.main import app

@pytest.fixture
async def client():
    """Async test client for FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_health_check(client):
    """Test health endpoint returns 200."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_create_post_validation(client):
    """Test validation error on invalid post."""
    response = await client.post("/api/posts", json={})
    assert response.status_code == 422  # Validation error
```

### Mocking External Services

```python
# server/tests/test_community.py
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_dynamodb():
    """Mock DynamoDB table."""
    with patch("server.community.routes.table") as mock:
        yield mock

@pytest.mark.asyncio
async def test_get_posts(client, mock_dynamodb):
    """Test getting posts from DynamoDB."""
    mock_dynamodb.query.return_value = {
        "Items": [{"post_id": "1", "title": "Test"}]
    }

    response = await client.get("/api/posts")
    assert response.status_code == 200
    assert len(response.json()["posts"]) == 1
```

### Lambda Handler Tests

```python
# server/tests/test_lambda.py
import json
from server.lambda_handler import handler

def test_lambda_handler():
    """Test Lambda handler with API Gateway event."""
    event = {
        "httpMethod": "GET",
        "path": "/health",
        "headers": {},
        "queryStringParameters": None,
        "body": None,
    }
    context = MagicMock()

    result = handler(event, context)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["status"] == "healthy"
```

## Agent Testing (Google ADK)

### Mocking Agent Responses

```python
# server/agentcore/tests/test_agents.py
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

@pytest.fixture
def mock_runner():
    """Mock Google ADK Runner."""
    with patch("google.adk.runners.Runner") as mock:
        runner_instance = MagicMock()
        mock.return_value = runner_instance

        # Mock async iteration
        async def mock_run_async(*args, **kwargs):
            event = MagicMock()
            event.is_final_response.return_value = True
            event.content.parts = [MagicMock(text='{"flashcards": []}')]
            yield event

        runner_instance.run_async = mock_run_async
        yield runner_instance

@pytest.mark.asyncio
async def test_flashcards_agent(mock_runner):
    """Test flashcards generation."""
    from server.agentcore.agents.flashcards_agent import FlashcardsAgent

    agent = FlashcardsAgent()
    result = await agent.generate(
        transcription="Test content",
        difficulty="medium",
        count=5,
    )

    assert "flashcards" in result
```

### Testing AgentCore Invocation

```python
# server/agentcore/tests/test_main.py
import pytest
from unittest.mock import patch

@pytest.fixture
def mock_agents():
    """Mock all agent classes."""
    with patch("server.agentcore.main.NEXOAgent") as nexo, \
         patch("server.agentcore.main.FlashcardsAgent") as flash:
        nexo_instance = nexo.return_value
        nexo_instance.invoke = AsyncMock(return_value="Test response")

        flash_instance = flash.return_value
        flash_instance.generate = AsyncMock(return_value={"flashcards": []})

        yield {"nexo": nexo_instance, "flashcards": flash_instance}

def test_invoke_nexo_chat(mock_agents):
    """Test nexo_chat action routing."""
    from server.agentcore.main import invoke

    payload = {
        "action": "nexo_chat",
        "question": "What is Python?",
        "transcription": "Python is a programming language.",
    }
    context = MagicMock()
    context.session_id = "test-session-123456789012345678901234"

    result = invoke(payload, context)

    assert "answer" in result
```

### Deterministic LLM Responses

```python
# server/agentcore/tests/conftest.py
import pytest
import json

@pytest.fixture
def flashcard_response():
    """Deterministic flashcard response for testing."""
    return {
        "flashcards": [
            {
                "id": "card-1",
                "question": "What is Python?",
                "answer": "A programming language",
                "difficulty": "easy"
            }
        ]
    }

@pytest.fixture
def mock_gemini_response(flashcard_response):
    """Mock Gemini API response."""
    def _mock(prompt):
        return json.dumps(flashcard_response)
    return _mock
```

## Running Tests

### Frontend

```bash
# Run all frontend tests
pnpm test

# Run tests in watch mode
pnpm test --watch

# Run specific test file
pnpm test PostCard.test.tsx

# Run with coverage
pnpm test --coverage
```

### Backend

```bash
# Run all backend tests
cd server && pytest

# Run with verbose output
cd server && pytest -v

# Run specific test file
cd server && pytest tests/test_main.py

# Run with coverage
cd server && pytest --cov=. --cov-report=html

# Run async tests only
cd server && pytest -m asyncio
```

### Full Stack

```bash
# Run all tests (frontend + backend)
pnpm test && cd server && pytest

# Quick validation
pnpm typecheck && pnpm build && cd server && pytest
```

## Test Utilities

### Wrapper with Providers

```typescript
// test-utils.tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { MemoryRouter } from "react-router-dom"
import { AuthProvider } from "@/contexts/AuthContext"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
  },
})

export function AllProviders({ children }) {
  return (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>
        <AuthProvider>
          {children}
        </AuthProvider>
      </MemoryRouter>
    </QueryClientProvider>
  )
}

export function renderWithProviders(ui: React.ReactElement) {
  return render(ui, { wrapper: AllProviders })
}
```

## Running Tests

```bash
# Run all tests
pnpm test

# Run tests in watch mode
pnpm test --watch

# Run specific test file
pnpm test PostCard.test.tsx

# Run with coverage
pnpm test --coverage

# Run tests matching pattern
pnpm test --grep "auth"
```

## Test Checklist

Before completing tests:

- [ ] Tests describe behavior, not implementation
- [ ] Each test has a single assertion focus
- [ ] Tests are independent (no shared state)
- [ ] Async operations properly awaited
- [ ] MSW handlers reset between tests
- [ ] Accessibility tested for interactive components
- [ ] Edge cases covered (empty, error, loading)
- [ ] Tests run in < 1 second each

## Common Issues

### Query Not Working in Tests

```typescript
// Need to wrap with QueryClientProvider
const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false }, // Don't retry in tests
  },
})
```

### Act Warning

```typescript
// ❌ Problem: State update not wrapped
fireEvent.click(button)

// ✅ Fix: Use userEvent (auto-wraps)
await userEvent.click(button)
```

### Async Not Completing

```typescript
// ❌ Problem: Not waiting
render(<Component />)
expect(screen.getByText("Loaded")).toBeInTheDocument() // Fails!

// ✅ Fix: Wait for element
await waitFor(() => {
  expect(screen.getByText("Loaded")).toBeInTheDocument()
})
```

## Response Format

When writing tests:

1. **Understand what to test**
   - User-visible behavior
   - Edge cases
   - Error states

2. **Structure clearly**
   - Arrange: Set up test data
   - Act: Perform action
   - Assert: Verify result

3. **Keep tests focused**
   - One concept per test
   - Descriptive test names
   - Use data-testid sparingly

4. **Verify coverage**
   - Run with `--coverage`
   - Check uncovered lines

Remember: Tests document expected behavior!
