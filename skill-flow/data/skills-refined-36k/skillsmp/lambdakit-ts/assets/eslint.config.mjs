import js from '@eslint/js';
import tsPlugin from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import prettierConfig from 'eslint-config-prettier/flat';
import checkFile from 'eslint-plugin-check-file';
import prettierPlugin from 'eslint-plugin-prettier';
import globals from 'globals';

const sharedPaddingLineConfig = [
  'error',
  {
    blankLine: 'always',
    prev: '*',
    next: [
      'class',
      'block',
      'block-like',
      'const',
      'return',
      'if',
      'case',
      'switch',
      'try',
      'throw',
      'expression',
      'while',
    ],
  },
];

export default [
  js.configs.recommended,
  {
    files: ['**/*.ts'],
    languageOptions: {
      parser: tsParser,
      parserOptions: { project: true, tsconfigRootDir: import.meta.dirname },
      globals: { ...globals.node },
    },
    plugins: { '@typescript-eslint': tsPlugin, prettier: prettierPlugin, 'check-file': checkFile },
    rules: {
      ...tsPlugin.configs.recommended.rules,
      ...tsPlugin.configs['recommended-type-checked'].rules,
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/no-unused-vars': 'error',
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-unsafe-assignment': 'warn',
      '@typescript-eslint/no-unsafe-return': 'warn',
      'no-undef': 'off',
      'no-console': 'warn',
      'check-file/filename-naming-convention': ['warn', { '**/*.{ts}': 'KEBAB_CASE' }],
      'check-file/folder-naming-convention': ['warn', { '**/**/': 'KEBAB_CASE' }],
      'padding-line-between-statements': sharedPaddingLineConfig,
      '@typescript-eslint/require-await': 'warn',
      'prettier/prettier': 'error',
    },
  },
  prettierConfig,
  { ignores: ['**/dist/**', '**/node_modules/**', '.claude'] },
];
