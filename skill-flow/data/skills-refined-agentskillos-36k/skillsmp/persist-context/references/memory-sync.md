# Memory Sync 워크플로우

> 세션 시작 시 메모리 동기화 프로세스

## 트리거

- 새 세션 시작 시 `skill:version-updater` Phase 4에서 자동 호출
- 수동 호출: `skill:memory sync`

## 동기화 흐름

```text
[세션 시작]
     ↓
[.claude/memory/ 존재 확인]
     ↓
     ├─ 없음 → 스킵 (메모리 없음)
     │
     └─ 있음 → 동기화 시작
              ↓
         [decisions.json 로드]
              ↓
         [preferences.json 로드]
              ↓
         [context/{project}.json 로드]
              ↓
         [세션 컨텍스트에 주입]
              ↓
         [동기화 완료 리포트]
```

## 컨텍스트 주입

로드된 메모리는 현재 세션의 동작에 영향을 미칩니다:

### decisions (결정 사항)

```text
저장된 결정: "API 응답은 JSON Envelope 패턴 사용"
     ↓
API 구현 시 자동으로 해당 패턴 적용
```

### preferences (선호도)

```text
저장된 선호도: "변수명은 camelCase"
     ↓
코드 생성 시 자동으로 camelCase 적용
```

### context (프로젝트 맥락)

```text
저장된 맥락: "Next.js 14 + Supabase"
     ↓
관련 기술 스택 기반으로 코드 생성
```

## MCP 연동 시 동작

Memory MCP가 활성화된 경우:

```text
[세션 시작]
     ↓
[MCP 서버 확인]
     ├─ MCP 활성화 → MCP에서 메모리 로드
     └─ MCP 비활성화 → 파일에서 메모리 로드
```

## 출력 예시

```markdown
[SEMO] Skill: memory 호출 - sync

=== 세션 메모리 복원 ===

✅ 결정 사항 3건 로드
  - api-envelope: JSON Envelope 패턴 사용
  - error-handling: Result 타입 사용
  - auth-method: JWT 인증

✅ 선호도 2건 로드
  - naming-convention: camelCase
  - language: ko

✅ 프로젝트 맥락 로드 (cm-office)
  - Framework: Next.js 14
  - Database: Supabase

세션 컨텍스트에 적용 완료
```

## 오류 처리

| 상황 | 동작 |
|------|------|
| 파일 손상 | 경고 출력 후 스킵 |
| 스키마 버전 불일치 | 마이그레이션 시도 |
| MCP 연결 실패 | 파일 기반으로 폴백 |
