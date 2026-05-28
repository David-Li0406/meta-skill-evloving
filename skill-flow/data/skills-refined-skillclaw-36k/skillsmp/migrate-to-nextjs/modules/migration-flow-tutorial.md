# Migration Flow Tutorial

React → Next.js 16 마이그레이션의 실제 명령어 사용 흐름을 단계별로 안내합니다.

---

## Quick Start (5분 요약)

```bash
# 1. 분석
/jikime:migrate-1-analyze "./my-react-app"

# 2. 계획 수립
/jikime:migrate-2-plan my-react-app

# 3. 프로젝트별 스킬 생성
/jikime:migrate-2-plan --skill my-react-app

# 4. 마이그레이션 실행
/jikime:migrate-3-execute my-react-app --output ./migrated
```

---

## 예시 프로젝트: TaskFlow

이 튜토리얼에서는 가상의 React CRA 프로젝트 "TaskFlow"를 Next.js 16으로 마이그레이션합니다.

### TaskFlow 프로젝트 구조 (Before)

```
taskflow/
├── public/
│   └── index.html
├── src/
│   ├── index.tsx
│   ├── App.tsx
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   └── TaskForm.tsx
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── DashboardPage.tsx
│   │   └── SettingsPage.tsx
│   ├── hooks/
│   │   └── useTasks.ts
│   ├── store/
│   │   └── taskSlice.ts (Redux)
│   ├── services/
│   │   └── api.ts
│   └── types/
│       └── task.ts
├── package.json
└── tsconfig.json
```

### 기술 스택 (Before)

- React 18.2 + TypeScript
- React Router 6
- Redux Toolkit
- Axios
- styled-components

---

## Phase 0: 사전 분석

### 명령어

```bash
/jikime:migrate-1-analyze "./taskflow"
```

### 실행 결과

Claude가 다음을 수행합니다:

1. **프레임워크 감지**
   ```
   ✅ Framework detected: React CRA (react-scripts)
   ✅ React version: 18.2.0
   ✅ TypeScript: Yes (5.0.4)
   ✅ Router: react-router-dom 6.x
   ✅ State: Redux Toolkit
   ```

2. **파일 분석**
   ```
   📊 Analysis Summary:
   - Total files: 42
   - Components: 12
   - Pages: 3
   - Hooks: 4
   - Services: 2
   - Types: 3
   ```

3. **생성되는 파일**
   ```
   ./migrations/taskflow/
   └── as_is_spec.md    ← 현재 상태 분석 문서
   ```

### as_is_spec.md 예시

```markdown
# TaskFlow AS-IS Specification

## Project Overview
- **Name**: taskflow
- **Framework**: React 18.2.0 (CRA)
- **Language**: TypeScript 5.0.4

## Technology Stack
| Category | Technology | Version |
|----------|------------|---------|
| Framework | React | 18.2.0 |
| Router | react-router-dom | 6.14.1 |
| State | Redux Toolkit | 1.9.5 |
| HTTP | Axios | 1.4.0 |
| Styling | styled-components | 6.0.0 |

## Component Inventory
| Component | Lines | Complexity | Dependencies |
|-----------|-------|------------|--------------|
| Header | 45 | Low | useState |
| TaskList | 120 | Medium | Redux, useTasks |
| TaskItem | 80 | Medium | Redux |
| TaskForm | 150 | High | Redux, Formik |

## Route Structure
| Path | Component | Auth Required |
|------|-----------|---------------|
| / | HomePage | No |
| /dashboard | DashboardPage | Yes |
| /settings | SettingsPage | Yes |

## State Management Analysis
- Global State: Redux Toolkit (taskSlice)
- Local State: useState (forms, UI states)
- Server State: Custom hooks with Axios

## Migration Risks
1. styled-components → Tailwind CSS 전환
2. Redux → Zustand 전환
3. React Router → App Router 전환
```

---

## Phase 1: 마이그레이션 계획

### 명령어

```bash
/jikime:migrate-2-plan taskflow
```

### 실행 결과

Claude가 다음을 수행합니다:

1. **전략 선택**
   - as_is_spec.md 기반으로 최적 전략 결정
   - 컴포넌트 우선순위 결정
   - 리스크 완화 계획 수립

2. **생성되는 파일**
   ```
   ./migrations/taskflow/
   ├── as_is_spec.md
   └── migration_plan.md    ← 마이그레이션 계획서
   ```

### migration_plan.md 예시

