---
name: coding-standards
description: >
  Sessionary 프로젝트의 코딩 표준과 개발 가이드를 제공하는 skill.
  사용자가 (1) 코드를 작성하거나 수정할 때, (2) 테스트를 작성할 때,
  (3) 프론트엔드/백엔드 개발 패턴을 물을 때, (4) TDD 개발을 진행할 때 사용.
  file types,or tasks that trigger it.
---

# Coding Standards

Sessionary 프로젝트 코딩 표준 및 개발 가이드

## 플랫폼 판별

작업 대상에 따라 적절한 가이드 로드:

| 대상 | 경로 패턴 | 참조 문서 |
|------|----------|----------|
| Frontend | `frontend/**` | `references/frontend.md` |
| Backend | `backend/**` | `references/backend.md` |

## 공통 규칙

### 코드 스타일

- 주석 대신 명확한 함수/변수명 사용
- private method로 실행 순서가 드러나게 리팩터링
- 과도한 추상화 금지

### 테스트 원칙

- Edge case 위주 테스트
- Approval case 최소 1개 포함
- 테스트 데이터는 fixture로 격리

## Frontend (Svelte 5)

**상세 가이드**: `references/frontend.md` 참조

### 핵심 패턴

```svelte
<script lang="ts">
  // Svelte 5 Runes 문법 사용
  let { data }: { data: SomeType } = $props()
  let count = $state(0)
  let doubled = $derived(count * 2)
</script>
```

### 테스트 실행

```bash
cd frontend
yarn test:integration  # Playwright E2E
yarn test:unit         # Vitest Unit
```

## Backend (FastAPI)

**상세 가이드**: `references/backend.md` 참조

### 핵심 패턴

```text
View (Router) → Service → Repository → DB
```

- Abstract Base Class로 인터페이스 정의
- dependency-injector로 DI 처리

### 테스트 실행

```bash
cd backend
uv run pytest
```

## TDD 워크플로우

1. **RED**: 실패하는 테스트 작성
2. **GREEN**: 테스트 통과하는 최소 코드
3. **REFACTOR**: 코드 정리

각 사이클 완료 후 커밋 (100줄 이하)
