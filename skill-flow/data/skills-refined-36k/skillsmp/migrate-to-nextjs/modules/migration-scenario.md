# React → Next.js 16 전체 마이그레이션 시나리오

실제 React (CRA/Vite) 프로젝트를 Next.js 16 App Router로 마이그레이션하는 종합 가이드입니다.

---

## 시나리오 개요

### 가상 프로젝트: "TaskFlow"

| 항목 | 현재 상태 (AS-IS) |
|------|-------------------|
| 프레임워크 | React 18 + Vite |
| 라우팅 | React Router v6 |
| 상태관리 | Redux Toolkit |
| 인증 | Firebase Auth |
| API | REST (Axios) |
| 스타일링 | Tailwind CSS |
| 테스트 | Jest + React Testing Library |

### 마이그레이션 목표 (TO-BE)

| 항목 | 목표 상태 |
|------|----------|
| 프레임워크 | Next.js 16 App Router |
| 라우팅 | File-based routing |
| 상태관리 | Zustand (client) + Server Components |
| 인증 | NextAuth v5 (Auth.js) |
| API | Server Actions + Route Handlers |
| 스타일링 | Tailwind CSS (유지) |
| 테스트 | Vitest + Playwright |

---

## Phase 0: 사전 분석 (1-2일)

### 0.1 프로젝트 구조 분석

```bash
# 현재 프로젝트 구조
taskflow/
├── src/
│   ├── main.tsx                 # Entry point
│   ├── App.tsx                  # Root component
│   ├── routes/
│   │   ├── index.tsx            # Router config
│   │   ├── ProtectedRoute.tsx   # Auth guard
│   │   └── routes.tsx           # Route definitions
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Tasks/
│   │   │   ├── TaskList.tsx
│   │   │   └── TaskDetail.tsx
│   │   ├── Auth/
│   │   │   ├── Login.tsx
│   │   │   └── Register.tsx
│   │   └── Settings.tsx
│   ├── components/
│   │   ├── Layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   ├── Task/
│   │   │   ├── TaskCard.tsx
│   │   │   └── TaskForm.tsx
│   │   └── ui/
│   │       └── (shadcn components)
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useTasks.ts
│   │   └── useDebounce.ts
│   ├── store/
│   │   ├── index.ts
│   │   ├── taskSlice.ts
│   │   └── userSlice.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── taskService.ts
│   │   └── authService.ts
│   ├── lib/
│   │   ├── firebase.ts
│   │   └── utils.ts
│   └── types/
│       └── index.ts
├── public/
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

### 0.2 의존성 분석

```bash
# 마이그레이션이 필요한 주요 패키지
react-router-dom     → next/navigation (built-in)
@reduxjs/toolkit     → zustand
firebase             → next-auth
axios                → fetch (built-in) / server actions
react-helmet         → next/head (metadata API)
```

### 0.3 컴포넌트 분류

| 분류 | 컴포넌트 | Server/Client |
|------|----------|---------------|
| 레이아웃 | Header, Sidebar, Footer | Server |
| 인터랙티브 | TaskForm, TaskCard (드래그) | Client |
| 데이터 표시 | TaskList, Dashboard | Server |
| 인증 | Login, Register, ProtectedRoute | Client |
| 모달/폼 | TaskForm, SettingsForm | Client |

### 0.4 마이그레이션 복잡도 평가

```yaml
complexity_score: 0.7  # High
components: 25
routes: 8
api_endpoints: 12
auth_flows: 3 (login, register, oauth)
state_slices: 2
estimated_effort: 2-3 weeks
```

---

## Phase 1: 프로젝트 초기화 (1일)

### 1.1 Next.js 16 프로젝트 생성

```bash
# 새 Next.js 프로젝트 생성
npx create-next-app@latest taskflow-next --typescript --tailwind --eslint --app --src-dir

cd taskflow-next

