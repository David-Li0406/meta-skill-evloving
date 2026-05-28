---
name: frontend-development
description: ForkLore 프론트엔드(Next.js 16/React 19) 개발 워크플로우 스킬. 이슈 기반 개발 + develop 브랜치 전략 + Server-First 아키텍처 + shadcn/ui 컴포넌트 + Zustand 상태관리 + Vitest/ESLint/Prettier 린트 + TDD 워크플로. Use when working on frontend features/bugfixes, components, pages, hooks, stores, API clients, or when asked to create PR targeting develop.
requires-skills:
  - nextjs-best-practices
  - vercel-react-best-practices
  - typescript-expert
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Frontend Development (ForkLore)

ForkLore 프론트엔드(Next.js 16 + React 19) 개발을 **이슈 기반 + Server-First + develop 중심 브랜치 전략**으로 일관되게 진행하기 위한 표준 워크플로.

## Quick Reference (빠른 참조)

### 자주 쓰는 커맨드

```bash
# 개발 서버
pnpm dev                                    # 로컬 서버 (port 3000)
pnpm build                                  # 프로덕션 빌드
pnpm start                                  # 프로덕션 서버

# 테스트
pnpm test                                   # Vitest 전체 실행
pnpm test:watch                             # 감시 모드
pnpm test -- --coverage                     # 커버리지

# 린트/포맷
pnpm lint                                   # ESLint 체크
pnpm lint --fix                             # ESLint 자동 수정

# E2E 테스트
pnpm playwright test                        # Playwright E2E
pnpm playwright test --ui                   # UI 모드
```

### Context7 빠른 조회

```typescript
// Next.js 16 최신 패턴
context7_query-docs(libraryId="/vercel/next.js", query="...")

// React 19 최신 패턴  
context7_query-docs(libraryId="/facebook/react", query="...")

// TanStack Query
context7_query-docs(libraryId="/tanstack/query", query="...")

// Zod 스키마 검증
context7_query-docs(libraryId="/colinhacks/zod", query="...")
```

## 소스 오브 트루스

- 레포 전체 규칙: `AGENTS.md`
- 프론트엔드 구조/원칙: `frontend/AGENTS.md`
- Next.js 가이드: `docs/frontend/nextjs-guide.md`
- React 19 가이드: `docs/frontend/react-guide.md`
- Shadcn/ui 가이드: `docs/frontend/shadcn-guide.md`
- Git 이슈/브랜치/커밋/PR: `docs/development-guidelines.md`

## 필수 원칙 (하드 룰)

### Server-First 아키텍처
- **기본은 Server Component**: 모든 파일은 기본적으로 서버 컴포넌트
- **Client는 최소한으로**: `'use client'`는 상호작용이 필요한 경우에만 사용
- **Client는 Leaf에 배치**: 클라이언트 컴포넌트는 트리의 말단에 위치

### 컴포넌트 결정 테이블

| 필요 기능 | Server Component | Client Component |
|-----------|:----------------:|:----------------:|
| 데이터 페칭 (DB 직접 접근) | O | X |
| 백엔드 리소스 직접 접근 (보안) | O | X |
| 민감한 정보 유지 (API 키 등) | O | X |
| 브라우저 API 사용 (window, localStorage) | X | O |
| 상태 및 생명주기 훅 사용 (useState, useEffect) | X | O |
| 사용자 상호작용 (onClick, onChange) | X | O |

### Next.js 16 필수 패턴

**Async Params (필수)**
```tsx
// Next.js 16 방식 (비동기 처리)
export default async function Page({ 
  params 
}: { 
  params: Promise<{ slug: string }> 
}) {
  const { slug } = await params;
  return <div>{slug}</div>;
}
```

### 스타일링 규칙
- **Tailwind CSS 4**: 유틸리티 클래스 사용, CSS 모듈 금지
- **shadcn/ui**: `components/ui/` 컴포넌트 활용 (직접 수정 가능)
- **cn() 유틸리티**: 조건부 클래스 결합 필수 사용

