---
name: javascript-tooling
description: Use this skill for essential development tools, linting, and testing in JavaScript projects.
---

# JavaScript Tooling

## **Priority: P1 (OPERATIONAL)**

Essential tooling for JavaScript development.

## Implementation Guidelines

- **Linting**: ESLint (Rec + Prettier). Fix on save.
- **Formatting**: Prettier. Run on save/commit.
- **Testing**: Jest/Vitest. Co-locate tests. >80% coverage.
- **Build**: Vite (for Apps), Rollup (for Libraries).
- **Package Manager**: Sync versions (`npm`/`yarn`/`pnpm`).

## Anti-Patterns

- **No Formatting Wars**: Adhere to Prettier rules.
- **No Untested Code**: Follow TDD and conduct post-code tests.
- **No Dirty Commits**: Lint before pushing code.

## Configuration

```javascript
// .eslintrc.js
module.exports = {
  extends: ['eslint:recommended', 'prettier'],
  rules: { 'no-console': 'warn', 'prefer-const': 'error' },
};
```

```json
// .prettierrc
{ "semi": true, "singleQuote": true, "printWidth": 80 }
```

```javascript
// jest.config.js
export default {
  coverageThreshold: { global: { lines: 80 } },
};
```

## Reference & Examples

For testing patterns and CI/CD, refer to the relevant documentation.

## Related Topics

best-practices | language