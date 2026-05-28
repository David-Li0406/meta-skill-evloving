---
name: security-headers-csp
description: Best practices for HSTS, CORS, CSP, and security headers.
---

# Security Headers & CSP

## When to use this skill
- Configuring web servers (Nginx, Caddy, Apache).
- Setting up middleware (Laravel, Express, Django).
- Auditing site security.

## 1. Essential Headers
- **HSTS**: `Strict-Transport-Security: max-age=31536000` (1 year).
- **No Sniff**: `X-Content-Type-Options: nosniff`.
- **Frame Options**: `X-Frame-Options: DENY` or `SAMEORIGIN`.

## 2. Content Security Policy (CSP)
- **Default**: Start with `default-src 'self'`.
- **Scripts**: Avoid `'unsafe-inline'` or `'unsafe-eval'`. Use nonces or hashes if inline scripts are necessary.
- **Reporting**: Use `report-uri` or `report-to` to monitor violations without breaking the site initially (`Content-Security-Policy-Report-Only`).

## 3. CORS
- **Scope**: Only enable CORS if you are serving an API consumed by browsers on *different* domains.
- **Origin**: Whitelist specific origins; avoid `Access-Control-Allow-Origin: *` with credentials.