# 추가 의존성 설치
npm install zustand @tanstack/react-query
npm install next-auth@beta @auth/prisma-adapter
npm install prisma @prisma/client
npm install zod react-hook-form @hookform/resolvers
npm install lucide-react
npm install -D vitest @vitejs/plugin-react @testing-library/react
```

### 1.2 디렉토리 구조 설정

```bash
# Next.js 16 구조
taskflow-next/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout
│   │   ├── page.tsx             # Home (/)
│   │   ├── loading.tsx          # Global loading
│   │   ├── error.tsx            # Global error
│   │   ├── not-found.tsx        # 404
│   │   ├── (auth)/              # Auth route group
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── register/
│   │   │       └── page.tsx
│   │   ├── (dashboard)/         # Dashboard route group
│   │   │   ├── layout.tsx       # Dashboard layout
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── tasks/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx
│   │   │   └── settings/
│   │   │       └── page.tsx
│   │   └── api/
│   │       └── auth/
│   │           └── [...nextauth]/
│   │               └── route.ts
│   ├── components/
│   │   ├── layout/
│   │   │   ├── header.tsx
│   │   │   ├── sidebar.tsx
│   │   │   └── footer.tsx
│   │   ├── task/
│   │   │   ├── task-card.tsx
│   │   │   ├── task-form.tsx
│   │   │   └── task-list.tsx
│   │   └── ui/
│   │       └── (shadcn)
│   ├── lib/
│   │   ├── auth.ts              # NextAuth config
│   │   ├── db.ts                # Prisma client
│   │   └── utils.ts
│   ├── hooks/
│   │   └── use-tasks.ts
│   ├── stores/
│   │   └── ui-store.ts          # Zustand for UI state only
│   ├── actions/
│   │   ├── task-actions.ts      # Server Actions
│   │   └── auth-actions.ts
│   └── types/
│       └── index.ts
├── prisma/
│   └── schema.prisma
├── auth.ts                      # NextAuth v5 config
├── middleware.ts                # Auth middleware
└── next.config.ts
```

### 1.3 기본 설정 파일

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    ppr: true,  // Partial Prerendering
  },
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'avatars.githubusercontent.com' },
      { protocol: 'https', hostname: 'lh3.googleusercontent.com' },
    ],
  },
}

export default nextConfig
```

```typescript
// auth.ts (NextAuth v5)
import NextAuth from 'next-auth'
import Google from 'next-auth/providers/google'
import GitHub from 'next-auth/providers/github'
import Credentials from 'next-auth/providers/credentials'
import { PrismaAdapter } from '@auth/prisma-adapter'
import { prisma } from '@/lib/db'

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: 'jwt' },
  providers: [Google, GitHub, Credentials({
    credentials: {
      email: { label: 'Email', type: 'email' },
      password: { label: 'Password', type: 'password' },
    },
    async authorize(credentials) {
      // Implement credential validation
      return null
    },
  })],
  pages: {
    signIn: '/login',
  },
})
```

```typescript
// middleware.ts
import { auth } from '@/auth'
import { NextResponse } from 'next/server'

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isOnDashboard = req.nextUrl.pathname.startsWith('/dashboard') ||
                        req.nextUrl.pathname.startsWith('/tasks') ||
                        req.nextUrl.pathname.startsWith('/settings')
  const isOnAuth = req.nextUrl.pathname.startsWith('/login') ||
                   req.nextUrl.pathname.startsWith('/register')

  if (isOnDashboard && !isLoggedIn) {
    return NextResponse.redirect(new URL('/login', req.url))
  }

  if (isOnAuth && isLoggedIn) {
    return NextResponse.redirect(new URL('/dashboard', req.url))
  }

  return NextResponse.next()
})

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
}
```

---

## Phase 2: 라우팅 마이그레이션 (2-3일)

### 2.1 라우트 매핑

| React Router | Next.js App Router |
|--------------|-------------------|
| `/` | `app/page.tsx` |
| `/login` | `app/(auth)/login/page.tsx` |
| `/register` | `app/(auth)/register/page.tsx` |
| `/dashboard` | `app/(dashboard)/dashboard/page.tsx` |
| `/tasks` | `app/(dashboard)/tasks/page.tsx` |
| `/tasks/:id` | `app/(dashboard)/tasks/[id]/page.tsx` |
| `/settings` | `app/(dashboard)/settings/page.tsx` |