```markdown
# TaskFlow Migration Plan

## Strategy: Incremental Migration

### Rationale
- 12개 컴포넌트, 중간 규모
- Redux 의존성이 있어 점진적 전환 필요
- 기존 테스트 코드 활용 가능

## Migration Phases

### Phase 1: Project Setup (Day 1)
- [ ] Next.js 16 프로젝트 생성
- [ ] TypeScript 설정
- [ ] Tailwind CSS 4 설정
- [ ] ESLint/Prettier 설정

### Phase 2: Static Components (Day 2-3)
- [ ] Header.tsx → Server Component
- [ ] TaskItem.tsx → Client Component
- [ ] UI 컴포넌트 (shadcn/ui)

### Phase 3: Pages & Routing (Day 4-5)
- [ ] HomePage → app/page.tsx
- [ ] DashboardPage → app/dashboard/page.tsx
- [ ] SettingsPage → app/settings/page.tsx

### Phase 4: State Migration (Day 6-7)
- [ ] Redux → Zustand 전환
- [ ] useTasks hook 마이그레이션

### Phase 5: API & Data (Day 8-9)
- [ ] Axios → fetch (Server Actions)
- [ ] API routes 구현

### Phase 6: Testing & QA (Day 10)
- [ ] E2E 테스트
- [ ] 성능 테스트
- [ ] 접근성 검사

## Component Priority Matrix

| Component | Priority | Complexity | Dependencies |
|-----------|----------|------------|--------------|
| Header | 1 | Low | None |
| TaskItem | 2 | Medium | None |
| TaskList | 3 | Medium | Zustand |
| TaskForm | 4 | High | Zustand, Zod |
| HomePage | 5 | Low | Header |
| DashboardPage | 6 | High | All |

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| styled-components 전환 | High | Tailwind 병행 운영 후 제거 |
| Redux 의존성 | Medium | Zustand adapter 패턴 사용 |
| 인증 로직 | High | NextAuth v5 사전 설정 |
```

---

## Phase 2: 프로젝트별 스킬 생성

### 명령어

```bash
/jikime:migrate-2-plan --skill taskflow
```

### 실행 결과

Claude가 다음을 수행합니다:

1. **컴포넌트 매핑 규칙 생성**
2. **코딩 컨벤션 정의**
3. **프로젝트별 SKILL.md 생성**

2. **생성되는 파일**
   ```
   ./migrations/taskflow/
   ├── as_is_spec.md
   ├── migration_plan.md
   ├── component_mapping.yaml    ← 컴포넌트 매핑
   └── SKILL.md                  ← 프로젝트별 스킬
   ```

### component_mapping.yaml 예시

```yaml
# TaskFlow Component Mapping Rules
version: "1.0"
project: taskflow
target: nextjs16

component_rules:
  Header:
    source: src/components/Header.tsx
    target: src/components/Header.tsx
    type: server  # Server Component (no state)
    styling: tailwind
    notes: "Convert styled-components to Tailwind"

  TaskList:
    source: src/components/TaskList.tsx
    target: src/components/TaskList.tsx
    type: client  # Client Component ('use client')
    styling: tailwind
    state_migration:
      from: redux (useSelector)
      to: zustand (useTaskStore)
    notes: "Add 'use client' directive"

  TaskItem:
    source: src/components/TaskItem.tsx
    target: src/components/TaskItem.tsx
    type: client
    styling: tailwind
    notes: "Convert onClick handlers"

  TaskForm:
    source: src/components/TaskForm.tsx
    target: src/components/TaskForm.tsx
    type: client
    styling: tailwind
    form_migration:
      from: formik
      to: react-hook-form + zod
    notes: "Use Server Actions for submission"

route_rules:
  HomePage:
    source: src/pages/HomePage.tsx
    target: app/page.tsx
    type: server

  DashboardPage:
    source: src/pages/DashboardPage.tsx
    target: app/dashboard/page.tsx
    type: server
    layout: app/dashboard/layout.tsx
    auth: required

  SettingsPage:
    source: src/pages/SettingsPage.tsx
    target: app/settings/page.tsx
    type: client
    auth: required

state_rules:
  taskSlice:
    source: src/store/taskSlice.ts
    target: src/stores/taskStore.ts
    migration:
      from: "@reduxjs/toolkit"
      to: "zustand"
    selectors:
      - selectTasks → useTaskStore(state => state.tasks)
      - selectLoading → useTaskStore(state => state.loading)
    actions:
      - addTask → actions.addTask
      - removeTask → actions.removeTask
      - toggleTask → actions.toggleTask
```

