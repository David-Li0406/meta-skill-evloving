# OAuth Providers Migration

Auth0, Firebase Auth, 소셜 로그인 프로바이더 마이그레이션 가이드입니다.

---

## Auth0

### Overview

Auth0는 엔터프라이즈급 인증 솔루션으로, 규정 준수가 필요한 대기업에 적합합니다.

### Installation

```bash
npm install @auth0/nextjs-auth0
```

### Configuration

```bash
# .env.local
AUTH0_SECRET='use-openssl-rand-base64-32'
AUTH0_BASE_URL='http://localhost:3000'
AUTH0_ISSUER_BASE_URL='https://YOUR_DOMAIN.auth0.com'
AUTH0_CLIENT_ID='YOUR_CLIENT_ID'
AUTH0_CLIENT_SECRET='YOUR_CLIENT_SECRET'
```

### App Router Integration

```typescript
// app/api/auth/[auth0]/route.ts
import { handleAuth } from '@auth0/nextjs-auth0'

export const GET = handleAuth()

// Customized handlers
export const GET = handleAuth({
  login: handleLogin({
    authorizationParams: {
      audience: 'https://api.example.com',
      scope: 'openid profile email read:products'
    }
  }),
  callback: handleCallback({
    afterCallback: async (req, session) => {
      // Custom logic after login
      return session
    }
  }),
  logout: handleLogout({
    returnTo: '/'
  })
})
```

### Middleware

```typescript
// middleware.ts
import { withMiddlewareAuthRequired } from '@auth0/nextjs-auth0/edge'

export default withMiddlewareAuthRequired()

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*']
}
```

### Server Component

```typescript
// app/dashboard/page.tsx
import { getSession } from '@auth0/nextjs-auth0'

export default async function DashboardPage() {
  const session = await getSession()

  if (!session) {
    redirect('/api/auth/login')
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session.user.name}</p>
      <img src={session.user.picture} alt="Profile" />
      <a href="/api/auth/logout">Logout</a>
    </div>
  )
}
```

### Client Component

```typescript
'use client'

import { useUser } from '@auth0/nextjs-auth0/client'

export function Profile() {
  const { user, error, isLoading } = useUser()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>{error.message}</div>

  if (user) {
    return (
      <div>
        <img src={user.picture} alt={user.name} />
        <h2>{user.name}</h2>
        <p>{user.email}</p>
      </div>
    )
  }

  return <a href="/api/auth/login">Login</a>
}
```

### Migration from Auth0 to NextAuth

```typescript
// auth.ts - NextAuth with Auth0 provider
import NextAuth from 'next-auth'
import Auth0Provider from 'next-auth/providers/auth0'

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Auth0Provider({
      clientId: process.env.AUTH0_CLIENT_ID!,
      clientSecret: process.env.AUTH0_CLIENT_SECRET!,
      issuer: process.env.AUTH0_ISSUER!,
    }),
  ],
})
```

---

## Firebase Auth

### Installation

```bash
npm install firebase firebase-admin
```

### Configuration

```typescript
// lib/firebase/client.ts
import { initializeApp, getApps } from 'firebase/app'
import { getAuth } from 'firebase/auth'

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
}

export const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0]
export const auth = getAuth(app)

// lib/firebase/admin.ts
import { initializeApp, getApps, cert } from 'firebase-admin/app'
import { getAuth } from 'firebase-admin/auth'

const adminApp = getApps().length === 0
  ? initializeApp({
      credential: cert({
        projectId: process.env.FIREBASE_PROJECT_ID,
        clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
        privateKey: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, '\n'),
      }),
    })
  : getApps()[0]

export const adminAuth = getAuth(adminApp)
```

### Client-Side Auth

```typescript
'use client'

import { auth } from '@/lib/firebase/client'
import {
  signInWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  User
} from 'firebase/auth'
import { useState, useEffect, createContext, useContext } from 'react'

// Auth Context
const AuthContext = createContext<{
  user: User | null
  loading: boolean
}>({ user: null, loading: true })

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user)
      setLoading(false)
    })
    return unsubscribe
  }, [])

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)

// Sign in functions
export async function signInWithEmail(email: string, password: string) {
  return signInWithEmailAndPassword(auth, email, password)
}

export async function signInWithGoogle() {
  const provider = new GoogleAuthProvider()
  return signInWithPopup(auth, provider)
}

export async function signOut() {
  return firebaseSignOut(auth)
}
```

### Server-Side Verification

```typescript
// app/api/protected/route.ts
import { adminAuth } from '@/lib/firebase/admin'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET() {
  const cookieStore = cookies()
  const token = cookieStore.get('firebase-token')?.value

  if (!token) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  try {
    const decodedToken = await adminAuth.verifyIdToken(token)
    return NextResponse.json({ uid: decodedToken.uid })
  } catch (error) {
    return NextResponse.json({ error: 'Invalid token' }, { status: 401 })
  }
}
```

### Session Cookie Pattern

```typescript
// app/api/auth/session/route.ts
import { adminAuth } from '@/lib/firebase/admin'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const { idToken } = await req.json()

  const expiresIn = 60 * 60 * 24 * 5 * 1000  // 5 days

  try {
    const sessionCookie = await adminAuth.createSessionCookie(idToken, { expiresIn })

    cookies().set('firebase-session', sessionCookie, {
      maxAge: expiresIn / 1000,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
    })

    return NextResponse.json({ status: 'success' })
  } catch (error) {
    return NextResponse.json({ error: 'Failed to create session' }, { status: 401 })
  }
}

export async function DELETE() {
  cookies().delete('firebase-session')
  return NextResponse.json({ status: 'success' })
}
```

