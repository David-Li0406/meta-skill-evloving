# Event Router 구현 가이드

## 아키텍처

Event Router는 Workers(Producer)와 SSE Gateway(Consumer) 사이의 브릿지 레이어.

```
Workers → Redis Streams → Event Router → Redis Pub/Sub → SSE Gateway
                              ↓
                         State KV (Recovery)
```

---

## Core Components

### 1. StreamConsumer

```python
from dataclasses import dataclass
from redis.asyncio import Redis

@dataclass
class StreamConsumer:
    """Redis Streams Consumer Group 기반 소비자"""

    redis: Redis
    group_name: str
    consumer_name: str
    stream_prefixes: list[str]
    shard_count: int

    async def setup(self) -> None:
        """Consumer Group 생성 (최초 1회)"""
        for prefix in self.stream_prefixes:
            for shard in range(self.shard_count):
                stream = f"{prefix}:{shard}"
                try:
                    await self.redis.xgroup_create(
                        stream,
                        self.group_name,
                        id="0",
                        mkstream=True,
                    )
                except ResponseError as e:
                    if "BUSYGROUP" not in str(e):
                        raise

    async def consume(self) -> AsyncIterator[tuple[str, str, dict]]:
        """이벤트 스트림 소비"""
        streams = {
            f"{prefix}:{shard}": ">"
            for prefix in self.stream_prefixes
            for shard in range(self.shard_count)
        }

        while True:
            messages = await self.redis.xreadgroup(
                groupname=self.group_name,
                consumername=self.consumer_name,
                streams=streams,
                block=5000,
                count=100,
            )

            for stream_name, events in messages:
                for event_id, data in events:
                    yield stream_name, event_id, data

    async def ack(self, stream: str, event_id: str) -> None:
        """메시지 ACK"""
        await self.redis.xack(stream, self.group_name, event_id)
```

### 2. EventProcessor

```python
@dataclass
class EventProcessor:
    """이벤트 처리 및 Pub/Sub 발행"""

    streams_redis: Redis  # State KV
    pubsub_redis: Redis   # Pub/Sub 전용

    # Lua Script: 상태 업데이트 + 중복 방지
    UPDATE_STATE_SCRIPT = """
    local state_key = KEYS[1]
    local publish_key = KEYS[2]
    local event_data = ARGV[1]
    local state_ttl = tonumber(ARGV[2])
    local publish_ttl = tonumber(ARGV[3])

    -- 이미 처리됨?
    if redis.call('EXISTS', publish_key) == 1 then
        return 0
    end

    -- State 업데이트
    redis.call('SETEX', state_key, state_ttl, event_data)
    -- 처리 완료 마킹
    redis.call('SETEX', publish_key, publish_ttl, '1')

    return 1
    """

    async def process(self, event: dict) -> bool:
        """이벤트 처리: State 업데이트 → Pub/Sub 발행"""
        job_id = event["job_id"]
        domain = event.get("domain", "scan")
        seq = event["seq"]

        state_key = f"{domain}:state:{job_id}"
        publish_key = f"router:published:{job_id}:{seq}"

        # Lua Script 실행 (원자적)
        result = await self.streams_redis.eval(
            self.UPDATE_STATE_SCRIPT,
            2,  # key count
            state_key,
            publish_key,
            json.dumps(event),
            3600,  # state_ttl
            7200,  # publish_ttl
        )

        if result == 1:
            # Pub/Sub 발행
            channel = f"sse:events:{job_id}"
            await self.pubsub_redis.publish(channel, json.dumps(event))
            return True

        return False  # 중복 이벤트
```

### 3. PendingReclaimer

```python
@dataclass
class PendingReclaimer:
    """미처리 메시지 복구"""

    redis: Redis
    group_name: str
    consumer_name: str
    stream_prefixes: list[str]
    shard_count: int
    min_idle_ms: int = 300000  # 5분
    processor: EventProcessor

    async def reclaim_loop(self, interval: int = 60) -> None:
        """주기적 Pending 메시지 복구"""
        while True:
            await asyncio.sleep(interval)
            await self.reclaim_all()

    async def reclaim_all(self) -> int:
        """모든 스트림에서 Pending 메시지 복구"""
        total = 0

        for prefix in self.stream_prefixes:
            for shard in range(self.shard_count):
                stream = f"{prefix}:{shard}"
                count = await self.reclaim_stream(stream)
                total += count

        return total

    async def reclaim_stream(self, stream: str) -> int:
        """단일 스트림 Pending 복구"""
        claimed = await self.redis.xautoclaim(
            stream,
            self.group_name,
            self.consumer_name,
            min_idle_time=self.min_idle_ms,
            count=100,
        )

        _, messages, _ = claimed
        for event_id, data in messages:
            event = json.loads(data[b"data"])
            await self.processor.process(event)
            await self.redis.xack(stream, self.group_name, event_id)

        return len(messages)
```

---

## Main Application

```python
# apps/event_router/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    consumer = StreamConsumer(...)
    processor = EventProcessor(...)
    reclaimer = PendingReclaimer(...)

    await consumer.setup()

    # Background tasks
    consumer_task = asyncio.create_task(run_consumer(consumer, processor))
    reclaim_task = asyncio.create_task(reclaimer.reclaim_loop())

    yield

    # Shutdown
    consumer_task.cancel()
    reclaim_task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    # Consumer Group 연결 확인
    return {"status": "ready"}
```

---

## Multi-Domain 지원

```python
# 여러 도메인의 이벤트 스트림 처리
DOMAINS = {
    "scan": {
        "stream_prefix": "scan:events",
        "state_prefix": "scan:state",
        "shards": 4,
    },
    "chat": {
        "stream_prefix": "chat:events",
        "state_prefix": "chat:state",
        "shards": 4,
    },
}
```

---

## Metrics

```python
# Prometheus metrics
EVENT_ROUTER_CONSUMED = Counter(
    "event_router_consumed_total",
    "Total events consumed",
    ["domain", "stage"],
)

EVENT_ROUTER_PUBLISHED = Counter(
    "event_router_published_total",
    "Total events published to Pub/Sub",
    ["domain"],
)

EVENT_ROUTER_DUPLICATES = Counter(
    "event_router_duplicates_total",
    "Duplicate events skipped",
    ["domain"],
)

EVENT_ROUTER_RECLAIMED = Counter(
    "event_router_reclaimed_total",
    "Pending messages reclaimed",
    ["stream"],
)

EVENT_ROUTER_LATENCY = Histogram(
    "event_router_latency_seconds",
    "Event processing latency",
    ["domain"],
)
```