### SKILL.md (프로젝트별) 예시

```markdown
---
name: taskflow-migration
description: TaskFlow React → Next.js 16 migration rules
version: 1.0.0
---

# TaskFlow Migration Skill

## Coding Conventions

### File Naming
- Components: PascalCase (TaskItem.tsx)
- Hooks: camelCase with 'use' prefix (useTaskStore.ts)
- Utilities: camelCase (formatDate.ts)

### Component Pattern

**Server Component (Default)**
\`\`\`tsx
// No 'use client' directive
import { db } from '@/lib/db'

export default async function TaskList() {
  const tasks = await db.task.findMany()
  return <ul>{/* ... */}</ul>
}
\`\`\`

**Client Component**
\`\`\`tsx
'use client'

import { useTaskStore } from '@/stores/taskStore'

export function TaskItem({ task }: { task: Task }) {
  const { toggleTask } = useTaskStore()
  return <li onClick={() => toggleTask(task.id)}>{/* ... */}</li>
}
\`\`\`

### Styling Rules
- Use Tailwind CSS classes
- Use cn() helper for conditional classes
- shadcn/ui for UI primitives

### State Management
- Global: Zustand (taskStore)
- Server: Server Components + fetch
- Form: react-hook-form + zod

## Import Aliases
\`\`\`json
{
  "@/*": ["src/*"],
  "@/components/*": ["src/components/*"],
  "@/stores/*": ["src/stores/*"],
  "@/lib/*": ["src/lib/*"]
}
\`\`\`
```

---

## Phase 3: 마이그레이션 실행

### 명령어

```bash
/jikime:migrate-3-execute taskflow --output ./migrated
```

### 실행 중 진행 상황

Claude가 각 단계별로 진행합니다:

> 💡 **참고**: 프로젝트 초기화 상세 과정은 `@modules/project-initialization.md` 참조

```
📦 Phase 1: Project Setup
  ✅ npx create-next-app@latest --typescript --tailwind --app --src-dir
  ✅ npx shadcn@latest init (New York style)
  ✅ npx shadcn@latest add button card input form dialog toast
  ✅ npm install zustand react-hook-form zod lucide-react

🔄 Phase 2: Component Migration (6/6)
  ✅ Header.tsx (Server Component)
  ✅ TaskItem.tsx (Client Component)
  ✅ TaskList.tsx (Client Component)
  ✅ TaskForm.tsx (Client Component)
  ✅ Button, Input (shadcn/ui)
  ✅ Card, Dialog (shadcn/ui)

🔄 Phase 3: Page Migration (3/3)
  ✅ app/page.tsx (from HomePage)
  ✅ app/dashboard/page.tsx (from DashboardPage)
  ✅ app/settings/page.tsx (from SettingsPage)

🔄 Phase 4: State Migration
  ✅ taskStore.ts (from Redux slice)
  ✅ Updated all consumers

🔄 Phase 5: API Migration
  ✅ app/api/tasks/route.ts
  ✅ Server Actions for mutations

✅ Migration Complete!
```

### 생성되는 구조

```
./migrated/taskflow/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx              # HomePage
│   │   ├── dashboard/
│   │   │   ├── layout.tsx        # Auth wrapper
│   │   │   └── page.tsx          # DashboardPage
│   │   ├── settings/
│   │   │   └── page.tsx          # SettingsPage
│   │   └── api/
│   │       └── tasks/
│   │           └── route.ts      # API endpoints
│   ├── components/
│   │   ├── ui/                   # shadcn/ui
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   └── input.tsx
│   │   ├── Header.tsx
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   └── TaskForm.tsx
│   ├── stores/
│   │   └── taskStore.ts          # Zustand
│   ├── lib/
│   │   ├── utils.ts
│   │   └── validations.ts
│   └── types/
│       └── task.ts
├── public/
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── next.config.ts
```

---

## Phase 4: 검증 및 테스트

### 빌드 테스트

```bash
cd ./migrated/taskflow
npm install
npm run build
```

### 개발 서버 실행

```bash
npm run dev
```

### 예상 결과

```
▲ Next.js 16.0.0

   - Local:        http://localhost:3000
   - Environments: .env.local

 ✓ Starting...
 ✓ Ready in 1.2s
```

---

## 실제 코드 변환 예시

### Before: Redux Slice

