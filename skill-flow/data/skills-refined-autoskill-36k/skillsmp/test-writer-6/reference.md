# Test Writer Reference

Comprehensive testing guide for Polibase.

## Testing Philosophy

1. **Fast**: Unit tests < 1s, integration tests < 5s
2. **Isolated**: No dependencies between tests
3. **Deterministic**: Same input → same output
4. **Mocked**: No real external services
5. **Comprehensive**: Cover happy path, edge cases, errors

## Test Types

### Unit Tests (`tests/unit/`)

**Purpose**: Test individual components in isolation

**Characteristics**:
- No external dependencies
- Uses mocks for all dependencies
- Fast execution (< 1 second)
- Tests single responsibility

**When**: Testing domain services, use cases, DTOs

### Integration Tests (`tests/integration/`)

**Purpose**: Test components working together

**Characteristics**:
- Uses real database (test instance)
- Tests actual integrations
- Slower execution (< 5 seconds)
- Tests end-to-end workflows

**When**: Testing repositories, database queries

### Evaluation Tests (`tests/evaluation/`)

**Purpose**: Evaluate LLM quality (NOT run in CI)

**Characteristics**:
- Uses real LLM APIs
- Expensive (API costs)
- Manual execution only
- For quality benchmarking

**When**: Evaluating LLM accuracy, testing prompts

## Mocking Strategies

### AsyncMock for Async Functions

```python
from unittest.mock import AsyncMock

@pytest.fixture
def mock_repo():
    mock = AsyncMock(spec=IPoliticianRepository)
    mock.find_by_id.return_value = Politician(id=1, name="Test")
    mock.save.return_value = Politician(id=1, name="Test")
    return mock
```

### spec= Parameter

Always use `spec=` to ensure type safety:

```python
# ✅ GOOD: Type checking
mock = AsyncMock(spec=ILLMService)
mock.nonexistent_method()  # Will fail appropriately

# ❌ BAD: No type checking
mock = AsyncMock()
mock.anything_works()  # Silently succeeds
```

### return_value vs side_effect

```python
# return_value: Always return same value
mock.method.return_value = "constant"

# side_effect: Return different values or raise
mock.method.side_effect = ["first", "second", "third"]
mock.method.side_effect = Exception("Error!")
```

### Patching External Libraries

```python
from unittest.mock import patch

@patch('src.infrastructure.external.gemini_llm_service.genai')
def test_llm_service(mock_genai):
    # Mock at integration point
    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value.text = "Response"
    mock_genai.GenerativeModel.return_value = mock_model

    service = GeminiLLMService(api_key="fake")
    result = await service.generate_text("prompt")
    assert result == "Response"
```

## Async Testing

### pytest-asyncio

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected
```

### Async Fixtures

```python
@pytest.fixture
async def async_resource():
    resource = await create_resource()
    yield resource
    await cleanup_resource(resource)
```

### Event Loop Scope

```python
# Default: function scope (new loop per test)
@pytest.mark.asyncio
async def test_1():
    ...

# Module scope (shared loop for all tests in module)
@pytest.mark.asyncio(scope="module")
async def test_2():
    ...
```

## Test Structure (AAA Pattern)

```python
async def test_create_politician_successfully():
    # Arrange: Setup test data and mocks
    input_dto = CreatePoliticianInputDTO(name="Test", party_id=1)
    mock_repo = AsyncMock(spec=IPoliticianRepository)
    mock_repo.save.return_value = Politician(id=1, name="Test", party_id=1)
    usecase = CreatePoliticianUseCase(politician_repository=mock_repo)

    # Act: Execute the operation
    output_dto = await usecase.execute(input_dto)

    # Assert: Verify results
    assert output_dto.success is True
    assert output_dto.politician_id == 1
    mock_repo.save.assert_called_once()
```

## Fixtures (conftest.py)

### Shared Fixtures

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_llm_service():
    """Shared mock LLM service."""
    mock = AsyncMock(spec=ILLMService)
    mock.generate_text.return_value = "Mocked response"
    return mock

@pytest.fixture
def sample_politician():
    """Sample politician for tests."""
    return Politician(
        id=1,
        name="山田太郎",
        party_id=1,
        furigana="やまだたろう"
    )
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default: new for each test
def function_scope():
    ...

@pytest.fixture(scope="class")  # Shared within test class
def class_scope():
    ...

@pytest.fixture(scope="module")  # Shared within module
def module_scope():
    ...

@pytest.fixture(scope="session")  # Shared across all tests
def session_scope():
    ...
```

