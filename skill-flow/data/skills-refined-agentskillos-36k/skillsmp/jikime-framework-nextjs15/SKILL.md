---
name: jikime-framework-nextjs@15
description: Next.js 15 upgrade guide with breaking changes from 14. Async params, Turbopack stable, fetch caching changes.
tags: ["framework", "nextjs", "version", "async-params", "turbopack", "react-19"]
triggers:
  keywords: ["nextjs 15", "next.js 15", "async params", "turbopack", "react 19"]
  phases: ["run"]
  agents: ["frontend"]
  languages: ["typescript"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2022
type: version
framework: nextjs
version: "15"
previous_version: "14"
user-invocable: false
---

# Next.js 15 Upgrade Guide (from 14)

Next.js 14에서 15로 업그레이드 시 필요한 breaking changes와 마이그레이션 패턴을 정의합니다.

## Version Info

| 항목 | 값 |
|------|-----|
| Version | 15.0.0 ~ 15.x |
| Release Date | October 2024 |
| Node.js | 18.18+ (20+ recommended) |
| React | 19 RC |

---

## Base Conventions (from Next.js 14)

다음 규칙은 Next.js 14부터 동일하게 적용됩니다. 상세 내용은 `jikime-framework-nextjs@14`를 참조하세요.

| 규칙 | 요약 |
|------|------|
| **프로젝트 구조** | `src/app/` 기반 App Router, `src/app/api/[endpoint]/route.ts` API 라우트 |
| **네이밍 규칙** | 폴더/파일: kebab-case, 컴포넌트 export: PascalCase |
| **UI 라이브러리** | shadcn/ui 필수 사용, lucide-react 아이콘 |
| **스타일링** | Tailwind CSS + CSS variables 기반 테마 |

---

## Breaking Changes Summary

| 변경 사항 | 영향도 | 자동 수정 |
|-----------|--------|----------|
| `params`/`searchParams` async | 🔴 High | codemod |
| fetch cache default 변경 | 🟡 Medium | Manual |
| `NextRequest.geo`/`ip` 제거 | 🟡 Medium | Manual |
| `next/dynamic` ssr 옵션 | 🟢 Low | codemod |
| Runtime config 제거 | 🟢 Low | Manual |

---

## 1. Async Params (CRITICAL)

### Before (Next.js 14)

```tsx
// src/app/posts/[slug]/page.tsx
type Props = {
  params: { slug: string }
  searchParams: { [key: string]: string | undefined }
}

export default function PostPage({ params, searchParams }: Props) {
  const { slug } = params  // Direct access
  const { sort } = searchParams
  return <div>Post: {slug}</div>
}

export async function generateMetadata({ params }: Props) {
  const post = await getPost(params.slug)  // Direct access
  return { title: post.title }
}
```

### After (Next.js 15)

```tsx
// src/app/posts/[slug]/page.tsx
type Props = {
  params: Promise<{ slug: string }>  // Now a Promise!
  searchParams: Promise<{ [key: string]: string | undefined }>
}

export default async function PostPage({ params, searchParams }: Props) {
  const { slug } = await params  // Must await
  const { sort } = await searchParams
  return <div>Post: {slug}</div>
}

export async function generateMetadata({ params }: Props) {
  const { slug } = await params  // Must await
  const post = await getPost(slug)
  return { title: post.title }
}
```

### Layout Props

```tsx
// Before (14)
type LayoutProps = {
  children: React.ReactNode
  params: { slug: string }
}

// After (15)
type LayoutProps = {
  children: React.ReactNode
  params: Promise<{ slug: string }>
}

export default async function Layout({ children, params }: LayoutProps) {
  const { slug } = await params
  return <div>{children}</div>
}
```

### Codemod

```bash
npx @next/codemod@canary next-async-request-api .
```

---

## 2. Fetch Caching Default Change

### Before (Next.js 14)

```tsx
// Default: force-cache (cached)
const data = await fetch('https://api.example.com/data')
// Equivalent to: fetch(url, { cache: 'force-cache' })
```

### After (Next.js 15)

```tsx
// Default: no-store (NOT cached)
const data = await fetch('https://api.example.com/data')
// Equivalent to: fetch(url, { cache: 'no-store' })

// To cache, must be explicit:
const data = await fetch('https://api.example.com/data', {
  cache: 'force-cache'
})

// Or use time-based revalidation:
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 }
})
```

### Migration Strategy

```tsx
// Option 1: Explicit caching per fetch
const data = await fetch(url, { cache: 'force-cache' })

// Option 2: Route segment config
export const fetchCache = 'default-cache'

// Option 3: next.config.js (temporary)
const nextConfig = {
  experimental: {
    staleTimes: {
      dynamic: 30,
      static: 180,
    }
  }
}
```

---

## 3. NextRequest Changes

### geo/ip Removed

```tsx
// Before (14)
export function middleware(request: NextRequest) {
  const { geo, ip } = request
  const country = geo?.country
}

// After (15) - Use headers from hosting provider
export function middleware(request: NextRequest) {
  // Vercel
  const country = request.headers.get('x-vercel-ip-country')
  const ip = request.headers.get('x-forwarded-for')

  // Or use @vercel/functions
  import { geolocation, ipAddress } from '@vercel/functions'
  const geo = geolocation(request)
  const ip = ipAddress(request)
}
```

---

## 4. Dynamic Import Changes

### ssr Option Renamed

```tsx
// Before (14)
const Component = dynamic(() => import('./component'), {
  ssr: false
})

// After (15)
const Component = dynamic(() => import('./component'), {
  ssr: false  // Still works but deprecated
})

// Recommended
import dynamic from 'next/dynamic'
const Component = dynamic(() => import('./component'), {
  loading: () => <p>Loading...</p>
})
// Use 'use client' directive for client-only components instead
```

---

## 5. Runtime Config Removed

```tsx
// Before (14) - next.config.js
const nextConfig = {
  serverRuntimeConfig: {
    mySecret: 'secret'
  },
  publicRuntimeConfig: {
    apiUrl: 'https://api.example.com'
  }
}

// In component
import getConfig from 'next/config'
const { serverRuntimeConfig, publicRuntimeConfig } = getConfig()

// After (15) - Use environment variables
// .env.local
MY_SECRET=secret
NEXT_PUBLIC_API_URL=https://api.example.com

// In component
const apiUrl = process.env.NEXT_PUBLIC_API_URL
```

---

## 6. Turbopack (Stable for Dev)

```bash
# Next.js 15: Turbopack is stable for development
next dev --turbo

# Or in package.json
{
  "scripts": {
    "dev": "next dev --turbo"
  }
}
```

### next.config.ts Support

```typescript
// next.config.ts (TypeScript support)
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // config
}

export default nextConfig
```

---

## 7. React 19 Compatibility

### New Hooks

```tsx
'use client'

import { useFormStatus, useFormState } from 'react-dom'
import { useOptimistic, use } from 'react'

// useFormStatus - form submission state
function SubmitButton() {
  const { pending } = useFormStatus()
  return <button disabled={pending}>Submit</button>
}

// useOptimistic - optimistic UI updates
function TodoList({ todos }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo) => [...state, newTodo]
  )
}
```

---

## Migration Checklist

### Automated (Codemod)

- [ ] `npx @next/codemod@canary next-async-request-api .`
- [ ] `npx @next/codemod@canary next-dynamic-ssr .`

### Manual Review

- [ ] All `params` access uses `await`
- [ ] All `searchParams` access uses `await`
- [ ] Fetch calls have explicit cache strategy
- [ ] `geo`/`ip` access updated for hosting provider
- [ ] `serverRuntimeConfig`/`publicRuntimeConfig` migrated to env vars
- [ ] TypeScript types updated for async params

### Testing

- [ ] Dynamic routes work correctly
- [ ] Data fetching behavior unchanged (explicit caching)
- [ ] Middleware functions correctly
- [ ] Build succeeds with `next build`

---

## Upgrade Commands

```bash
# Upgrade Next.js
npm install next@15 react@19 react-dom@19

# Run codemods
npx @next/codemod@canary next-async-request-api .

# Upgrade TypeScript types
npm install -D @types/react@19 @types/react-dom@19

# Test
npm run build
npm run dev
```

---

## Rollback Plan

If issues occur:

```bash
# Revert to Next.js 14
npm install next@14 react@18 react-dom@18

# Revert codemod changes
git checkout .
```

---

## Related Skills

| 스킬 | 용도 |
|------|------|
| `jikime-framework-nextjs@14` | Next.js 14 App Router 기본 패턴, 프로젝트 구조, 네이밍 규칙, shadcn/ui |
| `jikime-framework-nextjs@16` | Next.js 16 업그레이드 가이드 ('use cache', PPR, updateTag) |
| `jikime-platform-vercel` | Vercel 배포, Edge Functions, ISR |
| `jikime-library-shadcn` | shadcn/ui 컴포넌트 라이브러리 (Next.js 필수) |

---

Version: 1.1.0
Last Updated: 2026-01-23
Upgrade Path: Next.js 15 → 16: See `jikime-framework-nextjs@16`
