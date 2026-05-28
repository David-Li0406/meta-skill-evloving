# Test Writer Examples

Concrete test examples for each layer in Polibase.

## Domain Service Tests

```python
# tests/unit/domain/test_speaker_domain_service.py
import pytest
from src.domain.services.speaker_domain_service import SpeakerDomainService

class TestSpeakerDomainService:
    @pytest.fixture
    def service(self):
        return SpeakerDomainService()

    def test_normalize_name_removes_honorific_氏(self, service):
        assert service.normalize_name("山田太郎氏") == "山田太郎"

    def test_normalize_name_removes_honorific_君(self, service):
        assert service.normalize_name("山田太郎君") == "山田太郎"

    def test_normalize_name_converts_fullwidth_space(self, service):
        assert service.normalize_name("山田　太郎") == "山田 太郎"

    def test_normalize_name_handles_empty_string(self, service):
        assert service.normalize_name("") == ""

    def test_normalize_name_handles_none(self, service):
        with pytest.raises(AttributeError):
            service.normalize_name(None)
```

## Use Case Tests

```python
# tests/unit/application/test_create_politician_usecase.py
import pytest
from unittest.mock import AsyncMock
from src.application.usecases.create_politician_usecase import CreatePoliticianUseCase
from src.application.dto.politician_dto import CreatePoliticianInputDTO
from src.domain.entities.politician import Politician

class TestCreatePoliticianUseCase:
    @pytest.fixture
    def mock_politician_repo(self):
        mock = AsyncMock()
        return mock

    @pytest.fixture
    def mock_party_repo(self):
        mock = AsyncMock()
        return mock

    @pytest.fixture
    def usecase(self, mock_politician_repo, mock_party_repo):
        return CreatePoliticianUseCase(
            politician_repository=mock_politician_repo,
            party_repository=mock_party_repo
        )

    @pytest.mark.asyncio
    async def test_execute_creates_politician_successfully(
        self, usecase, mock_politician_repo, mock_party_repo
    ):
        # Arrange
        input_dto = CreatePoliticianInputDTO(name="山田太郎", party_id=1)
        mock_party_repo.find_by_id.return_value = MagicMock(id=1, name="テスト党")
        mock_politician_repo.save.return_value = Politician(
            id=1, name="山田太郎", party_id=1
        )

        # Act
        output_dto = await usecase.execute(input_dto)

        # Assert
        assert output_dto.success is True
        assert output_dto.politician_id == 1
        mock_politician_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_fails_when_party_not_found(
        self, usecase, mock_party_repo
    ):
        # Arrange
        input_dto = CreatePoliticianInputDTO(name="Test", party_id=999)
        mock_party_repo.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Party.*not found"):
            await usecase.execute(input_dto)
```

## Repository Integration Tests

```python
# tests/integration/test_politician_repository.py
import pytest
from src.infrastructure.persistence.politician_repository import PoliticianRepositoryImpl
from src.domain.entities.politician import Politician

@pytest.mark.integration
class TestPoliticianRepositoryIntegration:
    @pytest.fixture
    async def repository(self, db_session):
        return PoliticianRepositoryImpl(session=db_session)

    @pytest.mark.asyncio
    async def test_save_and_find_politician(self, repository):
        # Arrange
        politician = Politician(
            id=None,
            name="テスト太郎",
            party_id=1,
            furigana="てすとたろう"
        )

        # Act
        saved = await repository.save(politician)
        found = await repository.find_by_id(saved.id)

        # Assert
        assert found is not None
        assert found.name == "テスト太郎"
        assert found.id == saved.id

    @pytest.mark.asyncio
    async def test_find_by_name_returns_multiple(self, repository):
        # Arrange
        politician1 = Politician(id=None, name="山田太郎", party_id=1)
        politician2 = Politician(id=None, name="山田太郎", party_id=2)
        await repository.save(politician1)
        await repository.save(politician2)

        # Act
        found = await repository.find_by_name("山田太郎")

        # Assert
        assert len(found) >= 2
```

## External Service Tests (Mocked)

