---
name: nestjs-security
description: Use this skill when implementing security standards for NestJS applications, focusing on authentication, authorization, and hardening practices.
---

# NestJS Security Standards

## **Priority: P0 (CRITICAL)**

## Authentication (JWT)

- **Strategy**: Use `@nestjs/passport` with `passport-jwt`.
- **JWT Hardening**:
  - **Algorithm**: Enforce `RS256` (preferred) or `HS256`. **Reject `none`**.
  - **Claims**: Validate `iss` (Issuer) and `aud` (Audience).
  - **Secrets**: High entropy (> 256-bit) for HS256.
- **State**: Stateless. Use short access tokens (15m) and long httponly refresh tokens (7d).
- **MFA**: Require 2FA for sensitive access (e.g., admin panels).

## Authorization (RBAC)

- **Deny by default**: Bind `AuthGuard` globally (APP_GUARD).
- **Bypass**: Create a `@Public()` decorator for open routes.
- **Metadata**: Use `Reflector.createDecorator<string[]>()` for roles.
- **Guards**: Use `Reflector` to merge Method/Class roles with `getAllAndOverride`.

## Cryptography & Hashing

- **Hashing**: Use **Argon2id** instead of Bcrypt.
- **Encryption**: Use **AES-256-GCM** for data at rest. Rotate keys using a KMS (Key Management Service).

## CSRF (Cross-Site Request Forgery)

- **Context**: Mandatory for cookie-based sessions or JWTs.
- **Mitigation**: Use `csurf` middleware for synchronizer tokens. Ensure tokens are cryptographically strong and verified on state-changing requests (POST/PUT/DELETE).

## Hardening

1. **Helmet**: Mandatory. Enable HSTS and configure Content Security Policy (CSP).
2. **CORS**: Explicit origins only. No `*`.
3. **Throttling**: Use Redis-backed `@nestjs/throttler` in production.
4. **Data Protection**:
   - **Sanitization**: Use `ClassSerializerInterceptor` + `@Exclude()`.
   - **Validation**: Use `ValidationPipe({ whitelist: true })` to prevent mass assignment.
   - **Audit**: Log mutations (Who, What, When).

## Anti-Patterns

- **No Shadow APIs**: Regularly audit routes; disable `/docs` in production.
- **No SSRF**: Allowlist domains for outgoing HTTP requests.
- **No SQLi**: Use ORM; avoid raw `query()` with string concatenation.
- **No XSS**: Sanitize HTML input with `dompurify`.

## Secrets Management

- **CI/CD**: Run `npm audit --prod` in pipelines.
- **Runtime**: Inject secrets via vault (AWS Secrets Manager / HashiCorp Vault), not `.env`.

## Related Topics

common/security-standards | architecture | database