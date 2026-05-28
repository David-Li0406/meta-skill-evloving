# Components

## Server Components (`components/server/`)

Async functions that fetch data directly.

```typescript
// features/agents/components/server/agent-header.tsx
import { getAgent } from '@/features/agents/data/get-agent'
import { getTranslations } from 'next-intl/server'

interface AgentHeaderProps {
  agentId: number
}

export async function AgentHeader({ agentId }: AgentHeaderProps) {
  const [agent, t] = await Promise.all([
    getAgent(agentId),
    getTranslations()
  ])

  if (!agent) notFound()

  return (
    <header>
      <h1>{agent.title}</h1>
    </header>
  )
}
```

### Rules
- No `'use client'` directive
- Use `async/await` for data fetching
- Use `getTranslations()` from `next-intl/server`
- Call `notFound()` for missing resources
- File naming: `kebab-case.tsx`

---

## Client Components (`components/client/`)

Handle interactivity and browser APIs.

```typescript
// features/auth/components/client/login-form.tsx
'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'

export function LoginForm() {
  const [email, setEmail] = useState('')
  const t = useTranslations()

  return (
    <form>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <button>{t('log in')}</button>
    </form>
  )
}
```

### Rules
- `'use client'` directive at top of file
- Use `useTranslations()` from `next-intl`
- Handle state and events
- File naming: `kebab-case.tsx`

---

## Skeletons (`components/skeletons/`)

Mirror server component structure for Suspense fallbacks.

```typescript
// features/agents/components/skeletons/agent-header-skeleton.tsx
import { Skeleton } from '@/features/shared/components/ui/skeleton'

export function AgentHeaderSkeleton() {
  return (
    <header className="flex h-14 items-center gap-4 px-4 border-b">
      <Skeleton className="h-4 w-32" />
    </header>
  )
}
```

### Rules
- Match structure of corresponding server component
- Use shared `Skeleton` UI component
- File naming: `{component-name}-skeleton.tsx`

---

## Compound UI Components (`components/ui/{component}/`)

Complex reusable components using the compound pattern.

```typescript
// features/agents/components/ui/prompt-input/prompt-input.tsx
const PromptInputContext = createContext<ContextType | null>(null)

function PromptInputRoot({ children }: Props) {
  return (
    <PromptInputContext.Provider value={...}>
      <div>{children}</div>
    </PromptInputContext.Provider>
  )
}

export const PromptInput = Object.assign(PromptInputRoot, {
  Header: PromptInputHeader,
  Content: PromptInputContent,
  Footer: PromptInputFooter,
})
```

### Usage
```typescript
<PromptInput onSubmit={handleSubmit}>
  <PromptInput.Header />
  <PromptInput.Content placeholder="..." />
  <PromptInput.Footer />
</PromptInput>
```

---

## When to Use Which

| Need | Component Type | Location |
|------|---------------|----------|
| Fetch data | Server | `components/server/` |
| User interaction | Client | `components/client/` |
| Loading state | Skeleton | `components/skeletons/` |
| Complex reusable UI | Compound | `components/ui/` |
