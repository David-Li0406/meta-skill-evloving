---
name: nestjs-security
description: Use this skill for implementing authentication, role-based access control (RBAC), and hardening standards in NestJS applications.
---

# NestJS Security Standards

## **Priority: P0 (CRITICAL)**

## Authentication (JWT)

- **Strategy**: Use `@nestjs/passport` with `passport-jwt`.
- **Algorithm**: Enforce `RS256` (preferred) or `HS256`. **Reject `none`**.
- **Claims**: Validate `iss` (Issuer) and `aud` (Audience).
- **Tokens**: Use short access tokens (15m) and long httponly refresh tokens (7d).
- **MFA**: Require 2FA for sensitive access (e.g., admin panels).

## Authorization (RBAC)

- **Deny by default**: Bind `AuthGuard` globally (APP_GUARD).
- **Bypass**: Create a `@Public()` decorator for open routes.
- **Roles**: Use `Reflector.getAllAndOverride` for merging Method/Class roles.

## Cryptography & Hashing

- **Hashing**: Use **Argon2id** instead of Bcrypt. Implement with `await argon2.hash(password)`.
- **Encryption**: Use **AES-256-GCM** for data at rest. Rotate keys using a Key Management Service (KMS).

## CSRF (Cross-Site Request Forgery)

- **Context**: Mandatory for cookie-based sessions or JWTs.
- **Mitigation**: Use `csurf` or similar middleware for synchronizer tokens. Ensure tokens are cryptographically strong and verified on state-changing requests.

## Hardening

1. **Helmet**: Mandatory. Enable HSTS and configure Content Security Policy (CSP).
2. **CORS**: Allow explicit origins only. No wildcard (`*`).
3. **Throttling**: Use Redis-backed `@nestjs/throttler` in production to manage rate limits.
4. **Permissions-Policy**: Restrict browser permissions via `helmet.permissionsPolicy()`.

## Audit Logging

- **Requirement**: Track critical mutations (Who, What, When) using an `AuditInterceptor` for logging actions to a secure, immutable log store.

## Secrets & Configuration Management

- **CI/CD**: Run `npm audit --prod` in pipelines.
- **Runtime**: Inject secrets via environment variables from a vault (e.g., AWS Secrets Manager, HashiCorp Vault) instead of using `.env` files.

## Data Protection

- **Sanitization**: Use `ClassSerializerInterceptor` + `@Exclude()` to strip sensitive fields from responses.
- **Validation**: Implement `ValidationPipe({ whitelist: true })` to prevent mass assignment attacks.

## Anti-Patterns

- **Shadow APIs**: Regularly audit routes and disable Swagger/OpenAPI endpoints in production.
- **Server-Side Request Forgery (SSRF)**: Validate and allowlist domains for outgoing HTTP requests. Restrict egress traffic as necessary.
- **Injection Prevention**: Use ORM/ODM methods to avoid SQL injection. Sanitize HTML input to prevent XSS.

## Related Topics

common/security-standards | architecture | database