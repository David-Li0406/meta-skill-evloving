# LangGraph 패턴

## 1. Sequential Flow

가장 단순한 순차 실행 패턴.

```python
from langgraph.graph import END, StateGraph

graph = StateGraph(dict)

graph.add_node("step1", step1_node)
graph.add_node("step2", step2_node)
graph.add_node("step3", step3_node)

graph.add_edge("step1", "step2")
graph.add_edge("step2", "step3")
graph.add_edge("step3", END)

graph.set_entry_point("step1")
```

---

## 2. Branching Flow (조건부 분기)

의도/조건에 따라 다른 경로로 분기.

```python
def route_decision(state: dict) -> str:
    """상태 기반 라우팅 결정"""
    if state.get("needs_verification"):
        return "verify"
    if state.get("confidence", 0) < 0.7:
        return "clarify"
    return "proceed"

graph.add_conditional_edges(
    "classifier",
    route_decision,
    {
        "verify": "verification_node",
        "clarify": "clarification_node",
        "proceed": "execution_node",
    }
)
```

---

## 3. Fan-out / Fan-in (병렬 처리)

여러 노드로 분산 후 결과 통합.

```python
# Fan-out: 여러 노드로 동시 분기
graph.add_conditional_edges(
    "dispatcher",
    lambda s: ["node_a", "node_b", "node_c"],  # 리스트 반환
    {
        "node_a": "processor_a",
        "node_b": "processor_b",
        "node_c": "processor_c",
    }
)

# Fan-in: 결과 통합
graph.add_edge("processor_a", "aggregator")
graph.add_edge("processor_b", "aggregator")
graph.add_edge("processor_c", "aggregator")
```

---

## 4. Loop Pattern (반복/재시도)

조건 만족까지 반복 실행.

```python
def should_continue(state: dict) -> str:
    """반복 조건 판단"""
    if state.get("retry_count", 0) >= 3:
        return "fail"
    if state.get("success"):
        return "done"
    return "retry"

graph.add_conditional_edges(
    "executor",
    should_continue,
    {
        "retry": "executor",  # 자기 자신으로 루프
        "done": "success_handler",
        "fail": "failure_handler",
    }
)
```

---

## 5. Human-in-the-Loop

사용자 입력 대기 패턴.

```python
from langgraph.checkpoint.base import BaseCheckpointSaver

async def human_input_node(state: dict) -> dict:
    """사용자 입력 요청 - interrupt 발생"""
    # 이 노드에서 interrupt 발생
    # 사용자 응답 후 재개됨
    return {"awaiting_input": True}

# 컴파일 시 interrupt_before 설정
compiled = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["human_input_node"]
)

# 실행 후 중단된 지점에서 재개
result = await compiled.ainvoke(
    {"user_response": "approved"},
    config={"configurable": {"thread_id": thread_id}}
)
```

---

## 6. Subgraph Pattern

복잡한 로직을 서브그래프로 분리.

```python
# 서브그래프 정의
def create_rag_subgraph() -> StateGraph:
    subgraph = StateGraph(dict)
    subgraph.add_node("retrieve", retrieve_node)
    subgraph.add_node("rerank", rerank_node)
    subgraph.add_node("generate", generate_node)

    subgraph.add_edge("retrieve", "rerank")
    subgraph.add_edge("rerank", "generate")
    subgraph.set_entry_point("retrieve")

    return subgraph

# 메인 그래프에 서브그래프 노드로 추가
main_graph = StateGraph(dict)
rag_subgraph = create_rag_subgraph()

main_graph.add_node("intent", intent_node)
main_graph.add_node("rag", rag_subgraph.compile())  # 컴파일된 서브그래프
main_graph.add_node("answer", answer_node)

main_graph.add_edge("intent", "rag")
main_graph.add_edge("rag", "answer")
```

---

## 7. Feedback Loop Pattern (Eco² 패턴)

품질 평가 후 재시도하는 피드백 루프.

```python
def evaluate_quality(state: dict) -> str:
    """응답 품질 평가"""
    quality = state.get("quality_score", 0)

    if quality >= 0.8:
        return "accept"
    if state.get("feedback_count", 0) >= 2:
        return "fallback"
    return "refine"

graph.add_node("generate", generate_node)
graph.add_node("evaluate", evaluate_node)
graph.add_node("refine", refine_node)
graph.add_node("fallback", fallback_node)

graph.add_edge("generate", "evaluate")
graph.add_conditional_edges(
    "evaluate",
    evaluate_quality,
    {
        "accept": END,
        "refine": "refine",
        "fallback": "fallback",
    }
)
graph.add_edge("refine", "generate")  # 루프백
graph.add_edge("fallback", END)
```

---

## 노드 작성 Best Practices

### 1. 순수 함수로 작성

```python
# GOOD: 부수 효과 없는 순수 함수
async def process_node(state: dict) -> dict:
    result = await processor.process(state["input"])
    return {"output": result}

# BAD: 외부 상태 변경
async def process_node(state: dict) -> dict:
    global_counter += 1  # 부수 효과!
    return {"output": result}
```

### 2. 필요한 필드만 반환

```python
# GOOD: 업데이트할 필드만 반환
async def intent_node(state: dict) -> dict:
    return {"intent": "waste_query"}

# BAD: 전체 상태 복사 후 반환
async def intent_node(state: dict) -> dict:
    new_state = state.copy()
    new_state["intent"] = "waste_query"
    return new_state
```

### 3. 에러 처리는 State로

```python
async def risky_node(state: dict) -> dict:
    try:
        result = await risky_operation()
        return {"result": result, "error": None}
    except ServiceError as e:
        return {"result": None, "error": str(e)}
```
