---
name: code-quality
description: Run code quality checks for Laravel Spectrum (PHPStan, Laravel Pint, PHPUnit). Use when user mentions "lint", "format", "code quality", "PR準備", "コミット前チェック", or before creating commits/PRs. Also use after writing significant code changes.
---

# Code Quality

## Quick Start

Run all checks in order:

```bash
composer format:fix && composer analyze && composer test
```

## Workflow

Execute checks in this order. Fix issues at each step before proceeding.

### 1. Format (Laravel Pint)

```bash
composer format:fix    # Auto-fix code style
composer format        # Dry-run (check only)
```

### 2. Analyze (PHPStan Level 5)

```bash
composer analyze
```

No baseline additions allowed. Fix all reported issues.

### 3. Test (PHPUnit)

```bash
composer test                                    # All tests
vendor/bin/phpunit tests/Unit/SomeTest.php       # Specific file
vendor/bin/phpunit --filter testMethodName       # Specific method
composer test-coverage                           # With coverage report
```

## Pre-PR Checklist

1. `composer format:fix` - Fix code style
2. `composer analyze` - Pass static analysis (no new errors)
3. `composer test` - All tests pass
4. Verify in demo-app:
   ```bash
   cd demo-app/laravel-12-app
   php artisan spectrum:generate
   ```

## Common Issues

### PHPStan Errors

- Add proper type hints to method parameters and return types
- Use `@var` annotations for complex types
- Check for null safety issues

### Pint Violations

Usually auto-fixed. If manual fix needed, check Laravel preset rules.

### Test Failures

- Run specific test: `vendor/bin/phpunit --filter testName`
- Check test fixtures in `tests/Fixtures/`
