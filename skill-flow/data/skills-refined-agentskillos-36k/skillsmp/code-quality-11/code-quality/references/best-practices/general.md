# General Best Practices
- Keep functions small, single-responsibility.
- Prefer pure functions; isolate side effects.
- Consistent naming per category (functions camelCase, types PascalCase, constants SCREAMING_SNAKE).
- Enforce import grouping: stdlib/core, third-party, internal; alphabetical within groups.
- Handle errors explicitly; avoid silent failures; log with context.
- Write unit tests near code or in __tests__; name *.test.* or *.spec.* consistently.
- Document non-obvious logic with short comments; add JSDoc/type hints for public interfaces.
- Avoid duplicate logic; prefer shared utilities.
