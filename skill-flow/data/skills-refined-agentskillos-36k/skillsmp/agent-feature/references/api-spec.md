# Agent API Specification

> Agent 페이지 백엔드 API 엔드포인트 및 SSE 이벤트 형식

## 1. API 엔드포인트

### 1.1 대화 관리

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/v1/chat` | 대화 목록 조회 |
| POST | `/api/v1/chat` | 새 대화 생성 |
| DELETE | `/api/v1/chat/{chat_id}` | 대화 삭제 |
| PATCH | `/api/v1/chat/{chat_id}` | 대화 제목 수정 |

### 1.2 메시지

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/v1/chat/{chat_id}/messages` | 메시지 전송 |
| GET | `/api/v1/chat/{job_id}/events` | SSE 스트림 구독 |

---

## 2. 요청/응답 형식

### 2.1 대화 목록 조회

**Request:**
```http
GET /api/v1/chat?limit=20&cursor={cursor}
Cookie: s_access={JWT}
```

**Response:**
```typescript
interface ChatListResponse {
  chats: ChatSummary[];
  next_cursor: string | null;
}

interface ChatSummary {
  id: string;              // UUID
  title: string | null;    // 대화 제목
  preview: string | null;  // 마지막 메시지 미리보기 (100자)
  message_count: number;
  last_message_at: string | null;  // ISO 8601
  created_at: string;
}
```

### 2.2 새 대화 생성

**Request:**
```http
POST /api/v1/chat
Content-Type: application/json
Cookie: s_access={JWT}

{
  "title": "새 대화"  // optional
}
```

**Response:**
```json
{
  "id": "96a34b5b-6462-477c-b907-71f87f49b7d4",
  "title": null,
  "created_at": "2026-01-19T12:00:00Z"
}
```

### 2.3 메시지 전송

**Request:**
```http
POST /api/v1/chat/{chat_id}/messages
Content-Type: application/json
Cookie: s_access={JWT}

{
  "message": "플라스틱 분리배출 방법 알려줘",
  "image_url": "https://...",           // optional
  "user_location": {                     // optional
    "latitude": 37.5665,
    "longitude": 126.9780
  }
}
```

**Response:**
```json
{
  "job_id": "79d0f98c-5b77-4455-96cd-2eb409620612",
  "stream_url": "/api/v1/chat/79d0f98c-5b77-4455-96cd-2eb409620612/events",
  "status": "queued"
}
```

---

## 3. SSE 이벤트 형식

### 3.1 이벤트 타입 개요

| Event | 설명 | 중요도 |
|-------|------|--------|
| `token` | 실시간 토큰 스트리밍 | **핵심** |
| `token_recovery` | 늦은 구독자용 스냅샷 | **핵심** |
| `intent` | Intent 분류 결과 | 선택 |
| `router` | 라우팅 완료 | 선택 |
| `answer` | 답변 생성 상태 | 선택 |
| `done` | 전체 완료 + 최종 결과 | **핵심** |
| `keepalive` | 연결 유지 | 무시 |

### 3.2 token 이벤트 (실시간 스트리밍)

```
event: token
data: {"content":"플","seq":1001,"node":"answer"}

event: token
data: {"content":"라","seq":1002,"node":"answer"}

event: token
data: {"content":"스","seq":1003,"node":"answer"}
```

**필드:**
| 필드 | 타입 | 설명 |
|------|------|------|
| `content` | string | 토큰 텍스트 (UTF-8) |
| `seq` | number | 시퀀스 번호 (1001부터) |
| `node` | string | 생성 노드 ("answer") |

### 3.3 token_recovery 이벤트 (늦은 구독)

```
event: token_recovery
data: {
  "stage": "token_recovery",
  "status": "snapshot",
  "accumulated": "무색 **음료/생수 페트병(PET)**이라면...",
  "last_seq": 1175,
  "completed": true
}
```

**사용 시나리오:**
- 새로고침 후 기존 스트리밍 복구
- 네트워크 끊김 후 재연결
- `completed: true`면 더 이상 token 이벤트 없음

### 3.4 done 이벤트 (최종 결과)

```
event: done
data: {
  "job_id": "79d0f98c-5b77-4455-96cd-2eb409620612",
  "stage": "done",
  "status": "completed",
  "seq": 171,
  "progress": 100,
  "result": {
    "intent": "waste",
    "answer": "무색 **음료/생수 페트병(PET)**이라면...",
    "persistence": {
      "conversation_id": "96a34b5b-6462-477c-b907-71f87f49b7d4",
      "user_id": "8b8ec006-2d95-45aa-bdef-e08201f1bb82",
      "user_message": "플라스틱 페트병 분리배출 방법 알려줘",
      "assistant_message": "무색 **음료/생수 페트병(PET)**이라면...",
      "assistant_message_created_at": "2026-01-19T12:00:00Z"
    }
  }
}
```

---

## 4. SSE 연결 구현

### 4.1 EventSource 사용

```typescript
const subscribeSSE = (jobId: string) => {
  const url = `${import.meta.env.VITE_API_URL}/api/v1/chat/${jobId}/events`;

  const eventSource = new EventSource(url, {
    withCredentials: true,  // 쿠키 인증 필수
  });

  eventSource.addEventListener('token', (e) => {
    const data = JSON.parse(e.data);
    // data.content를 누적
  });

  eventSource.addEventListener('token_recovery', (e) => {
    const data = JSON.parse(e.data);
    // data.accumulated로 초기화
  });

  eventSource.addEventListener('done', (e) => {
    const data = JSON.parse(e.data);
    // 최종 결과 처리
    eventSource.close();
  });

  eventSource.onerror = (e) => {
    console.error('SSE error:', e);
    eventSource.close();
  };

  return eventSource;
};
```

### 4.2 생성 중단

```typescript
const stopGeneration = (eventSource: EventSource) => {
  eventSource.close();
  // UI 상태 업데이트
};
```

---

## 5. Intent 분류 (참고)

| Intent | 설명 |
|--------|------|
| `WASTE` | 분리배출 질문 |
| `CHARACTER` | 캐릭터 정보 |
| `LOCATION` | 장소 검색 |
| `BULK_WASTE` | 대형폐기물 |
| `RECYCLABLE_PRICE` | 재활용 시세 |
| `COLLECTION_POINT` | 수거함 위치 |
| `WEB_SEARCH` | 웹 검색 |
| `IMAGE_GENERATION` | 이미지 생성 |
| `GENERAL` | 일반 대화 |

---

## 6. 에러 처리

### HTTP 에러
| 코드 | 원인 | 처리 |
|------|------|------|
| 401 | 토큰 만료 | 갱신 후 재시도 (Axios 인터셉터) |
| 403 | 권한 없음 | 로그인 페이지 리디렉트 |
| 404 | 대화/작업 없음 | 에러 UI 표시 |

### SSE 에러
```typescript
eventSource.onerror = (e) => {
  // 자동 재연결 시도 (EventSource 기본 동작)
  // 3회 실패 시 에러 UI 표시
};
```

---

## 7. 클러스터 환경

```
Client
  ↓
ALB (api.dev.growbin.app)
  ↓
Istio Gateway
  ↓
VirtualService (chat-vs)
  ├─ /api/v1/chat/{job_id}/events → sse-gateway
  └─ /api/v1/chat/* → chat-api
```

**쿠키 → Header 변환:**
- Client: `Cookie: s_access=<JWT>`
- Backend: `Authorization: Bearer <JWT>` (EnvoyFilter 자동 변환)