### 안티패턴 (금지)
- X **useEffect로 데이터 페칭**: Server Component 또는 React Query 사용
- X **Prop Drilling**: Composition 또는 Zustand 사용
- X **Client-Side Secrets**: 클라이언트에 API 키/시크릿 노출 금지
- X **`as any`, `@ts-ignore`**: 타입 안전성 필수

## 프로젝트 구조

```
frontend/
├── app/                  # App Router 페이지 (Server Component 기본)
│   ├── (marketing)/      # Route Group
│   ├── layout.tsx        # 루트 레이아웃
│   └── page.tsx          # 홈 페이지
├── components/
│   ├── ui/               # shadcn/ui 컴포넌트 (수정 가능)
│   ├── common/           # 공통 UI (Header, Footer)
│   ├── feature/          # 도메인별 컴포넌트 (novels, reader, wiki)
│   └── providers/        # Context Providers
├── hooks/                # 커스텀 React 훅
├── lib/                  # 유틸리티, API 클라이언트, Zod 스키마
│   ├── api/              # API 클라이언트 함수
│   └── utils.ts          # cn() 등 유틸리티
└── stores/               # Zustand 스토어
```

### 파일명 규칙

| 종류 | 파일명 | export 이름 |
|------|--------|-------------|
| 컴포넌트 | `novel-card.tsx` | `NovelCard` |
| 훅 | `use-novel.ts` | `useNovel` |
| 스토어 | `auth-store.ts` | `useAuthStore` |
| API 클라이언트 | `novels-api.ts` | `getNovel`, `createNovel` |
| 테스트 | `novel-card.test.tsx` | - |

## 워크플로우

### 1) 이슈 확인/생성 (GitHub)

- 작업 시작 전 GitHub에서 관련 이슈가 있는지 검색
- 없으면 새 이슈를 생성하고, 요구사항/범위/완료 조건(AC)을 정리

### 2) 브랜치 생성 (Base: develop)

- `develop` 최신화 후, 이슈 기준으로 새 브랜치 생성
- 브랜치명: `feat/#<issue>-<short-english-summary>` 또는 `fix/#<issue>-<short-english-summary>`

### 3) 개발 환경 준비

```bash
cd frontend
pnpm install
pnpm dev
# http://localhost:3000 에서 확인
```

### 4) 컴포넌트 개발 (Server-First)

**Step 1: Server vs Client 결정**
- 상호작용 필요? → Client Component
- 데이터만 표시? → Server Component

**Step 2: 컴포넌트 생성**
```tsx
// Server Component (기본)
export async function NovelList() {
  const novels = await fetchNovels();
  return <div>{novels.map(renderNovel)}</div>;
}

// Client Component (상호작용 필요 시)
'use client';

export function NovelFilters() {
  const [filter, setFilter] = useState('all');
  return <select value={filter} onChange={(e) => setFilter(e.target.value)} />;
}
```

**Step 3: 테스트 작성**
```tsx
// novel-card.test.tsx
import { render, screen } from '@testing-library/react';
import { NovelCard } from './novel-card';

describe('NovelCard', () => {
  it('renders novel title', () => {
    render(<NovelCard novel={mockNovel} />);
    expect(screen.getByText(mockNovel.title)).toBeInTheDocument();
  });
});
```

### 5) 상태 관리 패턴

**서버 상태 (React Query)**
```tsx
import { useQuery } from '@tanstack/react-query';
import { getNovel } from '@/lib/api/novels-api';

export function useNovel(id: string) {
  return useQuery({
    queryKey: ['novel', id],
    queryFn: () => getNovel(id),
  });
}
```

**클라이언트 상태 (Zustand)**
```tsx
// stores/auth-store.ts
import { create } from 'zustand';

interface AuthState {
  user: User | null;
  setUser: (user: User | null) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}));
```

### 6) API 클라이언트 패턴

```tsx
// lib/api/novels-api.ts
import { apiClient } from './client';
import { NovelSchema, type Novel } from './schemas';

export async function getNovel(id: string): Promise<Novel> {
  const response = await apiClient.get(`/novels/${id}`);
  return NovelSchema.parse(response.data);
}

export async function createNovel(data: CreateNovelInput): Promise<Novel> {
  const response = await apiClient.post('/novels', data);
  return NovelSchema.parse(response.data);
}
```

