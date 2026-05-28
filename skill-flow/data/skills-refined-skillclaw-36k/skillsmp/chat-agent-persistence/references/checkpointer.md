# Checkpointer Reference

> LangGraph 멀티턴 대화 컨텍스트 영속화

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cache-Aside Pattern                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  조회 (aget_tuple)                                               │
│  ─────────────────                                               │
│  LangGraph → Redis (L1, ~1ms)                                    │
│                 │                                                │
│                 ├── Hit → Return                                 │
│                 │                                                │
│                 └── Miss → PostgreSQL (L2)                       │
│                               │                                  │
│                               └── Redis 캐싱 (warm-up)           │
│                                       │                          │
│                                       └── Return                 │
│                                                                  │
│  저장 (aput)                                                     │
│  ───────────                                                     │
│  LangGraph → PostgreSQL (영구) + Redis (캐시)                     │
│              Write-Through                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Components

| Class | Purpose | Layer |
|-------|---------|-------|
| `CachedPostgresSaver` | L1 Redis + L2 PostgreSQL | Adapter |
| `AsyncPostgresSaver` | LangGraph PostgreSQL 체크포인터 | External (langgraph) |
| `MemorySaver` | In-memory fallback | External (langgraph) |

## Current Issue

### Error

```
[WARNING] CachedPostgresSaver failed, falling back to Redis only:
object _AsyncGeneratorContextManager can't be used in 'await' expression
```

### Root Cause

`checkpointer.py:228`:

```python
# BUG: from_conn_string()은 async context manager 반환
postgres_saver = await AsyncPostgresSaver.from_conn_string(conn_string)  # WRONG!
```

### LangGraph API Signature

```python
# langgraph-checkpoint-postgres
class AsyncPostgresSaver:
    @classmethod
    @asynccontextmanager
    async def from_conn_string(cls, conn_string: str) -> AsyncIterator["AsyncPostgresSaver"]:
        """Async context manager - await 아님!"""
        ...
```

### Fallback Chain

```
CachedPostgresSaver (PostgreSQL + Redis)
       │
       │ Exception
       ▼
create_redis_checkpointer()
       │
       │ (Redis checkpointer도 lifecycle 이슈)
       ▼
MemorySaver (In-memory only)
```

## Fix Options

### Option A: Context Manager 수동 관리

```python
class CachedPostgresSaver(BaseCheckpointSaver):
    _postgres_cm: AsyncContextManager | None = None

    @classmethod
    async def create(cls, conn_string: str, redis: "Redis") -> "CachedPostgresSaver":
        from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

        cm = AsyncPostgresSaver.from_conn_string(conn_string)
        postgres_saver = await cm.__aenter__()

        instance = cls(postgres_saver=postgres_saver, redis=redis)
        instance._postgres_cm = cm
        return instance

    async def close(self) -> None:
        if self._postgres_cm:
            await self._postgres_cm.__aexit__(None, None, None)
```

### Option B: Connection Pool 직접 생성 (권장)

```python
from psycopg_pool import AsyncConnectionPool

async def create_cached_postgres_checkpointer(
    conn_string: str,
    redis: "Redis",
) -> CachedPostgresSaver:
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

    # Pool 직접 생성
    pool = AsyncConnectionPool(conninfo=conn_string)
    await pool.open()

    postgres_saver = AsyncPostgresSaver(pool)
    await postgres_saver.setup()  # 테이블 생성

    return CachedPostgresSaver(
        postgres_saver=postgres_saver,
        redis=redis,
        pool=pool,  # cleanup 위해 보관
    )
```

## Verification

```bash
# 1. Worker 로그에서 성공 메시지 확인
kubectl logs -n chat deploy/chat-worker --tail=50 | grep -E "CachedPostgresSaver (created|initialized)"

# 2. PostgreSQL 체크포인트 테이블 확인
kubectl exec -n postgres deploy/postgresql -- psql -U sesacthon -d ecoeco -c \
  "SELECT COUNT(*) FROM checkpoints;"

# 3. 멀티턴 대화 테스트
# 첫 번째 메시지: "내 이름은 철수야"
# 두 번째 메시지: "내 이름이 뭐라고 했지?" → 철수 기억하면 성공
```

## Configuration

| Variable | Value | Description |
|----------|-------|-------------|
| `POSTGRES_URL` | `postgresql+asyncpg://...` | PostgreSQL 연결 문자열 |
| `REDIS_URL` | `redis://rfr-pubsub-redis-0...` | Redis 캐시 URL |
| Cache TTL | 86400 (24h) | 체크포인트 캐시 TTL |

## Related Files

| File | Description |
|------|-------------|
| `checkpointer.py` | CachedPostgresSaver 구현 |
| `dependencies.py:641-678` | get_checkpointer() 함수 |
| `factory.py` | Graph 생성 시 checkpointer 주입 |
