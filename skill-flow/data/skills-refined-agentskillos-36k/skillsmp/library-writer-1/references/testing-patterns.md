# Testing Patterns

How to test libraries effectively across versions and environments.

## Test Framework Selection

### Use the Standard

Every language has a standard test framework. Use it.

| Language | Standard Framework | Why |
|----------|-------------------|-----|
| Python | pytest or unittest | Ships with Python, widely known |
| JavaScript | Jest or Vitest | De facto standards, good tooling |
| Go | testing | Built into language |
| Rust | built-in | Part of cargo |
| Ruby | Minitest | Ships with Ruby, simple |

### Why Standard Frameworks?

- Lower barrier to contribution
- Better IDE support
- More documentation
- Easier CI integration
- Familiar to users

## Test Structure

### Directory Layout

```
tests/
├── unit/              # Fast, isolated tests
│   ├── test_client.ext
│   ├── test_config.ext
│   └── test_utils.ext
├── integration/       # Tests with external systems
│   ├── test_api.ext
│   └── test_database.ext
├── fixtures/          # Test data
│   ├── sample_data.json
│   └── mock_responses/
└── conftest.ext       # Shared fixtures/setup
```

### Test File Naming

```
Source: lib/my_library/client.ext
Test:   tests/unit/test_client.ext

# Clear 1:1 mapping
# Easy to find tests for any module
```

## Unit Tests

### Test Public API

```
def test_client_initialization():
    client = Client(api_key="test")
    assert client.api_key == "test"

def test_client_default_timeout():
    client = Client(api_key="test")
    assert client.timeout == 30  # Default value
```

### Test Edge Cases

```
def test_empty_input():
    result = process("")
    assert result == default_result

def test_null_input():
    with raises(ArgumentError):
        process(None)

def test_large_input():
    large_data = "x" * 1_000_000
    result = process(large_data)
    assert result is not None
```

### Test Error Conditions

```
def test_invalid_api_key():
    with raises(ConfigError) as exc:
        Client(api_key="invalid")
    assert "API key must be" in str(exc)

def test_network_error():
    client = Client(api_key="test")
    # Mock network failure
    with raises(ConnectionError):
        client.fetch()
```

## Integration Tests

### Test External Systems

```
# Only run when integration tests enabled
@integration_test
def test_real_api_call():
    client = Client(api_key=os.environ["TEST_API_KEY"])
    result = client.fetch()
    assert result.status == "success"
```

### Test Framework Integration

```
# Django integration test
class DjangoIntegrationTest(TestCase):
    def test_model_extension(self):
        product = Product.objects.create(name="Test")
        assert hasattr(product, 'search')

# Express integration test
describe('Express middleware', () => {
    it('processes requests', async () => {
        const app = express();
        app.use(mylib.middleware());
        const res = await request(app).get('/');
        expect(res.status).toBe(200);
    });
});
```

## Fixture Patterns

### Static Fixtures

```
fixtures/
  sample_response.json
  error_response.json
  large_dataset.json

# Load in tests
def load_fixture(name):
    path = fixtures_dir / f"{name}.json"
    return json.loads(path.read_text())
```

### Generated Fixtures

```
# Factory functions for test data
def make_user(**overrides):
    defaults = {
        'name': 'Test User',
        'email': 'test@example.com',
    }
    return User(**{**defaults, **overrides})

# Usage
user = make_user(name='Custom Name')
```

### Fixture Scope

```
# Per-test fixture (isolated)
@fixture
def client():
    return Client(api_key="test")

# Per-module fixture (shared, faster)
@fixture(scope="module")
def database():
    db = setup_test_database()
    yield db
    teardown_test_database(db)
```

## Mocking

### Mock External Services

```
def test_api_call(mocker):
    # Mock HTTP client
    mock_response = {'status': 'success'}
    mocker.patch('requests.get', return_value=mock_response)

    client = Client()
    result = client.fetch()

    assert result == mock_response
```

### Mock at Boundaries

```
Good:
  # Mock the HTTP layer
  mock_http_client()

Bad:
  # Mock internal implementation details
  mock_internal_parser()
  # Couples tests to implementation
```

### When Not to Mock

```
Don't mock:
  - Pure functions (just call them)
  - Simple data classes
  - Your own code (unless necessary)

Do mock:
  - Network calls
  - File system (sometimes)
  - Time-dependent code
  - External services
```

## Multi-Version Testing

### Test Against Multiple Versions

```
CI Matrix:
  python: [3.9, 3.10, 3.11, 3.12]
  node: [18, 20, 22]
  ruby: [3.1, 3.2, 3.3]
```

### Version-Specific Tests

```
import sys

@skipif(sys.version_info < (3, 10))
def test_new_feature():
    # Only runs on Python 3.10+
    pass
```

### Framework Version Testing

```
CI Matrix:
  django: [4.0, 4.1, 4.2, 5.0]
  rails: [6.1, 7.0, 7.1]

# Test combinations
- python: 3.11
  django: 4.2
- python: 3.12
  django: 5.0
```

## CI Configuration

### Basic CI Setup

```yaml
# GitHub Actions example
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: pip install -e ".[test]"
      - run: pytest
```

### Test Coverage

```yaml
- run: pytest --cov=mylib --cov-report=xml
- uses: codecov/codecov-action@v3
```

### Separate Test Types

```yaml
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - run: pytest tests/unit

  integration:
    runs-on: ubuntu-latest
    needs: unit  # Run after unit tests pass
    steps:
      - run: pytest tests/integration
```

## Test Performance

### Keep Tests Fast

```
Guidelines:
  - Unit tests: < 100ms each
  - Integration tests: < 1s each
  - Full suite: < 5 minutes

Techniques:
  - Mock slow operations
  - Use in-memory databases
  - Parallelize test runs
  - Cache expensive setup
```

### Parallel Testing

```
# pytest
pytest -n auto  # Auto-detect CPU cores

# Jest
jest --maxWorkers=4
```

## Test Documentation

### Document Test Purpose

```
def test_client_retries_on_timeout():
    """
    Client should retry failed requests up to 3 times
    with exponential backoff before raising an error.
    """
    # Test implementation
```

### Document Test Data

```
fixtures/
  README.md  # Explain what each fixture is for

# sample_response.json
# Represents a successful API response with all fields populated
```

## Debugging Tests

### Useful Assertions

```
# Good: specific assertion
assert result.status == "success"

# Better: with message
assert result.status == "success", f"Expected success, got {result.status}"

# Best: detailed diff
assert result == expected_result
# Test framework shows detailed diff
```

### Test Isolation

```
# Each test should be independent
def test_a():
    # Don't depend on test_b running first
    setup_test_state()
    # Run test
    cleanup_test_state()

# Use fixtures for shared setup
@fixture(autouse=True)
def reset_state():
    yield
    clear_all_state()
```
