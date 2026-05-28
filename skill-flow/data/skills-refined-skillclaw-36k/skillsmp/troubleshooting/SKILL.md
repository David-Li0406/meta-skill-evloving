---
name: troubleshooting
description: Agent 기능 트러블슈팅 스킬. 빌드 에러, 이미지 업로드 실패, SSE 연결 문제 등 실전 문제 해결 가이드.
---

# Troubleshooting Skill

> Agent 기능 구현 중 발생하는 일반적인 문제와 해결 방법

## 1. 개요

Agent 기능 개발 중 발생 가능한 문제를 빠르게 진단하고 해결하는 가이드입니다.
각 문제는 증상 → 원인 → 해결 순서로 정리되어 있습니다.

## 2. 의사결정 트리

```
문제 발생
    │
    ├─ 빌드 에러?
    │   ├─ TypeScript 타입 에러 → references/build-errors.md §1
    │   ├─ ESLint 경고/에러 → references/build-errors.md §2
    │   └─ Vercel 배포 실패 → references/build-errors.md §3
    │
    ├─ 이미지 업로드 실패?
    │   ├─ 400 Bad Request → references/image-upload-fix.md §1
    │   ├─ 403 Forbidden → references/image-upload-fix.md §2
    │   └─ CORS 에러 → references/image-upload-fix.md §3
    │
    ├─ SSE 연결 문제?
    │   ├─ 타임아웃 발생 → §3.1
    │   ├─ 메시지 중복 수신 → §3.2
    │   └─ 연결 끊김 → §3.3
    │
    └─ IndexedDB 문제?
        ├─ Quota 초과 → §4.1
        ├─ 마이그레이션 실패 → §4.2
        └─ 데이터 유실 → §4.3
```

## 3. SSE 연결 문제

### 3.1 타임아웃 발생

**증상**:
```
[ERROR] 서버 응답 타임아웃
SSE connection timeout after 60s
```

**원인**:
- 긴 작업(vision, RAG) 중 이벤트 미수신
- Keepalive 이벤트 미처리

**해결**:
```typescript
// useAgentSSE.ts
es.addEventListener('keepalive', () => {
  resetEventTimeout();  // ✅ 타임아웃 리셋
});
```

### 3.2 메시지 중복 수신

**증상**:
- 동일한 토큰이 여러 번 표시됨
- UI에 메시지 2~3배 중복

**원인**:
- SSE 재연결 시 중복 필터링 누락
- Stream ID 기반 필터링 미구현

**해결**:
```typescript
// Backend: Stream ID 주입
event["stream_id"] = msg_id;  // Redis Stream ID

// Frontend: 중복 필터링 (이미 구현됨)
if (last_stream_id >= new_stream_id) return;  // Skip
```

### 3.3 연결 끊김

**증상**:
```
EventSource connection closed unexpectedly
```

**원인**:
- 네트워크 불안정
- 쿠키 인증 만료

**해결**:
```typescript
// 자동 재연결 (exponential backoff)
es.addEventListener('error', () => {
  if (reconnectAttempt < MAX_RETRIES) {
    const delay = 1000 * Math.pow(2, reconnectAttempt);
    setTimeout(() => createEventSource(jobId), delay);
  }
});
```

## 4. IndexedDB 문제

### 4.1 Quota 초과

**증상**:
```
QuotaExceededError: The quota has been exceeded
```

**원인**:
- 메시지가 너무 많이 쌓임 (cleanup 미실행)

**해결**:
```typescript
// 주기적 cleanup (1분마다)
setInterval(() => {
  messageDB.cleanup(userId, sessionId, {
    committedRetentionMs: 30000,  // 30초
    ttlMs: 7 * 24 * 60 * 60 * 1000,  // 7일
  });
}, 60000);
```

### 4.2 마이그레이션 실패

**증상**:
```
[MessageDB] Upgrade blocked - close other tabs
```

**원인**:
- 다른 탭에서 DB 사용 중

**해결**:
1. 모든 탭 닫기
2. 브라우저 재시작
3. IndexedDB 수동 삭제:
   ```javascript
   // DevTools Console
   indexedDB.deleteDatabase('agent-chat-db');
   ```

### 4.3 데이터 유실

**증상**:
- 새로고침 후 메시지 사라짐

**원인**:
- `saveMessages` 호출 누락
- `beforeunload` 핸들러 미실행

