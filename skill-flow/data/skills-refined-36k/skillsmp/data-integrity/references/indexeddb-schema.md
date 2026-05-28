# Chat ID / Session ID 검증 리포트

**작성일**: 2026-01-23
**대상**: Frontend IndexedDB 스키마 v3
**참조**: backend-event-router-improvement 리포트, Explore 에이전트 분석

---

## 1. ID 관계 검증

### 1.1 ID 정의 매핑

| ID | Backend | Frontend | IndexedDB | 설명 |
|---|---|---|---|---|
| **chat_id** | `Message.chat_id` (FK) | `currentChat.id` | `session_id` | 채팅 세션 UUID |
| **conversation_id** | `chat_conversations.id` | - | - | chat_id와 동일 (테이블 PK) |
| **session_id** | Worker 내부 추적 | - | `session_id` | = chat_id (동일 값) |
| **user_id** | `users_accounts.id` | `userId` | `user_id` | 사용자 격리 |
| **job_id** | 메시지별 작업 UUID | `response.job_id` | - | SSE 스트림 식별 |

### 1.2 계층 구조 검증

```
Backend DB:
  users_accounts.id (PK)
    └─ chat_conversations.id (PK, user_id FK)
       └─ chat_messages.id (PK, chat_id FK → conversations.id)

Frontend IndexedDB v3:
  user_id (users_accounts.id)
    └─ session_id (chat_conversations.id = chat_id)
       └─ client_id (PK) + created_at (정렬)
```

✅ **검증 결과**: 계층 구조 일치

---

## 2. SSE 이벤트 스키마 검증

### 2.1 일반 이벤트 (Stage/Token)

Explore 에이전트 분석 결과:
- `chat_id` 포함 **안 함**
- 이유: SSE 채널이 `job_id` 기반 (`sse:events:{job_id}`)
- Frontend가 이미 `currentChat.id`로 context 관리

```typescript
// Stage 이벤트
{
  "job_id": "3fa85f64-...",
  "stage": "answer",
  "status": "completed",
  "seq": 16,
  "stream_id": "1737415902456-0",
  // ❌ chat_id 없음
}

// Token 이벤트
{
  "stage": "token",
  "seq": 1001,
  "content": "안녕",
  "stream_id": "1737415902500-1"
  // ❌ chat_id 없음
}
```

### 2.2 Done 이벤트 (예외)

```typescript
// Done 이벤트 - persistence에 conversation_id 포함!
{
  "stage": "done",
  "status": "completed",
  "result": {
    "intent": "greeting",
    "answer": "안녕하세요",
    "persistence": {
      "conversation_id": "a087c2eb-...",  // ✅ chat_id
      "user_id": "user-123",
      "user_message": "msg-uuid-1",
      "assistant_message": "msg-uuid-2",
      "assistant_message_created_at": "2026-01-23T00:00:00Z"
    }
  }
}
```

✅ **검증 결과**: Done 이벤트는 `persistence.conversation_id` 제공 (검증용)

---

## 3. Frontend 구현 검증

### 3.1 메시지 전송 흐름

```typescript
// useAgentChat.ts:307-314
const response = await AgentService.sendMessage(chatId, requestData);
console.log('[DEBUG] sendMessage response:', response);

// SSE 연결
console.log('[DEBUG] Connecting to SSE with job_id:', response.job_id);
connectSSE(response.job_id);
```

✅ **검증**:
- `chatId` 전달 → Backend `chat_id` 파라미터
- `response.job_id` 수신 → SSE 연결 식별자
- Explore 분석과 일치

### 3.2 IndexedDB 저장

```typescript
// useAgentChat.ts:410
const localMessages = await messageDB.getMessages(userId, chatId);

// messageDB.ts:203 메서드 시그니처
async getMessages(userId: string, sessionId: string): Promise<AgentMessage[]>
```

✅ **검증**:
- Frontend `chatId` → `sessionId` 파라미터 → IndexedDB `session_id` 필드
- `session_id` = `chat_id` (Backend conversation_id)

### 3.3 Done 이벤트 처리

```typescript
// useAgentChat.ts:159-167
if (currentChatRef.current?.id) {
  messageDB
    .updateMessageStatus(
      pendingUserMessageIdRef.current,
      'committed',
      result.persistence?.user_message,  // server_id
    )
    .catch(console.error);
}
```

✅ **검증**:
- `result.persistence?.user_message` → `server_id` 매핑
- `result.persistence?.conversation_id` 사용 안 함 (Frontend가 이미 `currentChat.id` 알고 있음)
- 불필요한 중복 없음

### 3.4 recordToMessage 필드 제거

```typescript
// messageDB.ts:433-437
private recordToMessage(record: MessageRecord): AgentMessage {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { user_id, session_id, synced, local_timestamp, ...message } = record;
  return message;
}
```

✅ **검증**:
- `user_id`, `session_id`: IndexedDB 전용 필드 (격리/그룹핑)
- `synced`, `local_timestamp`: 내부 메타데이터
- `AgentMessage` 타입으로 변환 시 제거 필요
- 수정 완료

---

## 4. 메시지 순서 식별

### 4.1 Backend

```python
# message.py:38
created_at: datetime = field(default_factory=datetime.now)
```

### 4.2 IndexedDB 인덱스

```typescript
// schema.ts:59-60
'by-user-session-created': [string, string, string];
// [user_id, session_id, created_at]
```

### 4.3 조회 로직

```typescript
// messageDB.ts:207-213
const messages = await this.db!.getAllFromIndex(
  'messages',
  'by-user-session-created',
  IDBKeyRange.bound([userId, sessionId, ''], [userId, sessionId, '\uffff']),
);

return messages.map(this.recordToMessage);
```

