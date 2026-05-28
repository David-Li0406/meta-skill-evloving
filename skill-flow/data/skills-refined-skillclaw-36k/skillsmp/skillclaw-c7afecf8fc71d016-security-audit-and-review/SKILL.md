---
name: security-audit-and-review
description: Use this skill when you need to conduct a comprehensive security audit and review of your application to identify and mitigate vulnerabilities.
---

# Security Audit and Review

## When to Use

Use this skill when you are implementing features that involve user input, authentication, API endpoints, or handling sensitive data. It is essential to proactively identify and fix security vulnerabilities.

## Security Checklist

### 1. Sensitive Data Management (CRITICAL)

```typescript
// Prohibited: Hardcoding sensitive data
const apiKey = "sk-proj-xxxxx";  // Absolutely prohibited
const password = "admin123";      // Absolutely prohibited

// Correct: Use environment variables
const apiKey = process.env.OPENAI_API_KEY;
if (!apiKey) {
  throw new Error('OPENAI_API_KEY is not set');
}
```

**Checklist:**
- [ ] No hardcoded API keys, tokens, or passwords.
- [ ] All sensitive data is managed using environment variables.
- [ ] `.env.local` is included in .gitignore.
- [ ] No sensitive data in Git history.
- [ ] Production secrets stored securely.

### 2. Input Validation

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150)
});

export async function createUser(input: unknown) {
  const validated = CreateUserSchema.parse(input);
  return await db.users.create(validated);
}
```

**Checklist:**
- [ ] All user inputs are validated using a schema validation library.
- [ ] File uploads are restricted by size, type, and extension.
- [ ] Error messages do not expose sensitive information.

### 3. SQL Injection Protection (CRITICAL)

```typescript
// Prohibited: String concatenation in SQL
const query = `SELECT * FROM users WHERE email = '${userEmail}'`;

// Correct: Parameterized query
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('email', userEmail);
```

**Checklist:**
- [ ] All database queries use parameterized queries.
- [ ] No string concatenation in SQL queries.
- [ ] Proper use of ORM/Query Builder.

### 4. Authentication and Authorization

```typescript
// Correct: JWT Token stored in httpOnly cookies
res.setHeader('Set-Cookie',
  `token=${token}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600`);

// Correct: Authorization check
export async function deleteUser(userId: string, requesterId: string) {
  const requester = await db.users.findUnique({ where: { id: requesterId } });
  if (requester.role !== 'admin') {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
  }
  await db.users.delete({ where: { id: userId } });
}
```

**Checklist:**
- [ ] Tokens are stored in httpOnly cookies (not localStorage).
- [ ] Authorization checks are performed before sensitive operations.
- [ ] Implement Role-Based Access Control (RBAC).

### 5. Cross-Site Scripting (XSS) Protection

```typescript
import DOMPurify from 'isomorphic-dompurify';

function renderUserContent(html: string) {
  const clean = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'],
    ALLOWED_ATTR: []
  });
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}
```

**Checklist:**
- [ ] User-provided HTML is sanitized before rendering.

### 6. Additional Security Practices

- **HTTPS Enforcement:** Ensure all traffic is served over HTTPS.
- **HSTS:** Implement HTTP Strict Transport Security to protect against man-in-the-middle attacks.
- **Session Management:** Use secure session configurations to protect user sessions.

By following this comprehensive checklist, you can significantly enhance the security posture of your application and protect against common vulnerabilities outlined in the OWASP Top 10.