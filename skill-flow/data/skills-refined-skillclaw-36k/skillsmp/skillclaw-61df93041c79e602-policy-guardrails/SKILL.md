---
name: policy-guardrails
description: Use this skill when implementing lint rules, policy enforcement, and automated guardrails for various integrations, ensuring code quality and security best practices.
---

# Policy Guardrails

## Overview
Automated policy enforcement and guardrails for integrations with various platforms.

## Prerequisites
- ESLint configured in the project
- Pre-commit hooks infrastructure
- CI/CD pipeline with policy checks
- TypeScript for type enforcement

## ESLint Rules

### Custom Plugin Example
```javascript
// eslint-plugin-{platform}/rules/no-hardcoded-keys.js
module.exports = {
  meta: {
    type: 'problem',
    docs: {
      description: 'Disallow hardcoded API keys',
    },
    fixable: 'code',
  },
  create(context) {
    return {
      Literal(node) {
        if (typeof node.value === 'string') {
          if (node.value.match(/^sk_(live|test)_[a-zA-Z0-9]{24,}/)) {
            context.report({
              node,
              message: 'Hardcoded API key detected',
            });
          }
        }
      },
    };
  },
};
```

### ESLint Configuration
```javascript
// .eslintrc.js
module.exports = {
  plugins: ['{platform}'],
  rules: {
    '{platform}/no-hardcoded-keys': 'error',
    '{platform}/require-error-handling': 'warn',
    '{platform}/use-typed-client': 'warn',
  },
};
```

## Pre-Commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: {platform}-secrets-check
        name: Check for {platform} secrets
        entry: bash -c 'git diff --cached --name-only | xargs grep -l "sk_live_" && exit 1 || exit 0'
        language: system
        pass_filenames: false

      - id: {platform}-config-validate
        name: Validate {platform} configuration
        entry: node scripts/validate-{platform}-config.js
        language: node
        files: '\.{platform}\.json$'
```

## TypeScript Strict Patterns

```typescript
// Enforce typed configuration
interface {Platform}StrictConfig {
  apiKey: string;  // Required
  environment: 'development' | 'staging' | 'production';  // Enum
  timeout: number;  // Required number, not optional
  retries: number;
}

// Disallow any in {platform} code
// @ts-expect-error - Using any is forbidden
const client = new Client({ apiKey: any });
```

## Output
- ESLint plugin with platform-specific rules
- Pre-commit hooks blocking secrets
- CI policy checks passing
- Runtime guardrails active

## Error Handling
Refer to the documentation for comprehensive error handling strategies.

## Examples
See the documentation for detailed examples and best practices.

## Resources
- [ESLint Plugin Development](https://eslint.org/docs/latest/extend/plugins)
- [Pre-commit Framework](https://pre-commit.com/)
- [Open Policy Agent](https://www.openpolicyagent.org/)