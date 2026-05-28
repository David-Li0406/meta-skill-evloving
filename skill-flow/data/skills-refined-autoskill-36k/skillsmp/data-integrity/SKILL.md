---
name: data-integrity
description: Agent 채팅 데이터 무결성 관리 스킬. IndexedDB v3 스키마, Optimistic Updates, Eventual Consistency 패턴 구현 시 사용.
---

# Data Integrity Management Skill

> Agent 채팅의 데이터 무결성과 일관성을 보장하는 아키텍처 패턴 가이드

## 1. 개요

Agent 채팅은 다층 데이터 아키텍처로 실시간 UX와 데이터 안정성을 모두 확보합니다:
- **Optimistic Updates**: 즉각적인 UI 반응
- **IndexedDB**: 새로고침 대비 로컬 캐시
- **Eventual Consistency**: 서버와의 점진적 동기화

## 2. 아키텍처 계층

```
┌─────────────────────────────────────────────────────────────┐
│                   Frontend Data Layers                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: React State (메모리)                              │
│  ├─ 목적: 실시간 UI 렌더링                                   │
│  ├─ 생명주기: 컴포넌트 마운트 ~ 언마운트                      │
│  └─ 소실 조건: 새로고침, 탭 닫기                             │
│                                                             │
│  Layer 2: IndexedDB (브라우저)                               │
│  ├─ 목적: 새로고침 대비, 오프라인 캐시                        │
│  ├─ 생명주기: 브라우저 저장소 유지                            │
│  ├─ 격리: user_id + session_id                             │
│  └─ 정리: 30초 retention (committed) + 7일 TTL              │
│                                                             │
│  Layer 3: Backend DB (PostgreSQL)                           │
│  ├─ 목적: 영구 저장, Source of Truth                        │
│  ├─ 계층: users → conversations → messages                  │
│  └─ 정렬: created_at (timestamp)                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 3. 핵심 개념

### 3.1 Optimistic Updates

**사용 시기**: 메시지 전송 즉시

```typescript
// 1. User 메시지 즉시 표시 (pending 상태)
const userMessage = createUserMessage(content);
userMessage.status = 'pending';
setMessages(prev => [...prev, userMessage]);

// 2. 서버 전송
const response = await sendMessage(chatId, { message: content });

// 3. SSE 완료 시 committed로 업데이트
onSSEComplete((result) => {
  updateMessageStatus(userMessage.client_id, 'committed', result.server_id);
});
```

**메시지 상태 전이**:
```
pending → committed  (성공)
pending → failed     (실패)
```

### 3.2 IndexedDB v3 스키마

**계층 구조**: Backend와 정확히 일치

```typescript
// Backend
users_accounts.id → chat_conversations.id → chat_messages.id

// Frontend IndexedDB
user_id → session_id → client_id + created_at
```

**주요 인덱스**:
- `by-user-session-created`: [user_id, session_id, created_at]
- `by-synced`: 동기화 여부 (0/1)

### 3.3 Eventual Consistency

**30초 Retention Window**: 서버 committed 메시지를 30초간 IndexedDB에 유지

```typescript
// Reconcile 로직
const merged = reconcileMessages(localMessages, serverMessages, {
  committedRetentionMs: 30000,
});

// 정책
// - pending 메시지: 항상 유지 (재시도 가능)
// - committed 메시지: 30초 후 삭제 (서버가 Source of Truth)
```

## 4. 의사결정 트리

```
데이터 무결성 구현 시작
    │
    ├─ IndexedDB 스키마 설계?
    │   └─ references/indexeddb-schema.md 참조
    │
    ├─ 메시지 순서 보장?
    │   └─ references/message-ordering.md 참조
    │
    ├─ Optimistic Updates 구현?
    │   └─ references/optimistic-updates.md 참조
    │
    └─ Reconcile 정책 설정?
        └─ references/optimistic-updates.md §4 참조
