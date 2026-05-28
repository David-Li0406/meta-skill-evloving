# Redis Messaging 패턴

## Pub/Sub vs Streams

| 기능 | Pub/Sub | Streams |
|------|---------|---------|
| 메시지 보존 | X (Fire-and-forget) | O (MAXLEN) |
| 재처리 | 불가 | XPENDING, XCLAIM |
| Consumer Group | 불가 | XREADGROUP |
| 순서 보장 | O | O |
| 용도 | 실시간 전송 | 내구성 필요 |

---

## Pub/Sub 패턴

### Publisher

```python
from redis.asyncio import Redis
import json

class EventPublisher:
    """Redis Pub/Sub 이벤트 발행자"""

    def __init__(self, redis: Redis, prefix: str = "events"):
        self._redis = redis
        self._prefix = prefix

    async def publish(
        self,
        channel: str,
        event: dict,
    ) -> int:
        """이벤트 발행

        Returns:
            구독자 수
        """
        full_channel = f"{self._prefix}:{channel}"
        payload = json.dumps(event, ensure_ascii=False)
        return await self._redis.publish(full_channel, payload)

    async def publish_to_job(
        self,
        job_id: str,
        event: dict,
    ) -> int:
        """Job별 채널에 발행"""
        return await self.publish(f"sse:{job_id}", event)
```

### Subscriber

```python
from redis.asyncio.client import PubSub

class EventSubscriber:
    """Redis Pub/Sub 이벤트 구독자"""

    def __init__(self, redis: Redis, prefix: str = "events"):
        self._redis = redis
        self._prefix = prefix
        self._pubsub: PubSub | None = None

    async def subscribe(self, channel: str) -> None:
        """채널 구독"""
        if self._pubsub is None:
            self._pubsub = self._redis.pubsub()

        full_channel = f"{self._prefix}:{channel}"
        await self._pubsub.subscribe(full_channel)

    async def listen(self) -> AsyncIterator[dict]:
        """이벤트 수신"""
        if self._pubsub is None:
            raise RuntimeError("Not subscribed")

        async for message in self._pubsub.listen():
            if message["type"] == "message":
                yield json.loads(message["data"])

    async def unsubscribe(self, channel: str) -> None:
        """구독 해제"""
        if self._pubsub:
            await self._pubsub.unsubscribe(f"{self._prefix}:{channel}")

    async def close(self) -> None:
        """연결 종료"""
        if self._pubsub:
            await self._pubsub.close()
            self._pubsub = None
```

---

## Streams 패턴

### Producer (XADD)

```python
class StreamProducer:
    """Redis Streams 이벤트 생산자"""

    def __init__(
        self,
        redis: Redis,
        stream_prefix: str = "events",
        maxlen: int = 10000,
    ):
        self._redis = redis
        self._prefix = stream_prefix
        self._maxlen = maxlen

    async def produce(
        self,
        stream: str,
        event: dict,
    ) -> str:
        """이벤트 추가

        Returns:
            이벤트 ID
        """
        full_stream = f"{self._prefix}:{stream}"
        event_id = await self._redis.xadd(
            full_stream,
            {"data": json.dumps(event)},
            maxlen=self._maxlen,
            approximate=True,  # ~ 연산자
        )
        return event_id

    async def produce_to_shard(
        self,
        domain: str,
        job_id: str,
        event: dict,
        shard_count: int = 4,
    ) -> str:
        """샤딩된 스트림에 추가"""
        shard = int(hashlib.md5(job_id.encode()).hexdigest(), 16) % shard_count
        stream = f"{domain}:{shard}"
        return await self.produce(stream, event)
```

### Consumer Group

```python
class StreamConsumer:
    """Redis Streams Consumer Group 소비자"""

    def __init__(
        self,
        redis: Redis,
        stream_prefix: str = "events",
        group: str = "consumers",
        consumer: str = "consumer-1",
    ):
        self._redis = redis
        self._prefix = stream_prefix
        self._group = group
        self._consumer = consumer

    async def setup_group(self, stream: str) -> None:
        """Consumer Group 생성"""
        full_stream = f"{self._prefix}:{stream}"
        try:
            await self._redis.xgroup_create(
                full_stream,
                self._group,
                id="0",
                mkstream=True,
            )
        except ResponseError as e:
            if "BUSYGROUP" not in str(e):
                raise

    async def consume(
        self,
        streams: list[str],
        block_ms: int = 5000,
        count: int = 100,
    ) -> AsyncIterator[tuple[str, str, dict]]:
        """이벤트 소비

        Yields:
            (stream, event_id, event_data)
        """
        stream_dict = {
            f"{self._prefix}:{s}": ">"
            for s in streams
        }

        while True:
            messages = await self._redis.xreadgroup(
                groupname=self._group,
                consumername=self._consumer,
                streams=stream_dict,
                block=block_ms,
                count=count,
            )

            for stream_name, events in messages:
                for event_id, data in events:
                    event = json.loads(data[b"data"])
                    yield stream_name.decode(), event_id, event

    async def ack(self, stream: str, event_id: str) -> None:
        """이벤트 ACK"""
        full_stream = f"{self._prefix}:{stream}"
        await self._redis.xack(full_stream, self._group, event_id)
```

### Pending 복구 (XAUTOCLAIM)

```python
class PendingReclaimer:
    """미처리 메시지 복구"""

    def __init__(
        self,
        redis: Redis,
        stream_prefix: str,
        group: str,
        consumer: str,
        min_idle_ms: int = 300000,  # 5분
    ):
        self._redis = redis
        self._prefix = stream_prefix
        self._group = group
        self._consumer = consumer
        self._min_idle = min_idle_ms

    async def reclaim(
        self,
        stream: str,
        count: int = 100,
    ) -> list[tuple[str, dict]]:
        """Pending 메시지 복구"""
        full_stream = f"{self._prefix}:{stream}"

        result = await self._redis.xautoclaim(
            full_stream,
            self._group,
            self._consumer,
            min_idle_time=self._min_idle,
            count=count,
        )

        _, messages, _ = result

        reclaimed = []
        for event_id, data in messages:
            event = json.loads(data[b"data"])
            reclaimed.append((event_id, event))

        return reclaimed
```

---

## Eco² Composite Bus

```python
class CompositeEventBus:
    """Streams (내구성) + Pub/Sub (실시간) 조합"""

    def __init__(
        self,
        streams_redis: Redis,  # AOF 활성화
        pubsub_redis: Redis,   # 휘발성
    ):
        self._producer = StreamProducer(streams_redis)
        self._publisher = EventPublisher(pubsub_redis)

    async def emit(
        self,
        domain: str,
        job_id: str,
        event: dict,
    ) -> None:
        """이벤트 발행 (Streams + Pub/Sub)"""
        # 1. Streams에 저장 (내구성)
        await self._producer.produce_to_shard(domain, job_id, event)

        # 2. State KV 업데이트
        state_key = f"{domain}:state:{job_id}"
        await self._producer._redis.setex(
            state_key,
            3600,
            json.dumps(event),
        )

        # 3. Pub/Sub로 실시간 전송
        await self._publisher.publish_to_job(job_id, event)
```
