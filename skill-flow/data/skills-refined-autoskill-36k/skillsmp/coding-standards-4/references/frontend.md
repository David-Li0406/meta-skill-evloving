# Frontend 개발 가이드

Svelte 5 + SvelteKit + TailwindCSS 기반 프론트엔드 개발 가이드

## 기술 스택

- **Framework**: Svelte 5 (Runes 문법)
- **Router**: SvelteKit
- **Styling**: TailwindCSS + flowbite-svelte
- **API Client**: openapi-ts 자동 생성
- **Test**: Playwright (E2E) + Vitest (Unit)

## 디렉토리 구조

```text
frontend/src/
├── routes/              # SvelteKit 라우트
│   ├── +layout.svelte   # 전역 레이아웃
│   └── [feature]/       # 기능별 페이지
├── lib/
│   ├── api/             # API 클라이언트 (자동 생성)
│   ├── components/      # 공통 컴포넌트
│   │   └── layout/      # 레이아웃 컴포넌트
│   ├── features/        # 기능별 모듈
│   │   └── [feature]/
│   │       ├── components/
│   │       ├── stores/
│   │       └── utils/
│   ├── styles/          # 디자인 토큰
│   └── utils/           # 공통 유틸리티
└── tests/
    ├── routes/          # E2E 테스트 (Playwright)
    ├── features/        # 기능별 E2E 테스트
    └── unit/            # Unit 테스트 (Vitest)
```

## Svelte 5 Runes 문법

### 상태 관리

```svelte
<script lang="ts">
  // $state: 반응형 상태
  let count = $state(0)

  // $derived: 파생 상태
  let doubled = $derived(count * 2)

  // $props: 컴포넌트 Props
  let { data, children }: { data: SomeType; children: Snippet } = $props()
</script>
```

### 스토어 패턴 (.svelte.ts)

```typescript
// stores/auth.svelte.ts
let isAuthenticated = $state(false)

export function setIsAuthenticated(value: boolean) {
  isAuthenticated = value
}

export function useAuth() {
  return {
    get isAuthenticated() {
      return isAuthenticated
    }
  }
}
```

## 컴포넌트 작성 규칙

### Props 타입 정의

```svelte
<script lang="ts">
  import type { LectureInList } from '$lib/api/client'

  let { lecture }: { lecture: LectureInList } = $props()
</script>
```

### 스타일링 (TailwindCSS + clamp)

반응형 디자인에 `clamp()` 사용:

```svelte
<div class="w-[clamp(15rem,26vw,26.25rem)]">
  <h5 class="text-[clamp(0.75rem,1.1vw,1.1rem)] font-bold">
    {title}
  </h5>
</div>
```

### flowbite-svelte 컴포넌트

```svelte
<script lang="ts">
  import { Button, Modal } from 'flowbite-svelte'
</script>
```

## API 클라이언트

### 자동 생성

```bash
yarn generate-client
```

### 사용법

```typescript
import { initializeApi, lecturesGetLectures } from '$lib/api'

// 초기화 (layout에서 1회)
initializeApi(baseUrl)

// API 호출
const lectures = await lecturesGetLectures({ page: 1, per_page: 20 })
```

## 테스트

### E2E 테스트 (Playwright)

```bash
yarn test:integration
```

```typescript
// tests/routes/home.test.ts
import { expect, test } from '@playwright/test'

test.describe('홈 페이지', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/home')
  })

  test('네비게이션 바를 표시합니다', async ({ page }) => {
    const navbar = page.locator('[data-testid="navbar"]')
    await expect(navbar).toBeVisible()
  })
})
```

### Unit 테스트 (Vitest)

```bash
yarn test:unit
```

```typescript
// tests/unit/features/auth/LoginModal.test.ts
import { describe, it, expect, vi } from 'vitest'

describe('LoginModal', () => {
  it('기본 message는 "로그인이 필요합니다"이다', async () => {
    const { getDefaultMessage } = await import('$lib/features/auth/components/LoginModal.svelte')
    expect(getDefaultMessage()).toBe('로그인이 필요합니다')
  })
})
```

### 테스트 작성 원칙

1. **E2E (Playwright)**: 사용자 시나리오 기반
   - `data-testid` 속성 사용
   - 한글 테스트명 권장

2. **Unit (Vitest)**: 순수 로직/유틸리티
   - 모듈 export 함수 테스트
   - Mock 최소화

## 커맨드

| 명령어 | 설명 |
|--------|------|
| `yarn dev` | 개발 서버 |
| `yarn build` | 빌드 |
| `yarn test` | 전체 테스트 |
| `yarn test:integration` | E2E 테스트 |
| `yarn test:unit` | Unit 테스트 |
| `yarn check` | 타입 체크 |
| `yarn lint` | Lint |
| `yarn format` | 포맷팅 |
| `yarn generate-client` | API 클라이언트 생성 |

## 주의사항

- Svelte 5 Runes 문법 사용 (`$state`, `$derived`, `$props`)
- `$:` 반응형 선언문은 Svelte 4 문법이므로 사용 금지
- API 타입은 `$lib/api/client`에서 import
- 컴포넌트 테스트 시 export 함수로 로직 분리
