---
name: jikime-migration-patterns-auth
description: Authentication migration patterns for Next.js applications. Covers NextAuth v4→v5, Clerk, Auth0, Firebase Auth, and custom JWT migration.
version: 1.0.0
tags: ["migration", "auth", "nextauth", "clerk", "oauth", "jwt", "security"]
triggers:
  keywords: ["auth migration", "nextauth", "clerk", "auth0", "firebase auth", "인증 마이그레이션"]
  phases: ["run"]
  agents: ["security-auditor", "backend"]
  languages: ["typescript"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2077
type: domain
domain: auth
user-invocable: false
---

# Authentication Migration Patterns

Next.js 애플리케이션의 인증 시스템 마이그레이션 종합 가이드입니다.

## Overview

인증 마이그레이션은 보안에 민감하므로 신중하게 진행해야 합니다. 이 스킬은 다양한 인증 솔루션 간의 마이그레이션 패턴을 제공합니다.

---

## Auth Provider Decision Tree

```
현재 인증 방식은?
│
├─ 커스텀 JWT/Session
│   ├─ 간단한 앱 → NextAuth.js (Auth.js)
│   ├─ 엔터프라이즈 → Auth0
│   └─ 빠른 개발 + 좋은 UX → Clerk
│
├─ NextAuth v4
│   └─ NextAuth v5 (Auth.js) 업그레이드
│
├─ Firebase Auth
│   ├─ Firebase 에코시스템 유지 → Firebase Auth 유지
│   └─ 탈Firebase → NextAuth or Clerk
│
├─ Auth0
│   └─ 대부분 유지 권장 (마이그레이션 비용 높음)
│
└─ Passport.js (Express)
    └─ Next.js 전환 시 → NextAuth.js 권장
```

---

## Quick Comparison

| 솔루션 | 장점 | 단점 | 추천 |
|--------|------|------|------|
| **NextAuth.js v5** | 무료, 유연함, App Router 지원 | 설정 복잡 | 중소규모 앱 |
| **Clerk** | 최고의 DX, 즉시 사용 가능 | 유료 (무료 티어 있음) | 빠른 개발 |
| **Auth0** | 엔터프라이즈급, 규정 준수 | 복잡함, 비용 | 대기업 |
| **Firebase Auth** | Google 통합, 무료 | Firebase 락인 | Google 에코시스템 |

---

## Migration Modules

상세 마이그레이션 가이드는 각 모듈을 참조하세요:

| 모듈 | 파일 | 설명 |
|------|------|------|
| NextAuth v4→v5 | `@modules/nextauth-v5.md` | Auth.js로 리브랜딩, 주요 변경사항 |
| Clerk | `@modules/clerk.md` | Clerk 마이그레이션 및 통합 |
| OAuth Providers | `@modules/oauth-providers.md` | Auth0, Firebase, 소셜 로그인 |

---

## Common Migration Patterns

### 1. Session Structure Migration

```typescript
// Legacy custom session
interface LegacySession {
  user_id: string
  user_name: string
  user_email: string
  expires_at: number
}

// NextAuth v5 session
interface Session {
  user: {
    id: string
    name: string
    email: string
  }
  expires: string  // ISO date string
}

// Migration adapter
function migrateSession(legacy: LegacySession): Session {
  return {
    user: {
      id: legacy.user_id,
      name: legacy.user_name,
      email: legacy.user_email,
    },
    expires: new Date(legacy.expires_at * 1000).toISOString(),
  }
}
```

### 2. Protected Routes Pattern

```typescript
// middleware.ts - Universal pattern for all auth providers
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Auth check function - implement based on provider
async function isAuthenticated(request: NextRequest): Promise<boolean> {
  // NextAuth: Check session token
  const token = request.cookies.get('next-auth.session-token')

  // Clerk: Check clerk session
  // const token = request.cookies.get('__session')

  // Custom JWT: Verify token
  // const token = request.cookies.get('auth-token')

  return !!token
}

export async function middleware(request: NextRequest) {
  const isAuth = await isAuthenticated(request)

  if (!isAuth && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*']
}
```

### 3. User Data Migration

```typescript
// Migration script for user data
import { db } from '@/lib/db'

interface LegacyUser {
  id: string
  email: string
  password_hash: string  // Legacy hashed password
  created_at: Date
}

interface NewUser {
  id: string
  email: string
  emailVerified: Date | null
  accounts: Account[]  // OAuth accounts
}

async function migrateUsers() {
  const legacyUsers = await db.legacyUser.findMany()

  for (const user of legacyUsers) {
    // Create new user
    await db.user.create({
      data: {
        id: user.id,
        email: user.email,
        emailVerified: null,  // Will be verified on first login
      }
    })

    // If keeping password auth, create credentials account
    await db.account.create({
      data: {
        userId: user.id,
        type: 'credentials',
        provider: 'credentials',
        providerAccountId: user.id,
        // Store password hash securely
      }
    })
  }
}
```

---

## Security Checklist

### Pre-Migration

- [ ] Backup all user data and sessions
- [ ] Document current auth flow
- [ ] Identify all protected routes
- [ ] List all OAuth providers in use
- [ ] Check token/session expiration policies

### During Migration

- [ ] Implement parallel auth (old + new)
- [ ] Test with subset of users first
- [ ] Monitor for auth failures
- [ ] Maintain audit logs

### Post-Migration

- [ ] Verify all protected routes work
- [ ] Test OAuth flows (Google, GitHub, etc.)
- [ ] Verify session persistence
- [ ] Check remember me functionality
- [ ] Test password reset flow
- [ ] Verify email verification flow
- [ ] Remove old auth code after full migration

---

## Rollback Strategy

```typescript
// Feature flag for gradual rollout
const useNewAuth = process.env.USE_NEW_AUTH === 'true'

// middleware.ts
export async function middleware(request: NextRequest) {
  if (useNewAuth) {
    return newAuthMiddleware(request)
  }
  return legacyAuthMiddleware(request)
}

// Environment-based rollback
// .env.local
USE_NEW_AUTH=false  // Instant rollback
```

---

## Token Migration Patterns

### JWT to Session-based

```typescript
// Decode existing JWT and create session
import { jwtVerify } from 'jose'

async function migrateJwtToSession(jwt: string) {
  const secret = new TextEncoder().encode(process.env.JWT_SECRET)
  const { payload } = await jwtVerify(jwt, secret)

  // Create new session
  const session = await createSession({
    userId: payload.sub,
    expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),  // 30 days
  })

  return session
}
```

### Session to JWT

```typescript
import { SignJWT } from 'jose'

async function migrateSessionToJwt(sessionId: string) {
  const session = await getSession(sessionId)
  if (!session) return null

  const secret = new TextEncoder().encode(process.env.JWT_SECRET)
  const jwt = await new SignJWT({ sub: session.userId })
    .setProtectedHeader({ alg: 'HS256' })
    .setExpirationTime('30d')
    .sign(secret)

  return jwt
}
```

---

## Database Schema Migration

### Prisma Schema for Auth

```prisma
// NextAuth v5 compatible schema
model User {
  id            String    @id @default(cuid())
  name          String?
  email         String    @unique
  emailVerified DateTime?
  image         String?
  accounts      Account[]
  sessions      Session[]
}

model Account {
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String? @db.Text
  access_token      String? @db.Text
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String? @db.Text
  session_state     String?

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model VerificationToken {
  identifier String
  token      String   @unique
  expires    DateTime

  @@unique([identifier, token])
}
```

---

## Environment Variables Template

```bash
# NextAuth v5 (Auth.js)
AUTH_SECRET=your-secret-key
AUTH_URL=http://localhost:3000
AUTH_TRUST_HOST=true

# OAuth Providers
AUTH_GOOGLE_ID=your-google-client-id
AUTH_GOOGLE_SECRET=your-google-client-secret
AUTH_GITHUB_ID=your-github-client-id
AUTH_GITHUB_SECRET=your-github-client-secret

# Clerk
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Auth0
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
AUTH0_ISSUER=https://your-tenant.auth0.com

# Firebase
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=your-service-account@...
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n..."
```

---

Version: 1.0.0
Last Updated: 2026-01-22
