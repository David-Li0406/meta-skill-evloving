# Clerk Integration & Migration

Clerk로 마이그레이션하거나 통합하는 상세 가이드입니다.

## Overview

Clerk는 가장 현대적인 인증 솔루션으로, 뛰어난 DX와 즉시 사용 가능한 UI 컴포넌트를 제공합니다.

| 장점 | 단점 |
|------|------|
| 최고의 DX | 유료 (무료 티어 10K MAU) |
| Pre-built UI 컴포넌트 | 벤더 락인 |
| App Router 네이티브 지원 | 셀프호스팅 불가 |
| 세션 관리 자동화 | 커스터마이징 제한 |
| WebAuthn/Passkey 지원 | |

---

## Installation

```bash
npm install @clerk/nextjs
```

---

## Configuration

### Environment Variables

```bash
# .env.local
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Optional: Custom URLs
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard
```

### Middleware

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/api/webhook(.*)',
])

export default clerkMiddleware(async (auth, request) => {
  if (!isPublicRoute(request)) {
    await auth.protect()
  }
})

export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/(api|trpc)(.*)',
  ],
}
```

### Layout Provider

```typescript
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  )
}
```

---

## Migration from NextAuth

### Step 1: Session Data Migration

```typescript
// scripts/migrate-users.ts
import { clerkClient } from '@clerk/nextjs/server'
import { prisma } from '@/lib/prisma'

async function migrateUsers() {
  const users = await prisma.user.findMany({
    include: { accounts: true }
  })

  for (const user of users) {
    try {
      // Create user in Clerk
      const clerkUser = await clerkClient.users.createUser({
        emailAddress: [user.email],
        firstName: user.name?.split(' ')[0],
        lastName: user.name?.split(' ').slice(1).join(' '),
        skipPasswordRequirement: true,  // Will send password reset
      })

      // Store mapping for reference
      await prisma.user.update({
        where: { id: user.id },
        data: { clerkId: clerkUser.id }
      })

      console.log(`Migrated: ${user.email}`)
    } catch (error) {
      console.error(`Failed: ${user.email}`, error)
    }
  }
}
```

### Step 2: Replace Auth Hooks

**Before (NextAuth)**:
```typescript
'use client'
import { useSession } from 'next-auth/react'

function Profile() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <div>Loading...</div>
  if (!session) return <div>Not logged in</div>

  return <div>Hello, {session.user.name}</div>
}
```

**After (Clerk)**:
```typescript
'use client'
import { useUser } from '@clerk/nextjs'

function Profile() {
  const { user, isLoaded, isSignedIn } = useUser()

  if (!isLoaded) return <div>Loading...</div>
  if (!isSignedIn) return <div>Not logged in</div>

  return <div>Hello, {user.firstName}</div>
}
```

### Step 3: Replace Server-Side Auth

**Before (NextAuth)**:
```typescript
import { auth } from '@/auth'

async function DashboardPage() {
  const session = await auth()
  if (!session) redirect('/login')

  return <div>Welcome, {session.user.name}</div>
}
```

**After (Clerk)**:
```typescript
import { currentUser } from '@clerk/nextjs/server'
import { redirect } from 'next/navigation'

async function DashboardPage() {
  const user = await currentUser()
  if (!user) redirect('/sign-in')

  return <div>Welcome, {user.firstName}</div>
}
```

---

## Clerk Components

### Pre-built UI

```typescript
// app/sign-in/[[...sign-in]]/page.tsx
import { SignIn } from '@clerk/nextjs'

export default function SignInPage() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <SignIn />
    </div>
  )
}

// app/sign-up/[[...sign-up]]/page.tsx
import { SignUp } from '@clerk/nextjs'

export default function SignUpPage() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <SignUp />
    </div>
  )
}
```

### User Button

```typescript
// components/header.tsx
import { UserButton, SignedIn, SignedOut, SignInButton } from '@clerk/nextjs'

export function Header() {
  return (
    <header className="flex justify-between p-4">
      <h1>My App</h1>
      <div>
        <SignedIn>
          <UserButton afterSignOutUrl="/" />
        </SignedIn>
        <SignedOut>
          <SignInButton mode="modal">
            <button className="btn">Sign In</button>
          </SignInButton>
        </SignedOut>
      </div>
    </header>
  )
}
```

### Custom Sign In Form

```typescript
'use client'

import { useSignIn } from '@clerk/nextjs'
import { useState } from 'react'

