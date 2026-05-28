---
name: chat-agent-flow
description: Eco² Chat 서비스 E2E 테스트 및 디버깅 가이드. API 엔드포인트, SSE 이벤트 스트림, Redis Streams 파이프라인, Intent 분류 시스템. Use when: (1) Chat API E2E 테스트 시, (2) SSE 이벤트 수신 문제 해결 시, (3) Intent 분류/라우팅 확인 시, (4) Redis Streams 이벤트 파이프라인 디버깅 시.
---

# Chat Agent Flow Guide

> Chat 서비스 E2E 테스트 및 이벤트 파이프라인 가이드

## Quick Reference

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Chat Agent E2E Flow                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [1] POST /api/v1/chat              →  Create session (chat_id)             │
│  [2] POST /api/v1/chat/{id}/messages →  Send message (job_id)               │
│  [3] GET  /api/v1/chat/{job_id}/events →  Subscribe SSE (via chat-vs)       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## API Endpoints

| Step | Endpoint | Service | Response |
|------|----------|---------|----------|
| 1 | `POST /api/v1/chat` | chat-api | `{id, title, created_at}` |
| 2 | `POST /api/v1/chat/{chat_id}/messages` | chat-api | `{job_id, stream_url, status}` |
| 3 | `GET /api/v1/chat/{job_id}/events` | sse-gateway (via chat-vs) | SSE stream |

### API Endpoint 역할 상세

| Endpoint | 역할 | DB 영향 | Worker 제출 |
|----------|------|---------|-------------|
| `POST /chat` | 세션 생성 | `chat.conversations` INSERT | **NO** |
| `POST /chat/{id}/messages` | 메시지 전송 | 없음 (Worker 완료 후 배치) | **YES** (RabbitMQ) |
| `GET /chat/{job_id}/events` | SSE 구독 | 없음 | - |

⚠️ **중요**: `POST /chat`만 호출하면 세션만 생성되고 메시지는 처리되지 않습니다.
메시지를 Worker로 전송하려면 반드시 `POST /chat/{chat_id}/messages`를 호출해야 합니다.

## Istio VirtualService Routing

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Istio Routing Priority (chat-vs)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  순서가 중요! Regex는 Prefix보다 우선순위 낮음 → 같은 VS 내에서 순서로 제어   │
│                                                                              │
│  1. [regex]  /api/v1/chat/[^/]+/events  →  sse-gateway (SSE)                │
│  2. [prefix] /api/v1/chat               →  chat-api (REST)                  │
│                                                                              │
│  ⚠️ 순서 바뀌면 SSE 요청이 chat-api로 라우팅됨!                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**파일**: `workloads/routing/chat/base/virtual-service.yaml`

## E2E Test Commands

```bash
TOKEN="<JWT_TOKEN>"

# 1. Create chat session
CHAT_RESPONSE=$(curl -s -X POST "https://api.dev.growbin.app/api/v1/chat" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{"title": "E2E Test"}')
CHAT_ID=$(echo $CHAT_RESPONSE | jq -r '.id')

# 2. Send message
MSG_RESPONSE=$(curl -s -X POST "https://api.dev.growbin.app/api/v1/chat/${CHAT_ID}/messages" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{"message": "플라스틱 분리배출 방법 알려줘"}')
JOB_ID=$(echo $MSG_RESPONSE | jq -r '.job_id')

# 3. Subscribe SSE
curl -sN --max-time 60 \
  "https://api.dev.growbin.app/api/v1/chat/${JOB_ID}/events" \
  -H "Accept: text/event-stream" \
  -H "Cookie: s_access=$TOKEN"
```

## Intent Classification (10 types)

| Intent | Node | Description |
|--------|------|-------------|
| `WASTE` | waste_rag | 분리배출 질문 |
| `CHARACTER` | character | 캐릭터 정보 (gRPC) |
| `LOCATION` | location | 장소 검색 (Kakao API) |
| `BULK_WASTE` | bulk_waste | 대형폐기물 |
| `RECYCLABLE_PRICE` | recyclable_price | 재활용 시세 |
| `COLLECTION_POINT` | collection_point | 수거함 위치 (KECO API) |
| `WEB_SEARCH` | web_search | 웹 검색 |
| `IMAGE_GENERATION` | image_generation | 이미지 생성 |
| `GENERAL` | general | 일반 대화 |
| (weather) | weather | 날씨 enrichment (자동 추가) |

