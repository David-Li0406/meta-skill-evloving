---
name: java-authn-authz-jwt
description: Design and implement robust JWT-based authentication (AuthN) and authorization (AuthZ): verification, claims validation, key rotation, token lifetimes, and safe error handling. Use when implementing login/permissions or integrating with OIDC/OAuth2 providers.
license: CC-BY-4.0
compatibility: "JDK 17+ (recommended JDK 21). Framework-agnostic. Works with any HTTP stack. If using OIDC, must be able to fetch JWKS over HTTPS."
metadata:
  owner: "backend"
  version: "1.0"
  tags: [java, security, jwt, oauth2, oidc, authn, authz]
---

# JWT AuthN/AuthZ (Verification, Claims, Rotation, Lifetimes)

## Intent

This skill is a **playbook** to build and operate JWT-based authentication/authorization safely in Java.
It focuses on:

- **Correct verification** (signature + algorithm allowlist + key selection + rotation)
- **Strict claims validation** (issuer/audience/exp/nbf + token-type constraints)
- **Authorization modeling** (RBAC/ABAC mapping and guardrails)
- **Token lifetime strategy** (access vs refresh, rotation, revocation hooks)
- **Operational safety** (logging discipline, observability, failure handling)

If you follow this, you avoid the classic JWT pitfalls: `alg=none`, algorithm confusion, accepting untrusted claims, weak key handling, and unbounded lifetimes.

---

## Scope

### In scope

- JWT parsing + signature verification (JWS)
- JWKS fetching + caching + key rotation (`kid`)
- Claims validation: `iss`, `aud`, `exp`, `nbf`, `iat`, `jti`, `typ`, custom claims (roles/scopes)
- Access token vs ID token handling (OIDC)
- Authorization model: RBAC/ABAC, mapping claims to permissions
- Error model: 401 vs 403, WWW-Authenticate, safe logs
- Tests: unit + integration + negative security tests

### Out of scope

- Building a full identity provider (IdP)
- UI login flows
- Password storage policies (separate skill)
- Advanced cryptography beyond JOSE standards

---

## When to use

Triggers / keywords:

- “JWT verification”, “invalid signature”, “kid not found”, “JWKS rotate”
- “OIDC login”, “ID token”, “access token”
- “permission/roles”, “scope”, “RBAC”, “ABAC”
- “token expired too early/late”, “clock skew”
- “security review”, “pen-test finding”, “auth incident”

---

## Required inputs (context to attach in Cursor)

- The endpoint(s) to protect (controllers/handlers, filters/middleware)
- Current token format examples **redacted** (never paste raw tokens)
- Identity provider details:
  - Expected `issuer` (iss)
  - Expected `audience` (aud)
  - JWKS URL (if OIDC/OAuth2 provider publishes it)
  - Allowed algorithms (e.g., RS256/ES256)
- Current authorization rules:
  - roles/scopes/permissions mapping
  - resources and actions (verb-based)

In Cursor: attach auth filter/middleware, security config, error handler, and any “claims mapping” code.

---

## Design principles (non-negotiable guardrails)

1. **Never trust decoded JWT claims until signature verification passes.**
2. **Algorithm allowlist**: accept only explicitly allowed `alg` values.
3. **Key selection safety**:
   - Only from trusted key sources (JWKS from issuer, pinned keys, or internal KMS)
   - Use `kid` only as an index, not as trust
4. **Strict claims validation**:
   - Validate `iss`, `aud`, `exp`, `nbf` (and optional `iat` sanity)
5. **Fail closed**:
   - If anything is ambiguous (unknown kid, invalid alg, missing required claims), reject.

---

## Procedure (step-by-step)

### Step 1 — Clarify token types and trust boundaries

Decide what you are validating:

- **Access Token**: used for API authorization.
- **ID Token** (OIDC): used to authenticate the user session (often front-channel), not always meant for API authorization unless your architecture says so.

Define:

- Who issues tokens? (issuer)
- Who consumes them? (your API)
- Are tokens meant for multiple audiences? If yes, enforce correct audience per service.

Deliverable: `Auth Token Contract` (issuer, audience, alg, required claims, lifetime).

---

### Step 2 — Choose verification strategy (asymmetric vs symmetric)

Recommended for microservices: **asymmetric keys** (RS256/ES256) so verifiers do not share signing secrets.

Options:

- RS256 (RSA) — common, easy integration
- ES256 (ECDSA) — smaller signatures, more complex operationally
Avoid:
- HS256 across many services unless you have strict secret distribution and rotation controls.

Deliverable: allowed algorithms list.

---

### Step 3 — Implement robust JWT verification (signature + alg allowlist)

Pseudo-code structure (framework-agnostic):

1) Extract token from `Authorization: Bearer <token>`
2) Parse header WITHOUT trusting it yet
3) Validate `alg` is in allowlist (reject `none`)
4) Determine key:
   - If using JWKS: use `kid` to select candidate keys
5) Verify signature with the selected key
6) Only then decode/accept claims

Important: protect against “algorithm confusion” by **not** letting the JWT header dynamically choose between HS*and RS*/ES* verification code paths.

---

### Step 4 — Implement JWKS fetching + caching + rotation

If issuer publishes JWKS:

- Fetch JWKS via HTTPS from issuer-controlled endpoint
- Cache keys with TTL (e.g., 5–60 minutes depending on provider)
- Support rotation:
  - If `kid` not found, refresh JWKS once (single-flight) and retry verification once
  - If still not found, reject with 401

Caching requirements:

- Thread-safe cache
- Single-flight refresh to prevent stampede
- Circuit breaker/backoff if JWKS endpoint is failing

Deliverable: `JwksKeyResolver` with cache + refresh policy.

