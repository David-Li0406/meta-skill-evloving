# Authentication

This file is an example placeholder referenced by the Skill Creator skill.

## Supported Auth Modes

- API keys
- OAuth2 / OIDC (Authorization Code, Client Credentials)
- Session cookies
- Service-to-service auth (mTLS, signed JWT)

## Tokens & Claims

- Expected claims (issuer, audience, subject)
- Token lifetimes and refresh strategy
- Key rotation and JWKS

## Authorization

- Roles/permissions model
- Resource-level checks
- Multi-tenant boundaries

## Common Pitfalls

- Clock skew handling
- Audience/issuer mismatches
- Missing scope checks
