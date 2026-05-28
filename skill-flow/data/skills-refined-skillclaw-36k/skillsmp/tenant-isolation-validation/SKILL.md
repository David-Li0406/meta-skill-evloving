---
name: tenant-isolation-validation
description: Validate tenant isolation and RLS safety checks. Use when the user mentions tenant isolation, RLS validation, or multi-tenant access checks.
---
# Tenant Isolation Validation

## Quick Start

1. Review the tenant isolation guidance.
2. Run the tenant safety checks.
3. Summarize violations and remediation steps.

## Steps

- Follow `docs/security/tenant-isolation.md`.
- Use repo scripts:
  - `scripts/check-tenant-safety.ts`
  - `scripts/mcp/tenant-validate.sh`
- Confirm RLS policies enforce tenant boundaries.

## Output

- Report of any cross-tenant access risks.
- Clear remediation steps and affected tables.
