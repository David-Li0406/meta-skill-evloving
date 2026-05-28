# gRPC 테스트 패턴

## Mock 전략

Port/Adapter 패턴 덕분에 실제 gRPC 서버 없이 테스트 가능.

```
테스트 레벨:
├── Unit Test: Mock Stub 주입
├── Integration Test: Mock Client 주입
└── E2E Test: 실제 gRPC 서버 사용
```

---

## Unit Test: Stub Mock

```python
# tests/unit/infrastructure/integrations/character/test_grpc_client.py
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import grpc.aio

from apps.chat_worker.infrastructure.integrations.character.grpc_client import (
    CharacterGrpcClient,
)
from apps.chat_worker.infrastructure.integrations.character.proto import (
    character_pb2,
)

@pytest.fixture
def client():
    return CharacterGrpcClient(host="test-host", port=50051)


@pytest.fixture
def mock_response_found():
    """캐릭터 발견 응답"""
    response = MagicMock()
    response.found = True
    response.name = "플라"
    response.character_type = "플라스틱"
    response.dialog = "플라스틱은 깨끗이 씻어서 분리배출해요!"
    response.match_label = "플라스틱"
    return response


@pytest.fixture
def mock_response_not_found():
    """캐릭터 미발견 응답"""
    response = MagicMock()
    response.found = False
    return response


@pytest.mark.asyncio
async def test_get_character_found(client, mock_response_found):
    """캐릭터 조회 성공 테스트"""
    # Arrange
    mock_stub = AsyncMock()
    mock_stub.GetCharacterByMatch = AsyncMock(return_value=mock_response_found)

    with patch.object(client, "_get_stub", return_value=mock_stub):
        # Act
        result = await client.get_character_by_waste_category("플라스틱")

    # Assert
    assert result is not None
    assert result.name == "플라"
    assert result.match_label == "플라스틱"
    mock_stub.GetCharacterByMatch.assert_called_once()


@pytest.mark.asyncio
async def test_get_character_not_found(client, mock_response_not_found):
    """캐릭터 미발견 테스트"""
    mock_stub = AsyncMock()
    mock_stub.GetCharacterByMatch = AsyncMock(return_value=mock_response_not_found)

    with patch.object(client, "_get_stub", return_value=mock_stub):
        result = await client.get_character_by_waste_category("알수없음")

    assert result is None


@pytest.mark.asyncio
async def test_get_character_grpc_error(client):
    """gRPC 에러 처리 테스트"""
    mock_stub = AsyncMock()
    mock_stub.GetCharacterByMatch = AsyncMock(
        side_effect=grpc.aio.AioRpcError(
            code=grpc.StatusCode.UNAVAILABLE,
            initial_metadata=None,
            trailing_metadata=None,
            details="Service unavailable",
        )
    )

    with patch.object(client, "_get_stub", return_value=mock_stub):
        result = await client.get_character_by_waste_category("플라스틱")

    # Graceful degradation
    assert result is None
```

---

## Integration Test: Mock Client

```python
# tests/integration/test_character_node.py
import pytest
from unittest.mock import AsyncMock

from apps.chat_worker.application.ports.character_client import (
    CharacterClientPort,
    CharacterDTO,
)
from apps.chat_worker.infrastructure.orchestration.langgraph.nodes.character_node import (
    create_character_node,
)

@pytest.fixture
def mock_character_client():
    """Mock CharacterClientPort"""
    mock = AsyncMock(spec=CharacterClientPort)
    mock.get_character_by_waste_category.return_value = CharacterDTO(
        name="플라",
        character_type="플라스틱",
        dialog="분리배출 잘 하고 계시네요!",
        match_label="플라스틱",
    )
    return mock


@pytest.fixture
def mock_llm():
    """Mock LLM for category extraction"""
    mock = AsyncMock()
    mock.generate.return_value = "플라스틱"
    return mock


@pytest.mark.asyncio
async def test_character_node_integration(mock_character_client, mock_llm):
    """캐릭터 노드 통합 테스트"""
    # Arrange
    node = create_character_node(
        character_client=mock_character_client,
        llm=mock_llm,
    )

    state = {
        "query": "플라스틱 분리배출 방법 알려줘",
        "job_id": "test-job-1",
    }

    # Act
    result = await node(state)

    # Assert
    assert "character_context" in result
    assert result["character_context"]["name"] == "플라"
    mock_character_client.get_character_by_waste_category.assert_called_once()
```

