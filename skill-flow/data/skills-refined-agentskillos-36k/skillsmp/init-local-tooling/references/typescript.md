# TypeScript Tooling

## Choosing Your Tooling Approach

### ESLint + Prettier (Traditional)

**Pros:**
- Highly configurable and extensible
- Large ecosystem of plugins
- Industry standard, widely adopted
- Separate concerns (linting vs formatting)

**Cons:**
- Slower than Biome
- Requires configuring multiple tools
- Can have conflicts between ESLint and Prettier

**When to use:**
- Enterprise projects with specific style requirements
- Projects with existing ESLint configs
- Need specific ESLint plugins (React, Vue, etc.)

### Biome (Modern All-in-One)

**Pros:**
- Extremely fast (written in Rust)
- Single tool for linting + formatting
- Opinionated defaults
- Drop-in Prettier replacement
- No conflicts between tools

**Cons:**
- Less configurable
- Smaller plugin ecosystem
- Newer tool, less battle-tested
- Some ESLint rules not yet implemented

**When to use:**
- New greenfield projects
- Want maximum speed
- Prefer opinionated defaults
- Monorepos (especially with Biome + Nx)

---

## ESLint + Prettier Setup

### Installation

**Local dev dependencies (recommended):**
```bash
npm install -D eslint @eslint/js typescript-eslint prettier eslint-config-prettier eslint-plugin-prettier
```

**Verify installation:**
```bash
npx eslint --version
npx prettier --version
```

### ESLint Configuration (Flat Config)

**eslint.config.js:**
```js
import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import prettierConfig from 'eslint-config-prettier'

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  prettierConfig,
  {
    languageOptions: {
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      // Customizations
      '@typescript-eslint/no-unused-vars': ['error', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_'
      }],
      '@typescript-eslint/consistent-type-imports': 'error',
      '@typescript-eslint/no-explicit-any': 'error',
    },
  },
  {
    ignores: ['dist/', 'build/', 'node_modules/', '*.config.js'],
  }
)
```

**With React:**
```bash
npm install -D eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y
```

```js
import react from 'eslint-plugin-react'
import reactHooks from 'eslint-plugin-react-hooks'
import jsxA11y from 'eslint-plugin-jsx-a11y'

export default tseslint.config(
  // ... previous config
  react.configs.flat.recommended,
  {
    plugins: {
      'react-hooks': reactHooks,
      'jsx-a11y': jsxA11y,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      ...jsxA11y.configs.recommended.rules,
      'react/react-in-jsx-scope': 'off', // Not needed in React 17+
      'react/prop-types': 'off', // Using TypeScript
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
  }
)
```

### Prettier Configuration

**.prettierrc.json:**
```json
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "avoid"
}
```

**.prettierignore:**
```
dist/
build/
coverage/
node_modules/
*.min.js
pnpm-lock.yaml
package-lock.json
```

### TypeScript Configuration

**tsconfig.json (Strict):**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022"],
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowJs": false,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts"]
}
```

**For libraries (additional options):**
```json
{
  "compilerOptions": {
    "composite": true,
    "declarationMap": true,
    "stripInternal": true
  }
}
```

### Package.json Scripts

```json
{
  "scripts": {
    "lint": "eslint . --max-warnings 0",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "type-check": "tsc --noEmit",
    "validate": "npm run type-check && npm run lint && npm run format:check"
  }
}
```

---

## Biome Setup

### Installation

**Local dev dependencies:**
```bash
npm install -D @biomejs/biome
```

**Verify:**
```bash
npx biome --version
```

### Biome Configuration

**biome.json:**
```json
{
  "$schema": "https://biomejs.dev/schemas/1.5.3/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": {
        "noExtraBooleanCast": "error",
        "noMultipleSpacesInRegularExpressionLiterals": "error",
        "noUselessCatch": "error",
        "noWith": "error"
      },
      "correctness": {
        "noUnusedVariables": "error",
        "useExhaustiveDependencies": "warn"
      },
      "style": {
        "noNegationElse": "off",
        "useImportType": "error",
        "useNodejsImportProtocol": "error"
      },
      "suspicious": {
        "noExplicitAny": "error",
        "noExtraNonNullAssertion": "error",
        "noMisleadingInstantiator": "error",
        "noUnsafeDeclarationMerging": "error"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "formatWithErrors": false,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100,
    "lineEnding": "lf"
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingComma": "es5",
      "semicolons": "asNeeded",
      "arrowParentheses": "asNeeded"
    }
  },
  "json": {
    "formatter": {
      "enabled": true
    }
  },
  "files": {
    "ignore": [
      "dist",
      "build",
      "coverage",
      "node_modules",
      "*.min.js"
    ]
  }
}
```

### Package.json Scripts (Biome)

```json
{
  "scripts": {
    "lint": "biome lint .",
    "lint:fix": "biome lint --apply .",
    "format": "biome format --write .",
    "format:check": "biome format .",
    "check": "biome check .",
    "check:fix": "biome check --apply .",
    "type-check": "tsc --noEmit",
    "validate": "npm run type-check && npm run check"
  }
}
```

**Note:** `biome check` runs both linting and formatting.

---

## Testing

### Vitest (Recommended for modern projects)

**Installation:**
```bash
npm install -D vitest @vitest/ui
```

**vitest.config.ts:**
```ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.config.{js,ts}',
        '**/*.d.ts',
      ],
    },
  },
})
```

**Package.json:**
```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

