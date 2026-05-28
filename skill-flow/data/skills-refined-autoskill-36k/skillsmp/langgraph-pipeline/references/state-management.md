# State 관리 가이드

## State 정의

LangGraph의 State는 그래프 전체에서 공유되는 데이터 컨테이너.

---

## State 정의 방법

### 1. TypedDict (권장)

```python
from typing import TypedDict, Annotated
from operator import add

class ChatState(TypedDict):
    # 필수 필드
    query: str
    thread_id: str

    # 선택 필드 (기본값 필요 시 Annotated 사용)
    intent: str
    confidence: float
    context: list[str]
    answer: str
    error: str | None

    # 누적 필드 (리스트 append)
    messages: Annotated[list[dict], add]
```

### 2. dict (간단한 경우)

```python
graph = StateGraph(dict)

# 노드에서 자유롭게 필드 추가
async def node(state: dict) -> dict:
    return {"new_field": "value"}
```

### 3. Pydantic Model (검증 필요 시)

```python
from pydantic import BaseModel, Field

class ChatState(BaseModel):
    query: str
    intent: str = ""
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    messages: list[dict] = Field(default_factory=list)

    class Config:
        extra = "allow"  # 추가 필드 허용
```

---

## State Reducer

여러 노드의 출력을 병합하는 방법 정의.

### 기본 동작 (덮어쓰기)

```python
# 같은 키에 대해 마지막 값으로 덮어씀
state = {"count": 1}
update = {"count": 2}
# 결과: {"count": 2}
```

### Annotated Reducer (누적)

```python
from typing import Annotated
from operator import add

class State(TypedDict):
    # add reducer: 리스트 확장
    messages: Annotated[list[str], add]

# 노드 A 반환: {"messages": ["hello"]}
# 노드 B 반환: {"messages": ["world"]}
# 결과: {"messages": ["hello", "world"]}
```

### Custom Reducer

```python
def merge_contexts(existing: list[str], new: list[str]) -> list[str]:
    """중복 제거하며 병합"""
    return list(set(existing + new))

class State(TypedDict):
    contexts: Annotated[list[str], merge_contexts]
```

---

## Eco² ChatState 설계

```python
from typing import TypedDict, Annotated
from operator import add
from enum import Enum

class Intent(str, Enum):
    WASTE_QUERY = "waste_query"
    CHARACTER = "character"
    LOCATION = "location"
    WEB_SEARCH = "web_search"
    GENERAL = "general"

class ChatState(TypedDict):
    """Eco² 챗봇 파이프라인 State"""

    # === 입력 ===
    query: str                          # 사용자 질문
    thread_id: str                      # 세션 ID
    image_url: str | None               # 이미지 (Vision용)

    # === 의도 분류 ===
    intent: str                         # 분류된 의도
    confidence: float                   # 분류 신뢰도
    sub_intents: list[str]              # 복합 의도

    # === RAG ===
    retrieved_docs: list[dict]          # 검색된 문서
    reranked_docs: list[dict]           # 재순위 문서

    # === Subagent 결과 ===
    character_response: dict | None     # 캐릭터 서비스 응답
    location_response: dict | None      # 위치 서비스 응답
    web_search_results: list[dict]      # 웹 검색 결과

    # === 응답 생성 ===
    answer: str                         # 최종 응답
    sources: list[str]                  # 출처 목록

    # === 품질 평가 ===
    quality_score: float                # 응답 품질 점수
    feedback_count: int                 # 피드백 루프 횟수

    # === 메타데이터 ===
    messages: Annotated[list[dict], add]  # 대화 히스토리 (누적)
    error: str | None                   # 에러 메시지
```

---

## State 접근 패턴

### 안전한 접근 (기본값)

```python
async def node(state: dict) -> dict:
    # GOOD: 기본값과 함께 접근
    intent = state.get("intent", "general")
    confidence = state.get("confidence", 0.0)
    messages = state.get("messages", [])

    # BAD: KeyError 위험
    intent = state["intent"]
```

### 타입 가드

```python
async def node(state: ChatState) -> dict:
    # TypedDict 사용 시 타입 힌트 지원
    query: str = state["query"]  # IDE 자동완성

    # Optional 필드는 None 체크
    if state.get("image_url"):
        # Vision 처리
        pass
```

---

## State 불변성

노드는 기존 State를 변경하지 않고 새 값만 반환.

```python
# GOOD: 새 딕셔너리 반환
async def node(state: dict) -> dict:
    return {"answer": "새 응답"}

# BAD: State 직접 수정
async def node(state: dict) -> dict:
    state["answer"] = "새 응답"  # 부수 효과!
    return state

# BAD: 리스트 직접 수정
async def node(state: dict) -> dict:
    state["messages"].append(new_msg)  # 부수 효과!
    return {}
```

---

## State 전파 제어

### 선택적 필드 반환

```python
async def intent_node(state: dict) -> dict:
    # 의도 관련 필드만 반환
    # 다른 필드는 그대로 유지됨
    return {
        "intent": "waste_query",
        "confidence": 0.95,
    }
```

### 조건부 필드

```python
async def rag_node(state: dict) -> dict:
    result = {"retrieved_docs": docs}

    # 조건에 따라 추가 필드
    if high_confidence:
        result["skip_rerank"] = True

    return result
```

---

## 디버깅

### State 로깅

```python
import structlog

logger = structlog.get_logger()

async def debug_node(state: dict) -> dict:
    logger.debug(
        "node_state",
        intent=state.get("intent"),
        confidence=state.get("confidence"),
        doc_count=len(state.get("retrieved_docs", [])),
    )
    return {}
```

### State Snapshot

```python
async def snapshot_state(
    compiled_graph,
    config: dict,
) -> dict:
    """현재 State 스냅샷 조회"""
    state = await compiled_graph.aget_state(config)
    return state.values
```
