# SSE Event Format Reference

> **Last Updated**: 2026-01-19
> **검증됨**: E2E 테스트 완료 (223 token events)

## Overview

SSE Gateway에서 클라이언트로 전달되는 이벤트 형식 문서입니다.
Token streaming이 `stream_mode="messages"` 기반으로 구현되어 실시간 토큰 스트리밍이 가능합니다.

---

## Event Types

### 1. `token` - 토큰 스트리밍 이벤트

**실시간 LLM 토큰 스트리밍** - 가장 중요한 이벤트

```
event: token
data: {"content":"유","seq":1001,"node":"answer"}

event: token
data: {"content":"리","seq":1002,"node":"answer"}

event: token
data: {"content":"병","seq":1003,"node":"answer"}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `content` | string | 토큰 텍스트 (UTF-8 인코딩됨) |
| `seq` | number | 시퀀스 번호 (1001부터 시작, 연속 증가) |
| `node` | string | 생성 노드 ("answer") |

**특징**:
- `seq`는 1001부터 시작 (1000 이하는 stage 이벤트용)
- 토큰은 UTF-8 escape될 수 있음 (`\uXXXX` 형식)
- 빈 content는 전송되지 않음

---

### 2. `token_recovery` - 토큰 복구 이벤트

**늦게 구독한 클라이언트용 스냅샷** - SSE 연결이 늦어진 경우

```
event: token_recovery
data: {
  "stage": "token_recovery",
  "status": "snapshot",
  "accumulated": "무색 **음료/생수 페트병(PET)**이라면 **투명(무색) 페트병 전용 수거함**으로 분리배출하면 돼요 ♻️\n\n배출 방법은 이렇게 하면 깔끔해:\n1) **내용물 비우기** → 2) **라벨 떼기** → ...",
  "last_seq": 1175,
  "completed": true
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `stage` | string | "token_recovery" |
| `status` | string | "snapshot" |
| `accumulated` | string | 지금까지 누적된 전체 답변 텍스트 |
| `last_seq` | number | 마지막 토큰의 seq 번호 |
| `completed` | boolean | 답변 생성 완료 여부 |

**사용 시나리오**:
- 클라이언트가 SSE 연결을 늦게 시작한 경우
- 네트워크 끊김 후 재연결시
- `completed: true`면 추가 토큰 없음, `accumulated`로 전체 답변 표시

---

### 3. `intent` - Intent 분류 이벤트

```
event: intent
data: {
  "job_id": "79d0f98c-5b77-4455-96cd-2eb409620612",
  "stage": "intent",
  "status": "completed",
  "seq": 10,
  "ts": "1768800397.123456",
  "progress": 10,
  "result": {"intent": "waste", "confidence": 0.95},
  "message": "Intent 분류 완료"
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `job_id` | string | 작업 ID (UUID) |
| `stage` | string | "intent" |
| `status` | string | "started" \| "completed" |
| `seq` | number | 시퀀스 번호 (< 1000) |
| `progress` | number | 진행률 (0-100) |
| `result` | object | Intent 분류 결과 |

---

### 4. `router` - 라우팅 이벤트

```
event: router
data: {
  "job_id": "79d0f98c-5b77-4455-96cd-2eb409620612",
  "stage": "router",
  "status": "completed",
  "seq": 991,
  "ts": "1768800397.281926",
  "progress": 20,
  "result": "",
  "message": "router completed"
}
```

---

### 5. `answer` - 답변 생성 이벤트

```
event: answer
data: {
  "job_id": "79d0f98c-5b77-4455-96cd-2eb409620612",
  "stage": "answer",
  "status": "started",
  "seq": 160,
  "ts": "1768800401.4270668",
  "progress": 75,
  "message": "답변을 생성하고 있습니다..."
}

event: answer
data: {
  "job_id": "79d0f98c-5b77-4455-96cd-2eb409620612",
  "stage": "answer",
  "status": "completed",
  "seq": 161,
  "ts": "1768800401.4288013",
  "progress": 95,
  "message": "답변 생성 완료"
}
```

---

### 6. `done` - 작업 완료 이벤트

**전체 파이프라인 완료** - 최종 결과 포함

```
event: done
data: {
  "job_id": "79d0f98c-5b77-4455-96cd-2eb409620612",
  "stage": "done",
  "status": "completed",
  "seq": 171,
  "ts": "1768800401.4457195",
  "progress": 100,
  "result": {
    "intent": "waste",
    "answer": "무색 **음료/생수 페트병(PET)**이라면...",
    "persistence": {
      "conversation_id": "96a34b5b-6462-477c-b907-71f87f49b7d4",
      "user_id": "8b8ec006-2d95-45aa-bdef-e08201f1bb82",
      "user_message": "플라스틱 페트병 분리배출 방법 알려줘",
      "assistant_message": "무색 **음료/생수 페트병(PET)**이라면..."
    }
  }
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `result.intent` | string | 최종 intent |
| `result.answer` | string | 전체 답변 텍스트 |
| `result.persistence` | object | 저장된 메시지 정보 |

---

### 7. `keepalive` - 연결 유지

```
event: keepalive
data: {"timestamp": ""}
```

---

### 8. `ping` (Comment)

SSE 주석 형식의 ping:

```
: ping - 2026-01-19 05:28:52.965281+00:00
```

---

## Event Sequence (정상 흐름)

```
1. event: queued       (seq: ~1)      → 작업 대기열 등록
2. event: intent       (seq: ~10)     → Intent 분류
3. event: router       (seq: ~991)    → 라우팅 완료
4. event: answer       (seq: ~160)    → 답변 생성 시작
5. event: token        (seq: 1001+)   → 토큰 스트리밍 (실시간!)
   event: token        (seq: 1002)
   event: token        (seq: 1003)
   ...
   event: token        (seq: ~1175)
6. event: answer       (completed)    → 답변 생성 완료
7. event: done         (seq: ~171)    → 전체 완료 + 최종 결과
```

---

## Frontend Integration

### TypeScript Types

```typescript
// SSE 이벤트 타입
type SSEEventType =
  | 'token'           // 실시간 토큰 스트리밍
  | 'token_recovery'  // 늦은 구독자용 스냅샷
  | 'intent'          // Intent 분류
  | 'router'          // 라우팅
  | 'answer'          // 답변 생성 상태
  | 'done'            // 완료
  | 'error'           // 에러
  | 'keepalive';      // 연결 유지

// 토큰 이벤트
interface TokenEvent {
  content: string;    // 토큰 텍스트
  seq: number;        // 시퀀스 번호 (1001~)
  node: string;       // "answer"
}

// 토큰 복구 이벤트
interface TokenRecoveryEvent {
  stage: 'token_recovery';
  status: 'snapshot';
  accumulated: string;  // 누적된 전체 답변
  last_seq: number;     // 마지막 seq
  completed: boolean;   // 완료 여부
}

// Stage 이벤트 (intent, router, answer, done)
interface StageEvent {
  job_id: string;
  stage: string;
  status: 'started' | 'completed';
  seq: number;
  ts: string;
  progress: number;
  result: any;
  message: string;
}
```

### EventSource 사용 예시

```typescript
const eventSource = new EventSource(
  `${SSE_BASE_URL}/sse/conversations/${conversationId}/stream`,
  { withCredentials: true }
);

// 토큰 스트리밍 처리
eventSource.addEventListener('token', (event) => {
  const data: TokenEvent = JSON.parse(event.data);
  appendToMessage(data.content);  // 실시간 UI 업데이트
});

// 토큰 복구 (늦은 구독)
eventSource.addEventListener('token_recovery', (event) => {
  const data: TokenRecoveryEvent = JSON.parse(event.data);
  if (data.completed) {
    setMessage(data.accumulated);  // 전체 답변으로 대체
  }
});

// 완료 처리
eventSource.addEventListener('done', (event) => {
  const data: StageEvent = JSON.parse(event.data);
  finalizeMessage(data.result.answer);
  eventSource.close();
});

// 에러 처리
eventSource.addEventListener('error', (event) => {
  console.error('SSE Error:', event);
  eventSource.close();
});
```

---

## Sequence Number Rules

| Range | 용도 |
|-------|------|
| 1-999 | Stage 이벤트 (intent, router, answer, done) |
| 1001+ | Token 이벤트 (1001부터 연속 증가) |

---

## Notes

1. **UTF-8 Encoding**: 토큰 content는 UTF-8로 인코딩됨 (`\uXXXX` escape)
2. **Token Recovery**: 늦게 연결해도 `accumulated`로 전체 내용 복구 가능
3. **Seq 연속성**: token seq가 건너뛰면 네트워크 손실 감지 가능
4. **done 이벤트**: 항상 마지막에 전체 결과 포함 (fallback용)