### 2.2 Root Layout

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { SessionProvider } from 'next-auth/react'
import { auth } from '@/auth'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: {
    default: 'TaskFlow',
    template: '%s | TaskFlow',
  },
  description: 'Modern task management application',
}

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await auth()

  return (
    <html lang="en">
      <body className={inter.className}>
        <SessionProvider session={session}>
          {children}
        </SessionProvider>
      </body>
    </html>
  )
}
```

### 2.3 Dashboard Layout

```tsx
// app/(dashboard)/layout.tsx
import { auth } from '@/auth'
import { redirect } from 'next/navigation'
import { Header } from '@/components/layout/header'
import { Sidebar } from '@/components/layout/sidebar'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await auth()

  if (!session) {
    redirect('/login')
  }

  return (
    <div className="flex h-screen">
      <Sidebar user={session.user} />
      <div className="flex-1 flex flex-col">
        <Header user={session.user} />
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
```

### 2.4 Dynamic Route 변환

```tsx
// Before (React Router)
// pages/Tasks/TaskDetail.tsx
import { useParams } from 'react-router-dom'

export function TaskDetail() {
  const { id } = useParams<{ id: string }>()
  // ...
}

// After (Next.js 16)
// app/(dashboard)/tasks/[id]/page.tsx
import { notFound } from 'next/navigation'
import { getTask } from '@/actions/task-actions'
import { TaskDetailView } from '@/components/task/task-detail-view'

type Props = {
  params: Promise<{ id: string }>
}

export default async function TaskDetailPage({ params }: Props) {
  const { id } = await params
  const task = await getTask(id)

  if (!task) {
    notFound()
  }

  return <TaskDetailView task={task} />
}

export async function generateMetadata({ params }: Props) {
  const { id } = await params
  const task = await getTask(id)

  return {
    title: task?.title || 'Task Not Found',
  }
}
```

### 2.5 Navigation 변환

```tsx
// Before (React Router)
import { Link, useNavigate } from 'react-router-dom'

function TaskCard({ task }) {
  const navigate = useNavigate()

  const handleClick = () => {
    navigate(`/tasks/${task.id}`)
  }

  return (
    <div onClick={handleClick}>
      <Link to={`/tasks/${task.id}`}>{task.title}</Link>
    </div>
  )
}

// After (Next.js)
import Link from 'next/link'
import { useRouter } from 'next/navigation'

function TaskCard({ task }) {
  const router = useRouter()

  const handleClick = () => {
    router.push(`/tasks/${task.id}`)
  }

  return (
    <div onClick={handleClick}>
      <Link href={`/tasks/${task.id}`}>{task.title}</Link>
    </div>
  )
}
```

---

## Phase 3: 컴포넌트 마이그레이션 (3-4일)

### 3.1 Server Components로 변환

```tsx
// Before (React - Client Component)
// components/Task/TaskList.tsx
import { useState, useEffect } from 'react'
import { getTasks } from '@/services/taskService'

export function TaskList() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getTasks().then(data => {
      setTasks(data)
      setLoading(false)
    })
  }, [])

  if (loading) return <div>Loading...</div>

  return (
    <div>
      {tasks.map(task => <TaskCard key={task.id} task={task} />)}
    </div>
  )
}

// After (Next.js - Server Component)
// components/task/task-list.tsx
import { getTasks } from '@/actions/task-actions'
import { TaskCard } from './task-card'

