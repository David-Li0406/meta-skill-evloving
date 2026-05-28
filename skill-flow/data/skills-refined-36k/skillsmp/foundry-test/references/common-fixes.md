# Common Fixes

## Pattern: Missing Mock

**Symptom:** Test makes real network calls, causing timeouts or failures

### Python
```python
from unittest.mock import patch

@patch('module.requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {'key': 'value'}
    result = function_under_test()
    assert result == expected
```

### Go
```go
// Use interfaces for dependency injection
type HTTPClient interface {
    Get(url string) (*http.Response, error)
}

// In test, pass mock implementation
type mockClient struct{}
func (m *mockClient) Get(url string) (*http.Response, error) {
    return &http.Response{Body: io.NopCloser(strings.NewReader(`{"key":"value"}`))}, nil
}
```

### JavaScript (Jest)
```javascript
jest.mock('./api');
import { fetchData } from './api';

fetchData.mockResolvedValue({ key: 'value' });

test('api call', async () => {
    const result = await functionUnderTest();
    expect(result).toEqual(expected);
});
```

## Pattern: Setup/Fixture Scope Issues

**Symptom:** Test state leaking between tests

### Python (pytest)
```python
@pytest.fixture(scope='function')  # Fresh per test
def database():
    db = create_database()
    yield db
    db.cleanup()  # Always runs after test
```

### Go
```go
func TestSomething(t *testing.T) {
    // Setup
    db := createDatabase()
    t.Cleanup(func() {
        db.Close()  // Always runs after test
    })
    // Test code...
}
```

### JavaScript (Jest)
```javascript
let db;

beforeEach(() => {
    db = createDatabase();
});

afterEach(() => {
    db.cleanup();
});
```

## Pattern: Assertion Message Missing

**Symptom:** Assertion fails with no helpful context

### Python
```python
# Bad
assert result == expected

# Good
assert result == expected, f"Expected {expected}, got {result}"
```

### Go
```go
// Bad
if result != expected {
    t.Fail()
}

// Good
if result != expected {
    t.Errorf("Expected %v, got %v", expected, result)
}

// Better (using testify)
assert.Equal(t, expected, result, "result should match expected")
```

### JavaScript (Jest)
```javascript
// Bad
expect(result).toBe(expected);

// Good (Jest provides helpful messages, but you can add custom)
expect(result).toBe(expected); // Jest auto-generates diff
expect(result).toBe(expected, `Expected ${expected}, got ${result}`); // Custom message
```

## Pattern: Test Order Dependency

**Symptom:** Test passes alone, fails in suite (or vice versa)

**Diagnosis:**

### pytest
```bash
pytest --randomly-seed=12345  # Detect order dependencies
pytest -x  # Stop on first failure to isolate
```

### go test
```bash
go test -shuffle=on ./...  # Go 1.17+
go test -count=1 ./...     # Disable caching
```

### Jest
```bash
jest --randomize
jest --runInBand  # Run serially to detect shared state
```

**Fix:** Find and eliminate shared state - use fresh fixtures per test.

## Pattern: Async/Concurrent Race Condition

**Symptom:** Test passes sometimes, fails randomly

### Python
```python
# Use proper async test support
import pytest

@pytest.mark.asyncio
async def test_async_operation():
    result = await async_function()
    assert result == expected
```

### Go
```go
func TestConcurrent(t *testing.T) {
    // Use -race flag to detect
    // go test -race ./...

    var wg sync.WaitGroup
    wg.Add(2)
    go func() { defer wg.Done(); /* task 1 */ }()
    go func() { defer wg.Done(); /* task 2 */ }()
    wg.Wait()
}
```

### JavaScript
```javascript
test('async operation', async () => {
    // Always await async operations
    const result = await asyncFunction();
    expect(result).toBe(expected);
});

// Use fake timers for time-dependent code
jest.useFakeTimers();
jest.advanceTimersByTime(1000);
```

## Pattern: Environment-Dependent Test

**Symptom:** Test passes locally, fails in CI (or vice versa)

**Common causes:**
- Different OS (paths, line endings)
- Missing environment variables
- Different timezone
- Different locale

**Fixes:**
- Use OS-agnostic path handling (`os.path.join`, `path.join`, `filepath.Join`)
- Mock environment variables in tests
- Set explicit timezone/locale in test setup
- Use CI-aware test skipping when necessary
