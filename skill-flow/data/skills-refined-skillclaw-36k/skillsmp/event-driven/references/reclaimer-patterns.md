# Reclaimer 패턴

## 멀티 도메인 병렬 처리

Reclaimer는 여러 도메인의 Pending 메시지를 병렬로 처리합니다.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Reclaimer Multi-Domain Processing                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    Reclaimer                                                                │
│        │                                                                    │
│        └──► _reclaim_pending()                                              │
│                    │                                                        │
│                    ├──► asyncio.gather()                                    │
│                    │         │                                              │
│                    │         ├──► _reclaim_domain("scan:events", 4)         │
│                    │         │         │                                    │
│                    │         │         ├──► scan:events:0  ──┐              │
│                    │         │         ├──► scan:events:1  ──┤ 순차         │
│                    │         │         ├──► scan:events:2  ──┤              │
│                    │         │         └──► scan:events:3  ──┘              │
│                    │         │                                              │
│                    │         └──► _reclaim_domain("chat:events", 4)         │
│                    │                   │                     │ 병렬         │
│                    │                   ├──► chat:events:0  ──┐              │
│                    │                   ├──► chat:events:1  ──┤ 순차         │
│                    │                   ├──► chat:events:2  ──┤              │
│                    │                   └──► chat:events:3  ──┘              │
│                    │                                                        │
│                    └──► 결과 집계                                            │
│                                                                             │
│  ✅ 도메인 간 병렬 처리 (scan/chat 독립)                                     │
│  ✅ 도메인 내 샤드는 순차 처리 (Redis 부하 분산)                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## stream_configs 파라미터

```python
class PendingReclaimer:
    def __init__(
        self,
        redis_client: Redis,
        processor: EventProcessor,
        consumer_group: str,
        consumer_name: str,
        stream_configs: list[tuple[str, int]] | None = None,  # 멀티 도메인
        min_idle_ms: int = 300000,  # 5분
        interval_seconds: int = 60,
        count: int = 100,
    ) -> None:
        # 멀티 도메인 지원
        self._stream_configs = stream_configs or [("scan:events", 4)]
        # 예: [("scan:events", 4), ("chat:events", 4)]
```

---

## 도메인별 병렬 처리 구현

```python
async def _reclaim_pending(self) -> None:
    """모든 도메인의 모든 shard에서 Pending 메시지 재할당.

    각 도메인을 병렬로 처리하여 한 도메인의 지연이 다른 도메인에 영향 없음.
    """
    # 도메인별 병렬 처리
    tasks = [
        self._reclaim_domain(prefix, shard_count)
        for prefix, shard_count in self._stream_configs
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 결과 집계
    total_reclaimed = 0
    for result in results:
        if isinstance(result, Exception):
            logger.error("reclaim_domain_error", extra={"error": str(result)})
        elif isinstance(result, int):
            total_reclaimed += result

    if total_reclaimed > 0:
        logger.info(
            "reclaim_completed",
            extra={"total_reclaimed": total_reclaimed},
        )

async def _reclaim_domain(self, prefix: str, shard_count: int) -> int:
    """단일 도메인의 모든 shard에서 Pending 메시지 재할당."""
    domain = prefix.split(":")[0]
    domain_reclaimed = 0

    for shard in range(shard_count):
        stream_key = f"{prefix}:{shard}"
        shard_str = str(shard)

        try:
            start_time = time.perf_counter()
            result = await self._redis.xautoclaim(
                stream_key,
                self._consumer_group,
                self._consumer_name,
                min_idle_time=self._min_idle_ms,
                start_id="0-0",
                count=self._count,
            )
            reclaim_latency = time.perf_counter() - start_time

            # 메트릭 기록 (domain + shard 라벨)
            EVENT_ROUTER_RECLAIM_LATENCY.labels(
                domain=domain, shard=shard_str
            ).observe(reclaim_latency)

            if len(result) >= 2:
                messages = result[1]
                if messages:
                    reclaimed_count = await self._process_reclaimed(
                        stream_key, messages
                    )
                    domain_reclaimed += reclaimed_count
                    EVENT_ROUTER_RECLAIM_MESSAGES.labels(
                        domain=domain, shard=shard_str
                    ).inc(reclaimed_count)

        except Exception as e:
            if "NOGROUP" in str(e):
                continue  # Consumer Group 미생성 - 정상
            logger.error(
                "xautoclaim_error",
                extra={"stream": stream_key, "domain": domain, "error": str(e)},
            )

    return domain_reclaimed
```

