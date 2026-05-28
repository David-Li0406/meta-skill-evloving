# Chat Agent Troubleshooting Reference

> E2E 테스트 시 발생하는 일반적인 문제와 해결 방법

## Table of Contents

1. [SSE 404 오류](#issue-1-sse-요청이-404)
2. [TaskIQ 메시지 파싱 오류](#issue-2-taskiq-메시지-파싱-오류)
3. [Redis READONLY 오류](#issue-3-redis-readonly-오류)
4. [LangGraph State Access 오류](#issue-4-langgraph-state-access-오류)
5. [Send API 병렬 실행 충돌](#issue-5-send-api-병렬-실행-충돌)
6. [SSE 이벤트 수신 불가](#issue-6-sse-이벤트-수신-불가-redis-불일치)

---

## Issue 1: SSE 요청이 404

**증상**: `GET /api/v1/chat/{job_id}/events` → 404 Not Found

**원인**: VirtualService에서 SSE regex 규칙이 prefix 규칙 뒤에 배치됨

**VirtualService 순서**:
```yaml
# chat-vs: 순서가 중요!
http:
  # 1. SSE 규칙 (regex) - 먼저 배치!
  - match:
      - uri:
          regex: "/api/v1/chat/[^/]+/events"
    route:
      - destination:
          host: sse-gateway.sse-consumer.svc.cluster.local

  # 2. REST 규칙 (prefix) - 나중에 배치!
  - match:
      - uri:
          prefix: "/api/v1/chat"
    route:
      - destination:
          host: chat-api.chat.svc.cluster.local
```

**해결**: `workloads/routing/chat/base/virtual-service.yaml`에서 SSE 규칙을 prefix 규칙 앞에 배치

---

## Issue 2: TaskIQ 메시지 파싱 오류

**증상**: `Cannot parse message: b'{"args": [], "kwargs": {...}}'`

**원인**: Worker가 `TaskiqMessage` 전체 형식을 기대

**해결**: `task_id`, `task_name`, `labels` 필드 포함

```python
message = {
    "task_id": job_id,
    "task_name": "chat.process",
    "labels": {},
    "args": [],
    "kwargs": {...},
}
```

---

## Issue 3: Redis READONLY 오류

**증상**: `-READONLY You can't write against a read only replica`

**원인**: Headless service가 replica pod로 연결

**진단**:
```bash
# Redis 연결 확인
kubectl exec -n chat deploy/chat-worker -- env | grep REDIS_URL
```

**해결**: Master pod DNS 직접 사용

```
# Bad: Headless Service (replica 연결 가능)
rfr-pubsub-redis.redis.svc.cluster.local:6379

# Good: Master Pod DNS (항상 master)
rfr-pubsub-redis-0.rfr-pubsub-redis.redis.svc.cluster.local:6379
```

---

## Issue 4: LangGraph State Access 오류

**증상**: `KeyError: 'job_id'`

**원인**: `astream_events`에서 일부 이벤트에 state 누락

**해결**: `.get()` 메서드로 안전한 접근

```python
# Bad
job_id = state["job_id"]

# Good
job_id = state.get("job_id", "")
```

---

## Issue 5: Send API 병렬 실행 충돌

**증상**: `InvalidUpdateError: Can receive only one value per step. Use an Annotated key with a reducer.`

**원인**: `StateGraph(dict)` + Send API 병렬 실행 시 동일 key 업데이트 충돌

**임시 해결**: Dynamic routing 비활성화
```python
# dependencies.py
enable_dynamic_routing=False
```

**근본 해결**: Typed State + Annotated Reducer (구현 필요)
```python
from typing import Annotated
from langgraph.graph import StateGraph

class ChatState(TypedDict):
    weather_context: Annotated[dict | None, priority_reducer]
    # ... 각 채널별 reducer

graph = StateGraph(ChatState)
```

**상세**: `docs/plans/langgraph-channel-separation-adr.md`

---

## Issue 6: SSE 이벤트 수신 불가 (Redis 불일치)

**증상**: SSE 연결 성공, keepalive만 수신, 실제 이벤트 없음

**원인**: chat-worker와 event-router가 다른 Redis를 바라봄

```
# 문제 상황
chat-worker   → rfr-pubsub-redis (XADD 잘못된 곳)
event-router  → rfr-streams-redis (XREADGROUP 빈 스트림)
```

**진단**:
```bash
# chat-worker Redis 확인
kubectl exec -n chat deploy/chat-worker -- env | grep REDIS

# event-router Redis 확인
kubectl exec -n event-router deploy/event-router -- env | grep REDIS

# Redis Streams 데이터 확인
kubectl exec -n redis rfr-streams-redis-0 -c redis -- redis-cli XLEN chat:events:0
```

**해결**:
1. `config.py`에 `redis_streams_url` 설정 분리
2. `dependencies.py`에서 RedisProgressNotifier가 `get_redis_streams()` 사용
3. ConfigMap에 `CHAT_WORKER_REDIS_STREAMS_URL` 환경변수 설정

**환경변수**:
```yaml
# chat-worker ConfigMap
CHAT_WORKER_REDIS_URL: redis://rfr-pubsub-redis-0.rfr-pubsub-redis.redis.svc.cluster.local:6379/0
CHAT_WORKER_REDIS_STREAMS_URL: redis://rfr-streams-redis.redis.svc.cluster.local:6379/0
```

---

## Related PRs

| PR | Title | Issue |
|----|-------|-------|
| #400 | fix(routing): chat SSE 이벤트를 sse-gateway로 라우팅 | SSE 404 |
| #401 | fix(chat): TaskIQ 메시지 형식 수정 | 메시지 파싱 |
| #408-410 | fix(chat_worker): BaseCheckpointSaver 상속 | Checkpointer |
| #411 | fix(chat-worker): Redis URL 수정 | DNS 해석 실패 |
| #412 | fix(chat-worker): Master pod DNS 사용 | READONLY |
| #415 | feat(chat_worker): Channel Separation + Priority | Send API 충돌 |
