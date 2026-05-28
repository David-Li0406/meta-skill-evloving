# Pages & Layouts

## Route Groups

```
app/[locale]/
├── (app)/            # Authenticated application
├── (auth)/           # Authentication pages
└── (marketing)/      # Public marketing pages
```

---

## Page Template

```typescript
// app/[locale]/(app)/agents/[id]/page.tsx
import { Suspense } from 'react'
import { setRequestLocale } from 'next-intl/server'
import { AgentHeader } from '@/features/agents/components/server/agent-header'
import { AgentMessages } from '@/features/agents/components/server/agent-messages'
import { AgentHeaderSkeleton } from '@/features/agents/components/skeletons/agent-header-skeleton'
import { AgentMessagesSkeleton } from '@/features/agents/components/skeletons/agent-messages-skeleton'

interface Props {
  params: Promise<{ locale: string; id: string }>
}

export default async function AgentPage({ params }: Props) {
  const { locale, id } = await params
  setRequestLocale(locale)

  return (
    <>
      <Suspense fallback={<AgentHeaderSkeleton />}>
        <AgentHeader agentId={Number(id)} />
      </Suspense>
      <Suspense fallback={<AgentMessagesSkeleton />}>
        <AgentMessages agentId={Number(id)} />
      </Suspense>
    </>
  )
}
```

---

## Layout Template

```typescript
// app/[locale]/(app)/layout.tsx
import { setRequestLocale } from 'next-intl/server'
import { AnonymousAuthProvider } from '@/features/auth/components/client/anonymous-provider'
import { AppLayout } from '@/features/shared/components/layouts/app-layout/app-layout'

interface Props {
  children: React.ReactNode
  params: Promise<{ locale: string }>
}

export default async function Layout({ children, params }: Props) {
  const { locale } = await params
  setRequestLocale(locale)

  return (
    <AnonymousAuthProvider>
      <AppLayout>{children}</AppLayout>
    </AnonymousAuthProvider>
  )
}
```

---

## Metadata with Translations

```typescript
import { getTranslations } from 'next-intl/server'
import type { Metadata } from 'next'

interface Props {
  params: Promise<{ locale: string }>
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params
  const t = await getTranslations({ locale })

  return {
    title: t('page title'),
    description: t('page description')
  }
}
```

---

## Rules

### Params Are Async
In Next.js 16, `params` is a Promise:
```typescript
// ✅ Correct
const { locale, id } = await params

// ❌ Wrong
const { locale, id } = params
```

### Always Call setRequestLocale
Every page and layout must call `setRequestLocale(locale)`:
```typescript
export default async function Page({ params }: Props) {
  const { locale } = await params
  setRequestLocale(locale)  // Required for static rendering
  // ...
}
```

### Suspense Boundaries in Pages
- Wrap server components in Suspense
- Use matching skeleton fallbacks
- Pages compose features; features don't know about pages

### Route Group Organization
| Group | Purpose | Auth |
|-------|---------|------|
| `(app)` | Main application | Required |
| `(auth)` | Login, register, etc. | None |
| `(marketing)` | Landing, pricing, etc. | None |
