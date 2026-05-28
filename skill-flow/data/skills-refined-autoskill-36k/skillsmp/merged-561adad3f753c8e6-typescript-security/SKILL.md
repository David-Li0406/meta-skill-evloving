---
name: typescript-security
description: Use this skill for implementing secure coding practices in TypeScript applications based on OWASP guidelines.
---

# TypeScript Security

## **Priority: P0 (CRITICAL)**

Security standards for TypeScript applications based on OWASP guidelines.

## Implementation Guidelines

- **Validation**: Validate all inputs with `zod`/`joi`/`class-validator`.
- **Sanitization**: Use `DOMPurify` for HTML to prevent XSS.
- **Secrets**: Use environment variables; never hardcode secrets.
- **SQL Injection**: Use parameterized queries or ORMs (Prisma/TypeORM).
- **Auth**: Use `bcrypt` for hashing and implement strict RBAC.
- **HTTPS**: Enforce HTTPS and set `secure`, `httpOnly`, `sameSite` cookies.
- **Rate Limit**: Implement measures to prevent brute-force and DDoS attacks.
- **Dependencies**: Regularly audit dependencies with `npm audit`.

## Anti-Patterns

- **No `eval()`**: Avoid dynamic execution of code.
- **No Plaintext**: Never commit secrets in plaintext.
- **No Trust**: Always validate inputs server-side.

## Code Examples

```typescript
// Validation (Zod)
const UserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

// Secure Cookie
const cookieOpts = {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'prod',
  sameSite: 'strict' as const,
};
```

## Reference & Examples

For authentication patterns and security headers, refer to the relevant documentation.

## Related Topics

best-practices | language | common/security-standards