### 7) Zod 스키마 검증

```tsx
// lib/api/schemas.ts
import { z } from 'zod';

export const NovelSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1),
  author: z.string(),
  coverImage: z.string().url().nullable(),
});

export type Novel = z.infer<typeof NovelSchema>;
```

### 8) Form 처리 (React Hook Form + Zod)

```tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

const formSchema = z.object({
  title: z.string().min(2, '제목은 2글자 이상이어야 합니다'),
  description: z.string().optional(),
});

export function NovelForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { title: '', description: '' },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>제목</FormLabel>
              <FormControl>
                <Input placeholder="소설 제목" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">저장</Button>
      </form>
    </Form>
  );
}
```

### 9) Context7로 최신 사용법 확인 (필수)

**모든 라이브러리 사용 시 Context7로 최신 버전/패턴 확인**

#### 필수 확인 라이브러리 (ForkLore 스택)

| 라이브러리 | Context7 ID | 주요 확인 사항 |
|------------|-------------|----------------|
| Next.js 16 | `/vercel/next.js` | App Router, Server Actions, async params |
| React 19 | `/facebook/react` | use(), useActionState, Server Components |
| TanStack Query | `/tanstack/query` | useQuery, useMutation, prefetching |
| Zod 4 | `/colinhacks/zod` | 스키마 정의, 폼 검증, 타입 추론 |
| Zustand | `resolve-library-id`로 확인 | create, persist, devtools |
| Framer Motion | `resolve-library-id`로 확인 | motion, AnimatePresence |

#### Context7 활용 워크플로우

```
1. 라이브러리 사용 전:
   context7_resolve-library-id(libraryName="@tanstack/react-query", query="...")
   
2. 최신 패턴 확인:
   context7_query-docs(libraryId="/tanstack/query", query="useQuery best practices")
   
3. 코드 적용 시:
   - deprecated 경고 발견 → 즉시 대체 구현
   - 최신 권장 패턴 우선 적용
```

### 10) 테스트 실행

```bash
cd frontend
pnpm test                    # 전체 테스트
pnpm test novel-card         # 특정 파일
pnpm test -- --coverage      # 커버리지
```

### 11) 린트/포맷 점검

```bash
cd frontend
pnpm lint                    # ESLint 체크
pnpm lint --fix              # 자동 수정
```

### 12) 빌드 검증

```bash
cd frontend
pnpm build                   # 프로덕션 빌드
# 에러 없이 완료되어야 함
```

### 13) 커밋/푸시/PR 생성 (Target: develop)

- "하나의 feature 단위"가 끝날 때마다 커밋
- PR 생성 시 포함:
  - 이슈 링크/설명/테스트 결과
  - 스크린샷 (UI 변경 시)
  - 브레이킹 체인지 여부

## 연관 스킬 활용 (Skill Composition)

프론트엔드 개발 중 상황에 따라 다음 스킬을 적극 활용:

| 상황 | 활용 스킬 | 트리거 키워드 |
|------|-----------|---------------|
| **Next.js 패턴** | `/nextjs-best-practices` | App Router, Server Components, 캐싱 |
| **React 성능 최적화** | `/vercel-react-best-practices` | 리렌더, 번들 크기, waterfall |
| **TypeScript 이슈** | `/typescript-expert` | 타입 에러, 제네릭, 타입 추론 |
| **테스트 실패 시** | `/test-fixing` | 테스트 실패, vitest error |
| **디버깅 막힐 때** | `/systematic-debugging` | 버그, 에러, 원인 불명 |
| **코드 린트/검증** | `/lint-and-validate` | eslint, prettier, 포맷 |
| **코드 리뷰 요청** | `/requesting-code-review` | PR 생성 전, 머지 전 검토 |
| **코드 리뷰 수신** | `/receiving-code-review` | 리뷰 피드백 받았을 때 |
| **Git 작업** | `/git-master` (내장) | commit, rebase, squash |

### 스킬 활용 규칙

