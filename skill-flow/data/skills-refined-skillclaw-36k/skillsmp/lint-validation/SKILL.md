---
name: lint-validation
description: Standards for code linting, formatting, and pre-commit hooks.
---

# Lint & Validation

## When to use this skill
- Setting up a new project's CI/CD or git hooks.
- Configuring ESLint, Prettier, PHP CodeSniffer, or Ruff.
- Fixing lint errors.

## 1. PHP
- **Tools**: `PHP_CodeSniffer` (PSR-12) or `Laravel Pint`.
- **Command**: `composer lint` (custom script) or `./vendor/bin/pint`.
- **Static Analysis**: `PHPStan` (Level 5+) is recommended for logic errors.

## 2. JavaScript / TypeScript
- **Tools**: `ESLint` + `Prettier`.
- **Config**: Use strict configs (`eslint:recommended`, `plugin:@typescript-eslint/recommended`).
- **Imports**: Enforce sorted imports via `eslint-plugin-simple-import-sort`.

## 3. Python
- **Tools**: `Ruff` (replaces Flake8/Black/Isort).
- **Config**: Enable standard rules (E, F, I for imports).

## 4. Git Hooks
- **Husky**: Use Husky to run linters on `pre-commit`.
- **Strategy**: Lint only staged files (`lint-staged`) to keep commits fast.
