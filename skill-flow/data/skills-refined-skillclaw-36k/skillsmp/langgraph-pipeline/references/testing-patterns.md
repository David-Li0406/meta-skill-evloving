# LangGraph 테스트 패턴

## 테스트 전략

```
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph Testing Pyramid                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                        E2E Tests                                 │
│                    (Full Pipeline Flow)                          │
│                          ▲                                       │
│                         / \                                      │
│                        /   \                                     │
│               Integration Tests                                  │
│           (Node + Dependencies)                                  │
│                      ▲                                           │
│                     / \                                          │
│                    /   \                                         │
│                Unit Tests                                        │
│            (Individual Nodes)                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Unit Tests (노드 단위)

### 개별 노드 테스트

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_intent_node_classifies_waste_query():
    """의도 분류 노드가 분리배출 질문을 올바르게 분류"""
    # Arrange
    mock_classifier = AsyncMock()
    mock_classifier.classify.return_value = IntentResult(
        intent="waste_query",
        confidence=0.95,
    )

    node = create_intent_node(mock_classifier)
    state = {"query": "플라스틱 분리배출 방법"}

    # Act
    result = await node(state)

    # Assert
    assert result["intent"] == "waste_query"
    assert result["confidence"] == 0.95
    mock_classifier.classify.assert_called_once_with("플라스틱 분리배출 방법")


@pytest.mark.asyncio
async def test_intent_node_handles_unknown_intent():
    """알 수 없는 의도는 general로 분류"""
    # Arrange
    mock_classifier = AsyncMock()
    mock_classifier.classify.return_value = IntentResult(
        intent="unknown",
        confidence=0.3,
    )

    node = create_intent_node(mock_classifier)
    state = {"query": "오늘 날씨 어때?"}

    # Act
    result = await node(state)

    # Assert
    assert result["intent"] == "general"
```

### 라우팅 함수 테스트

```python
def test_route_by_intent_returns_waste_node():
    """waste_query 의도는 waste_node로 라우팅"""
    state = {"intent": "waste_query", "confidence": 0.9}
    assert route_by_intent(state) == "waste_node"


def test_route_by_intent_defaults_to_answer():
    """알 수 없는 의도는 answer로 라우팅"""
    state = {"intent": "unknown"}
    assert route_by_intent(state) == "answer"


@pytest.mark.parametrize("intent,expected", [
    ("waste_query", "waste_node"),
    ("character", "character_node"),
    ("location", "location_node"),
    ("general", "answer"),
])
def test_route_by_intent_parametrized(intent, expected):
    """모든 의도에 대한 라우팅 검증"""
    state = {"intent": intent}
    assert route_by_intent(state) == expected
```

---

## Integration Tests (노드 + 의존성)

### 실제 LLM 없이 파이프라인 테스트

```python
import pytest
from langgraph.graph import StateGraph
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_dependencies():
    """모든 의존성을 Mock으로 생성"""
    return {
        "llm": AsyncMock(spec=LLMClientPort),
        "retriever": AsyncMock(spec=RetrieverPort),
        "character_client": AsyncMock(spec=CharacterClientPort),
        "checkpointer": MagicMock(),
    }


@pytest.mark.asyncio
async def test_waste_query_flow(mock_dependencies):
    """분리배출 질문 전체 플로우 테스트"""
    # Arrange
    mock_dependencies["retriever"].retrieve.return_value = [
        {"content": "플라스틱은 깨끗이 씻어서...", "score": 0.9}
    ]
    mock_dependencies["llm"].generate.return_value = "플라스틱 분리배출 방법입니다."

    graph = create_chat_graph(**mock_dependencies)
    compiled = graph.compile()

    # Act
    result = await compiled.ainvoke({
        "query": "플라스틱 분리배출",
        "intent": "waste_query",
    })

    # Assert
    assert "플라스틱" in result["answer"]
    mock_dependencies["retriever"].retrieve.assert_called_once()
    mock_dependencies["llm"].generate.assert_called_once()
```

### Subagent 통합 테스트

```python
@pytest.mark.asyncio
async def test_character_subagent_integration(mock_dependencies):
    """캐릭터 Subagent 통합 테스트"""
    # Arrange
    mock_dependencies["character_client"].get_character.return_value = {
        "name": "에코",
        "message": "안녕! 나는 에코야!",
    }

    graph = create_chat_graph(**mock_dependencies)
    compiled = graph.compile()

    # Act
    result = await compiled.ainvoke({
        "query": "캐릭터 정보",
        "intent": "character",
    })

    # Assert
    assert result["character_response"] is not None
    mock_dependencies["character_client"].get_character.assert_called_once()
```

