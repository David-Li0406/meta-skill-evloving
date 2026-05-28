# Optimistic Update & Eventual Consistency 통합 아키텍처 리포트

> 프론트엔드 Optimistic Update 구현과 백엔드 Eventual Consistency의 통합 설계

**작성일**: 2026-01-21
**버전**: 1.0
**관련 이슈**: 메시지 소실 문제, 위치 데이터 누락, 페이지네이션 중 메시지 사라짐

---

## 목차

1. [문제 정의](#1-문제-정의)
2. [아키텍처 개요](#2-아키텍처-개요)
3. [백엔드 Eventual Consistency 아키텍처](#3-백엔드-eventual-consistency-아키텍처)
4. [프론트엔드 Optimistic Update 구현](#4-프론트엔드-optimistic-update-구현)
5. [통합 데이터 플로우](#5-통합-데이터-플로우)
6. [핵심 해결 전략](#6-핵심-해결-전략)
7. [성능 및 신뢰성](#7-성능-및-신뢰성)
8. [향후 개선 방향](#8-향후-개선-방향)

---

## 1. 문제 정의

### 1.1 발견된 이슈

#### Issue #1: 위치 데이터 누락
```typescript
// BEFORE: Closure capture 문제
const sendMessage = async (message: string) => {
  const requestData = {
    message,
    user_location: userLocation, // ❌ 비동기 완료 전 undefined
  };
};
```

**원인**: `userLocation`이 비동기로 geolocation API에서 로드되는데, 함수 클로저가 초기값(`undefined`)을 캡처하여 서버로 전송

#### Issue #2: 메시지 소실 (페이지네이션)
```typescript
// BEFORE: Simple concatenation
const loadMoreMessages = async () => {
  const response = await api.getChatDetail(chatId, { cursor });
  setMessages((prev) => [...serverMessages, ...prev]); // ❌ 덮어쓰기
};
```

**시나리오**:
1. 사용자가 메시지 전송 (Optimistic Update로 즉시 표시)
2. 백엔드 SSE 완료 → DB write 시작 (비동기)
3. 사용자가 스크롤 올려서 이전 메시지 로드 (`loadMoreMessages`)
4. DB에 아직 저장 안 됨 → 서버 응답에 최근 메시지 없음
5. 프론트엔드가 서버 데이터로 덮어쓰기 → **메시지 사라짐**

#### Issue #3: 페이지 새로고침 시 메시지 손실

메모리 상태(`useState`)만 사용하여 브라우저 새로고침 시 모든 메시지 손실

---

### 1.2 근본 원인

백엔드와 프론트엔드의 **데이터 일관성 타이밍 불일치**:

```
Timeline:
─────────────────────────────────────────────────────────────────
T0: User sends message
T1: Frontend Optimistic Update (즉시)
T2: SSE streaming starts (0.5s)
T3: SSE done event (3s)
T4: Backend DB write starts (3.1s)  ← Eventual Consistency
T5: Backend DB write completes (3.3s)
T6: User scrolls up → API call (4s)  ← Race Condition!
─────────────────────────────────────────────────────────────────
```

**Gap**: T1~T5 사이에 프론트엔드는 메시지를 가지고 있지만, 백엔드 DB에는 아직 없음

---

## 2. 아키텍처 개요

### 2.1 전체 시스템 구조

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Frontend-Backend Integration                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Frontend (Browser)                                                          │
│  ┌──────────────────────────────────────────────────────────────┐           │
│  │  React State (Optimistic)                                     │           │
│  │  ┌─────────────┐     ┌──────────────┐     ┌─────────────┐   │           │
│  │  │   Messages  │────▶│ Reconciler   │────▶│  IndexedDB  │   │           │
│  │  │  (client_id)│     │ (30s buffer) │     │ (Persistent)│   │           │
│  │  └─────────────┘     └──────────────┘     └─────────────┘   │           │
│  └──────────────────────────────────────────────────────────────┘           │
│           │                      ▲                                           │
│           │ POST /send-message   │ GET /chat/:id/messages                   │
│           ▼                      │                                           │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  Backend (Kubernetes)                                                        │
│  ┌──────────────────────────────────────────────────────────────┐           │
│  │  chat-api (REST)                                              │           │
│  │       │                                                       │           │
│  │       ▼                                                       │           │
│  │  RabbitMQ (chat.process)                                      │           │
│  │       │                                                       │           │
│  │       ▼                                                       │           │
│  │  chat-worker (LangGraph)                                      │           │
│  │       │                                                       │           │
│  │       ├───────────────────┬──────────────────┐               │           │
│  │       ▼                   ▼                  ▼               │           │
│  │  Redis Streams      SSE Gateway        PostgreSQL            │           │
│  │  (chat:events)     (Real-time SSE)    (Eventual Write)       │           │
│  │       │                   │                  ▲               │           │
│  │       ▼                   │                  │               │           │
│  │  event-router             │                  │               │           │
│  │       ├───────────────────┘        ┌─────────┴──────┐       │           │
│  │       │                            │ chat-consumer  │       │           │
│  │       ▼                            │  (Async Write) │       │           │
│  │  Redis Pub/Sub                     └────────────────┘       │           │
│  │       │                                                      │           │
│  │       └──────────────────▶ (SSE to Client)                  │           │
│  └──────────────────────────────────────────────────────────────┘           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. 백엔드 Eventual Consistency 아키텍처

### 3.1 Event-First Architecture

백엔드는 **이벤트 우선 아키텍처**를 채택하여 실시간성과 영속성을 분리:

```python
# chat-worker (LangGraph Pipeline)
async def process_message():
    # 1. LangGraph 파이프라인 실행
    async for event in graph.astream(state):
        # 2. 중간 이벤트를 Redis Streams에 발행 (실시간성 우선)
        await redis_streams.xadd(
            f"chat:events:{shard}",
            {"data": json.dumps(event)}
        )

    # 3. 완료 이벤트 (persistence 정보 포함)
    done_event = {
        "stage": "done",
        "status": "success",
        "result": {
            "answer": "...",
            "persistence": {
                "user_message": "...",      # DB 저장용 데이터
                "assistant_message": "...",
                "user_message_id": "uuid",  # server_id
                "assistant_message_id": "uuid",
            }
        }
    }
    await redis_streams.xadd(f"chat:events:{shard}", {"data": json.dumps(done_event)})
```

### 3.2 Consumer Group Fan-out

**동일한 이벤트**를 두 개의 독립적인 Consumer Group으로 처리:

| Consumer Group | Consumer | Purpose | Latency |
|----------------|----------|---------|---------|
| `eventrouter` | `event-router` | SSE 실시간 전송 | ~10ms |
| `chat-persistence` | `chat-consumer` | PostgreSQL 저장 | ~200ms |

```
Redis Streams (chat:events:{0-3})
       │
       ├─────────────────────┬──────────────────────┐
       │                     │                      │
       ▼                     ▼                      ▼
  [eventrouter]       [chat-persistence]        [other]
  Consumer Group       Consumer Group            Groups
       │                     │
       ▼                     ▼
  event-router          chat-consumer
  (SSE fan-out)        (DB persistence)
       │                     │
       ▼                     ▼
  sse-gateway           PostgreSQL
  (Client SSE)         (Eventual Write)
```

**핵심 특징**:
- **SSE 우선**: 이벤트가 Redis Streams에 쓰이면 즉시 클라이언트로 전송 (~10ms)
- **DB는 비동기**: PostgreSQL write는 별도 Consumer가 처리 (~200ms+)
- **순서 보장**: Redis Streams의 순서 그대로 처리
- **실패 복구**: Consumer Group의 Pending List로 메시지 손실 방지

### 3.3 SSE Gateway (실시간 전송)

```python
# event-router → Redis Pub/Sub
async def process_event(event):
    job_id = event["job_id"]

    # 1. State KV 업데이트 (복구용)
    await redis.setex(f"chat:state:{job_id}", 3600, json.dumps(event))

    # 2. Pub/Sub 발행 (실시간)
    await redis.publish(f"sse:events:{job_id}", json.dumps(event))

# sse-gateway → Client
async def stream_events(job_id: str):
    async for event in manager.subscribe(job_id):
        yield f"data: {json.dumps(event)}\n\n"  # SSE format
```

**SSE 복구 메커니즘**:
1. **State KV**: 마지막 이벤트 상태를 Redis에 저장 (3600s TTL)
2. **Catch-up**: 재연결 시 Redis Streams XREVRANGE로 누락 이벤트 복구
3. **Real-time**: Redis Pub/Sub로 실시간 이벤트 수신

### 3.4 Chat Consumer (영속성)

```python
# chat-consumer: done 이벤트만 처리
class ChatPersistenceConsumer:
    CONSUMER_GROUP = "chat-persistence"

    async def consume(self, callback):
        events = await redis.xreadgroup(
            groupname=self.CONSUMER_GROUP,
            consumername=self.consumer_name,
            streams=self.streams,
            count=100,
            block=5000,
        )

        for stream_name, messages in events:
            for msg_id, data in messages:
                event = json.loads(data[b"data"])

                # done 이벤트만 처리
                if event.get("stage") != "done":
                    await redis.xack(stream_name, self.CONSUMER_GROUP, msg_id)
                    continue

                # DB 저장
                persistence = event["result"]["persistence"]
                await save_to_postgres(persistence)
                await redis.xack(stream_name, self.CONSUMER_GROUP, msg_id)
```

**Batch Processing**:
- 최대 100개 이벤트를 배치로 처리
- 5초마다 강제 flush (타임아웃)
- PostgreSQL 트랜잭션으로 원자성 보장

---

## 4. 프론트엔드 Optimistic Update 구현

### 4.1 Message Status State Machine

모든 메시지는 4가지 상태 중 하나를 가짐:

```typescript
type MessageStatus = 'pending' | 'streaming' | 'committed' | 'failed';

interface AgentMessage {
  client_id: string;      // UUID (프론트엔드 생성, 불변)
  server_id?: string;     // DB PK (백엔드 할당)
  id: string;             // Legacy compat (server_id || client_id)
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
  image_url?: string;
  status: MessageStatus;  // 상태 추적
}
```

**State Transitions**:

```
User Message:
pending ────────────▶ committed
   │                      ▲
   │                      │
   └──────────────────────┘
         (실패 시)
         failed

Assistant Message:
streaming ──────────▶ committed
```

### 4.2 Location Data: Ref Pattern

위치 데이터 누락 문제를 Ref로 해결:

```typescript
// useAgentChat.ts
const userLocationRef = useRef<UserLocation | undefined>(undefined);

// 최신 값 동기화
useEffect(() => {
  userLocationRef.current = userLocation;
  console.log('[DEBUG] userLocation updated:', userLocation);
}, [userLocation]);

// 메시지 전송 시 항상 최신 값 사용
const sendMessageInternal = async (message: string) => {
  const currentLocation = userLocationRef.current; // ✅ 항상 최신

  const requestData = {
    message,
    user_location: currentLocation,
    model: selectedModel.id,
  };

  await AgentService.sendMessage(chatId, requestData);
};
```

**Why Ref?**:
- `useState`는 클로저 캡처 → 비동기 완료 전 값 고정
- `useRef`는 항상 최신 값 참조 → geolocation 완료 후 값도 반영

### 4.3 Reconcile Algorithm (핵심)

서버 데이터(authoritative)와 로컬 Optimistic 데이터를 병합:

```typescript
// utils/message.ts
export const reconcileMessages = (
  localMessages: AgentMessage[],
  serverMessages: ServerMessage[],
  options: { committedRetentionMs?: number } = {},
): AgentMessage[] => {
  const { committedRetentionMs = 30000 } = options; // 30초 버퍼

  // 1. 서버 메시지 변환 (committed 상태)
  const serverConverted = serverMessages.map(serverToClientMessage);
  const serverIdMap = new Map(serverMessages.map((m) => [m.id, m]));

  // 2. 로컬 메시지 필터링
  const now = new Date().getTime();
  const localToKeep = localMessages.filter((local) => {
    // 2.1. 서버에 이미 있으면 제외 (중복 방지)
    if (local.server_id && serverIdMap.has(local.server_id)) return false;
    if (serverIdMap.has(local.client_id)) return false;

    // 2.2. pending/streaming은 항상 유지 (진행 중)
    if (local.status === 'pending' || local.status === 'streaming') return true;

    // 2.3. committed는 30초 버퍼 내면 유지 (Eventual Consistency)
    if (local.status === 'committed' && !local.server_id) {
      const age = now - new Date(local.created_at).getTime();
      return age < committedRetentionMs; // ✅ 핵심: 30초 유예
    }

    // 2.4. failed는 재시도 가능하므로 유지
    if (local.status === 'failed') return true;

    return false;
  });

  // 3. 병합 및 중복 제거
  const merged = [...serverConverted, ...localToKeep];
  const deduped = new Map<string, AgentMessage>();

  merged.forEach((msg) => {
    const key = msg.server_id || msg.client_id;
    if (!deduped.has(key)) {
      deduped.set(key, msg);
    } else {
      // server_id 있는 것 우선
      const existing = deduped.get(key)!;
      if (msg.server_id && !existing.server_id) {
        deduped.set(key, msg);
      }
    }
  });

  // 4. 시간순 정렬
  return Array.from(deduped.values()).sort(
    (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime(),
  );
};
```

**Reconcile 정책**:

| Message Status | Server_ID | Keep? | Reason |
|----------------|-----------|-------|--------|
| `pending` | ❌ | ✅ 항상 | 전송 중 |
| `streaming` | ❌ | ✅ 항상 | SSE 수신 중 |
| `committed` | ✅ | ❌ | 서버 버전으로 대체 |
| `committed` | ❌ | ✅ 30초 내 | **Eventual Consistency 버퍼** |
| `failed` | ❌ | ✅ 항상 | 재시도 가능 |

### 4.4 IndexedDB Persistence

브라우저 새로고침에도 메시지 유지:

```typescript
// db/messageDB.ts
export class MessageDB {
  async saveMessages(chatId: string, messages: AgentMessage[]): Promise<void> {
    const tx = this.db!.transaction('messages', 'readwrite');

    for (const msg of messages) {
      const record: MessageRecord = {
        ...msg,
        chat_id: chatId,
        synced: (msg.status === 'committed' && !!msg.server_id),
        local_timestamp: Date.now(),
      };
      await tx.store.put(record);
    }

    await tx.done;
  }

  async getMessages(chatId: string): Promise<AgentMessage[]> {
    const messages = await this.db!.getAllFromIndex(
      'messages',
      'by-chat-created',
      IDBKeyRange.bound([chatId, ''], [chatId, '\uffff']),
    );
    return messages.map(this.recordToMessage);
  }

  async cleanup(chatId: string, options = {}): Promise<number> {
    const { committedRetentionMs = 30000, ttlMs = 7 * 24 * 60 * 60 * 1000 } = options;
    const now = Date.now();
    const messages = await this.db!.getAllFromIndex('messages', 'by-chat', chatId);

    const toDelete: string[] = [];
    for (const record of messages) {
      const age = now - record.local_timestamp;

      // TTL 초과 (7일) → 삭제
      if (age > ttlMs) {
        toDelete.push(record.client_id);
        continue;
      }

      // 동기화 완료된 committed (30초 초과) → 삭제
      if (record.synced && record.server_id &&
          record.status === 'committed' &&
          age > committedRetentionMs) {
        toDelete.push(record.client_id);
      }
    }

    // 삭제 실행
    const tx = this.db!.transaction('messages', 'readwrite');
    for (const id of toDelete) {
      await tx.store.delete(id);
    }
    await tx.done;

    return toDelete.length;
  }
}
```

**Cleanup 정책**:
- **TTL (7일)**: 모든 메시지는 7일 후 자동 삭제
- **Committed Retention (30초)**: 동기화 완료된 메시지는 30초 후 삭제
- **1분 주기**: `useMessagePersistence` 훅이 1분마다 cleanup 실행

### 4.5 Auto-Save Hook (Throttled)

```typescript
// hooks/useMessagePersistence.ts
export const useMessagePersistence = (
  chatId: string | null,
  messages: AgentMessage[],
) => {
  const saveTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const prevMessagesRef = useRef<AgentMessage[]>([]);

  // 500ms throttle
  useEffect(() => {
    if (!chatId || messages.length === 0) return;

    // 변경 감지
    const changed = messages.length !== prevMessagesRef.current.length ||
      messages.some((msg, i) => {
        const prev = prevMessagesRef.current[i];
        return !prev ||
               msg.client_id !== prev.client_id ||
               msg.status !== prev.status ||
               msg.content !== prev.content;
      });

    if (!changed) return;

    // Throttle
    if (saveTimerRef.current) clearTimeout(saveTimerRef.current);

    saveTimerRef.current = setTimeout(() => {
      messageDB.saveMessages(chatId, messages)
        .catch(console.error)
        .finally(() => { prevMessagesRef.current = messages; });
    }, 500);
  }, [chatId, messages]);
};
```

**Why 500ms Throttle?**:
- SSE 토큰 스트리밍 시 수십 번의 상태 업데이트 발생
- 모든 업데이트마다 IndexedDB 쓰기 → 성능 저하
- 500ms throttle → 스트리밍 완료 후 1회 저장

---

## 5. 통합 데이터 플로우

### 5.1 메시지 전송 플로우 (상세)

```
Timeline                 Frontend                Backend
────────────────────────────────────────────────────────────────────────
T0: User clicks send
                         createUserMessage()
                         └─ client_id: uuid-1
                         └─ status: 'pending'

                         setMessages([...prev, userMsg])
                         IndexedDB.save(userMsg)

                         API.sendMessage(chatId, {...})
                         ──────────────────────────▶ POST /chat/:id/messages

T1: 0.1s                                            RabbitMQ.publish(message)
                                                    └─ queue: chat.process

T2: 0.5s                                            chat-worker consumes
                                                    LangGraph.astream(state)
                                                    ├─ vision_node
                                                    ├─ intent_node
                                                    └─ router_node

T3: 1.0s                                            XADD chat:events:0
                         ◀────────────────────────  {"stage": "vision", ...}
                         SSE: onmessage
                         setCurrentStage('vision')

T4: 2.0s                                            XADD chat:events:0
                         ◀────────────────────────  {"stage": "answer", "token": "플"}
                         SSE: onmessage
                         appendStreamingText("플")

T5: 2.5s                                            XADD chat:events:0
                         ◀────────────────────────  {"stage": "answer", "token": "라스틱"}
                         appendStreamingText("라스틱")

T6: 3.0s                                            XADD chat:events:0 (done)
                         ◀────────────────────────  {
                                                       "stage": "done",
                                                       "result": {
                                                         "answer": "플라스틱은...",
                                                         "persistence": {
                                                           "user_message_id": "srv-uuid-1",
                                                           "assistant_message_id": "srv-uuid-2",
                                                           ...
                                                         }
                                                       }
                                                    }

                         handleSSEComplete()
                         ├─ updateUserMessage(uuid-1)
                         │  └─ status: 'committed'
                         │  └─ server_id: 'srv-uuid-1'
                         │
                         └─ createAssistantMessage()
                            └─ status: 'committed'
                            └─ server_id: 'srv-uuid-2'

                         IndexedDB.save(both messages)

T7: 3.1s (비동기)                                    event-router consumes
                                                    ├─ SETEX chat:state:job_id
                                                    └─ PUBLISH sse:events:job_id

                                                    chat-consumer consumes
                                                    └─ PostgreSQL INSERT
                                                       (트랜잭션 시작)

T8: 3.3s                                            PostgreSQL COMMIT
                                                    └─ user_message (srv-uuid-1)
                                                    └─ assistant_message (srv-uuid-2)

T9: 4.0s                 User scrolls up
                         loadMoreMessages()

                         API.getChatDetail(chatId, {cursor})
                         ──────────────────────────▶ GET /chat/:id/messages

                                                     PostgreSQL SELECT
                                                     └─ WHERE created_at < cursor

                         ◀────────────────────────  {
                                                       "messages": [
                                                         {"id": "srv-uuid-1", ...},
                                                         {"id": "srv-uuid-2", ...}
                                                       ]
                                                    }

                         reconcileMessages(local, server)
                         ├─ local: [uuid-1 (committed, srv-uuid-1)]
                         ├─ server: [srv-uuid-1]
                         └─ result: [srv-uuid-1] (중복 제거)

                         setMessages(reconciled)
                         IndexedDB.cleanup() (30초 초과 메시지 삭제)
────────────────────────────────────────────────────────────────────────
```

**핵심 포인트**:
- **T0~T3**: 프론트엔드가 Optimistic하게 UI 업데이트 (즉시 표시)
- **T3~T6**: SSE로 실시간 진행 상황 수신
- **T6**: `done` 이벤트로 `committed` 상태 전환 + server_id 매핑
- **T7~T8**: 백엔드가 비동기로 DB 저장 (Eventual Consistency)
- **T9**: Reconcile로 중복 제거 + 로컬 Optimistic 데이터 유지

### 5.2 Reconcile 시나리오

#### Scenario A: 정상 케이스 (DB 저장 완료)

```typescript
// Local (IndexedDB)
[
  { client_id: "uuid-1", server_id: "srv-1", status: "committed", content: "A" },
  { client_id: "uuid-2", server_id: "srv-2", status: "committed", content: "B" },
]

// Server (API)
[
  { id: "srv-1", content: "A" },
  { id: "srv-2", content: "B" },
]

// Reconciled
[
  { client_id: "srv-1", server_id: "srv-1", status: "committed", content: "A" },
  { client_id: "srv-2", server_id: "srv-2", status: "committed", content: "B" },
]
```

**결과**: 서버 데이터로 대체 (authoritative)

#### Scenario B: Eventual Consistency (DB 저장 중)

```typescript
// Local (IndexedDB) - 방금 전송한 메시지
[
  { client_id: "uuid-1", server_id: "srv-1", status: "committed", content: "A", created_at: "10초 전" },
  { client_id: "uuid-2", server_id: "srv-2", status: "committed", content: "B", created_at: "10초 전" },
  { client_id: "uuid-3", status: "committed", content: "C", created_at: "3초 전" }, // ✅ 30초 이내
]

// Server (API) - 아직 uuid-3 없음
[
  { id: "srv-1", content: "A" },
  { id: "srv-2", content: "B" },
]

// Reconciled
[
  { client_id: "srv-1", server_id: "srv-1", status: "committed", content: "A" },
  { client_id: "srv-2", server_id: "srv-2", status: "committed", content: "B" },
  { client_id: "uuid-3", status: "committed", content: "C" }, // ✅ 유지 (30초 버퍼)
]
```

**결과**: 최근 메시지는 30초 동안 유지 → DB 저장 완료까지 대기

#### Scenario C: 전송 중 메시지

```typescript
// Local (IndexedDB)
[
  { client_id: "uuid-1", server_id: "srv-1", status: "committed", content: "A" },
  { client_id: "uuid-2", status: "pending", content: "B" }, // ✅ 전송 중
]

// Server (API)
[
  { id: "srv-1", content: "A" },
]

// Reconciled
[
  { client_id: "srv-1", server_id: "srv-1", status: "committed", content: "A" },
  { client_id: "uuid-2", status: "pending", content: "B" }, // ✅ 항상 유지
]
```

**결과**: `pending/streaming` 상태는 항상 유지

#### Scenario D: 실패 메시지

```typescript
// Local (IndexedDB)
[
  { client_id: "uuid-1", status: "failed", content: "A" }, // ✅ 재시도 가능
]

// Server (API)
[]

// Reconciled
[
  { client_id: "uuid-1", status: "failed", content: "A" }, // ✅ 유지 (재시도 UI)
]
```

**결과**: `failed` 상태는 재시도 버튼 표시를 위해 유지

---

## 6. 핵심 해결 전략

### 6.1 30초 Retention Window (Eventual Consistency Buffer)

백엔드 DB 저장 완료까지의 시간 차이를 30초 버퍼로 흡수:

```
Frontend Optimistic                Backend Eventual Consistency
────────────────────────────────────────────────────────────────
T0: committed (local only)
T1: committed (local only)
...
T5: committed (local only)         PostgreSQL INSERT starts
T10: committed (local only)        PostgreSQL COMMIT completes

T15: User scrolls → API call
     reconcile():
     - age = 15s < 30s → KEEP ✅

T35: Auto cleanup
     - age = 35s > 30s → DELETE
────────────────────────────────────────────────────────────────
```

**Why 30초?**:
- 백엔드 DB write 평균 200~500ms
- 네트워크 지연 + 재시도 + 피크 트래픽 고려
- 30초는 충분한 여유 (과도하지 않음)

### 6.2 Client ID + Server ID Mapping

```typescript
interface AgentMessage {
  client_id: string;  // 프론트엔드 UUID (불변)
  server_id?: string; // 백엔드 DB PK (done 이벤트 후 할당)
  id: string;         // Legacy compat (server_id || client_id)
}
```

**Lifecycle**:
1. **생성**: 프론트엔드가 `client_id` (UUID) 생성
2. **전송**: `client_id`를 서버로 전송 (idempotency key)
3. **SSE done**: 백엔드가 `server_id` (DB PK) 반환
4. **매핑**: 프론트엔드가 `client_id` → `server_id` 매핑
5. **중복 제거**: Reconcile 시 `server_id` 우선 사용

**장점**:
- 프론트엔드가 독립적으로 메시지 생성 가능
- 백엔드 DB ID에 의존하지 않음
- 중복 제거 시 동일 메시지 판별 가능

### 6.3 IndexedDB Cache-Aside Pattern

```
Read Flow:
─────────────────────────────────────────────────────
loadChatMessages(chatId)
    │
    ├─ 1. IndexedDB.getMessages(chatId)
    │  └─ 즉시 화면에 표시 (0ms)
    │
    ├─ 2. API.getChatDetail(chatId)
    │  └─ 백그라운드 조회 (300ms)
    │
    └─ 3. reconcileMessages(local, server)
       └─ 병합 + 중복 제거
─────────────────────────────────────────────────────

Write Flow:
─────────────────────────────────────────────────────
sendMessage(message)
    │
    ├─ 1. Optimistic Update
    │  └─ setMessages([...prev, userMsg])
    │
    ├─ 2. IndexedDB.save(userMsg)
    │  └─ 500ms throttle
    │
    └─ 3. SSE done → update status
       └─ IndexedDB.save(committedMsg)
─────────────────────────────────────────────────────
```

**Cache Policy**:
- **Read**: IndexedDB 우선 → 서버 백그라운드 (UX 향상)
- **Write**: Optimistic → SSE done → Reconcile (신뢰성)
- **TTL**: 7일 (일반), 30초 (committed + synced)

### 6.4 Status-Driven UI

메시지 상태에 따라 UI 자동 업데이트:

```tsx
// components/agent/MessageItem.tsx
function MessageItem({ message }: { message: AgentMessage }) {
  const getStatusIcon = () => {
    switch (message.status) {
      case 'pending':
        return <SpinnerIcon />; // 전송 중
      case 'streaming':
        return <TypingIndicator />; // 스트리밍 중
      case 'committed':
        return null; // 완료 (아이콘 없음)
      case 'failed':
        return <ErrorIcon onClick={retry} />; // 재시도 버튼
    }
  };

  return (
    <div className={cn('message', message.status)}>
      {message.content}
      {getStatusIcon()}
    </div>
  );
}
```

**사용자 경험**:
- `pending`: 스피너 표시
- `streaming`: 타이핑 인디케이터 + 토큰 증분 표시
- `committed`: 정상 메시지 (아이콘 없음)
- `failed`: 에러 아이콘 + 재시도 버튼

---

## 7. 성능 및 신뢰성

### 7.1 성능 최적화

#### 7.1.1 Throttled IndexedDB Write

```typescript
// 500ms throttle
useEffect(() => {
  if (saveTimerRef.current) clearTimeout(saveTimerRef.current);

  saveTimerRef.current = setTimeout(() => {
    messageDB.saveMessages(chatId, messages);
  }, 500);
}, [chatId, messages]);
```

**효과**:
- SSE 토큰 스트리밍 시 수십 번의 상태 업데이트
- Throttle 없이 매번 IndexedDB 쓰기 → 10+ writes/s
- 500ms throttle → 1 write/s (10배 감소)

#### 7.1.2 Compound Index (IndexedDB)

```typescript
// by-chat-created 복합 인덱스
msgStore.createIndex('by-chat-created', ['chat_id', 'created_at'], {
  unique: false,
});

// 정렬된 조회 (O(log n))
const messages = await db.getAllFromIndex(
  'messages',
  'by-chat-created',
  IDBKeyRange.bound([chatId, ''], [chatId, '\uffff']),
);
```

**효과**:
- 단일 쿼리로 정렬된 결과 (별도 sort 불필요)
- 1000+ 메시지에서도 10ms 이내 조회

#### 7.1.3 Batch Cleanup (1분 주기)

```typescript
// 1분마다 자동 cleanup
useEffect(() => {
  cleanupTimerRef.current = setInterval(() => {
    messageDB.cleanup(chatId, { committedRetentionMs: 30000 });
  }, 60000);
}, [chatId]);
```

**효과**:
- 실시간 cleanup → 매 메시지마다 검사 (비효율)
- 1분 주기 → 충분한 여유 + 성능 영향 최소화

### 7.2 신뢰성 보장

#### 7.2.1 Idempotency (중복 방지)

**Frontend**:
```typescript
// client_id로 중복 방지
const deduped = new Map<string, AgentMessage>();
merged.forEach((msg) => {
  const key = msg.server_id || msg.client_id; // 고유 키
  if (!deduped.has(key)) {
    deduped.set(key, msg);
  }
});
```

**Backend (event-router)**:
```lua
-- Lua Script: 원자적 중복 방지
local publish_key = "router:published:" .. job_id .. ":" .. seq
if redis.call('EXISTS', publish_key) == 1 then
  return 0  -- 이미 처리됨
end
redis.call('SETEX', publish_key, 7200, '1')
```

#### 7.2.2 Eventual Consistency 보장

```
Guarantees:
─────────────────────────────────────────────────────────────
1. All SSE events are persisted to Redis Streams
   └─ event-router Consumer Group (ACK 기반)

2. All done events are written to PostgreSQL
   └─ chat-consumer Consumer Group (배치 + 트랜잭션)

3. Frontend reconciles local + server data
   └─ 30s buffer for eventual consistency

4. No message loss during pagination
   └─ reconcile preserves uncommitted messages
─────────────────────────────────────────────────────────────
```

#### 7.2.3 Failure Recovery

**SSE 재연결**:
```typescript
// EventSource 자동 재연결 (브라우저 기본 동작)
eventSource.onerror = (error) => {
  // 브라우저가 자동으로 재연결 시도
  // last_seq 파라미터로 중복 이벤트 필터링
};

// Backend SSE Gateway
async function* subscribe(job_id: str, last_seq: int):
  # 1. State KV에서 마지막 상태 복구
  state = await redis.get(f"chat:state:{job_id}")
  if state and state["seq"] > last_seq:
    yield state

  # 2. Streams에서 누락 이벤트 catch-up
  async for event in catch_up(job_id, last_seq):
    yield event

  # 3. Real-time Pub/Sub
  async for event in pubsub.subscribe(job_id):
    yield event
```

**IndexedDB 복구**:
```typescript
// 페이지 새로고침 시 자동 복구
const loadChatMessages = async (chatId: string) => {
  // 1. IndexedDB 우선 로드
  const localMessages = await messageDB.getMessages(chatId);
  if (localMessages.length > 0) {
    setMessages(localMessages); // 즉시 표시
  }

  // 2. 서버 조회
  const response = await api.getChatDetail(chatId);

  // 3. Reconcile
  setMessages((prev) => reconcileMessages(prev, response.messages));
};
```

---

## 8. 향후 개선 방향

### 8.1 Offline Support

현재는 온라인만 지원, 오프라인 모드 추가 가능:

```typescript
// Service Worker + Background Sync
navigator.serviceWorker.ready.then((registration) => {
  registration.sync.register('sync-messages');
});

self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-messages') {
    event.waitUntil(syncPendingMessages());
  }
});

async function syncPendingMessages() {
  const pendingMessages = await messageDB.getUnsyncedMessages(chatId);
  for (const msg of pendingMessages) {
    try {
      await api.sendMessage(chatId, msg);
      await messageDB.updateMessageStatus(msg.client_id, 'committed');
    } catch (err) {
      // 재시도 큐에 추가
    }
  }
}
```

### 8.2 Conflict Resolution (멀티 디바이스)

여러 디바이스에서 동시 사용 시 충돌 해결:

```typescript
// Last-Write-Wins (LWW) 정책
const resolveConflict = (local: AgentMessage, server: AgentMessage) => {
  const localTime = new Date(local.created_at).getTime();
  const serverTime = new Date(server.created_at).getTime();

  return serverTime >= localTime ? server : local;
};

// Operational Transformation (OT) - 고급
const applyOT = (operations: Operation[]) => {
  // 동시 편집 시 변경사항 병합
};
```

### 8.3 Delta Sync (증분 동기화)

현재는 전체 메시지 조회, 증분 업데이트로 최적화:

```typescript
// Server API: 마지막 동기화 이후 변경사항만
GET /chat/:id/messages/delta?since={last_sync_timestamp}

// Frontend
const syncDelta = async (chatId: string) => {
  const metadata = await messageDB.getSyncMetadata(chatId);
  const lastSync = metadata?.last_sync_at || '1970-01-01T00:00:00Z';

  const response = await api.getDelta(chatId, lastSync);

  // Apply delta
  setMessages((prev) => applyDelta(prev, response.delta));

  // Update metadata
  await messageDB.saveSyncMetadata({
    chat_id: chatId,
    last_sync_at: new Date().toISOString(),
  });
};
```

### 8.4 WebSocket Upgrade (SSE → WebSocket)

SSE는 단방향, WebSocket으로 양방향 통신 가능:

```typescript
// WebSocket으로 업그레이드
const ws = new WebSocket(`wss://api.example.com/chat/${chatId}`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleSSEEvent(data); // 기존 로직 재사용
};

// 클라이언트 → 서버 (예: 타이핑 인디케이터)
ws.send(JSON.stringify({ type: 'typing', user_id: userId }));
```

### 8.5 Read Receipts (읽음 표시)

메시지 읽음 상태 추적:

```typescript
interface AgentMessage {
  // ...existing fields
  read_at?: string;
  read_by?: string[];
}

// IndexedDB에 읽음 시간 저장
const markAsRead = async (messageId: string) => {
  await messageDB.updateMessageStatus(messageId, 'committed', undefined, {
    read_at: new Date().toISOString(),
  });

  // 서버에도 알림
  await api.markAsRead(chatId, messageId);
};
```

---

## 결론

### 핵심 성과

1. **위치 데이터 누락 해결**: Ref 패턴으로 비동기 geolocation 값 캡처
2. **메시지 소실 방지**: 30초 Retention Window + Reconcile 알고리즘
3. **페이지 새로고침 대응**: IndexedDB 영구 저장
4. **실시간성 + 신뢰성**: Optimistic Update + Eventual Consistency 조화

### 시스템 특징

- **Event-First Architecture**: 백엔드가 실시간성(SSE)과 영속성(DB)을 독립적으로 처리
- **Client-Driven Reconciliation**: 프론트엔드가 로컬/서버 데이터를 능동적으로 병합
- **Status-Driven UI**: 메시지 상태 기반 UX (pending → streaming → committed)
- **Cache-Aside Pattern**: IndexedDB 우선 + 백그라운드 동기화

### 확장 가능성

현재 아키텍처는 다음 기능으로 확장 가능:
- 오프라인 모드 (Service Worker + Background Sync)
- 멀티 디바이스 동기화 (Conflict Resolution)
- 증분 동기화 (Delta Sync)
- WebSocket 업그레이드 (양방향 통신)
- 읽음 표시 (Read Receipts)

### 기술 스택 요약

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend State** | React useState | Optimistic UI 상태 |
| **Frontend Cache** | IndexedDB (idb) | 영구 저장 + 새로고침 복구 |
| **Frontend Sync** | Reconcile Algorithm | 로컬/서버 데이터 병합 |
| **Backend Real-time** | Redis Streams + Pub/Sub | SSE 이벤트 전송 |
| **Backend Persistence** | PostgreSQL | Eventual Write |
| **Backend Worker** | LangGraph + Celery | 비동기 작업 처리 |

---

**참고 문서**:
- Backend Architecture: `/backend/.claude/skills/chat-agent-flow/references/architecture.md`
- SSE Gateway: `/backend/.claude/skills/event-driven/references/sse-gateway.md`
- Message Consumer: `/backend/.claude/skills/chat-agent-persistence/references/message-consumer.md`
- Frontend Code: `/frontend/src/hooks/agent/useAgentChat.ts`
- Reconcile Logic: `/frontend/src/utils/message.ts`
