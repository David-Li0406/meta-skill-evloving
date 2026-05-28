# Pattern 8: Testing

**Problem**: No tests, so every change is risky. Or tests exist but are slow, flaky, or test the wrong things.

**Solution**: Mock external dependencies, test business logic in isolation, and focus coverage on critical paths.

---

## Concept

Testing answers: **"Can I change this code confidently?"**

Good testing provides:
1. **Confidence** — Changes don't break existing functionality
2. **Documentation** — Tests show how code should be used
3. **Design Feedback** — Hard-to-test code is often poorly designed
4. **Fast Feedback** — Tests run in seconds, not minutes

---

## Testing Strategy

```
                    ┌─────────────┐
                    │ E2E Tests   │  Few, slow, catch integration issues
                    │ (10%)       │
                    └─────────────┘
                 ┌───────────────────┐
                 │ Integration Tests │  Some, mock external services
                 │ (20%)             │
                 └───────────────────┘
              ┌─────────────────────────┐
              │ Unit Tests              │  Many, fast, test business logic
              │ (70%)                   │
              └─────────────────────────┘
```

**Focus**: Unit tests for business logic, integration tests for boundaries.

---

## Implementation

### Python: pytest with Fixtures

```python
# tests/conftest.py - Shared fixtures
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
import tempfile

@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def sample_config():
    """Standard configuration for testing."""
    from my_tool.config import Config
    return Config(
        input_path="/tmp/input",
        output_path="/tmp/output",
        verbose=False
    )

@pytest.fixture
def sample_tasks():
    """Sample task data for testing."""
    from my_tool.models import Task, Status
    return [
        Task(id="1", name="Task 1", status=Status.PENDING),
        Task(id="2", name="Task 2", status=Status.PENDING),
        Task(id="3", name="Task 3", status=Status.COMPLETED),
    ]

@pytest.fixture
def mock_api_client():
    """Mock external API client."""
    with patch('my_tool.api.Client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client

# tests/test_processor.py - Unit tests
import pytest
from my_tool.processor import process_task, validate_input

class TestProcessTask:
    def test_process_pending_task(self, sample_config):
        from my_tool.models import Task, Status

        task = Task(id="1", name="Test", status=Status.PENDING)
        result = process_task(task, sample_config)

        assert result.success is True
        assert result.task.status == Status.COMPLETED

    def test_skip_completed_task(self, sample_config):
        from my_tool.models import Task, Status

        task = Task(id="1", name="Test", status=Status.COMPLETED)
        result = process_task(task, sample_config)

        assert result.success is True
        assert result.skipped is True

    def test_handle_processing_error(self, sample_config, mock_api_client):
        from my_tool.models import Task, Status

        mock_api_client.process.side_effect = Exception("API Error")
        task = Task(id="1", name="Test", status=Status.PENDING)

        result = process_task(task, sample_config)

        assert result.success is False
        assert "API Error" in result.error_message

class TestValidateInput:
    @pytest.mark.parametrize("input_val,expected", [
        ("valid", True),
        ("", False),
        (None, False),
        ("   ", False),
    ])
    def test_validate_input(self, input_val, expected):
        assert validate_input(input_val) == expected
```

### Python: Mocking External Services

```python
# tests/test_api_integration.py
import pytest
from unittest.mock import patch, MagicMock
import responses  # For mocking HTTP requests

class TestAPIIntegration:
    @responses.activate
    def test_fetch_data_success(self):
        """Test successful API response."""
        responses.add(
            responses.GET,
            "https://api.example.com/data",
            json={"items": [1, 2, 3]},
            status=200
        )

        from my_tool.api import fetch_data
        result = fetch_data("https://api.example.com/data")

        assert result == {"items": [1, 2, 3]}

    @responses.activate
    def test_fetch_data_retry_on_server_error(self):
        """Test retry on 500 error."""
        # First call fails, second succeeds
        responses.add(responses.GET, "https://api.example.com/data", status=500)
        responses.add(
            responses.GET,
            "https://api.example.com/data",
            json={"items": []},
            status=200
        )

        from my_tool.api import fetch_data
        result = fetch_data("https://api.example.com/data")

        assert len(responses.calls) == 2  # Verify retry happened

    @patch('my_tool.api.requests.get')
    def test_fetch_data_with_mock(self, mock_get):
        """Alternative: patch requests directly."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        from my_tool.api import fetch_data
        result = fetch_data("https://api.example.com/data")

        assert result == {"data": "test"}
        mock_get.assert_called_once()
```

### Node.js: Vitest with Mocks