---

## E2E Tests (전체 파이프라인)

### 실제 서비스 연동 테스트

```python
import pytest

@pytest.fixture(scope="module")
async def real_graph():
    """실제 의존성으로 그래프 생성 (E2E용)"""
    # 실제 서비스 연결
    llm = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
    retriever = LocalAssetRetriever(asset_path="./assets")

    graph = create_chat_graph(
        llm=llm,
        retriever=retriever,
        checkpointer=None,  # E2E에선 checkpointer 생략 가능
    )

    return graph.compile()


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_full_waste_query_flow(real_graph):
    """실제 분리배출 질문 E2E 테스트"""
    result = await real_graph.ainvoke({
        "query": "페트병 분리배출 방법 알려줘",
    })

    assert result["answer"]
    assert len(result["answer"]) > 50
    assert "페트" in result["answer"] or "플라스틱" in result["answer"]
```

---

## Checkpointer 테스트

```python
@pytest.mark.asyncio
async def test_multi_turn_conversation():
    """다중 턴 대화 테스트"""
    # Arrange
    from langgraph.checkpoint.memory import MemorySaver

    checkpointer = MemorySaver()
    graph = create_chat_graph(
        llm=mock_llm,
        retriever=mock_retriever,
        checkpointer=checkpointer,
    )
    compiled = graph.compile(checkpointer=checkpointer)

    thread_id = "test-thread-1"
    config = {"configurable": {"thread_id": thread_id}}

    # Act - Turn 1
    result1 = await compiled.ainvoke(
        {"query": "플라스틱 분리배출"},
        config=config,
    )

    # Act - Turn 2 (같은 thread_id)
    result2 = await compiled.ainvoke(
        {"query": "페트병은 어떻게?"},
        config=config,
    )

    # Assert
    # 두 번째 턴에서 이전 컨텍스트 활용 확인
    assert result2["answer"]
    # 히스토리에 두 개의 메시지가 있어야 함
    state = await compiled.aget_state(config)
    assert len(state.values.get("messages", [])) >= 2
```

---

## Mock 패턴

### Port Mock Factory

```python
def create_mock_llm(
    response: str = "Mock response",
    raise_error: bool = False,
) -> AsyncMock:
    """LLM Mock 생성 팩토리"""
    mock = AsyncMock(spec=LLMClientPort)

    if raise_error:
        mock.generate.side_effect = LLMError("API Error")
    else:
        mock.generate.return_value = response

    return mock


def create_mock_retriever(
    documents: list[dict] | None = None,
) -> AsyncMock:
    """Retriever Mock 생성 팩토리"""
    mock = AsyncMock(spec=RetrieverPort)
    mock.retrieve.return_value = documents or [
        {"content": "Mock document", "score": 0.9}
    ]
    return mock
```

### Fixture 조합

```python
@pytest.fixture
def graph_with_mocks(
    mock_llm,
    mock_retriever,
    mock_character_client,
):
    """Mock 의존성으로 그래프 생성"""
    return create_chat_graph(
        llm=mock_llm,
        retriever=mock_retriever,
        character_client=mock_character_client,
    )
```

---

## 테스트 마커

```python
# pytest.ini 또는 pyproject.toml
[tool.pytest.ini_options]
markers = [
    "unit: Unit tests (fast, no external deps)",
    "integration: Integration tests (may use mocks)",
    "e2e: End-to-end tests (requires real services)",
    "slow: Slow tests (LLM calls, etc.)",
]

# 실행 예시
# pytest -m unit           # 유닛 테스트만
# pytest -m "not e2e"      # E2E 제외
# pytest -m "not slow"     # 느린 테스트 제외
```

---

## 디버깅 팁

### State 추적

```python
@pytest.mark.asyncio
async def test_with_state_tracking():
    """각 노드의 State 변화 추적"""
    states = []

    async def tracking_wrapper(node_fn):
        async def wrapper(state):
            result = await node_fn(state)
            states.append({
                "node": node_fn.__name__,
                "input": state.copy(),
                "output": result,
            })
            return result
        return wrapper

    # ... 테스트 후 states 검사
    for s in states:
        print(f"{s['node']}: {s['input']} -> {s['output']}")
```
