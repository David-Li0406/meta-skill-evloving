# Cache-Aside 패턴

## 개념

```
Client → Cache (L1) → Database (L2)
         ↓ miss
         Database → Cache (write-through)
```

---

## 기본 구현

```python
from redis.asyncio import Redis
from typing import TypeVar, Callable, Awaitable
import json

T = TypeVar("T")

class CacheAside:
    """Cache-Aside 패턴 구현"""

    def __init__(
        self,
        redis: Redis,
        prefix: str = "cache",
        default_ttl: int = 3600,
    ):
        self._redis = redis
        self._prefix = prefix
        self._default_ttl = default_ttl

    def _key(self, key: str) -> str:
        return f"{self._prefix}:{key}"

    async def get(
        self,
        key: str,
        fetch_fn: Callable[[], Awaitable[T]],
        ttl: int | None = None,
        deserialize: Callable[[str], T] = json.loads,
        serialize: Callable[[T], str] = json.dumps,
    ) -> T:
        """Cache-Aside 조회"""
        cache_key = self._key(key)

        # 1. Cache Hit
        cached = await self._redis.get(cache_key)
        if cached:
            return deserialize(cached)

        # 2. Cache Miss → Fetch
        data = await fetch_fn()

        # 3. Write to Cache
        await self._redis.setex(
            cache_key,
            ttl or self._default_ttl,
            serialize(data) if not isinstance(data, str) else data,
        )

        return data

    async def invalidate(self, key: str) -> None:
        """캐시 무효화"""
        await self._redis.delete(self._key(key))

    async def refresh(
        self,
        key: str,
        fetch_fn: Callable[[], Awaitable[T]],
        ttl: int | None = None,
    ) -> T:
        """캐시 갱신 (강제)"""
        await self.invalidate(key)
        return await self.get(key, fetch_fn, ttl)
```

---

## Eco² Checkpoint 캐시

```python
from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

class CachedPostgresSaver(BaseCheckpointSaver):
    """L1 Redis + L2 PostgreSQL Checkpoint"""

    def __init__(
        self,
        redis: Redis,
        pg_saver: AsyncPostgresSaver,
        ttl: int = 3600,
    ):
        super().__init__()
        self._cache = CacheAside(redis, prefix="checkpoint", default_ttl=ttl)
        self._pg = pg_saver

    async def aget_tuple(
        self,
        config: RunnableConfig,
    ) -> CheckpointTuple | None:
        thread_id = config["configurable"]["thread_id"]

        return await self._cache.get(
            key=thread_id,
            fetch_fn=lambda: self._pg.aget_tuple(config),
            deserialize=self._deserialize_tuple,
            serialize=self._serialize_tuple,
        )

    async def aput(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
    ) -> RunnableConfig:
        thread_id = config["configurable"]["thread_id"]

        # L2 저장
        result = await self._pg.aput(config, checkpoint, metadata)

        # L1 갱신 (Write-Through)
        await self._cache.refresh(
            key=thread_id,
            fetch_fn=lambda: self._pg.aget_tuple(config),
        )

        return result
```

---

## Intent Classification 캐시

```python
class IntentCache:
    """의도 분류 결과 캐시"""

    def __init__(self, redis: Redis, ttl: int = 300):
        self._cache = CacheAside(redis, prefix="intent", default_ttl=ttl)

    async def get_or_classify(
        self,
        message: str,
        classifier: IntentClassifier,
    ) -> IntentResult:
        """캐시된 분류 결과 또는 새로 분류"""
        # 메시지 해시를 키로 사용
        key = hashlib.md5(message.encode()).hexdigest()

        return await self._cache.get(
            key=key,
            fetch_fn=lambda: classifier.classify(message),
            deserialize=IntentResult.from_json,
            serialize=lambda r: r.to_json(),
        )
```

---

## 캐시 전략

### Write-Through

```python
async def write_through(key: str, data: T) -> None:
    """쓰기 시 L1, L2 동시 업데이트"""
    # L2 (원본)
    await database.save(key, data)
    # L1 (캐시)
    await redis.setex(f"cache:{key}", ttl, serialize(data))
```

### Write-Behind (비동기)

```python
async def write_behind(key: str, data: T) -> None:
    """쓰기 시 L1만 업데이트, L2는 비동기"""
    # L1 즉시
    await redis.setex(f"cache:{key}", ttl, serialize(data))
    # L2 비동기
    asyncio.create_task(database.save(key, data))
```

### Cache Stampede 방지

```python
async def get_with_lock(
    key: str,
    fetch_fn: Callable,
    ttl: int = 3600,
    lock_timeout: int = 10,
) -> T:
    """Lock으로 Cache Stampede 방지"""
    cache_key = f"cache:{key}"
    lock_key = f"lock:{key}"

    # 캐시 확인
    cached = await redis.get(cache_key)
    if cached:
        return deserialize(cached)

    # Lock 획득 시도
    acquired = await redis.set(lock_key, "1", nx=True, ex=lock_timeout)

    if acquired:
        try:
            # 원본 조회 및 캐시
            data = await fetch_fn()
            await redis.setex(cache_key, ttl, serialize(data))
            return data
        finally:
            await redis.delete(lock_key)
    else:
        # Lock 대기 후 재시도
        await asyncio.sleep(0.1)
        return await get_with_lock(key, fetch_fn, ttl, lock_timeout)
```

---

## TTL 전략

| 데이터 유형 | TTL | 이유 |
|-------------|-----|------|
| Checkpoint | 1시간 | 세션 지속 시간 |
| Intent | 5분 | 동일 질문 반복 대응 |
| Session State | 30분 | 활성 세션 |
| Rate Limit | 1분 | Sliding Window |