## Assertion Strategies

### Basic Assertions

```python
assert result is True
assert value == expected
assert value != unexpected
assert item in collection
assert value is None
assert value is not None
```

### pytest Assertions

```python
# Expect exception
with pytest.raises(ValueError):
    validate_input("")

# Expect exception with message
with pytest.raises(ValueError, match="Name is required"):
    validate_input("")

# Warnings
with pytest.warns(UserWarning):
    deprecated_function()
```

### Mock Assertions

```python
# Called once
mock.method.assert_called_once()

# Called once with specific args
mock.method.assert_called_once_with(arg1, arg2)

# Called at all
mock.method.assert_called()

# Not called
mock.method.assert_not_called()

# Async version
await mock.method.assert_awaited_once()
```

## Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("山田太郎氏", "山田太郎"),
    ("山田太郎君", "山田太郎"),
    ("山田太郎議員", "山田太郎"),
])
def test_normalize_name(input, expected):
    service = SpeakerDomainService()
    result = service.normalize_name(input)
    assert result == expected
```

## Test Organization

### Test Classes

```python
class TestPoliticianDomainService:
    """Group related tests."""

    @pytest.fixture
    def service(self):
        return PoliticianDomainService()

    def test_is_duplicate_returns_true_for_same_name(self, service):
        ...

    def test_is_duplicate_returns_false_for_different_name(self, service):
        ...
```

### Test Naming

Format: `test_[what]_[condition]_[expected]`

Examples:
- `test_normalize_name_removes_honorifics`
- `test_create_politician_with_invalid_name_raises_error`
- `test_find_by_id_returns_none_when_not_found`

## Common Patterns

### Testing Domain Services

```python
class TestSpeakerDomainService:
    @pytest.fixture
    def service(self):
        return SpeakerDomainService()

    def test_normalize_name_removes_honorifics(self, service):
        assert service.normalize_name("山田氏") == "山田"

    def test_normalize_name_handles_empty_string(self, service):
        assert service.normalize_name("") == ""
```

### Testing Use Cases

```python
class TestCreatePoliticianUseCase:
    @pytest.fixture
    def mock_repo(self):
        return AsyncMock(spec=IPoliticianRepository)

    @pytest.fixture
    def usecase(self, mock_repo):
        return CreatePoliticianUseCase(politician_repository=mock_repo)

    @pytest.mark.asyncio
    async def test_execute_creates_politician(self, usecase, mock_repo):
        # Arrange
        input_dto = CreatePoliticianInputDTO(name="Test", party_id=1)
        mock_repo.save.return_value = Politician(id=1, name="Test", party_id=1)

        # Act
        output = await usecase.execute(input_dto)

        # Assert
        assert output.success
        mock_repo.save.assert_called_once()
```

### Testing Repositories (Integration)

```python
@pytest.mark.integration
class TestPoliticianRepositoryImpl:
    @pytest.fixture
    async def repo(self, db_session):
        return PoliticianRepositoryImpl(session=db_session)

    @pytest.mark.asyncio
    async def test_save_and_find(self, repo):
        # Arrange
        politician = Politician(id=None, name="Test", party_id=1)

        # Act
        saved = await repo.save(politician)
        found = await repo.find_by_id(saved.id)

        # Assert
        assert found is not None
        assert found.name == "Test"
```

## Coverage

```bash
# Run with coverage
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html

# Target: 80%+ coverage
```

## Performance

### Profiling Slow Tests

```bash
# Show slowest tests
pytest --durations=10

# Profile specific test
pytest --profile test_slow.py
```

### Optimizing Tests

1. Use fixtures to share setup
2. Mock expensive operations
3. Use `@pytest.mark.slow` for slow tests
4. Run fast tests first

## CI/CD Integration

### pytest.ini Configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --tb=short
    --disable-warnings
markers =
    asyncio: Async tests
    integration: Integration tests
    evaluation: Evaluation tests (not run in CI)
    slow: Slow tests
```

### Exclude Evaluation Tests in CI

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    pytest tests/ -m "not evaluation"
```

## Troubleshooting

### Event Loop Errors

```python
# Error: Event loop is closed
# Fix: Use pytest-asyncio
@pytest.mark.asyncio
async def test_async():
    ...
```

### Mock Not Working

```python
# Error: Mock not called
# Fix: Check if you're awaiting async mocks
await mock.method()  # Not: mock.method()
```

### Import Errors

```python
# Error: Module not found
# Fix: Ensure PYTHONPATH includes src/
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```
