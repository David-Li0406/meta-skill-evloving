---
name: security-basics
description: Apply project-specific security and privacy guardrails (auth, headers, rate limiting, logging). Use when touching authentication, request handling, metrics exposure, or anything that could leak sensitive data.
license: MIT
compatibility: Applies to the mjrwtf Go server; requires bash and git for repo work.
metadata:
  repo: mjrwtf
  runner: github-copilot-cli
  version: 1.3
allowed-tools: Bash(git:*) Bash(go:*) Bash(make:*) Read
---

## Tooling assumptions

- Use a terminal runner with bash and git available.
- Prefer `make` targets when available; fall back to direct CLI commands when needed.

## Authentication & secrets

- Auth tokens: `AUTH_TOKENS` (preferred; comma-separated) or `AUTH_TOKEN` (legacy; single token).
- Never hardcode tokens; use environment variables.
- Avoid logging full URLs, tokens, session cookies, or authorization headers.

## Rate limiting & client IP

- The rate limiter keys by client IP and may use `X-Forwarded-For` / `X-Real-IP`.
- In production, ensure the reverse proxy strips/overwrites forwarding headers to prevent spoofing.

## Metrics exposure

- `/metrics` may be public by default; enable protection when needed via `METRICS_AUTH_ENABLED=true`.

## Practical review checklist

- Inputs validated (especially short codes and URLs).
- Error responses don’t reveal internals/secrets.
- CORS settings (`ALLOWED_ORIGINS`) are appropriate for production.
- Secure cookies enabled (`SECURE_COOKIES=true`) when behind HTTPS.
