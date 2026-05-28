---
name: jikime-framework-nextjs@14
description: Next.js 14 App Router baseline guide. Core patterns, conventions, and best practices for Next.js 14.x applications.
tags: ["framework", "nextjs", "version", "app-router", "server-components", "server-actions"]
triggers:
  keywords: ["nextjs", "next.js 14", "app-router", "server-components", "server-actions"]
  phases: ["run"]
  agents: ["frontend"]
  languages: ["typescript"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2159
type: version
framework: nextjs
version: "14"
user-invocable: false
---

# Next.js 14 Baseline Guide

Next.js 14 App Router의 핵심 패턴과 규칙을 정의합니다. 버전 업그레이드 시 기준점으로 사용됩니다.

## Version Info

| 항목 | 값 |
|------|-----|
| Version | 14.0.0 ~ 14.2.x |
| Release Date | October 2023 |
| Node.js | 18.17+ |
| React | 18.2+ |

---

## Core Features (Next.js 14)

### 1. App Router (Stable)

```
src/
└── app/
    ├── layout.tsx          # Root layout (required)
    ├── page.tsx            # Home page
    ├── loading.tsx         # Loading UI
    ├── error.tsx           # Error boundary
    ├── not-found.tsx       # 404 page
    ├── [slug]/
    │   └── page.tsx        # Dynamic route
    └── api/
        ├── auth/
        │   └── route.ts    # POST /api/auth
        ├── users/
        │   ├── route.ts    # GET, POST /api/users
        │   └── [id]/
        │       └── route.ts # GET, PUT, DELETE /api/users/:id
        └── health-check/
            └── route.ts    # GET /api/health-check
```

### Naming Conventions (CRITICAL)

| 대상 | 규칙 | 예시 |
|------|------|------|
| 폴더명 | kebab-case | `user-profile/`, `health-check/` |
| route 파일명 | 고정 (`route.ts`, `page.tsx`) | Next.js 규약 |
| 컴포넌트 파일 | kebab-case | `user-card.tsx`, `nav-menu.tsx` |
| 컴포넌트 이름 | PascalCase | `UserCard`, `NavMenu` |
| 유틸리티 파일 | kebab-case | `format-date.ts`, `use-auth.ts` |

**WHY**: URL 경로가 폴더명에서 자동 생성되므로, kebab-case가 웹 표준 URL 규약과 일치합니다.

```
# CORRECT
src/app/user-profile/page.tsx    → /user-profile
src/app/api/health-check/route.ts → /api/health-check

# WRONG
src/app/userProfile/page.tsx     → /userProfile (비표준 URL)
src/app/api/healthCheck/route.ts → /api/healthCheck (비표준 URL)
```

### 2. Server Components (Default)

```tsx
// src/app/users/page.tsx - Server Component by default
async function getUsers() {
  const res = await fetch('https://api.example.com/users')
  return res.json()
}

export default async function UsersPage() {
  const users = await getUsers()
  return <UserList users={users} />
}
```

### 3. Client Components

```tsx
// src/components/counter.tsx
'use client'

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>
}
```

### 4. Server Actions (Stable in 14.0)

```tsx
// src/app/actions.ts
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title')
  await db.post.create({ data: { title } })
  revalidatePath('/posts')
}

// src/app/posts/new/page.tsx
import { createPost } from '../actions'

export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" />
      <button type="submit">Create</button>
    </form>
  )
}
```

### 5. Metadata API

```tsx
// Static metadata
export const metadata = {
  title: 'My App',
  description: 'App description',
}

// Dynamic metadata
export async function generateMetadata({ params }) {
  const post = await getPost(params.slug)
  return { title: post.title }
}
```

### 6. Route Handlers

```tsx
// src/app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const users = await db.user.findMany()
  return NextResponse.json(users)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const user = await db.user.create({ data: body })
  return NextResponse.json(user, { status: 201 })
}
```

---

## Data Fetching (Next.js 14)

### Fetch with Caching

```tsx
// Default: cached (equivalent to force-cache)
const data = await fetch('https://api.example.com/data')

// No caching
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store'
})

// Time-based revalidation
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 }  // Revalidate every hour
})

// Tag-based revalidation
const data = await fetch('https://api.example.com/data', {
  next: { tags: ['posts'] }
})
```

### Revalidation

```tsx
import { revalidatePath, revalidateTag } from 'next/cache'

// Path-based
revalidatePath('/posts')
revalidatePath('/posts/[slug]', 'page')

// Tag-based
revalidateTag('posts')
```

---

## Dynamic Routes (Next.js 14)

### Params Access (Synchronous)

```tsx
// src/app/posts/[slug]/page.tsx
type Props = {
  params: { slug: string }  // Direct access (synchronous)
  searchParams: { [key: string]: string | string[] | undefined }
}

export default function PostPage({ params, searchParams }: Props) {
  const { slug } = params  // Direct destructuring
  const { sort } = searchParams

  return <div>Post: {slug}</div>
}
```

### generateStaticParams

```tsx
export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map(post => ({ slug: post.slug }))
}
```

---

## Middleware (Next.js 14)

```tsx
// src/middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*']
}
```

---

## Configuration (Next.js 14)

### next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'example.com' }
    ]
  },
  experimental: {
    serverActions: true,  // Enabled by default in 14.0+
  }
}