export async function TaskList() {
  const tasks = await getTasks()

  return (
    <div className="grid gap-4">
      {tasks.map(task => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  )
}
```

### 3.2 Client Components 분리

```tsx
// components/task/task-card.tsx
// Server Component wrapper
import { Task } from '@/types'
import { TaskCardActions } from './task-card-actions'

type Props = {
  task: Task
}

export function TaskCard({ task }: Props) {
  return (
    <div className="border rounded-lg p-4">
      <h3 className="font-semibold">{task.title}</h3>
      <p className="text-gray-600">{task.description}</p>
      <div className="mt-2 flex items-center justify-between">
        <span className={`badge badge-${task.status}`}>
          {task.status}
        </span>
        {/* Client Component for interactions */}
        <TaskCardActions taskId={task.id} />
      </div>
    </div>
  )
}

// components/task/task-card-actions.tsx
'use client'

import { useState } from 'react'
import { deleteTask, toggleTaskStatus } from '@/actions/task-actions'
import { Button } from '@/components/ui/button'
import { Trash2, Check } from 'lucide-react'

type Props = {
  taskId: string
}

export function TaskCardActions({ taskId }: Props) {
  const [isPending, setIsPending] = useState(false)

  async function handleDelete() {
    setIsPending(true)
    await deleteTask(taskId)
    setIsPending(false)
  }

  async function handleToggle() {
    setIsPending(true)
    await toggleTaskStatus(taskId)
    setIsPending(false)
  }

  return (
    <div className="flex gap-2">
      <Button
        size="sm"
        variant="ghost"
        onClick={handleToggle}
        disabled={isPending}
      >
        <Check className="h-4 w-4" />
      </Button>
      <Button
        size="sm"
        variant="ghost"
        onClick={handleDelete}
        disabled={isPending}
      >
        <Trash2 className="h-4 w-4" />
      </Button>
    </div>
  )
}
```

### 3.3 Form 컴포넌트 변환

```tsx
// Before (React)
import { useState } from 'react'
import { useDispatch } from 'react-redux'
import { createTask } from '@/store/taskSlice'

export function TaskForm() {
  const dispatch = useDispatch()
  const [title, setTitle] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    await dispatch(createTask({ title }))
    setTitle('')
    setLoading(false)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <button disabled={loading}>
        {loading ? 'Creating...' : 'Create'}
      </button>
    </form>
  )
}

// After (Next.js - Server Actions)
// components/task/task-form.tsx
'use client'

import { useFormStatus } from 'react-dom'
import { createTask } from '@/actions/task-actions'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

function SubmitButton() {
  const { pending } = useFormStatus()
  return (
    <Button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create Task'}
    </Button>
  )
}

export function TaskForm() {
  return (
    <form action={createTask} className="flex gap-2">
      <Input
        name="title"
        placeholder="Enter task title..."
        required
      />
      <SubmitButton />
    </form>
  )
}
```

---

## Phase 4: 데이터 페칭 마이그레이션 (2-3일)

### 4.1 Server Actions 생성

```typescript
// actions/task-actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { auth } from '@/auth'
import { prisma } from '@/lib/db'
import { z } from 'zod'

// Schema validation
const createTaskSchema = z.object({
  title: z.string().min(1).max(100),
  description: z.string().optional(),
})

// GET - Cached data
export async function getTasks() {
  'use cache'

  const session = await auth()
  if (!session?.user?.id) return []

  return prisma.task.findMany({
    where: { userId: session.user.id },
    orderBy: { createdAt: 'desc' },
  })
}

export async function getTask(id: string) {
  'use cache'

  const session = await auth()
  if (!session?.user?.id) return null

  return prisma.task.findUnique({
    where: { id, userId: session.user.id },
  })
}

// CREATE
export async function createTask(formData: FormData) {
  const session = await auth()
  if (!session?.user?.id) throw new Error('Unauthorized')

  const rawData = {
    title: formData.get('title'),
    description: formData.get('description'),
  }

  const validated = createTaskSchema.parse(rawData)

  await prisma.task.create({
    data: {
      ...validated,
      userId: session.user.id,
    },
  })

  revalidatePath('/tasks')
}

// UPDATE
export async function updateTask(id: string, formData: FormData) {
  const session = await auth()
  if (!session?.user?.id) throw new Error('Unauthorized')

  const title = formData.get('title') as string

  await prisma.task.update({
    where: { id, userId: session.user.id },
    data: { title },
  })

  revalidatePath('/tasks')
  revalidatePath(`/tasks/${id}`)
}

// DELETE
export async function deleteTask(id: string) {
  const session = await auth()
  if (!session?.user?.id) throw new Error('Unauthorized')

  await prisma.task.delete({
    where: { id, userId: session.user.id },
  })

  revalidatePath('/tasks')
}

// TOGGLE STATUS
export async function toggleTaskStatus(id: string) {
  const session = await auth()
  if (!session?.user?.id) throw new Error('Unauthorized')

  const task = await prisma.task.findUnique({
    where: { id, userId: session.user.id },
  })

  if (!task) throw new Error('Task not found')

  await prisma.task.update({
    where: { id },
    data: {
      status: task.status === 'completed' ? 'pending' : 'completed',
    },
  })

  revalidatePath('/tasks')
}
```

### 4.2 Redux → Zustand 마이그레이션

```typescript
// Before (Redux)
// store/taskSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { taskService } from '@/services/taskService'

export const fetchTasks = createAsyncThunk(
  'tasks/fetchAll',
  async () => await taskService.getAll()
)

const taskSlice = createSlice({
  name: 'tasks',
  initialState: { items: [], loading: false },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchTasks.pending, (state) => { state.loading = true })
      .addCase(fetchTasks.fulfilled, (state, action) => {
        state.items = action.payload
        state.loading = false
      })
  },
})

// After (Zustand - UI state only, server data via Server Components)
// stores/ui-store.ts
import { create } from 'zustand'

interface UIState {
  sidebarOpen: boolean
  taskFilter: 'all' | 'pending' | 'completed'
  searchQuery: string
  toggleSidebar: () => void
  setTaskFilter: (filter: 'all' | 'pending' | 'completed') => void
  setSearchQuery: (query: string) => void
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  taskFilter: 'all',
  searchQuery: '',
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  setTaskFilter: (filter) => set({ taskFilter: filter }),
  setSearchQuery: (query) => set({ searchQuery: query }),
}))
```

### 4.3 API Routes (필요시)

```typescript
// app/api/tasks/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@/auth'
import { prisma } from '@/lib/db'