### Migration from Firebase to NextAuth

```typescript
// auth.ts
import NextAuth from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import { FirestoreAdapter } from '@auth/firebase-adapter'
import { cert } from 'firebase-admin/app'

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: FirestoreAdapter({
    credential: cert({
      projectId: process.env.FIREBASE_PROJECT_ID,
      clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
      privateKey: process.env.FIREBASE_PRIVATE_KEY,
    }),
  }),
  providers: [GoogleProvider],
})
```

---

## Social Login Providers

### Google OAuth

```typescript
// NextAuth
import Google from 'next-auth/providers/google'

providers: [
  Google({
    clientId: process.env.AUTH_GOOGLE_ID,
    clientSecret: process.env.AUTH_GOOGLE_SECRET,
    authorization: {
      params: {
        prompt: 'consent',
        access_type: 'offline',
        response_type: 'code'
      }
    }
  })
]
```

### GitHub OAuth

```typescript
import GitHub from 'next-auth/providers/github'

providers: [
  GitHub({
    clientId: process.env.AUTH_GITHUB_ID,
    clientSecret: process.env.AUTH_GITHUB_SECRET,
  })
]
```

### Apple Sign In

```typescript
import Apple from 'next-auth/providers/apple'

providers: [
  Apple({
    clientId: process.env.AUTH_APPLE_ID,
    clientSecret: process.env.AUTH_APPLE_SECRET,  // Generated JWT
  })
]
```

### Discord OAuth

```typescript
import Discord from 'next-auth/providers/discord'

providers: [
  Discord({
    clientId: process.env.AUTH_DISCORD_ID,
    clientSecret: process.env.AUTH_DISCORD_SECRET,
  })
]
```

---

## Migration Strategies

### Parallel Auth (Gradual Migration)

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  // Check new auth first
  const newAuthToken = request.cookies.get('new-auth-token')
  if (newAuthToken) {
    // Verify with new auth system
    const isValid = await verifyNewAuth(newAuthToken.value)
    if (isValid) return NextResponse.next()
  }

  // Fall back to old auth
  const oldAuthToken = request.cookies.get('old-auth-token')
  if (oldAuthToken) {
    const isValid = await verifyOldAuth(oldAuthToken.value)
    if (isValid) {
      // Optionally migrate to new auth
      const response = NextResponse.next()
      response.cookies.set('migrate-auth', 'true')
      return response
    }
  }

  // Not authenticated
  return NextResponse.redirect(new URL('/login', request.url))
}
```

### Token Migration Script

```typescript
// scripts/migrate-tokens.ts
import { prisma } from '@/lib/prisma'
import { adminAuth } from '@/lib/firebase/admin'

async function migrateFirebaseUsers() {
  // List all Firebase users
  const listUsersResult = await adminAuth.listUsers(1000)

  for (const firebaseUser of listUsersResult.users) {
    // Create in new system
    await prisma.user.upsert({
      where: { email: firebaseUser.email || '' },
      update: {
        firebaseUid: firebaseUser.uid,
        emailVerified: firebaseUser.emailVerified ? new Date() : null,
      },
      create: {
        email: firebaseUser.email || '',
        name: firebaseUser.displayName,
        image: firebaseUser.photoURL,
        firebaseUid: firebaseUser.uid,
        emailVerified: firebaseUser.emailVerified ? new Date() : null,
      },
    })

    console.log(`Migrated: ${firebaseUser.email}`)
  }
}
```

---

## Common Issues & Solutions

### CORS Errors

```typescript
// next.config.ts
const nextConfig = {
  async headers() {
    return [
      {
        source: '/api/auth/:path*',
        headers: [
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
          { key: 'Access-Control-Allow-Origin', value: 'https://yourdomain.com' },
        ],
      },
    ]
  },
}
```

### Callback URL Mismatch

```bash
# Ensure these match in provider dashboard
# Development
http://localhost:3000/api/auth/callback/google

# Production
https://yourdomain.com/api/auth/callback/google
```

### Token Refresh Issues

```typescript
// auth.ts
callbacks: {
  async jwt({ token, account }) {
    if (account) {
      token.accessToken = account.access_token
      token.refreshToken = account.refresh_token
      token.expiresAt = account.expires_at
    }

    // Return previous token if not expired
    if (Date.now() < (token.expiresAt as number) * 1000) {
      return token
    }

    // Refresh token
    return refreshAccessToken(token)
  },
}

async function refreshAccessToken(token: JWT) {
  try {
    const response = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        client_id: process.env.AUTH_GOOGLE_ID!,
        client_secret: process.env.AUTH_GOOGLE_SECRET!,
        grant_type: 'refresh_token',
        refresh_token: token.refreshToken as string,
      }),
    })

    const refreshedTokens = await response.json()

    return {
      ...token,
      accessToken: refreshedTokens.access_token,
      expiresAt: Math.floor(Date.now() / 1000 + refreshedTokens.expires_in),
      refreshToken: refreshedTokens.refresh_token ?? token.refreshToken,
    }
  } catch (error) {
    return { ...token, error: 'RefreshAccessTokenError' }
  }
}
```

---

Version: 1.0.0
Last Updated: 2026-01-22
