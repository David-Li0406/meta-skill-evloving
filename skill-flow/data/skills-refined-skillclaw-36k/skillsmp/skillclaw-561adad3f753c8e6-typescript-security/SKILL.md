---
name: typescript-security
description: Use this skill when implementing secure coding practices for building safe TypeScript applications.
---

# TypeScript Security

## **Priority: P0 (CRITICAL)**

Security standards for TypeScript applications based on OWASP guidelines.

## Implementation Guidelines

- **Validation**: Validate all inputs with `zod`/`joi`/`class-validator`.
- **Sanitization**: Use `DOMPurify` for HTML to prevent XSS.
- **Secrets Management**: Use environment variables; never hardcode secrets.
- **SQL Injection Prevention**: Use parameterized queries or ORMs (e.g., Prisma/TypeORM).
- **Authentication**: Use `bcrypt` for hashing passwords and implement strict RBAC.
- **HTTPS Enforcement**: Always enforce HTTPS and set `secure`, `httpOnly`, and `sameSite` attributes for cookies.
- **Rate Limiting**: Implement measures to prevent brute-force attacks and DDoS.
- **Dependency Auditing**: Regularly audit dependencies with `npm audit`.

## Anti-Patterns

- **Avoid `eval()`**: Do not use dynamic execution.
- **No Plaintext Secrets**: Never commit secrets in plaintext.
- **Validate Everything**: Always validate inputs server-side.

## Code Examples

```typescript
// Validation (Zod)
const UserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

// Secure Cookie Configuration
const cookieOpts = {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'prod',
  sameSite: 'strict' as const,
};
```

## Reference & Examples

For authentication patterns and security headers, refer to the relevant documentation.

## Related Topics

best-practices | language