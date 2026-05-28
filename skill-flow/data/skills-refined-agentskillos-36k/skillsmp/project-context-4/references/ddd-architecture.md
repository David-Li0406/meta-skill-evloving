# DDD Architecture

## 디렉토리 구조

```text
src/
├── app/
│   ├── {domain}/                 # 도메인별 디렉토리
│   │   ├── _repositories/        # 서버사이드 데이터 접근 ⭐
│   │   ├── _api-clients/         # 브라우저 HTTP 통신 ⭐
│   │   ├── _hooks/               # React 상태 관리 ⭐
│   │   ├── _components/          # 도메인 전용 UI ⭐
│   │   └── page.tsx              # 페이지 라우트
│   └── ...
├── repositories/                  # 공통 인프라
├── lib/api-clients/               # 공통 인프라
├── hooks/                         # 전역 Hooks
├── components/                    # Atomic Design (도메인 독립적)
│   ├── atoms/
│   ├── molecules/
│   ├── organisms/
│   └── templates/
├── models/                        # 전역 타입
└── lib/
    ├── supabase/
    └── utils/
```

## 핵심 원칙

1. **도메인 응집도**: 관련 코드가 `/app/{domain}/` 하위에 모임
2. **명확한 경계**: 각 도메인의 책임과 범위가 명확히 구분
3. **core-backend 정렬**: Spring Boot core-backend 구조와 동일한 패턴
4. **공통 인프라 분리**: 여러 도메인에서 공유하는 요소는 외부 계층에 위치

## Layer Responsibilities

| Layer | 역할 | 위치 | 핵심 규칙 |
|-------|------|------|----------|
| **Repository** | 서버사이드 데이터 접근 | `_repositories/` | `createServerSupabaseClient` 필수, `'use client'` 금지 |
| **API Client** | 브라우저 HTTP 통신 | `_api-clients/` | Factory Pattern + Singleton 필수 |
| **Hooks** | React 상태 관리 | `_hooks/` | React Query 사용, API Client 호출 |
| **Components** | 도메인 전용 UI | `_components/` | Hooks 사용, 비즈니스 로직 금지 |

## Data Flow (1-Hop Rule)

```text
Browser → API Client → [Spring Boot | Next.js API] → Repository → Supabase
                       ↓
                     Hooks → Components
```

**❌ 금지**: `Browser → Next.js → Spring Boot` (2-hop)
**✅ 권장**: `Browser → Spring Boot` (1-hop, 프로덕션)

## SSR-First Guidelines

1. **Server Components 기본** - `'use client'` 최소화
2. **Client는 interactive만** - 이벤트 핸들러, useState 필요 시만
3. **Server Actions 우선** - forms/mutations에 사용

### `'use client'` 추가 전 체크리스트

| 질문 | 답변 | 결론 |
|------|------|------|
| 이벤트 핸들러 필요? | 아니오 | Server Action 고려 |
| useState/useEffect 사용? | 예 | Client 필요 |
| 브라우저 API 접근? | 예 | Client 필수 |
| 순수 프레젠테이션? | 예 | Server 유지 |

## Violations to Avoid

| ❌ 금지 | ✅ 올바른 방법 |
|---------|---------------|
| `client/`, `server/` 디렉토리 생성 | Atomic Design 계층 사용 |
| UI 컴포넌트에서 auth/API 직접 import | Container Pattern 사용 |
| Molecules에 복잡한 컴포넌트 | Organisms에 배치 |
| Atoms에 비즈니스 로직 | 순수 프레젠테이션만 |
