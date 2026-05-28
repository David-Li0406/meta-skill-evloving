---
name: rls-policy-testing
description: Validate RLS policies and role-based access. Use when the user mentions RLS testing, role access checks, or permissions validation.
---
# RLS Policy Testing

## Quick Start

1. Identify role and table scope.
2. Run role-specific tests.
3. Summarize access violations.

## Steps

- Use docs and tests:
  - `docs/AUTH_ROLES.md`
  - `tests/rls/`
  - `tests/admins/`, `tests/therapists/`, `tests/clients/`
  - `cypress/e2e/auth-roles.cy.ts`
  - `cypress/e2e/role_access.cy.ts`

## Output

- Failing roles/tables and remediation hints.