module.exports = nextConfig
```

---

## UI Component Library (MANDATORY)

Next.js 프로젝트에서는 **항상 shadcn/ui**를 사용합니다.

### Setup

```bash
# 새 프로젝트: shadcn이 Next.js 프로젝트를 자동 생성
npx shadcn@latest init --src-dir

# 기존 프로젝트: 현재 프로젝트에 shadcn/ui 추가
npx shadcn@latest init
```

### components.json (프로젝트 루트)

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "src/app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "ui": "@/components/ui",
    "utils": "@/lib/utils",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

### Project Structure with shadcn/ui

```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css          # Tailwind + CSS variables
│   └── api/
│       └── users/
│           └── route.ts
├── components/
│   ├── ui/                  # shadcn/ui 컴포넌트 (자동 생성)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   └── custom/              # 프로젝트 커스텀 컴포넌트
│       ├── user-card.tsx
│       └── nav-menu.tsx
├── hooks/                   # 커스텀 훅
│   └── use-auth.ts
├── lib/
│   └── utils.ts             # cn() 유틸리티 (shadcn 필수)
└── types/
    └── index.ts
```

### Rules

- [HARD] UI 컴포넌트 구현 시 항상 shadcn/ui를 우선 사용
- [HARD] shadcn/ui에 없는 컴포넌트만 커스텀 구현
- [HARD] Tailwind CSS + CSS variables 기반 테마 시스템 사용
- [HARD] 아이콘은 lucide-react 사용
- 관련 스킬: `jikime-library-shadcn` (상세 구현 가이드)

### Component Usage

```tsx
// shadcn/ui 컴포넌트 사용
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardContent } from '@/components/ui/card'

export function UserCard({ user }) {
  return (
    <Card>
      <CardHeader>{user.name}</CardHeader>
      <CardContent>
        <Button variant="outline">Edit</Button>
      </CardContent>
    </Card>
  )
}
```

### Adding Components

```bash
# 개별 컴포넌트 추가
npx shadcn@latest add button
npx shadcn@latest add card dialog

# 사용 가능한 컴포넌트 목록 확인
npx shadcn@latest add
```

---

## Key Limitations (14.x)

| 기능 | 상태 |
|------|------|
| Server Actions | Stable |
| Partial Prerendering | Experimental |
| Turbopack | Dev only (unstable) |
| `params` access | Synchronous |
| `'use cache'` | Not available |

---

## Upgrade Path

**Next.js 14 → 15**: See `jikime-framework-nextjs@15`
- `params`/`searchParams` become async (Promise)
- Turbopack becomes stable for dev
- fetch caching default changes

---

Version: 1.0.0
Last Updated: 2026-01-22
