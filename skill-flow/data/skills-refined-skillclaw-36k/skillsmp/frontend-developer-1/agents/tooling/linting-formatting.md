---
name: Linting & Formatting Expert
description: Expert en qualité de code - ESLint, Prettier, Stylelint, règles et configuration
workflows:
  - id: lint-setup
    template: wf-creation
    phase: Brief
    name: Setup linting/formatting
    duration: 0.5 jour
  - id: lint-audit
    template: wf-audit
    phase: Analyse
    name: Audit qualité code
    duration: 0.5-1 jour
---

# Agent Linting & Formatting

## Responsabilité

Configurer et maintenir les outils de qualité de code.

## Tu NE fais PAS

- ❌ Écrire le code applicatif (features, composants) → `javascript/` ou `frameworks/`
- ❌ Configurer le build (Vite, Webpack) → `build-tools.md`
- ❌ Configurer les tests (Jest, Vitest) → `testing/`
- ❌ Faire la code review manuelle → skill `lead-dev`

## ESLint (Configuration Flat)

### Configuration moderne (ESLint 9+)

```javascript
// eslint.config.js
import js from '@eslint/js';
import typescript from '@typescript-eslint/eslint-plugin';
import typescriptParser from '@typescript-eslint/parser';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import prettier from 'eslint-config-prettier';

export default [
  js.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      parser: typescriptParser,
      parserOptions: {
        project: './tsconfig.json',
      },
    },
    plugins: {
      '@typescript-eslint': typescript,
      react,
      'react-hooks': reactHooks,
      'jsx-a11y': jsxA11y,
    },
    rules: {
      // TypeScript
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/no-explicit-any': 'warn',

      // React
      'react/react-in-jsx-scope': 'off',
      'react/prop-types': 'off',
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',

      // Accessibilité
      'jsx-a11y/alt-text': 'error',
      'jsx-a11y/anchor-has-content': 'error',

      // Général
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'prefer-const': 'error',
      'no-unused-expressions': 'error',
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
  },
  prettier, // Désactive les règles en conflit avec Prettier
];
```

### Configuration legacy (.eslintrc)

```json
{
  "root": true,
  "env": {
    "browser": true,
    "es2022": true,
    "node": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "plugin:jsx-a11y/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "plugins": [
    "@typescript-eslint",
    "react",
    "react-hooks",
    "jsx-a11y"
  ],
  "rules": {
    "react/react-in-jsx-scope": "off",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "no-console": ["warn", { "allow": ["warn", "error"] }]
  },
  "settings": {
    "react": {
      "version": "detect"
    }
  }
}
```

## Prettier

### Configuration

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "always",
  "endOfLine": "lf",
  "jsxSingleQuote": false,
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

```
// .prettierignore
dist
build
coverage
node_modules
*.min.js
pnpm-lock.yaml
```

## Stylelint

```json
// .stylelintrc.json
{
  "extends": [
    "stylelint-config-standard",
    "stylelint-config-css-modules"
  ],
  "plugins": [
    "stylelint-order"
  ],
  "rules": {
    "declaration-block-no-duplicate-properties": true,
    "no-descending-specificity": null,
    "order/properties-alphabetical-order": true,
    "selector-class-pattern": [
      "^[a-z][a-zA-Z0-9]*$",
      {
        "message": "Use camelCase for class names"
      }
    ]
  }
}
```

## Husky + lint-staged

### Installation

```bash
npx husky init
npm install -D lint-staged
```

### Configuration

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{css,scss}": [
      "stylelint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
npx lint-staged
```

### Commit lint

```bash
npm install -D @commitlint/cli @commitlint/config-conventional
```

```javascript
// commitlint.config.js
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'chore',
        'revert',
      ],
    ],
    'subject-case': [2, 'never', ['start-case', 'pascal-case', 'upper-case']],
  },
};
```

```bash
# .husky/commit-msg
npx --no -- commitlint --edit $1
```

## Biome (Alternative)

```json
// biome.json
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
        "noForEach": "warn"
      },
      "style": {
        "noNonNullAssertion": "warn"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "always"
    }
  }
}
```

## Intégration VS Code

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ]
}
```

```json
// .vscode/extensions.json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "stylelint.vscode-stylelint"
  ]
}
```

## Mots-clés de routage

`ESLint`, `Prettier`, `Stylelint`, `linting`, `formatting`, `règles`, `husky`, `lint-staged`, `commitlint`, `Biome`

## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration ESLint | eslint.config.js avec règles adaptées au projet |
| Configuration Prettier | .prettierrc avec formatage standardisé |
| Setup Git hooks | Husky + lint-staged pour validation pre-commit |
