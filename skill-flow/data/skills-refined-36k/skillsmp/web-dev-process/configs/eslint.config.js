/**
 * ESLint Flat Config - Configuration standard
 *
 * Ce fichier utilise le nouveau format "flat config" d'ESLint (v9+).
 * Adaptez les plugins selon votre stack technologique.
 *
 * @see https://eslint.org/docs/latest/use/configure/configuration-files-new
 */

import js from '@eslint/js';
import globals from 'globals';

/** @type {import('eslint').Linter.Config[]} */
export default [
  // Configuration de base JavaScript
  js.configs.recommended,

  // Fichiers ignorés globalement
  {
    ignores: [
      '**/node_modules/**',
      '**/dist/**',
      '**/build/**',
      '**/.next/**',
      '**/.nuxt/**',
      '**/coverage/**',
      '**/*.min.js',
      '**/vendor/**',
    ],
  },

  // Configuration pour tous les fichiers JS/TS
  {
    files: ['**/*.{js,mjs,cjs,jsx,ts,tsx}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2024,
      },
    },
    rules: {
      // ===== Qualité du code =====
      'no-unused-vars': ['error', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
        caughtErrorsIgnorePattern: '^_',
      }],
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'no-debugger': 'error',
      'no-alert': 'warn',

      // ===== Bonnes pratiques =====
      'eqeqeq': ['error', 'always', { null: 'ignore' }],
      'curly': ['error', 'all'],
      'no-var': 'error',
      'prefer-const': 'error',
      'prefer-arrow-callback': 'error',
      'prefer-template': 'error',
      'no-param-reassign': ['error', { props: false }],
      'no-nested-ternary': 'error',
      'no-unneeded-ternary': 'error',

      // ===== Style =====
      'arrow-body-style': ['error', 'as-needed'],
      'object-shorthand': ['error', 'always'],
      'quote-props': ['error', 'as-needed'],
      'prefer-destructuring': ['error', {
        array: false,
        object: true,
      }],

      // ===== Async =====
      'no-await-in-loop': 'warn',
      'no-return-await': 'error',
      'prefer-promise-reject-errors': 'error',

      // ===== Imports =====
      'no-duplicate-imports': 'error',
      'sort-imports': ['error', {
        ignoreCase: true,
        ignoreDeclarationSort: true,
      }],
    },
  },

  // Configuration spécifique pour les tests
  {
    files: ['**/*.test.{js,ts,jsx,tsx}', '**/*.spec.{js,ts,jsx,tsx}', '**/tests/**/*'],
    languageOptions: {
      globals: {
        ...globals.jest,
        ...globals.vitest,
      },
    },
    rules: {
      'no-console': 'off',
    },
  },

  // Configuration spécifique pour les fichiers de config
  {
    files: ['*.config.{js,mjs,cjs,ts}', '.*rc.{js,mjs,cjs}'],
    rules: {
      'no-console': 'off',
    },
  },
];

/**
 * EXTENSIONS RECOMMANDÉES PAR STACK
 *
 * TypeScript:
 * - typescript-eslint
 * - @typescript-eslint/parser
 *
 * React:
 * - eslint-plugin-react
 * - eslint-plugin-react-hooks
 * - eslint-plugin-jsx-a11y
 *
 * Vue:
 * - eslint-plugin-vue
 * - vue-eslint-parser
 *
 * Node.js:
 * - eslint-plugin-n
 * - eslint-plugin-security
 *
 * Testing:
 * - eslint-plugin-jest ou eslint-plugin-vitest
 * - eslint-plugin-testing-library
 */
