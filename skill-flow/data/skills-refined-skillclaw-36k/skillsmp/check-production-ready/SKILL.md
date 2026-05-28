---
name: check-production-ready
description: Verify code is ready for production - build, tests, security, and configuration checks
allowed-tools: Bash, Read, Glob, Grep
---

# Check Production Ready Skill

Validate that code meets production deployment standards.

## Usage

```bash
/check-production-ready        # Full production readiness check
```

## What Gets Checked

| Category | Checks |
|----------|--------|
| Build | Compiles without errors |
| Tests | All pass, none skipped without reason |
| Linting | ESLint, TypeScript, Clarinet |
| Security | npm audit, no hardcoded secrets |
| Environment | .env.example exists, no dev URLs |
| Git | Clean working directory, correct branch |

## Output

Checklist with pass/fail status and summary of any blockers or warnings.

## Runbook

Full procedure: `runbook/check-production-ready.md` in your knowledge base.
