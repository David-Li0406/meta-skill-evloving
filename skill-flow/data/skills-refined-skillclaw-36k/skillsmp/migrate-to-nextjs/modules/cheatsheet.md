# Migration Cheatsheet

React → Next.js 16 마이그레이션 빠른 참조 가이드입니다.

---

## 🚀 Quick Commands

```bash
# 1단계: 분석
/jikime:migrate-1-analyze "./my-app"

# 2단계: 계획
/jikime:migrate-2-plan my-app

# 3단계: 스킬
/jikime:migrate-2-plan --skill my-app

# 4단계: 실행
/jikime:migrate-3-execute my-app --output ./out
```

---

## 📁 생성 파일 위치

| 단계 | 파일 | 설명 |
|------|------|------|
| analyze | `./migrations/{project}/as_is_spec.md` | 현재 상태 분석 |
| plan | `./migrations/{project}/migration_plan.md` | 마이그레이션 계획 |
| skill | `./migrations/{project}/SKILL.md` | 프로젝트별 규칙 |
| run | `{output}/{project}/` | 마이그레이션된 프로젝트 |

---

## 🔄 패턴 변환 Quick Reference

### Imports

```tsx
// Before (React)
import { useNavigate } from 'react-router-dom'
import { useSelector, useDispatch } from 'react-redux'

// After (Next.js)
import { useRouter } from 'next/navigation'
import { useStore } from '@/stores/myStore'
```

### Navigation

```tsx
// Before
const navigate = useNavigate()
navigate('/dashboard')
navigate(-1)

// After
const router = useRouter()
router.push('/dashboard')
router.back()
```

### State (Redux → Zustand)

```tsx
// Before
const data = useSelector(selectData)
const dispatch = useDispatch()
dispatch(action(payload))

// After
const { data, action } = useStore()
action(payload)
```

### Styling (styled → Tailwind)

```tsx
// Before
const Button = styled.button`
  background: blue;
  color: white;
  padding: 8px 16px;
`

// After
<button className="bg-blue-500 text-white px-4 py-2">
```

### Environment Variables

```bash
# Before (CRA)
REACT_APP_API_URL=...

# After (Next.js)
NEXT_PUBLIC_API_URL=...
```

---

## 📦 Component Types

```tsx
// Server Component (기본값) - 'use client' 없음
export default async function Page() {
  const data = await fetch(...)
  return <div>{data}</div>
}

// Client Component - 'use client' 필수
'use client'
export function Button() {
  const [state, setState] = useState()
  return <button onClick={...}>
}
```

### When to use 'use client'

| 필요 | 불필요 |
|------|--------|
| useState, useEffect | 데이터 페칭만 |
| onClick, onChange | 정적 렌더링 |
| useRouter (push/back) | Link 컴포넌트 |
| Browser APIs | Server-only 로직 |

---

## 🗂️ Routing 변환

```
# Before (React Router)
src/pages/
├── Home.tsx           → app/page.tsx
├── Dashboard.tsx      → app/dashboard/page.tsx
├── Settings.tsx       → app/settings/page.tsx
└── Profile/[id].tsx   → app/profile/[id]/page.tsx

# Dynamic Routes
/users/:id            → /users/[id]
/posts/:slug          → /posts/[slug]
/*                    → [...slug] (catch-all)
```

---

## 📊 State Migration

```
Redux Toolkit          →  Zustand
---------------------------------------------
createSlice            →  create()
useSelector            →  useStore(state => ...)
useDispatch + action   →  useStore().action()
configureStore         →  삭제 (불필요)
Provider               →  삭제 (불필요)
```

---

## 🔧 Common Fixes

### Hydration Error

```tsx
'use client'
import { useEffect, useState } from 'react'

export function ClientOnly({ children }) {
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])
  if (!mounted) return null
  return children
}
```

### Image Optimization

```typescript
// next.config.ts
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'example.com' }
    ]
  }
}
```

### Missing 'use client'

```
Error: useState only works in Client Components
Fix: Add 'use client' at the top of the file
```

---

## 📋 Checklist

### Pre-Migration
- [ ] Node.js 20+ 설치
- [ ] 기존 프로젝트 백업
- [ ] 의존성 목록 확인

### During Migration
- [ ] 컴포넌트 타입 결정 (Server/Client)
- [ ] 상태 관리 전환
- [ ] 라우팅 구조 변환
- [ ] 스타일링 변환

### Post-Migration
- [ ] TypeScript 컴파일 확인
- [ ] 빌드 성공 확인
- [ ] 주요 기능 테스트
- [ ] 성능 벤치마크

---

## 🎯 Target Stack

| 항목 | 기술 |
|------|------|
| Framework | Next.js 16 (App Router) |
| Language | TypeScript 5.x |
| Styling | Tailwind CSS 4.x |
| UI | shadcn/ui |
| State | Zustand |
| Forms | react-hook-form + zod |
| Icons | lucide-react |

---

## 🔗 Related Commands

```bash
# 백서 생성 (사전 분석)
/jikime:migrate-1-analyze "./app" --whitepaper --client "Company"

# 완료 보고서
/jikime:migrate-3-execute app --whitepaper-report --client "Company"

# 커스텀 출력 경로
/jikime:migrate-3-execute app --output ./custom/path

# 특정 언어로 문서 생성
--lang ko  # 한국어
--lang en  # English
--lang ja  # 日本語
```

---

Version: 1.0.0
Last Updated: 2026-01-22
