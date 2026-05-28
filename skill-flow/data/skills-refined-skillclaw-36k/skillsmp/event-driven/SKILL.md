---
name: event-driven
description: Redis 기반 Composite Event Bus 패턴 가이드. Event Router, SSE Gateway, Redis Streams/Pub-Sub 구현 시 참조. "event", "sse", "stream", "pubsub", "broadcast", "realtime" 키워드로 트리거.
---

# Event-Driven Architecture Guide

## Eco² Composite Event Bus 아키텍처

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Composite Event Bus Architecture                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Producers (Workers)                                                 │
│  ├─ scan-worker (Celery)         → Redis Streams (Durable)          │
│  ├─ chat-worker (LangGraph)      → {domain}:events:{shard}          │
│  └─ character-worker                                                 │
│                                    │                                 │
│                                    ▼                                 │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │         Event Router (Event Bus Layer)                          │ │
│  │  ├─ Consumer: XREADGROUP (Consumer Group)                       │ │
│  │  ├─ Processor: Lua Script (State + Pub/Sub coordination)        │ │
│  │  ├─ Reclaimer: XAUTOCLAIM (Fault Recovery)                      │ │
│  │  └─ Publisher: Redis Pub/Sub (Real-time delivery)               │ │
│  └────────────────────────────────────────────────────────────────┘ │
│           │                                      │                   │
│     Streams Redis                          Pub/Sub Redis             │
│    (Durable Buffer)                       (Real-time Fan-out)        │
│     ├─ {domain}:state:{job_id}            └─ sse:events:{job_id}    │
│           │                                      │                   │
│           └──────────────────────────────────────┘                   │
│                                │                                     │
│                                ▼                                     │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │     SSE Gateway (Consumer/Publisher)                           │ │
│  │  ├─ Subscribe: Redis Pub/Sub channels                          │ │
│  │  ├─ Recovery: State KV polling                                 │ │
│  │  └─ Output: EventSource streaming                              │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                │                                     │
│                                ▼                                     │
│  Clients (Frontend) → EventSource API                                │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## 왜 Redis인가? (vs Kafka/RabbitMQ)

| Aspect | Kafka | RabbitMQ | Redis (Eco²) |
|--------|-------|----------|--------------|
| 용도 | 대용량 스트리밍 | Task Queue | SSE 실시간 전송 |
| Latency | ~10ms | ~5ms | <1ms |
| Fan-out | Consumer Group | Exchange | Pub/Sub |
| 영속성 | 파티션 로그 | Queue | Streams + KV |
| 운영 복잡도 | 높음 (ZK/KRaft) | 중간 | 낮음 |

**Eco² 선택 이유**: SSE는 다수 클라이언트에 저지연 fan-out 필요 → Redis Pub/Sub 최적

## Reference Files

- **Event Router**: See [event-router.md](./references/event-router.md)
- **SSE Gateway**: See [sse-gateway.md](./references/sse-gateway.md)
- **Idempotency 패턴**: See [idempotency.md](./references/idempotency.md)
- **Failure Recovery**: See [failure-recovery.md](./references/failure-recovery.md)
- **ACK Policy**: See [ack-policy.md](./references/ack-policy.md) ⚠️ Critical
- **Reclaimer 패턴**: See [reclaimer-patterns.md](./references/reclaimer-patterns.md)
- **SSE 표준**: See [sse-standard.md](./references/sse-standard.md)

## 핵심 컴포넌트

### 1. Event Publishing (Worker → Streams)

```python
# Idempotent XADD with Lua Script
async def publish_stage_event(
    job_id: str,
    stage: str,
    seq: int,
    status: str,
    data: dict,
) -> bool:
    """멱등성 보장 이벤트 발행"""
    shard = md5_hash(job_id) % SHARD_COUNT
    stream_key = f"{domain}:events:{shard}"
    publish_key = f"published:{job_id}:{stage}:{seq}"

    # Lua Script: Check → XADD → Mark
    result = await redis.eval(
        IDEMPOTENT_XADD_SCRIPT,
        keys=[stream_key, publish_key],
        args=[event_json, TTL],
    )
    return result == 1
```

### 2. Event Router Consumer

⚠️ **Critical: ACK는 처리 성공 시에만** - See [ack-policy.md](./references/ack-policy.md)

```python
async def consume_loop():
    """XREADGROUP 기반 이벤트 소비 - ACK on Success Only"""
    while True:
        messages = await redis.xreadgroup(
            groupname="eventrouter",
            consumername=f"router-{POD_ID}",
            streams={f"{domain}:events:{i}": ">" for i in range(SHARDS)},
            block=5000,
            count=100,
        )

        for stream, events in messages:
            for event_id, data in events:
                data["stream_id"] = event_id  # SSE id 필드용
                try:
                    success = await processor.process(data)
                    if not success:
                        continue  # ACK 스킵 - PEL에 유지
                except Exception:
                    continue  # ACK 스킵 - PEL에 유지
                await redis.xack(stream, "eventrouter", event_id)  # 성공 시만
```

### 3. SSE Gateway Streaming

SSE 표준 `id:` 필드를 포함하여 Last-Event-ID 복구 지원 - See [sse-standard.md](./references/sse-standard.md)

```python
async def stream_events(job_id: str) -> AsyncGenerator[str, None]:
    """SSE 이벤트 스트리밍 (표준 id 필드 포함)"""
    channel = f"sse:events:{job_id}"
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)

    # Recovery: State KV에서 마지막 상태 조회
    state = await redis.get(f"{domain}:state:{job_id}")
    if state:
        event = json.loads(state)
        stream_id = event.get("stream_id", "")
        stage = event.get("stage", "message")
        yield f"event: {stage}\nid: {stream_id}\ndata: {state}\n\n"

    # Real-time: Pub/Sub 구독
    async for message in pubsub.listen():
        if message["type"] == "message":
            event = json.loads(message["data"])
            stream_id = event.get("stream_id", "")
            stage = event.get("stage", "message")
            yield f"event: {stage}\nid: {stream_id}\ndata: {message['data']}\n\n"
```

## 설정

### Event Router

```python
@dataclass
class EventRouterSettings:
    redis_streams_url: str      # XREADGROUP, State KV
    redis_pubsub_url: str       # PUBLISH
    consumer_group: str = "eventrouter"
    shard_count: int = 4
    xread_block_ms: int = 5000
    xread_count: int = 100
    reclaim_min_idle_ms: int = 300000  # 5분
    state_ttl: int = 3600       # 1시간
    published_ttl: int = 7200   # 2시간
```

### SSE Gateway

```python
@dataclass
class SSEGatewaySettings:
    redis_streams_url: str      # State KV
    redis_pubsub_url: str       # Subscribe
    sse_keepalive_interval: float = 15.0
    sse_max_wait_seconds: int = 300
    sse_queue_maxsize: int = 100
```