1. **Next.js/React 패턴 불명확 시**: `/nextjs-best-practices` 또는 `/vercel-react-best-practices` invoke
2. **타입 에러 발생 시**: `/typescript-expert` invoke
3. **테스트 실패 시**: `/test-fixing` invoke 후 수정 시도
4. **라이브러리 사용 전 (필수)**: Context7로 최신 패턴 확인
5. **PR 생성 전**: `/requesting-code-review` invoke로 셀프 리뷰

### 워크플로우 예시 (스킬 체이닝 + Context7)

```
사용자: "소설 상세 페이지 만들어줘"

1. 이슈 확인/생성 → GitHub CLI
2. 브랜치 생성 → /git-master
3. Context7 확인 → Next.js 16 동적 라우트 패턴 조회
   - context7_query-docs(libraryId="/vercel/next.js", query="dynamic routes params")
4. Server Component로 페이지 생성 (app/novels/[id]/page.tsx)
5. API 클라이언트 작성 (lib/api/novels-api.ts)
6. 테스트 작성 (vitest)
7. 테스트 실패 시 → /test-fixing
8. 린트 체크 → pnpm lint
9. 빌드 확인 → pnpm build
10. PR 생성 전 → /requesting-code-review
11. 커밋/푸시 → /git-master
```

## 빠른 파일 네비게이션

### 설정/규약
- `frontend/next.config.ts`
- `frontend/tailwind.config.ts`
- `frontend/components.json`
- `frontend/vitest.config.ts`

### 컴포넌트 예시
- `frontend/components/ui/button.tsx`
- `frontend/components/feature/novels/novel-card.tsx`
- `frontend/components/common/header.tsx`

### 상태 관리 예시
- `frontend/stores/auth-store.ts`
- `frontend/hooks/use-novel.ts`

### API 클라이언트 예시
- `frontend/lib/api/novels-api.ts`
- `frontend/lib/api/client.ts`

## Quality Checklist (PR 전 필수 점검)

PR 생성 전 아래 항목을 모두 확인:

### 코드 품질
- [ ] Server-First 원칙 준수 (Client는 상호작용에만 사용)
- [ ] `'use client'`는 필요한 컴포넌트에만 선언
- [ ] Tailwind CSS 유틸리티 클래스 사용 (CSS 모듈 금지)
- [ ] cn() 유틸리티로 조건부 클래스 결합
- [ ] TypeScript 타입 적용 (as any, @ts-ignore 금지)

### Next.js 16 패턴
- [ ] Async params 패턴 준수 (`params: Promise<...>`)
- [ ] Server Actions는 `'use server'` 선언
- [ ] Suspense 경계 적절히 사용
- [ ] loading.tsx, error.tsx 파일 제공

### 테스트
- [ ] `pnpm test` 전체 통과
- [ ] 새 컴포넌트에 테스트 존재
- [ ] 커버리지 감소 없음

### 린트/포맷
- [ ] `pnpm lint` 에러 없음
- [ ] Prettier 포맷 적용

### 빌드
- [ ] `pnpm build` 성공
- [ ] 런타임 에러 없음

### 보안/민감정보
- [ ] 클라이언트에 API 키/시크릿 노출 없음
- [ ] `.env.local` 커밋 안 함

### 성능
- [ ] 불필요한 useEffect 데이터 페칭 없음
- [ ] React Query로 서버 상태 관리
- [ ] 이미지 최적화 (next/image 사용)
- [ ] barrel imports 지양 (직접 import)

### UI/UX
- [ ] 반응형 디자인 적용
- [ ] 로딩/에러 상태 처리
- [ ] 접근성(a11y) 고려

## Works well with

| 스킬 | 용도 |
|------|------|
| `/nextjs-best-practices` | App Router, Server Components, 라우팅 패턴 |
| `/vercel-react-best-practices` | React 성능 최적화, 리렌더 방지, 번들 최적화 |
| `/typescript-expert` | 타입 에러, 제네릭, 고급 타입 패턴 |
| `/test-fixing` | Vitest 테스트 실패 수정 |
| `/systematic-debugging` | 버그 원인 분석, 디버깅 전략 |
| `/lint-and-validate` | ESLint, Prettier 린트 |
| `/requesting-code-review` | PR 생성 전 셀프 리뷰 |
| `/git-master` | 커밋, 브랜치, rebase, squash |
