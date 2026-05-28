---
name: langgraph-pipeline
description: LangGraph 1.0+ 파이프라인 구축 가이드. Intent-Routed Workflow, Subagent 패턴, Checkpointing, Conditional Routing 구현 시 참조. "langgraph", "pipeline", "graph", "workflow", "subagent", "checkpointer" 키워드로 트리거.
---

# LangGraph Pipeline Guide (v1.0+)

## Eco² 파이프라인 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Intent-Routed Workflow with Subagent                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  START → intent → [vision?] → router ──┬─→ waste ────────┐              │
│                              │         ├─→ character ────┤              │
│                              │         ├─→ location ─────┤──→ answer → END
│                              │         ├─→ web_search ───┤              │
│                              │         └─→ general ──────┘              │
│                              │                                           │
│                              └─→ [feedback_loop] ─→ answer              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## StateGraph 기본 패턴

### Graph 생성 및 컴파일

```python
from langgraph.graph import END, StateGraph

# State는 TypedDict 또는 dict 사용
graph = StateGraph(dict)

# 노드 추가
graph.add_node("intent", intent_node)
graph.add_node("router", router_node)
graph.add_node("answer", answer_node)

# 엣지 추가
graph.add_edge("intent", "router")
graph.add_edge("answer", END)

# 조건부 라우팅
graph.add_conditional_edges(
    "router",
    route_by_intent,  # 라우팅 함수
    {
        "waste": "waste_node",
        "character": "character_node",
        "general": "answer",
    }
)

# 시작점 설정 및 컴파일
graph.set_entry_point("intent")
compiled = graph.compile(checkpointer=checkpointer)
```

### Node 정의 패턴

```python
async def intent_node(state: dict) -> dict:
    """노드는 state를 받아 업데이트할 필드만 반환"""
    intent = await classifier.classify(state["query"])
    return {
        "intent": intent.value,
        "confidence": intent.confidence,
    }
```

## Checkpointing (Cache-Aside 패턴)

### L1: Redis + L2: PostgreSQL

```python
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

class CachedPostgresSaver(BaseCheckpointSaver):
    """Redis L1 캐시 + PostgreSQL L2 영속 저장소"""

    def __init__(
        self,
        redis: Redis,
        pg_saver: AsyncPostgresSaver,
        ttl: int = 3600,
    ):
        self._redis = redis
        self._pg = pg_saver
        self._ttl = ttl

    async def aget(
        self,
        config: RunnableConfig,
    ) -> Checkpoint | None:
        thread_id = config["configurable"]["thread_id"]
        key = f"checkpoint:{thread_id}"

        # L1 캐시 조회
        cached = await self._redis.get(key)
        if cached:
            return self._deserialize(cached)

        # L2 조회 후 L1 캐시
        checkpoint = await self._pg.aget(config)
        if checkpoint:
            await self._redis.setex(
                key,
                self._ttl,
                self._serialize(checkpoint)
            )
        return checkpoint
```

## Conditional Routing

### 의도 기반 라우팅

```python
def route_by_intent(state: dict) -> str:
    """의도에 따라 다음 노드 결정"""
    intent = state.get("intent", "general")

    routing_map = {
        "waste_query": "waste_node",
        "character_query": "character_node",
        "location_query": "location_node",
        "web_search": "web_search_node",
    }

    return routing_map.get(intent, "answer")
```

### 조건부 진입/스킵

```python
def should_use_vision(state: dict) -> str:
    """이미지 존재 여부로 vision 노드 사용 결정"""
    if state.get("image_url"):
        return "vision"
    return "router"

graph.add_conditional_edges(
    "intent",
    should_use_vision,
    {
        "vision": "vision_node",
        "router": "router_node",
    }
)
```

## Subagent 통합 패턴

### gRPC Client 주입

```python
def create_chat_graph(
    llm: LLMClientPort,
    retriever: RetrieverPort,
    character_client: CharacterClientPort | None = None,
    location_client: LocationClientPort | None = None,
    checkpointer: BaseCheckpointSaver | None = None,
) -> StateGraph:
    """Port 기반 의존성 주입으로 Subagent 통합"""

    graph = StateGraph(dict)

    # Subagent 노드는 클라이언트가 주입된 경우에만 추가
    if character_client:
        graph.add_node(
            "character",
            create_character_node(character_client)
        )

    if location_client:
        graph.add_node(
            "location",
            create_location_node(location_client)
        )

    return graph.compile(checkpointer=checkpointer)
```

## Reference Files

- **Graph 패턴**: See [graph-patterns.md](./references/graph-patterns.md)
- **Checkpointing**: See [checkpointing.md](./references/checkpointing.md)
- **State 관리**: See [state-management.md](./references/state-management.md)
- **테스트 패턴**: See [testing-patterns.md](./references/testing-patterns.md)

## LangGraph 1.0 변경사항

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| Prebuilt agents | `langgraph.prebuilt` | `langchain.agents` (deprecated) |
| Breaking changes | - | 없음 |
| Checkpointer | 동일 | 동일 |
| StateGraph API | 동일 | 동일 |

> **Note**: LangGraph 1.0.0 릴리즈는 zero breaking changes. 기존 코드 호환.
