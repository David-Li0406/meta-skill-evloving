# Self-Review Checklist

Before committing, verify:

## Code Quality

- [ ] No over-engineering (abstractions only used once)
- [ ] No unnecessary complexity
- [ ] Changes focused on acceptance criteria (no scope creep)

## Conventions

- [ ] File naming follows conventions (PascalCase components, camelCase utilities)
- [ ] Function declarations for components (not const arrows)
- [ ] Explicit return types on exported functions
- [ ] Booleans prefixed with is/has/can/should

## Comments

- [ ] Comments explain WHY, not WHAT
- [ ] No redundant JSDoc
- [ ] No section divider comments

## Testing

- [ ] Tests pass: `pnpm test`
- [ ] Types check: `pnpm typecheck`
- [ ] Lint passes: `pnpm lint`

## Reuse

- [ ] Checked lib/ for existing utilities
- [ ] No duplicate code that should be extracted
- [ ] Reusable code promoted to lib/ if appropriate
