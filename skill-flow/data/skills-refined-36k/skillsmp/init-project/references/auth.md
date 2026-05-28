# Authentication Service

A passwordless authentication system using **better-auth** with **Email OTP** and **Effect-TS** integration.

## Libraries

| Package                      | Purpose                                |
| ---------------------------- | -------------------------------------- |
| `better-auth`                | Authentication framework with plugins  |
| `better-auth/client`         | Client-side auth utilities             |
| `better-auth/client/plugins` | Client plugins (emailOTPClient)        |
| `better-auth/next-js`        | Next.js route handler adapter          |
| `better-auth/plugins`        | Server plugins (emailOTP, nextCookies) |
| `@neondatabase/serverless`   | Serverless PostgreSQL driver           |
| `drizzle-orm/neon-http`      | Drizzle adapter for Neon               |
| `effect`                     | Functional programming primitives      |

## File Structure

```
lib/services/auth/
├── index.ts              # Main BetterAuth Effect service
├── auth-client.ts        # Client-side auth client
├── get-session.ts        # Simple session getter (non-Effect)
└── get-session-effect.ts # Effect-wrapped session guards

app/api/auth/
└── [...all]/route.ts     # Catch-all auth API route
```

## Scaffolding from Scratch

### 1. Install Dependencies

```bash
npm install better-auth @neondatabase/serverless drizzle-orm effect
```

### 2. Create Database Schema (`lib/services/db/schema.ts`)

better-auth requires specific table structures:

```typescript
import { pgTable, text, timestamp, boolean } from 'drizzle-orm/pg-core'
import { createId } from '@paralleldrive/cuid2'

export const user = pgTable('user', {
  id: text('id')
    .primaryKey()
    .$defaultFn(() => createId()),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  emailVerified: boolean('emailVerified').notNull().default(false),
  image: text('image'),
  role: text('role', { enum: ['USER', 'ADMIN'] })
    .notNull()
    .default('USER'),
  createdAt: timestamp('createdAt').notNull().defaultNow(),
  updatedAt: timestamp('updatedAt')
    .notNull()
    .defaultNow()
    .$onUpdate(() => new Date())
})

export const session = pgTable('session', {
  id: text('id').primaryKey(),
  expiresAt: timestamp('expiresAt').notNull(),
  token: text('token').notNull().unique(),
  createdAt: timestamp('createdAt').notNull().defaultNow(),
  updatedAt: timestamp('updatedAt')
    .notNull()
    .defaultNow()
    .$onUpdate(() => new Date()),
  ipAddress: text('ipAddress'),
  userAgent: text('userAgent'),
  userId: text('userId')
    .notNull()
    .references(() => user.id, { onDelete: 'cascade' })
})

export const account = pgTable('account', {
  id: text('id').primaryKey(),
  accountId: text('accountId').notNull(),
  providerId: text('providerId').notNull(),
  userId: text('userId')
    .notNull()
    .references(() => user.id, { onDelete: 'cascade' }),
  accessToken: text('accessToken'),
  refreshToken: text('refreshToken'),
  idToken: text('idToken'),
  accessTokenExpiresAt: timestamp('accessTokenExpiresAt'),
  refreshTokenExpiresAt: timestamp('refreshTokenExpiresAt'),
  scope: text('scope'),
  password: text('password'),
  createdAt: timestamp('createdAt').notNull().defaultNow(),
  updatedAt: timestamp('updatedAt')
    .notNull()
    .defaultNow()
    .$onUpdate(() => new Date())
})

export const verification = pgTable('verification', {
  id: text('id').primaryKey(),
  identifier: text('identifier').notNull(),
  value: text('value').notNull(),
  expiresAt: timestamp('expiresAt').notNull(),
  createdAt: timestamp('createdAt').notNull().defaultNow(),
  updatedAt: timestamp('updatedAt')
    .notNull()
    .defaultNow()
    .$onUpdate(() => new Date())
})
```

