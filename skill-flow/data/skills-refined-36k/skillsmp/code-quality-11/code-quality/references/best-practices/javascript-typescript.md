# JavaScript/TypeScript Best Practices
- Use ESLint flat config with typescript-eslint; align with EditorConfig whitespace.
- Prefer TypeScript strict mode; enable noImplicitAny, strictNullChecks, noUncheckedIndexedAccess.
- Imports: use path aliases or absolute paths for shared modules; avoid deep relative chains.
- Exports: favor named exports; use barrels only when stable APIs exist.
- Async: use async/await; wrap fetch/axios with a shared client for retries/error handling.
- Types: prefer readonly for constants; use discriminated unions for variants.
- Testing: use jest/vitest; mock HTTP via msw; keep fixtures small and deterministic.
- Formatting: hand off formatting to Prettier; disable conflicting ESLint formatting rules via eslint-config-prettier.
