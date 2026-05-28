---
name: nestjs-security
description: Use this skill for implementing authentication, role-based access control (RBAC), and hardening standards in NestJS applications.
---

# NestJS Security Standards

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

- **Hashing**: Use **Argon2id** instead of Bcrypt.
- **Encryption**: Use **AES-256-GCM** with KMS rotation. Never hardcode keys.

## CSRF (Cross-Site Request Forgery)

- **Context**: Mandatory for cookie-based sessions or JWTs.
- **Mitigation**: Use a synchronizer token (e.g., `csurf`) and ensure strong token verification on state-changing requests.

## Hardening

- **Helmet**: Mandatory. Enable HSTS and configure Content Security Policy (CSP).
- **CORS**: Allow explicit origins only. No `*`.
- **Throttling**: Use Redis-backed `@nestjs/throttler` in production.
- **Audit Logging**: Track critical mutations (Who, What, When) using an `AuditInterceptor`.

## Data Protection

- **Sanitization**: Use `ClassSerializerInterceptor` + `@Exclude()` to strip sensitive fields from responses.
- **Validation**: Implement `ValidationPipe({ whitelist: true })` to prevent mass assignment attacks.

## Secrets Management

- **CI/CD**: Run `npm audit --prod` in pipelines.
- **Runtime**: Inject secrets via vault (e.g., AWS Secrets Manager / HashiCorp Vault), not `.env` files.

## Anti-Patterns

- **Shadow APIs**: Regularly audit routes and disable `/docs` in production.
- **SSRF**: Allowlist domains for outgoing HTTP requests and restrict egress traffic.
- **SQLi**: Use ORM methods and avoid raw queries with string concatenation.
- **XSS**: Sanitize HTML input (e.g., `dompurify`) before storage or output.

## Related Topics

common/security-standards | architecture | database