### 3. Create Tagged Errors (`lib/services/auth/errors.ts`)

```typescript
import { Data } from 'effect'

export class BetterAuthApiError extends Data.TaggedError('BetterAuthApiError')<{
  error: unknown
}> {}

export class BetterAuthConfigError extends Data.TaggedError('BetterAuthConfigError')<{
  message: string
}> {}

export class BetterAuthSessionError extends Data.TaggedError('BetterAuthSessionError')<{
  message: string
}> {}

export class UnauthenticatedError extends Data.TaggedError('UnauthenticatedError')<{
  message: string
}> {}

export class UnauthorizedError extends Data.TaggedError('UnauthorizedError')<{
  message: string
}> {}
```

### 4. Create the Effect Service (`lib/services/auth/index.ts`)

```typescript
import { betterAuth } from 'better-auth'
import { drizzleAdapter } from 'better-auth/adapters/drizzle'
import { emailOTP } from 'better-auth/plugins'
import { nextCookies } from 'better-auth/next-js'
import { neon } from '@neondatabase/serverless'
import { drizzle } from 'drizzle-orm/neon-http'
import { Context, Data, Effect, Layer, Config, Redacted } from 'effect'
import * as schema from '../db/schema'
import { Email } from '../email'

// Database tag for auth (separate from main app DB)
export class AuthDb extends Context.Tag('@app/AuthDb')<AuthDb, ReturnType<typeof drizzle>>() {}

// Auth database layer using Neon HTTP driver
export const AuthDbLive = Layer.effect(
  AuthDb,
  Effect.gen(function* () {
    const url = yield* Config.string('DATABASE_URL')
    const sql = neon(url)
    return drizzle(sql, { schema })
  })
)

// Main BetterAuth service
export class BetterAuth extends Effect.Service<BetterAuth>()('@app/BetterAuth', {
  accessors: true,
  effect: Effect.gen(function* () {
    const authDb = yield* AuthDb
    const emailService = yield* Email

    const auth = betterAuth({
      // Base URL (supports Vercel preview deployments)
      baseURL: process.env.VERCEL_URL
        ? `https://${process.env.VERCEL_URL}`
        : process.env.NEXT_PUBLIC_APP_URL,

      // Trusted origins for CORS
      trustedOrigins: [
        process.env.NEXT_PUBLIC_APP_URL!,
        ...(process.env.VERCEL_BRANCH_URL ? [`https://${process.env.VERCEL_BRANCH_URL}`] : []),
        ...(process.env.VERCEL_URL ? [`https://${process.env.VERCEL_URL}`] : [])
      ],

      // Database adapter
      database: drizzleAdapter(authDb, {
        provider: 'pg',
        schema
      }),

      // Custom user fields
      user: {
        additionalFields: {
          role: {
            type: 'string',
            required: true,
            defaultValue: 'USER',
            input: false // Prevents users from setting their own role
          }
        }
      },

      // Session configuration
      session: {
        expiresIn: 60 * 60 * 24 * 90, // 90 days
        cookieCache: {
          enabled: true,
          maxAge: 5 * 60 // 5 minutes
        }
      },

      // Plugins
      plugins: [
        emailOTP({
          disableSignUp: true, // Invite-only system
          async sendVerificationOTP({ email, otp, type }) {
            if (type !== 'sign-in') return

            await emailService
              .sendEmail({
                from: 'App <login@yourapp.com>',
                to: email,
                subject: 'Your login code',
                html: `Your login code is: <strong>${otp}</strong>`
              })
              .pipe(Effect.runPromise)
          }
        }),
        nextCookies() // Must be last
      ]
    })

    // Wrapper for API calls
    const call = <A>(f: (client: typeof auth, signal: AbortSignal) => Promise<A>) =>
      Effect.tryPromise({
        try: signal => f(auth, signal),
        catch: error => new BetterAuthApiError({ error })
      })

    const signIn = (email: string, password: string) =>
      call(auth => auth.api.signInEmail({ body: { email, password } }))

    const signOut = (headers: Headers = new Headers()) =>
      call(auth => auth.api.signOut({ headers }))

    const getSession = (headers: Headers = new Headers()) =>
      call(auth => auth.api.getSession({ headers }))

    const getSessionFromCookies = () =>
      Effect.gen(function* () {
        const { cookies } = yield* Effect.tryPromise(() => import('next/headers'))
        const cookieStore = yield* Effect.tryPromise(() => cookies())

        const headers = new Headers()
        cookieStore.getAll().forEach((cookie: { name: string; value: string }) => {
          headers.append('cookie', `${cookie.name}=${cookie.value}`)
        })

        return yield* getSession(headers)
      })

    const updateUser = (data: { name?: string; email?: string }) =>
      call(auth => auth.api.updateUser({ body: data }))

    return {
      auth,
      signIn,
      signOut,
      getSession,
      getSessionFromCookies,
      updateUser
    } as const
  })
}) {}
```

### 5. Create Session Helpers (`lib/services/auth/get-session-effect.ts`)

```typescript
import { Effect } from 'effect'
import { cookies } from 'next/headers'
import { BetterAuth, UnauthenticatedError, UnauthorizedError } from '.'

