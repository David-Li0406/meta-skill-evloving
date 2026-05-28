---
name: pr-reviewer
description: 코드 리뷰 체크리스트를 적용하는 PR 검토 스킬
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# PR Reviewer Skill

이 스킬은 ForkLore 프로젝트의 Pull Request를 체계적으로 검토합니다.

## 리뷰 프로세스

### 1. 변경 범위 파악

```bash
# PR diff 확인
gh pr diff {PR_NUMBER}

# 변경된 파일 목록
gh pr diff {PR_NUMBER} --name-only
```

### 2. 코드 품질 체크리스트

#### Backend (Python/Django)

- [ ] **타입 힌트**: 모든 함수에 타입 힌트가 있는가?
- [ ] **Docstring**: Google 스타일 docstring이 있는가?
- [ ] **서비스 패턴**: 비즈니스 로직이 서비스 레이어에 있는가? (뷰에 있으면 ❌)
- [ ] **에러 메시지**: 사용자 대상 에러 메시지가 한국어인가?
- [ ] **트랜잭션**: 복합 작업에 `@transaction.atomic` 사용했는가?
- [ ] **테스트**: 새 기능/버그 수정에 테스트가 있는가?
- [ ] **커버리지**: 95% 이상 유지되는가?

#### Frontend (TypeScript/React)

- [ ] **타입 안전성**: `any`, `@ts-ignore`, `@ts-expect-error` 사용 금지
- [ ] **Named Export**: default export 대신 named export 사용
- [ ] **컴포넌트 구조**: Server/Client 컴포넌트 적절히 분리
- [ ] **테스트**: 컴포넌트 테스트가 있는가?

### 3. 보안 체크

- [ ] 비밀키/자격증명이 하드코딩되지 않았는가?
- [ ] 사용자 입력이 적절히 검증되는가?
- [ ] SQL 인젝션 위험이 없는가?
- [ ] XSS 위험이 없는가?

### 4. 성능 체크

- [ ] N+1 쿼리 문제가 없는가?
- [ ] 불필요한 데이터베이스 호출이 없는가?
- [ ] 적절한 인덱스가 사용되는가?

### 5. API 규칙 체크 (해당시)

- [ ] 뷰가 RAW 데이터만 반환하는가? (StandardJSONRenderer가 래핑함)
- [ ] DRF 예외 사용하는가? (NotFound, PermissionDenied, ValidationError)
- [ ] 중복 래핑 없는가? (`{"success": True, "data": ...}` 금지)

## 리뷰 결과 템플릿

```markdown
## 리뷰 결과

### ✅ 통과 항목
- 항목 1
- 항목 2

### ⚠️ 개선 권장
- 항목 1: 이유

### ❌ 수정 필요
- 항목 1: 이유
```
