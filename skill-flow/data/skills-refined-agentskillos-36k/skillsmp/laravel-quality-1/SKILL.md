---
name: laravel-quality
description: Run comprehensive quality checks including Pint formatting, PHPStan analysis, and Pest tests. Use this before commits, after major changes, or when requested by user.
allowed-tools: Bash,Read
---

# Laravel Quality Checks

Run unified quality assurance workflow before committing code or finalizing features.

## Quality Gate Workflow

### 1. Code Formatting (Pint)

**Check formatting:**
```bash
vendor/bin/pint --test
```

**Auto-fix formatting:**
```bash
vendor/bin/pint --dirty
```

**What it checks:**
- PSR-12 code style compliance
- Laravel-specific conventions
- Consistent spacing and indentation
- Import statement organization

### 2. Static Analysis (Optional - if PHPStan configured)

**Run PHPStan:**
```bash
vendor/bin/phpstan analyse --memory-limit=2G
```

**What it checks:**
- Type errors and mismatches
- Undefined methods/properties
- Dead code detection
- Laravel-specific patterns

### 3. Test Suite (Pest)

**Run specific tests:**
```bash
php artisan test --filter=[TestName]
```

**Run all tests:**
```bash
php artisan test
```

**Run with parallel execution:**
```bash
php artisan test --parallel
```

**What it checks:**
- Feature tests (HTTP endpoints, user flows)
- Unit tests (isolated logic)
- Browser tests (Pest v4 UI testing)
- Database integrity
- Livewire component behavior

### 4. Frontend Checks (if applicable)

**Check if frontend needs building:**
```bash
npm run build
```

**Or ask user to run:**
- `npm run dev` for development
- `composer run dev` if configured

## Recommended Workflow

### Before Every Commit
1. ✅ Run Pint: `vendor/bin/pint --dirty`
2. ✅ Run related tests: `php artisan test --filter=[Feature]`

### Before Pull Requests
1. ✅ Run Pint: `vendor/bin/pint --dirty`
2. ✅ Run full test suite: `php artisan test`
3. ✅ Run PHPStan (if configured): `vendor/bin/phpstan analyse`
4. ✅ Check for N+1 queries in browser (Laravel Debugbar)

### After Major Feature Work
1. ✅ Run Pint: `vendor/bin/pint --dirty`
2. ✅ Run feature tests: `php artisan test tests/Feature/[Feature]Test.php`
3. ✅ Run full test suite: `php artisan test`
4. ✅ Manual smoke test in browser
5. ✅ Check Laravel logs: `tail -n 50 storage/logs/laravel.log`

## Quality Checklist

Before marking work complete, verify:

- [ ] **Pint passes:** No formatting violations
- [ ] **Tests pass:** All relevant tests green
- [ ] **No N+1 queries:** Checked with Debugbar or tests
- [ ] **No errors in logs:** `storage/logs/laravel.log` is clean
- [ ] **Frontend builds:** Assets compile without errors
- [ ] **Browser console clean:** No JavaScript errors (use browser-logs tool)
- [ ] **PHPStan clean:** No type errors (if configured)

## Common Issues

### Pint Failures
**Fix automatically:**
```bash
vendor/bin/pint --dirty
```

Most violations are auto-fixable. Review changes before committing.

### Test Failures
**Debug failing test:**
```bash
php artisan test --filter=[FailingTest]
```

**Common causes:**
- Database not in expected state (use `RefreshDatabase` trait)
- Missing model factories or relationships
- Validation rules changed
- Authorization logic issues
- Livewire component state problems

### PHPStan Issues
**Common violations:**
- Missing return type declarations
- Undefined properties on models (add PHPDoc)
- Incorrect type hints
- Dead code that should be removed

**Fix pattern:**
```php
// ❌ PHPStan error: Missing return type
public function getPosts()
{
    return $this->posts;
}

// ✅ Fixed with return type
public function getPosts(): Collection
{
    return $this->posts;
}
```

### Frontend Build Errors
**Check Vite config:**
```bash
cat vite.config.js
```

**Common fixes:**
- Run `npm install` to update dependencies
- Clear Vite cache: `rm -rf node_modules/.vite`
- Ask user to run `npm run dev`

## Integration with TodoWrite

When running quality checks as part of feature work, update todos:

```
1. [completed] Implement feature
2. [in_progress] Run quality checks
3. [pending] Fix any issues found
4. [pending] Rerun checks to confirm
```

## Output

After running quality checks, report:

1. ✅ **Pint status:** Pass/Fail (with file count if auto-fixed)
2. ✅ **Test status:** X/Y tests passing (show failures if any)
3. ✅ **PHPStan status:** Pass/Fail (if configured)
4. ✅ **Action items:** What needs fixing (if anything)

Example output:
```
Quality Checks Complete:
✅ Pint: Auto-fixed 3 files
✅ Tests: 42/42 passing
✅ PHPStan: Not configured (skip)

All checks passed! Ready to commit.
```

## Important Reminders

- **ALWAYS** run Pint before committing: `vendor/bin/pint --dirty`
- **ALWAYS** run relevant tests, minimum: `php artisan test --filter=[Feature]`
- **NEVER** commit code with failing tests
- **NEVER** skip Pint (it's fast and auto-fixes issues)
- **NEVER** add dark mode support (light mode only)
- **NEVER** customize Flux UI component colors, typography, or borders (only padding/margins)
- **ASK** user if they want full test suite after feature tests pass
- **CHECK** browser console using `browser-logs` tool if UI issues
