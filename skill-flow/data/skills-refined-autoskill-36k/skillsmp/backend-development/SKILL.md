---
name: backend-development
description: Modern backend patterns, API design, OWASP security checklist, testing pyramid. For Node.js, Python, Go backends.
---

# Backend Development

> **Load this skill** before implementing APIs, databases, or server-side logic.

## Core Principles

1. **Security First** - Never trust user input
2. **Fail Fast** - Validate at the boundary
3. **Idempotency** - Same request = same result
4. **Observability** - Log, trace, monitor everything

---

## API Design

### RESTful Conventions

| Method | Action | Idempotent | Safe |
|--------|--------|------------|------|
| GET | Read | ✅ | ✅ |
| POST | Create | ❌ | ❌ |
| PUT | Replace | ✅ | ❌ |
| PATCH | Update | ❌ | ❌ |
| DELETE | Remove | ✅ | ❌ |

### Response Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation failed |
| 401 | Unauthorized | No/invalid auth |
| 403 | Forbidden | Auth valid, no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate, version mismatch |
| 422 | Unprocessable | Semantic errors |
| 500 | Server Error | Unexpected failures |

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": [
      { "field": "email", "message": "Invalid format" }
    ]
  }
}
```

---

## OWASP Security Checklist

### 1. Injection Prevention
```typescript
// ❌ NEVER
db.query(`SELECT * FROM users WHERE id = ${userId}`)

// ✅ ALWAYS parameterize
db.query("SELECT * FROM users WHERE id = ?", [userId])
```

### 2. Authentication
- Use bcrypt/argon2 for passwords (cost factor ≥ 12)
- JWT with short expiry + refresh tokens
- Rate limit login attempts (5/min)
- Secure session cookies (httpOnly, secure, sameSite)

### 3. Authorization
```typescript
// Check ownership on EVERY request
if (resource.userId !== currentUser.id) {
  throw new ForbiddenError()
}
```

### 4. Input Validation
```typescript
// Validate at the boundary with Zod
const schema = z.object({
  email: z.string().email(),
  age: z.number().int().positive().max(150),
})
const data = schema.parse(req.body)
```

### 5. Output Encoding
- Escape HTML in responses
- Use Content-Type headers
- Sanitize before storage AND display

### 6. Sensitive Data
- Never log passwords, tokens, PII
- Encrypt at rest and in transit
- Use environment variables for secrets

---

## Testing Pyramid

```
        ╱╲
       ╱  ╲      E2E Tests (10%)
      ╱────╲     - Full system flows
     ╱      ╲    - Critical paths only
    ╱────────╲   
   ╱          ╲  Integration Tests (20%)
  ╱────────────╲ - API endpoints
 ╱              ╲- Database operations
╱────────────────╲
╲                ╱ Unit Tests (70%)
 ╲──────────────╱  - Pure functions
  ╲            ╱   - Business logic
   ╲──────────╱    - Fast, isolated
```

### Test Structure

```typescript
describe("UserService", () => {
  describe("createUser", () => {
    it("should create user with valid data", async () => {
      // Arrange
      const input = { email: "test@example.com", name: "Test" }
      
      // Act
      const user = await userService.createUser(input)
      
      // Assert
      expect(user.id).toBeDefined()
      expect(user.email).toBe(input.email)
    })
    
    it("should reject duplicate email", async () => {
      // ... test error case
    })
  })
})
```

---

## Database Patterns

### N+1 Prevention
```typescript
// ❌ N+1 problem
const users = await db.users.findMany()
for (const user of users) {
  user.posts = await db.posts.findMany({ where: { userId: user.id }})
}

// ✅ Eager loading
const users = await db.users.findMany({
  include: { posts: true }
})
```

### Connection Pooling
```typescript
// Configure pool size based on:
// pool_size = (core_count * 2) + effective_spindle_count
const pool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})
```

### Transactions
```typescript
await db.$transaction(async (tx) => {
  const user = await tx.user.create({ data: userData })
  await tx.account.create({ data: { userId: user.id, ...accountData }})
  // Both succeed or both fail
})
```

---

## Performance Patterns

### Caching Strategy

| Cache Type | TTL | Use Case |
|------------|-----|----------|
| Response | 5min | Static content |
| Session | 30min | User data |
| Computed | 1hr | Expensive queries |
| Permanent | ∞ | Immutable data |

### Rate Limiting
```typescript
const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 100, // 100 requests per minute
  message: { error: "Too many requests" }
})
```

---

## Logging Standards

```typescript
// Structured logging
logger.info("User created", {
  userId: user.id,
  email: user.email, // Consider PII masking
  action: "user.create",
  duration: Date.now() - start,
})

// Error logging
logger.error("Database connection failed", {
  error: err.message,
  stack: err.stack,
  service: "postgres",
  retryCount: 3,
})
```

---

## Quick Checklist

Before shipping any backend code:

- [ ] Input validated with schema (Zod/Joi)
- [ ] SQL queries parameterized
- [ ] Authentication checked
- [ ] Authorization verified (ownership)
- [ ] Errors handled gracefully
- [ ] Sensitive data not logged
- [ ] Rate limiting in place
- [ ] Tests written and passing
- [ ] Database queries optimized (no N+1)