// Basic session guard - requires authentication
export const getSessionEffect = () =>
  Effect.gen(function* () {
    yield* Effect.promise(() => cookies()) // Mark as dynamic

    const authService = yield* BetterAuth
    const session = yield* authService.getSessionFromCookies()

    if (!session) {
      return yield* Effect.fail(new UnauthenticatedError({ message: 'Not authenticated' }))
    }

    return session
  }).pipe(Effect.withSpan('auth.session.get'))

// Admin guard - requires ADMIN role
export const getAdminSession = () =>
  Effect.gen(function* () {
    const authService = yield* BetterAuth
    const session = yield* authService.getSessionFromCookies()

    if (!session) {
      return yield* Effect.fail(new UnauthenticatedError({ message: 'Not authenticated' }))
    }

    if (session.user.role !== 'ADMIN') {
      return yield* Effect.fail(new UnauthorizedError({ message: 'Not authorized' }))
    }

    return session
  }).pipe(Effect.withSpan('auth.session.get-admin'))
```

### 6. Create Simple Session Getter (`lib/services/auth/get-session.ts`)

```typescript
import { Effect } from 'effect'
import { cookies } from 'next/headers'
import { BetterAuth } from '.'
import { AuthLayer } from '@/lib/layers'

export async function getSession() {
  await cookies() // Mark as dynamic

  const result = await Effect.runPromise(
    Effect.gen(function* () {
      const authService = yield* BetterAuth
      return yield* authService.getSessionFromCookies()
    }).pipe(Effect.provide(AuthLayer), Effect.scoped)
  )

  return result
}
```

### 7. Create Client Auth (`lib/services/auth/auth-client.ts`)

```typescript
import { createAuthClient } from 'better-auth/client'
import { emailOTPClient } from 'better-auth/client/plugins'

export const authClient = createAuthClient({
  plugins: [emailOTPClient()]
})
```

### 8. Create API Route (`app/api/auth/[...all]/route.ts`)

```typescript
import { Effect } from 'effect'
import { BetterAuth } from '@/lib/services/auth'
import { AuthLayer } from '@/lib/layers'
import { toNextJsHandler } from 'better-auth/next-js'

async function getAuthHandler() {
  return await Effect.runPromise(
    Effect.gen(function* () {
      const authService = yield* BetterAuth
      return authService.auth
    }).pipe(Effect.provide(AuthLayer), Effect.scoped)
  )
}

export async function GET(request: Request) {
  const auth = await getAuthHandler()
  const handler = toNextJsHandler(auth.handler)
  return handler.GET(request)
}

