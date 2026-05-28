# SSE 표준 구현

## SSE 이벤트 포맷

Server-Sent Events (SSE) 표준에 따른 이벤트 포맷입니다.

```
event: <event-type>
id: <event-id>
data: <json-payload>

```

### 필수 필드

| 필드 | 용도 | 예시 |
|------|------|------|
| `event:` | 이벤트 타입 (클라이언트 핸들러 분기) | `answer`, `token`, `done` |
| `id:` | 이벤트 식별자 (재연결 시 복구용) | `1737415902456-0` |
| `data:` | JSON 페이로드 | `{"job_id": "...", "seq": 16}` |

---

## id 필드와 Last-Event-ID

### SSE 표준 동작

1. 서버가 `id:` 필드를 포함하여 이벤트 전송
2. 클라이언트(브라우저)가 마지막 `id` 값을 저장
3. 연결 끊김 시 자동 재연결
4. 재연결 요청에 `Last-Event-ID` 헤더 포함
5. 서버가 해당 ID 이후 이벤트만 전송

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SSE Last-Event-ID Recovery Flow                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Browser (EventSource)              SSE Gateway                             │
│        │                                  │                                 │
│        │───── GET /events ───────────────►│                                 │
│        │                                  │                                 │
│        │◄──── event: answer ─────────────│                                 │
│        │      id: 1737415902456-0         │                                 │
│        │      data: {...}                 │                                 │
│        │                                  │                                 │
│        │◄──── event: token ──────────────│                                 │
│        │      id: 1737415902500-1         │                                 │
│        │      data: {...}                 │                                 │
│        │                                  │                                 │
│   [연결 끊김]                              │                                 │
│        │                                  │                                 │
│        │───── GET /events ───────────────►│                                 │
│        │      Last-Event-ID:              │                                 │
│        │      1737415902500-1             │                                 │
│        │                                  │                                 │
│        │◄──── (누락 이벤트만 전송) ────────│                                 │
│        │      id: 1737415902600-0         │                                 │
│        │      ...                         │                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## stream_id를 SSE id로 사용

Redis Stream ID는 단조 증가하므로 SSE `id:` 필드로 적합합니다.

```python
# Event Router: stream_id 주입
event["stream_id"] = event_id  # Redis Stream ID (예: "1737415902456-0")

# SSE Gateway: id 필드로 사용
async def event_generator():
    async for event in manager.subscribe(job_id, last_event_id):
        stream_id = event.get("stream_id", "")
        stage = event.get("stage", "message")

        yield {
            "event": stage,
            "id": stream_id,  # ⚠️ 핵심: SSE 표준 id 필드
            "data": json.dumps(event),
        }
```

---

## FastAPI StreamingResponse 구현

```python
from fastapi import Request
from fastapi.responses import StreamingResponse

@router.get("/{service}/{job_id}/events")
async def stream_events_restful(
    request: Request,
    service: str,
    job_id: str,
):
    """SSE 스트리밍 엔드포인트"""
    # Last-Event-ID 헤더 확인
    last_event_id = request.headers.get("Last-Event-ID", "0-0")

    async def event_generator():
        async for event in broadcast_manager.subscribe(job_id, last_event_id):
            stream_id = event.get("stream_id", "")
            stage = event.get("stage", "message")

            # SSE 표준 포맷
            yield f"event: {stage}\n"
            yield f"id: {stream_id}\n"
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
```

---

## 이벤트 스키마

### Stage 이벤트

```
event: answer
id: 1737415902456-0
data: {
  "job_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "stage": "answer",
  "status": "completed",
  "seq": 16,
  "progress": 100,
  "result": { ... },
  "message": "응답 생성 완료",
  "stream_id": "1737415902456-0"
}
```

### Token 이벤트

```
event: token
id: 1737415902500-1
data: {
  "stage": "token",
  "status": "streaming",
  "seq": 1001,
  "content": "안녕",
  "node": "answer",
  "stream_id": "1737415902500-1"
}
```

### Done 이벤트

```
event: done
id: 1737415902600-0
data: {
  "stage": "done",
  "status": "completed",
  "seq": 17,
  "message": "완료",
  "stream_id": "1737415902600-0"
}
```

---

## 이벤트 필드 정의

| 필드 | 타입 | 설명 |
|------|------|------|
| `job_id` | UUID | 메시지별 작업 식별자 |
| `stage` | string | 파이프라인 단계명 |
| `status` | string | 처리 상태 (started, completed, streaming, failed) |
| `seq` | int | 시퀀스 번호 (Stage: 0~180, Token: 1000+) |
| `progress` | int | 진행률 0~100 (선택적) |
| `result` | object | 완료 시 결과 데이터 (선택적) |
| `message` | string | UI 표시용 메시지 (선택적) |
| `content` | string | 토큰 내용 (token 이벤트 전용) |
| `node` | string | 토큰 발생 노드명 (token 이벤트 전용) |
| `stream_id` | string | Redis Stream ID (SSE id 필드) |

---

## 클라이언트 구현 (JavaScript)

```javascript
class ResilientEventSource {
  constructor(url, jobId) {
    this.url = url;
    this.jobId = jobId;
    this.connect();
  }

  connect() {
    // Last-Event-ID는 브라우저가 자동으로 헤더에 포함
    this.eventSource = new EventSource(`${this.url}/${this.jobId}/events`);

    // 이벤트 타입별 핸들러
    this.eventSource.addEventListener('answer', (e) => {
      const data = JSON.parse(e.data);
      this.onAnswer(data);
    });

    this.eventSource.addEventListener('token', (e) => {
      const data = JSON.parse(e.data);
      this.onToken(data);
    });

    this.eventSource.addEventListener('done', (e) => {
      const data = JSON.parse(e.data);
      this.onDone(data);
      this.eventSource.close();
    });

    // 에러 시 자동 재연결 (브라우저 기본 동작)
    // Last-Event-ID 헤더가 자동으로 포함됨
    this.eventSource.onerror = (error) => {
      console.log('SSE connection error, will auto-reconnect');
    };
  }
}
```

---

## 체크리스트

- [ ] 모든 이벤트에 `stream_id`가 포함되어 있는가?
- [ ] SSE 응답에 `id:` 필드가 포함되어 있는가?
- [ ] `Last-Event-ID` 헤더를 처리하는가?
- [ ] 재연결 시 누락 이벤트만 전송하는가?