## Dynamic Routing (Send API)

```python
# Multi-Intent: "종이 버리는 법이랑 수거함도 알려줘"
→ intent = "waste"
→ additional_intents = ["collection_point"]
→ Sends:
   - Send("waste_rag", state)         # 주 intent
   - Send("collection_point", state)  # multi-intent
   - Send("weather", state)           # enrichment rule

# 3개 노드 병렬 실행!
```

## Redis Streams Event Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Redis Streams Event Pipeline                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [1] chat-worker                                                             │
│       │                                                                      │
│       │ XADD chat:events:{shard} (Redis Streams)                            │
│       ▼                                                                      │
│  [2] rfr-streams-redis (Redis Sentinel)                                     │
│       │                                                                      │
│       │ XREADGROUP (Consumer Group)                                         │
│       ▼                                                                      │
│  [3] event-router                                                            │
│       │                                                                      │
│       │ PUBLISH sse:events:{job_id} (Redis Pub/Sub)                         │
│       ▼                                                                      │
│  [4] rfr-pubsub-redis (Redis Sentinel)                                      │
│       │                                                                      │
│       │ SUBSCRIBE (SSE Gateway)                                              │
│       ▼                                                                      │
│  [5] sse-gateway → SSE Stream → Client                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Redis Instances

| Instance | Namespace | Purpose | Protocol |
|----------|-----------|---------|----------|
| `rfr-streams-redis` | redis | Event Streams (XADD/XREADGROUP) | Redis Streams |
| `rfr-pubsub-redis` | redis | SSE Broadcast (PUBLISH/SUBSCRIBE) | Redis Pub/Sub |

## Message Persistence Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Message Persistence Pipeline                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [1] chat-worker                                                             │
│       │                                                                      │
│       │ XADD chat:events:{shard} (done event 포함)                           │
│       ▼                                                                      │
│  [2] Redis Streams                                                           │
│       │                                                                      │
│       ├──► Consumer Group: eventrouter → event-router → SSE                 │
│       │                                                                      │
│       └──► Consumer Group: chat-persistence → chat-persistence-consumer                 │
│                   │                                                          │
│                   ▼                                                          │
│  [3] chat-persistence-consumer (ChatPersistenceConsumer)                                │
│       │                                                                      │
│       │ INSERT INTO chat.messages                                            │
│       ▼                                                                      │
│  [4] PostgreSQL (chat.messages)                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Persistence Components

| Component | Namespace | Image | Entry Point |
|-----------|-----------|-------|-------------|
| chat-persistence-consumer | chat | chat-api-dev-latest | `python -m chat.persistence_consumer` |

### Consumer Group 확인

```bash
# Consumer Group 목록 조회
kubectl exec -n redis rfr-streams-redis-0 -c redis -- \
  redis-cli XINFO GROUPS chat:events:0

# Expected:
# 1) name: eventrouter
# 2) name: chat-persistence

# 메시지 수 확인
kubectl exec -n postgres deploy/postgresql -- \
  psql -U sesacthon -d ecoeco -c "SELECT COUNT(*) FROM chat.messages;"
```

### Persistence 관련 테이블

| Table | Schema | Purpose |
|-------|--------|---------|
| `chat.conversations` | chat | 대화 세션 |
| `chat.messages` | chat | 메시지 내용 |
| `checkpoints` | public | LangGraph 체크포인트 |
| `checkpoint_blobs` | public | 체크포인트 Blob |
| `checkpoint_writes` | public | 체크포인트 Write Log |

### Hop-by-Hop Address Reference

| Hop | Component | Kube DNS | Pod DNS (Master) | Protocol | Port |
|-----|-----------|----------|------------------|----------|------|
| 1→2 | chat-worker → Redis Streams | `rfr-streams-redis.redis.svc.cluster.local` | `rfr-streams-redis-0.rfr-streams-redis.redis.svc.cluster.local` | XADD | 6379 |
| 2→3 | Redis Streams → event-router | (Consumer Group) | - | XREADGROUP | 6379 |
| 3→4 | event-router → Redis Pub/Sub | `rfr-pubsub-redis.redis.svc.cluster.local` | `rfr-pubsub-redis-0.rfr-pubsub-redis.redis.svc.cluster.local` | PUBLISH | 6379 |
| 4→5 | Redis Pub/Sub → sse-gateway | (Subscriber) | - | SUBSCRIBE | 6379 |

