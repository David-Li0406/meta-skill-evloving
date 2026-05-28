# Project Initialization Guide

Next.js 16 + shadcn/ui 프로젝트 초기화 완전 가이드입니다.

---

## Quick Setup (Copy & Paste)

```bash
# 1. Next.js 프로젝트 생성
npx create-next-app@latest my-project --typescript --tailwind --eslint --app --src-dir

# 2. 프로젝트 폴더 이동
cd my-project

# 3. shadcn/ui 초기화
npx shadcn@latest init

# 4. 기본 컴포넌트 설치
npx shadcn@latest add button card input label

# 5. 추가 패키지 설치
npm install zustand react-hook-form @hookform/resolvers zod lucide-react

# 6. 개발 서버 실행
npm run dev
```

---

## Step 1: Next.js 프로젝트 생성

### 명령어

```bash
npx create-next-app@latest my-project
```

### 대화형 옵션 선택

```
✔ Would you like to use TypeScript? … Yes
✔ Would you like to use ESLint? … Yes
✔ Would you like to use Tailwind CSS? … Yes
✔ Would you like your code inside a `src/` directory? … Yes
✔ Would you like to use App Router? (recommended) … Yes
✔ Would you like to use Turbopack for next dev? … Yes
✔ Would you like to customize the import alias? … No
```

### 또는 플래그로 한 번에 설정

```bash
npx create-next-app@latest my-project \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --turbopack \
  --import-alias "@/*"
```

### 생성되는 구조

```
my-project/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   └── lib/
├── public/
├── package.json
├── tailwind.config.ts
├── tsconfig.json
├── next.config.ts
└── .eslintrc.json
```

---

## Step 2: shadcn/ui 초기화

### 프로젝트 폴더 이동

```bash
cd my-project
```

### shadcn 초기화

```bash
npx shadcn@latest init
```

### 대화형 옵션 선택

```
✔ Which style would you like to use? › New York
✔ Which color would you like to use as the base color? › Neutral
✔ Would you like to use CSS variables for theming? › Yes
```

### 권장 설정

| 옵션 | 권장값 | 설명 |
|------|--------|------|
| Style | **New York** | 모던하고 깔끔한 스타일 |
| Base color | **Neutral** | 범용적인 그레이 톤 |
| CSS variables | **Yes** | 다크모드, 테마 지원 |

### 생성/수정되는 파일

```
my-project/
├── src/
│   ├── components/
│   │   └── ui/           ← 새로 생성
│   └── lib/
│       └── utils.ts      ← cn() 함수 추가
├── components.json       ← shadcn 설정 파일
└── tailwind.config.ts    ← 업데이트됨
```

### components.json 예시

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
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
```

---

## Step 3: 기본 컴포넌트 설치

### 필수 컴포넌트 (권장)

```bash
# 기본 UI 요소
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add textarea

# 한 번에 여러 개 설치
npx shadcn@latest add button card input label textarea
```

### 폼 관련 컴포넌트

```bash
npx shadcn@latest add form
npx shadcn@latest add checkbox
npx shadcn@latest add select
npx shadcn@latest add switch
npx shadcn@latest add radio-group
```

### 레이아웃/네비게이션

```bash
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
npx shadcn@latest add sheet
npx shadcn@latest add tabs
npx shadcn@latest add navigation-menu
```

### 피드백/상태

```bash
npx shadcn@latest add alert
npx shadcn@latest add badge
npx shadcn@latest add toast
npx shadcn@latest add skeleton
npx shadcn@latest add progress
```

### 데이터 표시

```bash
npx shadcn@latest add table
npx shadcn@latest add avatar
npx shadcn@latest add separator
```

### 마이그레이션 프로젝트 추천 세트

```bash
# 한 번에 설치 (마이그레이션용 추천)
npx shadcn@latest add \
  button card input label textarea \
  form checkbox select switch \
  dialog dropdown-menu sheet tabs \
  alert badge toast skeleton \
  table avatar separator
```

---

## Step 4: 추가 패키지 설치

### 상태 관리 (Zustand)

```bash
npm install zustand
```

### 폼 검증 (react-hook-form + zod)

```bash
npm install react-hook-form @hookform/resolvers zod
```

### 아이콘 (lucide-react)

```bash
npm install lucide-react
```

### 날짜 처리 (선택)

```bash
npm install date-fns
```

### HTTP 클라이언트 (선택 - Server Actions 사용 시 불필요)

```bash
# Server Actions 사용 시 불필요
# 외부 API 호출 필요 시에만
npm install ky
# 또는
npm install axios
```

### 전체 한 번에 설치

```bash
npm install \
  zustand \
  react-hook-form @hookform/resolvers zod \
  lucide-react \
  date-fns
