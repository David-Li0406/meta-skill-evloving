---
name: supabase
description: |
  Supabase 관련 컨벤션 및 코드 생성 지원. Use when (1) "Supabase 테이블 생성",
  (2) "RLS 정책 추가", (3) "마이그레이션 작성", (4) "Edge Function 생성",
  (5) Supabase 관련 코드 리뷰/생성.
tools: [Read, Write, Bash]
model: inherit
---

> **시스템 메시지**: `[SEMO] Skill: supabase 호출`

# supabase Skill

> Semicolon Supabase 컨벤션 기반 코드 생성 및 검증

## Trigger Keywords

- "Supabase 테이블 생성", "테이블 만들어줘"
- "RLS 정책 추가", "RLS 설정"
- "마이그레이션 작성", "migration 생성"
- "Edge Function 만들어줘"
- "Supabase 코드 리뷰"

## 반드시 참조할 파일

### 컨벤션

- **CONVENTIONS.md**: 전체 컨벤션 요약
- **references/rls-patterns.md**: RLS 정책 패턴
- **references/migration-guide.md**: 마이그레이션 가이드
- **references/edge-functions.md**: Edge Functions 가이드

## Workflow

### 1. 테이블 생성 요청

```
입력: "purchases 테이블 만들어줘"

1. CONVENTIONS.md에서 테이블 네이밍 규칙 확인
2. migration-guide.md에서 템플릿 참조
3. 마이그레이션 파일 생성
4. RLS 정책 자동 추가 제안
```

### 2. RLS 정책 추가 요청

```
입력: "purchases 테이블에 소유자만 접근하도록 RLS 설정해줘"

1. rls-patterns.md에서 적절한 패턴 선택
2. 정책 이름 컨벤션 적용
3. SQL 생성
```

### 3. Edge Function 생성 요청

```
입력: "purchase-item Edge Function 만들어줘"

1. edge-functions.md에서 템플릿 참조
2. _shared 유틸리티 import
3. 함수 구조 생성
```

## 출력 포맷

```
[SEMO] supabase: 요청 분석 완료
  - 타입: 테이블 생성
  - 대상: purchases

[SEMO] supabase: 컨벤션 적용
  - 테이블명: purchases (복수형, snake_case ✓)
  - 마이그레이션: 20251216_create_purchases_table.sql

[SEMO] supabase: 코드 생성 완료
  → supabase/migrations/20251216_create_purchases_table.sql

RLS 정책도 추가할까요? (소유자 기반 접근 권장)
```

## 검증 체크리스트

### 테이블

- [ ] snake_case 사용
- [ ] 복수형 사용
- [ ] Primary Key는 uuid
- [ ] created_at, updated_at 포함
- [ ] RLS 활성화

### RLS 정책

- [ ] 정책명 컨벤션 준수
- [ ] 적절한 auth.uid() 사용
- [ ] 인덱스 추가 여부 확인

### Edge Function

- [ ] kebab-case 디렉토리명
- [ ] CORS 처리 포함
- [ ] 에러 핸들링 포함
- [ ] 타입 정의 사용

## References

- [CONVENTIONS.md](./CONVENTIONS.md)
- [RLS Patterns](./references/rls-patterns.md)
- [Migration Guide](./references/migration-guide.md)
- [Edge Functions](./references/edge-functions.md)