```typescript
// src/store/taskSlice.ts (Before - Redux)
import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface Task {
  id: string
  title: string
  completed: boolean
}

interface TaskState {
  tasks: Task[]
  loading: boolean
}

const initialState: TaskState = {
  tasks: [],
  loading: false,
}

export const taskSlice = createSlice({
  name: 'tasks',
  initialState,
  reducers: {
    addTask: (state, action: PayloadAction<Task>) => {
      state.tasks.push(action.payload)
    },
    toggleTask: (state, action: PayloadAction<string>) => {
      const task = state.tasks.find(t => t.id === action.payload)
      if (task) task.completed = !task.completed
    },
    removeTask: (state, action: PayloadAction<string>) => {
      state.tasks = state.tasks.filter(t => t.id !== action.payload)
    },
  },
})

export const { addTask, toggleTask, removeTask } = taskSlice.actions
```

### After: Zustand Store

```typescript
// src/stores/taskStore.ts (After - Zustand)
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface Task {
  id: string
  title: string
  completed: boolean
}

interface TaskStore {
  tasks: Task[]
  loading: boolean
  addTask: (task: Task) => void
  toggleTask: (id: string) => void
  removeTask: (id: string) => void
}

export const useTaskStore = create<TaskStore>()(
  persist(
    (set) => ({
      tasks: [],
      loading: false,

      addTask: (task) =>
        set((state) => ({
          tasks: [...state.tasks, task],
        })),

      toggleTask: (id) =>
        set((state) => ({
          tasks: state.tasks.map((task) =>
            task.id === id
              ? { ...task, completed: !task.completed }
              : task
          ),
        })),

      removeTask: (id) =>
        set((state) => ({
          tasks: state.tasks.filter((task) => task.id !== id),
        })),
    }),
    {
      name: 'task-storage',
    }
  )
)
```

### Before: React Router Page

```tsx
// src/pages/DashboardPage.tsx (Before)
import { useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import styled from 'styled-components'
import { TaskList } from '../components/TaskList'
import { TaskForm } from '../components/TaskForm'
import { selectTasks } from '../store/taskSlice'

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
`

const Title = styled.h1`
  font-size: 2rem;
  margin-bottom: 1rem;
`

export function DashboardPage() {
  const tasks = useSelector(selectTasks)
  const navigate = useNavigate()

  return (
    <Container>
      <Title>Dashboard</Title>
      <TaskForm />
      <TaskList tasks={tasks} />
    </Container>
  )
}
```

### After: Next.js App Router Page

```tsx
// app/dashboard/page.tsx (After)
import { Suspense } from 'react'
import { TaskList } from '@/components/TaskList'
import { TaskForm } from '@/components/TaskForm'
import { TaskListSkeleton } from '@/components/TaskListSkeleton'

export const metadata = {
  title: 'Dashboard | TaskFlow',
  description: 'Manage your tasks',
}

export default function DashboardPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="mb-6 text-3xl font-bold">Dashboard</h1>

      <TaskForm />

      <Suspense fallback={<TaskListSkeleton />}>
        <TaskList />
      </Suspense>
    </div>
  )
}
```

### Before: Component with styled-components

```tsx
// src/components/TaskItem.tsx (Before)
import { useDispatch } from 'react-redux'
import styled from 'styled-components'
import { toggleTask, removeTask } from '../store/taskSlice'
import type { Task } from '../types/task'

const Item = styled.li<{ $completed: boolean }>`
  display: flex;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #eee;
  text-decoration: ${props => props.$completed ? 'line-through' : 'none'};
  opacity: ${props => props.$completed ? 0.6 : 1};
`

const Checkbox = styled.input`
  margin-right: 1rem;
`

const DeleteButton = styled.button`
  margin-left: auto;
  color: red;
  background: none;
  border: none;
  cursor: pointer;
`

export function TaskItem({ task }: { task: Task }) {
  const dispatch = useDispatch()

  return (
    <Item $completed={task.completed}>
      <Checkbox
        type="checkbox"
        checked={task.completed}
        onChange={() => dispatch(toggleTask(task.id))}
      />
      <span>{task.title}</span>
      <DeleteButton onClick={() => dispatch(removeTask(task.id))}>
        Delete
      </DeleteButton>
    </Item>
  )
}
```

### After: Component with Tailwind + Zustand

```tsx
// src/components/TaskItem.tsx (After)
'use client'

import { useTaskStore } from '@/stores/taskStore'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { cn } from '@/lib/utils'
import type { Task } from '@/types/task'

interface TaskItemProps {
  task: Task
}

