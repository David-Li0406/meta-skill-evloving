---
name: javascript-tooling
description: Use this skill when you need to set up essential development tools, linting, and testing for JavaScript projects.
---

# JavaScript Tooling

## **Priority: P1 (OPERATIONAL)**

Essential tooling for JavaScript development.

## Implementation Guidelines

- **Linting**: Use ESLint with Prettier. Configure to fix issues on save.
- **Formatting**: Apply Prettier formatting on save and before commits.
- **Testing**: Utilize Jest or Vitest for testing. Ensure tests are co-located with code and maintain over 80% coverage.
- **Build**: Use Vite for applications and Rollup for libraries.
- **Package Manager**: Keep package versions in sync using npm, yarn, or pnpm.

## Anti-Patterns

- **No Formatting Wars**: Adhere to Prettier rules to avoid conflicts.
- **No Untested Code**: Follow Test-Driven Development (TDD) and conduct post-code tests.
- **No Dirty Commits**: Ensure code is linted before pushing to the repository.

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