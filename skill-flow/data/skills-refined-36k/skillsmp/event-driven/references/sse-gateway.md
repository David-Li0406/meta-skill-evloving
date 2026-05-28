# SSE Gateway 구현 가이드

## 아키텍처

SSE Gateway는 클라이언트에 실시간 이벤트를 스트리밍하는 엔드포인트.

```
Client (EventSource)
    ↓
SSE Gateway
    ├─ Redis Pub/Sub 구독 (실시간)
    ├─ State KV 조회 (Recovery)
    └─ Streams XREVRANGE (Catch-up)
```

---

## Core: SSEBroadcastManager

```python
from dataclasses import dataclass, field
from asyncio import Queue
from redis.asyncio import Redis
from redis.asyncio.client import PubSub

@dataclass
class SSEBroadcastManager:
    """SSE 브로드캐스트 관리자"""

    streams_redis: Redis      # State KV, XREVRANGE
    pubsub_redis: Redis       # Pub/Sub 구독
    channel_prefix: str = "sse:events"
    state_prefix: str = "scan:state"
    queue_maxsize: int = 100
    keepalive_interval: float = 15.0

    # job_id → subscriber queues
    _subscribers: dict[str, list[Queue]] = field(default_factory=dict)
    # job_id → pubsub connection
    _pubsubs: dict[str, PubSub] = field(default_factory=dict)

    async def subscribe(
        self,
        job_id: str,
        last_seq: int = 0,
    ) -> AsyncIterator[dict]:
        """SSE 이벤트 스트림 구독"""
        queue: Queue[dict | None] = Queue(maxsize=self.queue_maxsize)

        # 1. Subscriber 등록
        if job_id not in self._subscribers:
            self._subscribers[job_id] = []
            await self._start_listener(job_id)
        self._subscribers[job_id].append(queue)

        try:
            # 2. Recovery: State KV에서 마지막 상태
            state = await self._get_state(job_id)
            if state and state.get("seq", 0) > last_seq:
                yield state

            # 3. Catch-up: 누락 이벤트 복구
            async for event in self._catch_up(job_id, last_seq):
                yield event

            # 4. Real-time: Pub/Sub 이벤트
            while True:
                try:
                    event = await asyncio.wait_for(
                        queue.get(),
                        timeout=self.keepalive_interval,
                    )
                    if event is None:  # 종료 시그널
                        break
                    if event.get("seq", 0) > last_seq:
                        yield event
                        last_seq = event["seq"]
                        if event.get("stage") == "done":
                            break
                except asyncio.TimeoutError:
                    yield {"type": "keepalive"}

        finally:
            # Cleanup
            self._subscribers[job_id].remove(queue)
            if not self._subscribers[job_id]:
                await self._stop_listener(job_id)
                del self._subscribers[job_id]

    async def _start_listener(self, job_id: str) -> None:
        """Pub/Sub 리스너 시작"""
        pubsub = self.pubsub_redis.pubsub()
        channel = f"{self.channel_prefix}:{job_id}"
        await pubsub.subscribe(channel)
        self._pubsubs[job_id] = pubsub

        asyncio.create_task(self._listen(job_id, pubsub))

    async def _listen(self, job_id: str, pubsub: PubSub) -> None:
        """Pub/Sub 메시지 수신 및 브로드캐스트"""
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    event = json.loads(message["data"])
                    await self._broadcast(job_id, event)
        except asyncio.CancelledError:
            pass
        finally:
            await pubsub.unsubscribe()

    async def _broadcast(self, job_id: str, event: dict) -> None:
        """모든 구독자에게 이벤트 전송"""
        for queue in self._subscribers.get(job_id, []):
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                # 느린 클라이언트: 오래된 이벤트 드롭
                try:
                    queue.get_nowait()
                    queue.put_nowait(event)
                except asyncio.QueueEmpty:
                    pass

    async def _get_state(self, job_id: str) -> dict | None:
        """State KV에서 현재 상태 조회"""
        key = f"{self.state_prefix}:{job_id}"
        data = await self.streams_redis.get(key)
        return json.loads(data) if data else None

    async def _catch_up(
        self,
        job_id: str,
        from_seq: int,
    ) -> AsyncIterator[dict]:
        """Streams에서 누락 이벤트 복구"""
        # Shard 계산
        shard = md5_hash(job_id) % SHARD_COUNT
        stream = f"scan:events:{shard}"

        # 최근 100개 이벤트 역순 조회
        messages = await self.streams_redis.xrevrange(
            stream,
            count=100,
        )

        # 해당 job_id 이벤트만 필터링 & 정렬
        events = []
        for _, data in messages:
            event = json.loads(data[b"data"])
            if event["job_id"] == job_id and event["seq"] > from_seq:
                events.append(event)

        # 시간순 정렬 후 반환
        for event in sorted(events, key=lambda e: e["seq"]):
            yield event

    async def _stop_listener(self, job_id: str) -> None:
        """Pub/Sub 리스너 정지"""
        if job_id in self._pubsubs:
            pubsub = self._pubsubs.pop(job_id)
            await pubsub.unsubscribe()
```

