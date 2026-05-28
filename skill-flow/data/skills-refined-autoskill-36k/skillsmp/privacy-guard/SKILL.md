---
name: privacy-guard
description: Enforces zero-tolerance scanning for PII, secrets, and unauthorized file types before code processing.
---

# Privacy Guard Protocol

## File Scope (Strict Allowlist)

**ONLY** process:

- **Code:** `.go`, `.rs`, `.zig`, `.ts`, `.js`, `.py`, `.c`, `.cpp`, `.h`, `.css`, `.html`
- **Build:** `go.mod`, `go.sum`, `build.zig*`, `Cargo.*`, `package.json`, `*lock*`, `requirements.txt`, `Pipfile`, `Makefile`
- **Config:** `Dockerfile`, `*.yaml/yml`, `.env.example`, `.gitignore`, `.editorconfig`, `.toml`, `.json` (only if infrastructure/build config)

**REJECT immediately:**

- Documents: `.pdf`, `.docx`, `.doc`, `.rtf`, `.pages`
- Data: `.xls*`, `.csv`, `.numbers`, user-record JSON/YAML/XML
- Secrets: `.pem`, `.key`, `id_rsa`, `secrets.*`

## Privacy Scan (Execute Before Processing)

**Detect and redact** to `<REDACTED>`:

- API keys (AWS, Stripe, etc.)
- Database passwords
- Real names (non-author)
- Email addresses (non-dummy)
- Phone numbers
- Physical addresses
- Credit cards
- Internal IPs (`192.168.x.x`, `10.x.x.x`) → `<INTERNAL_IP>`

## Execution

1. **Validate** file type against allowlist
2. **Scan** for PII/secrets
3. **Redact** matches + report types found
4. **Proceed** with request OR output: `🚫 PRIVACY GUARD: File/content rejected`

**Never output real PII or use it in examples.**
