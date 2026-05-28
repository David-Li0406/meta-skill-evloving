# Checkpointing Guide

## 개요

Checkpointing은 LangGraph의 상태 영속화 메커니즘. Multi-turn 대화, 실행 중단/재개, 히스토리 추적에 필수.

---

## Checkpointer 종류

| Checkpointer | 용도 | 영속성 |
|--------------|------|--------|
| `MemorySaver` | 개발/테스트 | 프로세스 내 |
| `SqliteSaver` | 로컬 개발 | 파일 |
| `AsyncPostgresSaver` | 프로덕션 | DB |
| `RedisSaver` | 캐시 레이어 | 휘발성 |

---

## Cache-Aside 패턴 (Eco² 구현)

L1 Redis + L2 PostgreSQL 조합으로 성능과 영속성 확보.

```python
from langgraph.checkpoint.base import (
    BaseCheckpointSaver,
    Checkpoint,
    CheckpointMetadata,
    CheckpointTuple,
)
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from redis.asyncio import Redis
import json

class CachedPostgresSaver(BaseCheckpointSaver):
    """
    Cache-Aside Pattern Checkpointer

    Read: Redis → PostgreSQL (miss 시)
    Write: PostgreSQL → Redis (write-through)
    """

    def __init__(
        self,
        redis: Redis,
        pg_saver: AsyncPostgresSaver,
        ttl: int = 3600,
        prefix: str = "checkpoint",
    ):
        super().__init__()
        self._redis = redis
        self._pg = pg_saver
        self._ttl = ttl
        self._prefix = prefix

    def _cache_key(self, thread_id: str) -> str:
        return f"{self._prefix}:{thread_id}"

    def _serialize(self, checkpoint: Checkpoint) -> str:
        return json.dumps({
            "v": checkpoint["v"],
            "ts": checkpoint["ts"],
            "channel_values": checkpoint["channel_values"],
            "channel_versions": checkpoint["channel_versions"],
            "versions_seen": checkpoint["versions_seen"],
        })

    def _deserialize(self, data: str) -> Checkpoint:
        parsed = json.loads(data)
        return Checkpoint(
            v=parsed["v"],
            ts=parsed["ts"],
            channel_values=parsed["channel_values"],
            channel_versions=parsed["channel_versions"],
            versions_seen=parsed["versions_seen"],
        )

    async def aget_tuple(
        self,
        config: RunnableConfig,
    ) -> CheckpointTuple | None:
        thread_id = config["configurable"]["thread_id"]
        key = self._cache_key(thread_id)

        # L1: Redis 조회
        cached = await self._redis.get(key)
        if cached:
            checkpoint = self._deserialize(cached)
            return CheckpointTuple(
                config=config,
                checkpoint=checkpoint,
                metadata=CheckpointMetadata(),
            )

        # L2: PostgreSQL 조회
        tuple_ = await self._pg.aget_tuple(config)
        if tuple_:
            # L1 캐시 갱신
            await self._redis.setex(
                key,
                self._ttl,
                self._serialize(tuple_.checkpoint)
            )
        return tuple_

    async def aput(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
    ) -> RunnableConfig:
        thread_id = config["configurable"]["thread_id"]
        key = self._cache_key(thread_id)

        # L2: PostgreSQL 저장
        result = await self._pg.aput(config, checkpoint, metadata)

        # L1: Redis 캐시 갱신 (write-through)
        await self._redis.setex(
            key,
            self._ttl,
            self._serialize(checkpoint)
        )

        return result

    async def alist(
        self,
        config: RunnableConfig,
        *,
        before: RunnableConfig | None = None,
        limit: int | None = None,
    ):
        # 히스토리 조회는 PostgreSQL에서 직접
        async for item in self._pg.alist(config, before=before, limit=limit):
            yield item
```

---

## 사용법

### Checkpointer 초기화

```python
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from redis.asyncio import Redis

async def create_checkpointer(
    redis_url: str,
    postgres_url: str,
) -> CachedPostgresSaver:
    redis = Redis.from_url(redis_url)
    pg_saver = AsyncPostgresSaver.from_conn_string(postgres_url)

    # PostgreSQL 테이블 생성 (최초 1회)
    await pg_saver.setup()

    return CachedPostgresSaver(redis, pg_saver)
```

### Graph 컴파일 시 주입

```python
checkpointer = await create_checkpointer(
    redis_url="redis://localhost:6379",
    postgres_url="postgresql://user:pass@localhost/db"
)

compiled = graph.compile(checkpointer=checkpointer)
```

### Thread ID로 대화 추적

```python
# 새 대화 시작
result = await compiled.ainvoke(
    {"query": "플라스틱 분리배출 방법"},
    config={"configurable": {"thread_id": "user-123-session-1"}}
)

# 같은 thread_id로 대화 이어가기
result = await compiled.ainvoke(
    {"query": "페트병은 어떻게?"},
    config={"configurable": {"thread_id": "user-123-session-1"}}
)
```

---

## 히스토리 조회

```python
async def get_conversation_history(
    checkpointer: BaseCheckpointSaver,
    thread_id: str,
    limit: int = 10,
) -> list[Checkpoint]:
    """대화 히스토리 조회"""
    history = []
    config = {"configurable": {"thread_id": thread_id}}

    async for tuple_ in checkpointer.alist(config, limit=limit):
        history.append(tuple_.checkpoint)

    return history
```

---

## Interrupt & Resume

Human-in-the-loop 패턴에서 중단/재개.

```python
# 특정 노드 전에 중단
compiled = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["human_approval"]
)

# 실행 (human_approval 전에 중단됨)
result = await compiled.ainvoke(
    {"request": "delete all users"},
    config={"configurable": {"thread_id": "admin-action-1"}}
)

# ... 사용자 승인 대기 ...

# 승인 후 재개
result = await compiled.ainvoke(
    {"approved": True},
    config={"configurable": {"thread_id": "admin-action-1"}}
)
```

---

## Best Practices

### 1. TTL 설정

```python
# 대화 세션 TTL (1시간)
SESSION_TTL = 3600

# 임시 처리 TTL (5분)
TEMP_TTL = 300
```

### 2. Thread ID 네이밍

```python
# 패턴: {user_id}-{session_type}-{timestamp}
thread_id = f"user-{user_id}-chat-{int(time.time())}"
```

### 3. 캐시 무효화

```python
async def invalidate_cache(
    redis: Redis,
    thread_id: str,
) -> None:
    """세션 종료 시 캐시 정리"""
    key = f"checkpoint:{thread_id}"
    await redis.delete(key)
```