export function CustomSignIn() {
  const { signIn, isLoaded, setActive } = useSignIn()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!isLoaded) return

    try {
      const result = await signIn.create({
        identifier: email,
        password,
      })

      if (result.status === 'complete') {
        await setActive({ session: result.createdSessionId })
        window.location.href = '/dashboard'
      }
    } catch (err: any) {
      setError(err.errors?.[0]?.message || 'Sign in failed')
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="text-red-500">{error}</div>}
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Sign In</button>
    </form>
  )
}
```

---

## Database Sync with Webhooks

```typescript
// app/api/webhook/clerk/route.ts
import { Webhook } from 'svix'
import { headers } from 'next/headers'
import { WebhookEvent } from '@clerk/nextjs/server'
import { prisma } from '@/lib/prisma'

export async function POST(req: Request) {
  const WEBHOOK_SECRET = process.env.CLERK_WEBHOOK_SECRET!

  const headerPayload = headers()
  const svix_id = headerPayload.get('svix-id')
  const svix_timestamp = headerPayload.get('svix-timestamp')
  const svix_signature = headerPayload.get('svix-signature')

  if (!svix_id || !svix_timestamp || !svix_signature) {
    return new Response('Missing headers', { status: 400 })
  }

  const payload = await req.json()
  const body = JSON.stringify(payload)

  const wh = new Webhook(WEBHOOK_SECRET)
  let evt: WebhookEvent

  try {
    evt = wh.verify(body, {
      'svix-id': svix_id,
      'svix-timestamp': svix_timestamp,
      'svix-signature': svix_signature,
    }) as WebhookEvent
  } catch (err) {
    return new Response('Invalid signature', { status: 400 })
  }

  const eventType = evt.type

  if (eventType === 'user.created') {
    const { id, email_addresses, first_name, last_name, image_url } = evt.data

    await prisma.user.create({
      data: {
        clerkId: id,
        email: email_addresses[0]?.email_address || '',
        name: `${first_name || ''} ${last_name || ''}`.trim(),
        image: image_url,
      },
    })
  }

  if (eventType === 'user.updated') {
    const { id, email_addresses, first_name, last_name, image_url } = evt.data

    await prisma.user.update({
      where: { clerkId: id },
      data: {
        email: email_addresses[0]?.email_address,
        name: `${first_name || ''} ${last_name || ''}`.trim(),
        image: image_url,
      },
    })
  }

  if (eventType === 'user.deleted') {
    const { id } = evt.data

    await prisma.user.delete({
      where: { clerkId: id },
    })
  }

  return new Response('OK', { status: 200 })
}
```

---

## Server Actions with Clerk

```typescript
// app/actions.ts
'use server'

import { auth, currentUser } from '@clerk/nextjs/server'
import { prisma } from '@/lib/prisma'

export async function createPost(formData: FormData) {
  const { userId } = await auth()

  if (!userId) {
    throw new Error('Unauthorized')
  }

  const title = formData.get('title') as string
  const content = formData.get('content') as string

  const post = await prisma.post.create({
    data: {
      title,
      content,
      authorId: userId,  // Clerk user ID
    },
  })

  return post
}

export async function getUserProfile() {
  const user = await currentUser()

  if (!user) {
    return null
  }

  return {
    id: user.id,
    email: user.emailAddresses[0]?.emailAddress,
    name: `${user.firstName} ${user.lastName}`,
    image: user.imageUrl,
  }
}
```

---

## Migration Checklist

### Setup

- [ ] Install `@clerk/nextjs`
- [ ] Get API keys from Clerk Dashboard
- [ ] Configure environment variables
- [ ] Add middleware
- [ ] Add ClerkProvider to layout

### User Migration

- [ ] Export users from current system
- [ ] Run migration script
- [ ] Verify user data in Clerk Dashboard
- [ ] Set up webhook for sync

### Code Updates

- [ ] Replace `useSession` → `useUser`
- [ ] Replace `getServerSession` → `currentUser` / `auth`
- [ ] Replace login/signup pages with Clerk components
- [ ] Update middleware
- [ ] Update protected routes

### Testing

- [ ] Test sign up flow
- [ ] Test sign in flow
- [ ] Test OAuth (Google, GitHub)
- [ ] Test session persistence
- [ ] Test webhook sync
- [ ] Test protected routes

---

Version: 1.0.0
Last Updated: 2026-01-22