export async function GET(request: NextRequest) {
  const session = await auth()
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const searchParams = request.nextUrl.searchParams
  const status = searchParams.get('status')

  const tasks = await prisma.task.findMany({
    where: {
      userId: session.user.id,
      ...(status && { status }),
    },
  })

  return NextResponse.json(tasks)
}

// app/api/tasks/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@/auth'
import { prisma } from '@/lib/db'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const session = await auth()
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { id } = await params
  const task = await prisma.task.findUnique({
    where: { id, userId: session.user.id },
  })

  if (!task) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 })
  }

  return NextResponse.json(task)
}
```

---

## Phase 5: 인증 마이그레이션 (2-3일)

### 5.1 Firebase → NextAuth 마이그레이션

```typescript
// scripts/migrate-firebase-users.ts
import { initializeApp, cert } from 'firebase-admin/app'
import { getAuth } from 'firebase-admin/auth'
import { prisma } from '@/lib/db'
import bcrypt from 'bcryptjs'

// Initialize Firebase Admin
const adminApp = initializeApp({
  credential: cert({
    projectId: process.env.FIREBASE_PROJECT_ID,
    clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
    privateKey: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, '\n'),
  }),
})

const firebaseAuth = getAuth(adminApp)

async function migrateUsers() {
  const listUsersResult = await firebaseAuth.listUsers(1000)

  for (const firebaseUser of listUsersResult.users) {
    try {
      // Create user in Prisma
      const user = await prisma.user.create({
        data: {
          email: firebaseUser.email!,
          name: firebaseUser.displayName,
          image: firebaseUser.photoURL,
          emailVerified: firebaseUser.emailVerified ? new Date() : null,
        },
      })

      // If user has Google provider
      const googleProvider = firebaseUser.providerData.find(
        (p) => p.providerId === 'google.com'
      )

      if (googleProvider) {
        await prisma.account.create({
          data: {
            userId: user.id,
            type: 'oauth',
            provider: 'google',
            providerAccountId: googleProvider.uid,
          },
        })
      }

      console.log(`Migrated: ${firebaseUser.email}`)
    } catch (error) {
      console.error(`Failed: ${firebaseUser.email}`, error)
    }
  }
}

migrateUsers()
```

### 5.2 인증 컴포넌트 변환

```tsx
// Before (Firebase)
import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth'
import { auth } from '@/lib/firebase'

export function LoginPage() {
  const handleGoogleLogin = async () => {
    const provider = new GoogleAuthProvider()
    await signInWithPopup(auth, provider)
  }

  return (
    <button onClick={handleGoogleLogin}>
      Sign in with Google
    </button>
  )
}

// After (NextAuth v5)
// app/(auth)/login/page.tsx
import { signIn } from '@/auth'
import { AuthForm } from '@/components/auth/auth-form'

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-md space-y-4">
        <h1 className="text-2xl font-bold text-center">Sign In</h1>

        {/* OAuth Buttons */}
        <form action={async () => {
          'use server'
          await signIn('google', { redirectTo: '/dashboard' })
        }}>
          <button className="w-full p-3 bg-white border rounded-lg flex items-center justify-center gap-2">
            <GoogleIcon />
            Continue with Google
          </button>
        </form>

        <form action={async () => {
          'use server'
          await signIn('github', { redirectTo: '/dashboard' })
        }}>
          <button className="w-full p-3 bg-gray-900 text-white rounded-lg flex items-center justify-center gap-2">
            <GitHubIcon />
            Continue with GitHub
          </button>
        </form>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-white px-2 text-gray-500">Or</span>
          </div>
        </div>

        {/* Credentials Form */}
        <AuthForm />
      </div>
    </div>
  )
}
```

### 5.3 useAuth 훅 변환

```typescript
// Before (Firebase)
// hooks/useAuth.ts
import { useState, useEffect } from 'react'
import { onAuthStateChanged, User } from 'firebase/auth'
import { auth } from '@/lib/firebase'

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user)
      setLoading(false)
    })
    return unsubscribe
  }, [])

  return { user, loading, isAuthenticated: !!user }
}

// After (NextAuth v5 - Server)
// Server Component에서 직접 사용
import { auth } from '@/auth'

export default async function DashboardPage() {
  const session = await auth()
  // session.user 사용
}