```

---

## Step 5: 프로젝트 구조 설정

### 권장 폴더 구조 생성

```bash
# 폴더 생성
mkdir -p src/components/ui
mkdir -p src/stores
mkdir -p src/hooks
mkdir -p src/types
mkdir -p src/actions
```

### 최종 구조

```
my-project/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   ├── api/
│   │   │   ├── auth/
│   │   │   │   └── route.ts
│   │   │   └── health-check/   ← kebab-case
│   │   │       └── route.ts
│   │   └── (routes)/
│   │       ├── dashboard/
│   │       │   └── page.tsx
│   │       └── user-settings/  ← kebab-case
│   │           └── page.tsx
│   ├── components/
│   │   ├── ui/              ← shadcn 컴포넌트
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   └── input.tsx
│   │   └── custom/          ← 커스텀 컴포넌트
│   │       ├── site-header.tsx  ← kebab-case
│   │       └── site-footer.tsx
│   ├── stores/              ← Zustand 스토어
│   │   └── use-app-store.ts
│   ├── hooks/               ← 커스텀 훅
│   │   └── use-auth.ts
│   ├── actions/             ← Server Actions
│   │   └── auth.ts
│   ├── lib/
│   │   ├── utils.ts         ← cn() 함수
│   │   └── validations.ts   ← Zod 스키마
│   └── types/
│       └── index.ts
├── public/
├── package.json
├── components.json
├── tailwind.config.ts
├── tsconfig.json
└── next.config.ts
```

### 네이밍 규칙 (CRITICAL)

| 대상 | 규칙 | 예시 |
|------|------|------|
| 폴더명 | kebab-case | `user-profile/`, `health-check/` |
| 파일명 | kebab-case | `site-header.tsx`, `use-auth.ts` |
| route/page 파일 | Next.js 규약 고정 | `route.ts`, `page.tsx`, `layout.tsx` |
| 컴포넌트 export 이름 | PascalCase | `SiteHeader`, `UserCard` |

**WHY**: URL 경로가 폴더명에서 자동 생성되므로, kebab-case가 웹 표준 URL 규약과 일치합니다.

---

## Step 6: 기본 파일 설정

### lib/utils.ts (shadcn에서 자동 생성)

```typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### lib/validations.ts (새로 생성)

```typescript
import { z } from 'zod'

// 공통 스키마
export const emailSchema = z.string().email('유효한 이메일을 입력하세요')
export const passwordSchema = z.string().min(8, '8자 이상 입력하세요')

// 폼 스키마 예시
export const loginSchema = z.object({
  email: emailSchema,
  password: passwordSchema,
})

export type LoginInput = z.infer<typeof loginSchema>
```

### stores/useAppStore.ts (새로 생성)

```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AppState {
  // Theme
  theme: 'light' | 'dark'
  setTheme: (theme: 'light' | 'dark') => void

  // User
  user: { id: string; name: string } | null
  setUser: (user: { id: string; name: string } | null) => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),

      user: null,
      setUser: (user) => set({ user }),
    }),
    {
      name: 'app-storage',
    }
  )
)
```

### types/index.ts (새로 생성)

```typescript
// 공통 타입 정의
export interface User {
  id: string
  email: string
  name: string
  avatar?: string
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}
```

---

## Step 7: 개발 서버 실행

```bash
npm run dev
```

### 예상 출력

```
▲ Next.js 16.0.0 (Turbopack)

   - Local:        http://localhost:3000
   - Network:      http://192.168.1.100:3000

 ✓ Starting...
 ✓ Ready in 980ms
```

---

## 검증 체크리스트

### 설치 확인

```bash
# package.json 확인
cat package.json | grep -E "next|react|zustand|zod"
```

### 파일 확인

```bash
# shadcn 설정 확인
cat components.json

# 컴포넌트 확인
ls src/components/ui/
```

### 빌드 테스트

```bash
npm run build
```

### 예상 결과

```
✓ Compiled successfully
✓ Linting and checking validity of types
✓ Collecting page data
✓ Generating static pages
✓ Finalizing page optimization

Route (app)                    Size     First Load JS
─────────────────────────────────────────────────────
○ /                            5.2 kB         89.1 kB
○ /dashboard                   3.1 kB         87.0 kB
```

---

## 문제 해결

### shadcn init 실패

```bash
# 캐시 클리어 후 재시도
npm cache clean --force
npx shadcn@latest init
```

### Tailwind 스타일 미적용

```typescript
// tailwind.config.ts 확인
const config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',  // src 폴더 포함 확인
  ],
  // ...
}
```

### TypeScript 경로 오류

```json
// tsconfig.json 확인
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

---

## 마이그레이션 프로젝트용 원라인 설정

### 전체 설정 스크립트

```bash
#!/bin/bash
# migration-setup.sh

PROJECT_NAME=${1:-"migration-project"}

# 1. 프로젝트 생성
npx create-next-app@latest $PROJECT_NAME \
  --typescript --tailwind --eslint --app --src-dir --turbopack

# 2. 폴더 이동
cd $PROJECT_NAME

# 3. shadcn 초기화 (기본값 사용)
npx shadcn@latest init -d

# 4. 기본 컴포넌트 설치
npx shadcn@latest add button card input label form dialog toast

# 5. 패키지 설치
npm install zustand react-hook-form @hookform/resolvers zod lucide-react

# 6. 폴더 구조 생성
mkdir -p src/stores src/hooks src/types src/actions

# 7. 완료 메시지
echo "✅ Project setup complete!"
echo "Run: cd $PROJECT_NAME && npm run dev"
```

### 사용법

```bash
# 스크립트 실행
chmod +x migration-setup.sh
./migration-setup.sh my-new-project
```

---

Version: 1.0.0
Last Updated: 2026-01-22