---

## FastAPI Endpoint

```python
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse

app = FastAPI()
manager = SSEBroadcastManager(...)

@app.get("/api/v1/stream")
async def stream_events(
    job_id: str = Query(...),
    last_seq: int = Query(default=0),
):
    """SSE 스트리밍 엔드포인트"""

    async def event_generator():
        async for event in manager.subscribe(job_id, last_seq):
            if event.get("type") == "keepalive":
                yield ": keepalive\n\n"
            else:
                yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Nginx buffering 비활성화
        },
    )
```

---

## Client (Frontend)

```javascript
// EventSource 사용
const eventSource = new EventSource(
  `/api/v1/stream?job_id=${jobId}&last_seq=${lastSeq}`
);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);

  switch (data.stage) {
    case 'vision':
      updateVisionProgress(data);
      break;
    case 'answer':
      appendAnswer(data.content);
      break;
    case 'done':
      eventSource.close();
      break;
  }

  lastSeq = data.seq;
};

eventSource.onerror = (error) => {
  // 자동 재연결 (브라우저 기본 동작)
  // last_seq 파라미터로 중복 방지
};
```

---

## Multi-Domain 지원

```python
# 도메인별 State prefix 매핑
DOMAIN_STATE_PREFIXES = {
    "scan": "scan:state:",
    "chat": "chat:state:",
}

async def get_state(domain: str, job_id: str) -> dict | None:
    prefix = DOMAIN_STATE_PREFIXES.get(domain, "scan:state:")
    key = f"{prefix}{job_id}"
    return await redis.get(key)
```

---

## Metrics

```python
SSE_CONNECTIONS_ACTIVE = Gauge(
    "sse_connections_active",
    "Active SSE connections",
)

SSE_EVENTS_SENT = Counter(
    "sse_events_sent_total",
    "Total events sent to clients",
    ["domain", "stage"],
)

SSE_TTFB = Histogram(
    "sse_ttfb_seconds",
    "Time to first byte",
    ["domain"],
)

SSE_CONNECTION_DURATION = Histogram(
    "sse_connection_duration_seconds",
    "SSE connection duration",
    buckets=[1, 5, 10, 30, 60, 120, 300],
)
```

---

## 에러 처리

```python
async def stream_with_timeout(
    manager: SSEBroadcastManager,
    job_id: str,
    max_wait: int = 300,
) -> AsyncIterator[dict]:
    """타임아웃 처리가 포함된 스트리밍"""
    start = time.monotonic()

    async for event in manager.subscribe(job_id):
        yield event

        # 최대 대기 시간 초과
        if time.monotonic() - start > max_wait:
            yield {"type": "error", "message": "Timeout"}
            break

        # done 이벤트로 정상 종료
        if event.get("stage") == "done":
            break
```