**Example test:**
```ts
import { describe, it, expect } from 'vitest'

describe('example', () => {
  it('should work', () => {
    expect(1 + 1).toBe(2)
  })
})
```

### Jest (Traditional)

**Installation:**
```bash
npm install -D jest ts-jest @types/jest
```

**jest.config.js:**
```js
export default {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/*.spec.ts',
  ],
  coverageThresholds: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
}
```

---

## Running on Staged Files (Pre-commit)

### With lint-staged

**Installation:**
```bash
npm install -D lint-staged
```

**ESLint + Prettier:**
```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

**Biome:**
```json
{
  "lint-staged": {
    "*.{ts,tsx,json}": [
      "biome check --apply --no-errors-on-unmatched"
    ]
  }
}
```

---

## Monorepo Considerations

### Project References

For TypeScript monorepos, use project references:

**packages/pkg-a/tsconfig.json:**
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "composite": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"],
  "references": []
}
```

**packages/pkg-b/tsconfig.json:**
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "composite": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"],
  "references": [
    { "path": "../pkg-a" }
  ]
}
```

**Root tsconfig.json:**
```json
{
  "files": [],
  "references": [
    { "path": "./packages/pkg-a" },
    { "path": "./packages/pkg-b" }
  ]
}
```

### Shared Configs

**@repo/eslint-config/package.json:**
```json
{
  "name": "@repo/eslint-config",
  "version": "0.0.0",
  "private": true,
  "main": "index.js"
}
```

**@repo/eslint-config/index.js:**
```js
import js from '@eslint/js'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended
)
```

**In consuming packages:**
```js
import baseConfig from '@repo/eslint-config'

export default [
  ...baseConfig,
  // Package-specific overrides
]
```

---

## Common Issues

### ESLint + Prettier Conflicts

If ESLint and Prettier fight over formatting:

1. Ensure `eslint-config-prettier` is **last** in extends
2. Use `eslint-plugin-prettier` to run Prettier as an ESLint rule
3. Or run them separately and use `lint-staged` to orchestrate

### TypeScript Performance

For large projects:

1. Use `skipLibCheck: true` in tsconfig.json
2. Enable `incremental` compilation
3. Use project references for monorepos
4. Consider `tsc --build` for monorepos

### Biome Migration from ESLint

```bash
# Check compatibility
npx @biomejs/biome migrate --write

# Review changes
git diff biome.json
```

Not all ESLint rules have Biome equivalents. Check compatibility docs.

---

## Quick Reference

**ESLint + Prettier:**
```bash
npm install -D eslint @eslint/js typescript-eslint prettier eslint-config-prettier
```

**Biome:**
```bash
npm install -D @biomejs/biome
```

**Testing:**
```bash
npm install -D vitest @vitest/ui  # Modern
npm install -D jest ts-jest       # Traditional
```

**Commands:**
```bash
# ESLint + Prettier
npx eslint . --fix
npx prettier --write .
npx tsc --noEmit

# Biome
npx biome check --apply .
npx tsc --noEmit

# Testing
npx vitest
npx jest
```