✅ **검증**:
- 복합 인덱스로 시간순 정렬된 메시지 조회
- `created_at` 필드로 순서 보장
- Redis Stream ID는 SSE 중복 필터링용 (별도)

---

## 5. 전체 데이터 흐름 검증

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          전체 데이터 흐름 검증                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Frontend                                                                   │
│      │ currentChat = { id: "chat-abc-123", ... }                            │
│      │                                                                      │
│      │ POST /chat/chat-abc-123/messages                                     │
│      │ body: { message: "안녕" }                                            │
│      ▼                                                                      │
│  Backend Chat API                                                           │
│      │                                                                      │
│      ├── chat_id = "chat-abc-123" (path param)                              │
│      ├── job_id = uuid4()  // "job-xyz-789"                                 │
│      ├── Worker.submit(session_id=chat_id, job_id=job_id)                   │
│      │                                                                      │
│      └── 응답: { job_id: "job-xyz-789" }                                    │
│      │                                                                      │
│      ▼                                                                      │
│  Frontend                                                                   │
│      │ connectSSE("job-xyz-789")                                            │
│      │                                                                      │
│      │ GET /api/v1/chat/job-xyz-789/events                                  │
│      │                                                                      │
│      ▼                                                                      │
│  SSE Gateway                                                                │
│      │                                                                      │
│      │ 이벤트 스트림:                                                        │
│      ├── Stage: { job_id, stage, seq, stream_id, ... }                      │
│      ├── Token: { seq, content, stream_id, ... }                            │
│      └── Done: {                                                            │
│            result: {                                                        │
│              persistence: {                                                 │
│                conversation_id: "chat-abc-123",  // ✅ 검증 가능            │
│                user_id: "user-123",                                         │
│                user_message: "msg-uuid-1",                                  │
│                assistant_message: "msg-uuid-2"                              │
│              }                                                              │
│            }                                                                │
│          }                                                                  │
│      │                                                                      │
│      ▼                                                                      │
│  Frontend                                                                   │
│      │                                                                      │
│      ├── UI 업데이트 (currentChat.id = "chat-abc-123" 사용)                  │
│      │                                                                      │
│      └── IndexedDB 저장:                                                    │
│            messageDB.saveMessages(                                          │
│              userId: "user-123",                                            │
│              sessionId: "chat-abc-123",  // = currentChat.id               │
│              messages: [...]                                                │
│            )                                                                │
│                                                                             │
│  ✅ chat_id 일관성:                                                          │
│     - Frontend context: currentChat.id = "chat-abc-123"                     │
│     - Backend DB: Message.chat_id = "chat-abc-123"                          │
│     - IndexedDB: MessageRecord.session_id = "chat-abc-123"                  │
│     - SSE Done: persistence.conversation_id = "chat-abc-123" (검증)         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. 검증 결과 요약

| 검증 항목 | 상태 | 비고 |
|---|---|---|
| ID 계층 구조 | ✅ 일치 | users → conversations → messages |
| `session_id` = `chat_id` | ✅ 동일 | 명명 차이만 있음 |
| SSE 이벤트 스키마 | ✅ 올바름 | Stage/Token에 chat_id 없음, Done에만 있음 |
| Frontend context 관리 | ✅ 올바름 | `currentChat.id`로 chat_id 추적 |
| IndexedDB 저장 | ✅ 올바름 | `userId`, `sessionId` (=chatId) 전달 |
| `recordToMessage` | ✅ 수정 완료 | `user_id`, `session_id` 제거 |
| 메시지 순서 보장 | ✅ 올바름 | `created_at` 기반 복합 인덱스 |
| Done 이벤트 검증 | ✅ 가능 | `persistence.conversation_id` 제공 |

---

## 7. 추가 권장 사항

### 7.1 Done 이벤트 검증 로직 추가 (선택)

현재는 Frontend가 `currentChat.id`를 신뢰하고 있습니다. 추가 안정성을 위해 Done 이벤트의 `conversation_id`로 검증할 수 있습니다:

```typescript
// useAgentChat.ts:143 (handleSSEComplete)
const handleSSEComplete = useCallback(
  (result: DoneEvent['result']) => {
    if (!isMountedRef.current) return;

    // ✅ 선택적 검증
    if (result.persistence?.conversation_id !== currentChatRef.current?.id) {
      console.error(
        '[SSE] conversation_id mismatch',
        'expected:', currentChatRef.current?.id,
        'received:', result.persistence?.conversation_id
      );
      // 에러 처리 또는 무시
    }

    // 기존 로직...
  },
  [onMessageComplete],
);
```

### 7.2 명명 일관성 (선택)

현재 명명:
- Backend: `chat_id`, `conversation_id` 혼용
- Frontend IndexedDB: `session_id`
- Frontend 코드: `chatId`

권장 사항: Backend 용어 통일 후 Frontend도 일치시키기

---

## 8. 결론

✅ **전체 검증 완료**

- IndexedDB v3 스키마는 Backend 계층 구조와 정확히 일치
- `session_id` = `chat_id` (명명만 다름, 값은 동일)
- SSE 이벤트 스키마 분석 일치 (Stage/Token에 chat_id 없음, Done에만 있음)
- Frontend는 context로 chat_id 관리하므로 중복 전송 불필요
- `recordToMessage` 버그 수정 완료
- 메시지 순서는 `created_at` 기반 인덱스로 보장

**현재 구현은 올바르며, Explore 에이전트 분석 결과와 일치합니다.**