### Stream Keys & Patterns

| Key Pattern | Example | Purpose |
|-------------|---------|---------|
| `chat:events:{shard}` | `chat:events:0` ~ `chat:events:3` | Sharded event streams (4 shards) |
| `chat:published:{job_id}:{stage}:{seq}` | `chat:published:abc123:intent:10` | Idempotency marker (TTL 2h) |
| `chat:tokens:{job_id}` | `chat:tokens:abc123` | Token stream for recovery |
| `chat:token_state:{job_id}` | `chat:token_state:abc123` | Accumulated text snapshot |
| `sse:events:{job_id}` | `sse:events:abc123` | Pub/Sub channel for SSE |

### Environment Variables

| Component | Variable | Value (Dev) |
|-----------|----------|-------------|
| chat-worker | `CHAT_WORKER_REDIS_STREAMS_URL` | `redis://rfr-streams-redis.redis.svc.cluster.local:6379/0` |
| chat-worker | `CHAT_WORKER_REDIS_URL` | `redis://rfr-pubsub-redis-0.rfr-pubsub-redis.redis.svc.cluster.local:6379/0` |
| event-router | `REDIS_STREAMS_URL` | `redis://rfr-streams-redis.redis.svc.cluster.local:6379/0` |
| event-router | `REDIS_PUBSUB_URL` | `redis://rfr-pubsub-redis.redis.svc.cluster.local:6379/0` |

### Debug Commands (Redis)

```bash
# Redis Streams 확인 (rfr-streams-redis)
kubectl exec -n redis rfr-streams-redis-0 -- redis-cli XLEN chat:events:0
kubectl exec -n redis rfr-streams-redis-0 -- redis-cli XRANGE chat:events:0 - + COUNT 5

# Pub/Sub 모니터링 (rfr-pubsub-redis)
kubectl exec -n redis rfr-pubsub-redis-0 -- redis-cli PSUBSCRIBE "sse:events:*"

# Consumer Group 상태 확인
kubectl exec -n redis rfr-streams-redis-0 -- redis-cli XINFO GROUPS chat:events:0
```

## Troubleshooting

### Issue 1: SSE 요청이 404

**증상**: `GET /api/v1/chat/{job_id}/events` → 404

**원인**: VirtualService에서 SSE 규칙이 prefix 뒤에 배치

**해결**: `chat-vs`에서 SSE events 규칙을 prefix 규칙 **앞에** 배치

### Issue 2: TaskIQ 메시지 파싱 오류

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

### Issue 3: Redis READONLY 오류

**증상**: `-READONLY You can't write against a read only replica`

**원인**: Headless service가 replica로 연결

**해결**: Master pod DNS 직접 사용

```
rfr-pubsub-redis-0.rfr-pubsub-redis.redis.svc.cluster.local:6379
```

### Issue 4: LangGraph State Access 오류

**증상**: `KeyError: 'job_id'`

**원인**: `astream_events`에서 일부 이벤트에 state 누락

**해결**: `.get()` 메서드로 안전한 접근

```python
# Bad
job_id = state["job_id"]

# Good
job_id = state.get("job_id", "")
```

### Issue 5: Send API 병렬 실행 충돌

**증상**: `InvalidUpdateError: Can receive only one value per step`

**원인**: `StateGraph(dict)` + Send API 병렬 실행

**해결**: Typed State + Annotated Reducer (진행 중)

```python
# 임시: dynamic_routing 비활성화
enable_dynamic_routing=False

# 근본: StateGraph(ChatState) + Reducer
```

### Issue 6: Message Persistence 실패 (chat-persistence-consumer)

**증상**: 대화는 정상 진행되지만 `chat.messages` 테이블에 메시지가 저장되지 않음

**진단**:
```bash
# 1. chat.messages 레코드 수 확인
kubectl exec -n postgres deploy/postgresql -- \
  psql -U sesacthon -d ecoeco -c "SELECT COUNT(*) FROM chat.messages;"

# 2. chat-persistence Consumer Group 확인
kubectl exec -n redis rfr-streams-redis-0 -c redis -- \
  redis-cli XINFO GROUPS chat:events:0 | grep -A5 chat-persistence

# 3. chat-persistence-consumer Pod 상태 확인
kubectl get pods -n chat -l app=chat-persistence-consumer
```

**가능한 원인**:

