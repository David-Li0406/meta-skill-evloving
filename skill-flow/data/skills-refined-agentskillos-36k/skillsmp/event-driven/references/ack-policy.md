# ACK Policy Best Practices

## Consumer Group ACK 정책

Redis Streams Consumer Group에서 **ACK는 처리 성공 시에만** 수행해야 합니다.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ACK Policy: AS-IS vs TO-BE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [AS-IS - 데이터 유실]                                                       │
│                                                                             │
│    XREADGROUP                                                               │
│        │                                                                    │
│        ▼                                                                    │
│    process_event()                                                          │
│        │                                                                    │
│        ├── success ──┐                                                      │
│        │             │                                                      │
│        └── failure ──┼──► XACK ──► PEL에서 제거 ──► ❌ 데이터 유실          │
│                      │                                                      │
│                      ▼                                                      │
│                   Reclaimer                                                 │
│                      │                                                      │
│                      └──► PEL 비어있음 ──► 재처리 불가                       │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [TO-BE - 데이터 보존]                                                       │
│                                                                             │
│    XREADGROUP                                                               │
│        │                                                                    │
│        ▼                                                                    │
│    process_event()                                                          │
│        │                                                                    │
│        ├── success ──► XACK ──► PEL에서 제거 ──► ✅ 정상 완료               │
│        │                                                                    │
│        └── failure ──► continue (ACK 스킵)                                  │
│                           │                                                 │
│                           ▼                                                 │
│                     PEL에 유지                                              │
│                           │                                                 │
│                           ▼                                                 │
│                     Reclaimer                                               │
│                           │                                                 │
│                           └──► XAUTOCLAIM ──► 재처리 ──► ✅ 복구           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 올바른 Consumer 구현

```python
async def consume_loop(self) -> None:
    """Consumer 메인 루프 - ACK on Success Only"""
    while not self._shutdown:
        messages = await self._redis.xreadgroup(
            groupname=self._consumer_group,
            consumername=self._consumer_name,
            streams=self._streams,
            block=self._block_ms,
            count=self._count,
        )

        for stream_name, events in messages:
            for event_id, data in events:
                event = self._parse_event(data)

                # stream_id 주입 (SSE Gateway 중복 필터링용)
                event["stream_id"] = event_id

                # 처리 시도
                try:
                    success = await self._processor.process_event(
                        event, stream_name=stream_name
                    )
                    if not success:
                        # Pub/Sub 발행 실패 - ACK 스킵
                        logger.warning("process_event_pubsub_failed", ...)
                        continue  # ⚠️ ACK 스킵 - PEL에 유지

                except Exception as e:
                    # 처리 실패 - ACK 스킵
                    logger.error("process_event_error", ...)
                    continue  # ⚠️ ACK 스킵 - PEL에 유지

                # ✅ 성공한 경우만 ACK
                try:
                    await self._redis.xack(
                        stream_name,
                        self._consumer_group,
                        event_id,
                    )
                except Exception as e:
                    logger.error("xack_error", ...)
```

---

## 핵심 원칙

### 1. ACK는 처리 완료 보장

```python
# ❌ 잘못된 패턴: 무조건 ACK
try:
    await process_event(event)
except Exception:
    logger.error(...)
await redis.xack(stream, group, event_id)  # 실패해도 ACK!

# ✅ 올바른 패턴: 성공 시만 ACK
try:
    success = await process_event(event)
    if not success:
        continue  # ACK 스킵
except Exception:
    continue  # ACK 스킵
await redis.xack(stream, group, event_id)  # 성공 시만 실행
```

### 2. PEL(Pending Entries List) 활용

- ACK되지 않은 메시지는 PEL에 유지됩니다
- Reclaimer가 XAUTOCLAIM으로 오래된 Pending 메시지를 재할당합니다
- 이를 통해 처리 실패한 메시지의 자동 복구가 가능합니다

### 3. Processor 반환값 활용

```python
async def process_event(self, event: dict, stream_name: str) -> bool:
    """이벤트 처리

    Returns:
        bool: True=성공(ACK 수행), False=실패(ACK 스킵)
    """
    try:
        # State 업데이트 (Lua Script)
        result = await self._update_state(event)
        if result == 0:
            return True  # 중복 이벤트 - 이미 처리됨

        # Pub/Sub 발행
        await self._publish_event(event)
        return True

    except Exception as e:
        logger.error("process_event_error", extra={"error": str(e)})
        return False  # 실패 - ACK 스킵 필요
```

---

## Reclaimer도 동일한 정책

Reclaimer에서 재처리할 때도 동일한 ACK 정책을 적용해야 합니다.

```python
async def _process_reclaimed(
    self,
    stream_key: str,
    messages: list[tuple[str, dict]],
) -> int:
    """재할당된 메시지 처리 - ACK on Success Only"""
    processed_count = 0

    for msg_id, data in messages:
        event = self._parse_event(data)
        event["stream_id"] = msg_id  # stream_id 주입

        try:
            success = await self._processor.process_event(
                event, stream_name=stream_key
            )
            if not success:
                continue  # ACK 스킵 - 다음 reclaim 주기에 재시도
            processed_count += 1
        except Exception as e:
            continue  # ACK 스킵 - 다음 reclaim 주기에 재시도

        # 성공한 경우만 ACK
        await self._redis.xack(stream_key, self._consumer_group, msg_id)

    return processed_count
```

---

## 안티패턴

### 1. try-finally에서 무조건 ACK

```python
# ❌ 안티패턴
try:
    await process_event(event)
finally:
    await redis.xack(stream, group, event_id)  # 실패해도 ACK!
```

### 2. 예외 처리 후 ACK 도달

```python
# ❌ 안티패턴
try:
    await process_event(event)
except Exception as e:
    logger.error(...)
    # continue 없음!
await redis.xack(stream, group, event_id)  # 실패해도 ACK!
```

### 3. 배치 처리 후 일괄 ACK

```python
# ❌ 안티패턴
event_ids = []
for event_id, data in events:
    event_ids.append(event_id)
    try:
        await process_event(data)
    except:
        pass  # 실패 무시

# 일부 실패해도 전체 ACK
await redis.xack(stream, group, *event_ids)
```

---

## 모니터링

### Pending 메시지 확인

```bash
# PEL 상태 확인
redis-cli XPENDING scan:events:0 eventrouter

# 특정 Consumer의 Pending 메시지
redis-cli XPENDING scan:events:0 eventrouter - + 10 consumer-0
```

### Prometheus 메트릭

```python
# ACK 성공/실패 카운터
EVENT_ROUTER_XACK_TOTAL = Counter(
    "event_router_xack_total",
    "Total XACK operations",
    labelnames=["result"],  # success, error
)

# Reclaim 메시지 카운터
EVENT_ROUTER_RECLAIM_MESSAGES = Counter(
    "event_router_reclaim_messages_total",
    "Total messages reclaimed via XAUTOCLAIM",
    labelnames=["domain", "shard"],
)
```