---

## Mock Client Factory

```python
# tests/mocks/character_client_mock.py
from apps.chat_worker.application.ports.character_client import (
    CharacterClientPort,
    CharacterDTO,
)

class MockCharacterClient(CharacterClientPort):
    """테스트용 Mock 캐릭터 클라이언트"""

    def __init__(
        self,
        characters: list[CharacterDTO] | None = None,
        should_fail: bool = False,
    ):
        self._characters = characters or self._default_characters()
        self._should_fail = should_fail
        self._call_history: list[str] = []

    def _default_characters(self) -> list[CharacterDTO]:
        return [
            CharacterDTO(
                name="플라",
                character_type="플라스틱",
                dialog="플라스틱은 깨끗이 씻어서!",
                match_label="플라스틱",
            ),
            CharacterDTO(
                name="유리",
                character_type="유리",
                dialog="유리병은 색깔별로 분리!",
                match_label="유리",
            ),
        ]

    async def get_character_by_waste_category(
        self,
        waste_category: str,
    ) -> CharacterDTO | None:
        self._call_history.append(f"get_character:{waste_category}")

        if self._should_fail:
            raise RuntimeError("Mock failure")

        for char in self._characters:
            if char.match_label == waste_category:
                return char
        return None

    async def get_catalog(self) -> list[CharacterDTO]:
        self._call_history.append("get_catalog")
        return self._characters

    @property
    def call_history(self) -> list[str]:
        return self._call_history
```

---

## E2E Test: 실제 서버

```python
# tests/e2e/test_grpc_e2e.py
import pytest
import os

from apps.chat_worker.infrastructure.integrations.character.grpc_client import (
    CharacterGrpcClient,
)

@pytest.fixture(scope="module")
async def real_client():
    """실제 gRPC 서버 연결"""
    client = CharacterGrpcClient(
        host=os.getenv("CHARACTER_GRPC_HOST", "localhost"),
        port=int(os.getenv("CHARACTER_GRPC_PORT", "50051")),
    )
    yield client
    await client.close()


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_real_character_lookup(real_client):
    """실제 캐릭터 조회 E2E 테스트"""
    result = await real_client.get_character_by_waste_category("플라스틱")

    # 실제 서버 응답 검증
    assert result is not None
    assert result.name  # 이름이 있어야 함
    assert result.dialog  # 대사가 있어야 함


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_real_catalog(real_client):
    """실제 카탈로그 조회 E2E 테스트"""
    result = await real_client.get_catalog()

    assert isinstance(result, list)
    assert len(result) > 0
```

---

## Fixture Factory 패턴

```python
# tests/conftest.py
import pytest
from tests.mocks.character_client_mock import MockCharacterClient
from tests.mocks.location_client_mock import MockLocationClient

@pytest.fixture
def mock_character_client():
    return MockCharacterClient()


@pytest.fixture
def mock_location_client():
    return MockLocationClient()


@pytest.fixture
def mock_clients(mock_character_client, mock_location_client):
    """모든 Mock 클라이언트 번들"""
    return {
        "character_client": mock_character_client,
        "location_client": mock_location_client,
    }
```

---

## 테스트 마커

```python
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "unit: Unit tests (no external deps)",
    "integration: Integration tests (may use mocks)",
    "e2e: End-to-end tests (requires real services)",
    "grpc: gRPC-related tests",
]

# 실행
# pytest -m "unit and grpc"
# pytest -m "not e2e"
```
