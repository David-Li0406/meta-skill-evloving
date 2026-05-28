# NextAuth v4 → v5 (Auth.js) Migration

NextAuth.js v4에서 v5 (Auth.js)로 마이그레이션하는 상세 가이드입니다.

## Overview

NextAuth.js v5는 "Auth.js"로 리브랜딩되었으며, Next.js App Router를 네이티브로 지원합니다.

| 항목 | v4 | v5 |
|------|-----|-----|
| 패키지명 | `next-auth` | `next-auth@beta` (or `@auth/nextjs`) |
| Config 위치 | `pages/api/auth/[...nextauth].ts` | `auth.ts` (root) |
| 환경변수 | `NEXTAUTH_*` | `AUTH_*` |
| App Router | 부분 지원 | 네이티브 지원 |

---

## Breaking Changes

### 1. Configuration File Location

**Before (v4)**:
```typescript
// pages/api/auth/[...nextauth].ts
import NextAuth from 'next-auth'

export default NextAuth({
  providers: [...],
  callbacks: {...},
})
```

**After (v5)**:
```typescript
// auth.ts (project root)
import NextAuth from 'next-auth'
import Google from 'next-auth/providers/google'
import GitHub from 'next-auth/providers/github'

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [Google, GitHub],
  callbacks: {...},
})

// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth'
export const { GET, POST } = handlers
```

### 2. Environment Variables

**Before (v4)**:
```bash
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret

GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

**After (v5)**:
```bash
AUTH_URL=http://localhost:3000
AUTH_SECRET=your-secret
AUTH_TRUST_HOST=true

AUTH_GOOGLE_ID=...
AUTH_GOOGLE_SECRET=...
```

### 3. Provider Configuration

**Before (v4)**:
```typescript
import GoogleProvider from 'next-auth/providers/google'

providers: [
  GoogleProvider({
    clientId: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  }),
]
```

**After (v5)**:
```typescript
import Google from 'next-auth/providers/google'

providers: [
  Google,  // Auto-reads AUTH_GOOGLE_ID and AUTH_GOOGLE_SECRET
]

// Or with custom config
providers: [
  Google({
    clientId: process.env.AUTH_GOOGLE_ID,
    clientSecret: process.env.AUTH_GOOGLE_SECRET,
    authorization: {
      params: { scope: 'openid email profile' }
    }
  }),
]
```

### 4. Getting Session

**Before (v4) - Client**:
```typescript
'use client'
import { useSession } from 'next-auth/react'

function Component() {
  const { data: session, status } = useSession()
  if (status === 'loading') return <div>Loading...</div>
  if (!session) return <div>Not authenticated</div>
  return <div>Hello, {session.user.name}</div>
}
```

**After (v5) - Server Component**:
```typescript
// Server Component (recommended)
import { auth } from '@/auth'

async function Component() {
  const session = await auth()
  if (!session) return <div>Not authenticated</div>
  return <div>Hello, {session.user.name}</div>
}
```

**After (v5) - Client Component**:
```typescript
'use client'
import { useSession } from 'next-auth/react'

function Component() {
  const { data: session, status } = useSession()
  // Same as v4
}

// Don't forget SessionProvider in layout
// app/layout.tsx
import { SessionProvider } from 'next-auth/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <SessionProvider>{children}</SessionProvider>
      </body>
    </html>
  )
}
```

### 5. Middleware

**Before (v4)**:
```typescript
// middleware.ts
export { default } from 'next-auth/middleware'

export const config = {
  matcher: ['/dashboard/:path*']
}
```

**After (v5)**:
```typescript
// middleware.ts
import { auth } from '@/auth'

export default auth((req) => {
  if (!req.auth && req.nextUrl.pathname.startsWith('/dashboard')) {
    const newUrl = new URL('/login', req.nextUrl.origin)
    return Response.redirect(newUrl)
  }
})

export const config = {
  matcher: ['/dashboard/:path*']
}
```

### 6. Sign In / Sign Out

**Before (v4)**:
```typescript
import { signIn, signOut } from 'next-auth/react'

// Client-side only
<button onClick={() => signIn('google')}>Sign in</button>
<button onClick={() => signOut()}>Sign out</button>
```

**After (v5)**:
```typescript
// Server Action (recommended)
import { signIn, signOut } from '@/auth'

// In Server Component or Server Action
export async function LoginButton() {
  return (
    <form action={async () => {
      'use server'
      await signIn('google')
    }}>
      <button type="submit">Sign in with Google</button>
    </form>
  )
}