```

## 5. 핵심 구현 패턴

### 5.1 IndexedDB 초기화

```typescript
// db/messageDB.ts
const messageDB = new MessageDB();
await messageDB.init();

// v1 → v2 → v3 자동 마이그레이션
// 레거시 인덱스 정리 + 신규 인덱스 생성
```

### 5.2 메시지 저장 (User Isolation)

```typescript
await messageDB.saveMessages(
  userId,      // users_accounts.id
  sessionId,   // chat_conversations.id
  messages,    // AgentMessage[]
);
```

### 5.3 Reconcile (서버 병합)

```typescript
// 1. IndexedDB에서 로드 (즉시 표시)
const localMessages = await messageDB.getMessages(userId, sessionId);
setMessages(localMessages);

// 2. 서버 조회 (백그라운드)
const serverMessages = await getChatDetail(sessionId);

// 3. Reconcile (로컬 pending + 서버 committed)
const merged = reconcileMessages(localMessages, serverMessages, {
  committedRetentionMs: 30000,
});
setMessages(merged);
```

## 6. 주의사항

### 6.1 메시지 순서 보장

❌ **Redis Stream ID 사용 금지**
- Redis Stream ID는 SSE 중복 필터링 전용
- 메시지 순서는 `created_at` 필드 사용

✅ **created_at 기반 정렬**
```typescript
const messages = await db.getAllFromIndex(
  'messages',
  'by-user-session-created',
  IDBKeyRange.bound([userId, sessionId, ''], [userId, sessionId, '\uffff'])
);
```

### 6.2 Session ID 명명

**일관성 유지**:
- Backend: `chat_id`, `conversation_id` (동일한 값)
- Frontend: `session_id` (명확한 계층 표현)
- 값은 동일, 명명만 다름

### 6.3 Cleanup 정책

```typescript
// 30초 retention (committed + synced)
await messageDB.cleanup(userId, sessionId, {
  committedRetentionMs: 30000,
});

// 7일 TTL (모든 메시지)
await messageDB.cleanup(userId, sessionId, {
  ttlMs: 7 * 24 * 60 * 60 * 1000,
});
```

## 7. 참조 문서

| 파일 | 내용 |
|------|------|
| `references/indexeddb-schema.md` | v3 스키마 상세, 마이그레이션, ID 계층 구조 |
| `references/message-ordering.md` | created_at vs stream_id, 순서 보장 검증 |
| `references/optimistic-updates.md` | 상태 전이, Reconcile 로직, Retention 정책 |

## 8. 체크리스트

구현 시 아래 순서대로 진행:

```
[ ] 1. IndexedDB v3 스키마 구현 (user_id + session_id)
[ ] 2. Optimistic Update 패턴 (pending → committed)
[ ] 3. SSE 완료 시 상태 업데이트 로직
[ ] 4. IndexedDB 자동 저장 (throttled, 500ms)
[ ] 5. Reconcile 로직 (로컬 + 서버 병합)
[ ] 6. Cleanup 정책 (30초 retention + 7일 TTL)
[ ] 7. User isolation 검증 (multi-user 시나리오)
[ ] 8. 메시지 순서 검증 (created_at 기반)
```

## 9. 트러블슈팅

문제 발생 시 `../troubleshooting/SKILL.md` 참조:
- 메시지 중복 수신
- 순서 뒤바뀜
- IndexedDB quota 초과
- 마이그레이션 실패

## 10. 테스트 시나리오

### 기본 흐름
1. 메시지 전송 → pending 상태 즉시 표시
2. SSE 완료 → committed로 업데이트
3. 새로고침 → IndexedDB에서 복구
4. 서버 조회 → Reconcile로 병합
5. 30초 경과 → committed 메시지 cleanup

### Edge Cases
- 네트워크 실패 → failed 상태로 전환
- 늦은 구독 → token_recovery로 복구
- Multi-tab → IndexedDB blocking 핸들러
- Quota 초과 → cleanup 트리거