```python
# tests/unit/infrastructure/test_gemini_llm_service.py
import pytest
from unittest.mock import AsyncMock, patch
from src.infrastructure.external.gemini_llm_service import GeminiLLMService

class TestGeminiLLMService:
    @pytest.fixture
    def mock_genai(self):
        with patch('src.infrastructure.external.gemini_llm_service.genai') as mock:
            mock_model = AsyncMock()
            mock_model.generate_content_async.return_value.text = "Mocked LLM response"
            mock.GenerativeModel.return_value = mock_model
            yield mock

    @pytest.mark.asyncio
    async def test_generate_text_returns_response(self, mock_genai):
        # Arrange
        service = GeminiLLMService(api_key="fake-api-key")
        prompt = "Test prompt"

        # Act
        response = await service.generate_text(prompt)

        # Assert
        assert response == "Mocked LLM response"
        # No actual API call was made!

    @pytest.mark.asyncio
    async def test_generate_text_handles_error(self, mock_genai):
        # Arrange
        service = GeminiLLMService(api_key="fake-api-key")
        mock_genai.GenerativeModel.return_value.generate_content_async.side_effect = \
            Exception("API Error")

        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            await service.generate_text("prompt")
```

## Parametrized Tests

```python
# tests/unit/domain/test_speaker_domain_service_parametrized.py
import pytest
from src.domain.services.speaker_domain_service import SpeakerDomainService

class TestSpeakerNormalization:
    @pytest.mark.parametrize("input_name,expected", [
        ("山田太郎氏", "山田太郎"),
        ("山田太郎君", "山田太郎"),
        ("山田太郎議員", "山田太郎"),
        ("山田太郎委員", "山田太郎"),
        ("山田太郎", "山田太郎"),  # No honorific
        ("山田　太郎", "山田 太郎"),  # Fullwidth space
        ("  山田太郎  ", "山田太郎"),  # Extra spaces
    ])
    def test_normalize_name(self, input_name, expected):
        service = SpeakerDomainService()
        assert service.normalize_name(input_name) == expected
```

## conftest.py Examples

```python
# tests/conftest.py
import pytest
import asyncio
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.domain.entities.politician import Politician

# Async fixtures
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def db_session():
    """Test database session."""
    engine = create_async_engine("postgresql+asyncpg://test_user:test_pass@localhost/test_db")
    async with AsyncSession(engine) as session:
        yield session
    await engine.dispose()

# Mock fixtures
@pytest.fixture
def mock_llm_service():
    """Mock LLM service for all tests."""
    mock = AsyncMock()
    mock.generate_text.return_value = "Mocked LLM response"
    return mock

@pytest.fixture
def mock_storage_service():
    """Mock storage service."""
    mock = AsyncMock()
    mock.upload.return_value = "gs://bucket/file.pdf"
    mock.download.return_value = b"PDF content"
    return mock

# Sample data fixtures
@pytest.fixture
def sample_politician():
    """Sample politician for tests."""
    return Politician(
        id=1,
        name="山田太郎",
        party_id=1,
        furigana="やまだたろう",
        district="東京都"
    )

@pytest.fixture
def sample_politicians():
    """Multiple sample politicians."""
    return [
        Politician(id=1, name="山田太郎", party_id=1),
        Politician(id=2, name="鈴木一郎", party_id=2),
        Politician(id=3, name="田中花子", party_id=1),
    ]
```

## Anti-Pattern Examples

### ❌ BAD: Real API Call

```python
# DON'T DO THIS!
async def test_llm_generation():
    service = GeminiLLMService(api_key=os.getenv("GOOGLE_API_KEY"))
    response = await service.generate_text("Test")  # Real API call!
    assert response
```

### ✅ GOOD: Mocked Service

```python
async def test_llm_generation():
    mock_service = AsyncMock(spec=ILLMService)
    mock_service.generate_text.return_value = "Expected response"
    response = await mock_service.generate_text("Test")
    assert response == "Expected response"
```

### ❌ BAD: Test Dependency

```python
# DON'T DO THIS!
def test_create_politician():
    politician = create_politician("Test")
    assert politician.id == 1

def test_find_politician():
    politician = find_politician(1)  # Depends on previous test!
    assert politician.name == "Test"
```

### ✅ GOOD: Independent Tests

```python
def test_find_politician(mock_repo):
    mock_repo.find_by_id.return_value = Politician(id=1, name="Test")
    politician = find_politician(1)
    assert politician.name == "Test"
```

### ❌ BAD: Testing Implementation

```python
# DON'T DO THIS!
def test_private_method():
    service = SomeService()
    result = service._internal_method()  # Testing private method
    assert result
```

### ✅ GOOD: Testing Public Interface

```python
def test_public_behavior():
    service = SomeService()
    result = service.public_method()  # Test public interface
    assert result == expected_output
```