// After (NextAuth v5 - Client)
// hooks/use-auth.ts
'use client'

import { useSession } from 'next-auth/react'

export function useAuth() {
  const { data: session, status } = useSession()

  return {
    user: session?.user,
    loading: status === 'loading',
    isAuthenticated: status === 'authenticated',
  }
}
```

---

## Phase 6: 테스트 및 배포 (2-3일)

### 6.1 테스트 설정

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})

// tests/setup.ts
import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock next/navigation
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
  }),
  usePathname: () => '/',
  useSearchParams: () => new URLSearchParams(),
}))
```

### 6.2 컴포넌트 테스트

```typescript
// tests/components/task-card.test.tsx
import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { TaskCard } from '@/components/task/task-card'

describe('TaskCard', () => {
  it('renders task title', () => {
    const task = {
      id: '1',
      title: 'Test Task',
      description: 'Test Description',
      status: 'pending',
    }

    render(<TaskCard task={task} />)

    expect(screen.getByText('Test Task')).toBeInTheDocument()
    expect(screen.getByText('Test Description')).toBeInTheDocument()
  })
})
```

### 6.3 E2E 테스트 (Playwright)

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('should redirect to login when not authenticated', async ({ page }) => {
    await page.goto('/dashboard')
    await expect(page).toHaveURL('/login')
  })

  test('should login with credentials', async ({ page }) => {
    await page.goto('/login')

    await page.fill('[name="email"]', 'test@example.com')
    await page.fill('[name="password"]', 'password123')
    await page.click('[type="submit"]')

    await expect(page).toHaveURL('/dashboard')
  })
})

// tests/e2e/tasks.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Tasks', () => {
  test.beforeEach(async ({ page }) => {
    // Login first
    await page.goto('/login')
    await page.fill('[name="email"]', 'test@example.com')
    await page.fill('[name="password"]', 'password123')
    await page.click('[type="submit"]')
    await page.waitForURL('/dashboard')
  })

  test('should create a new task', async ({ page }) => {
    await page.goto('/tasks')

    await page.fill('[name="title"]', 'New Test Task')
    await page.click('button[type="submit"]')

    await expect(page.getByText('New Test Task')).toBeVisible()
  })
})
```

### 6.4 배포 체크리스트

```markdown
## Pre-Deployment Checklist

### Environment Variables
- [ ] AUTH_SECRET 설정
- [ ] AUTH_URL 설정 (production URL)
- [ ] DATABASE_URL 설정
- [ ] OAuth provider credentials 설정

### Database
- [ ] Prisma migrate 실행
- [ ] 사용자 데이터 마이그레이션 완료

### Testing
- [ ] Unit tests 통과
- [ ] Integration tests 통과
- [ ] E2E tests 통과
- [ ] 수동 QA 완료

### Performance
- [ ] Lighthouse 점수 확인
- [ ] Core Web Vitals 확인
- [ ] 번들 사이즈 확인

### Security
- [ ] HTTPS 적용
- [ ] CSP 헤더 설정
- [ ] Rate limiting 설정

### Monitoring
- [ ] Error tracking 설정 (Sentry)
- [ ] Analytics 설정
- [ ] Logging 설정
```

### 6.5 Vercel 배포

```bash
# Vercel CLI로 배포
npm i -g vercel
vercel

# 환경변수 설정
vercel env add AUTH_SECRET
vercel env add AUTH_URL
vercel env add DATABASE_URL

# Production 배포
vercel --prod
```

---

## 마이그레이션 타임라인

| Phase | 작업 | 예상 기간 |
|-------|------|----------|
| 0 | 사전 분석 | 1-2일 |
| 1 | 프로젝트 초기화 | 1일 |
| 2 | 라우팅 마이그레이션 | 2-3일 |
| 3 | 컴포넌트 마이그레이션 | 3-4일 |
| 4 | 데이터 페칭 마이그레이션 | 2-3일 |
| 5 | 인증 마이그레이션 | 2-3일 |
| 6 | 테스트 및 배포 | 2-3일 |
| **Total** | | **13-19일** |

---

## 롤백 계획

```bash
# Git 브랜치 전략
main              # 프로덕션 (현재 React 버전)
├── develop       # 개발 브랜치
└── feature/nextjs-migration  # 마이그레이션 작업

# 문제 발생 시 롤백
git checkout main
vercel --prod

# 점진적 롤아웃 (Feature Flag)
# .env
ENABLE_NEXTJS_FEATURES=false
```

---

Version: 1.0.0
Last Updated: 2026-01-22