export async function POST(request: Request) {
  const auth = await getAuthHandler()
  const handler = toNextJsHandler(auth.handler)
  return handler.POST(request)
}
```

### 9. Create Layer Composition (`lib/layers.ts`)

```typescript
import { Layer } from 'effect'
import { BetterAuth, AuthDbLive } from './services/auth'
import { EmailLive } from './services/email'

// Auth layer with all dependencies
export const AuthLayer = Layer.provide(BetterAuth.Default, Layer.merge(AuthDbLive, EmailLive))
```

## Usage Patterns

### Login Form (Client)

```typescript
'use client'

import { authClient } from '@/lib/services/auth/auth-client'
import { useRouter } from 'next/navigation'

export function LoginForm() {
  const router = useRouter()

  const handleSubmit = async (email: string) => {
    const { data, error } = await authClient.emailOtp.sendVerificationOtp({
      email,
      type: 'sign-in'
    })

    if (data?.success) {
      router.push(`/login/otp?email=${encodeURIComponent(email)}`)
    }
  }

  return (/* form JSX */)
}
```

### OTP Verification Form (Client)

```typescript
'use client'

import { authClient } from '@/lib/services/auth/auth-client'

export function OTPForm({ email }: { email: string }) {
  const handleVerify = async (otp: string) => {
    const { error } = await authClient.signIn.emailOtp({ email, otp })

    if (!error) {
      window.location.href = '/dashboard'
    }
  }

  return (/* form JSX */)
}
```

### Logout Button (Client)

```typescript
'use client'

import { authClient } from '@/lib/services/auth/auth-client'

export function LogoutButton() {
  const handleLogout = () => {
    authClient.signOut({
      fetchOptions: {
        onSuccess: () => {
          window.location.href = '/' // Full reload clears cache
        }
      }
    })
  }

  return <button onClick={handleLogout}>Logout</button>
}
```

### Protected Server Action

```typescript
'use server'

import { Effect, Layer, Match } from 'effect'
import { NextEffect } from '@/lib/next-effect'
import { AppLayer } from '@/lib/layers'
import { getSessionEffect, UnauthenticatedError, UnauthorizedError } from '@/lib/services/auth'

export const protectedAction = async (input: string) => {
  return await NextEffect.runPromise(
    Effect.gen(function* () {
      const { user } = yield* getSessionEffect()

      yield* Effect.annotateCurrentSpan({
        'user.id': user.id,
        operation: 'protected.action'
      })

      // ... action logic
      return { success: true }
    }).pipe(
      Effect.withSpan('action.protected'),
      Effect.provide(AppLayer),
      Effect.scoped,
      Effect.matchEffect({
        onFailure: error =>
          Match.value(error._tag).pipe(
            Match.when('UnauthenticatedError', () => NextEffect.redirect('/login')),
            Match.when('UnauthorizedError', () => NextEffect.redirect('/')),
            Match.orElse(() => Effect.succeed({ success: false, error: 'Something went wrong' }))
          ),
        onSuccess: result => Effect.succeed(result)
      })
    )
  )
}
```

### Admin-Only Server Action

```typescript
'use server'

import { getAdminSession } from '@/lib/services/auth'

export const adminAction = async () => {
  return await NextEffect.runPromise(
    Effect.gen(function* () {
      const { user } = yield* getAdminSession()

      // Only ADMIN users reach here
      // ... admin logic
    }).pipe(
      Effect.withSpan('action.admin'),
      Effect.provide(AppLayer),
      Effect.scoped,
      Effect.matchEffect({
        onFailure: error =>
          Match.value(error._tag).pipe(
            Match.when('UnauthenticatedError', () => NextEffect.redirect('/login')),
            Match.when('UnauthorizedError', () => NextEffect.redirect('/')),
            Match.orElse(() => Effect.succeed({ error: 'Failed' }))
          ),
        onSuccess: result => Effect.succeed(result)
      })
    )
  )
}
```

### Resource Access Verification

```typescript
import { Effect } from 'effect'
import { getSessionEffect, UnauthorizedError } from '@/lib/services/auth'
import { DbLive } from '@/lib/services/db'
import { eq } from 'drizzle-orm'
import * as schema from '@/lib/services/db/schema'

