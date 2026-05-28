# Build Errors 트러블슈팅

**출처**: Code Quality Verification Report
**작성일**: 2026-01-23

---

## 1. TypeScript 컴파일 에러

### 1.1 타입 불일치 (Argument Type)

**에러**:
```typescript
src/db/messageDB.ts(361,65): error TS2345: Argument of type '"by-chat"' is not assignable to parameter of type '"by-user" | "by-user-session" | ...'.
```

**원인**: v3 스키마로 업그레이드하면서 `by-chat` 인덱스 제거됨

**해결**:
```typescript
// Before
const messages = await this.db!.getAllFromIndex('messages', 'by-chat', chatId);

// After
const messages = await this.db!.getAllFromIndex('messages', 'by-session', sessionId);
```

### 1.2 Property Does Not Exist

**에러**:
```typescript
src/db/messageDB.ts(65,45): error TS2339: Property 'objectStore' does not exist on type '...'.
```

**원인**: `db.transaction`은 함수이지 객체가 아님

**해결**:
```typescript
// Before
upgrade(db, oldVersion) {
  const msgStore = db.transaction.objectStore('messages');
}

// After
upgrade(db, oldVersion, _newVersion, transaction) {
  const msgStore = transaction.objectStore('messages');
}
```

### 1.3 레거시 인덱스 타입 에러

**에러**:
```typescript
src/db/messageDB.ts(47,34): error TS2345: Argument of type '"by-chat"' is not assignable to parameter of type ...
```

**원인**: v1, v2 마이그레이션에서 생성하는 인덱스가 v3 타입 정의에 없음

**해결**: `as any` 캐스팅으로 레거시 마이그레이션 허용

```typescript
// v1 마이그레이션 (레거시)
if (oldVersion < 1) {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (msgStore as any).createIndex('by-chat', 'chat_id', { unique: false });
}
```

**이유**: v3에서는 사용하지 않지만, 기존 DB에서 업그레이드 시 필요

### 1.4 미사용 파라미터

**에러**:
```typescript
src/db/messageDB.ts(38,33): error TS6133: 'newVersion' is declared but its value is never read.
```

**해결**:
```typescript
// Before
upgrade(db, oldVersion, newVersion, transaction) {

// After
upgrade(db, oldVersion, _newVersion, transaction) {
  // _ prefix로 의도적 미사용 표시
}
```

---

## 2. ESLint 에러

### 2.1 no-this-alias

**에러**:
```
src/db/messageDB.ts:31:13  error  Unexpected aliasing of 'this' to local variable  @typescript-eslint/no-this-alias
```

**원인**: `const self = this` 패턴 사용

**잘못된 코드**:
```typescript
this.initPromise = (async () => {
  const self = this;

  this.db = await openDB({
    blocking() {
      self.db?.close();  // function() 내부에서 this 접근 불가
    }
  });
})();
```

**해결**: 화살표 함수로 전환

```typescript
this.initPromise = (async () => {
  this.db = await openDB({
    blocking: () => {
      this.db?.close();  // ✅ 화살표 함수로 this 보존
    },
  });
})();
```

### 2.2 no-unused-vars

**에러**:
```
src/hooks/agent/useAgentSSE.ts(261,39): error TS6133: 'e' is declared but its value is never read.
```

**해결**:
```typescript
// Before
es.addEventListener('keepalive', (e) => {
  resetEventTimeout();
});

// After
es.addEventListener('keepalive', () => {
  resetEventTimeout();
});
```

---

## 3. Vercel 배포 실패

### 3.1 빌드 실패 증상

**Vercel Checks**:
```
Vercel – eco2         fail    Deployment has failed
Vercel – frontend     fail    Deployment has failed
```

**원인**: TypeScript 컴파일 에러

### 3.2 로컬 검증

**빌드 테스트**:
```bash
npm run build

# 에러 확인
# ✓ 0 errors → Vercel 성공
# ✗ N errors → Vercel 실패
```

**ESLint 검증**:
```bash
npx eslint src/**/*.ts

# 목표: 0 errors, 0 warnings
```

**Prettier 검증**:
```bash
npx prettier --check src/**/*.ts

# 자동 수정
npx prettier --write src/**/*.ts
```

### 3.3 Vercel 재배포

**자동 트리거**:
- PR 브랜치에 push → 자동 재배포
- 수정 후 commit & push 시 Vercel이 다시 빌드

**수동 트리거**:
```bash
# Vercel CLI 사용
vercel --prod
```

---

## 4. 일반적인 패턴

### 4.1 Migration 타입 안전성

**패턴**: 레거시 인덱스는 `as any`로 우회

```typescript
// 현재 타입에 없는 필드 생성 시
if (oldVersion < 2) {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (msgStore as any).createIndex('legacy-index', 'old_field', { unique: false });
}
```

### 4.2 함수 파라미터 미사용

**패턴**: `_` prefix로 의도 표시

```typescript
// OpenDB upgrade 콜백
upgrade(db, oldVersion, _newVersion, transaction) {
  // newVersion은 DB_VERSION 상수로 대체
  console.log(`Upgrading from ${oldVersion} to ${DB_VERSION}`);
}
```

### 4.3 이벤트 핸들러 this 바인딩

**패턴**: 항상 화살표 함수 사용

```typescript
// ❌ function() 사용 금지
{
  blocking() {
    this.db?.close();  // this가 undefined
  }
}

// ✅ 화살표 함수
{
  blocking: () => {
    this.db?.close();  // ✅ this 보존
  }
}
```

---

## 5. 빌드 체크리스트

배포 전 확인:

```bash
# 1. TypeScript 컴파일
npm run build
# 예상: ✓ built in Xs

# 2. ESLint
npx eslint src/**/*.ts
# 예상: ✓ No issues found

# 3. Prettier
npx prettier --check src/**/*.ts
# 예상: All files formatted correctly

# 4. Git 상태
git status
# 예상: nothing to commit, working tree clean
```

---

## 6. 긴급 해결

### Vercel 빌드 급하게 통과시키기

**임시 우회** (권장하지 않음):
```json
// tsconfig.json
{
  "compilerOptions": {
    "skipLibCheck": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false
  }
}
```

**근본 해결** (권장):
- 위 섹션 1~2의 에러별 해결 방법 적용
- 로컬에서 `npm run build` 성공 확인
- Commit & Push

---

## 7. 참조

- TypeScript Handbook: https://www.typescriptlang.org/docs/
- ESLint Rules: https://typescript-eslint.io/rules/
- Vercel Build Logs: PR의 Checks → Vercel → View logs
