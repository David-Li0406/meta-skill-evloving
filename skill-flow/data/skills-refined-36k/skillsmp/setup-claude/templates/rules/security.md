# Security Rules

Security best practices to prevent vulnerabilities.

## Always Do

- **Validate all inputs** - Never trust user input, validate type, length, format
- **Escape outputs** - HTML-escape when rendering, SQL-escape for queries
- **Use parameterized queries** - Never concatenate SQL strings
- **Store secrets in environment** - Use .env files, never hardcode
- **Check authentication** - Verify user identity before protected actions
- **Check authorization** - Verify user has permission for the action
- **Use HTTPS** - All external communication over TLS
- **Hash passwords** - Use bcrypt, argon2, or similar with proper salt
- **Set secure headers** - CSP, X-Frame-Options, etc.
- **Log security events** - Failed logins, permission denials, suspicious activity

## Never Do

- ❌ **Hardcode secrets** - No API keys, passwords, tokens in code
- ❌ **Commit .env files** - Keep secrets out of version control
- ❌ **Use eval()** - Avoid dynamic code execution
- ❌ **Trust client data** - Always validate server-side
- ❌ **Expose stack traces** - Hide internal errors from users
- ❌ **Use MD5/SHA1 for passwords** - Use proper password hashing
- ❌ **Store sensitive data in localStorage** - Use httpOnly cookies
- ❌ **Disable CORS carelessly** - Be specific about allowed origins
- ❌ **Log sensitive data** - No passwords, tokens, PII in logs
- ❌ **Use HTTP for sensitive data** - Always use HTTPS

## Examples

### Input Validation

**Good**:
```typescript
function createUser(input: unknown) {
  const parsed = userSchema.parse(input); // Zod validation
  if (parsed.email.length > 255) {
    throw new Error('Email too long');
  }
  // proceed with validated data
}
```

**Bad**:
```typescript
function createUser(input: any) {
  db.insert('users', input); // No validation!
}
```

### SQL Queries

**Good**:
```typescript
// Parameterized query
const user = await db.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);
```

**Bad**:
```typescript
// SQL injection vulnerability!
const user = await db.query(
  `SELECT * FROM users WHERE id = ${userId}`
);
```

### Secret Storage

**Good**:
```typescript
// Read from environment
const apiKey = process.env.STRIPE_SECRET_KEY;
if (!apiKey) throw new Error('Missing STRIPE_SECRET_KEY');
```

**Bad**:
```typescript
// Hardcoded secret!
const apiKey = 'sk_live_abc123...';
```

### Authentication Check

**Good**:
```typescript
async function updateProfile(userId: string, data: ProfileData) {
  const session = await getSession();
  if (!session || session.userId !== userId) {
    throw new UnauthorizedError();
  }
  // proceed with update
}
```

**Bad**:
```typescript
async function updateProfile(userId: string, data: ProfileData) {
  // No auth check - anyone can update any profile!
  await db.update('profiles', userId, data);
}
```

## Exceptions

When these rules may be relaxed:

1. **Development/testing only** - Mock secrets in test fixtures (never in production code)
2. **Public data** - No auth needed for truly public endpoints
3. **Internal tools** - May have relaxed validation for admin-only tools (still be careful)

## Security Checklist

Before committing code that handles:

### User Input
- [ ] Input validated (type, length, format)
- [ ] Error messages don't leak internals
- [ ] Rate limiting considered

### Authentication
- [ ] Session validated
- [ ] Tokens properly verified
- [ ] Logout clears all state

### Database
- [ ] Queries parameterized
- [ ] Sensitive fields encrypted
- [ ] Backups encrypted

### API
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] Rate limiting in place
- [ ] Auth required for protected routes

### Files
- [ ] Upload validation (type, size)
- [ ] No path traversal possible
- [ ] Sensitive files not in public folder