export function TaskItem({ task }: TaskItemProps) {
  const { toggleTask, removeTask } = useTaskStore()

  return (
    <li
      className={cn(
        'flex items-center gap-3 border-b p-4',
        task.completed && 'opacity-60'
      )}
    >
      <Checkbox
        checked={task.completed}
        onCheckedChange={() => toggleTask(task.id)}
      />

      <span
        className={cn(
          'flex-1',
          task.completed && 'line-through'
        )}
      >
        {task.title}
      </span>

      <Button
        variant="ghost"
        size="sm"
        onClick={() => removeTask(task.id)}
        className="text-destructive hover:text-destructive"
      >
        Delete
      </Button>
    </li>
  )
}
```

---

## 백서 생성 (선택)

### 사전 분석 백서

클라이언트 제출용 백서가 필요한 경우:

```bash
/jikime:migrate-1-analyze "./taskflow" --whitepaper --client "ABC Corp" --lang ko
```

생성되는 파일:
```
./whitepaper/
├── 00_cover.md                # 표지
├── 01_executive_summary.md    # 경영진 요약
├── 02_feasibility_report.md   # 타당성 보고서
├── 03_architecture_report.md  # 아키텍처 보고서
├── 04_complexity_matrix.md    # 복잡도 매트릭스
├── 05_migration_roadmap.md    # 마이그레이션 로드맵
└── 06_baseline_report.md      # 보안/성능 기준선
```

### 완료 보고서

마이그레이션 완료 후:

```bash
/jikime:migrate-3-execute taskflow --whitepaper-report --client "ABC Corp"
```

생성되는 파일:
```
./whitepaper-report/
├── 00_cover.md                    # 핵심 성과 요약
├── 01_executive_summary.md        # 경영진 보고
├── 02_performance_comparison.md   # Before/After 성능
├── 03_security_improvement.md     # 보안 개선
├── 04_code_quality_report.md      # 코드 품질
├── 05_architecture_evolution.md   # 아키텍처 진화
├── 06_cost_benefit_analysis.md    # ROI 분석
└── 07_maintenance_guide.md        # 유지보수 가이드
```

---

## Troubleshooting

### 자주 발생하는 문제

#### 1. TypeScript 타입 에러

```
Error: Type 'string' is not assignable to type 'Task'
```

**해결**: 타입 정의 확인 및 import 경로 수정
```bash
# 타입 파일 위치 확인
ls src/types/
```

#### 2. 'use client' 누락

```
Error: useState only works in Client Components
```

**해결**: 파일 최상단에 'use client' 추가
```tsx
'use client'  // ← 추가

import { useState } from 'react'
```

#### 3. 이미지 최적화 에러

```
Error: Invalid src prop on next/image
```

**해결**: next.config.ts에 도메인 추가
```typescript
// next.config.ts
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
      },
    ],
  },
}
```

#### 4. 환경변수 미인식

```
Error: process.env.REACT_APP_API_URL is undefined
```

**해결**: 환경변수 이름 변경
```bash
# Before (CRA)
REACT_APP_API_URL=...

# After (Next.js)
NEXT_PUBLIC_API_URL=...
```

#### 5. Hydration 에러

```
Error: Hydration failed because the initial UI does not match
```

**해결**: 서버/클라이언트 불일치 수정
```tsx
'use client'

import { useEffect, useState } from 'react'

export function ClientOnlyComponent() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return <div>Client-only content</div>
}
```

---

## 명령어 요약

| 단계 | 명령어 | 설명 |
|------|--------|------|
| 분석 | `/jikime:migrate-1-analyze "./path"` | AS-IS 분석 |
| 계획 | `/jikime:migrate-2-plan {name}` | 마이그레이션 계획 |
| 스킬 | `/jikime:migrate-2-plan --skill {name}` | 프로젝트별 규칙 생성 |
| 실행 | `/jikime:migrate-3-execute {name}` | 마이그레이션 수행 |
| 백서 | `--whitepaper --client "Name"` | 사전 분석 백서 |
| 보고 | `--whitepaper-report --client "Name"` | 완료 보고서 |

---

## 다음 단계

마이그레이션 완료 후:

1. **E2E 테스트 작성**
   ```bash
   npm install -D @playwright/test
   npx playwright test
   ```

2. **성능 최적화**
   ```bash
   npm run build
   npx next-bundle-analyzer
   ```

3. **배포**
   ```bash
   # Vercel 배포
   npx vercel
   ```

---

Version: 1.0.0
Last Updated: 2026-01-22
