---
name: redis-patterns
description: Redis 패턴 가이드. Cache-Aside, Rate Limiting, Pub/Sub, Streams 구현 시 참조. "redis", "cache", "rate limit", "pubsub", "streams" 키워드로 트리거.
---

# Redis Patterns Guide

## Eco² Redis 사용 패턴

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Redis Usage in Eco²                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Cache-Aside (L1)                                                        │
│  ├─ LangGraph Checkpoint 캐시                                           │
│  ├─ Intent Classification 캐시                                          │
│  └─ Session State 캐시                                                  │
│                                                                          │
│  Rate Limiting                                                           │
│  └─ API 요청 제한 (Sliding Window)                                      │
│                                                                          │
│  Pub/Sub                                                                 │
│  └─ SSE 실시간 이벤트 (sse:events:{job_id})                             │
│                                                                          │
│  Streams                                                                 │
│  ├─ 이벤트 버퍼 ({domain}:events:{shard})                               │
│  └─ State KV ({domain}:state:{job_id})                                  │
│                                                                          │
│  Human-in-the-Loop                                                       │
│  ├─ 입력 요청 (input:request:{job_id})                                  │
│  └─ 상호작용 상태 (interaction:state:{job_id})                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 주요 패턴

### 1. Cache-Aside

```python
async def get_with_cache(
    key: str,
    fetch_fn: Callable[[], Awaitable[T]],
    ttl: int = 3600,
) -> T:
    """Cache-Aside 패턴"""
    # 1. 캐시 조회
    cached = await redis.get(key)
    if cached:
        return deserialize(cached)

    # 2. 원본 조회
    data = await fetch_fn()

    # 3. 캐시 저장
    await redis.setex(key, ttl, serialize(data))

    return data
```

### 2. Rate Limiting (Sliding Window)

```python
async def check_rate_limit(
    key: str,
    limit: int,
    window_seconds: int,
) -> bool:
    """Sliding Window Rate Limit"""
    now = time.time()
    window_start = now - window_seconds

    pipe = redis.pipeline()
    pipe.zremrangebyscore(key, 0, window_start)  # 오래된 기록 제거
    pipe.zadd(key, {str(now): now})               # 현재 요청 추가
    pipe.zcard(key)                               # 요청 수 확인
    pipe.expire(key, window_seconds)

    _, _, count, _ = await pipe.execute()
    return count <= limit
```

### 3. Pub/Sub

```python
async def publish_event(job_id: str, event: dict) -> None:
    """이벤트 발행"""
    channel = f"sse:events:{job_id}"
    await redis.publish(channel, json.dumps(event))

async def subscribe_events(job_id: str) -> AsyncIterator[dict]:
    """이벤트 구독"""
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"sse:events:{job_id}")

    async for message in pubsub.listen():
        if message["type"] == "message":
            yield json.loads(message["data"])
```

### 4. Streams (Consumer Group)

```python
async def consume_stream(
    stream: str,
    group: str,
    consumer: str,
) -> AsyncIterator[tuple[str, dict]]:
    """Consumer Group 기반 스트림 소비"""
    while True:
        messages = await redis.xreadgroup(
            groupname=group,
            consumername=consumer,
            streams={stream: ">"},
            block=5000,
            count=100,
        )

        for stream_name, events in messages:
            for event_id, data in events:
                yield event_id, data
                await redis.xack(stream_name, group, event_id)
```

## Reference Files

- **Cache-Aside**: See [cache-aside.md](./references/cache-aside.md)
- **Rate Limiting**: See [rate-limiting.md](./references/rate-limiting.md)
- **Pub/Sub & Streams**: See [messaging.md](./references/messaging.md)

## Redis 인스턴스 분리

### Eco² 클러스터 Redis 서비스

| 인스턴스 | K8s 서비스 | 용도 |
|----------|------------|------|
| **Streams** | `rfr-streams-redis.redis.svc.cluster.local:6379` | Streams, State KV (영속) |
| **Pub/Sub** | `rfr-pubsub-redis.redis.svc.cluster.local:6379` | 실시간 전송 (휘발) |

```yaml
# ConfigMap 환경변수 예시
CHAT_WORKER_REDIS_STREAMS_URL: redis://rfr-streams-redis.redis.svc.cluster.local:6379/0
CHAT_WORKER_REDIS_PUBSUB_URL: redis://rfr-pubsub-redis.redis.svc.cluster.local:6379/0
```

### 인스턴스별 특성

```yaml
rfr-streams-redis:    # Streams, State KV (영속)
  - AOF 활성화
  - Checkpoint 데이터
  - Consumer Group

rfr-pubsub-redis:     # Pub/Sub (휘발)
  - 실시간 전송 전용
  - SSE Gateway 구독
```
