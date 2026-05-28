# Security Review Example Output

This is an example of the expected output format for a security review.

---

## Security Review

**Scope:** src/api/users.ts, src/data/UserRepository.ts
**Project Type:** Node.js/TypeScript

### Findings

| Severity | Count |
|----------|-------|
| Critical | 2 |
| Major | 1 |
| Minor | 1 |

### Critical Issues (Must Fix)

**1. SQL Injection in User Query** `Critical` `Security`
`src/data/UserRepository.ts:45-48`

User input is directly concatenated into SQL query without parameterization.

```typescript
// Current code (vulnerable)
const query = `SELECT * FROM users WHERE email = '${email}'`;
const result = await db.query(query);
```

**Fix**:
```diff
- const query = `SELECT * FROM users WHERE email = '${email}'`;
- const result = await db.query(query);
+ const query = 'SELECT * FROM users WHERE email = ?';
+ const result = await db.query(query, [email]);
```

---

**2. Hardcoded API Key** `Critical` `Security`
`src/api/users.ts:12`

API key is hardcoded in source code. This exposes the key in version control.

```typescript
const STRIPE_KEY = 'sk_live_abc123def456';
```

**Fix prompt** (copy to Claude Code):
> Move the Stripe API key to environment variables:
> 1. Add STRIPE_KEY to .env.example (without the actual value)
> 2. Replace hardcoded key with process.env.STRIPE_KEY in src/api/users.ts:12
> 3. Add validation to fail fast if STRIPE_KEY is not set

---

### Major Issues (Should Fix)

**3. Missing Rate Limiting on Login** `Major` `Security`
`src/api/auth.ts:34-50`

Login endpoint has no rate limiting, enabling brute force attacks.

**Fix prompt** (copy to Claude Code):
> Add rate limiting to the login endpoint in src/api/auth.ts:
> 1. Install express-rate-limit if not present
> 2. Create a strict limiter (5 attempts per 15 minutes per IP)
> 3. Apply to the POST /api/auth/login route

---

### Minor Issues

**4. Missing Security Headers** `Minor` `Security`
`src/app.ts:1-20`

Application does not set recommended security headers.

**Fix prompt** (copy to Claude Code):
> Add helmet middleware to src/app.ts for security headers:
> 1. Install helmet: npm install helmet
> 2. Add app.use(helmet()) after express() initialization
> This adds CSP, X-Frame-Options, and other security headers.

---

### Summary

- **2 Critical issues** require immediate attention before deployment
- **1 Major issue** should be addressed to prevent abuse
- **1 Minor issue** improves defense-in-depth

---
Review saved to: .security-review.md
