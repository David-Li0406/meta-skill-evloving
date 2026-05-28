# EquipQR review-comment resolution playbook

## What “resolved” means

- The code change is implemented and aligns with the relevant `.cursor/rules/*`.
- You’ve verified locally with the appropriate checks (typecheck/lint/tests as applicable).
- The PR has an updated summary comment explaining what was done.

## Where to look for standards

- `.cursor/rules/coding-standards.mdc`
- `.cursor/rules/design-system.mdc`
- `.cursor/rules/accessibility.mdc`
- `.cursor/rules/performance.mdc`
- `.cursor/rules/supabase-migrations.mdc` (if SQL migrations touched)

## Prioritization (suggested)

- **HIGH**: security issues, data correctness, broken UX, type errors
- **MEDIUM**: performance, maintainability, correctness in edge cases
- **LOW**: naming, formatting, minor refactors, documentation