```javascript
// tests/setup.js - Global test setup
import { vi } from 'vitest';

// Mock Chrome APIs globally
global.chrome = {
  storage: {
    local: {
      get: vi.fn().mockResolvedValue({}),
      set: vi.fn().mockResolvedValue(undefined),
    },
  },
  runtime: {
    sendMessage: vi.fn(),
    onMessage: {
      addListener: vi.fn(),
    },
  },
};

// tests/processor.test.js
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { processItem, validateInput } from '../src/processor.js';

describe('processItem', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('processes valid item successfully', async () => {
    const item = { id: '1', name: 'Test' };
    const result = await processItem(item);

    expect(result.success).toBe(true);
    expect(result.itemId).toBe('1');
  });

  it('handles processing errors gracefully', async () => {
    const item = { id: 'bad', name: null }; // Invalid item

    const result = await processItem(item);

    expect(result.success).toBe(false);
    expect(result.error).toBeDefined();
  });
});

describe('validateInput', () => {
  it.each([
    ['valid', true],
    ['', false],
    [null, false],
    ['   ', false],
  ])('validates "%s" as %s', (input, expected) => {
    expect(validateInput(input)).toBe(expected);
  });
});
```

### Node.js: Manual Mocks

```javascript
// __mocks__/googleapis.js - Manual mock for Google APIs
const mockGmail = {
  users: {
    messages: {
      list: jest.fn().mockResolvedValue({
        data: { messages: [] },
      }),
      get: jest.fn().mockResolvedValue({
        data: { id: '123', snippet: 'Test email' },
      }),
      trash: jest.fn().mockResolvedValue({ data: {} }),
    },
  },
};

const google = {
  gmail: jest.fn(() => mockGmail),
};

module.exports = { google, mockGmail };

// tests/gmail-monitor.test.js
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mockGmail } from '../__mocks__/googleapis.js';

vi.mock('googleapis');

import { getUnreadEmails, trashEmails } from '../src/gmail-monitor.js';

describe('Gmail Monitor', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('fetches unread emails', async () => {
    mockGmail.users.messages.list.mockResolvedValueOnce({
      data: {
        messages: [{ id: '1' }, { id: '2' }],
      },
    });

    const emails = await getUnreadEmails();

    expect(emails).toHaveLength(2);
    expect(mockGmail.users.messages.list).toHaveBeenCalledWith({
      userId: 'me',
      q: 'is:unread',
    });
  });

  it('returns empty array on error', async () => {
    mockGmail.users.messages.list.mockRejectedValueOnce(new Error('API Error'));

    const emails = await getUnreadEmails();

    expect(emails).toEqual([]);
  });
});
```

### TypeScript: Testing Type Guards

```typescript
// src/types.test.ts
import { describe, it, expect } from 'vitest';
import { isValidConfig, isTask, Config, Task } from './types';

describe('Type Guards', () => {
  describe('isValidConfig', () => {
    it('accepts valid config', () => {
      const config: unknown = {
        inputPath: '/input',
        outputPath: '/output',
        verbose: true,
      };

      expect(isValidConfig(config)).toBe(true);
    });

    it('rejects config with missing required fields', () => {
      const config: unknown = {
        inputPath: '/input',
        // missing outputPath
      };

      expect(isValidConfig(config)).toBe(false);
    });

    it('rejects config with wrong types', () => {
      const config: unknown = {
        inputPath: 123, // should be string
        outputPath: '/output',
      };

      expect(isValidConfig(config)).toBe(false);
    });

    it('accepts optional fields as undefined', () => {
      const config: unknown = {
        inputPath: '/input',
        outputPath: '/output',
        // verbose is optional
      };

      expect(isValidConfig(config)).toBe(true);
    });
  });
});
```

---

## What to Test

| Priority | What | Why |
|----------|------|-----|
| **High** | Business logic | Core value, changes frequently |
| **High** | Data transformations | Easy to get wrong |
| **Medium** | Type guards / validation | Boundary protection |
| **Medium** | Error handling | User experience |
| **Low** | CLI parsing | Framework handles it |
| **Low** | Third-party integrations | Mock, don't test their code |

---

## Test Organization

```
tests/
├── conftest.py / setup.js    # Shared fixtures and mocks
├── fixtures/                  # Test data files
│   ├── sample_input.json
│   └── expected_output.json
├── test_<module>.py          # Mirror src/ structure
├── test_integration.py       # Integration tests (marked slow)
└── __mocks__/                # Manual mocks (Node.js)
```

---

## Checklist

- [ ] Unit tests for business logic (>80% coverage)
- [ ] External APIs are mocked (no real network calls)
- [ ] Fixtures provide consistent test data
- [ ] Tests run in <10 seconds (unit tests)
- [ ] Slow tests marked with `@pytest.mark.slow` or `describe.skip`
- [ ] Test names describe behavior, not implementation
- [ ] Edge cases covered (empty input, nulls, errors)

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Testing implementation | Breaks when refactoring | Test behavior |
| No mocks | Tests are slow and flaky | Mock external deps |
| Testing frameworks | Wasted effort | Trust the framework |
| 100% coverage goal | Diminishing returns | Focus on critical paths |
| Tests depend on order | Flaky | Each test is independent |