**해결**:
```typescript
// useMessagePersistence.ts
// 1. Pending 메시지 즉시 저장
useEffect(() => {
  const pending = messages.filter(m => m.status === 'pending');
  if (pending.length > 0) {
    messageDB.saveMessages(userId, sessionId, pending);
  }
}, [messages]);

// 2. beforeunload 핸들러
useEffect(() => {
  const handler = () => {
    messageDB.saveMessages(userId, sessionId, messages);
  };
  window.addEventListener('beforeunload', handler);
  return () => window.removeEventListener('beforeunload', handler);
}, []);
```

## 5. 일반적인 패턴

### 5.1 에러 로깅

**권장 패턴**:
```typescript
try {
  await riskyOperation();
} catch (err) {
  console.error('[Context] Operation failed:', {
    error: err,
    context: { userId, sessionId },
    timestamp: Date.now(),
  });

  // User-friendly 에러 메시지
  setError(err instanceof Error ? err : new Error('Unknown error'));
}
```

### 5.2 Race Condition 방지

**문제**:
```typescript
// ❌ 중복 전송 가능
const sendMessage = async (msg) => {
  await api.post('/messages', msg);
};
```

**해결**:
```typescript
// ✅ Flag로 방지
const isSendingRef = useRef(false);

const sendMessage = async (msg) => {
  if (isSendingRef.current) return;
  isSendingRef.current = true;

  try {
    await api.post('/messages', msg);
  } finally {
    isSendingRef.current = false;
  }
};
```

### 5.3 Memory Leak 방지

**문제**:
```typescript
// ❌ Cleanup 누락
useEffect(() => {
  const es = new EventSource(url);
  es.addEventListener('message', handler);
}, []);
```

**해결**:
```typescript
// ✅ Cleanup 함수
useEffect(() => {
  const es = new EventSource(url);
  es.addEventListener('message', handler);

  return () => {
    es.close();  // ✅ 명시적 cleanup
  };
}, []);
```

## 6. 참조 문서

| 파일 | 내용 |
|------|------|
| `references/image-upload-fix.md` | 이미지 업로드 400 에러 진단 및 해결 |
| `references/build-errors.md` | TypeScript/ESLint/Vercel 빌드 에러 |

## 7. 디버깅 팁

### 7.1 SSE 디버깅

```typescript
// 모든 이벤트 로깅
es.onmessage = (e) => {
  console.log('[SSE]', e.type, JSON.parse(e.data));
};

// Network 탭에서 확인
// - EventStream 탭에서 실시간 이벤트 보기
// - Headers에서 쿠키 확인
```

### 7.2 IndexedDB 디버깅

```javascript
// DevTools > Application > IndexedDB
// - agent-chat-db > messages 테이블 확인
// - user_id, session_id 필터링

// 프로그래밍 방식 조회
const stats = await messageDB.getStats();
console.log(stats);
// { totalMessages: 42, unsyncedMessages: 3, ... }
```

### 7.3 React DevTools

```typescript
// useAgentChat 상태 확인
// - messages (pending/committed 구분)
// - isStreaming
// - currentChat

// 컴포넌트 리렌더링 추적
// Profiler > Record > 느린 렌더링 찾기
```

## 8. 긴급 복구

### 8.1 전체 캐시 삭제

```javascript
// DevTools Console
await messageDB.clear();
localStorage.clear();
sessionStorage.clear();
location.reload();
```

### 8.2 특정 채팅 삭제

```javascript
await messageDB.deleteChat(sessionId);
```

### 8.3 서버 동기화 강제

```typescript
// 로컬 데이터 버리고 서버에서 재로드
await messageDB.clear();
const serverMessages = await getChatDetail(sessionId);
setMessages(serverMessages);
```

## 9. 체크리스트

문제 발생 시:

```
[ ] 1. 에러 메시지 전문 복사
[ ] 2. Console/Network 탭 캡처
[ ] 3. 재현 시나리오 정리
[ ] 4. IndexedDB 상태 확인
[ ] 5. SSE 연결 상태 확인
[ ] 6. 관련 references 문서 참조
[ ] 7. 임시 해결 후 근본 원인 분석
```

## 10. 추가 리소스

- Backend Event Router 리포트: `/Users/mango/workspace/SeSACTHON/backend-event-router-improvement/docs/reports/`
- Agent Feature Skill: `../agent-feature/SKILL.md`
- Data Integrity Skill: `../data-integrity/SKILL.md`