// Or use the client-side imports for compatibility
'use client'
import { signIn, signOut } from 'next-auth/react'
```

---

## Full Migration Example

### auth.ts

```typescript
// auth.ts
import NextAuth from 'next-auth'
import Google from 'next-auth/providers/google'
import GitHub from 'next-auth/providers/github'
import Credentials from 'next-auth/providers/credentials'
import { PrismaAdapter } from '@auth/prisma-adapter'
import { prisma } from '@/lib/prisma'
import bcrypt from 'bcryptjs'

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: 'jwt' },
  providers: [
    Google,
    GitHub,
    Credentials({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null
        }

        const user = await prisma.user.findUnique({
          where: { email: credentials.email as string }
        })

        if (!user || !user.password) {
          return null
        }

        const isValid = await bcrypt.compare(
          credentials.password as string,
          user.password
        )

        if (!isValid) {
          return null
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name,
        }
      },
    }),
  ],
  callbacks: {
    async session({ session, token }) {
      if (token.sub) {
        session.user.id = token.sub
      }
      return session
    },
    async jwt({ token, user }) {
      if (user) {
        token.sub = user.id
      }
      return token
    },
  },
  pages: {
    signIn: '/login',
    error: '/auth/error',
  },
})
```

### API Route

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth'

export const { GET, POST } = handlers
```

### Middleware

```typescript
// middleware.ts
import { auth } from '@/auth'
import { NextResponse } from 'next/server'

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isOnDashboard = req.nextUrl.pathname.startsWith('/dashboard')
  const isOnLogin = req.nextUrl.pathname === '/login'

  if (isOnDashboard && !isLoggedIn) {
    return NextResponse.redirect(new URL('/login', req.url))
  }

  if (isOnLogin && isLoggedIn) {
    return NextResponse.redirect(new URL('/dashboard', req.url))
  }

  return NextResponse.next()
})

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
}
```

### Login Page

```typescript
// app/login/page.tsx
import { signIn } from '@/auth'

export default function LoginPage() {
  return (
    <div className="flex flex-col gap-4 max-w-md mx-auto mt-20">
      <h1 className="text-2xl font-bold">Sign In</h1>

      {/* OAuth Buttons */}
      <form action={async () => {
        'use server'
        await signIn('google', { redirectTo: '/dashboard' })
      }}>
        <button type="submit" className="w-full p-2 bg-blue-500 text-white rounded">
          Sign in with Google
        </button>
      </form>

      <form action={async () => {
        'use server'
        await signIn('github', { redirectTo: '/dashboard' })
      }}>
        <button type="submit" className="w-full p-2 bg-gray-800 text-white rounded">
          Sign in with GitHub
        </button>
      </form>

      {/* Credentials Form */}
      <form action={async (formData) => {
        'use server'
        await signIn('credentials', {
          email: formData.get('email'),
          password: formData.get('password'),
          redirectTo: '/dashboard',
        })
      }}>
        <input name="email" type="email" placeholder="Email" className="w-full p-2 border rounded mb-2" />
        <input name="password" type="password" placeholder="Password" className="w-full p-2 border rounded mb-2" />
        <button type="submit" className="w-full p-2 bg-green-500 text-white rounded">
          Sign in with Email
        </button>
      </form>
    </div>
  )
}
```

### Protected Page

```typescript
// app/dashboard/page.tsx
import { auth, signOut } from '@/auth'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const session = await auth()

  if (!session) {
    redirect('/login')
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session.user.name}!</p>
      <p>Email: {session.user.email}</p>

      <form action={async () => {
        'use server'
        await signOut({ redirectTo: '/' })
      }}>
        <button type="submit">Sign Out</button>
      </form>
    </div>
  )
}
```

---

## Migration Checklist

### Configuration

- [ ] Create `auth.ts` in project root
- [ ] Move providers to new format
- [ ] Update environment variables (`NEXTAUTH_*` → `AUTH_*`)
- [ ] Create `app/api/auth/[...nextauth]/route.ts`

### Code Updates

- [ ] Replace `getServerSession` with `auth()`
- [ ] Update middleware to use `auth()` callback
- [ ] Convert `signIn`/`signOut` to Server Actions
- [ ] Add `SessionProvider` to layout if using client components

### Testing

- [ ] Test OAuth flows (Google, GitHub, etc.)
- [ ] Test credentials login
- [ ] Test session persistence
- [ ] Test protected routes
- [ ] Test sign out flow

---

## Troubleshooting

### "AUTH_SECRET is missing"

```bash
# Generate a new secret
openssl rand -base64 32

# Add to .env.local
AUTH_SECRET=your-generated-secret
```

### OAuth Callback Error

```typescript
// Ensure AUTH_URL is set correctly
AUTH_URL=http://localhost:3000  // Development
AUTH_URL=https://yourdomain.com  // Production

// Or set AUTH_TRUST_HOST
AUTH_TRUST_HOST=true
```

### Session Not Persisting

```typescript
// Ensure you're using the correct session strategy
export const { ... } = NextAuth({
  session: { strategy: 'jwt' },  // or 'database'
  // ...
})
```

---

Version: 1.0.0
Last Updated: 2026-01-22