---

## stream_id 주입

Reclaimer가 재처리할 때도 Consumer와 동일하게 `stream_id`를 주입해야 합니다.

```python
async def _process_reclaimed(
    self,
    stream_key: str,
    messages: list[tuple[str, dict]],
) -> int:
    """재할당된 메시지 처리.

    Consumer와 동일한 패턴:
    - stream_id 주입 (SSE Gateway 중복 필터링용)
    - stream_name 전달 (도메인별 state prefix 결정)
    - 실패 시 ACK 스킵 (다음 reclaim 주기에 재시도)
    """
    processed_count = 0

    for msg_id, data in messages:
        if isinstance(msg_id, bytes):
            msg_id = msg_id.decode()

        event = self._parse_event(data)

        # ⚠️ 핵심: stream_id 주입
        # SSE Gateway에서 중복 필터링에 사용
        event["stream_id"] = msg_id

        try:
            # stream_key 전달하여 도메인별 state prefix 결정
            success = await self._processor.process_event(
                event, stream_name=stream_key
            )
            if not success:
                continue  # ACK 스킵

            processed_count += 1
        except Exception as e:
            continue  # ACK 스킵

        # 성공한 경우만 ACK
        await self._redis.xack(stream_key, self._consumer_group, msg_id)

    return processed_count
```

---

## Metrics 라벨 분리

domain + shard로 라벨을 분리하여 Grafana 쿼리를 용이하게 합니다.

```python
# AS-IS: 결합된 라벨
EVENT_ROUTER_RECLAIM_MESSAGES = Counter(
    ...,
    labelnames=["shard"],  # shard="scan:0" (도메인:샤드 결합)
)

# TO-BE: 분리된 라벨
EVENT_ROUTER_RECLAIM_MESSAGES = Counter(
    "event_router_reclaim_messages_total",
    "Total messages reclaimed via XAUTOCLAIM",
    labelnames=["domain", "shard"],  # domain="scan", shard="0"
)

EVENT_ROUTER_RECLAIM_LATENCY = Histogram(
    "event_router_reclaim_latency_seconds",
    "XAUTOCLAIM latency per shard",
    labelnames=["domain", "shard"],
)
```

### Grafana 쿼리 예시

```promql
# 도메인별 reclaim 총량
sum by (domain) (
    rate(event_router_reclaim_messages_total[5m])
)

# 특정 도메인의 샤드별 분포
event_router_reclaim_messages_total{domain="scan"}

# Reclaim latency p99
histogram_quantile(0.99,
    rate(event_router_reclaim_latency_seconds_bucket{domain="chat"}[5m])
)
```

---

## Main Application 초기화

```python
# apps/event_router/main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Stream configs: [(prefix, shard_count), ...]
    stream_configs = [
        ("scan:events", settings.scan_shard_count),
        ("chat:events", settings.chat_shard_count),
    ]

    # Consumer 초기화
    consumer = StreamConsumer(
        redis_client=streams_redis,
        processor=processor,
        consumer_group=settings.consumer_group,
        consumer_name=consumer_name,
        stream_configs=stream_configs,
    )

    # Reclaimer 초기화 (동일한 stream_configs 사용)
    reclaimer = PendingReclaimer(
        redis_client=streams_redis,
        processor=processor,
        consumer_group=settings.consumer_group,
        consumer_name=consumer_name,
        stream_configs=stream_configs,  # ⚠️ 핵심: 멀티 도메인 지원
        min_idle_ms=settings.reclaim_min_idle_ms,
        interval_seconds=settings.reclaim_interval_seconds,
    )

    # Background tasks
    consumer_task = asyncio.create_task(consumer.run())
    reclaim_task = asyncio.create_task(reclaimer.run())

    yield

    # Shutdown
    await consumer.shutdown()
    await reclaimer.shutdown()
    consumer_task.cancel()
    reclaim_task.cancel()
```

---

## 체크리스트

- [ ] `stream_configs`에 모든 도메인이 포함되어 있는가?
- [ ] Consumer와 Reclaimer가 동일한 `stream_configs`를 사용하는가?
- [ ] `stream_id`가 재처리 시에도 주입되는가?
- [ ] 처리 실패 시 ACK를 스킵하는가?
- [ ] 메트릭 라벨이 `domain` + `shard`로 분리되어 있는가?
