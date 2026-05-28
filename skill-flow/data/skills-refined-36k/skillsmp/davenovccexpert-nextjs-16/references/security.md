<overview>
Security best practices for Next.js 16 applications. Covers authentication, input validation, headers, and common vulnerabilities.
</overview>

<key_cves>
**Recent CVEs addressed in Next.js 16:**

<cve name="CVE-2025-29927">
**Issue:** Middleware authentication bypass under load
**Impact:** Auth checks in middleware could be skipped
**Fix:** Don't rely on middleware/proxy for auth. Use Data Access Layer.
</cve>

<cve name="CVE-2025-55182">
**Issue:** RSC Flight protocol deserialization RCE
**Impact:** Unauthenticated remote code execution
**Fix:** Upgrade to Next.js 16.1+ (automatically patched)
</cve>

<cve name="CVE-2025-66478">
**Issue:** Related RSC deserialization vulnerability
**Impact:** RCE via crafted payloads
**Fix:** Upgrade to Next.js 16.1+ (automatically patched)
</cve>

**Check for vulnerabilities:**
```bash
npm audit
npm audit fix
```
</key_cves>

<authentication>
**Auth must happen in Data Access Layer, NOT proxy:**

```typescript
// lib/dal.ts
export async function getUser() {
  const cookieStore = await cookies()
  const session = cookieStore.get('session')

  if (!session) return null

  // Validate HERE, not in proxy
  const user = await verifyJWT(session.value)
  return user
}

export async function requireAuth() {
  const user = await getUser()
  if (!user) redirect('/login')
  return user
}
```

**Every Server Action must verify auth:**
```typescript
'use server'

export async function sensitiveAction(data: FormData) {
  const user = await requireAuth()  // REQUIRED

  // Then proceed...
}
```
</authentication>

<input_validation>
**Never trust client input:**

```typescript
'use server'

import { z } from 'zod'

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  // Don't allow client to set role!
})

export async function createUser(formData: FormData) {
  const user = await requireAuth()

  const parsed = CreateUserSchema.safeParse({
    email: formData.get('email'),
    name: formData.get('name'),
  })

  if (!parsed.success) {
    return { error: parsed.error.flatten() }
  }

  // Safe to use parsed.data
  await db.users.create({
    data: {
      ...parsed.data,
      role: 'user',  // Set role on server, not from input
    }
  })
}
```

**SQL Injection prevention:**
```typescript
// BAD - vulnerable to SQL injection
const user = await db.$queryRaw`SELECT * FROM users WHERE id = ${userId}`

// GOOD - parameterized query (Prisma does this automatically)
const user = await db.users.findUnique({ where: { id: userId } })
```
</input_validation>

<security_headers>
**Configure security headers:**

```typescript
// next.config.ts
const nextConfig = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
        ],
      },
    ]
  },
}
```

**Content Security Policy:**
```typescript
{
  key: 'Content-Security-Policy',
  value: `
    default-src 'self';
    script-src 'self' 'unsafe-inline' 'unsafe-eval';
    style-src 'self' 'unsafe-inline';
    img-src 'self' data: https:;
    font-src 'self';
    connect-src 'self' https://api.example.com;
    frame-ancestors 'none';
  `.replace(/\n/g, ''),
}
```

**For stricter CSP (requires nonce):**
```tsx
// app/layout.tsx
import { headers } from 'next/headers'

export default async function Layout({ children }) {
  const nonce = headers().get('x-nonce')

  return (
    <html>
      <head>
        <script nonce={nonce} src="/script.js" />
      </head>
      <body>{children}</body>
    </html>
  )
}
```
</security_headers>

<csrf_protection>
**Server Actions have built-in CSRF protection:**

- Origin header verification
- SameSite cookie setting
- Automatic token handling

**For API routes, add CSRF token:**
```typescript
// lib/csrf.ts
import { cookies } from 'next/headers'
import crypto from 'crypto'

export async function getCSRFToken() {
  const cookieStore = await cookies()
  let token = cookieStore.get('csrf')?.value

  if (!token) {
    token = crypto.randomBytes(32).toString('hex')
    cookieStore.set('csrf', token, {
      httpOnly: true,
      sameSite: 'strict',
      secure: process.env.NODE_ENV === 'production',
    })
  }

  return token
}

export async function verifyCSRFToken(token: string) {
  const cookieStore = await cookies()
  const storedToken = cookieStore.get('csrf')?.value
  return token === storedToken
}
```
</csrf_protection>

<secrets>
**Never expose secrets:**

```typescript
// BAD - exposed to client
const apiKey = process.env.NEXT_PUBLIC_API_KEY  // Anyone can see this

// GOOD - server only
const apiKey = process.env.API_KEY  // Only available on server
```

**Use server-only package:**
```bash
npm i server-only
```

```typescript
// lib/secrets.ts
import 'server-only'

export const apiKey = process.env.API_KEY
```

If imported in Client Component, build will fail.
</secrets>

<rate_limiting>
**Implement rate limiting:**

```typescript
// lib/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
})

// In Server Action
export async function login(formData: FormData) {
  const ip = headers().get('x-forwarded-for') ?? 'unknown'

  const { success, limit, remaining } = await ratelimit.limit(ip)

  if (!success) {
    return { error: 'Too many requests. Please try again later.' }
  }

  // Proceed with login...
}
```
</rate_limiting>

<sensitive_data>
**Don't log sensitive data:**

```typescript
// BAD
console.log('User login:', { email, password })

// GOOD
console.log('User login attempt:', { email })
```

**Sanitize error messages:**
```typescript
try {
  await db.users.create({ data })
} catch (error) {
  console.error('Database error:', error)  // Log full error server-side

  // Return generic message to client
  return { error: 'Failed to create account. Please try again.' }
}
```
</sensitive_data>

<checklist>
**Security checklist:**

- [ ] Auth verified in DAL, not proxy
- [ ] All Server Actions check authentication
- [ ] All input validated with schema (Zod)
- [ ] Security headers configured
- [ ] CSP policy in place
- [ ] Secrets not exposed to client
- [ ] Rate limiting on sensitive endpoints
- [ ] Error messages sanitized
- [ ] Dependencies audited (`npm audit`)
- [ ] Latest Next.js version (16.1+)
</checklist>