export const verifyPostAccess = (postId: string) =>
  Effect.gen(function* () {
    const session = yield* getSessionEffect()
    const db = yield* DbLive

    const post = yield* db.query.post.findFirst({
      where: eq(schema.post.id, postId)
    })

    if (!post) {
      return yield* new PostNotFoundError({ message: 'Post not found', postId })
    }

    // Admin can access any post, users only their own
    if (session.user.role !== 'ADMIN' && post.userId !== session.user.id) {
      return yield* new UnauthorizedError({ message: 'Not authorized' })
    }

    return { post, session }
  }).pipe(Effect.withSpan('post.access.verify'))
```

## Best Practices

### 1. Separate Auth Database Connection

Use a serverless-compatible driver (Neon HTTP) for auth to avoid connection pooling issues:

```typescript
// Auth uses Neon HTTP (stateless)
const sql = neon(url)
const authDb = drizzle(sql, { schema })

// Main app uses Effect SQL (connection pooling)
const db = yield * DbLive
```

### 2. Don't Report Auth Errors to Sentry

`UnauthenticatedError` and `UnauthorizedError` are expected business cases, not bugs:

```typescript
Effect.matchEffect({
  onFailure: error =>
    Match.value(error._tag).pipe(
      Match.when('UnauthenticatedError', () => NextEffect.redirect('/login')),
      Match.when('UnauthorizedError', () => NextEffect.redirect('/')),
      // Only report unexpected errors
      Match.orElse(error => {
        reportError(error)
        return Effect.succeed({ error: 'Failed' })
      })
    )
  // ...
})
```

### 3. Always Annotate Spans with User Context

Add user ID after authentication for tracing:

```typescript
const { user } = yield * getSessionEffect()
yield *
  Effect.annotateCurrentSpan({
    'user.id': user.id,
    'user.role': user.role
  })
```

### 4. Use `input: false` for Sensitive Fields

Prevent users from setting their own role:

```typescript
additionalFields: {
  role: {
    type: 'string',
    defaultValue: 'USER',
    input: false // Cannot be set by user
  }
}
```

### 5. Handle Dynamic URLs for Vercel Deployments

Support preview deployments with dynamic base URLs:

```typescript
baseURL: process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : process.env.NEXT_PUBLIC_APP_URL,

trustedOrigins: [
  process.env.NEXT_PUBLIC_APP_URL!,
  ...(process.env.VERCEL_URL ? [`https://${process.env.VERCEL_URL}`] : [])
]
```

### 6. Use Full Page Reload on Logout

Ensure all client-side caches are cleared:

```typescript
authClient.signOut({
  fetchOptions: {
    onSuccess: () => (window.location.href = '/')
  }
})
```

### 7. Mark Routes as Dynamic

Always access cookies before auth to mark Next.js routes as dynamic:

```typescript
yield * Effect.promise(() => cookies())
const session = yield * authService.getSessionFromCookies()
```

## Environment Variables

| Variable              | Required | Description                           |
| --------------------- | -------- | ------------------------------------- |
| `DATABASE_URL`        | Yes      | PostgreSQL connection string          |
| `NEXT_PUBLIC_APP_URL` | Yes      | Production app URL                    |
| `VERCEL_URL`          | Auto     | Set by Vercel for preview deployments |
| `VERCEL_BRANCH_URL`   | Auto     | Set by Vercel for branch deployments  |

## Adding OAuth Providers

To add OAuth providers (Google, GitHub, etc.), extend the better-auth configuration:

```typescript
import { betterAuth } from 'better-auth'

const auth = betterAuth({
  // ... existing config
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!
    }
  }
})
```

Then use the client:

```typescript
authClient.signIn.social({ provider: 'google' })
```
