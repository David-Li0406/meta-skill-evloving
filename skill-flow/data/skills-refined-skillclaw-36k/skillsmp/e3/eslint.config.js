import tseslint from '@typescript-eslint/eslint-plugin';
import tsparser from '@typescript-eslint/parser';
import headers from 'eslint-plugin-headers';

// BSL 1.1 packages: e3-core, e3-cli, e3-api-client, e3-api-server
const bslHeader = 'Copyright (c) 2025 Elara AI Pty Ltd\nLicensed under BSL 1.1. See LICENSE for details.';

// Dual AGPL-3.0 / Commercial packages: e3, e3-types
const agplHeader = 'Copyright (c) 2025 Elara AI Pty Ltd\nDual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.';

const bslPackages = ['e3-core', 'e3-cli', 'e3-api-client', 'e3-api-server'];
const agplPackages = ['e3', 'e3-types'];

const baseRules = {
  ...tseslint.configs.recommended.rules,
  '@typescript-eslint/no-explicit-any': 'off',
  '@typescript-eslint/no-unused-vars': ['error', { 'argsIgnorePattern': '^_', 'varsIgnorePattern': '^_' }],
  '@typescript-eslint/explicit-function-return-type': 'off',
  '@typescript-eslint/no-unnecessary-type-constraint': 'off',
  '@typescript-eslint/no-floating-promises': 'error',
  '@typescript-eslint/require-await': 'error',
  '@typescript-eslint/no-misused-promises': 'error',
};

const testRules = {
  ...tseslint.configs.recommended.rules,
  '@typescript-eslint/no-explicit-any': 'off',
  '@typescript-eslint/no-unused-vars': ['warn', { 'argsIgnorePattern': '^_', 'varsIgnorePattern': '^_' }],
  '@typescript-eslint/explicit-function-return-type': 'off',
  '@typescript-eslint/no-unnecessary-type-constraint': 'off',
  '@typescript-eslint/no-floating-promises': 'off',
  '@typescript-eslint/require-await': 'off',
  '@typescript-eslint/no-misused-promises': 'off',
  'no-console': 'off',
};

export default [
  {
    ignores: ['**/dist/**', '**/node_modules/**', '**/coverage/**']
  },
  // BSL 1.1 packages - source files
  ...bslPackages.map(pkg => ({
    files: [`packages/${pkg}/src/**/*.ts`],
    ignores: ['**/*.spec.ts'],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        project: true
      }
    },
    plugins: {
      '@typescript-eslint': tseslint,
      'headers': headers
    },
    rules: {
      ...baseRules,
      'headers/header-format': ['error', {
        source: 'string',
        content: bslHeader
      }]
    }
  })),
  // BSL 1.1 packages - test files
  ...bslPackages.map(pkg => ({
    files: [`packages/${pkg}/src/**/*.spec.ts`],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        project: true
      }
    },
    plugins: {
      '@typescript-eslint': tseslint,
      'headers': headers
    },
    rules: {
      ...testRules,
      'headers/header-format': ['error', {
        source: 'string',
        content: bslHeader
      }]
    }
  })),
  // AGPL packages - source files
  ...agplPackages.map(pkg => ({
    files: [`packages/${pkg}/src/**/*.ts`],
    ignores: ['**/*.spec.ts'],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        project: true
      }
    },
    plugins: {
      '@typescript-eslint': tseslint,
      'headers': headers
    },
    rules: {
      ...baseRules,
      'headers/header-format': ['error', {
        source: 'string',
        content: agplHeader
      }]
    }
  })),
  // AGPL packages - test files
  ...agplPackages.map(pkg => ({
    files: [`packages/${pkg}/src/**/*.spec.ts`],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        project: true
      }
    },
    plugins: {
      '@typescript-eslint': tseslint,
      'headers': headers
    },
    rules: {
      ...testRules,
      'headers/header-format': ['error', {
        source: 'string',
        content: agplHeader
      }]
    }
  })),
  // Integration tests (BSL 1.1)
  {
    files: ['test/integration/src/**/*.ts'],
    ignores: ['**/*.spec.ts'],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        project: true
      }
    },
    plugins: {
      '@typescript-eslint': tseslint,
      'headers': headers
    },
    rules: {
      ...baseRules,
      'headers/header-format': ['error', {
        source: 'string',
        content: bslHeader
      }]
    }
  },
  {
    files: ['test/integration/src/**/*.spec.ts'],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        project: true
      }
    },
    plugins: {
      '@typescript-eslint': tseslint,
      'headers': headers
    },
    rules: {
      ...testRules,
      'headers/header-format': ['error', {
        source: 'string',
        content: bslHeader
      }]
    }
  },
  // Fuzz tests (BSL 1.1)
  {
    files: ['test/fuzz/**/*.ts'],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        project: true
      }
    },
    plugins: {
      '@typescript-eslint': tseslint,
      'headers': headers
    },
    rules: {
      ...testRules,
      'headers/header-format': ['error', {
        source: 'string',
        content: bslHeader
      }]
    }
  }
];
