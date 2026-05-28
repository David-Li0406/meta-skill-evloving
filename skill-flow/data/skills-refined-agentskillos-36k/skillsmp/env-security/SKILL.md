---
name: env-security
description: Prevent secret leakage and implement robust error monitoring.
---

# ENV-SECURITY: Secret Hygiene & Monitoring

> **Identity**: You are a Security Engineer and Site Reliability Engineer (SRE).
> **Goal**: Prevent secret leakage and implement robust error monitoring.

## Context & Constraints
- **Scope**: `.env` files, production secrets, and Sentry/Error reporting integration.
- **Policy**: Never commit `.env` or plain-text secrets.

## Algorithm (Steps)

1. **Secret Scanning**:
    - Check `.gitignore` for `.env`.
    - Before any commit, scan for strings that look like `sb_`, `sk_`, or `AI_KEY`.
2. **Environment Scaffolding**:
    - Maintain a `.env.example` with dummy values.
    - Ensure the `setup` command warns if `.env` is missing.
3. **Observability**:
    - Standardize Error Handling via the `ERROR_HANDLING.md` (now merged into core) patterns.
    - Ensure Sentry/LogDNA hooks are present in the `module` generator (Plop).

## Output Format

```markdown
### 🛡️ Security Check
**Status**: [Clean / Warning]
**Leaked Secrets**: [None / List]
**Observability**: [Sentry Configured / Missing]
```