| 원인 | 증상 | 해결 |
|------|------|------|
| chat-persistence-consumer 미배포 | Pod 없음 | `workloads/domains/chat/base/deployment-persistence-consumer.yaml` 배포 |
| livenessProbe 실패 | CrashLoopBackOff | `/proc/1/cmdline` 패턴 사용 |
| RabbitMQ 큐 불일치 | taskiq 큐에 메시지 쌓임 | `CHAT_RABBITMQ_QUEUE=chat.process` 설정 |

**참조**: `docs/troubleshooting/chat-messages-not-persisted.md`

### Issue 7: SSE 이벤트 수신 불가 (Redis 불일치)

**SSE Event Types (검증됨 - 2026-01-19)**:

| Event | seq 범위 | Description |
|-------|----------|-------------|
| `intent` | 1-999 | Intent 분류 완료 |
| `router` | 1-999 | 라우팅 완료 |
| `answer` | 1-999 | 답변 생성 시작/완료 |
| **`token`** | **1001+** | **실시간 토큰 스트리밍 (핵심!)** |
| `token_recovery` | - | 늦은 구독자용 스냅샷 |
| `done` | 1-999 | 처리 완료 + 최종 결과 |
| `error` | - | 오류 발생 |
| `keepalive` | - | 연결 유지 |

> **상세 형식**: `references/sse-event-format.md` 참조

## Redis Streams Pipeline

```
chat-worker → XADD chat:events:{0-3} → event-router → PUBLISH sse:events:{job_id} → sse-gateway
```

| Instance | Purpose |
|----------|---------|
| `rfr-streams-redis` | Event Streams (XADD/XREADGROUP) |
| `rfr-pubsub-redis` | SSE Broadcast (PUBLISH/SUBSCRIBE) |

## Debug Commands

```bash
# Worker logs
kubectl logs -n chat -l app=chat-worker -f --tail=100

# Event Router logs
kubectl logs -n event-router -l app=event-router -f --tail=50

# Redis Streams check
kubectl exec -n redis rfr-streams-redis-0 -c redis -- redis-cli XLEN chat:events:0
kubectl exec -n redis rfr-streams-redis-0 -c redis -- redis-cli XINFO GROUPS chat:events:0

# Pub/Sub monitoring
kubectl exec -n redis rfr-pubsub-redis-0 -c redis -- redis-cli PSUBSCRIBE "sse:events:*"
```

## Reference Files

- **SSE Event Format**: `references/sse-event-format.md` ← Token streaming 이벤트 형식 상세
- **E2E Test Plan**: `docs/reports/e2e-intent-test-plan.md`
- **Troubleshooting (E2E)**: `docs/troubleshooting/chat-worker-e2e-infra-fixes.md`
- **Troubleshooting (Persistence)**: `docs/troubleshooting/chat-messages-not-persisted.md`
- **VirtualService (Chat)**: `workloads/routing/chat/base/virtual-service.yaml`
- **VirtualService (SSE)**: `workloads/domains/sse-gateway/base/virtualservice.yaml`
- **Frontend Spec**: `docs/specs/chat-agent-frontend-spec.md`
- **Dynamic Routing**: `docs/blogs/applied/30-langgraph-dynamic-routing-send-api.md`
- **Native Streaming**: `docs/blogs/applied/32-langgraph-native-streaming.md`

## Related Documents

| PR | Title | Issue |
|----|-------|-------|
| #400 | fix(routing): chat SSE 이벤트를 sse-gateway로 라우팅 | SSE 라우팅 오류 |
| #401 | fix(chat): TaskIQ 메시지 형식 수정 | 메시지 파싱 오류 |
| #408-410 | fix(chat_worker): BaseCheckpointSaver 상속 | Checkpointer 오류 |
| #411 | fix(chat-worker): Redis URL 수정 | DNS 해석 실패 |
| #412 | fix(chat-worker): Master pod DNS 사용 | READONLY 오류 |
| #413 | fix(chat_worker): max_completion_tokens 사용 | OpenAI API 오류 |
| #415 | feat(chat_worker): Channel Separation + Priority | Send API 병렬 충돌 |
| #422-424 | feat(chat): ChatPersistenceConsumer 배포 | 메시지 영속화 |
| #425 | fix(chat): CachedPostgresSaver 트랜잭션 | CREATE INDEX CONCURRENTLY 오류 |
| #440 | fix(chat_worker): LangChain LLM 직접 호출로 토큰 스트리밍 | stream_mode="messages" 캡처 안됨 |
