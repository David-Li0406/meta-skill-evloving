# Idempotency 패턴

## E2E Exactly-Once Semantics

Eco² Event Bus는 다중 레이어에서 멱등성을 보장.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Idempotency Layers                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Layer 1: Worker → Streams                                       │
│  ├─ Key: published:{job_id}:{stage}:{seq}                       │
│  ├─ TTL: 2시간                                                  │
│  └─ 효과: 동일 이벤트 중복 XADD 방지                            │
│                                                                  │
│  Layer 2: Router → State KV                                      │
│  ├─ Key: router:published:{job_id}:{seq}                        │
│  ├─ TTL: 2시간                                                  │
│  └─ 효과: 동일 이벤트 중복 State 업데이트 방지                  │
│                                                                  │
│  Layer 3: Router → Pub/Sub                                       │
│  ├─ Mechanism: Lua Script 원자성                                │
│  └─ 효과: State 업데이트 성공 시에만 Publish                    │
│                                                                  │
│  Layer 4: Gateway → Client                                       │
│  ├─ Mechanism: seq 기반 필터링 (last_seq)                       │
│  └─ 효과: 재연결 시 중복 이벤트 필터링                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Worker → Streams

### Lua Script: IDEMPOTENT_XADD

```lua
-- KEYS[1]: stream_key (scan:events:0)
-- KEYS[2]: state_key (scan:state:{job_id})
-- KEYS[3]: publish_key (published:{job_id}:{stage}:{seq})
-- ARGV[1]: event_data (JSON)
-- ARGV[2]: state_ttl (3600)
-- ARGV[3]: publish_ttl (7200)

local stream_key = KEYS[1]
local state_key = KEYS[2]
local publish_key = KEYS[3]
local event_data = ARGV[1]
local state_ttl = tonumber(ARGV[2])
local publish_ttl = tonumber(ARGV[3])

-- 이미 발행됨?
if redis.call('EXISTS', publish_key) == 1 then
    return 0  -- Skip
end

-- XADD (MAXLEN 제한)
redis.call('XADD', stream_key, 'MAXLEN', '~', '10000', '*',
    'data', event_data)

-- State KV 업데이트
redis.call('SETEX', state_key, state_ttl, event_data)

-- 발행 완료 마킹
redis.call('SETEX', publish_key, publish_ttl, '1')

return 1  -- Success
```

### Python 구현

```python
IDEMPOTENT_XADD = """
local stream_key = KEYS[1]
local state_key = KEYS[2]
local publish_key = KEYS[3]
local event_data = ARGV[1]
local state_ttl = tonumber(ARGV[2])
local publish_ttl = tonumber(ARGV[3])

if redis.call('EXISTS', publish_key) == 1 then
    return 0
end

redis.call('XADD', stream_key, 'MAXLEN', '~', '10000', '*', 'data', event_data)
redis.call('SETEX', state_key, state_ttl, event_data)
redis.call('SETEX', publish_key, publish_ttl, '1')

return 1
"""

async def publish_event(
    redis: Redis,
    domain: str,
    job_id: str,
    stage: str,
    seq: int,
    data: dict,
) -> bool:
    """멱등성 보장 이벤트 발행"""
    shard = md5_hash(job_id) % SHARD_COUNT

    event = {
        "job_id": job_id,
        "domain": domain,
        "stage": stage,
        "seq": seq,
        "data": data,
        "timestamp": datetime.utcnow().isoformat(),
    }

    result = await redis.eval(
        IDEMPOTENT_XADD,
        3,  # key count
        f"{domain}:events:{shard}",      # stream
        f"{domain}:state:{job_id}",      # state
        f"published:{job_id}:{stage}:{seq}",  # dedup key
        json.dumps(event),
        3600,   # state TTL
        7200,   # publish TTL
    )

    return result == 1
```

---

## Layer 2: Router → State KV

### Lua Script: UPDATE_STATE

```lua
-- KEYS[1]: state_key
-- KEYS[2]: publish_key
-- ARGV[1]: event_data
-- ARGV[2]: state_ttl
-- ARGV[3]: publish_ttl

local state_key = KEYS[1]
local publish_key = KEYS[2]

-- 이미 처리됨?
if redis.call('EXISTS', publish_key) == 1 then
    return 0
end

-- State 업데이트
redis.call('SETEX', state_key, tonumber(ARGV[2]), ARGV[1])
-- 처리 완료 마킹
redis.call('SETEX', publish_key, tonumber(ARGV[3]), '1')

return 1
```

---

## Layer 4: Gateway seq 필터링

```python
async def subscribe(
    self,
    job_id: str,
    last_seq: int = 0,  # 클라이언트가 마지막으로 받은 seq
) -> AsyncIterator[dict]:
    """seq 기반 중복 필터링"""

    async for event in self._event_stream(job_id):
        event_seq = event.get("seq", 0)

        # 이미 받은 이벤트 스킵
        if event_seq <= last_seq:
            continue

        yield event
        last_seq = event_seq
```

---

## seq 넘버링 규칙

```python
# Stage별 seq 범위 (Eco² 컨벤션)
SEQ_RANGES = {
    "vision": (10, 19),      # 10, 11, 12...
    "rule": (20, 29),        # 20, 21, 22...
    "answer": (30, 39),      # 30, 31, 32...
    "reward": (40, 49),      # 40, 41, 42...
    "done": (50, 59),        # 51 (final)
}

def get_next_seq(stage: str, sub_seq: int = 0) -> int:
    """Stage별 seq 계산"""
    base, _ = SEQ_RANGES.get(stage, (0, 9))
    return base + sub_seq
```

---

## TTL 전략

| Key Pattern | TTL | 용도 |
|-------------|-----|------|
| `{domain}:state:{job_id}` | 1시간 | 최신 상태 (Recovery용) |
| `published:{job_id}:{stage}:{seq}` | 2시간 | Worker 중복 방지 |
| `router:published:{job_id}:{seq}` | 2시간 | Router 중복 방지 |

**왜 2시간?**
- Job 처리 시간 + 재시도 여유
- TTL 후 자동 정리 (메모리 효율)
- 재시도 시 멱등성 보장

---

## 테스트 패턴

```python
@pytest.mark.asyncio
async def test_idempotent_publish():
    """동일 이벤트 중복 발행 테스트"""
    redis = await get_redis()

    # 첫 번째 발행 - 성공
    result1 = await publish_event(
        redis, "scan", "job-1", "vision", 10, {"status": "done"}
    )
    assert result1 is True

    # 두 번째 발행 - 스킵
    result2 = await publish_event(
        redis, "scan", "job-1", "vision", 10, {"status": "done"}
    )
    assert result2 is False

    # Stream에 1개만 존재
    messages = await redis.xrange("scan:events:0")
    job1_events = [m for m in messages if b"job-1" in m[1][b"data"]]
    assert len(job1_events) == 1
```
