# Failure Recovery 시나리오

## 장애 복구 매트릭스

| 시나리오 | 감지 방법 | 복구 메커니즘 | 데이터 손실 |
|----------|-----------|---------------|-------------|
| Worker 크래시 | Celery ACK 미수신 | Task 재전송 + 멱등성 | 없음 |
| Router 크래시 | XACK 미수신 | XAUTOCLAIM | 없음 |
| Pub/Sub Redis 다운 | Health check | State KV 폴링 | 지연만 |
| SSE Gateway 크래시 | 클라이언트 재연결 | last_seq 복구 | 없음 |
| 클라이언트 연결 끊김 | EventSource onerror | 자동 재연결 | 없음 |

---

## 시나리오 1: Worker Pod 크래시

```
Timeline:
1. Worker-0: XADD 성공, published:{...} 마킹
2. Worker-0: Celery ACK 전에 크래시
3. RabbitMQ: ACK 타임아웃 → Task 재전송
4. Worker-1: 동일 Task 수신
5. Worker-1: XADD 시도 → published:{...} 존재 → Skip
6. Worker-1: Celery ACK → 완료
```

**보장**: 멱등성 Lua Script로 중복 XADD 방지

---

## 시나리오 2: Event Router 크래시

```
Timeline:
1. Router-0: Event 소비 (XREADGROUP)
2. Router-0: State 업데이트 성공
3. Router-0: XACK 전에 크래시
4. Message: Pending 상태 유지
5. Reclaimer (Router-1): 60초 주기 실행
6. Reclaimer: XAUTOCLAIM (5분 idle 메시지)
7. Reclaimer: 재처리 → 중복 체크 → Pub/Sub 발행
8. Reclaimer: XACK → 완료
```

**구현**:

```python
@dataclass
class PendingReclaimer:
    redis: Redis
    min_idle_ms: int = 300000  # 5분

    async def reclaim(self, stream: str, group: str) -> int:
        """Pending 메시지 복구"""
        # XAUTOCLAIM: min_idle_time 이상 처리 안 된 메시지
        result = await self.redis.xautoclaim(
            stream,
            group,
            f"reclaimer-{POD_ID}",
            min_idle_time=self.min_idle_ms,
            count=100,
        )

        _, messages, _ = result
        for msg_id, data in messages:
            await self.process_and_ack(stream, group, msg_id, data)

        return len(messages)
```

---

## 시나리오 3: Pub/Sub Redis 다운

```
Timeline:
1. Event Router: State 업데이트 성공
2. Event Router: Pub/Sub PUBLISH 실패 (연결 끊김)
3. SSE Gateway: Pub/Sub 메시지 못 받음
4. SSE Gateway: Keepalive 타임아웃 (15초)
5. SSE Gateway: State KV 폴링 시작
6. SSE Gateway: State에서 최신 상태 획득
7. Client: 지연은 있지만 데이터 수신
```

**구현**:

```python
async def subscribe_with_fallback(
    self,
    job_id: str,
) -> AsyncIterator[dict]:
    """Pub/Sub 실패 시 State 폴링 폴백"""
    last_seq = 0
    pubsub_silent_count = 0

    while True:
        try:
            # Pub/Sub 대기 (15초 타임아웃)
            event = await asyncio.wait_for(
                self._wait_pubsub(job_id),
                timeout=self.keepalive_interval,
            )
            pubsub_silent_count = 0
            yield event

        except asyncio.TimeoutError:
            pubsub_silent_count += 1

            # 3회 연속 타임아웃 → State 폴링
            if pubsub_silent_count >= 3:
                state = await self._get_state(job_id)
                if state and state.get("seq", 0) > last_seq:
                    yield state
                    last_seq = state["seq"]

            # Keepalive 전송
            yield {"type": "keepalive"}
```

---

## 시나리오 4: SSE Gateway 크래시

```
Timeline:
1. Client: SSE 연결 중
2. Gateway-0: 크래시
3. Client: EventSource onerror 발생
4. Client: 자동 재연결 (브라우저 기본)
5. Client: last_seq 파라미터와 함께 재연결
6. Gateway-1: 새 연결 수신
7. Gateway-1: State KV에서 현재 상태 조회
8. Gateway-1: Streams에서 누락 이벤트 Catch-up
9. Client: 중복 없이 이벤트 재수신
```

**클라이언트 구현**:

```javascript
class ResilientEventSource {
  constructor(baseUrl, jobId) {
    this.baseUrl = baseUrl;
    this.jobId = jobId;
    this.lastSeq = 0;
    this.connect();
  }

  connect() {
    const url = `${this.baseUrl}?job_id=${this.jobId}&last_seq=${this.lastSeq}`;
    this.eventSource = new EventSource(url);

    this.eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.seq) {
        this.lastSeq = data.seq;  // seq 업데이트
      }
      this.onEvent(data);
    };

    this.eventSource.onerror = () => {
      // 자동 재연결 시 last_seq 유지
      setTimeout(() => this.connect(), 1000);
    };
  }
}
```

---

## 시나리오 5: Streams Redis 다운

```
Timeline:
1. Worker: XADD 실패 (연결 끊김)
2. Worker: Exception → Celery retry (exponential backoff)
3. Celery: 3회 재시도 후 DLQ (Dead Letter Queue)
4. 운영팀: DLQ 모니터링 알림 수신
5. Redis 복구 후 DLQ 재처리
```

**구현**:

```python
@celery.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    retry_backoff=True,
)
async def process_scan(self, job_id: str, ...):
    try:
        result = await do_scan(job_id)
        await publish_event(job_id, "done", 51, result)
    except RedisConnectionError as e:
        logger.error(f"Redis connection failed: {e}")
        raise self.retry(exc=e)
```

---

## Health Check 엔드포인트

```python
@app.get("/health")
async def health():
    """Liveness probe"""
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    """Readiness probe - 의존성 확인"""
    checks = {}

    # Redis Streams 연결
    try:
        await streams_redis.ping()
        checks["streams_redis"] = "ok"
    except Exception as e:
        checks["streams_redis"] = str(e)

    # Redis Pub/Sub 연결
    try:
        await pubsub_redis.ping()
        checks["pubsub_redis"] = "ok"
    except Exception as e:
        checks["pubsub_redis"] = str(e)

    all_ok = all(v == "ok" for v in checks.values())
    status_code = 200 if all_ok else 503

    return JSONResponse(
        content={"checks": checks},
        status_code=status_code,
    )
```

---

## 모니터링 알림

```yaml
# Prometheus AlertManager rules
groups:
  - name: event-bus
    rules:
      - alert: EventRouterPendingHigh
        expr: redis_stream_pending_messages > 1000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Event Router pending messages high"

      - alert: SSEConnectionsSpike
        expr: rate(sse_connections_active[5m]) > 100
        for: 2m
        labels:
          severity: warning

      - alert: EventProcessingLatencyHigh
        expr: histogram_quantile(0.99, event_router_latency_seconds) > 1
        for: 5m
        labels:
          severity: critical
```