---

### Step 5 — Strict claims validation checklist

After signature verification, validate claims:

**Required (typical)**:

- `iss` equals expected issuer
- `aud` contains expected audience (service/client id)
- `exp` is in the future (allow small clock skew)
- `nbf` (if present) is in the past (allow skew)

**Strongly recommended**:

- `iat` sanity: reject tokens with `iat` far in the future
- `typ` or token use indicator (if your issuer uses it) to prevent mixing token types
- `jti` if you need replay detection / revocation lists

Clock skew:

- Use small leeway (e.g., 30–120 seconds) but keep it explicit.

Deliverable: `ClaimsValidator` + unit tests for each rule.

---

### Step 6 — Authorization model (AuthZ) design

JWT-based AuthZ typically uses:

- **Scopes**: coarse-grained capabilities (OAuth2 style)
- **Roles**: RBAC groups
- **Permissions**: fine-grained actions

Recommended approach:

- Keep JWT claims **small and stable** (roles/scopes)
- Do fine-grained permission checks in code/policy layer
- Avoid embedding large ACLs in tokens (size + staleness + leakage risk)

Patterns:

- RBAC: `roles=["ADMIN","SUPPORT"]`
- Scope-based: `scope="orders:read orders:write"`
- ABAC: `tenant_id`, `org_id`, `region` + policy evaluation

Deliverable: `Authorization Policy` (resource, action, required roles/scopes, tenant constraints).

---

### Step 7 — Token lifetimes, refresh, rotation, revocation

A practical baseline:

- Access token: short-lived (minutes)
- Refresh token: longer-lived (hours/days) and stored securely by clients
- Rotation:
  - rotate signing keys on a schedule
  - plan how verifiers refresh JWKS and for how long old keys remain published
- Revocation strategy:
  - If you must revoke before expiry: use `jti` and a denylist (cache/redis) or use introspection (architecture-dependent)

Deliverable: `Token Lifetime Policy` + `Rotation Runbook`.

---

### Step 8 — Error handling and logging (security-safe)

Rules:

- Never log raw tokens or full claims.
- Log only:
  - high-level reason category (`invalid_signature`, `expired`, `bad_audience`, `kid_missing`)
  - request id / trace id
  - issuer identifier (safe)
- Responses:
  - 401 Unauthorized for invalid/missing token
  - 403 Forbidden for valid identity but insufficient permissions
  - Use `WWW-Authenticate: Bearer error="invalid_token"` where appropriate

Deliverable: standardized auth error mapper.

---

### Step 9 — Tests (must-have)

Unit tests:

- Reject `alg=none`
- Reject wrong `iss`, wrong `aud`
- Expiration/nbf boundary tests with clock skew
- Invalid signature
- Tampered payload

Integration tests:

- Spin up a mock JWKS server with rotating keys
- Validate refresh-on-kid-miss behavior
- Ensure caching + single-flight refresh (no stampede)

Security regression tests:

- Algorithm confusion attempts
- Oversized token / header injection handling

Deliverable: `Auth Test Suite` with reproducible execution.

---

## Outputs / Artifacts

- `Auth Token Contract` (issuer, audience, alg, required claims)
- `JwtVerifier` (verification + claims validation)
- `JwksKeyResolver` (cache + rotation)
- `Authorization Policy` mapping (roles/scopes -> permissions)
- Tests (unit + integration + negative security tests)
- Runbook (key rotation + incident response for auth failures)

---

## Definition of Done (DoD)

- [ ] Verification fails closed (unknown alg/kid/issuer/audience)
- [ ] Claims validation implemented and tested
- [ ] JWKS caching with safe refresh behavior
- [ ] 401 vs 403 semantics consistent across endpoints
- [ ] No tokens printed in logs; sanitized logging enforced
- [ ] Integration tests cover key rotation and failure modes
- [ ] Documentation: token contract + rotation runbook

---

## Common failure modes & fixes

- Symptom: “Works in dev, fails in prod with kid not found”
  - Cause: JWKS cache never refreshes or issuer rotated keys
  - Fix: refresh-on-miss + TTL + single-flight refresh

- Symptom: “Users get randomly logged out”
  - Cause: clock skew too strict; exp/nbf validation too tight
  - Fix: small leeway, sync time, monitor exp failures

- Symptom: “Token accepted but wrong permissions”
  - Cause: trusting a claim not meant for AuthZ; poor mapping
  - Fix: formal policy mapping; separate identity claims from permissions

- Symptom: “Pen-test found alg=none acceptance”
  - Cause: missing alg allowlist
  - Fix: hard allowlist + unit test

---

## Guardrails (What NOT to do)

- Do NOT decode-and-use claims before verifying the signature.
- Do NOT accept algorithms dynamically without an explicit allowlist.
- Do NOT log raw tokens, full claims, or PII-bearing claims.
- Do NOT embed large permission lists or sensitive data inside JWT.
- Do NOT rely solely on JWT for revocation if your threat model requires immediate revoke.

---

## References (primary)

- RFC 7519 (JWT): <https://www.rfc-editor.org/rfc/rfc7519>
- RFC 7515 (JWS): <https://www.rfc-editor.org/rfc/rfc7515>
- RFC 7517 (JWK): <https://www.rfc-editor.org/rfc/rfc7517>
- RFC 8725 (JWT Best Current Practices): <https://www.rfc-editor.org/rfc/rfc8725>
- RFC 9700 (OAuth 2.0 Security Best Current Practice): <https://www.rfc-editor.org/rfc/rfc9700>
- OpenID Connect Core 1.0: <https://openid.net/specs/openid-connect-core-1_0.html>
- OWASP JWT for Java Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html>
